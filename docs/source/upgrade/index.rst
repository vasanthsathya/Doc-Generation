.. _upgrade-index:

Upgrading Omnia
===============

This section provides comprehensive guidance for upgrading Omnia from version 2.0 to 2.1. The upgrade process is designed to preserve your existing configurations while enabling new features and improvements.

.. note::
   This topic is pending SME validation. Content may change before publication.

.. toctree::
   :maxdepth: 2

   concept-core-upgrade
   how-to-upgrade-core
   how-to-migrate-inputs
   how-to-rollback-upgrade

Upgrade Overview
----------------

The Omnia 2.0 to 2.1 upgrade involves:

* **Core Container Upgrade**: Replace the Omnia core container from version 1.0 to 1.1
* **Input File Migration**: Transform configuration files from 2.0 to 2.1 format
* **Backup and Recovery**: Automated backup creation with rollback capability
* **Feature Enablement**: Access new 2.1 capabilities after cluster reprovisioning

Before You Begin
----------------

**Prerequisites**:
- Omnia 2.0.0.0 with core container 1.0 currently running
- Administrator access on the Omnia Infrastructure Manager (OIM) node
- Minimum 2 GB free disk space for backup operations
- Network connectivity for container image downloads

**Planning Considerations**:
- Schedule 5-10 minute maintenance window for core container swap
- Plan for cluster reprovisioning if using new 2.1 features
- Ensure backup storage is available and accessible
- Test upgrade process in non-production environment if possible

**What Gets Preserved**:
- All input files and configurations
- Cluster metadata and settings
- Custom parameter values
- Network and storage configurations

**What Changes**:
- Core container version (1.0 → 1.1)
- Omnia version (2.0.0.0 → 2.1.0.0)
- Input file format and structure
- Available configuration parameters

Upgrade Process
--------------

The upgrade follows a structured approach:

1. **Preparation**: Download 2.1 script and verify prerequisites
2. **Core Container Upgrade**: Replace container and create backups
3. **Input Migration**: Transform configurations to 2.1 format
4. **Validation**: Verify system operation and configuration integrity
5. **Optional Reprovisioning**: Enable new features through cluster reprovisioning

For detailed step-by-step instructions, see :doc:`how-to-upgrade-core`.

Key Features in 2.1
--------------------

Omnia 2.1 introduces several enhancements:

* **IB Network Support**: Enhanced InfiniBand network configuration options
* **Improved Configuration Sources**: Multiple configuration source types and better management
* **Enhanced Scheduler Integration**: Improved Slurm and Kubernetes integration
* **Better Performance**: Optimized container operations and resource management
* **Enhanced Security**: Updated security configurations and compliance features

.. warning::
   To use new 2.1 features, you must perform a full cluster reprovision after the upgrade. The core container upgrade alone preserves existing functionality.

Rollback Capability
-------------------

The upgrade includes comprehensive rollback capabilities:

* **Automatic Backup**: All critical files backed up before any changes
* **Rollback Command**: ``./omnia.sh --rollback`` restores previous version
* **Validation Checks**: System validation before and after rollback
* **Data Protection**: No data loss during rollback process

For rollback procedures, see :doc:`how-to-rollback-upgrade`.

Troubleshooting
---------------

Common issues and solutions:

* **Validation Failures**: Check prerequisites and system requirements
* **Backup Problems**: Verify disk space and file permissions
* **Container Issues**: Check system resources and image availability
* **Migration Errors**: Validate input file syntax and structure

For comprehensive troubleshooting guidance, see :doc:`../troubleshooting/upgrade-issues`.

Related Topics
--------------

* :doc:`../Overview/Architecture/index`
* :doc:`../OmniaInstallGuide/index`
* :doc:`../reference/cli/omnia-upgrade`
