.. _buildstream-pipelines:

BuildStream Pipeline Workflows
==============================

BuildStream introduces a three-pipeline architecture that separates build, deployment, and validation workflows. This guide provides step-by-step instructions for executing each pipeline type.

Prerequisites
-------------

Before executing BuildStream pipelines, ensure the following:

- **BuildStream API Service Running**
  - BuildStream container is running and accessible
  - PostgreSQL database is operational
  - Playbook watcher service is active

- **OAuth Authentication**
  - OAuth client credentials configured
  - Valid JWT token available for API requests

- **GitLab CI/CD Configuration**
  - Three-pipeline GitLab CI/CD configuration deployed
  - Parent pipeline router configured
  - Dynamic child pipeline generation enabled

- **Input Files Prepared**
  - Catalog JSON file (``catalog_rhel.json``) for build pipeline
  - Configuration files for build pipeline
  - PXE mapping file (``pxe_mapping_file.csv``) for deploy pipeline

Build Pipeline Workflow
----------------------

The Build Pipeline creates OS images from catalog definitions and configuration files. It is triggered by changes to catalog or configuration files.

Step 1: Create Job
~~~~~~~~~~~~~~~~~~

Create a new Job to track the build pipeline execution.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-001" \
     -H "Idempotency-Key: build-$(date +%Y%m%d-%H%M%S)" \
     -H "Content-Type: application/json" \
     -d '{
       "client_id": "gitlab-ci",
       "client_name": "GitLab CI/CD Pipeline"
     }'

**Expected Response:**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "state": "CREATED",
     "stages": [
       {"name": "parse-catalog", "state": "PENDING"},
       {"name": "generate-input-files", "state": "PENDING"},
       {"name": "create-local-repository", "state": "PENDING"},
       {"name": "build-image", "state": "PENDING"}
     ],
     "created_at": "2026-05-11T10:00:00Z",
     "client_id": "gitlab-ci"
   }

Record the ``job_id`` for subsequent steps.

Step 2: Upload Input Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload catalog and configuration files to the BuildStream input directory.

.. code-block:: bash

   curl -X PUT https://<buildstream-host>:5001/api/v1/jobs/{job_id}/upload \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-002" \
     -F "catalog=@catalog_rhel.json" \
     -F "network_config=@network_config.yml" \
     -F "local_repo_config=@local_repo_config.yml"

**File Upload Constraints:**

   - Maximum file size: 5 MB per file
   - Maximum archive size: 50 MB uncompressed
   - Allowed file types: JSON, YAML, CSV, TXT
   - Path traversal sequences (``../``) are rejected

Step 3: Execute Parse Catalog Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parse the catalog JSON file to generate adapter policy output.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/parse-catalog \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-003" \
     -H "Content-Type: multipart/form-data" \
     -F "catalog=@catalog_rhel.json"

**Expected Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "parse-catalog",
     "status": "accepted",
     "submitted_at": "2026-05-11T10:01:00Z",
     "correlation_id": "build-003"
   }

Step 4: Execute Generate Input Files Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate input files from the parsed catalog output.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/generate-input-files \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-004"

**Expected Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "generate-input-files",
     "status": "accepted",
     "submitted_at": "2026-05-11T10:02:00Z",
     "correlation_id": "build-004"
   }

Step 5: Execute Create Local Repository Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a local package repository from input files via Ansible playbook.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/create-local-repository \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-005"

**Expected Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "create-local-repository",
     "status": "accepted",
     "submitted_at": "2026-05-11T10:03:00Z",
     "correlation_id": "build-005"
   }

Step 6: Execute Build Image Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build the OS image using the local repository and parsed catalog output.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/build-image \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-006"

**Expected Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "build-image",
     "status": "accepted",
     "submitted_at": "2026-05-11T10:04:00Z",
     "correlation_id": "build-006"
   }

Step 7: Monitor Job Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor the Job status and stage execution progress.

.. code-block:: bash

   curl -X GET https://<buildstream-host>:5001/api/v1/jobs/{job_id} \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**Expected Response (COMPLETED):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "state": "COMPLETED",
     "stages": [
       {"name": "parse-catalog", "state": "COMPLETED"},
       {"name": "generate-input-files", "state": "COMPLETED"},
       {"name": "create-local-repository", "state": "COMPLETED"},
       {"name": "build-image", "state": "COMPLETED"}
     ],
     "created_at": "2026-05-11T10:00:00Z",
     "updated_at": "2026-05-11T10:30:00Z",
     "client_id": "gitlab-ci"
   }

Step 8: Verify Build Completion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verify that the Image Group was created successfully.

.. code-block:: bash

   curl -X GET "https://<buildstream-host>:5001/api/v1/images?status=BUILT" \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**Expected Response:**

.. code-block:: json

   {
     "image_groups": [
       {
         "image_group_id": "image-build19",
         "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
         "status": "BUILT",
         "created_at": "2026-05-11T10:30:00Z",
         "constituent_images": [...]
       }
     ],
     "total_count": 1
   }

Deploy & Validate Pipeline Workflow
---------------------------------

The Deploy & Validate Pipeline deploys built images to target nodes, restarts nodes via PXE boot, and validates the deployment. It is triggered by PXE mapping file changes.

Step 1: Select Image Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List available Image Groups and select the one to deploy.

.. code-block:: bash

   curl -X GET "https://<buildstream-host>:5001/api/v1/images?status=BUILT" \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

Record the ``image_group_id`` and ``job_id`` for deployment.

Step 2: Upload Updated Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload updated configuration files for deployment.

.. code-block:: bash

   curl -X PUT https://<buildstream-host>:5001/api/v1/jobs/{job_id}/upload \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -F "pxe_mapping=@pxe_mapping_file.csv"

Step 3: Execute Deploy Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deploy the Image Group to target nodes.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/deploy \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "Content-Type: application/json" \
     -d '{"image_group_id": "image-build19"}'

**Expected Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "deploy",
     "status": "accepted",
     "submitted_at": "2026-05-11T11:00:00Z",
     "correlation_id": "deploy-001"
   }

**Image Group State Transition:** ``BUILT`` → ``DEPLOYING`` → ``DEPLOYED``

Step 4: Execute Restart Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Restart target nodes via PXE boot with node diff handling.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/restart \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "Content-Type: application/json" \
     -d '{"disable_pxe_boot": false}'

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ``disable_pxe_boot`` | boolean | No | ``false`` | If ``true``, skip PXE boot for this restart request |

**Expected Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "restart",
     "status": "accepted",
     "submitted_at": "2026-05-11T11:15:00Z",
     "correlation_id": "deploy-002"
   }

**Image Group State Transition:** ``DEPLOYED`` → ``RESTARTING`` → ``RESTARTED``

**Node Diff Logic:** Only newly added nodes (not previously booted with the current image) are PXE-booted.

Step 5: Execute Validate Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validate the deployment via Molecule test framework.

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/validate \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "Content-Type: application/json" \
     -d '{"test_suite": "basic", "timeout": 600}'

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ``test_suite`` | string | No | All basic tests | Specific test suite to run (``smoke``, ``sanity``, ``regression``) |
| ``timeout`` | integer | No | 600 | Timeout in seconds |

**Expected Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "validate",
     "status": "accepted",
     "submitted_at": "2026-05-11T11:30:00Z",
     "correlation_id": "deploy-003"
   }

**Image Group State Transition:** ``RESTARTED`` → ``VALIDATING`` → ``PASSED`` or ``FAILED``

Step 6: Monitor Deployment Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor the Job status to track deployment progress.

.. code-block:: bash

   curl -X GET https://<buildstream-host>:5001/api/v1/jobs/{job_id} \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**Expected Response (PASSED):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "state": "COMPLETED",
     "stages": [
       {"name": "deploy", "state": "COMPLETED"},
       {"name": "restart", "state": "COMPLETED"},
       {"name": "validate", "state": "COMPLETED"}
     ],
     "created_at": "2026-05-11T11:00:00Z",
     "updated_at": "2026-05-11T12:00:00Z",
     "client_id": "gitlab-ci"
   }

CleanUp Pipeline Workflow
------------------------

The CleanUp Pipeline removes artifacts and images for completed or failed Jobs. It can be triggered manually or via scheduled automation.

Step 1: Select Job for Cleanup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List Jobs and select the one to clean up.

.. code-block:: bash

   curl -X GET "https://<buildstream-host>:5001/api/v1/images" \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

Step 2: Execute CleanUp
~~~~~~~~~~~~~~~~~~~~~~~~

Delete the Job and perform cleanup of associated artifacts and images.

.. code-block:: bash

   curl -X DELETE https://<buildstream-host>:5001/api/v1/jobs/{job_id} \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: cleanup-001"

**Expected Response (204 No Content):**

No response body on success.

**Cleanup Actions:**

   - Deletes all built OS images from S3 storage (``s3://boot-images``)
   - Removes NFS artifact files (config files, catalog JSON, generated inputs)
   - Transitions Image Group to ``CLEANED`` state
   - Marks Job status as ``CLEANED``
   - Records audit event with cleanup details

**Image Group State Transition:** Any state → ``CLEANED``

Step 3: Verify Cleanup
~~~~~~~~~~~~~~~~~~~~~

Verify that the Job and Image Group are in ``CLEANED`` state.

.. code-block:: bash

   curl -X GET https://<buildstream-host>:5001/api/v1/jobs/{job_id} \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**Expected Response:**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "state": "CLEANED",
     "created_at": "2026-05-11T10:00:00Z",
     "updated_at": "2026-05-11T14:00:00Z",
     "client_id": "gitlab-ci"
   }

GitLab CI/CD Pipeline Configuration
---------------------------------

BuildStream uses a parent pipeline router with dynamic child pipeline generation.

Parent Pipeline (.gitlab-ci.yml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Build Pipeline (.gitlab-ci-build.yml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
       - curl -X POST $BUILDSTREAM_API/jobs -H "Authorization: Bearer $JWT_TOKEN" -d '{"client_id": "gitlab-ci"}'
     artifacts:
       reports:
         job_artifact: job_id.json

   parse-catalog:
     stage: parse-catalog
     script:
       - JOB_ID=$(cat job_id.json | jq -r '.job_id')
       - curl -X PUT $BUILDSTREAM_API/jobs/$JOB_ID/upload -F "catalog=@catalog_rhel.json"
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/parse-catalog -F "catalog=@catalog_rhel.json"
     dependencies:
       - initialization

   # ... additional stages ...

Deploy Pipeline (.gitlab-ci-deploy.yml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
       - curl -X GET "$BUILDSTREAM_API/images?status=BUILT" -H "Authorization: Bearer $JWT_TOKEN" > images.json
       - cat images.json
     artifacts:
       reports:
         job_artifact: images.json

   deploy:
     stage: deploy
     script:
       - IMAGE_GROUP_ID=$(cat images.json | jq -r '.image_groups[0].image_group_id')
       - JOB_ID=$(cat images.json | jq -r '.image_groups[0].job_id')
       - curl -X PUT $BUILDSTREAM_API/jobs/$JOB_ID/upload -F "pxe_mapping=@pxe_mapping_file.csv"
       - curl -X POST $BUILDSTREAM_API/jobs/$JOB_ID/stages/deploy -d "{\"image_group_id\": \"$IMAGE_GROUP_ID\"}"
     dependencies:
       - select-image

   # ... additional stages ...

Verification
------------

After executing any pipeline, verify the following:

**Build Pipeline Verification:**

   - [ ] Job state is ``COMPLETED``
   - [ ] All stages show ``COMPLETED`` status
   - [ ] Image Group created with ``BUILT`` status
   - [ ] Constituent images listed in Image Group
   - [ ] S3 storage contains built images

**Deploy Pipeline Verification:**

   - [ ] Job state is ``COMPLETED``
   - [ ] All stages show ``COMPLETED`` status
   - [ ] Image Group status is ``PASSED``
   - [ ] Target nodes are accessible
   - [ ] Services are running on deployed nodes

**CleanUp Pipeline Verification:**

   - [ ] Job state is ``CLEANED``
   - [ ] Image Group status is ``CLEANED``
   - [ ] S3 storage no longer contains Job images
   - [ ] NFS artifacts removed
   - [ ] Audit event recorded

**Next Steps**

After successful pipeline execution:

   - **Build Pipeline:** Proceed to deploy the built images using the Deploy Pipeline
   - **Deploy Pipeline:** Monitor cluster performance and validate node functionality
   - **CleanUp Pipeline:** Verify storage cleanup and audit trail completeness

Related Topics
--------------

* :doc:`buildstream-architecture`
* :doc:`buildstream-api-reference`
* :doc:`buildstream-resume-retry`
* :doc:`buildstream_troubleshooting`

.. note::
   This guide covers BuildStream pipeline workflows. For architectural details, see :doc:`buildstream-architecture`.

.. [SME VALIDATION REQUIRED: Verify all pipeline steps, stage names, and API usage against actual BuildStream implementation]
