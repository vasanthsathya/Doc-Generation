.. _how-to-buildstream-build-pipeline:

Building Omnia Images with BuildStreaM
=======================================

Build Omnia OS images using the BuildStreaM build pipeline. This procedure covers creating build jobs, executing build stages, and monitoring the build process through GitLab CI/CD or direct API calls.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before building images with BuildStreaM:

* Deploy and configure BuildStreaM container on OIM node (see :doc:`prepare_oim_buildstream`)
* Complete GitLab deployment for BuildStreaM (see :doc:`how-to-gitlab-deployment`)
* Verify access to the GitLab project repository
* Ensure input files are available in the build directory
* Configure OAuth 2.0 client credentials (if OAuth authentication is enabled)

Build Pipeline Overview
-----------------------

The BuildStreaM build pipeline automates the end-to-end image build process through sequential stages:

**Build Stages**

BuildStreaM executes the following build stages in mandatory sequential order:

| Stage | API Endpoint | Description |
|-------|-------------|-------------|
| ``create-local-repository`` | ``POST /api/v1/jobs/{job_id}/stages/create-local-repository`` | Creates a local package repository from input files via Ansible playbook |
| ``parse-catalog`` | ``POST /api/v1/jobs/{job_id}/stages/parse-catalog`` | Uploads and parses a Dell catalog JSON file to generate adapter policy output |
| ``build-image`` | ``POST /api/v1/jobs/{job_id}/stages/build-image`` | Builds the OS image using the local repository and parsed catalog output |

**Sequential Enforcement**

Each stage must complete successfully before the next stage can begin:

```
create-local-repository → MUST be COMPLETED
parse-catalog → MUST be COMPLETED  
build-image → CAN now execute
```

**Pipeline Architecture**

BuildStreaM uses a three-pipeline architecture:

* **BUILD Pipeline** — Prepare → Build → Verify stages
* **DEPLOY Pipeline** — Prepare → Deploy → Verify stages  
* **CLEANUP Pipeline** — Cleanup stage only

The ``pipeline_type`` parameter in the catalog metadata determines which child pipeline is triggered.

Procedure
---------

#. **Create a Build Job**

   Create a new build job to initiate the build pipeline.

   .. code-block:: bash

      curl -X POST https://<oim_host>:5001/api/v1/jobs \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>" \
        -H "X-Correlation-Id: <correlation_id>" \
        -H "Idempotency-Key: <unique_key>" \
        -H "Content-Type: application/json" \
        -d '{
          "client_id": "<client_id>",
          "client_name": "<client_name>"
        }'

   The response includes the ``job_id`` and initial stage states:

   .. code-block:: json

      {
        "job_id": "uuid",
        "state": "CREATED",
        "stages": [
          { "name": "create-local-repository", "state": "PENDING" },
          { "name": "parse-catalog", "state": "PENDING" },
          { "name": "build-image", "state": "PENDING" }
        ],
        "created_at": "2026-04-08T10:00:00Z",
        "client_id": "<client_id>"
      }

#. **Upload Input Files**

   Upload the required input files for the build pipeline.

   .. code-block:: bash

      curl -X PUT https://<oim_host>:5001/api/v1/jobs/{job_id}/upload \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>" \
        -F "input_files=@/path/to/input_files.tar.gz"

   .. note::
      BuildStreaM validates file names and formats against an allowlist. Maximum upload size is 5 MB per file.

#. **Execute create-local-repository Stage**

   Trigger the first build stage to create the local repository.

   .. code-block:: bash

      curl -X POST https://<oim_host>:5001/api/v1/jobs/{job_id}/stages/create-local-repository \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

   The stage transitions to ``IN_PROGRESS`` and returns ``202 Accepted``.

   .. code-block:: json

      {
        "job_id": "uuid",
        "stage": "create-local-repository",
        "status": "accepted",
        "submitted_at": "2026-04-08T10:01:00Z",
        "correlation_id": "string"
      }

#. **Execute parse-catalog Stage**

   Upload and parse the catalog JSON file.

   .. code-block:: bash

      curl -X POST https://<oim_host>:5001/api/v1/jobs/{job_id}/stages/parse-catalog \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>" \
        -F "catalog=@/path/to/catalog_rhel.json"

   BuildStreaM validates the JSON structure and processes the catalog to generate adapter policy output files.

#. **Execute build-image Stage**

   Build the OS image using the local repository and parsed catalog output.

   .. code-block:: bash

      curl -X POST https://<oim_host>:5001/api/v1/jobs/{job_id}/stages/build-image \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

   This stage produces one or more OS images as output artifacts and tags successful builds with a build identifier.

#. **Monitor Job Progress**

   Query the job status to monitor progress.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/jobs/{job_id} \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

   The response shows the current state of all stages:

   .. code-block:: json

      {
        "job_id": "uuid",
        "state": "IN_PROGRESS",
        "stages": [
          { "name": "create-local-repository", "state": "COMPLETED" },
          { "name": "parse-catalog", "state": "IN_PROGRESS" },
          { "name": "build-image", "state": "PENDING" }
        ],
        "created_at": "2026-04-08T10:00:00Z",
        "updated_at": "2026-04-08T10:05:00Z",
        "client_id": "<client_id>"
      }

**Alternative: GitLab CI/CD Pipeline**

To trigger the build pipeline using GitLab CI/CD:

#. Navigate to the GitLab project URL: ``https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>``
#. Go to **Code** → **Repository**
#. Locate the catalog file ``catalog_rhel.json``
#. Set ``pipeline_type`` to ``build`` in the catalog metadata
#. Commit and push the catalog changes to trigger the BUILD pipeline

Verification
------------

After the build pipeline completes, verify the results:

#. **Check Job Status**

   Navigate to **Build** → **Pipelines** in GitLab or query the API to confirm the job status is ``COMPLETED``.

#. **Review Build Artifacts**

   Retrieve the built images from the artifact store.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/jobs/{job_id}/artifacts/{label} \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

#. **Verify Image Group Status**

   Confirm that the image group is in ``BUILT`` state and ready for deployment.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/images \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

Troubleshooting
---------------

**Stage Fails with Prerequisite Error**

If a stage fails with ``STAGE_PREREQUISITE_PENDING``, ensure that all preceding stages have completed successfully before retrying.

**Catalog Validation Error**

If the catalog validation fails, verify that:

* The file has a ``.json`` extension
* The content is valid JSON
* The root element is a dictionary
* All required fields are present

**Immutability Constraint**

A completed build stage cannot be re-run. If you need to rebuild, create a new job.

Related Topics
--------------

* :doc:`how-to-buildstream-deploy-pipeline`
* :doc:`how-to-buildstream-validate-pipeline`
* :doc:`how-to-update-catalog-pipeline`
* :doc:`buildstream-architecture`