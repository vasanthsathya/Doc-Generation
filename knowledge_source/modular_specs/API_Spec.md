# BuildStream Release 2 API Specification

**Version:** 2.0  
**Date:** March 31, 2026  
**Author:** Rajeshkumar S  
**Status:** Draft  
**Base URL:** `https://api.buildstream.example.com/api/v1`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Authentication](#2-authentication)
3. [Common Concepts](#3-common-concepts)
4. [API Endpoints](#4-api-endpoints)
   - 4.1 [Job Management](#41-job-management)
      - 4.1.1 [Create Job](#411-create-job)
      - 4.1.2 [Get Job](#412-get-job)
   - 4.2 [Upload API](#42-upload-api)
   - 4.3 [ListImages API](#43-listimages-api)
   - 4.4 [Deploy API](#44-deploy-api)
   - 4.5 [ReStart API](#45-restart-api)
   - 4.6 [Validate API](#46-validate-api)
   - 4.7 [CleanUp API](#47-cleanup-api)
5. [API Flow Sequence](#5-api-flow-sequence)
6. [Error Handling](#6-error-handling)
7. [HTTP Status Codes](#7-http-status-codes)
8. [Data Models](#8-data-models)
   - 8.1 [Job Model](#81-job-model)
   - 8.2 [ImageGroup Model](#82-imagegroup-model)
   - 8.3 [Stage Model](#83-stage-model)
   - 8.4 [Database Schema](#84-database-schema)
   - 8.5 [Deploy Pipeline Pydantic Schemas](#85-deploy-pipeline-pydantic-schemas)
   - 8.6 [State Machine Precondition Matrix](#86-state-machine-precondition-matrix)
   - 8.7 [Deploy Pipeline DB Write Summary](#87-deploy-pipeline-db-write-summary)
9. [Security Considerations](#9-security-considerations)
10. [Versioning](#10-versioning)
11. [OpenAPI 3.0 Compatibility](#11-openapi-30-compatibility)

---

## 1. Overview

### 1.1 Purpose

The BuildStream Release 2 API provides enhanced REST endpoints for managing infrastructure build and deploy workflows. These APIs can be invoked in two contexts:

1. **Pipeline Context**: Integrated within GitLab CI/CD pipelines for automated workflows
2. **Direct Invocation**: Independent API calls by external clients, UI applications, or orchestration systems

The APIs enable clients to:

- Upload configuration files and catalogs via a unified Upload endpoint
- List available Image Groups with Job ID mappings
- Deploy, restart, and validate built images
- Clean up artifacts and images after completion
- Manage jobs and stages independently or as part of orchestrated workflows

### 1.2 Architecture

BuildStream Release 2 supports both pipeline and direct invocation patterns:

#### Pipeline Architecture (Automated Workflows)
```
Build Pipeline: Create Job → Upload → Parse → Generate → Create Repo → Build Image
                (Job ID established, 1:1 JobID ↔ ImageGroupID mapping created)

Deploy Pipeline: ListImages → Select → Upload → Deploy → ReStart → Validate
                (Same Job ID reused, ImageGroup status transitions)
```

**Pipeline Constraints & Setup**:
- **Concurrency**: Simultaneous invocation of the Build and Deploy pipelines for the same or different jobs is **not supported**. The system assumes sequential operation where build completes before deploy begins.
- **Initial Setup**: As part of the initial GitLab configuration triggered by the gitlab playbook, all required configuration files (`local_repo_config.yml`, `network_spec.yml`, `provision_config.yml`, `pxe_mapping_file.csv`, `storage_config.yml`, `telemetry_config.yml`), the catalog (`catalog_rhel.json`), and pipeline definitions are automatically copied to the repository.

#### Direct Invocation Architecture (Independent API Calls)
```
Direct API Usage: Create Job → Upload → Execute Stages → Clean Up
                  (Any stage can be called independently based on preconditions)
                  (pipeline_phase is optional, defaults to appropriate context)
```

#### Hybrid Architecture
Clients can mix pipeline and direct invocation patterns, allowing for:
- Pipeline-created jobs to be managed via direct API calls
- Direct API-created jobs to be continued by pipeline stages
- Flexible workflow orchestration across different systems

### 1.3 API Characteristics

| Characteristic | Value |
|----------------|-------|
| **Protocol** | HTTPS (TLS 1.2+) |
| **Format** | JSON (application/json) |
| **Authentication** | OAuth 2.0 Client Credentials + JWT Bearer Tokens |
| **Encoding** | UTF-8 |
| **Max Request Size** | 5 MB (configurable) |

---

## 2. Authentication

Authentication follows the same OAuth 2.0 Client Credentials flow as Release 1. Refer to the [Base API Specification](API_SPECIFICATION.md#2-authentication) for complete details.

### 2.1 Required Scopes

| Endpoint | Required Scope | Description |
|----------|----------------|-------------|
| Upload API | `catalog:write` | Upload files to job artifacts |
| ListImages API | `catalog:read` | List available image groups |
| Deploy API | `job:write` | Trigger deployment stage |
| ReStart API | `job:write` | Trigger restart stage |
| Validate API | `job:write` | Trigger validation stage |
| CleanUp API | `job:write` | Clean up job artifacts |

---

## 3. Common Concepts

### 3.1 Job ID ↔ Image Group ID Mapping

Release 2 enforces a strict 1:1 mapping between Job IDs and Image Group IDs:

- **Job ID**: UUID v7 created once during Build Pipeline, reused in Deploy Pipeline
- **Image Group ID**: String identifier sourced from catalog payload
- **Mapping**: Enforced by UNIQUE foreign key constraint in database

### 3.2 Cross-Pipeline Job Continuity

A single Job ID can span multiple execution contexts:
- `jobs.pipeline_phase` optionally tracks execution context (`BUILD`, `DEPLOY`, or `NULL` for direct invocation)
- When `NULL`, the job is considered context-agnostic and can be used in any pipeline or direct invocation
- All stages from all contexts recorded in `job_stages` table
- Job status reflects overall lifecycle state regardless of execution context

#### Pipeline Phase Behavior

| Context | pipeline_phase Value | Description |
|---------|---------------------|-------------|
| Build Pipeline | `BUILD` | Job created/managed by Build Pipeline |
| Deploy Pipeline | `DEPLOY` | Job created/managed by Deploy Pipeline |
| Direct Invocation | `NULL` | Job created/managed via direct API calls |
| Hybrid/Unknown | `NULL` | Job can transition between contexts |

#### Phase Transitions

- Pipeline phases are **optional hints** and not strict constraints
- Direct API calls can work with jobs regardless of pipeline_phase value
- Phase transitions occur automatically when appropriate (e.g., first deploy stage call sets phase to `DEPLOY`)
- Jobs can be created without a phase and acquire one through usage

### 3.3 Image Group States

| State | Description | Terminal |
|-------|-------------|----------|
| `BUILT` | Images successfully built | No |
| `DEPLOYING` | Discovery playbook executing | No |
| `DEPLOYED` | Discovery completed | No |
| `RESTARTING` | PXE boot executing | No |
| `RESTARTED` | Nodes restarted successfully | No |
| `VALIDATING` | Test suites executing | No |
| `PASSED` | All validations passed | Yes |
| `FAILED` | Any stage failed | Yes |
| `CLEANED` | Artifacts removed | Yes |

---

## 4. API Endpoints

### 4.1 Job Management

#### 4.1.1 Create Job

##### Endpoint

```
POST /api/v1/jobs
```

##### Description

Creates a new job with optional pipeline phase context. Jobs can be created for pipeline execution or direct API invocation.

##### Authentication

Bearer Token with `catalog:read` scope.

##### Request Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
Idempotency-Key: <optional-key>
X-Correlation-ID: <optional-uuid>
```

##### Request Body

```json
{
  "client_id": "client-123",
  "client_name": "ACME Corp",
  "pipeline_phase": null
}
```

##### Request Parameters

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `client_id` | string | Yes | 1-128 chars, non-empty | Client identifier |
| `client_name` | string | No | 1-128 chars | Human-readable client name |
| `pipeline_phase` | string | No | `BUILD`, `DEPLOY`, or `null` | Optional execution context |

##### Pipeline Phase Behavior

- `BUILD`: Job intended for Build Pipeline execution
- `DEPLOY`: Job intended for Deploy Pipeline execution  
- `null` (default): Context-agnostic, suitable for direct invocation

##### Success Response (201 Created)

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "correlation_id": "018f3c4b-2d9e-7d1a-8a2b-111111111111",
  "job_state": "CREATED",
  "pipeline_phase": null,
  "created_at": "2026-03-15T10:30:00Z",
  "updated_at": "2026-03-15T10:30:00Z",
  "client_id": "client-123",
  "client_name": "ACME Corp"
}
```

#### 4.1.2 Get Job

##### Endpoint

```
GET /api/v1/jobs/{job_id}
```

##### Description

Retrieves job details including current state, pipeline phase, and all stage information. Works for jobs created via any context.

##### Authentication

Bearer Token with `catalog:read` scope.

##### Success Response (200 OK)

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "correlation_id": "018f3c4b-2d9e-7d1a-8a2b-111111111111",
  "job_state": "IN_PROGRESS",
  "pipeline_phase": "DEPLOY",
  "created_at": "2026-03-15T10:30:00Z",
  "updated_at": "2026-03-15T15:30:00Z",
  "image_group_id": "omnia-cluster-v1.2",
  "stages": [
    {
      "stage_name": "deploy",
      "stage_state": "COMPLETED",
      "started_at": "2026-03-15T15:00:00Z",
      "completed_at": "2026-03-15T15:25:00Z"
    }
  ]
}
```

### 4.2 Upload API

#### Endpoint

```
PUT /api/v1/jobs/{job_id}/upload
```

#### Description

Generic upload endpoint for synchronizing configuration files and/or catalog from GitLab to the BuildStream NFS backend. Replaces the previous `PUT /artifacts` endpoint with clearer intent.

#### Authentication

Bearer Token with `catalog:write` scope.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | string (UUID) | Job identifier |

#### Request Headers

```http
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
X-Correlation-ID: <optional-uuid>
```

#### Request Body (Multipart Form Data)

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `files` | file[] | Yes | ≤ 5 MB total, UTF-8 encoded | Configuration files and/or catalog |

#### Allowed File Types

| File Type | Extensions | Description |
|-----------|------------|-------------|
| Catalog | `.json` | Infrastructure catalog (e.g., `catalog_rhel.json`) |
| Configuration | `.yml`, `.yaml` | Omnia configuration files |
| Mapping | `.csv` | PXE mapping file (e.g., `pxe_mapping_file.csv`) |
| Config | `.conf`, `.cfg` | System configuration files |

#### Success Response (200 OK)

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "uploaded_files": [
    {
      "filename": "catalog_rhel.json",
      "size_bytes": 2048,
      "stored_path": "/mnt/build_stream/artifacts/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10/catalog_rhel.json"
    },
    {
      "filename": "pxe_mapping_file.csv",
      "size_bytes": 512,
      "stored_path": "/mnt/build_stream/artifacts/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10/pxe_mapping_file.csv"
    }
  ],
  "total_size_bytes": 2560
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_FILE_FORMAT` | Unsupported file type |
| 400 | `FILE_SIZE_EXCEEDED` | File exceeds size limit |
| 400 | `PATH_TRAVERSAL_DETECTED` | Malicious file path detected |
| 401 | `UNAUTHORIZED` | Missing/invalid token |
| 403 | `FORBIDDEN` | Insufficient scope |
| 404 | `JOB_NOT_FOUND` | Job ID doesn't exist |
| 409 | `JOB_IN_TERMINAL_STATE` | Job cannot accept uploads |
| 500 | `STORAGE_ERROR` | NFS write failed |
| 500 | `INTERNAL_ERROR` | Server error |

#### Example Request

```bash
curl -X PUT \
  "https://api.buildstream.example.com/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10/upload" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -F "files=@catalog_rhel.json" \
  -F "files=@pxe_mapping_file.csv"
```

---

### 4.3 ListImages API

#### Endpoint

```
GET /api/v1/images
```

#### Description

Returns the list of available Image Groups with their associated Job IDs and constituent images, providing the Job ID ↔ Image Group ID mapping required for the Deploy Pipeline to select a target. Each Image Group includes its constituent images identified by role name (e.g., `slurm_node`, `slurm_controller_node`), enabling end users to make informed deployment selections based on the composition of each Image Group.

#### Authentication

Bearer Token with `catalog:read` scope.

#### Request Headers

```http
Authorization: Bearer <access_token>
X-Correlation-ID: <optional-uuid>
```

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `status` | string | No | `BUILT` | Filter by ImageGroup status |
| `limit` | integer | No | 100 | Maximum number of results |
| `offset` | integer | No | 0 | Pagination offset |

#### Success Response (200 OK)

```json
{
  "image_groups": [
    {
      "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
      "image_group_id": "omnia-cluster-v1.2",
      "images": [
        {
          "role": "slurm_node",
          "image_name": "slurm_node.img"
        },
        {
          "role": "slurm_controller_node",
          "image_name": "slurm_controller_node.img"
        },
        {
          "role": "login_node",
          "image_name": "login_node.img"
        }
      ],
      "status": "BUILT",
      "created_at": "2026-03-15T10:30:00Z",
      "updated_at": "2026-03-15T14:45:00Z"
    },
    {
      "job_id": "018f3c4b-8d9e-8f2a-9b3c-0a1b2c3d4e5f",
      "image_group_id": "compute-node-v2.0",
      "images": [
        {
          "role": "kube_control_plane",
          "image_name": "kube_control_plane.img"
        },
        {
          "role": "kube_node",
          "image_name": "kube_node.img"
        }
      ],
      "status": "BUILT",
      "created_at": "2026-03-14T09:15:00Z",
      "updated_at": "2026-03-14T13:20:00Z"
    }
  ],
  "pagination": {
    "total_count": 2,
    "limit": 100,
    "offset": 0,
    "has_more": false
  }
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `job_id` | string (UUID) | Associated Job ID |
| `image_group_id` | string | Image Group identifier from catalog |
| `images` | object[] | Array of constituent image objects within this Image Group. Each object contains `role` and `image_name`. |
| `images[].role` | string | Functional role name identifying the image (e.g., `slurm_node`, `slurm_controller_node`, `kube_control_plane`, `kube_node`, `login_node`, `nfs_node`). Corresponds to the node role or functional layer that the image was built for. |
| `images[].image_name` | string | Generated image file name (e.g., `slurm_node.img`). |
| `status` | string | Current ImageGroup status |
| `created_at` | timestamp | ImageGroup creation time |
| `updated_at` | timestamp | Last status update time |

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 401 | `UNAUTHORIZED` | Missing/invalid token |
| 403 | `FORBIDDEN` | Insufficient scope |
| 400 | `INVALID_STATUS` | Invalid status filter |
| 500 | `INTERNAL_ERROR` | Server error |

#### Example Request

```bash
curl -X GET \
  "https://api.buildstream.example.com/api/v1/images?status=BUILT&limit=50" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..."
```

---

### 4.4 Deploy API

#### Endpoint

```
POST /api/v1/jobs/{job_id}/stages/deploy
```

#### Description

Initiates the deployment stage for a previously built Image Group. Renamed from the legacy `validate-image-on-test` stage. Validates 1:1 Job ID ↔ Image Group ID mapping and executes the Discovery playbook.

#### Authentication

Bearer Token with `job:write` scope.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | string (UUID) | Job identifier |

#### Request Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
X-Correlation-ID: <optional-uuid>
```

#### Request Body

```json
{
  "image_group_id": "omnia-cluster-v1.2"
}
```

#### Request Parameters

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `image_group_id` | string | Yes | 1-128 chars | Must match Job's associated ImageGroup |

#### Success Response (202 Accepted)

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "stage": "deploy",
  "status": "accepted",
  "submitted_at": "2026-03-15T15:00:00Z",
  "image_group_id": "omnia-cluster-v1.2",
  "correlation_id": "018f3c4b-2d9e-7d1a-8a2b-111111111111",
  "_links": {
    "self": "/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
    "status": "/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10"
  }
}
```

#### Status Polling

After receiving 202 Accepted, poll the job status endpoint:

```bash
curl -X GET \
  "https://api.buildstream.example.com/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..."
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_JOB_ID` | Invalid jobId format |
| 400 | `INVALID_IMAGE_GROUP_ID` | Invalid image_group_id format |
| 401 | `UNAUTHORIZED` | Missing/invalid token |
| 403 | `FORBIDDEN` | Insufficient scope |
| 404 | `JOB_NOT_FOUND` | Job doesn't exist |
| 409 | `IMAGEGROUP_MISMATCH` | image_group_id doesn't match Job's ImageGroup |
| 409 | `INVALID_STATE_TRANSITION` | Job not in valid state |
| 412 | `PRECONDITION_FAILED` | ImageGroup not in BUILT status |
| 500 | `DEPLOY_EXECUTION_ERROR` | Deploy playbook failed |
| 500 | `INTERNAL_ERROR` | Server error |

#### Example Request

```bash
curl -X POST \
  "https://api.buildstream.example.com/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10/stages/deploy" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "image_group_id": "omnia-cluster-v1.2"
  }'
```

---

### 4.5 ReStart API

#### Endpoint

```
POST /api/v1/jobs/{job_id}/stages/restart
```

#### Description

Triggers PXE-based node restart for the deployed Image Group. Renamed from the legacy `boot` API for clarity. Executes the `utils/set_pxe_boot.yml` playbook. The solution handles node diffs for PXE booting, ensuring that PXE boot is triggered only for newly added nodes and already booted nodes are explicitly excluded.

#### Authentication

Bearer Token with `job:write` scope.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | string (UUID) | Job identifier |

#### Request Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
X-Correlation-ID: <optional-uuid>
```

#### Request Body

```json
{
  "disable_pxe_boot": false
}
```

#### Request Parameters

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `disable_pxe_boot` | boolean | No | `false` | Whether to disable PXE booting entirely |

#### Success Response (202 Accepted)

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "stage": "restart",
  "status": "accepted",
  "submitted_at": "2026-03-15T16:30:00Z",
  "image_group_id": "omnia-cluster-v1.2",
  "correlation_id": "018f3c4b-2d9e-7d1a-8a2b-111111111111",
  "_links": {
    "self": "/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
    "status": "/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10"
  }
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_JOB_ID` | Invalid jobId format |
| 401 | `UNAUTHORIZED` | Missing/invalid token |
| 403 | `FORBIDDEN` | Insufficient scope |
| 404 | `JOB_NOT_FOUND` | Job doesn't exist |
| 409 | `INVALID_STATE_TRANSITION` | Job not in valid state |
| 412 | `PRECONDITION_FAILED` | ImageGroup not in DEPLOYED status |
| 500 | `RESTART_EXECUTION_ERROR` | PXE boot playbook failed |
| 500 | `INTERNAL_ERROR` | Server error |

#### Example Request

```bash
curl -X POST \
  "https://api.buildstream.example.com/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10/stages/restart" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json"
```

---

### 4.6 Validate API

#### Endpoint

```
POST /api/v1/jobs/{job_id}/stages/validate
```

#### Description

Runs post-deployment validation test suites and persists the results in the `job_stages.result_detail` JSONB column. This stage leverages the existing molecule test framework, which contains sufficient benchmark tests to comprehensively validate the cluster deployment, network configuration, and service health.

#### Authentication

Bearer Token with `job:write` scope.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | string (UUID) | Job identifier |

#### Request Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
X-Correlation-ID: <optional-uuid>
```

#### Request Body

```json
{
  "test_suite": "full",
  "timeout_minutes": 60
}
```

#### Request Parameters

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `test_suite` | string | No | `full` | Test suite type (`full`, `smoke`, `custom`) |
| `timeout_minutes` | integer | No | `60` | Maximum execution time (min: 1, max: 480 minutes) |

#### Success Response (202 Accepted)

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "stage": "validate",
  "status": "accepted",
  "submitted_at": "2026-03-15T17:00:00Z",
  "test_suite": "full",
  "timeout_minutes": 60,
  "correlation_id": "018f3c4b-2d9e-7d1a-8a2b-111111111111",
  "_links": {
    "self": "/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
    "status": "/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10"
  }
}
```

#### Validation Results Structure

Upon completion, validation results are stored in `job_stages.result_detail`:

```json
{
  "outcome": "PASSED",
  "summary": {
    "total_tests": 45,
    "passed": 43,
    "failed": 2,
    "skipped": 0,
    "duration_seconds": 1847
  },
  "test_results": [
    {
      "test_name": "connectivity_test",
      "status": "PASSED",
      "duration_seconds": 12,
      "details": "All nodes reachable"
    },
    {
      "test_name": "service_health_check",
      "status": "FAILED",
      "duration_seconds": 45,
      "error": "Slurm service not responding",
      "node": "compute-01"
    }
  ],
  "node_status": {
    "compute-01": "FAILED",
    "compute-02": "PASSED",
    "storage-01": "PASSED"
  }
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_JOB_ID` | Invalid jobId format |
| 400 | `INVALID_TEST_SUITE` | Invalid test_suite value |
| 401 | `UNAUTHORIZED` | Missing/invalid token |
| 403 | `FORBIDDEN` | Insufficient scope |
| 404 | `JOB_NOT_FOUND` | Job doesn't exist |
| 409 | `INVALID_STATE_TRANSITION` | Job not in valid state |
| 412 | `PRECONDITION_FAILED` | ImageGroup not in RESTARTED status |
| 500 | `VALIDATION_EXECUTION_ERROR` | Test suite execution failed |
| 500 | `INTERNAL_ERROR` | Server error |

#### Example Request

```bash
curl -X POST \
  "https://api.buildstream.example.com/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10/stages/validate" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "test_suite": "full",
    "timeout_minutes": 60
  }'
```

---

### 4.7 CleanUp API

#### Endpoint

```
DELETE /api/v1/jobs/{job_id}/cleanup
```

#### Description

Removes all images built for a given Job ID and cleans up the associated NFS artifacts. Only allowed for jobs in terminal states.

#### Authentication

Bearer Token with `job:write` scope.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | string (UUID) | Job identifier |

#### Request Headers

```http
Authorization: Bearer <access_token>
X-Correlation-ID: <optional-uuid>
```

#### Request Body

Empty request body.

#### Success Response (200 OK)

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "cleanup_status": "completed",
  "cleaned_at": "2026-03-15T18:00:00Z",
  "summary": {
    "files_removed": 12,
    "total_size_freed_mb": 2048,
    "images_removed": 3,
    "directories_cleaned": [
      "/mnt/build_stream/artifacts/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
      "/var/lib/omnia/images/omnia-cluster-v1.2"
    ]
  },
  "image_group_id": "omnia-cluster-v1.2"
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_JOB_ID` | Invalid jobId format |
| 401 | `UNAUTHORIZED` | Missing/invalid token |
| 403 | `FORBIDDEN` | Insufficient scope |
| 404 | `JOB_NOT_FOUND` | Job doesn't exist |
| 409 | `ACTIVE_OPERATION` | Job has active operations in progress |
| 412 | `ALREADY_CLEANED` | Job already cleaned up |
| 412 | `NOT_TERMINAL_STATE` | Job not in terminal state |
| 500 | `CLEANUP_ERROR` | Cleanup operation failed |
| 500 | `INTERNAL_ERROR` | Server error |

#### Example Request

```bash
curl -X DELETE \
  "https://api.buildstream.example.com/api/v1/jobs/018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10/cleanup" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..."
```

---

## 5. API Flow Sequence

### 5.1 Build Pipeline Flow

```mermaid
sequenceDiagram
    participant Client
    participant JobsAPI as Jobs API
    participant UploadAPI as Upload API
    participant ParseAPI as Parse Catalog
    participant GenAPI as Generate API
    participant LocalRepo as Local Repository
    participant BuildAPI as Build Image
    
    Client->>JobsAPI: POST /jobs (Create Job, pipeline_phase: BUILD)
    JobsAPI-->>Client: 201 Created (job_id)
    
    Client->>UploadAPI: PUT /upload (catalog + configs)
    UploadAPI-->>Client: 200 OK
    
    Client->>ParseAPI: POST /stages/parse-catalog
    ParseAPI-->>Client: 200 OK
    
    Client->>GenAPI: POST /stages/generate-input-files
    GenAPI-->>Client: 200 OK
    
    Client->>LocalRepo: POST /stages/create-local-repository
    LocalRepo-->>Client: 202 Accepted
    
    Client->>BuildAPI: POST /stages/build-image
    Note over BuildAPI: ImageGroup created<br>1:1 JobID ImageGroupID mapping
    BuildAPI-->>Client: 202 Accepted
```

### 5.2 Deploy Pipeline Flow

```mermaid
sequenceDiagram
    participant Client
    participant ListAPI as ListImages API
    participant UploadAPI as Upload API
    participant DeployAPI as Deploy API
    participant RestartAPI as ReStart API
    participant ValidateAPI as Validate API
    
    Client->>ListAPI: GET /images (List JobID ↔ ImageGroupID mappings with constituent images)
    ListAPI-->>Client: 200 OK (includes images array per group with role + image_name)
    
    Note over Client: User reviews constituent images per group and selects JobID + ImageGroupID pair
    
    Client->>UploadAPI: PUT /upload (CSV + configs to selected JobID)
    UploadAPI-->>Client: 200 OK
    
    Client->>DeployAPI: POST /stages/deploy (validate 1:1 mapping)
    DeployAPI-->>Client: 202 Accepted
    
    Client->>RestartAPI: POST /stages/restart
    RestartAPI-->>Client: 202 Accepted
    
    Client->>ValidateAPI: POST /stages/validate
    ValidateAPI-->>Client: 202 Accepted
```

### 5.3 Direct Invocation Flow

```mermaid
sequenceDiagram
    participant Client
    participant JobsAPI as Jobs API
    participant UploadAPI as Upload API
    participant StageAPI as Stage APIs
    participant CleanUpAPI as CleanUp API
    
    Client->>JobsAPI: POST /jobs (pipeline_phase: null)
    Note over JobsAPI: Context-agnostic job creation
    JobsAPI-->>Client: 201 Created (job_id, no phase)
    
    Client->>UploadAPI: PUT /upload (any files)
    UploadAPI-->>Client: 200 OK
    
    Client->>StageAPI: POST /stages/{any} (independent execution)
    Note over StageAPI: Any stage can be called<br>based on preconditions
    StageAPI-->>Client: 202 Accepted
    
    Client->>CleanUpAPI: DELETE /cleanup (when finished)
    CleanUpAPI-->>Client: 200 OK
```

### 5.4 Hybrid Flow

```mermaid
sequenceDiagram
    participant Pipeline as Build Pipeline
    participant JobsAPI as Jobs API
    participant UploadAPI as Upload API
    participant StageAPI as Stage APIs
    participant DirectAPI as Direct API Client
    
    Pipeline->>JobsAPI: POST /jobs (pipeline_phase: BUILD)
    JobsAPI-->>Pipeline: 201 Created (job_id, phase: BUILD)
    
    Pipeline->>StageAPI: Execute Build Stages...
    StageAPI-->>Pipeline: 202 Accepted
    
    Note over Pipeline,DirectAPI: Job transitions to direct usage
    DirectAPI->>StageAPI: POST /stages/deploy (same job_id)
    Note over StageAPI: Continuing with<br>pipeline-created job
    StageAPI-->>DirectAPI: 202 Accepted
```

---

## 6. Error Handling

### 6.1 Error Response Format

All error responses follow a consistent JSON structure:

```json
{
  "error": {
    "code": "IMAGEGROUP_MISMATCH",
    "message": "Supplied image_group_id does not match the Job's associated Image Group",
    "details": {
      "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
      "supplied_image_group_id": "wrong-cluster-v1.0",
      "expected_image_group_id": "omnia-cluster-v1.2"
    },
    "correlation_id": "018f3c4b-2d9e-7d1a-8a2b-111111111111",
    "timestamp": "2026-03-15T15:30:00Z"
  }
}
```

### 6.2 Common Error Codes

| Error Code | Description | HTTP Status |
|------------|-------------|-------------|
| `INVALID_JOB_ID` | Invalid UUID format for job_id | 400 |
| `UNAUTHORIZED` | Missing or invalid authentication | 401 |
| `FORBIDDEN` | Insufficient scope for operation | 403 |
| `JOB_NOT_FOUND` | Job ID doesn't exist | 404 |
| `IMAGEGROUP_MISMATCH` | ImageGroup ID doesn't match Job's mapping | 409 |
| `INVALID_STATE_TRANSITION` | Invalid state transition requested | 409 |
| `ACTIVE_OPERATION` | Cannot cleanup during active operations | 409 |
| `PRECONDITION_FAILED` | Required precondition not met | 412 |
| `ALREADY_CLEANED` | Job already cleaned up | 412 |
| `NOT_TERMINAL_STATE` | Operation requires terminal state | 412 |

---

## 7. HTTP Status Codes

| Status | Usage | Description |
|--------|-------|-------------|
| 200 | Success | Synchronous operation completed |
| 201 | Created | Resource created (e.g., job) |
| 202 | Accepted | Asynchronous operation accepted |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required/failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict or invalid transition |
| 412 | Precondition Failed | Required precondition not met |
| 500 | Internal Error | Server-side error |

---

## 8. Data Models

### 8.1 Job Model

```json
{
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "correlation_id": "018f3c4b-2d9e-7d1a-8a2b-111111111111",
  "status": "IN_PROGRESS",
  "pipeline_phase": null,
  "created_at": "2026-03-15T10:30:00Z",
  "updated_at": "2026-03-15T14:45:00Z",
  "client_id": "client-123",
  "image_group_id": "omnia-cluster-v1.2"
}
```

#### Pipeline Phase Field

| Value | Context | Description |
|-------|---------|-------------|
| `"BUILD"` | Pipeline Context | Job created/managed by Build Pipeline |
| `"DEPLOY"` | Pipeline Context | Job created/managed by Deploy Pipeline |
| `null` | Direct Invocation | Context-agnostic, suitable for any use case |

#### Notes:
- `pipeline_phase` is **optional** and defaults to `null`
- APIs do not enforce strict constraints based on `pipeline_phase`
- Field is informational for tracking and debugging
- Direct API invocations can work with jobs regardless of phase value

### 8.2 ImageGroup Model

```json
{
  "image_group_id": "omnia-cluster-v1.2",
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "images": [
    {
      "role": "slurm_node",
      "image_name": "slurm_node.img"
    },
    {
      "role": "slurm_controller_node",
      "image_name": "slurm_controller_node.img"
    },
    {
      "role": "login_node",
      "image_name": "login_node.img"
    }
  ],
  "status": "BUILT",
  "created_at": "2026-03-15T14:45:00Z",
  "updated_at": "2026-03-15T14:45:00Z"
}
```

#### ImageGroup Fields

| Field | Type | Description |
|-------|------|-------------|
| `image_group_id` | string | Unique Image Group identifier from catalog |
| `job_id` | string (UUID) | Associated Job ID (1:1 mapping) |
| `images` | object[] | Array of constituent images within this Image Group |
| `images[].role` | string | Functional role name (e.g., `slurm_node`, `slurm_controller_node`, `kube_control_plane`, `kube_node`, `login_node`, `nfs_node`) |
| `images[].image_name` | string | Generated image file name on NFS (e.g., `slurm_node.img`) |
| `status` | string | Current Image Group lifecycle status |
| `created_at` | timestamp | Image Group creation time |
| `updated_at` | timestamp | Last status update time |

#### Notes:
- The `images` array lists all constituent OS images built for this Image Group, each identified by its functional `role`.
- The `role` field corresponds to the node role or functional layer (e.g., `slurm_node` for Slurm compute nodes, `slurm_controller_node` for Slurm controller nodes, `kube_control_plane` for Kubernetes control plane nodes).
- This information helps end users understand the composition of an Image Group before selecting it for deployment.

### 8.3 Stage Model

```json
{
  "stage_id": "stage-uuid",
  "job_id": "018f3c4b-7b5b-7a9d-b6c4-9f3b4f9b2c10",
  "stage_name": "deploy",
  "status": "COMPLETED",
  "attempt_number": 2,
  "started_at": "2026-03-15T15:00:00Z",
  "last_attempt_at": "2026-03-15T15:15:00Z",
  "completed_at": "2026-03-15T15:25:00Z",
  "result_detail": {
    "nodes_deployed": 5,
    "duration_seconds": 1500
  }
}
```

### 8.4 Database Schema

This section provides the complete database schema for all tables consumed or modified by the BuildStream Release 2 APIs. The schema is authoritative for both Build Pipeline (Component 1) and Deploy Pipeline (Component 2) APIs.

#### 8.4.1 Table: `jobs` (Modified)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID (v7) | PK | Job ID. Created once during Build Pipeline, reused by Deploy Pipeline. |
| `status` | Enum(`JobStatus`) | NOT NULL | Overall job status. |
| `pipeline_phase` | Enum(`PipelinePhase`) | NULLABLE | Tracks which pipeline currently owns the job. `BUILD`, `DEPLOY`, or `NULL`. |
| `client_id` | String(128) | NOT NULL | Client identifier. |
| `client_name` | String(128) | NULLABLE | Human-readable client name. |
| `correlation_id` | UUID | NOT NULL | Correlation ID for request tracing. |
| `created_at` | Timestamp | NOT NULL | Job creation timestamp. |
| `updated_at` | Timestamp | NOT NULL | Last status change timestamp. |

**Enum `JobStatus`:** `CREATED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `CANCELLED`

**Enum `PipelinePhase`:** `BUILD`, `DEPLOY`

**Deploy Pipeline writes:** The Deploy API (`POST /stages/deploy`) transitions `pipeline_phase` from `BUILD` (or `NULL`) to `DEPLOY` when the first deploy stage is invoked.

#### 8.4.2 Table: `image_groups` (New)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String(128) | PK | Image Group ID from catalog. Replaces legacy `Image-key`. |
| `job_id` | UUID | FK → `jobs.id`, **UNIQUE**, NOT NULL | Enforces 1:1 Job ↔ ImageGroup mapping. |
| `status` | Enum(`ImageGroupStatus`) | NOT NULL | Lifecycle status. |
| `created_at` | Timestamp | NOT NULL | Record creation timestamp. |
| `updated_at` | Timestamp | NOT NULL | Last status change timestamp. |

**Enum `ImageGroupStatus`:** `BUILT`, `DEPLOYING`, `DEPLOYED`, `RESTARTING`, `RESTARTED`, `VALIDATING`, `PASSED`, `FAILED`, `CLEANED`

**Indexes:**
- `idx_image_groups_job_id` (UNIQUE) — Enforces 1:1 mapping; enables Job ID → Image Group lookups.
- `idx_image_groups_status` — Supports filtering by status (e.g., `ListImages` queries for `BUILT`).

**Deploy Pipeline status transitions:**

| Transition | Triggered By | Precondition |
|-----------|-------------|--------------|
| `BUILT` → `DEPLOYING` | `POST /stages/deploy` | `status == BUILT` |
| `DEPLOYING` → `DEPLOYED` | Deploy playbook success | Internal (async) |
| `DEPLOYING` → `FAILED` | Deploy playbook failure | Internal (async) |
| `DEPLOYED` → `RESTARTING` | `POST /stages/restart` | `status == DEPLOYED` |
| `RESTARTING` → `RESTARTED` | PXE boot playbook success | Internal (async) |
| `RESTARTING` → `FAILED` | PXE boot playbook failure | Internal (async) |
| `RESTARTED` → `VALIDATING` | `POST /stages/validate` | `status == RESTARTED` |
| `VALIDATING` → `PASSED` | Molecule tests all pass | Internal (async) |
| `VALIDATING` → `FAILED` | Molecule tests any fail | Internal (async) |

#### 8.4.3 Table: `images` (New)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID (v7) | PK | Unique image identifier. |
| `image_group_id` | String(128) | FK → `image_groups.id`, NOT NULL | Parent Image Group. |
| `role` | String(128) | NOT NULL | Functional role name (e.g., `slurm_node`, `kube_control_plane`). |
| `image_name` | String(256) | NOT NULL | Generated image file name on NFS (e.g., `slurm_node.img`). |
| `created_at` | Timestamp | NOT NULL | Record creation timestamp. |

**Indexes:**
- `idx_images_image_group_id` — Enables efficient lookup of constituent images by Image Group.
- `idx_images_image_group_id_role` (UNIQUE) — Enforces one image per role within an Image Group.

**Deploy Pipeline reads:** The `GET /images` API joins `images` on `image_group_id` to return constituent images.

#### 8.4.4 Table: `job_stages` (Extended)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID (v7) | PK | Stage ID. |
| `job_id` | UUID | FK → `jobs.id`, NOT NULL | Parent Job. |
| `stage_name` | Enum(`StageName`) | NOT NULL | Stage identifier. |
| `status` | Enum(`StageStatus`) | NOT NULL | Execution status. |
| `attempt_number` | Integer | NOT NULL, DEFAULT 1 | Execution attempt count. |
| `result_detail` | JSONB | NULLABLE | Structured output (used by `validate` stage). |
| `started_at` | Timestamp | NULLABLE | Latest attempt start time. |
| `last_attempt_at` | Timestamp | NULLABLE | Most recent attempt timestamp. |
| `completed_at` | Timestamp | NULLABLE | Stage completion time. |
| `created_at` | Timestamp | NOT NULL | Record creation timestamp. |
| `updated_at` | Timestamp | NOT NULL | Last update timestamp. |

**Enum `StageName`:** `parse_catalog`, `generate_input_files`, `create_local_repository`, `build_image`, `deploy`, `pxe_boot`, `validate`

**Enum `StageStatus`:** `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`

**Indexes:**
- `idx_job_stages_job_id_stage_name` (UNIQUE) — One record per job + stage combination.
- `idx_job_stages_status` — Supports filtering by status.

**Deploy Pipeline stages:** `deploy`, `pxe_boot`, `validate` records are inserted by the Deploy Pipeline APIs. The `validate` stage populates `result_detail` with the Molecule test results.

#### 8.4.5 Entity Relationship Diagram

```
┌──────────────────┐       1:1       ┌────────────────────┐       1:N       ┌──────────────┐
│      jobs        │────────────────▶│   image_groups     │────────────────▶│    images     │
│                  │                 │                    │                 │              │
│ id (PK, UUID v7) │                 │ id (PK, String)    │                 │ id (PK, UUID)│
│ status           │                 │ job_id (UNIQUE FK) │                 │ image_group_id│
│ pipeline_phase   │                 │ status             │                 │ role         │
│ client_id        │                 │ created_at         │                 │ image_name   │
│ created_at       │                 │ updated_at         │                 │ created_at   │
│ updated_at       │                 └────────────────────┘                 └──────────────┘
│                  │
│                  │       1:N       ┌────────────────────┐
│                  │────────────────▶│   job_stages       │
│                  │                 │                    │
└──────────────────┘                 │ id (PK, UUID)      │
                                     │ job_id (FK)        │
                                     │ stage_name         │
                                     │ status             │
                                     │ attempt_number     │
                                     │ result_detail (JSONB)│
                                     │ started_at         │
                                     │ completed_at       │
                                     └────────────────────┘
```

### 8.5 Deploy Pipeline Pydantic Schemas

This section documents the Pydantic request/response schemas specific to the Deploy Pipeline APIs (Component 2).

#### 8.5.1 Deploy Request Schema

```json
{
  "$schema": "Pydantic v2 model",
  "model": "DeployRequest",
  "fields": {
    "image_group_id": {
      "type": "string",
      "required": true,
      "min_length": 1,
      "max_length": 128,
      "description": "Must match the Job's associated ImageGroup ID"
    }
  }
}
```

#### 8.5.2 Restart Request Schema

```json
{
  "$schema": "Pydantic v2 model",
  "model": "RestartRequest",
  "fields": {
    "disable_pxe_boot": {
      "type": "boolean",
      "required": false,
      "default": false,
      "description": "Whether to disable PXE booting entirely for all nodes"
    }
  }
}
```

#### 8.5.3 Validate Request Schema

```json
{
  "$schema": "Pydantic v2 model",
  "model": "ValidateRequest",
  "fields": {
    "test_suite": {
      "type": "string",
      "required": false,
      "default": "full",
      "allowed_values": ["full", "smoke", "custom"],
      "description": "Test suite type to execute"
    },
    "timeout_minutes": {
      "type": "integer",
      "required": false,
      "default": 60,
      "minimum": 1,
      "maximum": 480,
      "description": "Maximum execution time in minutes"
    }
  }
}
```

#### 8.5.4 Validation Result Detail Schema (JSONB)

This schema defines the structure persisted in `job_stages.result_detail` for the `validate` stage:

```json
{
  "outcome": "PASSED",
  "summary": {
    "total_tests": 45,
    "passed": 43,
    "failed": 2,
    "skipped": 0,
    "duration_seconds": 1847
  },
  "test_results": [
    {
      "test_name": "connectivity_test",
      "status": "PASSED",
      "duration_seconds": 12,
      "details": "All nodes reachable"
    },
    {
      "test_name": "service_health_check",
      "status": "FAILED",
      "duration_seconds": 45,
      "error": "Slurm service not responding",
      "node": "compute-01"
    }
  ],
  "node_status": {
    "compute-01": "FAILED",
    "compute-02": "PASSED",
    "storage-01": "PASSED"
  }
}
```

**Validation Result Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `outcome` | string | Yes | Overall result: `PASSED` or `FAILED` |
| `summary.total_tests` | integer | Yes | Total number of tests executed |
| `summary.passed` | integer | Yes | Number of tests that passed |
| `summary.failed` | integer | Yes | Number of tests that failed |
| `summary.skipped` | integer | No | Number of tests skipped (default: 0) |
| `summary.duration_seconds` | number | No | Total execution duration |
| `test_results` | object[] | No | Per-test result details |
| `test_results[].test_name` | string | Yes | Test identifier |
| `test_results[].status` | string | Yes | `PASSED`, `FAILED`, or `SKIPPED` |
| `test_results[].duration_seconds` | number | No | Individual test duration |
| `test_results[].details` | string | No | Success details |
| `test_results[].error` | string | No | Error message on failure |
| `test_results[].node` | string | No | Node where failure occurred |
| `node_status` | object | No | Per-node aggregate status map |

#### 8.5.5 ListImages Response Schema

```json
{
  "$schema": "Pydantic v2 model",
  "model": "ListImagesResponse",
  "fields": {
    "image_groups": {
      "type": "array",
      "items": {
        "type": "ImageGroupResponse",
        "fields": {
          "job_id": {"type": "UUID", "required": true},
          "image_group_id": {"type": "string", "required": true},
          "images": {
            "type": "array",
            "items": {
              "type": "ImageResponse",
              "fields": {
                "role": {"type": "string", "required": true},
                "image_name": {"type": "string", "required": true}
              }
            }
          },
          "status": {"type": "ImageGroupStatus", "required": true},
          "created_at": {"type": "datetime", "required": true},
          "updated_at": {"type": "datetime", "required": true}
        }
      }
    },
    "pagination": {
      "type": "PaginationResponse",
      "fields": {
        "total_count": {"type": "integer", "minimum": 0},
        "limit": {"type": "integer", "minimum": 1, "maximum": 1000},
        "offset": {"type": "integer", "minimum": 0},
        "has_more": {"type": "boolean"}
      }
    }
  }
}
```

### 8.6 State Machine Precondition Matrix

This matrix documents the required `ImageGroupStatus` precondition for each Deploy Pipeline endpoint and the resulting status transitions:

| Endpoint | Required Status | Immediate Transition | On Success | On Failure |
|----------|----------------|---------------------|------------|------------|
| `POST /stages/deploy` | `BUILT` | → `DEPLOYING` | → `DEPLOYED` | → `FAILED` |
| `POST /stages/restart` | `DEPLOYED` | → `RESTARTING` | → `RESTARTED` | → `FAILED` |
| `POST /stages/validate` | `RESTARTED` | → `VALIDATING` | → `PASSED` | → `FAILED` |

**Guard behavior:** If the precondition is not met, the API returns `412 Precondition Failed` with the current status and required status in the error details. The `image_groups` row is locked with `SELECT ... FOR UPDATE` before the guard check to prevent concurrent modifications.

### 8.7 Deploy Pipeline DB Write Summary

| Endpoint | Tables Modified | Write Operations |
|----------|----------------|-----------------|
| `GET /images` | None | Read-only: `SELECT` on `image_groups` JOIN `images` |
| `POST /stages/deploy` | `jobs`, `image_groups`, `job_stages` | Update `jobs.pipeline_phase` → `DEPLOY`; Update `image_groups.status` → `DEPLOYING`/`DEPLOYED`/`FAILED`; Insert/update `job_stages` record for `deploy` |
| `POST /stages/restart` | `jobs`, `image_groups`, `job_stages` | Update `jobs.status`; Update `image_groups.status` → `RESTARTING`/`RESTARTED`/`FAILED`; Insert/update `job_stages` record for `pxe_boot` |
| `POST /stages/validate` | `jobs`, `image_groups`, `job_stages` | Update `jobs.status`; Update `image_groups.status` → `VALIDATING`/`PASSED`/`FAILED`; Insert/update `job_stages` record for `validate`; Persist `result_detail` JSONB |

---

## 9. Security Considerations

### 9.1 Authentication & Authorization

- All endpoints require OAuth 2.0 Client Credentials flow
- JWT tokens validated on every request
- Scope-based access control enforced
- Token expiration: 1 hour (renew as needed)

### 9.2 Input Validation

- File uploads validated for type, size, and path traversal
- UUID format validation for all job_id parameters
- String length constraints enforced
- SQL injection protection via parameterized queries

### 9.3 Error Information Security

- Error messages avoid exposing internal system details
- Sensitive data redacted from logs (first 8 chars of IDs only)
- Stack traces never returned to clients
- Correlation IDs for secure debugging

### 9.4 Rate Limiting

- Upload API: 10 requests per minute per client
- Stage APIs: 5 requests per minute per job
- ListImages API: 20 requests per minute per client

---

## 10. Versioning

### 10.1 API Version Strategy

- URL path versioning: `/api/v1/`
- Semantic versioning for breaking changes
- Backward compatibility maintained within major versions
- Deprecation notices for retired endpoints

### 10.2 Version Compatibility

| Version | Status | Release Date | Deprecation |
|---------|--------|--------------|-------------|
| 1.0 | Active | Feb 2026 | - |
| 2.0 | Draft | Mar 2026 | - |

---

## 11. OpenAPI 3.0 Compatibility

This specification is compatible with OpenAPI 3.0. The complete OpenAPI definition is available at:

```
https://api.buildstream.example.com/docs/openapi.json
```

Interactive API documentation is available at:

```
https://api.buildstream.example.com/docs
```

---

## References

- [Base BuildStream API Specification v1.0](API_SPECIFICATION.md)
- [BuildStream Release 2 Engineering Specification](build_stream/irc2/Engineering_Spec.md)
- [OAuth 2.0 Client Credentials Grant](https://tools.ietf.org/html/rfc6749#section-4.4)
- [JWT RFC 7519](https://tools.ietf.org/html/rfc7519)
