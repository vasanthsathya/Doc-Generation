.. _reference-buildstream-api:

BuildStreaM API Reference
=========================

.. note::
   This topic is pending SME validation. Content may change before publication.

Complete reference documentation for BuildStreaM REST API endpoints. Use these APIs to integrate BuildStreaM into your CI/CD pipelines and automation workflows.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStreaM provides a RESTful API for managing build jobs, catalogs, and monitoring workflow execution. The API uses OAuth 2.0 authentication and follows standard HTTP status codes.

**Base URL**: ``https://buildstream.example.com/api/v1``

**Authentication**: OAuth 2.0 Bearer tokens

**Content-Type**: ``application/json``

Authentication
--------------

All API requests must include an OAuth 2.0 Bearer token in the Authorization header:

.. code-block:: bash

   curl -H "Authorization: Bearer <your-oauth-token>" \
        https://buildstream.example.com/api/v1/jobs

Obtain tokens from your OAuth provider using the client credentials flow:

.. code-block:: bash

   curl -X POST "https://oauth-provider.com/oauth/token" \
        -d "grant_type=client_credentials&client_id=buildstream-client&client_secret=<secret>"

Jobs API
--------

### Create Job

Submit a new build job using a catalog.

.. code-block:: http

   POST /api/v1/jobs

**Request Body**:

.. code-block:: json

   {
     "catalog_path": "/path/to/catalog.yaml",
     "build_options": {
       "parallel_validation": false,
       "generate_sbom": true,
       "timeout": 3600,
       "retry_count": 3
     },
     "notification_settings": {
       "on_success": ["email"],
       "on_failure": ["email", "slack"],
       "recipients": ["admin@example.com"]
     }
   }

**Response**:

.. code-block:: json

   {
     "job_id": "job-20240301-001",
     "status": "submitted",
     "created_at": "2024-03-01T12:00:00Z",
     "stages": [
       "parse-catalog",
       "generate-input-files",
       "prepare-repos",
       "build-image",
       "validate-image",
       "validate-image-on-test",
       "promote"
     ]
   }

### Get Job Status

Retrieve the current status of a specific job.

.. code-block:: http

   GET /api/v1/jobs/{job_id}

**Response**:

.. code-block:: json

   {
     "job_id": "job-20240301-001",
     "status": "running",
     "current_stage": "build-image",
     "created_at": "2024-03-01T12:00:00Z",
     "started_at": "2024-03-01T12:01:30Z",
     "stages": [
       {
         "name": "parse-catalog",
         "status": "completed",
         "started_at": "2024-03-01T12:01:30Z",
         "completed_at": "2024-03-01T12:02:15Z"
       },
       {
         "name": "generate-input-files",
         "status": "completed",
         "started_at": "2024-03-01T12:02:15Z",
         "completed_at": "2024-03-01T12:03:45Z"
       },
       {
         "name": "prepare-repos",
         "status": "completed",
         "started_at": "2024-03-01T12:03:45Z",
         "completed_at": "2024-03-01T12:08:20Z"
       },
       {
         "name": "build-image",
         "status": "running",
         "started_at": "2024-03-01T12:08:20Z",
         "progress": 65
       }
     ]
   }

### List Jobs

Retrieve a list of all jobs with optional filtering.

.. code-block:: http

   GET /api/v1/jobs?status=running&limit=10&offset=0

**Query Parameters**:

- ``status``: Filter by job status (submitted, running, completed, failed)
- ``limit``: Maximum number of jobs to return (default: 50)
- ``offset``: Number of jobs to skip (default: 0)
- ``created_after``: Filter jobs created after this timestamp
- ``created_before``: Filter jobs created before this timestamp

**Response**:

.. code-block:: json

   {
     "jobs": [
       {
         "job_id": "job-20240301-001",
         "status": "running",
         "created_at": "2024-03-01T12:00:00Z"
       },
       {
         "job_id": "job-20240301-002",
         "status": "completed",
         "created_at": "2024-03-01T12:15:00Z"
       }
     ],
     "total_count": 25,
     "limit": 10,
     "offset": 0
   }

### Delete Job

Cancel and delete a job. Only works for jobs that haven't completed the promote stage.

.. code-block:: http

   DELETE /api/v1/jobs/{job_id}

**Response**:

.. code-block:: json

   {
     "job_id": "job-20240301-001",
     "status": "cancelled",
     "cancelled_at": "2024-03-01T12:30:00Z",
     "message": "Job cancelled successfully"
   }

Catalog API
-----------

### Validate Catalog

Validate a catalog file without submitting a build job.

.. code-block:: http

   POST /api/v1/catalog/validate

**Request Body**:

.. code-block:: json

   {
     "catalog_content": "catalog_version: \"1.0\"\n...",
     "strict_mode": true
   }

**Response**:

.. code-block:: json

   {
     "valid": true,
     "errors": [],
     "warnings": [
       "Package 'optional-package' has no validation dependencies"
     ],
     "summary": {
       "roles_count": 3,
       "packages_count": 15,
       "validation_dependencies_count": 8
     }
   }

### Get Catalog Schema

Retrieve the JSON schema for catalog files.

.. code-block:: http

   GET /api/v1/catalog/schema

**Response**:

.. code-block:: json

   {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "type": "object",
     "properties": {
       "catalog_version": {
         "type": "string",
         "pattern": "^\\d+\\.\\d+\\.\\d+$"
       },
       "description": {
         "type": "string",
         "maxLength": 500
       },
       "roles": {
         "type": "array",
         "items": {
           "$ref": "#/definitions/role"
         }
       }
     }
   }

Stages API
----------

### Get Stage Details

Retrieve detailed information about a specific job stage.

.. code-block:: http

   GET /api/v1/jobs/{job_id}/stages/{stage_name}

**Response**:

.. code-block:: json

   {
     "job_id": "job-20240301-001",
     "stage_name": "build-image",
     "status": "completed",
     "started_at": "2024-03-01T12:08:20Z",
     "completed_at": "2024-03-01T12:25:45Z",
     "duration": 1025,
     "logs": [
       {
         "timestamp": "2024-03-01T12:08:20Z",
         "level": "INFO",
         "message": "Starting image build for role: compute-node"
       },
       {
         "timestamp": "2024-03-01T12:15:30Z",
         "level": "INFO",
         "message": "Build progress: 45%"
       }
     ],
     "artifacts": [
       {
         "name": "compute-node.img",
         "size": 2147483648,
         "checksum": "sha256:abc123...",
         "location": "/opt/omnia/artifacts/job-20240301-001/"
       }
     ]
   }

### Retry Stage

Retry a failed stage (only available for certain stages).

.. code-block:: http

   POST /api/v1/jobs/{job_id}/stages/{stage_name}/retry

**Response**:

.. code-block:: json

   {
     "job_id": "job-20240301-001",
     "stage_name": "validate-image",
     "retry_count": 1,
     "status": "pending_retry",
     "message": "Stage retry queued"
   }

System API
----------

### Health Check

Check the health status of the BuildStreaM system.

.. code-block:: http

   GET /api/v1/health

**Response**:

.. code-block:: json

   {
     "status": "healthy",
     "version": "1.0.0",
     "uptime": 86400,
     "services": {
       "api": "running",
       "database": "connected",
       "orchestrator": "ready",
       "artifact_repository": "accessible"
     },
     "metrics": {
       "active_jobs": 3,
       "completed_jobs_today": 15,
       "average_build_time": 1800
     }
   }

### System Information

Get detailed system information and capabilities.

.. code-block:: http

   GET /api/v1/system/info

**Response**:

.. code-block:: json

   {
     "version": "1.0.0",
     "build_date": "2024-02-15T10:30:00Z",
     "capabilities": {
       "max_concurrent_builds": 1,
      "supported_os_types": ["rocky-linux", "ubuntu"],
       "supported_package_formats": ["rpm", "deb", "tar"],
       "validation_engines": ["basic", "comprehensive"]
     },
     "limits": {
       "max_catalog_size": 10485760,
       "max_job_duration": 7200,
       "max_artifact_size": 10737418240
     }
   }

Error Handling
--------------

BuildStreaM API uses standard HTTP status codes:

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Authentication failed
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., duplicate job)
- **422 Unprocessable Entity**: Validation failed
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service temporarily unavailable

**Error Response Format**:

.. code-block:: json

   {
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "Catalog validation failed",
       "details": {
         "field": "packages[0].version",
         "issue": "Invalid version format"
       },
       "correlation_id": "req-abc123"
     }
   }

Rate Limiting
-------------

API requests are rate limited to prevent abuse:

- **Authentication endpoints**: 10 requests per minute
- **Job submission**: 5 requests per minute
- **Status queries**: 100 requests per minute
- **Other endpoints**: 50 requests per minute

Rate limit headers are included in responses:

.. code-block:: http

   X-RateLimit-Limit: 100
   X-RateLimit-Remaining: 95
   X-RateLimit-Reset: 1677638400

Examples
--------

### Submit a Build Job

.. code-block:: bash

   # Submit a build job with custom options
   curl -X POST "https://buildstream.example.com/api/v1/jobs" \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{
          "catalog_path": "/opt/omnia/catalogs/hpc-cluster.yaml",
          "build_options": {
            "generate_sbom": true,
            "parallel_validation": false
          }
        }'

### Monitor Job Progress

.. code-block:: bash

   # Get job status
   curl -H "Authorization: Bearer <token>" \
        "https://buildstream.example.com/api/v1/jobs/job-20240301-001"

### Validate Catalog

.. code-block:: bash

   # Validate catalog before submission
   curl -X POST "https://buildstream.example.com/api/v1/catalog/validate" \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d '{"catalog_content": "'"$(cat catalog.yaml)"'"}'

Related Topics
--------------

* :doc:`../../buildstream/concept-architecture`
* :doc:`../../buildstream/how-to-get-started`
* :doc:`../../buildstream/how-to-gitlab-integration`
