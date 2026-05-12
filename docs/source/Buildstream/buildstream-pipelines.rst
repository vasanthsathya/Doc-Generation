.. _buildstream-pipelines:

BuildStreaM GitLab CI/CD Pipeline Configuration
===============================================

This guide provides GitLab CI/CD pipeline configuration examples for BuildStreaM. For step-by-step execution procedures, see the pipeline-specific how-to guides: :doc:`how-to-buildstream-build-pipeline`, :doc:`how-to-buildstream-deploy-pipeline`, and :doc:`how-to-buildstream-validate-pipeline`.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before configuring BuildStreaM GitLab CI/CD pipelines:

* BuildStreaM API service running and accessible
* GitLab instance deployed and configured (see :doc:`how-to-gitlab-deployment`)
* OAuth 2.0 client credentials configured (if OAuth authentication is enabled)
* BuildStreaM project repository created in GitLab

Pipeline Architecture Overview
-----------------------------

BuildStreaM uses a parent pipeline router with dynamic child pipeline generation. For detailed architectural information, see :doc:`buildstream-architecture`.

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

| Variable | Description | Example |
|----------|-------------|---------|
| ``BUILDSTREAM_API`` | BuildStreaM API endpoint | ``https://<oim-host>:5001/api/v1`` |
| ``JWT_TOKEN`` | OAuth access token (if OAuth enabled) | Obtained via OAuth flow |
| ``BS_OAUTH_CLIENT_ID`` | OAuth client ID | ``buildstream-client`` |
| ``BS_OAUTH_CLIENT_SECRET`` | OAuth client secret | ``[your-secret]`` |
| ``OAUTH_TOKEN_URL`` | OAuth token endpoint | ``https://<oim-host>:8443/oauth/token`` |

Pipeline Execution
------------------

**Triggering Pipelines**

* **Build Pipeline**: Commit changes to ``catalog_rhel.json`` or configuration files
* **Deploy Pipeline**: Commit changes to ``pxe_mapping_file.csv``
* **Cleanup Pipeline**: Manually trigger from GitLab web interface

**Monitoring Pipeline Execution**

1. Navigate to **Build** → **Pipelines** in GitLab
2. Click on the running pipeline to view details
3. Monitor parent pipeline status and triggered child pipeline
4. Access job logs for each stage

**Pipeline Artifacts**

* Job ID and image group information stored as pipeline artifacts
* Build logs and test results available as job artifacts
* Artifacts retained according to GitLab retention policy

Troubleshooting
---------------

**Pipeline Fails to Start**

* Verify BuildStreaM API is accessible from GitLab runner
* Check OAuth token retrieval (if OAuth enabled)
* Ensure required environment variables are configured

**Stage Fails with Authentication Error**

* Verify JWT token is valid and not expired
* Check OAuth client credentials are correct
* Ensure token has required scopes (``buildstream:read``, ``buildstream:write``)

**Child Pipeline Not Triggered**

* Verify parent pipeline configuration is correct
* Check catalog ``pipeline_type`` parameter matches expected values
* Review GitLab trigger rules and conditions

Related Topics
--------------

* :doc:`buildstream-architecture`
* :doc:`how-to-buildstream-build-pipeline`
* :doc:`how-to-buildstream-deploy-pipeline`
* :doc:`how-to-buildstream-validate-pipeline`
* :doc:`buildstream-resume-retry`

.. note::
   This guide focuses on GitLab CI/CD configuration. For architectural details, see :doc:`buildstream-architecture`. For step-by-step API usage, see the pipeline-specific how-to guides.