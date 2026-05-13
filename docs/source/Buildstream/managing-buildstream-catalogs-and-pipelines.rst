.. _managing-buildstream-catalogs-and-pipelines:

Managing BuildStreaM Catalogs and Pipelines
===========================================

Manage BuildStreaM catalogs and execute build, deploy, and validate pipelines through GitLab or direct API calls. This comprehensive guide covers catalog modifications, pipeline type selection, GitLab CI/CD configuration, and step-by-step execution procedures for each pipeline type.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before managing catalogs and pipelines:

* Deploy and configure BuildStreaM container on OIM node (see :doc:`prepare_oim_buildstream`)
* Complete GitLab deployment for BuildStreaM (see :doc:`how-to-gitlab-deployment`)
* Verify access to the GitLab project repository

BuildStreaM Catalog Structure
----------------------------------------

BuildStreaM uses an enhanced catalog structure with support for pipeline type selection:

**Pipeline Type Selection**

   The catalog metadata includes a ``pipeline_type`` parameter that determines which child pipeline is triggered:

   - ``build`` - Triggers the BUILD pipeline (see :doc:`how-to-buildstream-build-pipeline`)
   - ``deploy`` - Triggers the DEPLOY pipeline (see :doc:`how-to-buildstream-deploy-pipeline`)
   - ``cleanup`` - Triggers the CLEANUP pipeline (removes stale artifacts)

**OAuth Authentication Configuration**

   If OAuth 2.0 is enabled in the BuildStreaM configuration, include the following parameters in the catalog metadata:

   - ``oauth_enabled`` - Set to ``true`` to enable OAuth authentication
   - ``oauth_client_id`` - OAuth client identifier (configured in ``omnia_auth.service``)
   - ``oauth_token_url`` - OAuth token endpoint URL (typically ``https://<oim_host>:<auth_port>/oauth/token``)
   - ``oauth_scope`` - OAuth token scope (e.g., ``buildstream:read buildstream:write``)

   For OAuth configuration details, see :doc:`buildstream-architecture`.

**Catalog Example**

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

Catalog Management Procedure
----------------------------

#. **Navigate to the GitLab project URL**

   Navigate to:

   .. code-block:: text

      https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

#. **Locate the catalog file**

   Go to **Code** → **Repository** and locate the catalog file ``catalog_rhel.json``.

#. **Modify the catalog file**

   Modify the ``catalog_rhel.json`` file to define your build requirements.

   .. note:: Ensure that the catalog file is updated with valid functional group names, architecture types, operating system types and versions, and package types. The pipeline fails if invalid details are provided.

   The following are the supported values:
      - **Functional group names**: For supported functional group names, see :ref:`functional-groups-section`.
      - **Architecture type**: ``x86_64`` and ``aarch64``.
      - **OS type**: ``RHEL``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **OS version**: ``10.0``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **Package types**: ``rpm``, ``rpm_repo``, ``image``, ``iso``, ``tarball``, ``pip_module``, ``git``, ``manifest``.

#. **Set the pipeline type**

   Configure the ``pipeline_type`` parameter in the catalog metadata to trigger the appropriate pipeline:

   - Set to ``build`` to trigger the build pipeline
   - Set to ``deploy`` to trigger the deploy pipeline
   - Set to ``cleanup`` to trigger the cleanup pipeline

#. **Commit and push catalog changes**

   To trigger the pipeline, commit and push catalog changes.

   .. note::
      BuildStreaM uses a three-pipeline architecture (parent router + dynamic child pipelines). The parent pipeline (``.gitlab-ci.yml``) analyzes the catalog and triggers the appropriate child pipeline (BUILD, DEPLOY, or CLEANUP) based on the ``pipeline_type`` parameter.
      Each child pipeline processes the catalog entries independently and executes the corresponding workflow stages.
      BuildStreaM pipeline behaviour is controlled by the GitLab CI/CD configuration in your environment.

Pipeline Execution Procedures
------------------------------

For detailed step-by-step procedures for each pipeline type, see the following topics:

.. toctree::
   :maxdepth: 1

   how-to-buildstream-build-pipeline
   how-to-buildstream-deploy-pipeline
   how-to-buildstream-validate-pipeline

GitLab CI/CD Pipeline Configuration
-----------------------------------

BuildStreaM uses a parent pipeline router with dynamic child pipeline generation. This section provides GitLab CI/CD pipeline configuration examples.

**Parent Pipeline Router**

The parent pipeline (``.gitlab-ci.yml``) acts as a router that analyzes the catalog file and dynamically generates child pipelines based on the ``pipeline_type`` parameter in the catalog metadata.

**Dynamic Child Pipelines**

* **BUILD Pipeline** (``.gitlab-ci-build.yml``) — Triggered by ``pipeline_type: build``
* **DEPLOY Pipeline** (``.gitlab-ci-deploy.yml``) — Triggered by ``pipeline_type: deploy``
* **CLEANUP Pipeline** (``.gitlab-ci-cleanup.yml``) — Triggered by ``pipeline_type: cleanup``

Parent Pipeline Configuration (.gitlab-ci.yml)
--------------------------------------------

The parent pipeline routes to appropriate child pipelines based on catalog changes.

.. code-block:: yaml

   stages:
     - build
     - deploy
     - cleanup

   variables:
     PIPELINE_TYPE: "parent"

   build_pipeline:
     stage: build
     trigger:
       include:
         - project: 'your-gitlab-project'
           file: '.gitlab-ci-build.yml'
           ref: main
     rules:
       - changes:
           - catalog_rhel.json
           - config_files/
       - when: always

   deploy_pipeline:
     stage: deploy
     trigger:
       include:
         - project: 'your-gitlab-project'
           file: '.gitlab-ci-deploy.yml'
           ref: main
       strategy: depend
     rules:
       - changes:
           - pxe_mapping_file.csv
       - when: always

   cleanup_pipeline:
     stage: cleanup
     trigger:
       include:
         - project: 'your-gitlab-project'
           file: '.gitlab-ci-cleanup.yml'
           ref: main
     when: manual

Build Pipeline Configuration (.gitlab-ci-build.yml)
--------------------------------------------------

The build pipeline executes the image build workflow through sequential stages.

.. code-block:: yaml

   stages:
     - initialization
     - parse-catalog
     - generate-input-files
     - create-local-repository
     - build-image
     - summary

   variables:
     PIPELINE_TYPE: "build"

   initialization:
     stage: initialization
     script:
       - echo "Initializing build pipeline"
       - curl -X POST $BUILDSTREAM_API/jobs \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" \
         -H "Content-Type: application/json" \
         -d '{"client_id": "gitlab-ci", "client_name": "GitLab CI/CD Pipeline"}'
     artifacts:
       reports:
         job_artifact: job_id.json

   parse-catalog:
     stage: parse-catalog
     script:
       - JOB_ID=$(cat job_id.json | jq -r '.job_id')
       - curl -X PUT $BUILDSTREAM_API/jobs/$JOB_ID/upload \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" \
         -F "catalog=@catalog_rhel.json"
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/parse-catalog \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" \
         -F "catalog=@catalog_rhel.json"
     dependencies:
       - initialization

   generate-input-files:
     stage: generate-input-files
     script:
       - JOB_ID=$(cat job_id.json | jq -r '.job_id')
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/generate-input-files \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci"
     dependencies:
       - parse-catalog

   create-local-repository:
     stage: create-local-repository
     script:
       - JOB_ID=$(cat job_id.json | jq -r '.job_id')
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/create-local-repository \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci"
     dependencies:
       - generate-input-files

   build-image:
     stage: build-image
     script:
       - JOB_ID=$(cat job_id.json | jq -r '.job_id')
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/build-image \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci"
     dependencies:
       - create-local-repository

   summary:
     stage: summary
     script:
       - JOB_ID=$(cat job_id.json | jq -r '.job_id')
       - curl -X GET $BUILDSTREAM_API/jobs/$JOB_ID \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci"
     dependencies:
       - build-image

Deploy Pipeline Configuration (.gitlab-ci-deploy.yml)
----------------------------------------------------

The deploy pipeline executes the deployment workflow through deploy, restart, and validate stages.

.. code-block:: yaml

   stages:
     - select-image
     - deploy
     - restart
     - validate
     - summary

   variables:
     PIPELINE_TYPE: "deploy"

   select-image:
     stage: select-image
     script:
       - echo "Selecting image for deployment"
       - curl -X GET "$BUILDSTREAM_API/images?status=BUILT" \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" > images.json
       - cat images.json
     artifacts:
       reports:
         job_artifact: images.json

   deploy:
     stage: deploy
     script:
       - IMAGE_GROUP_ID=$(cat images.json | jq -r '.image_groups[0].image_group_id')
       - JOB_ID=$(cat images.json | jq -r '.image_groups[0].job_id')
       - curl -X PUT $BUILDSTREAM_API/jobs/$JOB_ID/upload \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" \
         -F "pxe_mapping=@pxe_mapping_file.csv"
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/deploy \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" \
         -H "Content-Type: application/json" \
         -d "{\"image_group_id\": \"$IMAGE_GROUP_ID\"}"
     dependencies:
       - select-image

   restart:
     stage: restart
     script:
       - JOB_ID=$(cat images.json | jq -r '.image_groups[0].job_id')
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/restart \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" \
         -H "Content-Type: application/json" \
         -d '{"disable_pxe_boot": false}'
     dependencies:
       - deploy

   validate:
     stage: validate
     script:
       - JOB_ID=$(cat images.json | jq -r '.image_groups[0].job_id')
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/validate \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" \
         -H "Content-Type: application/json" \
         -d '{"test_suite": "basic", "timeout": 600}'
     dependencies:
       - restart

   summary:
     stage: summary
     script:
       - JOB_ID=$(cat images.json | jq -r '.image_groups[0].job_id')
       - curl -X GET $BUILDSTREAM_API/jobs/$JOB_ID \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci"
     dependencies:
       - validate

Cleanup Pipeline Configuration (.gitlab-ci-cleanup.yml)
------------------------------------------------------

The cleanup pipeline removes artifacts and images for specified jobs.

.. code-block:: yaml

   stages:
     - select-job
     - cleanup
     - verify

   variables:
     PIPELINE_TYPE: "cleanup"

   select-job:
     stage: select-job
     script:
       - echo "Selecting job for cleanup"
       - curl -X GET "$BUILDSTREAM_API/images" \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci" > images.json
       - cat images.json
     artifacts:
       reports:
         job_artifact: images.json

   cleanup:
     stage: cleanup
     script:
       - JOB_ID=$(cat images.json | jq -r '.image_groups[0].job_id')
       - curl -X DELETE $BUILDSTREAM_API/jobs/$JOB_ID \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci"
     dependencies:
       - select-job

   verify:
     stage: verify
     script:
       - JOB_ID=$(cat images.json | jq -r '.image_groups[0].job_id')
       - curl -X GET $BUILDSTREAM_API/jobs/$JOB_ID \
         -H "Authorization: Bearer $JWT_TOKEN" \
         -H "X-Client-Id: gitlab-ci"
     dependencies:
       - cleanup

OAuth Authentication Integration
------------------------------

If OAuth 2.0 authentication is enabled, include token retrieval in your pipeline configuration.

.. code-block:: yaml

   before_script:
     - |
       # Obtain OAuth token
       JWT_TOKEN=$(curl -X POST $OAUTH_TOKEN_URL \
         -d "grant_type=client_credentials" \
         -d "client_id=$BS_OAUTH_CLIENT_ID" \
         -d "client_secret=$BS_OAUTH_CLIENT_SECRET" \
         -d "scope=buildstream:read buildstream:write" \
         | jq -r '.access_token')
       export JWT_TOKEN

Environment Variables
---------------------

Configure the following environment variables in your GitLab project settings:

.. list-table:: GitLab Environment Variables
   :widths: 30 50 20
   :header-rows: 1

   * - Variable
     - Description
     - Example
   * - ``BUILDSTREAM_API``
     - BuildStreaM API endpoint
     - ``https://<oim-host>:5001/api/v1``
   * - ``JWT_TOKEN``
     - OAuth access token (if OAuth enabled)
     - Obtained via OAuth flow
   * - ``BS_OAUTH_CLIENT_ID``
     - OAuth client ID
     - ``buildstream-client``
   * - ``BS_OAUTH_CLIENT_SECRET``
     - OAuth client secret
     - ``[your-secret]``
   * - ``OAUTH_TOKEN_URL``
     - OAuth token endpoint
     - ``https://<oim-host>:8443/oauth/token``

Monitoring Pipeline Execution
-----------------------------

#. **Track pipeline progress through GitLab**

   The following image shows the BuildStreaM pipeline currently running and the stages being executed:

   .. image:: ../images/buildstream_pipeline_running.png

   Perform the following steps to track the pipeline progress through the GitLab web interface:

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

#. **Review stage status**

   The following image shows each stage of the BuildStreaM pipeline and its status:

   .. image:: ../images/buildstream_pipeline_stages.png

   Expected pipeline status indicators:
      - |success| **Green checkmark**: Stage completed successfully
      - |failed| **Red X**: Stage failed (click for error details)
      - |running| **Blue circle**: Stage currently running

.. |success| image:: ../images/Icons/green_check.png
.. |failed| image:: ../images/Icons/red_x.png
.. |running| image:: ../images/Icons/blue_circle.png

#. **Check overall pipeline status**

   The following image shows overall pipeline status:

   .. image:: ../images/buildstream_pipeline_passed.png

Verification
------------

After the pipeline is completed, verify the following:

1. Navigate to **Build** → **Pipelines**
2. Review the job list and status.
3. Click on individual jobs to view:
      - Execution logs
      - Resource usage
      - Error messages (if any)

Next Steps
-----------

After successful execution of the pipeline:

* For build pipelines, proceed to deployment (see :doc:`how-to-buildstream-deploy-pipeline`)
* For deploy pipelines, proceed to validation (see :doc:`how-to-buildstream-validate-pipeline`)
* Manually PXE boot the nodes to deploy the images if needed
* Use the PXE boot utility to deploy the images. See :doc:`set_pxe_boot_order_buildstream` for detailed instructions.

.. note::
   BuildStreaM uses a three-pipeline architecture with parent router and dynamic child pipelines. For detailed information on pipeline architecture, see :doc:`buildstream-architecture`. For OAuth configuration details, see :doc:`buildstream-architecture`.

Related Topics
--------------

* :doc:`buildstream-architecture`
* :doc:`buildstream-resume-retry`
* :doc:`buildstream_troubleshooting`