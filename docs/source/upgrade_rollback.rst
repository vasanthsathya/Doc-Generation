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

.. image:: images/upgrade_options.png

2. Select the relevant version.

3. To backup the current version files, enter yes. The location of the backup files is displayed. A backup is created in the directory in the NFS share path. After the upgrade is successful, a message is displayed. The backup files are available in the directory ``/opt/omnia/backups/upgrade/input``.

.. image:: images/upgrade_successful.png

.. image:: images/upgrad_running_successfully.png

Once the upgrade is successful, a running upgrade_omnia.yml along with a success message is displayed.

Post-Upgrade Status
-------------------

Upon successful upgrade, user will be directly inside omnia_core container and now has to proceed for step2.

User can also be able to check backups present at the directory "/opt/omnia/backups/upgrade/input"

Before step2, if user runs any playbook other than upgrade_omnia.yml, he gets the below error with instructions:

Post-Upgrade Options
--------------------

Here, user has 2 options:

**Option 1: Proceed with Input File Migration**

Proceed with the 2nd upgrade step by running upgrade_omnia.yml using the following command::

    ansible-playbook /omnia/upgrade/upgrade_omnia.yml

This will migrate the 2.0 input files from backup to 2.1 format.

Above you can see the further guidance given to user after successful input migration (full upgrade) is done.

**Note**: Cluster reprovision guidance is to be still modified.

Also here, if any config files are missing from the backup, a warning is shown before reprovisioning guidance saying omnia execution might not be completed.

**Option 2: Skip Input File Migration**

Skip the input file migration from backup, reconfigure the default input files manually and then remove the upgrade lock using the following command::

    rm /opt/omnia/.data/upgrade_in_progress.lock

This will ensure that other playbooks run without any problem.

Rollback
^^^^^^^^

To rollback to a previous version, run the following command::

    ./omnia.sh --rollback

When this command is run, user is shown the available versions to rollback to and is prompted to select a version. User is then prompted yes/no to continue to rollback to that particular version. Then rollback successful is shown and user is given some important info.

Post-Rollback Status
--------------------

After rollback, omnia 2.0 container will run with the original inputs and configurations (restored from backup).

