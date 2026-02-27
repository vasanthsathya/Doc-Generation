.. _how-to-rollback-upgrade:

Rolling Back Omnia Core Container Upgrade
==========================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Roll back the Omnia core container upgrade to restore your system to the previous 2.0 state when upgrade failures occur or when you need to return to a stable configuration. This procedure uses the automatically created backups to restore your original environment.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before rolling back the upgrade:

* A failed or problematic upgrade to Omnia 2.1
* Available backup directory from the upgrade process
* Access to the OIM node with administrator privileges
* The 2.1 version of ``omnia.sh`` script (used for rollback operations)

.. important::
   Rollback restores your system to the exact state it was in before the upgrade, including all input files and configurations from the backup.

When to Use Rollback
-------------------

Use rollback in these situations:

* **Upgrade Failure**: The upgrade process fails during any phase
* **Container Issues**: The new 1.1 container fails to start or has health problems
* **Configuration Problems**: Migrated input files cause system instability
* **Performance Issues**: The upgraded system shows unexpected performance degradation
* **Feature Incompatibility**: New features conflict with your existing workflows

.. warning::
   Rollback will undo all changes made during the upgrade, including any manual configuration changes made after the upgrade.

Procedure
---------

#. Navigate to the directory containing the ``omnia.sh`` script.

.. code-block:: bash

   cd /path/to/omnia_2.1_script

#. Initiate the rollback process.

.. code-block:: bash

   ./omnia.sh --rollback

#. Review available rollback options.

The system displays available backup versions:

.. code-block:: text

   Available rollback versions:
   1. Omnia 2.0.0.0 (backup: 20240227_143022)
      - Created: 2024-02-27 14:30:22
      - Size: 245 MB
      - Status: Valid

   Select version to rollback to [1]: 1

#. Confirm the rollback operation.

The system shows rollback details and requests confirmation:

.. code-block:: text

   Rollback to Omnia 2.0.0.0
   This will:
   - Stop Omnia core 1.1 container
   - Restore input files from backup
   - Start Omnia core 1.0 container
   - Update metadata to version 2.0.0.0
   
   Do you want to continue? (y/N): y

.. warning::
   This action will stop the current Omnia services and restore the previous version. Ensure you have an appropriate maintenance window.

#. Monitor the rollback process.

The rollback automatically performs these steps:

**Step 1: Backup Validation**
- Locates the specified backup directory
- Verifies backup integrity and completeness
- Checks that required files are present

**Step 2: Container Management**
- Stops the Omnia core 1.1 container gracefully
- Verifies the 1.1 container is completely stopped
- Prepares for container restoration

**Step 3: Input File Restoration**
- Executes ``rollback_omnia.yml`` playbook
- Restores input files from backup directory
- Replaces 2.1 format files with original 2.0 files
- Validates restored file integrity

**Step 4: Container Restoration**
- Starts the Omnia core 1.0 container
- Verifies the 1.0 container starts successfully
- Performs health checks on the restored container

**Step 5: Metadata Update**
- Updates ``/opt/omnia/.data/oim_metadata.yml``
- Sets ``omnia_version`` back to ``2.0.0.0``
- Records rollback operation in metadata

**Step 6: Final Validation**
- Verifies 1.0 container is running and healthy
- Confirms input files are accessible and valid
- Displays rollback success confirmation

#. Verify the rollback completed successfully.

Expected success message:

.. code-block:: text

   Rollback completed successfully!
   - Omnia version: 2.0.0.0
   - Core container: 1.0
   - Input files restored from: /opt/omnia/backups/upgrade_20240227_143022
   - System ready for operation

Result
------

Your Omnia system is now restored to version 2.0.0.0 with:
- Original 1.0 core container running
- All input files restored to 2.0 format
- Original configurations and settings preserved
- Metadata updated to reflect rollback

Verification
------------

Verify the rollback completed successfully:

#. Check the Omnia version.

.. code-block:: bash

   ./omnia.sh --version

Expected output:

.. code-block:: text

   Omnia version: 2.0.0.0
   Core container: 1.0

#. Verify the core container is running.

.. code-block:: bash

   podman ps | grep omnia-core

Expected output shows the omnia-core container with tag ``1.0``.

#. Confirm input files are restored.

.. code-block:: bash

   ls -la /opt/omnia/input/

Expected output shows your original 2.0 input files.

#. Test system functionality.

.. code-block:: bash

   podman exec -it omnia-core bash
   ls -la /opt/omnia/input/

Verify you can access the container and input files normally.

Next Steps
----------

After completing the rollback:

#. **Investigate Upgrade Issues**: Determine why the original upgrade failed
   - Review upgrade logs for error messages
   - Check system resources and dependencies
   - Verify network connectivity and image availability

#. **Address Root Causes**: Fix issues that caused upgrade failure
   - Resolve disk space problems
   - Fix permission issues
   - Update configuration conflicts

#. **Plan Re-attempt**: Prepare for another upgrade attempt
   - Ensure all prerequisites are met
   - Schedule appropriate maintenance window
   - Have rollback plan ready

#. **Document Issues**: Record the problems encountered and solutions applied
   - Update your operational procedures
   - Share lessons learned with team
   - Consider opening support tickets if needed

.. tip::
   Keep the failed upgrade backup directory until you have successfully completed a new upgrade. It may contain useful diagnostic information.

Manual Rollback Procedure
------------------------

If the automated rollback fails, you can perform manual rollback:

#. Stop the current container.

.. code-block:: bash

   podman stop omnia-core

#. Manually restore input files.

.. code-block:: bash

   cp -r /opt/omnia/backups/upgrade_<timestamp>/input/* /opt/omnia/input/

#. Start the original container.

.. code-block:: bash

   podman start omnia-core-1.0

#. Update metadata manually.

.. code-block:: bash

   vi /opt/omnia/.data/oim_metadata.yml
   # Set omnia_version: 2.0.0.0

.. warning::
   Manual rollback should only be used when automated rollback fails. It requires careful attention to detail and may miss important validation steps.

Troubleshooting
---------------

Common rollback issues and solutions:

**Rollback Fails - Backup Not Found**:
- Verify backup directory exists in ``/opt/omnia/backups/``
- Check backup directory permissions
- Ensure backup timestamp is correct

**Container Stop Fails**:
- Force stop the container: ``podman kill omnia-core``
- Check for processes using the container
- Verify system resources are available

**File Restoration Fails**:
- Check backup file permissions and integrity
- Verify sufficient disk space for restoration
- Review error messages for specific file issues

**Container Start Fails**:
- Verify 1.0 container image is available
- Check container configuration files
- Review system logs for startup errors

**Metadata Update Fails**:
- Check file permissions on ``oim_metadata.yml``
- Verify YAML syntax in metadata file
- Manually update metadata if needed

For detailed troubleshooting guidance, see :doc:`../troubleshooting/upgrade-issues`.

Post-Rollback Considerations
----------------------------

After a successful rollback, consider these factors:

**System State**:
- Your cluster continues operating with 2.0 functionality
- All configurations are restored to their pre-upgrade state
- No data loss should have occurred

**Upgrade Strategy**:
- Review why the upgrade failed
- Address root causes before re-attempting
- Consider testing in a non-production environment first

**Backup Management**:
- Keep the failed upgrade backup for analysis
- Clean up old backup directories to save space
- Document the rollback for future reference

**Communication**:
- Notify stakeholders about the rollback
- Document the timeline and impact
- Plan for the next upgrade attempt

Related Topics
--------------

* :doc:`concept-core-upgrade`
* :doc:`how-to-upgrade-core`
* :doc:`how-to-migrate-inputs`
* :doc:`../troubleshooting/upgrade-issues`
