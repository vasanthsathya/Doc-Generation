.. _executing-deploy-pipeline:

Execute Deploy Pipeline
========================

Execute the BuildStream deploy pipeline to deploy images to cluster nodes. This procedure covers the three deploy stages: deploy, restart, and validate.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

The BuildStream deploy pipeline automates the deployment of built images to target cluster nodes. The pipeline consists of three sequential stages:

* **deploy**: Deploys the built images to the target nodes
* **restart**: Restarts the nodes to load the deployed images
* **validate**: Validates that the deployment was successful

The deploy pipeline is automatically triggered when you update the PXE mapping file (``pxe_mapping_file.csv``) in the GitLab repository, or can be manually initiated through the GitLab interface.

Prerequisites
------------

Before executing the deploy pipeline, ensure the following:

* Build pipeline has completed successfully and images are available
* Target nodes are powered on and accessible via BMC
* PXE mapping file (``pxe_mapping_file.csv``) is correctly configured with target node information
* PXE mapping file is present in the GitLab repository ``input/`` folder for automatic triggering
* GitLab project is accessible and the runner is active
* BuildStream API server is reachable from the GitLab node

Procedure
---------

Trigger Deploy Pipeline
~~~~~~~~~~~~~~~~~~~~~~~

#. Navigate to the GitLab project URL::

    https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

#. Trigger the deploy pipeline by updating the ``pxe_mapping_file.csv`` file in the GitLab repository and committing the changes. The parent router (``.gitlab-ci.yml``) detects the PXE mapping file change and automatically triggers the deploy pipeline.

.. note::
   The parent router (``.gitlab-ci.yml``) uses file change detection to automatically trigger the appropriate child pipeline. Changes to ``input/pxe_mapping_file.csv`` trigger the deploy pipeline, while changes to ``catalog_rhel.json`` trigger the build pipeline.
   * If the pipeline fails, you can use the manual retry procedure to update input parameters and retry the pipeline.

Manual Pipeline Retry After Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the deploy pipeline fails, you can update the input parameters in the input files and manually retry the pipeline. Use this procedure when you need to modify configuration parameters after a pipeline failure.

When to Use Manual Retry
~~~~~~~~~~~~~~~~~~~~~~~~

Use the manual retry procedure when:

* Pipeline fails due to invalid parameters configured in the input files
* Network or resource issues caused transient failures
* You need to modify PXE mapping file parameters
* You want to retry the pipeline with updated parameters

Procedure for Manual Retry
~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Identify the failure reason by reviewing the pipeline logs in GitLab.

   .. TODO:: Add screenshot: GitLab failed pipeline view showing deploy stage error logs

   a. Navigate to **Build** → **Pipelines**.
   
   b. Click on the failed pipeline.
   
   c. Click on the failed stage to view error logs.

#. Update the input parameters in the GitLab repository.

   **Update PXE Mapping File**:
   
   a. Navigate to the GitLab project repository.
   
   b. Edit the ``input/pxe_mapping_file.csv`` file to fix PXE mapping-related issues.
   
   c. Commit and push the changes.

   **Update Input Configuration Files**:
   
   a. Navigate to the ``input/`` folder in the GitLab repository.
   
   b. Edit the relevant configuration file:
      
      - ``network_spec.yml`` - Network configuration
      - ``storage_config.yml`` - Storage configuration
   
   c. Commit and push the changes.

   For detailed parameter descriptions, see :doc:`../../reference/buildstream/configuration-tables`.

#. Manually trigger the pipeline with the updated parameters.

   .. TODO:: Add screenshot: GitLab New Pipeline dialog showing deploy selection

   a. Navigate to **Build** → **Pipelines**.
   
   b. Click **New Pipeline**.
   
   c. In the pipeline configuration dialog, select ``deploy`` from the dropdown list.
   
   d. Click **Run Pipeline** to execute the deploy pipeline.

#. Monitor the pipeline progress to ensure it completes successfully.

   a. Click on the running pipeline to view details.
   
   b. Monitor each stage as it progresses:
      - **deploy**: Deploys images to target nodes based on catalog specifications
      - **restart**: Restarts nodes to load the deployed images
      - **validate**: Validates that nodes are running the correct images

.. note::
   When using manual retry, ensure that only the necessary parameters are updated. Unnecessary changes may cause additional pipeline failures.

For troubleshooting common pipeline issues, see :doc:`../../troubleshooting/buildstream/common-pipeline-issues`.

Monitor Deploy Pipeline Progress
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Monitor the deploy pipeline progress through the GitLab web interface:

   .. TODO:: Add screenshot: GitLab deploy pipeline detail view showing stage progress

   a. Click on the running pipeline to view details.
   
   b. Monitor each stage as it progresses:
      - **deploy**: Deploys images to target nodes based on catalog specifications
      - **restart**: Restarts nodes to load the deployed images
      - **validate**: Validates that nodes are running the correct images

#. Review the stage status indicators:
   - |success| **Green checkmark**: Stage completed successfully
   - |failed| **Red X**: Stage failed (click for error details)
   - |running| **Blue circle**: Stage currently running

.. |success| image:: ../../../images/Icons/green_check.png
.. |failed| image:: ../../../images/Icons/red_x.png
.. |running| image:: ../../../images/Icons/blue_circle.png

#. If any stage fails, review the error logs by clicking on the failed job.

.. note::
   The deploy pipeline uses the PXE mapping file to determine which nodes receive which images based on functional group assignments.

Verification
------------

After the deploy pipeline completes, verify the deployment:

.. TODO:: Add screenshot: GitLab deploy pipeline completed status showing all stages passed

#. Check the overall pipeline status in GitLab to ensure all stages passed.

#. Verify that the target nodes have restarted and are accessible.

#. Log in to a sample of deployed nodes to verify the correct image is loaded.

#. Check the BuildStreaM API for deployment status and image group information.

Next Steps
----------

After successful deployment, configure PXE boot for the target nodes to load the deployed images. See :doc:`../management/configuring-pxe-boot`.

