.. _task-migrate-input-files:

Managing Input File Migration After Upgrade
==========================================

Migrate your Omnia input files from 2.0 to 2.1 format after completing the core container upgrade. This procedure transforms your existing configurations to work with the new Omnia 2.1 architecture.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before starting the migration, ensure the following requirements are met:

* Core container upgrade to 2.1 has been completed successfully
* You are inside the upgraded Omnia core container
* Backup of original 2.0 input files exists
* No other Omnia operations are in progress

.. note::
   This is Step 2 of the upgrade process. Complete Step 1 (core container upgrade) before proceeding.

.. important::
   This topic is pending SME validation. Content may change before publication.

Understanding Input File Migration
---------------------------------

The migration process transforms your 2.0 input files to 2.1 format to maintain cluster functionality. Key changes include:

**New Input Parameters in 2.1:**
* [SME VALIDATION REQUIRED: Complete list of new 2.1 parameters]
* IB network settings for InfiniBand configurations
* Config sources for external configuration management
* [TO BE PROVIDED: Additional new parameters]

**Transformation Process:**
The migration playbook:
* Reads existing 2.0 input files from backup
* Transforms parameter names and values to 2.1 format
* Adds new parameters with default values
* Preserves your custom configurations
* Validates transformed files for syntax correctness

Procedure
---------

#. Enter the upgraded Omnia core container:

   .. code-block:: bash

      ./omnia.sh

   You should now be inside the omnia_core container with version 2.1.

#. Verify you are in the correct container:

   .. code-block:: bash

      cat /opt/omnia/.data/oim_metadata.yml | grep omnia_version

   Expected output: ``omnia_version: 2.1.0.0``

#. Navigate to the upgrade directory:

   .. code-block:: bash

      cd /omnia/upgrade

#. Run the input migration playbook:

   .. code-block:: bash

      ansible-playbook upgrade_omnia.yml

   .. note::
      This playbook reads from the backup directory and writes transformed files to the active input location.

#. Monitor the migration progress:

   The system will display:
   * Files being processed
   * Transformations being applied
   * New parameters being added
   * Validation results

#. Review the migration summary:

   When migration completes, you will see:
   * Successfully migrated input files
   * List of new parameters added
   * Manual configuration requirements
   * Next steps for cluster operations

Result
------

Your input files have been migrated from 2.0 to 2.1 format. The system has:

* Transformed existing parameter names and values
* Added new 2.1 parameters with default values
* Preserved your custom configurations
* Validated transformed files for syntax correctness
* Updated configuration for 2.1 compatibility

Verification
------------

Verify the migration was successful:

#. Check input file format:

   .. code-block:: bash

      ls -la /opt/omnia/input

   Your input files should be present and updated.

#. Verify new parameters were added:

   .. code-block:: bash

      grep -r "new_parameter" /opt/omnia/input/

   [TO BE PROVIDED: Specific new parameter names]

#. Validate input file syntax:

   .. code-block:: bash

      ansible-playbook --syntax-check /omnia/upgrade/upgrade_omnia.yml

   No syntax errors should be reported.

#. Check for migration warnings:

   .. code-block:: bash

      cat /opt/omnia/.data/migration_warnings.log

   [TO BE PROVIDED: Warning file location and format]

Manual Configuration Required
-----------------------------

After migration, you may need to manually configure new parameters:

**IB Network Settings**
[TO BE PROVIDED: Configuration steps for IB network]

**Config Sources**
[TO BE PROVIDED: Configuration steps for config sources]

**Other New Parameters**
[TO BE PROVIDED: Additional manual configuration steps]

.. important::
   Review all new parameters and configure them according to your cluster requirements before proceeding with cluster operations.

Alternative: Skip Migration
------------------------

If you prefer to reconfigure manually instead of migrating:

#. Skip the migration playbook
#. Remove the upgrade lock:

   .. code-block:: bash

      rm /opt/omnia/.data/upgrade_in_progress.lock

#. Reconfigure input files manually:
   * Use default 2.1 input files as templates
   * Configure parameters based on your requirements
   * Validate configuration syntax

.. warning::
   Manual reconfiguration requires more effort but gives you full control over the final configuration.

Next Steps
----------

**For Existing Clusters (Continue Operations)**

If you want to continue using your existing cluster with 2.1:

#. Validate cluster functionality:

   .. code-block:: bash

      omnia-cli status

   [TO BE PROVIDED: Status validation commands]

#. Test basic operations:

   .. code-block:: bash

      omnia-cli node list

   [TO BE PROVIDED: Additional test commands]

**For New Features (Cluster Reprovisioning Required)**

If you want to use new 2.1 features:

.. note::
   New features in Omnia 2.1 require a full cluster reprovisioning. The core container upgrade and input migration alone do not enable new cluster capabilities.

#. Update local repository:

   .. code-block:: bash

      ansible-playbook local_repo.yml

#. Build new images:

   .. code-block:: bash

      ./build_images.sh

   [TO BE PROVIDED: Complete reprovisioning steps]

#. Run discovery:

   .. code-block:: bash

      ansible-playbook discovery.yml

#. Re-provision your cluster:

   .. code-block:: bash

      ansible-playbook provision.yml

.. important::
   Cluster reprovisioning is a significant operation that affects all nodes. Plan accordingly and ensure you have adequate maintenance windows.

**Troubleshooting Migration Issues**

If migration fails:

#. Check the migration log:

   .. code-block:: bash

      cat /var/log/omnia/migration.log

   [TO BE PROVIDED: Log location and format]

#. Verify backup integrity:

   .. code-block:: bash

      ls -la /opt/omnia/backups/upgrade_*/input

#. Consider rollback:

   If migration cannot be completed, you may need to rollback to 2.0:
   :doc:`how-to-rollback-upgrade`

**Related topics:**
* :doc:`concept-omnia-core-upgrade`
* :doc:`how-to-perform-upgrade`
* :doc:`troubleshooting-upgrade-issues`
