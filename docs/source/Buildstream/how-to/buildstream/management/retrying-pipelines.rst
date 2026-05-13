.. _retrying-pipelines:

Retry Pipeline Operations
==========================

Retry failed BuildStream pipeline stages or entire pipelines to resolve transient failures and complete deployments successfully.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStream retry operations allow you to re-execute failed pipeline stages or entire pipelines after resolving the issues that caused the initial failure. Unlike resume operations, retry operations create a new execution attempt.

* **Stage Retry**: Retry a specific failed stage
* **Pipeline Retry**: Retry the entire pipeline from the beginning
* **Job Retry**: Retry specific failed jobs within a stage

Retry operations are useful for handling transient failures such as network issues, temporary resource constraints, or configuration errors that have been corrected.

Prerequisites
------------

Before retrying pipeline operations, ensure the following:

* Pipeline has failed
* The issue that caused the failure has been identified and resolved
* BuildStream infrastructure is operational
* BuildStream API server is running and accessible
* Sufficient system resources are available for the retry

Procedure
---------

#. Identify the failed pipeline by checking the GitLab project:

   a. Navigate to **Build** → **Pipelines**.
   
   b. Locate the failed pipeline and note the Pipeline ID and Job ID.

#. Determine the point of failure:

   a. Click on the failed pipeline to view details.
   
   b. Identify which stage or job failed and review the error logs.

#. Resolve the issue that caused the failure:

   a. Fix configuration errors if present.
   
   b. Resolve network connectivity issues.
   
   c. Clear resource constraints if applicable.
   
   d. Address any other specific error conditions.

#. Access the Omnia core container::

    ssh omnia_core

#. Navigate to the BuildStream utilities directory::

    cd /omnia/utils

#. To retry a specific failed stage, run::

    ansible-playbook retry_pipeline.yml -e "pipeline_id=<pipeline_id>" -e "stage_name=<stage_name>"

#. To retry the entire pipeline from the beginning, run::

    ansible-playbook retry_pipeline.yml -e "pipeline_id=<pipeline_id>" -e "retry_all=true"

.. note::
   Retry operations create a new Pipeline ID but may preserve the Job ID depending on configuration. Check the BuildStream API documentation for specific behavior.

#. Monitor the retry operation through the GitLab interface:

   a. Navigate to **Build** → **Pipelines**.
   
   b. The retried pipeline will appear as a new pipeline execution.
   
   c. Monitor stage execution to ensure it progresses successfully.

#. Verify that the pipeline completes successfully.

Verification
------------

#. Check the GitLab pipeline status to ensure all stages passed.

#. Verify the new Pipeline ID is created for the retry operation.

#. Check the BuildStream API to confirm pipeline and Image Group status.

#. For build pipelines, verify that images were created successfully.

#. For deploy pipelines, verify that nodes were deployed correctly.

#. Compare results with the original failed pipeline to confirm the issue is resolved.

Troubleshooting
---------------

**Retry operation fails with same error**:
* Verify that the root cause was properly identified and resolved
* Check for persistent configuration errors
* Review system logs for underlying issues
* Verify resource availability

**Retry creates duplicate resources**:
* Check if the original pipeline created partial resources
* Verify cleanup operations are run before retry
* Review Image Group status in the BuildStream API

**Retry operation hangs**:
* Check BuildStream API server status
* Verify network connectivity
* Review system resource utilization
* Check for deadlocked processes

Related Topics
--------------

* :doc:`../management/resuming-pipelines` - Resume Pipeline Operations
* :doc:`../management/performing-cleanup-operations` - Cleanup Operations
* :doc:`../../troubleshooting/buildstream/common-pipeline-issues` - Troubleshooting Guide