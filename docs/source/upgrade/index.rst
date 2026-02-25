Omnia Upgrade Guide
===================

This section provides comprehensive documentation for upgrading Omnia from version 2.0 to 2.1, including the core container upgrade process, input file migration, and rollback procedures.

.. note::
   This section is pending SME validation. Content may change before publication.

.. toctree::
   :maxdepth: 2

   concept-omnia-core-upgrade
   how-to-perform-upgrade
   how-to-rollback-upgrade
   how-to-migrate-input-files
   reference-upgrade-commands
   troubleshooting-upgrade-issues

Upgrade Overview
----------------

The Omnia 2.1 upgrade process introduces a new automated workflow for transitioning your core container while preserving your existing configuration and data.

**Key Features:**
* Automated six-phase upgrade workflow
* Built-in backup and rollback capabilities
* Input file migration from 2.0 to 2.1 format
* Validation and health checks throughout the process

**Upgrade Process:**
1. **Core Container Upgrade**: Transition from Omnia 2.0 to 2.1 core container
2. **Input File Migration**: Transform configurations to 2.1 format
3. **Cluster Reprovisioning**: Optional - for new 2.1 features

**Important Notes:**
* New features in Omnia 2.1 require full cluster reprovisioning
* Core container upgrade alone preserves existing cluster operations
* Rollback capability provides safety net for failed upgrades

Getting Started
---------------

To begin the upgrade process:

1. Review the :doc:`concept-omnia-core-upgrade` topic
2. Follow the :doc:`how-to-perform-upgrade` procedure
3. Complete :doc:`how-to-migrate-input-files` for configuration updates
4. Use :doc:`reference-upgrade-commands` for command reference
5. Consult :doc:`troubleshooting-upgrade-issues` if issues occur

**Prerequisites:**
* Omnia 2.0 deployment with healthy core container
* Sufficient disk space for backups (minimum 2 GB)
* Network connectivity for container operations
* Appropriate system permissions (sudo/root access)

**Support:**
If you encounter issues during the upgrade process, refer to the troubleshooting guide or consider using the rollback procedure to restore system stability.
