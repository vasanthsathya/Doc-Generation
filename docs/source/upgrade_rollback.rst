Upgrade Omnia Core Containers
================================
This section describes how to upgrade Omnia Core containers.

Prerequisites
--------------

* Run the following command to retrieve the omnia.sh file for 2.1 version. ::

    wget https://raw.githubusercontent.com/dell/omnia/refs/heads/pub/q1_dev/omnia.sh

* Omnia 2.1 image must be available in the OIM. If the image is not available, run the following command to download the image. ::

    ./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev

* Ensure that Omnia 2.0 core container is running.
* Go to the same directory where the omnia.sh file for version 2.1 is located.

Omnia Configurations
-------------------

The following operations can be performed on the Omnia Core Containers: Version, upgrade, and rollback.

.. image:: images/omnia_configurations.png

View Omnia Version
^^^^^^^^^^^^^^^^^^^

To view the Omnia version, run the following command: ::
    
    ./omnia.sh --version

.. image:: images/upgrade_version.png

Upgrade to version 2.1
^^^^^^^^^^^^^^^^^^^^^^^

1. To view the versions to upgrade, run the following command: ::
    
    ./omnia.sh --upgrade

.. image:: images/upgrade_options.png

2. Select the relevant version and enter yes to backup the current version files.

3. The location of the backup files is displayed. A backup is created in the directory in the NFS share path. After the upgrade is successful, a message is displayed. The backup files are available in the directory ``/opt/omnia/backups/upgrade/input``.

.. image:: images/upgrade_successful.png

.. image:: images/upgrade_running.png

After successful upgrade, run upgrade_omnia.yml to complete the process.

Post-Upgrade Status
-------------------

After upgrade, you are placed inside the Omnia core container. Proceed to the next step.

Check backup files at ``/opt/omnia/backups/upgrade/input``.

Running playbooks other than the upgrade_omnia.yml command before ./omnia.sh --upgrade triggers an error with instructions.

.. image:: images/error_trigger.png

Post-Upgrade Options
--------------------

Choose one of two options:

**Option 1: Migrate Input Files**

Run the upgrade_omnia.yml playbook::

    ansible-playbook /omnia/upgrade/upgrade_omnia.yml

This migrates 2.0 input files to 2.1 format.

The system displays guidance after successful migration completes.

.. image:: images/successful_input_migration.png

**Note**: Cluster reprovision guidance requires updates.

Missing config files trigger warnings before reprovisioning begins.

.. image:: images/missing_config_files_warning.png

**Option 2: Skip Migration**

Manually reconfigure default input files, then remove the upgrade lock::

    rm /opt/omnia/.data/upgrade_in_progress.lock

This allows other playbooks to run normally.

Rollback to the previous version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To rollback to a previous version, run the following command::

    ./omnia.sh --rollback

Select version 2.0 and confirm to proceed. The system displays rollback success and important information.

.. image:: images/rollback_one.png
.. image:: images/rollback_two.png
.. image:: images/rollback_three.png

Post-Rollback Status
--------------------

Omnia 2.0 container runs with original inputs and configurations restored from backup.
