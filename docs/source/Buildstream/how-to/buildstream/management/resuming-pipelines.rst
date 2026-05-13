.. _resuming-pipelines:

Resume Pipeline Operations
===========================

Resume interrupted or failed BuildStream pipelines from the last successful state to complete deployment without starting from the beginning.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStream resume operations allow you to recover from pipeline interruptions by resuming execution from the last successful state rather than restarting the entire pipeline. This saves time and resources when dealing with transient failures.

* **Pipeline Resume**: Resume an entire pipeline from the last completed stage
* **Stage Resume**: Resume from a specific failed stage
* **Job Resume**: Resume specific failed jobs within a stage

Resume operations maintain the existing Job ID and Image Group ID, ensuring continuity of the deployment process.

Prerequisites
------------

Before resuming pipeline operations, ensure the following:

* Pipeline has failed or been interrupted
* BuildStream infrastructure is operational
* The issue that caused the failure has been resolved
* BuildStream API server is running and accessible

Procedure
---------

#. Identify the failed pipeline by checking the GitLab project:

   a. Navigate to **Build** → **Pipelines**.
   
   b. Locate the failed pipeline and note the Pipeline ID and Job ID.

#. Determine the point of failure:

   a. Click on the failed pipeline to view details.
   
   b. Identify which stage failed and review the error logs.

#. Access the Omnia core container::

    ssh omnia_core

#. Navigate to the BuildStream utilities directory::

    cd /omnia/utils

#. To resume the entire pipeline from the last successful stage, run::

    ansible-playbook resume_pipeline.yml -e "pipeline_id=<pipeline_id>"

#. To resume from a specific stage, run::

    ansible-playbook resume_pipeline.yml -e "pipeline_id=<pipeline_id>" -e "from_stage=<stage_name>"

.. note::
   Supported stage names for resume operations: ``create-local-repository``, ``parse-catalog``, ``generate-input-files``, ``build-image``, ``deploy``, ``restart``, ``validate``

#. Monitor the resume operation through the GitLab interface:

   a. Navigate to **Build** → **Pipelines**.
   
   b. The resumed pipeline will appear with a new Pipeline ID but the same Job ID.
   
   c. Monitor stage execution to ensure it progresses successfully.

#. Verify that the pipeline completes successfully.

Verification
------------

#. Check the GitLab pipeline status to ensure all stages passed.

#. Verify the Job ID remains the same as the original pipeline.

#. Check the BuildStream API to confirm Image Group status.

#. For build pipelines, verify that images were created successfully.

#. For deploy pipelines, verify that nodes were deployed correctly.

Troubleshooting
---------------

**Resume operation fails**:
* Verify the original pipeline exists in the database
* Check that the stage name is valid
* Ensure the issue that caused the original failure is resolved
* Review BuildStream API logs for detailed error information

**Pipeline resumes from wrong stage**:
* Verify the stage name spelling matches exactly
* Check the pipeline execution history
* Review the resume operation logs

**Resume creates new Image Group**:
* Verify the Job ID is preserved during resume
* Check the resume operation parameters
* Review the BuildStream API documentation for resume behavior

Related Topics
--------------

* :doc:`../management/retrying-pipelines` - Retry Pipeline Operations
* :doc:`../management/performing-cleanup-operations` - Cleanup Operations
* :doc:`../../troubleshooting/buildstream/common-pipeline-issues` - Troubleshooting Guide