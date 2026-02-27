.. _concept-core-upgrade:

Omnia Core Container Upgrade Overview
======================================

.. note::
   This topic is pending SME validation. Content may change before publication.

The Omnia core container upgrade process transitions your Omnia Infrastructure Manager (OIM) from version 2.0 to 2.1 while preserving your existing cluster configurations and data. This upgrade introduces new capabilities and requires understanding the two-step upgrade process.

.. contents:: On This Page
   :local:
   :depth: 2

What is the Core Container Upgrade
---------------------------------

The core container upgrade replaces the Omnia core container running within OIM from version 1.0 (Omnia 2.0 code) to version 1.1 (Omnia 2.1 code). This upgrade maintains data integrity by creating backups of input files and configurations before applying the new container image.

The upgrade involves:
- **Core container replacement**: Swapping the 1.0 container for the 1.1 container
- **Input file migration**: Transforming 2.0 format input files to 2.1 compatibility
- **Configuration preservation**: Maintaining existing cluster settings and metadata
- **Backup creation**: Automated backup of critical files before any changes

Why the Upgrade Matters
-----------------------

Upgrading to Omnia 2.1 provides access to new features and improvements while maintaining your existing cluster investment. The upgrade process is designed to minimize downtime and reduce the risk of data loss.

Key benefits include:
- **New feature access**: Enable Omnia 2.1 capabilities for enhanced cluster management
- **Improved stability**: Benefit from bug fixes and performance improvements
- **Future compatibility**: Position your cluster for subsequent upgrades
- **Configuration preservation**: Maintain your existing cluster settings and customizations

.. warning::
   New feature enablement for the cluster requires a full re-provision on a fresh Omnia 2.1 deployment. The core container upgrade alone does not enable new cluster features.

How the Upgrade Process Works
------------------------------

The upgrade follows a comprehensive six-phase workflow that ensures system stability and data protection.

Phase 1: Pre-Upgrade Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before starting the upgrade, the system validates:
- Current core container version must be 1.0 (Omnia 2.0)
- Target container version 1.1 (Omnia 2.1) is available locally
- ``/opt/omnia`` mount and permissions are valid
- Sufficient disk space exists for backup operations

Phase 2: Approval Gate
~~~~~~~~~~~~~~~~~~~~~

The upgrade process requires explicit administrator approval:
- Displays current version (2.0) and target version (2.1)
- Lists new features in Omnia 2.1
- Shows breaking changes and migration impacts
- Prompts for backup destination location
- Requires explicit confirmation before proceeding

Phase 3: Backup Creation
~~~~~~~~~~~~~~~~~~~~~~~

Automated backup protects your data:
- Creates timestamped backup directory
- Copies input files from ``/opt/omnia/input/``
- Backs up container configuration files
- Preserves ``oim_metadata.yml``
- Generates backup manifest for verification
- Validates backup integrity before proceeding

Phase 4: Container Swap
~~~~~~~~~~~~~~~~~~~~~~~

The core container replacement occurs:
- Stops Omnia core 1.0 container gracefully
- Verifies 1.0 container is stopped
- Starts Omnia core 1.1 Quadlet unit
- Waits for 1.1 container health check (60s timeout)
- Updates metadata with ``omnia_version: 2.1.0.0``

Phase 5: Migration and Apply
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inside the new 1.1 container:
- Executes ``upgrade_omnia.yml`` playbook
- Runs ``upgrade_oim.yml`` to transform inputs from 2.0 to 2.1
- Reads existing 2.0 input files
- Writes 2.1 compatible input files
- Generates reprovision guidance
- Validates migrated input file syntax

Phase 6: Post-Upgrade Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Final verification ensures success:
- Verifies 1.1 container is running and healthy
- Validates Omnia CLI responds (new ``omnia.sh --version`` command)
- Confirms migrated input files are valid for 2.1
- Displays upgrade success message
- Provides post-upgrade workflow guidance

Two-Step Upgrade Process
------------------------

The Omnia upgrade is designed as a two-step process:

**Step 1: Core Container Upgrade**
- Replace the core container from 1.0 to 1.1
- Create backups of existing configurations
- Prepare the environment for input migration

**Step 2: Input File Migration**
- Transform 2.0 input files to 2.1 format
- Add new parameters and configuration options
- Validate migrated configurations
- Prepare for cluster reprovisioning (if using new features)

.. note::
   You must complete both steps to fully upgrade to Omnia 2.1. The core container upgrade alone does not complete the migration process.

Backup Strategy
---------------

The upgrade process automatically creates comprehensive backups:

**Backup Location**: ``/opt/omnia/backups/upgrade_<timestamp>``

**Backup Contents**:
- Input files from ``/opt/omnia/input/``
- Container configuration files
- ``oim_metadata.yml`` with version information
- Backup manifest with integrity checksums

**Backup Validation**:
- Automatic integrity verification after creation
- Rollback capability if upgrade fails
- Manual restoration options available

Cluster Reprovisioning Requirements
-----------------------------------

After upgrading to Omnia 2.1, consider your cluster reprovisioning needs:

**No Reprovisioning Required**:
- Continue using existing cluster with current features
- Maintain 2.0 functionality within 2.1 environment
- Access stability improvements and bug fixes

**Reprovisioning Required**:
- Enable new 2.1 features (IB networking, enhanced configuration sources)
- Add new nodes to the cluster
- Apply major architectural changes
- Utilize advanced workload management capabilities

.. warning::
   Adding new nodes or enabling new features requires a full cluster re-provision on a fresh Omnia 2.1 deployment. In-place upgrades do not support cluster expansion.

Related Topics
--------------

* :doc:`how-to-upgrade-core`
* :doc:`how-to-migrate-inputs`
* :doc:`how-to-rollback-upgrade`
* :doc:`../reference/cli/omnia-upgrade`
