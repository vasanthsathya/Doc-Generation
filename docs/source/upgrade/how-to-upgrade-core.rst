.. _how-to-upgrade-core:

Upgrading Omnia Core Container from 2.0 to 2.1
================================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Upgrade your Omnia Infrastructure Manager (OIM) from version 2.0 to 2.1 by replacing the core container and preparing your environment for the new features. This procedure guides you through the complete upgrade process with built-in validation and rollback capabilities.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before beginning the upgrade:

* Ensure you have OIM-level administrator access on the control plane node
* Verify the current Omnia 2.0 core container is running and healthy
* Download the Omnia 2.1 shell script:

.. code-block:: bash

   wget https://raw.githubusercontent.com/dell/omnia/refs/heads/pub/q1_dev/omnia.sh

* Ensure the Omnia 2.1 core container image is available locally:

.. code-block:: bash

   ./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev

* Confirm network connectivity to Docker Hub for image pulling
* Verify at least 2 GB of free disk space for backup operations
* Plan for a 5-10 minute downtime window during the container swap

.. important::
   The ``omnia.sh`` script version must match your target Omnia version. Use the 2.1 version of the script to upgrade to Omnia 2.1.

Procedure
---------

#. Navigate to the directory containing the new ``omnia.sh`` file (version 2.1).

.. code-block:: bash

   cd /path/to/omnia_2.1_script

#. Verify the current Omnia version.

.. code-block:: bash

   ./omnia.sh --version

Expected output:

.. code-block:: text

   Omnia version: 2.0.0.0
   Core container: 1.0

#. Initiate the core container upgrade.

.. code-block:: bash

   ./omnia.sh --upgrade

#. Review the pre-upgrade validation results.

The system displays:
- Current Omnia version (2.0) and target version (2.1)
- Available upgrade options
- Validation results for prerequisites

If validation fails, address the reported issues before proceeding.

#. Review the upgrade information and backup destination.

The approval gate shows:
- New features available in Omnia 2.1
- Breaking changes and migration impacts
- Default backup destination: ``/opt/omnia/backups/upgrade_<timestamp>``
- Option to specify custom backup location

#. Confirm you want to proceed with the upgrade.

When prompted, enter ``y`` to continue or ``n`` to cancel:

.. code-block:: console

   Do you want to proceed with the upgrade? (y/N): y

.. warning::
   This action will stop the current Omnia core container and begin the upgrade process. Ensure you have a maintenance window available.

#. Wait for backup creation to complete.

The system automatically:
- Creates the timestamped backup directory
- Copies input files from ``/opt/omnia/input/``
- Backs up container configuration files
- Preserves ``oim_metadata.yml``
- Validates backup integrity

If backup creation fails, the upgrade stops and you must resolve the issue before retrying.

#. Monitor the container swap process.

The upgrade automatically:
- Stops the Omnia core 1.0 container gracefully
- Verifies the 1.0 container is stopped
- Starts the Omnia core 1.1 Quadlet unit
- Performs health checks on the new container
- Updates metadata with version information

If any step fails, the system initiates automatic rollback.

#. Verify the core container upgrade success.

After the container swap completes, the system displays:
- Upgrade success confirmation
- New version information
- Next steps for input file migration
- Rollback command availability

Result
------

The Omnia core container is now upgraded from version 1.0 to 1.1, running Omnia 2.1 code. Your original configurations are backed up and the system is prepared for input file migration.

Verification
------------

Verify the upgrade completed successfully:

#. Check the new Omnia version.

.. code-block:: bash

   ./omnia.sh --version

Expected output:

.. code-block:: text

   Omnia version: 2.1.0.0
   Core container: 1.1

#. Verify the new core container is running.

.. code-block:: bash

   podman ps | grep omnia-core

Expected output should show the omnia-core container with tag ``1.1``.

#. Confirm backup creation.

.. code-block:: bash

   ls -la /opt/omnia/backups/upgrade_*

Expected output shows a timestamped backup directory with your original files.

#. Access the new core container.

.. code-block:: bash

   podman exec -it omnia-core bash

You should now be inside the upgraded Omnia core container running version 2.1.

Next Steps
----------

After completing the core container upgrade:

#. **Migrate Input Files**: Run the input file migration process to transform your 2.0 configurations to 2.1 format. See :doc:`how-to-migrate-inputs`.

#. **Validate Cluster Operation**: Test your cluster functionality with the new core container.

#. **Plan Reprovisioning**: If you want to use new 2.1 features, plan for cluster reprovisioning.

#. **Monitor System Performance**: Observe system behavior and performance after the upgrade.

.. tip::
   Keep the backup directory available until you have verified that all systems are operating correctly with Omnia 2.1.

Troubleshooting
---------------

If issues occur during the upgrade:

* **Upgrade fails during validation**: Address the specific validation errors before retrying
* **Backup creation fails**: Verify disk space and permissions, then retry the upgrade
* **Container swap fails**: The system automatically initiates rollback, or you can manually run ``./omnia.sh --rollback``
* **Health check timeout**: Check system resources and network connectivity, then retry

For detailed troubleshooting guidance, see :doc:`../troubleshooting/upgrade-issues`.

Related Topics
--------------

* :doc:`concept-core-upgrade`
* :doc:`how-to-migrate-inputs`
* :doc:`how-to-rollback-upgrade`
* :doc:`../reference/cli/omnia-upgrade`
