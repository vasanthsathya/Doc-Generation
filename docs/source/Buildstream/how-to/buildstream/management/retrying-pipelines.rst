.. _retrying-pipelines:

Retry Pipeline Operations
==========================

Retry failed BuildStream pipelines by creating a new job and re-executing the full pipeline through GitLab. This procedure covers pipeline retry through GitLab when stages fail and cannot be individually re-run.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStream retry operations allow you to recover from pipeline failures by creating a new job and re-executing the full pipeline through GitLab. 

**Important**: Individual failed stages cannot be re-run separately. Retry operations require creating a new job and re-executing the entire pipeline from the beginning. This is due to the immutability constraint in the current BuildStream release.

Retry operations are useful for handling transient failures such as network issues, temporary resource constraints, or configuration errors that have been corrected.

Prerequisites
------------

Before retrying pipeline operations, ensure the following:

* Pipeline has failed
* The issue that caused the failure has been identified and resolved
* GitLab project is accessible
* GitLab runner is active and available
* Configuration files (catalog, PXE mapping, etc.) have been corrected if needed

Procedure
---------

Retry Pipeline Through GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Identify the failed pipeline by checking the GitLab project:

   a. Navigate to **Build** → **Pipelines**.
   
   b. Locate the failed pipeline and note the Pipeline ID.

#. Determine the point of failure:

   a. Click on the failed pipeline to view details.
   
   b. Identify which stage failed and review the error logs.

#. Resolve the issue that caused the failure:

   a. Fix configuration errors if present.
   
   b. Resolve network connectivity issues.
   
   c. Clear resource constraints if applicable.
   
   d. Address any other specific error conditions.

#. Retry the pipeline by triggering a new pipeline execution through GitLab:

   a. Navigate to **Build** → **Pipelines**.
   
   b. Click **New Pipeline**.
   
   c. In the pipeline configuration dialog, select ``build`` from the dropdown list.
   
   d. For build pipeline retry: Run the build stage
   
   e. For deploy pipeline retry: Run the deploy stage
   
   f. Click **Run Pipeline** to execute the pipeline retry.

.. note::
   This creates a new job and re-executes the entire pipeline from the beginning. Individual failed stages cannot be retried separately due to immutability constraints in the current BuildStream release.

#. Monitor the retry operation through the GitLab interface:

   a. Navigate to **Build** → **Pipelines**.
   
   b. The retried pipeline will appear as a new pipeline execution.
   
   c. Monitor stage execution to ensure it progresses successfully.

#. Verify that the pipeline completes successfully.

Verification
------------

#. Check the GitLab pipeline status to ensure all stages passed.

#. Verify the new Pipeline ID is created for the retry operation.

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

**GitLab runner not available**:
* Check GitLab runner status in GitLab project settings
* Verify GitLab runner is set to "Running Always"
* Check runner connectivity and resource availability

**Pipeline fails to start**:
* Verify GitLab project configuration
* Check that "build" is selected from the dropdown list
* Verify the correct stage (build/deploy) is selected for execution
* Review GitLab pipeline logs for specific error messages

**Configuration files not updated**:
* Verify that configuration files (catalog, PXE mapping) were corrected
* Check that files are committed to the GitLab repository
* Verify file syntax and format

Related Topics
--------------

* :doc:`../build/executing-build-pipeline` - Execute Build Pipeline
* :doc:`../deploy/executing-deploy-pipeline` - Execute Deploy Pipeline
* :doc:`../../reference/buildstream/pipeline-stages` - Pipeline Stages Reference
* :doc:`../../troubleshooting/buildstream/common-pipeline-issues` - Troubleshooting Guide