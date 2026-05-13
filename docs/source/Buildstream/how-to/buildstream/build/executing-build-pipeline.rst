.. _executing-build-pipeline:

Execute Build Pipeline
======================

Update the ``catalog_rhel.json`` file and execute the Omnia BuildStreaM build pipeline through GitLab. This procedure covers catalog modifications, pipeline triggering (automatic and manual), and verification of pipeline status and job execution.

Prerequisites
-------------

Before updating catalogs and checking pipelines:

* Deploy and Configure BuildStreaM Container on OIM Node (see :doc:`../setup/preparing-oim-buildstream`)
* GitLab deployment for BuildStreaM is completed (see :doc:`../setup/deploying-gitlab-buildstream`)
* Confirm that you can access GitLab project repository

Procedure
---------

Update Catalog and Trigger Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to the GitLab project URL::

    https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

2. Go to **Code** → **Repository**.
3. Locate the catalog file ``catalog_rhel.json``.
4. Modify the ``catalog_rhel.json`` file to define your build requirements.

.. note:: Ensure that the catalog file is updated with valid functional group names, architecture types, operating system types and versions, and package types. The pipeline fails if invalid details are provided.

   The following are the supported values:
      - **Functional group names**: For supported functional group names, see :ref:`functional-groups-section`.
      - **Architecture type**: ``x86_64`` and ``aarch64``.
      - **OS type**: ``RHEL``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **OS version**: ``10.0``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **Package types**: ``rpm``, ``rpm_repo``, ``image``, ``iso``, ``tarball``, ``pip_module``, ``git``, ``manifest``.

5. Trigger the build pipeline using one of the following methods:

   **Automatic Trigger (Recommended)**:
   
   Commit and push the catalog changes. The pipeline triggers automatically when catalog changes are committed.

   **Manual Trigger**:
   
   a. Navigate to **Build** → **Pipelines**.
   
   b. Click **New Pipeline**.
   
   c. In the pipeline configuration dialog, enter ``build`` as the pipeline type.
   
   d. Click **Run Pipeline** to execute the build pipeline.

.. note:: 
   * Currently, BuildStream supports only one catalog file and one pipeline trigger. BuildStream pipeline behaviour is controlled by the GitLab CI/CD configuration in your environment.
   * Each pipeline processes the catalog changes independently and builds the specified images according to the catalog requirements.   
   * Manual trigger is useful when you want to execute the pipeline without making catalog changes.

The following image shows the BuildStreaM pipeline is currently running and the stages are being executed:

   .. image:: ../images/buildstream_pipeline_running.png
   
Monitor Pipeline Progress
~~~~~~~~~~~~~~~~~~~~~~~~~

6. Perform the following steps to track the pipeline progress through the GitLab web interface:

      a. Navigate to **Build** → **Pipeline**.
      b. Click on the running pipeline to view details.
      c. Monitor each stage as it progresses:
            - **create-local-repository**: Creates and configures the local repository for build artifacts
            - **parse-catalog**: Parses and validates the catalog file for build requirements
            - **generate-input-files**: Generates input files and configuration data for image building
            - **build-image**: Builds the diskless images based on catalog specifications

The following image shows each stage of the BuildStreaM pipeline and its status:
   .. image:: ../images/buildstream_pipeline_stages.png  

   Expected pipeline status indicators:
      - |success| **Green checkmark**: Stage completed successfully
      - |failed| **Red X**: Stage failed (click for error details)
      - |running| **Blue circle**: Stage currently running

.. |success| image:: ../images/Icons/green_check.png
.. |failed| image:: ../images/Icons/red_x.png
.. |running| image:: ../images/Icons/blue_circle.png

The following image shows overall pipeline status:
   .. image:: ../images/buildstream_pipeline_passed.png

Image Groups Overview
~~~~~~~~~~~~~~~~~~~~~

BuildStream uses **Image Groups** to organize and manage the images created during the build process. Each Image Group has a 1:1 mapping with a Job ID, ensuring traceability and management of built images.

* **Image Group**: A collection of constituent images built for a specific functional group
* **Job ID**: Unique identifier for the build pipeline execution
* **Constituent Images**: Individual images within an Image Group (e.g., base image, package images)
* **Functional Group Mapping**: Image Groups are mapped to functional groups for deployment

The build pipeline automatically creates Image Groups based on the catalog specifications. You can view Image Group details through the BuildStream API or GitLab pipeline logs.
      
Verification
------------

After the pipeline is completed, you can check the overall pipeline status and job execution.

1. Navigate to **Build** → **Pipelines**
2. Review the job list and status.
3. Click on individual jobs to view:
      - Execution logs
      - Resource usage
      - Error messages (if any)

Next Steps
-----------

After successful execution of the build pipeline, proceed with deploying the images to cluster nodes. See :doc:`../deploy/executing-deploy-pipeline` for detailed instructions on executing the deploy pipeline.
