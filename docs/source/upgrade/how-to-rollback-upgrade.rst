.. _task-rollback-upgrade:

Rolling Back Omnia Core Container Upgrade
==========================================

Roll back your Omnia core container from version 2.1 to 2.0 when an upgrade fails or causes issues. This procedure restores your previous configuration using the backup created during the upgrade process.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before starting the rollback, ensure the following requirements are met:

* A backup exists from a previous upgrade
* The backup directory is accessible and intact
* You have sudo/root access on the OIM node
* No other Omnia operations are in progress
* You understand that rollback will revert to Omnia 2.0 functionality

.. note::
   This topic is pending SME validation. Content may change before publication.

.. warning::
   Rollback will restore your Omnia core container to version 2.0 and revert configuration changes made during the upgrade. Ensure this is the desired action before proceeding.

Procedure
---------

#. Navigate to the directory containing the ``omnia.sh`` file:

   .. code-block:: bash

      cd /path/to/omnia.sh

#. Verify your current Omnia version:

   .. code-block:: bash

      ./omnia.sh --version

   Expected output should show version 2.1.0.0.

#. Start the rollback process:

   .. code-block:: bash

      ./omnia.sh --rollback

#. Review available rollback options:

   The system will display available versions to rollback to. Select version 2.0.0.0.

#. Confirm the rollback destination:

   The system will show the backup location that will be used for restoration.

#. Approve the rollback:

   When prompted, review the rollback summary and type ``y`` to proceed or ``n`` to cancel.

   .. caution::
      Once you approve the rollback, the system will begin stopping the 2.1 container and restoring your 2.0 configuration.

#. Monitor the rollback progress:

   The system will progress through six rollback steps:
   * Step 1: Validate backup exists
   * Step 2: Stop 2.1 container
   * Step 3: Restore inputs from backup
   * Step 4: Start 1.0 container
   * Step 5: Update metadata to version 2.0.0.0
   * Step 6: Validate rollback success

#. Wait for the rollback completion message:

   When the rollback completes successfully, you will see:
   * "Rollback successful" message
   * Restored version information (2.0.0.0)
   * Confirmation that original inputs are restored

Result
------

Your Omnia core container has been rolled back from version 2.1 to 2.0. The system has:

* Stopped the 2.1 core container
* Restored input files from the backup
* Started the 2.0 core container
* Updated metadata to reflect version 2.0.0.0
* Validated the rollback was successful

Verification
------------

Verify the rollback was successful:

#. Check the restored version:

   .. code-block:: bash

      ./omnia.sh --version

   Expected output: ``2.0.0.0``

#. Verify the container is running:

   .. code-block:: bash

      podman ps | grep omnia-core

   You should see the omnia-core container running with the 1.0 tag.

#. Verify inputs were restored:

   .. code-block:: bash

      ls -la /opt/omnia/input

   Your original input files should be present.

#. Verify metadata was reverted:

   .. code-block:: bash

      cat /opt/omnia/.data/oim_metadata.yml | grep omnia_version

   Expected output: ``omnia_version: 2.0.0.0``

Next Steps
----------

**After Successful Rollback**

#. Review the rollback log:

   Check for any issues that may have caused the original upgrade failure.

#. Address upgrade prerequisites:

   Ensure all requirements are met before attempting another upgrade:
   * Sufficient disk space
   * Network connectivity
   * Correct image availability
   * No conflicting operations

#. Consider troubleshooting:

   If the upgrade failed due to specific issues, consult the troubleshooting guide:
   :doc:`troubleshooting-upgrade-issues`

#. Plan for another upgrade attempt:

   When ready, you can attempt the upgrade again:
   :doc:`how-to-perform-upgrade`

**Rollback Limitations**

.. important::
   Consider the following limitations when using rollback:

* **Data Changes**: Any data changes made after the upgrade will be lost
* **New Features**: You will lose access to 2.1-specific features
* **Configuration**: Manual changes made after upgrade will be reverted
* **Cluster State**: Cluster nodes may be in an inconsistent state

**When to Use Rollback vs. Troubleshooting**

Use rollback when:
* Upgrade fails completely and system is unstable
* Critical functionality is broken after upgrade
* You need to quickly restore production operations
* [TO BE PROVIDED: Additional rollback scenarios]

Use troubleshooting when:
* Minor issues occur that can be fixed without rollback
* Specific features are not working but core functionality is fine
* You want to preserve 2.1 functionality while fixing issues

**Related topics:**
* :doc:`concept-omnia-core-upgrade`
* :doc:`how-to-perform-upgrade`
* :doc:`troubleshooting-upgrade-issues`
