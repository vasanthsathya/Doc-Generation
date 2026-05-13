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

#. Trigger the deploy pipeline using one of the following methods:

   **Automatic Trigger (PXE Mapping File Update)**:
   
   Update the ``pxe_mapping_file.csv`` file in the GitLab repository and commit the changes. The parent router (``.gitlab-ci.yml``) detects the PXE mapping file change and automatically triggers the deploy pipeline.

   **Manual Trigger**:
   
   a. Navigate to **Build** → **Pipelines**.
   
   b. Click **New Pipeline**.
   
   c. In the pipeline configuration dialog, select ``build`` from the dropdown list.
   
   d. Run the deploy stage.
   
.. note::
   The parent router (``.gitlab-ci.yml``) uses file change detection to automatically trigger the appropriate child pipeline. Changes to ``input/pxe_mapping_file.csv`` trigger the deploy pipeline, while changes to ``catalog_rhel.json`` trigger the build pipeline.

Monitor Deploy Pipeline Progress
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Monitor the deploy pipeline progress through the GitLab web interface:

   a. Click on the running pipeline to view details.
   
   b. Monitor each stage as it progresses:
      - **deploy**: Deploys images to target nodes based on catalog specifications
      - **restart**: Restarts nodes to load the deployed images
      - **validate**: Validates that nodes are running the correct images

#. Review the stage status indicators:
   - |success| **Green checkmark**: Stage completed successfully
   - |failed| **Red X**: Stage failed (click for error details)
   - |running| **Blue circle**: Stage currently running

.. |success| image:: ../../images/Icons/green_check.png
.. |failed| image:: ../../images/Icons/red_x.png
.. |running| image:: ../../images/Icons/blue_circle.png

#. If any stage fails, review the error logs by clicking on the failed job.

.. note::
   The deploy pipeline uses the PXE mapping file to determine which nodes receive which images based on functional group assignments.

Verification
------------

After the deploy pipeline completes, verify the deployment:

#. Check the overall pipeline status in GitLab to ensure all stages passed.

#. Verify that the target nodes have restarted and are accessible.

#. Log in to a sample of deployed nodes to verify the correct image is loaded.

#. Check the BuildStream API for deployment status and image group information.

Troubleshooting
---------------

If the deploy pipeline fails:

1. **Deploy stage fails**: 
   - Verify that the build pipeline completed successfully
   - Check that images are available in the local repository
   - Verify PXE mapping file configuration

2. **Restart stage fails**:
   - Verify BMC connectivity from the OIM
   - Check that nodes are powered on
   - Verify iDRAC credentials and permissions

3. **Validate stage fails**:
   - Verify network connectivity to nodes
   - Check that nodes completed the boot process
   - Review cloud-init logs on target nodes

For detailed troubleshooting guidance, see :doc:`../../troubleshooting/buildstream/common-pipeline-issues`.

Related Topics
--------------

* :doc:`../build/executing-build-pipeline` - Execute Build Pipeline
* :doc:`deploy/configuring-pxe-boot` - Configure PXE Boot
* :doc:`../../reference/buildstream/pipeline-stages` - Pipeline Stages Reference
* :doc:`../../reference/buildstream/configuration-tables` - Configuration Reference