.. _performing-cleanup-operations:

Perform Cleanup Operations
============================

Manage BuildStream resources by performing manual and automated cleanup operations to remove old Image Groups and maintain system performance.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStream cleanup operations remove old Image Groups and associated resources to free up disk space and maintain system performance. Cleanup can be performed manually through GitLab pipelines or configured to run automatically on a scheduled basis.

* **Manual Cleanup**: On-demand removal using GitLab pipeline execution
* **Automated Cleanup**: Scheduled cleanup using cron jobs with configurable retention policies

The automated cleanup retains a maximum of 50 Image Groups and runs every 24 hours by default.

.. important::
   The cleanup pipeline cannot be triggered automatically. It must be manually triggered through GitLab using the procedure below.

Prerequisites
------------

Before performing cleanup operations, ensure the following:

* BuildStream infrastructure is operational
* You have administrative access to the OIM
* BuildStream API server is running
* PostgreSQL database is accessible

Procedure
---------

Manual Cleanup
~~~~~~~~~~~~~~

#. Navigate to the GitLab project URL::

    https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

#. Navigate to **Build** → **Pipelines**.

#. Click **New Pipeline**.

#. In the pipeline configuration dialog, enter ``clean`` as the pipeline type.

#. Click **Run Pipeline** to execute the cleanup pipeline.

.. note::
   The cleanup pipeline will remove Image Groups based on the configured retention policy in the BuildStream configuration. It does not require specific Image Group IDs to be specified.

#. Monitor the cleanup pipeline progress through the GitLab web interface:

   a. Click on the running pipeline to view details.
   
   b. Monitor the cleanup stage as it progresses:
      - **cleanup**: Removes old Image Groups based on retention policy

#. Review the stage status indicators:
   - |success| **Green checkmark**: Stage completed successfully
   - |failed| **Red X**: Stage failed (click for error details)
   - |running| **Blue circle**: Stage currently running

.. |success| image:: ../../images/Icons/green_check.png
.. |failed| image:: ../../images/Icons/red_x.png
.. |running| image:: ../../images/Icons/blue_circle.png

Automated Cleanup
~~~~~~~~~~~~~~~~~

#. Access the Omnia core container::

    ssh omnia_core

#. Navigate to the BuildStream configuration directory::

    cd /opt/omnia/input/project_default

#. Edit the ``build_stream_config.yml`` file to configure automated cleanup settings::

    cleanup:
      enabled: true
      schedule: "0 2 * * *"  # Runs daily at 2 AM
      retention_limit: 50     # Maximum number of Image Groups to retain

#. Set up the cron job for automated cleanup::

    crontab -e

#. Add the following line to schedule the cleanup pipeline::

    0 2 * * * cd /omnia/utils && ansible-playbook cleanup_image_groups.yml >> /var/log/buildstream_cleanup.log 2>&1

#. Save the crontab and exit.

.. note::
   The automated cleanup job will remove Image Groups beyond the retention limit, starting with the oldest Image Groups first.

Verification
------------

Manual Cleanup Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Check the GitLab pipeline status to ensure the cleanup stage passed.

#. Check the BuildStream API to verify Image Groups were removed::

    curl -X GET http://<oim_ip>:<build_stream_port>/api/image-groups

#. Verify the Image Group count is within the configured retention limit.

#. Review the cleanup pipeline logs in GitLab for specific details about which Image Groups were removed.

Automated Cleanup Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Check the cron job log file to verify the cleanup executed::

    tail -f /var/log/buildstream_cleanup.log

#. Verify the cron job is scheduled::

    crontab -l

#. Monitor the Image Group count over time to ensure it stays within the retention limit.

Troubleshooting
---------------

**Cleanup fails to remove Image Groups (GitLab Pipeline)**:
* Verify GitLab runner is active and accessible
* Check BuildStream API server connectivity from GitLab node
* Verify cleanup pipeline configuration in GitLab CI/CD
* Review pipeline logs in GitLab for specific error messages

**Automated cleanup not running**:
* Verify cron service is running: ``systemctl status cron``
* Check crontab syntax
* Review cron logs: ``journalctl -u cron``
* Verify playbook path and permissions

**Disk space not freed after cleanup**:
* Verify Image Groups were actually removed from database
* Check for orphaned files on disk
* Review local repository storage

Related Topics
--------------

* :doc:`../management/resuming-pipelines` - Resume Pipeline Operations
* :doc:`../management/retrying-pipelines` - Retry Pipeline Operations
* :doc:`../../reference/buildstream/configuration-tables` - Configuration Reference