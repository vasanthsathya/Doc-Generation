

Deploy Additional Packages
==========================


Install custom software packages on provisioned cluster nodes using Ansible
ad-hoc commands, playbooks, or the Omnia local repository infrastructure..


Overview
--------


After initial cluster provisioning, you may need to install additional
packages on some or all nodes:

- Development tools (compilers, libraries)
- Scientific libraries (BLAS, LAPACK, FFTW)
- Monitoring agents
- Custom in-house software

This guide covers three approaches:

#. **Ansible ad-hoc commands** -- Quick one-off installations.
#. **Custom Ansible playbook** -- Repeatable, versioned package deployment.
#. **Local Pulp repository** -- Add custom RPMs to the Omnia repository
   infrastructure for automated deployment to new nodes.



Prerequisites
-------------


- Cluster nodes are provisioned and reachable via Ansible.
- The ``omnia_core`` container has SSH access to all target nodes.
- Local repositories are synced (see `Create Local Repos <../Setup/create_local_repos.rst>`_)
  if installing from OS repos.



Procedure
---------



Approach 1: Ansible Ad-Hoc Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Install a package on all compute nodes**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m dnf -a "name=htop state=present"



#. **Install multiple packages at once**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m dnf -a "name=gcc,gcc-c++,make,cmake state=present"



#. **Install on a specific group of nodes**:


**Run on: omnia_core container**

.. code-block:: bash
      # Install only on login nodes
      ansible login_node -m dnf -a "name=emacs,vim-enhanced state=present"



#. **Install from a specific repository**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m dnf -a "name=openmpi-devel enablerepo=epel state=present"





Approach 2: Custom Ansible Playbook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Create a custom playbook** for repeatable deployments:


**Run on: omnia_core container**

.. code-block:: bash
      cat <<'EOF' > /omnia/custom_packages.yml
      ---
      - name: Deploy custom packages to compute nodes
        hosts: slurm_node
        become: true
        tasks:
          - name: Install development tools
            dnf:
              name:
                - gcc
                - gcc-c++
                - gcc-gfortran
                - make
                - cmake
                - autoconf
                - automake
              state: present
   
          - name: Install scientific libraries
            dnf:
              name:
                - openblas-devel
                - lapack-devel
                - fftw-devel
                - hdf5-devel
              state: present
   
          - name: Install Python scientific stack
            pip:
              name:
                - numpy
                - scipy
                - matplotlib
                - pandas
              executable: pip3
   
          - name: Install monitoring tools
            dnf:
              name:
                - htop
                - iotop
                - sysstat
                - perf
              state: present
      EOF



#. **Run the custom playbook**:


**Run on: omnia_core container**

.. code-block:: bash
      cd /omnia
      ansible-playbook custom_packages.yml





Approach 3: Custom Pulp Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Add custom RPMs to Pulp** for automatic deployment to new nodes:


**Run on: omnia_core container**

.. code-block:: bash
      # Create a custom repository in Pulp
      pulp rpm repository create --name custom-packages
   
      # Upload custom RPMs
      pulp rpm content upload --file /path/to/custom-package.rpm --repository custom-packages
   
      # Create publication and distribution
      pulp rpm publication create --repository custom-packages
      pulp rpm distribution create --name custom-packages \
        --base-path custom-packages \
        --repository custom-packages



#. **Configure nodes to use the custom repository**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible all -m yum_repository -a "
        name=custom-packages
        description='Custom Omnia Packages'
        baseurl=http://<oim-ip>:8080/pulp/content/custom-packages/
        gpgcheck=0
        enabled=1
      "



#. **Install from the custom repository**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m dnf -a "name=custom-package state=present enablerepo=custom-packages"





Verification
------------


#. **Verify packages are installed**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m shell -a "rpm -q gcc cmake htop"



#. **Check package versions**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m shell -a "gcc --version | head -1"



#. **Verify Python packages**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m shell -a "pip3 list | grep numpy"



#. **Verify custom Pulp repository** is available:


**Run on: compute node**

.. code-block:: bash
      dnf repolist | grep custom-packages





Next Steps
----------


- `Use Apptainer <use_apptainer.rst>`_ -- Use containers for complex application stacks.
- `Run Hpc Benchmarks <../Slurm/run_hpc_benchmarks.rst>`_ -- Run benchmarks with the
  installed packages.



Troubleshooting
---------------


**"No package available" error**
   Verify the package name and check available repositories:


**Run on: compute node**

.. code-block:: bash
      dnf search <package-name>
      dnf repolist



**Package conflicts**
   Check for conflicting packages:


**Run on: compute node**

.. code-block:: bash
      dnf check



**Custom Pulp repository not accessible**
   Verify the distribution URL:


**Run on: compute node**

.. code-block:: bash
      curl -s http://<oim-ip>:8080/pulp/content/custom-packages/repodata/repomd.xml | head



**Pip install fails**
   Ensure pip and Python are installed:


**Run on: compute node**

.. code-block:: bash
      dnf install -y python3 python3-pip



**Ansible times out on large installations**
   Increase the Ansible timeout:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m dnf -a "name=large-package state=present" -e "ansible_timeout=600"

