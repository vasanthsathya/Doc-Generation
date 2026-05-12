.. _how-to-buildstream-update-catalog-pipeline:

Step 5: Update Catalog and Execute Omnia BuildStreaM Pipeline
===============================================================
Update the ``catalog_rhel.json`` file and monitor pipeline execution through GitLab. This procedure covers catalog modifications, automatic pipeline triggering, and verification of pipeline status and job execution.

Prerequisites
-------------

Before updating catalogs and checking pipelines:

* Deploy and Configure BuildStreaM Container on OIM Node (see :doc:`prepare_oim_buildstream`)
* GitLab deployment for BuildStreaM is completed (see :doc:`how-to-gitlab-deployment`)
* Confirm that you can access GitLab project repository

BuildStreaM Catalog Structure
----------------------------------------

BuildStreaM introduces an enhanced catalog structure with support for pipeline type selection and OAuth authentication:

**Pipeline Type Selection**
   The catalog metadata includes a ``pipeline_type`` parameter that determines which child pipeline is triggered:

   - ``build`` - Triggers the BUILD pipeline (Prepare, Build, Verify stages)
   - ``deploy`` - Triggers the DEPLOY pipeline (Prepare, Deploy, Verify stages)
   - ``cleanup`` - Triggers the CLEANUP pipeline (removes stale artifacts)

**OAuth Authentication Configuration**
   If OAuth 2.0 is enabled in the BuildStream configuration, include the following parameters in the catalog metadata:

   - ``oauth_enabled`` - Set to ``true`` to enable OAuth authentication
   - ``oauth_client_id`` - OAuth client identifier (configured in ``omnia_auth.service``)
   - ``oauth_token_url`` - OAuth token endpoint URL (typically ``https://<oim_host>:<auth_port>/oauth/token``)
   - ``oauth_scope`` - OAuth token scope (e.g., ``buildstream:read buildstream:write``)

** Catalog Example**

   .. code-block:: json

      {
        "metadata": {
          "pipeline_type": "build",
          "oauth_enabled": true,
          "oauth_client_id": "buildstream-client",
          "oauth_token_url": "https://oim.example.com:8443/oauth/token",
          "oauth_scope": "buildstream:read buildstream:write"
        },
        "images": [
          {
            "name": "rhel-10.0-compute",
            "functional_group": "compute",
            "architecture": "x86_64",
            "os_type": "RHEL",
            "os_version": "10.0",
            "package_type": "image"
          }
        ]
      }

**Pipeline Stages**
   BuildStreaM uses the following pipeline stages:

   - **Prepare** - Sets up the build environment and validates catalog entries
   - **Build** - Builds the specified images (BUILD pipeline only)
   - **Deploy** - Deploys images to cluster nodes (DEPLOY pipeline only)
   - **Verify** - Validates the build or deployment results
   - **Cleanup** - Removes stale artifacts and frees storage (CLEANUP pipeline only)

Procedure
---------

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
       

5. To trigger the pipeline, commit and push catalog changes.

.. note::
   * BuildStreaM uses a three-pipeline architecture (parent router + dynamic child pipelines). The parent pipeline (``.gitlab-ci.yml``) analyzes the catalog and triggers the appropriate child pipeline (BUILD, DEPLOY, or CLEANUP) based on the ``pipeline_type`` parameter.
   * Each child pipeline processes the catalog entries independently and executes the corresponding workflow stages.
   * BuildStream pipeline behaviour is controlled by the GitLab CI/CD configuration in your environment.   

The following image shows the BuildStreaM pipeline is currently running and the stages are being executed:

   .. image:: ../images/buildstream_pipeline_running.png
   
6. Perform the following steps to track the pipeline progress through the GitLab web interface:

      a. Navigate to **Build** → **Pipeline**.
      b. Click on the running pipeline to view details.
      c. Monitor the parent pipeline status and the triggered child pipeline:

         **Parent Pipeline Stages**:
            - **parse-catalog**: Parses catalog file and determines pipeline type
            - **trigger-child-pipeline**: Triggers the appropriate child pipeline based on ``pipeline_type``

         **Child Pipeline Stages**:
            - **BUILD Pipeline**: Prepare → Build → Verify
            - **DEPLOY Pipeline**: Prepare → Deploy → Verify
            - **CLEANUP Pipeline**: Cleanup

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

After successful execution of the pipeline, do one of the following:

* Manually PXE boot the nodes to deploy the images.
* Use the PXE boot utility to deploy the images. See :doc:`set_pxe_boot_order_buildstream` for detailed instructions.

.. note::
   BuildStreaM introduces a three-pipeline architecture with simplified stages (Prepare, Build, Deploy, Verify, Cleanup) and OAuth 2.0 authentication support. For detailed information on  pipeline architecture and catalog configuration, see :doc:`buildstream-release2-pipelines` and :doc:`buildstream-release2-api-reference`.
