.. _task-perform-upgrade:

Performing Omnia Core Container Upgrade
========================================

Upgrade your Omnia core container from version 2.0 to 2.1 using the automated upgrade workflow. This procedure transitions your Omnia Infrastructure Manager while preserving your existing configuration and data.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before starting the upgrade, ensure the following requirements are met:

* You have the Omnia 2.1 ``omnia.sh`` script file
* The Omnia 2.1 core container image is present on your OIM host
* Your current Omnia 2.0 core container is running and healthy
* You have sudo/root access on the OIM node
* Network connectivity to Docker Hub is available
* Minimum 2 GB of free disk space for backups
* No other Omnia operations are in progress

.. note::
   This topic is pending SME validation. Content may change before publication.

Download Required Files
----------------------

#. Download the Omnia 2.1 shell script:

   .. code-block:: bash

      wget https://raw.githubusercontent.com/dell/omnia/refs/heads/pub/q1_dev/omnia.sh

   [TO BE PROVIDED: Updated branch and tag information after release]

#. Ensure the Omnia 2.1 core container image is available:

   .. code-block:: bash

      ./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev

   .. note::
      If the image is already present locally, this step can be skipped.

Procedure
---------

#. Navigate to the directory containing the new ``omnia.sh`` file:

   .. code-block:: bash

      cd /path/to/omnia.sh

#. Verify your current Omnia version:

   .. code-block:: bash

      ./omnia.sh --version

   Expected output should show version 2.0.0.0.

#. Start the upgrade process:

   .. code-block:: bash

      ./omnia.sh --upgrade

#. Review the pre-upgrade validation results:
   
   The system will display:
   * Current Omnia version (2.0)
   * Target upgrade version (2.1)
   * Validation results for prerequisites

#. Confirm the backup destination:

   The system will show the default backup location:
   ``/opt/omnia/backups/upgrade_<timestamp>``

   You can accept the default or specify a custom location.

#. Approve the upgrade:

   When prompted, review the upgrade summary and type ``y`` to proceed or ``n`` to cancel.

   .. warning::
      Once you approve the upgrade, the system will begin stopping services and creating backups. Ensure you have a maintenance window of 5-10 minutes.

#. Monitor the upgrade progress:

   The system will progress through six phases:
   * Phase 1: Pre-upgrade validation
   * Phase 2: Approval gate (completed)
   * Phase 3: Backup creation
   * Phase 4: Container swap
   * Phase 5: Migration and apply
   * Phase 6: Post-upgrade validation

#. Wait for the upgrade completion message:

   When the upgrade completes successfully, you will see:
   * "Upgrade successful" message
   * New version information (2.1.0.0)
   * Instructions for Step 2 (input file migration)

Result
------

Your Omnia core container has been upgraded from version 2.0 to 2.1. The system has:

* Created backups of your original configuration
* Swapped the core container from image 1.0 to 1.1
* Updated metadata to reflect version 2.1.0.0
* Validated the new container health
* Prepared for input file migration

Verification
------------

Verify the upgrade was successful:

#. Check the new version:

   .. code-block:: bash

      ./omnia.sh --version

   Expected output: ``2.1.0.0``

#. Verify the container is running:

   .. code-block:: bash

      podman ps | grep omnia-core

   You should see the omnia-core container running with the 2.1 tag.

#. Check the backup was created:

   .. code-block:: bash

      ls -la /opt/omnia/backups/upgrade_*

   You should see a timestamped backup directory.

#. Verify metadata was updated:

   .. code-block:: bash

      cat /opt/omnia/.data/oim_metadata.yml | grep omnia_version

   Expected output: ``omnia_version: 2.1.0.0``

Next Steps
----------

**Step 2: Input File Migration**

After successful core container upgrade, you must migrate your input files:

#. Enter the upgraded container:

   .. code-block:: bash

      ./omnia.sh

#. Run the input migration playbook:

   .. code-block:: bash

      ansible-playbook /omnia/upgrade/upgrade_omnia.yml

   This transforms your 2.0 input files to 2.1 format.

#. Review the migration results:

   The system will display:
   * Successfully migrated input files
   * New parameters introduced in 2.1
   * Manual configuration requirements
   * Cluster reprovisioning guidance

.. important::
   For new features in Omnia 2.1, you must perform a full cluster reprovisioning. The core container upgrade alone does not enable new cluster capabilities.

**Optional: Cluster Reprovisioning**

If you want to use new 2.1 features:

#. Update local repository:

   .. code-block:: bash

      ansible-playbook local_repo.yml

#. Build new images:

   .. code-block:: bash

      ./build_images.sh

#. Run discovery:

   .. code-block:: bash

      ansible-playbook discovery.yml

#. Re-provision your cluster:

   .. code-block:: bash

      ansible-playbook provision.yml

**Related topics:**
* :doc:`concept-omnia-core-upgrade`
* :doc:`how-to-migrate-input-files`
* :doc:`how-to-rollback-upgrade`
* :doc:`troubleshooting-upgrade-issues`
