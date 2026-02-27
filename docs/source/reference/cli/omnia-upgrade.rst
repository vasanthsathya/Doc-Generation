.. _ref-omnia-upgrade:

Omnia CLI Upgrade Commands
=========================

.. note::
   This topic is pending SME validation. Content may change before publication.

The Omnia 2.1 release introduces three new CLI commands for upgrade management, rollback operations, and version checking. These commands provide the primary interface for managing Omnia version transitions and monitoring system state.

.. contents:: On This Page
   :local:
   :depth: 2

omnia.sh --upgrade
-----------------

Upgrade the Omnia core container from the current version to the next available version.

Synopsis
--------

.. code-block:: bash

   ./omnia.sh --upgrade

Description
-----------

The ``--upgrade`` command initiates the Omnia core container upgrade process. This command validates the current environment, creates backups, swaps the core container, and prepares the system for input file migration.

The upgrade process follows these phases:
1. Pre-upgrade validation
2. Approval gate with user confirmation
3. Backup creation
4. Container swap
5. Migration preparation
6. Post-upgrade validation

Options
-------

This command does not accept additional options. All configuration is handled interactively during the upgrade process.

Examples
--------

Initiate the upgrade process:

.. code-block:: bash

   ./omnia.sh --upgrade

Expected output shows the upgrade workflow:

.. code-block:: text

   Current Omnia version: 2.0.0.0
   Target version: 2.1.0.0
   
   New features in Omnia 2.1:
   - IB network support
   - Enhanced configuration sources
   - Improved scheduler integration
   
   Backup destination: /opt/omnia/backups/upgrade_20240227_143022
   
   Do you want to proceed with the upgrade? (y/N): y

Exit Codes
----------

* **0**: Upgrade completed successfully
* **1**: Upgrade failed due to validation errors
* **2**: Upgrade failed during container swap
* **3**: Upgrade failed during backup creation
* **4**: User cancelled the upgrade

Related Topics
--------------

* :doc:`../../upgrade/how-to-upgrade-core`
* :doc:`../../upgrade/concept-core-upgrade`

omnia.sh --rollback
-------------------

Roll back the Omnia core container to a previous version using available backups.

Synopsis
--------

.. code-block:: bash

   ./omnia.sh --rollback

Description
-----------

The ``--rollback`` command reverts the Omnia core container to a previous version by restoring from available backups. This command is used when upgrade failures occur or when you need to return to a previous stable version.

The rollback process:
1. Validates available backups
2. Stops the current container
3. Restores input files from backup
4. Starts the previous container version
5. Updates metadata accordingly

Options
-------

This command does not accept additional options. The rollback process is interactive and presents available backup options.

Examples
--------

Initiate the rollback process:

.. code-block:: bash

   ./omnia.sh --rollback

Expected output shows available rollback options:

.. code-block:: text

   Available rollback versions:
   1. Omnia 2.0.0.0 (backup: 20240227_143022)
   
   Select version to rollback to [1]: 1
   
   Rollback to Omnia 2.0.0.0?
   This will restore the 2.0.0.0 core container and input files.
   Do you want to continue? (y/N): y

Exit Codes
----------

* **0**: Rollback completed successfully
* **1**: No suitable backup found
* **2**: Rollback failed during container operations
* **3**: Rollback failed during file restoration
* **4**: User cancelled the rollback

Related Topics
--------------

* :doc:`../../upgrade/how-to-rollback-upgrade`
* :doc:`../../upgrade/concept-core-upgrade`

omnia.sh --version
------------------

Display the current Omnia version and core container information.

Synopsis
--------

.. code-block:: bash

   ./omnia.sh --version

Description
-----------

The ``--version`` command displays detailed version information about the current Omnia installation, including the core container version and metadata details. This command is new in Omnia 2.1.

Options
-------

This command does not accept any options.

Examples
--------

Check the current Omnia version:

.. code-block:: bash

   ./omnia.sh --version

Example output for Omnia 2.0:

.. code-block:: text

   Omnia version: 2.0.0.0
   Core container: 1.0
   Installation date: 2024-01-15
   Metadata path: /opt/omnia/.data/oim_metadata.yml

Example output for Omnia 2.1:

.. code-block:: text

   Omnia version: 2.1.0.0
   Core container: 1.1
   Installation date: 2024-02-27
   Last upgrade: 2024-02-27 14:30:22
   Metadata path: /opt/omnia/.data/oim_metadata.yml

Exit Codes
----------

* **0**: Version information displayed successfully
* **1**: Unable to determine version (metadata corrupted)

Usage Notes
-----------

* This command is available starting with Omnia 2.1
* Version information is read from ``/opt/omnia/.data/oim_metadata.yml``
* The command works both before and after upgrade operations

Related Topics
--------------

* :doc:`../../upgrade/how-to-upgrade-core`
* :doc:`../../upgrade/concept-core-upgrade`

Command Dependencies
--------------------

The upgrade commands have specific dependencies and requirements:

**System Requirements**:
- Root or sudo access on the OIM node
- Podman or Docker for container management
- Sufficient disk space for backups (minimum 2 GB)

**Version Compatibility**:
- ``--upgrade`` requires Omnia 2.0.0.0 with core container 1.0
- ``--rollback`` requires available backup from previous upgrade
- ``--version`` works with all Omnia 2.x versions

**Network Requirements**:
- Internet access for downloading upgrade images (if not locally available)
- Network connectivity to container registries

**File System Requirements**:
- Writable ``/opt/omnia`` directory
- Sufficient permissions for backup operations
- Access to ``/opt/omnia/.data/`` for metadata operations

Error Conditions
---------------

Common error conditions and their meanings:

**Validation Errors**:
- Container version mismatch: Upgrade requires specific current version
- Insufficient disk space: Backup creation needs adequate space
- Permission denied: Requires root or sudo access

**Backup Errors**:
- Backup directory creation failed: Check permissions and disk space
- File copy failed: Verify source files are accessible
- Integrity check failed: Backup may be corrupted

**Container Errors**:
- Container stop failed: Force stop may be required
- Container start failed: Check image availability and resources
- Health check timeout: Container may not be ready

**Metadata Errors**:
- Metadata file missing: System may be in inconsistent state
- Version information corrupted: May require manual intervention

Troubleshooting
---------------

For command-specific troubleshooting:

* **Upgrade command fails**: Check prerequisites and system requirements
* **Rollback command fails**: Verify backup availability and integrity
* **Version command fails**: Check metadata file permissions and integrity

For comprehensive troubleshooting guidance, see :doc:`../../troubleshooting/upgrade-issues`.

Related Topics
--------------

* :doc:`../../upgrade/how-to-upgrade-core`
* :doc:`../../upgrade/how-to-rollback-upgrade`
* :doc:`../../upgrade/how-to-migrate-inputs`
* :doc:`../../troubleshooting/upgrade-issues`
