

Deploy omnia_core
=================


Install the ``omnia_core`` Podman container on your Omnia Infrastructure Manager
(OIM). The ``omnia_core`` container encapsulates the Ansible toolchain and all
Omnia playbooks, providing a reproducible and isolated control plane for cluster
management.


Overview
--------


The ``omnia_core`` deployment process consists of three stages:

#. **Clone** the Omnia repository from Dell's artifact repository.
#. **Build** the container images using the ``build_images.sh`` script.
#. **Install** the ``omnia_core`` service using ``omnia.sh --install``.


Once installed, ``omnia_core`` runs as a systemd-managed Podman container that
starts automatically on boot.



Prerequisites
-------------



.. list-table::
   :header-rows: 1
   :widths: auto

   * - Requirement
     - Details
   * - **Operating system**
     - RHEL 8.8+ / 9.2+ or Rocky Linux 8.x / 9.x on the OIM
   * - **RAM**
     - Minimum 64 GB (128 GB recommended for clusters > 100 nodes)
   * - **Disk**
     - Minimum 256 GB free (SSD recommended)
   * - **Network interfaces**
     - At least 2 NICs: one for the admin network, one for the BMC/iDRAC network
   * - **Podman**
     - Podman 4.x or later installed (``dnf install -y podman``)
   * - **Internet access**
     - Required to clone the repository and pull base container images
   * - **Git**
     - Git 2.x or later (``dnf install -y git``)






.. note::


   Ensure that SELinux is set to ``permissive`` or ``enforcing`` with the
   appropriate container policies. Disabling SELinux is **not recommended** in
   production environments.



Procedure
---------


#. **Log in to the OIM** as ``root`` or a user with ``sudo`` privileges:

   .. code-block:: bash
      :caption: Run on: OIM host

      ssh root@<oim-ip-address>



#. **Clone the Omnia repository** from Dell's artifact repository:

   .. code-block:: bash
      :caption: Run on: OIM host

      cd /opt
      git clone https://github.com/dell/omnia.git
      cd omnia



   !!! note

       To use a specific release, check out the corresponding tag:


.. code-block:: bash
   :caption: Run on: OIM host

          git checkout v2.1.0.0



#. **Build the container images** using the provided build script:

   .. code-block:: bash
      :caption: Run on: OIM host

      bash build_images.sh core



   This builds the ``omnia_core`` container image locally. The build process
   takes approximately 10-15 minutes depending on network speed and hardware.

#. **Install the omnia_core service**:

   .. code-block:: bash
      :caption: Run on: OIM host

      bash omnia.sh --install



   This script:

  - Creates the ``omnia_core`` Podman container.
  - Registers it as a systemd service (``omnia_core.service``).
  - Mounts the necessary volumes for configuration and playbook storage.
  - Starts the container automatically.


#. **Verify the service is running**:

   .. code-block:: bash
      :caption: Run on: OIM host

      systemctl status omnia_core.service



   Expected output:


**Expected output on: OIM host**

.. code-block:: text

      ● omnia_core.service - Omnia Core Container
           Loaded: loaded (/etc/systemd/system/omnia_core.service; enabled; vendor preset: disabled)
           Active: active (running) since ...





Verification
------------


#. **Check the container is running**:

   .. code-block:: bash
      :caption: Run on: OIM host

      podman ps --filter name=omnia_core



   You should see a running container named ``omnia_core``.

#. **Enter the omnia_core container** and verify Ansible is available:

   .. code-block:: bash
      :caption: Run on: OIM host

      podman exec -it -u root omnia_core bash




.. code-block:: bash
   :caption: Run on: omnia_core container

      ansible --version



#. **Verify playbooks are accessible**:

   .. code-block:: bash
      :caption: Run on: omnia_core container

      ls /omnia/*.yml



   You should see the key playbooks: ``omnia_startup.yml``,
   ``input_validator.yml``, ``credentials_utility.yml``, ``prepare_oim.yml``,
   ``local_repo.yml``, ``discovery.yml``, and others.

#. **Verify input directory exists**:

   .. code-block:: bash
      :caption: Run on: omnia_core container

      ls /opt/omnia/input/project_default/





Next Steps
----------


- :doc:`Create Mapping File <create_mapping_file>` -- Create the PXE mapping file for node discovery.
- :doc:`Configure Inputs <configure_inputs>` -- Configure Omnia input files.
- :doc:`Configure Credentials <configure_credentials>` -- Set up encrypted credentials.






Troubleshooting
---------------


**Container fails to start**
   Check the Podman logs for detailed error output:


.. code-block:: bash
   :caption: Run on: OIM host

      podman logs omnia_core



**systemd service not found**
   Re-run the installation script:


.. code-block:: bash
   :caption: Run on: OIM host

      bash omnia.sh --install



**Build fails with network errors**
   Ensure the OIM has internet access and DNS is configured correctly:


.. code-block:: bash
   :caption: Run on: OIM host

      ping -c 3 github.com
      cat /etc/resolv.conf



**Podman not installed**
   Install Podman from the default OS repositories:


.. code-block:: bash
   :caption: Run on: OIM host

      dnf install -y podman
      systemctl enable --now podman.socket



**Insufficient disk space**
   Check available disk space. At least 256 GB is required:


.. code-block:: bash
   :caption: Run on: OIM host

      df -h /opt

