.. _concept-omnia-core-upgrade:

Understanding Omnia Core Container Upgrade
==========================================

The Omnia core container upgrade process transforms your Omnia deployment from version 2.0 to 2.1 while preserving your existing configuration and data.

**Why it matters:** The upgrade enables you to access new features, security improvements, and architectural enhancements introduced in Omnia 2.1, including containerized OIM, enhanced LocalRepo, and OpenCHAMI integration.

**How it works:** The upgrade follows a comprehensive six-phase workflow that safely transitions your core container from the 1.0 image (Omnia 2.0 code) to the 1.1 image (Omnia 2.1 code) while maintaining data integrity and providing rollback capabilities.

Six-Phase Upgrade Workflow
---------------------------

The upgrade process orchestrates the transition through six distinct phases:

**Phase 1: Pre-Upgrade Validation**
The system validates that your environment meets upgrade requirements:
- Verifies the running container is version 1.0 (Omnia 2.0)
- Confirms the target 1.1 image (Omnia 2.1) is available locally
- Validates existing ``/opt/omnia`` mount and permissions
- Ensures sufficient disk space for backups (minimum 2 GB required)

**Phase 2: Approval Gate**
Before proceeding with the upgrade, you must explicitly approve the operation:
- Displays current version (2.0) and target version (2.1)
- Lists new features and breaking changes in Omnia 2.1
- Shows the backup destination location
- Requires your explicit confirmation to continue

**Phase 3: Backup Creation**
The system creates timestamped backups of critical data:
- Backs up input files from ``/opt/omnia/input/``
- Preserves container configuration files
- Copies ``oim_metadata.yml`` 
- Generates a backup manifest for integrity verification
- Verifies backup completeness before proceeding

**Phase 4: Container Swap**
The core container transition occurs:
- Gracefully stops the Omnia core 1.0 container
- Starts the Omnia core 1.1 Quadlet unit
- Waits for container health check validation (60-second timeout)
- Updates metadata to reflect new version (2.1.0.0)

**Phase 5: Migration and Apply**
Inside the new container, configuration migration occurs:
- Executes ``upgrade_omnia.yml`` playbook
- Transforms input files from 2.0 to 2.1 format
- Generates reprovisioning guidance for cluster updates
- Validates migrated input file syntax
- Applies configuration updates

**Phase 6: Post-Upgrade Validation**
Final verification confirms successful upgrade:
- Verifies the 1.1 container is running and healthy
- Validates Omnia CLI responsiveness (new ``--version`` option)
- Confirms migrated input files are valid for 2.1
- Displays upgrade success message and next steps

Core Container vs. Full Cluster Upgrade
-------------------------------------

**Core Container Upgrade** (this process):
- Upgrades only the Omnia Infrastructure Manager (OIM) core container
- Preserves existing cluster operations during upgrade
- Maintains your current input configurations
- Requires additional steps for new feature enablement
- Typical downtime: 5-10 minutes

**Full Cluster Reprovisioning**:
- Required for enabling new 2.1 features in your cluster
- Involves rebuilding cluster components with new capabilities
- Updates all nodes with new software and configurations
- Longer downtime and more complex planning

**Data Preservation**
The upgrade process preserves:
- Your existing input files and configurations
- SSH keys and authentication data
- Provisioning data and node information
- Network settings and storage configurations
- [SME VALIDATION REQUIRED: Complete list of preserved data items]

**Manual Reconfiguration Required**
After upgrade, you may need to manually configure:
- New input parameters introduced in 2.1 (IB network settings, config sources)
- Feature-specific settings for new capabilities
- Integration points with updated components
- [TO BE PROVIDED: Complete list of manual configuration steps]

**Important Note:** New features in Omnia 2.1 require a full cluster reprovision on a fresh Omnia 2.1 deployment. The core container upgrade alone does not enable new cluster capabilities.

**Related topics:**
* :doc:`how-to-perform-upgrade`
* :doc:`how-to-rollback-upgrade`
* :doc:`reference-upgrade-commands`
