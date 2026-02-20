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

Version
^^^^^^^^

To view the Omnia version, run the following command: ::
    
    ./omnia.sh --version

.. image:: images/upgrade_version.png

Upgrade
^^^^^^^

1. To view the upgrade options, run the following command: ::
    
    ./omnia.sh --upgrade

2. Select the relevant version.

3. To backup the current version files, enter yes. The location of the backup files is displayed. A backup is created in the directory in the NFS share path. After the upgrade is successful, a message is displayed. The backup files are available in the directory ``/opt/omnia/backups/upgrade/input``.

Post-Upgrade Status
-------------------

Upon successful completion of the upgrade process:

- You will be automatically placed inside the `omnia_core` container
- You can proceed with Step 2 of the upgrade process
- Backup files are available at `/opt/omnia/backups/upgrade/input`

**Important Note**: If you attempt to run any playbook other than `upgrade_omnia.yml` before proceeding to Step 2, you will encounter an error message with specific instructions on how to proceed.
