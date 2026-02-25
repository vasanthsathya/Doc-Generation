.. _ref-upgrade-commands:

Omnia Upgrade Command Reference
===============================

Reference documentation for the upgrade-related commands introduced in Omnia 2.1. These commands provide version information, upgrade capabilities, and rollback functionality.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

Omnia 2.1 introduces three new command-line options for managing core container upgrades:

* ``--version`` - Display current Omnia version information
* ``--upgrade`` - Initiate core container upgrade process
* ``--rollback`` - Revert to previous Omnia version

.. note::
   This topic is pending SME validation. Content may change before publication.

Command Syntax
--------------

All upgrade commands use the following syntax:

.. code-block:: bash

   ./omnia.sh <command> [options]

Prerequisites
--------------

Before using upgrade commands, ensure:

* You have the correct version of ``omnia.sh`` for your target operation
* Required container images are available locally
* You have appropriate permissions (sudo/root access)
* No other Omnia operations are in progress

Commands
--------

omnia.sh --version
~~~~~~~~~~~~~~~~~~

Display the current Omnia version and core container information.

**Syntax:**

.. code-block:: bash

   ./omnia.sh --version

**Description:**
Shows the current Omnia version, core container tag, and related version information.

**Output Example:**

.. code-block:: text

   Omnia Version: 2.1.0.0
   Core Container Tag: 2.1
   Build Date: 2026-01-15
   Git Commit: abc123def

**Usage Notes:**
* Use this command to verify your current version before upgrade
* Available in both Omnia 2.0 and 2.1 versions
* Requires no additional parameters

omnia.sh --upgrade
~~~~~~~~~~~~~~~~~~~

Initiate the upgrade process from the current version to the next available version.

**Syntax:**

.. code-block:: bash

   ./omnia.sh --upgrade

**Description:**
Starts the six-phase upgrade workflow that transitions the core container to the next version while preserving configuration and data.

**Upgrade Phases:**
1. Pre-upgrade validation
2. Approval gate
3. Backup creation
4. Container swap
5. Migration and apply
6. Post-upgrade validation

**Prerequisites:**
* Target version container image must be present locally
* Sufficient disk space for backups (minimum 2 GB)
* Current container must be healthy
* No conflicting operations in progress

**Interactive Prompts:**
During upgrade, you will be prompted for:
* Version selection (if multiple options available)
* Backup destination confirmation
* Upgrade approval confirmation

**Example Session:**

.. code-block:: bash

   $ ./omnia.sh --upgrade
   Current version: 2.0.0.0
   Available upgrade: 2.1.0.0
   Backup destination: /opt/omnia/backups/upgrade_20260115_143022
   Proceed with upgrade? (y/N): y
   [Upgrade progress messages...]
   Upgrade completed successfully

**Usage Notes:**
* Requires explicit user approval before proceeding
* Creates automatic backups before making changes
* Provides rollback capability if upgrade fails
* Typical duration: 5-10 minutes

omnia.sh --rollback
~~~~~~~~~~~~~~~~~~~

Revert the Omnia core container to a previous version using available backups.

**Syntax:**

.. code-block:: bash

   ./omnia.sh --rollback

**Description:**
Initiates the rollback process that restores the core container and configuration from a previous backup.

**Rollback Steps:**
1. Validate backup exists
2. Stop current container
3. Restore inputs from backup
4. Start previous container
5. Update metadata
6. Validate rollback success

**Prerequisites:**
* Valid backup must exist from previous upgrade
* Backup directory must be accessible and intact
* No conflicting operations in progress

**Interactive Prompts:**
During rollback, you will be prompted for:
* Version selection to rollback to
* Backup source confirmation
* Rollback approval confirmation

**Example Session:**

.. code-block:: bash

   $ ./omnia.sh --rollback
   Available rollback versions:
   1. 2.0.0.0 (backup: 20260115_143022)
   Select version to rollback: 1
   Proceed with rollback? (y/N): y
   [Rollback progress messages...]
   Rollback completed successfully

**Usage Notes:**
* Requires explicit user approval before proceeding
* Restores configuration from backup
* Reverts all changes made during upgrade
* Typical duration: 3-5 minutes

Error Messages
--------------

Common error messages and their meanings:

**Version Check Errors:**

.. code-block:: text

   ERROR: No upgrade available from current version
   ERROR: Invalid version specified for rollback

**Prerequisite Errors:**

.. code-block:: text

   ERROR: Target container image not found
   ERROR: Insufficient disk space for backup
   ERROR: Container health check failed

**Operation Conflicts:**

.. code-block:: text

   ERROR: Upgrade already in progress
   ERROR: Another Omnia operation is running
   ERROR: System in maintenance mode

**Backup Errors:**

.. code-block:: text

   ERROR: Backup creation failed
   ERROR: Backup integrity check failed
   ERROR: No valid backup found for rollback

**Permission Errors:**

.. code-block:: text

   ERROR: Insufficient permissions for operation
   ERROR: Cannot access required directories

Troubleshooting Command Issues
------------------------------

**Command Not Found:**
Ensure you're using the correct ``omnia.sh`` file for your target version.

**Permission Denied:**
Run commands with appropriate privileges (sudo/root access).

**Network Issues:**
Verify network connectivity for container image operations.

**Container Issues:**
Check container status with ``podman ps`` before running commands.

**Related topics:**
* :doc:`how-to-perform-upgrade`
* :doc:`how-to-rollback-upgrade`
* :doc:`concept-omnia-core-upgrade`
