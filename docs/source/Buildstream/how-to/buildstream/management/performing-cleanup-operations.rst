.. _performing-cleanup-operations:

Perform Cleanup Operations
============================

BuildStreaM cleanup operations remove old Image Groups and associated resources to free up disk space and maintain system performance. Cleanup is performed manually through GitLab pipeline execution.

Prerequisites
------------

Before performing cleanup operations, ensure the following:

* BuildStream infrastructure is operational
* You have administrative access to the OIM
* BuildStream API server is running
* PostgreSQL database is accessible

Procedure
---------

#. Navigate to the GitLab project URL::

    https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

#. Navigate to **Build** → **Pipelines**.

#. Click **New Pipeline**.

#. In the pipeline configuration dialog, select ``clean`` from the dropdown list.

.. TODO:: Add screenshot: GitLab New Pipeline dialog showing clean selection

#. Click **Run Pipeline** to execute the cleanup pipeline.

#. In the Run Pipeline dialog, select the image group(s) to be cleaned up.

.. TODO:: Add screenshot: Run Pipeline dialog showing image group selection

#. Monitor the cleanup pipeline progress through the GitLab web interface:

   a. Click on the running pipeline to view details.
   
   b. Monitor the cleanup stage as it progresses:
   
#. Review the stage status indicators:
   - |success| **Green checkmark**: Stage completed successfully
   - |failed| **Red X**: Stage failed (click for error details)
   - |running| **Blue circle**: Stage currently running

.. |success| image:: ../../../../images/Icons/green_check.png
.. |failed| image:: ../../../../images/Icons/red_x.png
.. |running| image:: ../../../../images/Icons/blue_circle.png

Verification
------------

#. Check the GitLab pipeline status to ensure the cleanup stage passed.

#. Verify the Image Group count is within the configured retention limit.

#. Review the cleanup pipeline logs in GitLab for specific details about which Image Groups were removed.

Related Topics
--------------

* :doc:`../management/retrying-pipelines` - Retry Pipeline Operations
* :doc:`../../../reference/buildstream/configuration-tables` - Configuration Reference