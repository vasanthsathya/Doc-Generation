Upgrade Omnia
================
This section describes how to upgrade Omnia Core containers.

Upgrade omnia core container
----------------------------

Prerequisites
--------------

* Run the following command to retrieve the omnia.sh file for 2.1 version. ::

    wget https://raw.githubusercontent.com/dell/omnia/refs/heads/pub/q1_dev/omnia.sh

* Omnia 2.1 image must be available in the OIM. If the image is not available, run the following command to download the image. ::

    ./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev

* Ensure that Omnia 2.0 core container is running.
* Go to the same directory where the omnia.sh file for version 2.1 is located.

Omnia Configurations
--------------------

The following operations can be performed on the Omnia Core Containers: Version, upgrade, and rollback.

.. image:: images/omnia_configurations_list.png

View Omnia Version
------------------

To view the Omnia version, run the following command: ::
    
    ./omnia.sh --version

.. image:: images/omnia_output_version.png

Upgrade
^^^^^^^^

1. To view the versions to upgrade, run the following command: ::
    
    ./omnia.sh --upgrade

.. image:: images/omnia_upgrade_options.png

2. Select the relevant version and enter yes to backup the current version files.

3. The location of the backup files is displayed. A backup is created in the directory in the NFS share path. After the upgrade is successful, a message is displayed. The backup files are available in the directory ``/opt/omnia/backups/upgrade/input``.

.. image:: images/upgrade_successful.png

.. image:: images/upgrade_running.png

After successful upgrade, run ``upgrade_omnia.yml`` to complete the process.

The upgrade process runs inside the ``Omnia_core`` container.

The backup files are available in the directory ``/opt/omnia/backups/upgrade/input``.

Running playbooks other than the ``upgrade_omnia.yml`` before ``./omnia.sh --upgrade`` generates an error with instructions.

.. image:: images/upgrade_error_trigger.png

Choose one of the following options:

**Option 1: Migrate Input Files**

Run the ``upgrade_omnia.yml`` playbook. ::

    ansible-playbook /omnia/upgrade/upgrade_omnia.yml

The input files are migrated from 2.0 to 2.1 format.

The system displays guidance after successful migration completes.

.. image:: images/successful_input_migration.png

If any configuration files are missing from the backup, a warning is generated before reprovisioning is started.

.. image:: images/missing_config_files_warning.png

**Option 2: Skip Migration**

Manually reconfigure default input files, then remove the upgrade lock using the following command: ::

    rm /opt/omnia/.data/upgrade_in_progress.lock

Other playbooks are allowed to run normally.
