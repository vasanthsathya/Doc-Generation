

Build Slurm Repository
======================


Build a custom Slurm RPM repository for use with Omnia's local repository
infrastructure. This is useful when you need a specific Slurm version or
custom build options.


Overview
--------


By default, Omnia installs Slurm from pre-built RPM packages in the local
Pulp repositories. If you need a specific Slurm version, custom compile
options, or patches, you can build Slurm RPMs from source and host them in a
local repository.



Prerequisites
-------------


- The :doc:`Create Local Repos <../Setup/create_local_repos>` procedure is complete (Pulp is
  running and base OS repos are synced).
- A build host with:

  - RHEL 8.x / 9.x or Rocky Linux matching your cluster OS
  - ``rpm-build``, ``rpmbuild``, and development tools installed
  - At least 10 GB free disk space

- Slurm source tarball (download from
  ``<https://www.schedmd.com/downloads.php>``_).



Procedure
---------


#. **Install build dependencies** on the build host:


**Run on: build host (OIM or dedicated build server)**

.. code-block:: bash

      dnf groupinstall -y "Development Tools"
      dnf install -y rpm-build munge-devel munge-libs pam-devel \
        perl-ExtUtils-MakeMaker readline-devel openssl-devel \
        mariadb-devel hwloc-devel lua-devel numactl-devel \
        http-parser-devel json-c-devel libcurl-devel



#. **Create the RPM build directory structure**:


**Run on: build host**

.. code-block:: bash

      mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}



#. **Download the Slurm source tarball**:


**Run on: build host**

.. code-block:: bash

      cd ~/rpmbuild/SOURCES
      wget https://download.schedmd.com/slurm/slurm-23.11.4.tar.bz2



   !!! note

       Replace the version number with your desired Slurm version.

#. **Extract the spec file**:


**Run on: build host**

.. code-block:: bash

      tar xjf slurm-23.11.4.tar.bz2 --strip-components=1 -C /tmp slurm-23.11.4/slurm.spec
      cp /tmp/slurm.spec ~/rpmbuild/SPECS/



#. **Build the RPMs**:


**Run on: build host**

.. code-block:: bash

      rpmbuild -ba ~/rpmbuild/SPECS/slurm.spec



   This process takes **10-30 minutes** depending on hardware. The resulting
   RPMs will be in ``~/rpmbuild/RPMS/x86_64/``.

#. **Create a local repository** from the built RPMs:


**Run on: build host**

.. code-block:: bash

      dnf install -y createrepo_c
      mkdir -p /opt/omnia/custom_repos/slurm
      cp ~/rpmbuild/RPMS/x86_64/slurm-*.rpm /opt/omnia/custom_repos/slurm/
      createrepo_c /opt/omnia/custom_repos/slurm/



#. **Upload to Pulp** (from the omnia_core container):


**Run on: omnia_core container**

.. code-block:: bash

      # Create a Pulp repository for custom Slurm RPMs
      pulp rpm repository create --name slurm-custom

      # Upload RPMs
      for rpm in /opt/omnia/custom_repos/slurm/*.rpm; do
        pulp rpm content upload --file "$rpm" --repository slurm-custom
      done

      # Create a publication and distribution
      pulp rpm publication create --repository slurm-custom
      pulp rpm distribution create --name slurm-custom \
        --base-path slurm-custom \
        --repository slurm-custom





Verification
------------


#. **List the custom repository contents**:


**Run on: build host**

.. code-block:: bash

      ls -la /opt/omnia/custom_repos/slurm/



#. **Verify the repository metadata**:


**Run on: build host**

.. code-block:: bash

      ls /opt/omnia/custom_repos/slurm/repodata/



   You should see ``repomd.xml`` and related files.

#. **Test package availability via Pulp**:


**Run on: OIM host**

.. code-block:: bash

      curl -s http://localhost:8080/pulp/content/slurm-custom/repodata/repomd.xml | head



#. **Verify RPM versions**:


**Run on: build host**

.. code-block:: bash

      rpm -qip ~/rpmbuild/RPMS/x86_64/slurm-23*.rpm | grep -E "^(Name|Version)"





Next Steps
----------


- :doc:`Setup Slurm <setup_slurm>` -- Deploy Slurm using the custom RPMs.
- :doc:`Create Local Repos <../Setup/create_local_repos>` -- Integrate the custom repo with
  Omnia's repo management.



Troubleshooting
---------------


**rpmbuild fails with missing dependency**
   Install the missing development package:


**Run on: build host**

.. code-block:: bash

      dnf install -y <missing-package>-devel



**Spec file not found in tarball**
   Download the spec file separately from SchedMD's GitHub:


**Run on: build host**

.. code-block:: bash

      wget -O ~/rpmbuild/SPECS/slurm.spec \
        https://raw.githubusercontent.com/SchedMD/slurm/slurm-23-11-4-1/slurm.spec



**createrepo_c fails**
   Ensure the package is installed:


**Run on: build host**

.. code-block:: bash

      dnf install -y createrepo_c



**Custom RPMs conflict with existing Slurm packages**
   Remove existing Slurm packages before installing custom ones:


**Run on: compute node**

.. code-block:: bash

      dnf remove -y slurm slurm-slurmd slurm-slurmctld
      dnf install -y --disablerepo='*' --enablerepo='slurm-custom' slurm slurm-slurmd

