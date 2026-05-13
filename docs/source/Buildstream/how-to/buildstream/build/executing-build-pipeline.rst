.. _executing-build-pipeline:

Execute Build Pipeline
======================

Update the ``catalog_rhel.json`` file and execute the Omnia BuildStreaM build pipeline through GitLab. This procedure covers catalog modifications, pipeline triggering (automatic and manual), and verification of pipeline status and job execution.

The BuildStream build pipeline automates the creation of diskless images based on catalog specifications. The pipeline consists of four sequential stages:

* **parse-catalog**: Parses and validates the catalog file for build requirements
* **create-local-repository**: Creates and configures the local repository for build artifacts
* **generate-input-files**: Generates input files and configuration data for image building
* **build-image**: Builds the diskless images based on catalog specifications

The build pipeline is automatically triggered when you update the ``catalog_rhel.json`` file in the GitLab repository, or can be manually initiated through the GitLab interface.

Prerequisites
-------------

Before updating catalogs and checking pipelines:

* Deploy and Configure BuildStreaM Container on OIM Node (see :doc:`../setup/preparing-oim-buildstream`)
* GitLab deployment for BuildStreaM is completed (see :doc:`../setup/deploying-gitlab-buildstream`)
* Confirm that you can access GitLab project repository

Procedure
---------

1. Go to the GitLab project URL::

    https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

2. Go to **Code** → **Repository**.

   .. TODO:: Add screenshot: GitLab Code → Repository view showing catalog file location

3. Locate the catalog file ``catalog_rhel.json``.
4. Modify the ``catalog_rhel.json`` file to define your build requirements.

.. note:: Ensure that the catalog file is updated with valid functional group names, architecture types, operating system types and versions, and package types. The pipeline fails if invalid details are provided.

   The following are the supported values:
      - **Functional group names**: For supported functional group names, see :ref:`functional-groups-section`.
      - **Architecture type**: ``x86_64`` and ``aarch64``.
      - **OS type**: ``RHEL``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **OS version**: ``10.0``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **Package types**: ``rpm``, ``rpm_repo``, ``image``, ``iso``, ``tarball``, ``pip_module``, ``git``, ``manifest``.

5. Trigger the build pipeline by committing and pushing the catalog changes. The pipeline triggers automatically when catalog changes are committed.

6. Monitor the pipeline progress to ensure it completes successfully. See :ref:`Monitor Pipeline Progress <monitor-pipeline-progress>` for detailed instructions.

.. note:: 
   * Currently, BuildStreaM supports only one catalog file and one pipeline trigger. BuildStreaM pipeline behaviour is controlled by the GitLab CI/CD configuration in your environment.
   * Each pipeline processes the catalog changes independently and builds the specified images according to the catalog requirements.   
   * If the pipeline fails, you can use the manual retry procedure to update input parameters and retry the pipeline.

Manual Pipeline Retry After Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the build pipeline fails, you can update the input parameters in the input files and manually retry the pipeline. 

Procedure
---------

#. Identify the failure reason by reviewing the pipeline logs in GitLab.

   .. TODO:: Add screenshot: GitLab failed pipeline view showing error logs

   a. Navigate to **Build** → **Pipelines**.
   
   b. Click on the failed pipeline.
   
   c. Click on the failed stage to view error logs.

#. Update the input parameters in the GitLab repository.

   **Update Catalog File**:
   
   a. Navigate to the GitLab project repository.
   
   b. Edit the ``catalog_rhel.json`` file to fix catalog-related issues.
   
   c. Commit and push the changes.

   **Update Input Configuration Files**:
   
   a. Navigate to the ``input/`` folder in the GitLab repository.
   
   b. Edit the relevant configuration file:
      
      - ``local_repo_config.yml`` - Local repository configuration
      - ``network_spec.yml`` - Network configuration
      - ``provision_config.yml`` - Provision configuration
      - ``storage_config.yml`` - Storage configuration
      - ``telemetry_config.yml`` - Telemetry configuration
   
   c. Commit and push the changes.

   For detailed parameter descriptions, see :doc:`../../../reference/buildstream/configuration-tables`.

#. Manually trigger the pipeline with the updated parameters.

   .. TODO:: Add screenshot: GitLab New Pipeline dialog showing build selection

   a. Navigate to **Build** → **Pipelines**.
   
   b. Click **New Pipeline**.
   
   c. In the pipeline configuration dialog, select ``build`` from the dropdown list.
   
   d. Click **Run Pipeline** to execute the build pipeline.

#. Monitor the pipeline progress to ensure it completes successfully. See :ref:`Monitor Pipeline Progress <monitor-pipeline-progress>` for detailed instructions.

For troubleshooting common pipeline issues, see :doc:`../../troubleshooting/buildstream/common-pipeline-issues`.

.. _monitor-pipeline-progress:

Monitor Pipeline Progress
~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor the build pipeline progress through the GitLab web interface to track stage execution and identify any issues.

.. TODO:: Add screenshot: GitLab pipeline detail view showing stage progress

1. Navigate to **Build** → **Pipeline**.
   
2. Click on the running pipeline to view details.
   
3. Monitor each stage as it progresses:
   - **parse-catalog**: Parses and validates the catalog file for build requirements
   - **create-local-repository**: Creates and configures the local repository for build artifacts
   - **generate-input-files**: Generates input files and configuration data for image building
   - **build-image**: Builds the diskless images based on catalog specifications

4. Review the stage status indicators:
   - |success| **Green checkmark**: Stage completed successfully
   - |failed| **Red X**: Stage failed (click for error details)
   - |running| **Blue circle**: Stage currently running

5. If any stage fails, review the error logs by clicking on the failed job.

.. |success| image:: ../../../../images/Icons/green_check.png
.. |failed| image:: ../../../../images/Icons/red_x.png
.. |running| image:: ../../../../images/Icons/blue_circle.png

The following image shows the BuildStreaM pipeline is currently running and the stages are being executed:

   .. image:: ../../../../images/buildstream_pipeline_running.png

.. note::
   The build pipeline uses the catalog file to determine which images to build based on functional group assignments.

Verification
------------

After the pipeline is completed, you can check the overall pipeline status and job execution.

.. TODO:: Add screenshot: GitLab Pipelines list showing completed pipeline status

1. Navigate to **Build** → **Pipelines**
2. Review the job list and status.

.. TODO:: Add screenshot: GitLab job detail view showing execution logs and resource usage

3. Click on individual jobs to view:
      - Execution logs
      - Resource usage
      - Error messages (if any)

Next Steps
-----------

After successful execution of the build pipeline, proceed with deploying the images to cluster nodes. See :doc:`../deploy/executing-deploy-pipeline` for detailed instructions on executing the deploy pipeline.
