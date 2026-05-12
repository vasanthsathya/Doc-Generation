.. _buildstream-api-reference:

BuildStream API Reference
==========================

BuildStream provides a comprehensive RESTful API for orchestrating image build, deployment, validation, and cleanup workflows. This reference documents all available API endpoints, authentication methods, request/response schemas, and error handling.

API Overview
------------

The BuildStream API is a RESTful service that accepts HTTP requests and returns JSON responses. All API endpoints require OAuth 2.0 authentication using JWT bearer tokens.

**Base URL:** ``https://<buildstream-host>:5001/api/v1``

**Authentication:** OAuth 2.0 client credentials flow with JWT bearer tokens

**Content Type:** ``application/json``

Authentication
--------------

BuildStream uses OAuth 2.0 client credentials for authentication. Clients must obtain a JWT token before making API requests.

### OAuth 2.0 Client Credentials Flow

**Token Request:**

.. code-block:: http

   POST /oauth/token HTTP/1.1
   Host: <oauth-server>:4444
   Content-Type: application/x-www-form-urlencoded

   grant_type=client_credentials&client_id=<client_id>&client_secret=<client_secret>&scope=buildstream:read buildstream:write

**Token Response:**

.. code-block:: json

   {
     "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "Bearer",
     "expires_in": 3600,
     "scope": "buildstream:read buildstream:write"
   }

### Using JWT Tokens in API Requests

Include the JWT token in the ``Authorization`` header:

.. code-block:: http

   GET /api/v1/jobs/{job_id} HTTP/1.1
   Host: <buildstream-host>:5001
   Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
   Content-Type: application/json

### Common Request Headers

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Header
     - Required
     - Description
   * - ``Authorization``
     - Yes
     - Bearer JWT token (``Bearer <token>``)
   * - ``Content-Type``
     - Yes
     - ``application/json``
   * - ``X-Client-Id``
     - Yes
     - Client identifier for request tracking
   * - ``X-Correlation-Id``
     - Yes
     - Unique request correlation ID for tracing
   * - ``Idempotency-Key``
     - Yes
     - Unique key for request deduplication

### Common Response Codes

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Code
     - Meaning
   * - ``200 OK``
     - Request succeeded
   * - ``202 Accepted``
     - Request accepted for asynchronous processing
   * - ``400 Bad Request``
     - Invalid request parameters
   * - ``401 Unauthorized``
     - Missing or invalid authentication
   * - ``403 Forbidden``
     - Insufficient permissions
   * - ``404 Not Found``
     - Resource not found
   * - ``409 Conflict``
     - Request conflicts with current state
   * - ``422 Unprocessable Entity``
     - Valid request but semantic errors
   * - ``500 Internal Server Error``
     - Server error

Job Management Endpoints
-------------------------

### POST /api/v1/jobs

Create a new build Job.

**Request Headers:**

.. code-block:: http

   Authorization: Bearer <jwt_token>
   X-Client-Id: gitlab-ci
   X-Correlation-Id: req-12345
   Idempotency-Key: unique-key-123
   Content-Type: application/json

**Request Body:**

.. code-block:: json

   {
     "client_id": "gitlab-ci",
     "client_name": "GitLab CI/CD Pipeline"
   }

**Response (201 Created):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "state": "CREATED",
     "stages": [
       {
         "name": "parse-catalog",
         "state": "PENDING"
       },
       {
         "name": "generate-input-files",
         "state": "PENDING"
       },
       {
         "name": "create-local-repository",
         "state": "PENDING"
       },
       {
         "name": "build-image",
         "state": "PENDING"
       }
     ],
     "created_at": "2026-05-11T10:00:00Z",
     "client_id": "gitlab-ci"
   }

**Error Responses:**

- ``401 Unauthorized`` - Invalid or missing JWT token
- ``409 Conflict`` - Duplicate ``Idempotency-Key``

### GET /api/v1/jobs/{job_id}

Retrieve the current status of a Job by Job ID.

**Request Headers:**

.. code-block:: http

   Authorization: Bearer <jwt_token>
   X-Client-Id: gitlab-ci
   X-Correlation-Id: req-12346

**Response (200 OK):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "state": "IN_PROGRESS",
     "stages": [
       {
         "name": "parse-catalog",
         "state": "COMPLETED"
       },
       {
         "name": "generate-input-files",
         "state": "IN_PROGRESS"
       },
       {
         "name": "create-local-repository",
         "state": "PENDING"
       },
       {
         "name": "build-image",
         "state": "PENDING"
       }
     ],
     "created_at": "2026-05-11T10:00:00Z",
     "updated_at": "2026-05-11T10:05:00Z",
     "client_id": "gitlab-ci"
   }

**Error Responses:**

- ``401 Unauthorized`` - Invalid or missing JWT token
- ``403 Forbidden`` - Client does not own this Job
- ``404 Not Found`` - Job does not exist

### DELETE /api/v1/jobs/{job_id}

Delete a Job and perform cleanup of associated artifacts and images.

**Request Headers:**

.. code-block:: http

   Authorization: Bearer <jwt_token>
   X-Client-Id: gitlab-ci
   X-Correlation-Id: req-12347

**Response (204 No Content):**

No response body on success.

**Error Responses:**

- ``401 Unauthorized`` - Invalid or missing JWT token
- ``403 Forbidden`` - Client does not own this Job
- ``404 Not Found`` - Job does not exist
- ``409 Conflict`` - Image Group is in an active state
- ``412 Precondition Failed`` - Job has already been cleaned

File Management Endpoints
-------------------------

### PUT /api/v1/jobs/{job_id}/upload

Upload configuration files and catalogs for the build pipeline.

**Request Headers:**

.. code-block:: http

   Authorization: Bearer <jwt_token>
   X-Client-Id: gitlab-ci
   X-Correlation-Id: req-12348
   Idempotency-Key: unique-key-124
   Content-Type: multipart/form-data

**Request Body (multipart/form-data):**

.. code-block:: text

   catalog: [catalog file]
   config_files: [configuration files]

**File Upload Constraints:**

- Maximum file size: 5 MB per file
- Maximum archive size: 50 MB uncompressed, 500 entries
- Allowed file types: JSON, YAML, CSV, TXT
- Path traversal sequences (``../``) are rejected
- Empty files are rejected

**Response (200 OK):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "uploaded_files": [
       "catalog_rhel.json",
       "network_config.yml"
     ],
     "uploaded_at": "2026-05-11T10:02:00Z"
   }

**Error Responses:**

- ``400 Bad Request`` - Invalid file format or path traversal
- ``413 Payload Too Large`` - File exceeds size limit
- ``404 Not Found`` - Job does not exist
- ``422 Unprocessable Entity`` - File validation failed

### GET /api/v1/jobs/{job_id}/artifacts/{label}

Retrieve artifacts generated during pipeline execution.

**Request Headers:**

.. code-block:: http

   Authorization: Bearer <jwt_token>
   X-Client-Id: gitlab-ci
   X-Correlation-Id: req-12349

**Path Parameters:**

- ``label`` - Artifact label (e.g., ``catalog``, ``config``, ``logs``)

**Response (200 OK):**

Returns the artifact file content.

**Error Responses:**

- ``401 Unauthorized`` - Invalid or missing JWT token
- ``403 Forbidden`` - Client does not own this Job
- ``404 Not Found`` - Job or artifact does not exist

Image Management Endpoints
-------------------------

### GET /api/v1/images

List all built Image Groups with constituent image details.

**Request Headers:**

.. code-block:: http

   Authorization: Bearer <jwt_token>
   X-Client-Id: gitlab-ci
   X-Correlation-Id: req-12350

**Query Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 15 35

   * - Parameter
     - Type
     - Required
     - Default
     - Description
   * - ``status``
     - string
     - No
     - All
     - Filter by Image Group status (``BUILT``, ``DEPLOYED``, ``PASSED``, etc.)
   * - ``limit``
     - integer
     - No
     - 50
     - Maximum number of results to return
   * - ``offset``
     - integer
     - No
     - 0
     - Number of results to skip for pagination

**Response (200 OK):**

.. code-block:: json

   {
     "image_groups": [
       {
         "image_group_id": "image-build19",
         "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
         "status": "BUILT",
         "created_at": "2026-05-11T10:30:00Z",
         "constituent_images": [
           {
             "role": "slurm_controller_node",
             "image_name": "slurm_controller.img",
             "s3_path": "s3://boot-images/slurm_controller.img"
           },
           {
             "role": "slurm_node",
             "image_name": "slurm_node.img",
             "s3_path": "s3://boot-images/slurm_node.img"
           }
         ]
       }
     ],
     "total_count": 1,
     "limit": 50,
     "offset": 0
   }

**Error Responses:**

- ``401 Unauthorized`` - Invalid or missing JWT token
- ``400 Bad Request`` - Invalid query parameters

Stage Execution Endpoints
-------------------------

### POST /api/v1/jobs/{job_id}/stages/{stage_name}

Execute a specific pipeline stage.

**Request Headers:**

.. code-block:: http

   Authorization: Bearer <jwt_token>
   X-Client-Id: gitlab-ci
   X-Correlation-Id: req-12351
   Idempotency-Key: unique-key-125
   Content-Type: application/json

**Path Parameters:**

- ``stage_name`` - Stage name (``parse-catalog``, ``generate-input-files``, ``create-local-repository``, ``build-image``, ``deploy``, ``restart``, ``validate``)

**Request Body (varies by stage):**

**For deploy stage:**

.. code-block:: json

   {
     "image_group_id": "image-build19"
   }

**For restart stage:**

.. code-block:: json

   {
     "disable_pxe_boot": false
   }

**For validate stage:**

.. code-block:: json

   {
     "test_suite": "basic",
     "timeout": 600
   }

**Response (202 Accepted):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "deploy",
     "status": "accepted",
     "submitted_at": "2026-05-11T11:00:00Z",
     "correlation_id": "req-12351"
   }

**Error Responses:**

- ``401 Unauthorized`` - Invalid or missing JWT token
- ``403 Forbidden`` - Client does not own this Job
- ``404 Not Found`` - Job does not exist
- ``409 Conflict`` - Stage prerequisites not met or stage already active
- ``422 Unprocessable Entity`` - Invalid request body for stage type

### Stage-Specific Error Codes

**Deploy Stage:**

- ``IMAGE_GROUP_NOT_FOUND`` - Image Group does not exist
- ``IMAGE_NOT_DEPLOYABLE`` - Image Group not in ``BUILT`` state
- ``IMAGE_JOB_MISMATCH`` - Image Group belongs to different Job
- ``IMAGE_ALREADY_DEPLOYED`` - Image Group already deployed (re-deployment requires new Job)

**Restart Stage:**

- ``PXE_MAPPING_NOT_FOUND`` - PXE mapping file not found
- ``NODE_DISCOVERY_FAILED`` - Node discovery failed

**Validate Stage:**

- ``VALIDATION_TIMEOUT`` - Validation tests exceeded timeout
- ``TEST_SUITE_NOT_FOUND`` - Specified test suite does not exist

Error Handling
-------------

### Error Response Format

All error responses follow this format:

.. code-block:: json

   {
     "error_code": "ERROR_CODE",
     "error_message": "Human-readable error message",
     "error_details": {
       "field": "additional_context"
     },
     "correlation_id": "req-12345",
     "timestamp": "2026-05-11T10:00:00Z"
   }

### Common Error Codes

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Error Code
     - HTTP Status
     - Description
   * - ``UNAUTHORIZED``
     - 401
     - Invalid or missing authentication
   * - ``FORBIDDEN``
     - 403
     - Insufficient permissions
   * - ``JOB_NOT_FOUND``
     - 404
     - Job does not exist
   * - ``IMAGE_GROUP_NOT_FOUND``
     - 404
     - Image Group does not exist
   * - ``FILE_NOT_FOUND``
     - 404
     - Requested file or artifact does not exist
   * - ``STAGE_NOT_FOUND``
     - 404
     - Stage does not exist
   * - ``INVALID_REQUEST``
     - 400
     - Invalid request parameters
   * - ``FILE_TOO_LARGE``
     - 413
     - Uploaded file exceeds size limit
   * - ``FILE_EMPTY``
     - 400
     - Uploaded file is empty
   * - ``FILE_PATH_TRAVERSAL``
     - 400
     - Path traversal detected in file upload
   * - ``FILE_FORMAT_INVALID``
     - 422
     - Invalid file format
   * - ``FILE_JSON_INVALID``
     - 400
     - Invalid JSON content
   * - ``STAGE_PREREQUISITE_PENDING``
     - 409
     - Prerequisite stages not completed
   * - ``IMAGE_NOT_DEPLOYABLE``
     - 409
     - Image Group not in deployable state
   * - ``IMAGE_ALREADY_DEPLOYED``
     - 409
     - Image Group already deployed
   * - ``STAGE_ALREADY_ACTIVE``
     - 409
     - Stage already in progress
   * - ``CONFLICT``
     - 409
     - Request conflicts with current state
   * - ``PRECONDITION_FAILED``
     - 412
     - Precondition for operation failed
   * - ``INTERNAL_ERROR``
     - 500
     - Internal server error

### Idempotency

BuildStream API supports idempotent operations using the ``Idempotency-Key`` header. When a request with the same ``Idempotency-Key`` and ``client_id`` is received, the API returns the original response without creating a duplicate resource.

**Idempotency Rules:**

- Job creation: Duplicate requests return the same Job ID
- Stage execution: Duplicate requests return the same stage execution ID
- File upload: Duplicate requests overwrite existing files

**Example Idempotency-Key Usage:**

.. code-block:: http

   POST /api/v1/jobs HTTP/1.1
   Idempotency-Key: gitlab-build-20250511-001
   X-Client-Id: gitlab-ci

Rate Limiting
-------------

BuildStream API implements rate limiting to prevent abuse and ensure fair resource allocation.

**Rate Limits:**

- Job creation: 10 requests per minute per client
- Stage execution: 30 requests per minute per client
- File upload: 5 requests per minute per client
- Other endpoints: 100 requests per minute per client

**Rate Limit Response:**

When rate limits are exceeded, the API returns:

.. code-block:: http

   HTTP/1.1 429 Too Many Requests
   X-RateLimit-Limit: 10
   X-RateLimit-Remaining: 0
   X-RateLimit-Reset: 1715427200

   {
     "error_code": "RATE_LIMIT_EXCEEDED",
     "error_message": "Rate limit exceeded. Please retry later."
   }

API Usage Examples
-----------------

### Complete Build Workflow Example

**1. Create Job:**

.. code-block:: bash

   curl -X POST https://buildstream.example.com:5001/api/v1/jobs \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-001" \
     -H "Idempotency-Key: build-20250511-001" \
     -H "Content-Type: application/json" \
     -d '{"client_id": "gitlab-ci", "client_name": "GitLab CI/CD"}'

**2. Upload Catalog:**

.. code-block:: bash

   curl -X PUT https://buildstream.example.com:5001/api/v1/jobs/{job_id}/upload \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "X-Correlation-Id: build-002" \
     -F "catalog=@catalog_rhel.json" \
     -F "config=@network_config.yml"

**3. Execute Build Stages:**

.. code-block:: bash

   # Parse catalog
   curl -X POST https://buildstream.example.com:5001/api/v1/jobs/{job_id}/stages/parse-catalog \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

   # Generate input files
   curl -X POST https://buildstream.example.com:5001/api/v1/jobs/{job_id}/stages/generate-input-files \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

   # Create local repository
   curl -X POST https://buildstream.example.com:5001/api/v1/jobs/{job_id}/stages/create-local-repository \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

   # Build image
   curl -X POST https://buildstream.example.com:5001/api/v1/jobs/{job_id}/stages/build-image \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**4. Query Job Status:**

.. code-block:: bash

   curl -X GET https://buildstream.example.com:5001/api/v1/jobs/{job_id} \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

### Deploy Workflow Example

**1. List Available Images:**

.. code-block:: bash

   curl -X GET "https://buildstream.example.com:5001/api/v1/images?status=BUILT" \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**2. Deploy Image Group:**

.. code-block:: bash

   curl -X POST https://buildstream.example.com:5001/api/v1/jobs/{job_id}/stages/deploy \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "Content-Type: application/json" \
     -d '{"image_group_id": "image-build19"}'

**3. Restart Nodes:**

.. code-block:: bash

   curl -X POST https://buildstream.example.com:5001/api/v1/jobs/{job_id}/stages/restart \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "Content-Type: application/json" \
     -d '{"disable_pxe_boot": false}'

**4. Validate Deployment:**

.. code-block:: bash

   curl -X POST https://buildstream.example.com:5001/api/v1/jobs/{job_id}/stages/validate \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci" \
     -H "Content-Type: application/json" \
     -d '{"test_suite": "basic", "timeout": 600}'

Related Topics
--------------

* :doc:`buildstream-architecture`
* :doc:`buildstream-pipelines`
* :doc:`buildstream-resume-retry`

.. note::
   For architectural details about the three-pipeline model, see :doc:`buildstream-architecture`. For pipeline execution procedures, see :doc:`buildstream-pipelines`.

.. [SME VALIDATION REQUIRED: Verify all API endpoints, request/response schemas, and error codes against actual BuildStream API implementation]
