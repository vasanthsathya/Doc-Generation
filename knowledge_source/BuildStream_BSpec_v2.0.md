# BuildStream — Behaviour Specification (BSpec) v2.0

| Field              | Value                                                                 |
|:-------------------|:----------------------------------------------------------------------|
| Version            | 2.1                                                                   |
| Date               | 2026-05-02                                                            |
| Status             | Draft                                                                 |
| Capability ID      | 16427                                                                 |
| Capability Name    | NERSC Automated Tools NRE Milestone 4                                 |
| Author             | Omnia Product Team                                                    |
| Reviewed By        | Omnia Engineering Team                                                |
| Change History     | v1.0 (26 Mar 2026) — Initial release; v2.0 (08 Apr 2026) — Enriched per Gap Analysis recommendations; v2.1 (02 May 2026) — Added capability ID, updated API endpoints, pipeline decomposition details |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [User Personas](#3-user-personas)
4. [Feature 1 — Workflow Optimization](#4-feature-1--workflow-optimization)
5. [Feature 2 — Image Management](#5-feature-2--image-management)
6. [Authentication and Authorization](#6-authentication-and-authorization)
7. [API Contract Summary](#7-api-contract-summary)
8. [Job Lifecycle State Machine](#8-job-lifecycle-state-machine)
9. [Build Stage State Machine](#9-build-stage-state-machine)
10. [Image Group State Machine](#10-image-group-state-machine)
11. [Detailed Workflow Descriptions](#11-detailed-workflow-descriptions)
12. [Error Handling](#12-error-handling)
13. [Customer-Facing Constraints](#13-customer-facing-constraints)
14. [Rate Limiting](#14-rate-limiting)
15. [Non-Functional Requirements](#15-non-functional-requirements)
16. [Acceptance Criteria](#16-acceptance-criteria)
17. [Future Considerations](#17-future-considerations)
18. [Glossary](#18-glossary)
19. [Gap Analysis Traceability](#19-gap-analysis-traceability)

---

## 1. Introduction

### 1.1 Purpose

BuildStream is a RESTful API service that automates the end-to-end workflow for building, deploying, validating, and managing Omnia OS images. It provides a programmatic interface for both human operators and CI/CD pipelines (e.g., GitLab CI/CD) to orchestrate the image lifecycle.

### 1.2 Core Features

BuildStream delivers two core features:

| Feature                   | Description                                                                                       |
|---------------------------|---------------------------------------------------------------------------------------------------|
| **Workflow Optimization** | Automates the build pipeline through a sequenced set of API-driven stages: input file management, local repository creation, catalog parsing, and image building |
| **Image Management**      | Provides APIs for deploying built images to target nodes, validating deployments via automated tests, tagging images as passed or failed, and cleaning up failed images |

### 1.3 How Users Interact

Users interact with BuildStream through its REST API. Two primary interaction patterns are supported:

- **GitLab CI/CD Pipeline** — A `.gitlab-ci.yml` pipeline calls the BuildStream API at each stage, automating the full build-and-deploy lifecycle.
- **Direct API** — Users interact with the API directly using `curl`, Postman, or custom clients, following the same sequential stage execution pattern.

---

## 2. Scope

> **Gap addressed:** A-01 (Scope Definition)

### 2.1 In-Scope (This Release)

| #  | Item                                                                        |
|----|-----------------------------------------------------------------------------|
| 1  | RESTful API for build pipeline orchestration                                 |
| 2  | Job lifecycle management (create, query, delete)                             |
| 3  | Build stages: `parse-catalog`, `generate-input-files`, `create-local-repository`, `build-image`      |
| 4  | OAuth 2.0 client credentials authentication with JWT tokens                  |
| 5  | Image building workflow (parse catalog, generate input files, build image)   |
| 6  | Image deployment via deploy API                                              |
| 7  | Node PXE boot / restart for image provisioning                               |
| 8  | Image validation (test execution and pass/fail tagging)                      |
| 9  | Image cleanup via CleanUp API (`DELETE /api/v1/jobs/{job_id}`) — delete images from S3 storage, remove catalog/config artifacts, transition to CLEANED status |
| 10 | Configuration file upload via Upload API (`PUT /api/v1/jobs/{job_id}/upload`) with file allowlist and security validation |
| 11 | Pipeline decomposition: separate Build, Deploy, and Cleanup pipelines with parent-child architecture |
| 12 | Dynamic child pipeline generation for image selection with actual image_group names |
| 13 | Image group lifecycle tracking (BUILT → DEPLOYING → DEPLOYED → VALIDATING → PASSED/FAILED → CLEANED) |
| 14 | Database schema with `image_groups` and `images` tables, semicolon-delimited S3 paths (VARCHAR(512)) |
| 15 | Artifact storage and retrieval via `GET /api/v1/jobs/{job_id}/artifacts/{label}` |
| 16 | Idempotent API operations (`Idempotency-Key` header)                         |
| 17 | Audit event logging for all state transitions                                |
| 18 | Single-cluster, x86_64 and aarch64 architecture support                      |
| 19 | Build pipeline summary filtering (shows only build-related stages)           |

### 2.2 Out-of-Scope (This Release)

| #  | Item                                                                        |
|----|-----------------------------------------------------------------------------|
| 1  | Multi-cluster deployments                                                    |
| 2  | Non-x86 architectures (ARM, etc.)                                            |
| 3  | VM + physical hybrid deployments                                             |
| ~~4~~ | ~~Automated scheduled cleanup~~ — **Moved to In-Scope** (cron-based cleanup of validation-failed images) |
| 5  | Concurrent/simultaneous pipeline execution                                   |
| 6  | "Promoted" image tagging                                                     |
| 7  | Direct PXE mapping file upload via restart API                               |
| 8  | Deploy via CSV pointing to a mapping file                                    |
| 9  | Persistent database storage (PostgreSQL)                                     |

---

## 3. User Personas

> **Gap addressed:** A-02 (User Personas)

| Persona                  | Role                                                       | Interaction Pattern               | Authentication                     |
|--------------------------|------------------------------------------------------------|-----------------------------------|------------------------------------|
| **Platform Operator**    | Primary user building and deploying Omnia OS images        | Full API access — all operations  | OAuth 2.0 JWT bearer token         |
| **CI/CD Pipeline Agent** | Automated agent (e.g., GitLab CI/CD) triggering workflows  | Programmatic API calls            | OAuth 2.0 JWT bearer token         |
| **Direct API Consumer**  | Developer or tool integrating with the BuildStream API     | REST calls via curl/Postman       | OAuth 2.0 JWT bearer token         |
| **System Administrator** | Manages OIM infrastructure, credentials, container lifecycle| OAuth client registration, config | Basic Auth (registration); JWT (ops)|

---

## 4. Feature 1 — Workflow Optimization

### 4.1 Overview

Workflow Optimization automates the build pipeline through a sequential set of API-driven stages. The user creates a Job, uploads input files, and triggers stages in order. Each stage performs a specific function and must complete before the next can begin.

### 4.2 Job Creation

> **Gap addressed:** A-04 (Job Creation Specification)

**User story:** As a Platform Operator, I want to create a build Job so that I can orchestrate the image build pipeline.

**API:** `POST /api/v1/jobs`

**Request headers:**

| Header               | Required | Description                                           |
|----------------------|----------|-------------------------------------------------------|
| `Authorization`      | Yes      | Bearer JWT token                                       |
| `X-Client-Id`        | Yes      | Client identifier                                      |
| `X-Correlation-Id`   | Yes      | Unique request correlation ID for tracing              |
| `Idempotency-Key`    | Yes      | Unique key for request deduplication                   |

**Request body:**

```json
{
  "client_id": "string (required)",
  "client_name": "string (required)"
}
```

**Response (`201 Created`):**

```json
{
  "job_id": "uuid",
  "state": "CREATED",
  "stages": [
    { "name": "create-local-repository", "state": "PENDING" },
    { "name": "parse-catalog", "state": "PENDING" },
    { "name": "build-image", "state": "PENDING" }
  ],
  "created_at": "2026-04-08T10:00:00Z",
  "client_id": "string"
}
```

**Behavior:**
- The system assigns a unique Job ID (UUID format).
- The Job is initialized in `CREATED` state with all stages in `PENDING`.
- Idempotency: duplicate requests with the same `Idempotency-Key` + `client_id` return the original response without creating a duplicate Job.
- Each Job is owned by the creating client. Only the owning client may query, modify, or delete the Job.

### 4.3 Job Query

**API:** `GET /api/v1/jobs/{job_id}`

**Response (`200 OK`):**

```json
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
  "client_id": "string"
}
```

**Behavior:**
- Returns `404 Not Found` if the Job does not exist.
- Returns `403 Forbidden` if the requesting client does not own the Job.

### 4.4 Job Deletion (Hard Delete with CleanUp)

**API:** `DELETE /api/v1/jobs/{job_id}`

**Behavior:**
- Accepts a Job ID as input. Internally resolves the associated Image Group ID (1:1 mapping).
- Deletes all built OS images from S3 storage (`s3://boot-images`) using `s3cmd del` to remove all objects matching the job_id pattern.
- Removes all NFS artifact files for the Job (config files, catalog JSON, generated inputs).
- Transitions the Image Group to `CLEANED` state.
- Marks the Job status as `CLEANED`.
- Records an audit event with cleanup details.
- Returns `204 No Content` on success.
- Returns `404 Not Found` if the Job does not exist.
- Returns `403 Forbidden` if the requesting client does not own the Job.
- Returns `409 Conflict` if the Image Group is in an active state.
- Returns `412 Precondition Failed` if the Job has already been cleaned.

> **Note:** This is a hard delete operation that removes all artifacts and images, not a soft delete (tombstone). The Job and Image Group records are preserved in the database with `CLEANED` status for audit trail.

### 4.5 File Upload

> **Gap addressed:** A-05 (File Upload Specification)

**User story:** As a Platform Operator, I want to upload input files for the build pipeline.

**Behavior:**
- The system accepts file uploads for the build pipeline input directory.
- Accepted file names and formats are validated against an allowlist.
- **Maximum upload size:** 5 MB per file (configurable).
- **Maximum archive size:** 50 MB uncompressed, 500 entries.
- **Partial upload semantics:** Only uploaded files are overwritten; existing files not included in the upload are preserved.
- **Security:** Files with path traversal sequences (e.g., `../`) are rejected. Empty files are rejected.

**Validation errors:**

| Scenario                        | HTTP Status | Error Code             |
|---------------------------------|-------------|------------------------|
| File exceeds max size            | `413`       | `FILE_TOO_LARGE`       |
| Empty file                       | `400`       | `FILE_EMPTY`           |
| Path traversal detected          | `400`       | `FILE_PATH_TRAVERSAL`  |
| Unsupported file format          | `422`       | `FILE_FORMAT_INVALID`  |

### 4.6 Build Stages

> **Gap addressed:** A-06 (Image Building Stage Details), C-03 (Build Stage Names and Count)

BuildStream defines the following build stages, executed in mandatory sequential order:

| Order | Stage Name                | API Endpoint                                              | Description                              |
|-------|---------------------------|-----------------------------------------------------------|------------------------------------------|
| 1     | `create-local-repository` | `POST /api/v1/jobs/{job_id}/stages/create-local-repository`| Creates a local package repository from input files via Ansible playbook |
| 2     | `parse-catalog`           | `POST /api/v1/jobs/{job_id}/stages/parse-catalog`          | Uploads and parses a Dell catalog JSON file to generate adapter policy output |
| 3     | `build-image`             | `POST /api/v1/jobs/{job_id}/stages/build-image`            | Builds the OS image using the local repository and parsed catalog output |

#### 4.6.1 Stage: `create-local-repository`

**API:** `POST /api/v1/jobs/{job_id}/stages/create-local-repository`

**Behavior:**
- Validates that the Job exists and is in a state allowing stage execution.
- Validates that required input files exist in the input directory.
- Transitions the Job from `CREATED` to `IN_PROGRESS`.
- Transitions the Stage from `PENDING` to `IN_PROGRESS`.
- Submits a playbook execution request asynchronously (non-blocking).
- Returns `202 Accepted` immediately.
- The Stage transitions to `COMPLETED` or `FAILED` upon receiving the asynchronous result.

**Response (`202 Accepted`):**

```json
{
  "job_id": "uuid",
  "stage": "create-local-repository",
  "status": "accepted",
  "submitted_at": "2026-04-08T10:01:00Z",
  "correlation_id": "string"
}
```

#### 4.6.2 Stage: `parse-catalog`

**API:** `POST /api/v1/jobs/{job_id}/stages/parse-catalog` (multipart file upload)

**Behavior:**
- Accepts a catalog JSON file via multipart upload.
- Validates: `.json` extension, valid JSON content, root element is a dictionary.
- Validates that the Job exists and preceding stages are `COMPLETED`.
- Processes the catalog to generate adapter policy output files.
- Stores generated artifacts in the artifact store.
- Returns `200 OK` with parsed results.

**Validation errors:**

| Scenario                        | HTTP Status | Error Code             |
|---------------------------------|-------------|------------------------|
| Non-JSON file extension          | `400`       | `FILE_JSON_INVALID`    |
| Invalid JSON content             | `400`       | `FILE_JSON_INVALID`    |
| JSON root is not a dictionary    | `400`       | `FILE_JSON_INVALID`    |
| Prerequisite stages not complete | `409`       | `STAGE_PREREQUISITE_PENDING` |

#### 4.6.3 Stage: `build-image`

**API:** `POST /api/v1/jobs/{job_id}/stages/build-image`

**Behavior:**
- Enforces sequential ordering — the stage only executes if all prerequisite stages are `COMPLETED`.
- Submits the image build asynchronously. Returns `202 Accepted`.
- Produces one or more OS images as output artifacts.
- Tags successful builds with a build identifier.
- The Stage transitions to `COMPLETED` or `FAILED` upon result.

**Sequential enforcement:**

```
create-local-repository  →  MUST be COMPLETED
parse-catalog            →  MUST be COMPLETED
build-image              →  CAN now execute
```

**Immutability:** A completed build stage cannot be re-run. The user must create a new Job to rebuild.

---

## 5. Feature 2 — Image Management

### 5.1 Overview

Image Management provides APIs for deploying built images to target nodes, validating deployments via automated tests, tagging images as passed or failed, and cleaning up failed or obsolete images.

### 5.2 Deploy

> **Gap addressed:** A-07 (Deployment Details)

**User story:** As a Platform Operator, I want to deploy a built image to target nodes.

**API:** `POST /api/v1/jobs/{job_id}/deploy`

**Request body:**

```json
{
  "image_group_id": "string (required)"
}
```

**Behavior:**
- Validates the Image Group exists, belongs to the specified Job, and is in `BUILT` state.
- Transitions the Image Group: `BUILT` → `DEPLOYING` → `DEPLOYED`.
- Returns `202 Accepted`.

**Validation errors:**

| Scenario                            | HTTP Status | Error Code                |
|-------------------------------------|-------------|---------------------------|
| Image Group not found                | `404`       | `IMAGE_GROUP_NOT_FOUND`   |
| Image Group not in `BUILT` state     | `409`       | `IMAGE_NOT_DEPLOYABLE`    |
| Image Group belongs to wrong Job     | `400`       | `IMAGE_JOB_MISMATCH`     |
| Re-deploying already deployed image  | `409`       | `IMAGE_ALREADY_DEPLOYED`  |

**Re-deployment semantics:** Re-deploying an Image Group that is already in `DEPLOYED` state is rejected. A new deployment requires a new build.

### 5.3 PXE Boot / Node Restart

> **Gap addressed:** A-08 (PXE Boot / Node Restart Details)

**User story:** As a Platform Operator, I want to PXE boot target nodes after deploying an image.

**API:** `POST /api/v1/jobs/{job_id}/restart`

**Request body:**

```json
{
  "disable_pxe_boot": false
}
```

| Field              | Type    | Required | Default | Description                                      |
|--------------------|---------|----------|---------|--------------------------------------------------|
| `disable_pxe_boot` | boolean | No       | `false` | If `true`, skip PXE boot for this restart request |

**Behavior:**
- Consumes the PXE mapping file to determine target nodes.
- **Node diff logic:** Only newly added nodes (not previously booted with the current image) are PXE-booted.
- Transitions the Image Group: `DEPLOYED` → `RESTARTING` → `RESTARTED`.
- Returns per-node status (which nodes were restarted, which were skipped).

### 5.4 TestValidate

> **Gap addressed:** A-09 (Validation Test Results Structure), D-02 ("Minimum Basic Tests" Definition)

**User story:** As a Platform Operator, I want to run validation tests against deployed images to confirm they work correctly.

**API:** `POST /api/v1/jobs/{job_id}/validate`

**Request body:**

```json
{
  "test_suite": "basic",
  "timeout": 600
}
```

| Field        | Type    | Required | Default              | Description                                      |
|--------------|---------|----------|----------------------|--------------------------------------------------|
| `test_suite` | string  | No       | All basic tests      | Specific test suite to run                        |
| `timeout`    | integer | No       | System-defined (600s)| Timeout in seconds                                |

**Behavior:**
- Transitions the Image Group: `RESTARTED` → `VALIDATING`.
- Executes minimum basic tests associated with each functional role on the deployed nodes.
- Tags the Image Group as `PASSED` or `FAILED` based on aggregate test results.

**"Minimum basic tests"** include tests associated with each functional role deployed to the nodes. Examples include network connectivity checks, service availability checks, and role-specific functionality tests. A test suite passes only if all individual tests pass; any failure causes the overall status to be `FAILED`.

**Response (`200 OK`) — Test Results:**

```json
{
  "job_id": "uuid",
  "image_group_id": "uuid",
  "overall_status": "PASSED",
  "summary": {
    "total_tests": 12,
    "passed": 12,
    "failed": 0
  },
  "results": [
    {
      "test_name": "network_connectivity",
      "status": "passed",
      "node": "node-001",
      "failure_details": null,
      "duration_ms": 1200
    },
    {
      "test_name": "slurm_daemon_active",
      "status": "passed",
      "node": "node-001",
      "failure_details": null,
      "duration_ms": 800
    }
  ]
}
```

### 5.5 CleanUp

> **Gap addressed:** B-01 (Automated Cleanup), C-02 (Automated vs. User-Initiated Cleanup), D-03 (Cleanup Failure Handling)

#### 5.5.1 Manual Cleanup

**Trigger:** User-initiated via `DELETE /api/v1/jobs/{job_id}` API or CleanUp Pipeline.

**Behavior:**
1. The system accepts a Job ID as input.
2. The system internally resolves the associated Image Group ID (1:1 mapping).
3. The system queries the `images` table to retrieve all image names (S3 paths) associated with the Image Group.
4. For each image, the system executes `s3cmd del s3://boot-images/<image_path>` to remove the image from S3 storage.
5. The system removes all NFS artifact files for the Job (config files, catalog JSON, inventories, generated inputs).
6. The system transitions the Image Group to `CLEANED` state and marks the Job as `CLEANED`.
7. The system records an audit event with cleanup type (`cleanup_manual`), files removed, S3 objects deleted, and timestamp.
8. The system returns `204 No Content` on success.

**Eligible states for cleanup:** `BUILT`, `PASSED`, `FAILED`. Cleanup is **not** permitted while stages are actively running (`DEPLOYING`, `RESTARTING`, `VALIDATING`).

**CleanUp Pipeline:** A dedicated CleanUp Pipeline (`.gitlab-ci-cleanup.yml`) is provided for operator-initiated cleanup. The pipeline:
1. Authenticates via OAuth2.
2. Calls `GET /api/v1/images` to list available Image Groups (showing both Job ID and Image Group ID).
3. Presents a selection UI for the operator to choose a Job ID.
4. Calls `DELETE /api/v1/jobs/{job_id}` for the selected Job.

#### 5.5.2 Automated CleanUp

**Behavior:**
- A cron job runs inside the BuildStream container every **24 hours** (configurable).
- The cron job queries the `image_groups` table for all records with status `FAILED`.
- For each `FAILED` Image Group, the system:
  a. Queries the `images` table to retrieve all image names (S3 paths) for the Image Group.
  b. Executes `s3cmd del s3://boot-images/<image_path>` for each image to remove from S3.
  c. Removes NFS artifact files for the associated Job.
  d. Transitions the Image Group to `CLEANED` and the Job to `CLEANED`.
  e. Records an audit event with reason `auto_cleanup_validation_failed`.
- The cron job logs all actions to the BuildStream audit log.

#### 5.5.3 Image Retention Limit

**Behavior:**
- The system enforces a maximum retention limit of **50** stored images per system (configurable).
- During the `build-image` stage, before building, the system checks the current count of non-CLEANED Image Groups.
- If the count equals or exceeds 50, the build is **aborted** with an error instructing the user to clean up existing jobs via the CleanUp Pipeline.
- The Build Pipeline exits with a clear error message: `"Image retention limit reached (50). Please clean up existing jobs using the CleanUp Pipeline before building new images."`

#### 5.5.4 Cleanup Failure Behavior

| Scenario                          | System Behavior                                          |
|-----------------------------------|----------------------------------------------------------|
| Cleanup succeeds                  | Image Group and artifacts removed, `200 OK` returned with summary |
| Cleanup partially fails (S3)      | Image Group remains in its previous state (no corruption); error response with details returned |
| Retry after failure               | User may retry the cleanup operation                      |
| Job not found                     | `404 Not Found`                                           |
| Image Group in active state       | `409 Conflict` — cleanup not allowed during active operations |
| Job already cleaned               | `412 Precondition Failed`                                 |

---

## 6. Authentication and Authorization

> **Gap addressed:** A-10 (Authentication / Authorization Specification)

### 6.1 Overview

BuildStream uses **OAuth 2.0 client credentials** flow with JWT bearer tokens for API authentication.

### 6.2 Client Registration

**API:** `POST /api/v1/auth/register` (secured by HTTP Basic Authentication)

**Request body:**

```json
{
  "client_name": "string (required)",
  "description": "string (optional)",
  "allowed_scopes": ["jobs:read", "jobs:write", "stages:execute", "catalog:read", "catalog:write", "deploy:execute"]
}
```

**Response (`201 Created`):**

```json
{
  "client_id": "uuid",
  "client_secret": "string (shown ONCE — save immediately)",
  "client_name": "string",
  "allowed_scopes": ["..."],
  "created_at": "2026-04-08T10:00:00Z",
  "expires_at": null
}
```

**Behavior:**
- Basic Auth credentials are stored in an Ansible Vault (encrypted at rest).
- The `client_secret` is displayed only at registration time and cannot be retrieved later. It is hashed (bcrypt) before storage.
- Maximum **1 OAuth client** can be registered at a time for this release.

### 6.3 Token Generation

**API:** `POST /api/v1/auth/token`

**Request body (form-encoded):**

```
grant_type=client_credentials
client_id=<client_id>
client_secret=<client_secret>
scope=jobs:read jobs:write stages:execute
```

**Response (`200 OK`):**

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "jobs:read jobs:write stages:execute"
}
```

**Behavior:**
- Verifies `client_id` and `client_secret` against stored records.
- Validates that requested scopes are a subset of the client's allowed scopes.
- Generates a signed JWT containing: `client_id`, `client_name`, `scopes`, `token_id`, `exp`.
- Tokens expire after a configurable duration (default: **3600 seconds**).

### 6.4 Token Verification

Every protected API endpoint requires a valid JWT bearer token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

- Missing, expired, or invalid tokens → `401 Unauthorized`
- Insufficient scope → `403 Forbidden`

### 6.5 Authorization Scopes

| Scope              | Description                          | Persona Access                    |
|--------------------|--------------------------------------|-----------------------------------|
| `jobs:read`        | Query job status                      | All personas                      |
| `jobs:write`       | Create and delete jobs                | Platform Operator, CI/CD Agent    |
| `stages:execute`   | Trigger build stages                  | Platform Operator, CI/CD Agent    |
| `catalog:read`     | Parse catalog files                   | Platform Operator, CI/CD Agent    |
| `catalog:write`    | Upload catalog files                  | Platform Operator                 |
| `deploy:execute`   | Deploy images, restart nodes          | Platform Operator                 |
| `admin:register`   | Register new OAuth clients            | System Administrator              |

---

## 7. API Contract Summary

> **Gap addressed:** A-11 (API Input/Output Specifications)

### 7.1 Endpoint Table

| Method   | Endpoint                                              | Auth           | Scope Required    | Description                    |
|----------|-------------------------------------------------------|----------------|-------------------|--------------------------------|
| `GET`    | `/`                                                   | None           | —                 | Welcome / service info         |
| `GET`    | `/health`                                             | None           | —                 | Health check                   |
| `POST`   | `/api/v1/auth/register`                               | Basic Auth     | —                 | Register OAuth client          |
| `POST`   | `/api/v1/auth/token`                                  | None (creds in body) | —           | Generate JWT token             |
| `POST`   | `/api/v1/jobs`                                        | JWT            | `jobs:write`      | Create new Job                 |
| `GET`    | `/api/v1/jobs/{job_id}`                               | JWT            | `jobs:read`       | Get Job status                 |
| `DELETE` | `/api/v1/jobs/{job_id}`                               | JWT            | `jobs:write`      | Delete Job (cleanup S3/NFS artifacts) |
| `GET`    | `/api/v1/jobs/{job_id}/artifacts/{label}`             | JWT            | `jobs:read`       | Download job artifact by label |
| `PUT`    | `/api/v1/jobs/{job_id}/upload`                        | JWT            | `jobs:write`      | Upload configuration files     |
| `POST`   | `/api/v1/jobs/{job_id}/stages/parse-catalog`          | JWT            | `catalog:read`    | Parse catalog file             |
| `GET`    | `/api/v1/jobs/{job_id}/catalog/roles`                 | JWT            | `catalog:read`    | Get catalog roles              |
| `POST`   | `/api/v1/jobs/{job_id}/stages/generate-input-files`   | JWT            | `stages:execute`  | Generate input files           |
| `POST`   | `/api/v1/jobs/{job_id}/stages/create-local-repository`| JWT            | `stages:execute`  | Trigger local repo stage       |
| `POST`   | `/api/v1/jobs/{job_id}/stages/build-image`            | JWT            | `stages:execute`  | Trigger image build            |
| `GET`    | `/api/v1/images`                                      | JWT            | `images:read`     | List image groups with filters |
| `POST`   | `/api/v1/jobs/{job_id}/stages/deploy`                 | JWT            | `deploy:execute`  | Deploy images to nodes         |
| `POST`   | `/api/v1/jobs/{job_id}/stages/restart`                | JWT            | `deploy:execute`  | PXE boot / restart nodes       |
| `POST`   | `/api/v1/jobs/{job_id}/stages/validate`               | JWT            | `stages:execute`  | Run validation tests           |

### 7.2 Common Request Headers

| Header               | Required | Description                                           |
|----------------------|----------|-------------------------------------------------------|
| `Authorization`      | Yes*     | Bearer JWT token (* except public endpoints)           |
| `Content-Type`       | Yes      | `application/json` or `multipart/form-data`            |
| `X-Client-Id`        | Yes      | Client identifier for ownership tracking               |
| `X-Correlation-Id`   | Yes      | Unique request correlation ID for distributed tracing  |
| `Idempotency-Key`    | Yes**    | Unique key for idempotent deduplication (** write ops)  |

### 7.3 Standard Error Response Format

All error responses follow a consistent structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error description",
    "details": {
      "field": "Additional context if applicable"
    },
    "correlation_id": "request-correlation-id",
    "timestamp": "2026-04-08T10:00:00Z"
  }
}
```

### 7.4 Standard HTTP Status Codes

| Status Code | Usage                                                              |
|-------------|--------------------------------------------------------------------|
| `200`       | Successful GET or synchronous operation                             |
| `201`       | Resource created (Job creation, client registration)                |
| `202`       | Accepted — async operation submitted (stage triggers)               |
| `204`       | No Content — successful deletion or cleanup                         |
| `400`       | Bad Request — invalid input, path traversal, malformed JSON         |
| `401`       | Unauthorized — missing or invalid authentication                    |
| `403`       | Forbidden — insufficient scope or not owner                         |
| `404`       | Not Found — resource does not exist                                 |
| `409`       | Conflict — invalid state transition or duplicate                    |
| `413`       | Payload Too Large — file exceeds size limit                         |
| `422`       | Unprocessable Entity — valid format but invalid content             |
| `429`       | Too Many Requests — rate limit exceeded                             |
| `500`       | Internal Server Error                                               |

---

## 8. Job Lifecycle State Machine

### 8.1 States

| State          | Description                                                        | Terminal? |
|----------------|--------------------------------------------------------------------|-----------|
| `CREATED`      | Job created, no stages executed                                     | No        |
| `IN_PROGRESS`  | At least one stage has been triggered                                | No        |
| `COMPLETED`    | All stages completed successfully                                    | Yes       |
| `FAILED`       | One or more stages failed                                            | Yes       |
| `CANCELLED`    | Job cancelled by the user                                            | Yes       |

### 8.2 Valid Transitions

| Current State  | Allowed Transitions                 | Trigger                             |
|----------------|-------------------------------------|-------------------------------------|
| `CREATED`      | `IN_PROGRESS`, `CANCELLED`          | First stage triggered, or cancel    |
| `IN_PROGRESS`  | `COMPLETED`, `FAILED`, `CANCELLED`  | All stages done, stage failure, or cancel |
| `COMPLETED`    | *(none — terminal)*                 | —                                   |
| `FAILED`       | *(none — terminal)*                 | —                                   |
| `CANCELLED`    | *(none — terminal)*                 | —                                   |

### 8.3 Transition Diagram

```
                    ┌──────────┐
                    │ CREATED  │
                    └────┬─────┘
                         │ start()
                    ┌────▼─────┐
              ┌─────│IN_PROGRESS├─────┐
              │     └────┬─────┘     │
              │          │           │
         fail()     complete()   cancel()
              │          │           │
         ┌────▼──┐  ┌───▼────┐  ┌──▼──────┐
         │FAILED │  │COMPLETED│  │CANCELLED│
         └───────┘  └────────┘  └─────────┘
```

Any attempt to transition from a terminal state is rejected with `409 Conflict`.

---

## 9. Build Stage State Machine

### 9.1 States

| State          | Description                                     | Terminal? |
|----------------|-------------------------------------------------|-----------|
| `PENDING`      | Stage has not yet started                        | No        |
| `IN_PROGRESS`  | Stage is currently executing                     | No        |
| `COMPLETED`    | Stage finished successfully                      | Yes       |
| `FAILED`       | Stage finished with an error                     | Yes       |
| `SKIPPED`      | Stage was skipped (not applicable)               | Yes       |

### 9.2 Valid Transitions

| Current State  | Allowed Transitions        | Trigger                       |
|----------------|----------------------------|-------------------------------|
| `PENDING`      | `IN_PROGRESS`, `SKIPPED`   | Stage triggered, or skipped   |
| `IN_PROGRESS`  | `COMPLETED`, `FAILED`      | Execution result              |
| `COMPLETED`    | *(terminal)*               | —                             |
| `FAILED`       | *(terminal)*               | —                             |
| `SKIPPED`      | *(terminal)*               | —                             |

---

## 10. Image Group State Machine

> **Gap addressed:** A-15 (Image Group State Machine)

### 10.1 States

| State          | Description                                                        | Terminal? |
|----------------|--------------------------------------------------------------------|-----------|
| `BUILT`        | Image successfully built                                             | No        |
| `DEPLOYING`    | Image being deployed to target nodes                                 | No        |
| `DEPLOYED`     | Image deployed to nodes                                              | No        |
| `RESTARTING`   | Target nodes being PXE-booted / restarted                            | No        |
| `RESTARTED`    | Nodes restarted with the new image                                   | No        |
| `VALIDATING`   | Automated validation tests running                                   | No        |
| `PASSED`       | All validation tests passed                                          | Yes       |
| `FAILED`       | One or more validation tests failed                                  | Yes*      |
| `CLEANED`      | Image and artifacts cleaned up                                       | Yes       |

*`FAILED` images are eligible for cleanup.

### 10.2 Valid Transitions

| Current State  | Allowed Transitions    | Trigger                          |
|----------------|------------------------|----------------------------------|
| `BUILT`        | `DEPLOYING`            | Deploy request                   |
| `DEPLOYING`    | `DEPLOYED`, `FAILED`   | Deployment success / failure     |
| `DEPLOYED`     | `RESTARTING`           | Restart request                  |
| `RESTARTING`   | `RESTARTED`, `FAILED`  | Restart success / failure        |
| `RESTARTED`    | `VALIDATING`           | Validate request                 |
| `VALIDATING`   | `PASSED`, `FAILED`     | Test results                     |
| `PASSED`       | *(terminal)*           | —                                |
| `FAILED`       | `CLEANED`              | Cleanup request                  |
| `CLEANED`      | *(terminal)*           | —                                |

### 10.3 Transition Diagram

```
BUILT → DEPLOYING → DEPLOYED → RESTARTING → RESTARTED → VALIDATING → PASSED
                                                                    ↘ FAILED → CLEANED
```

Each intermediate state can also transition to `FAILED` on error. Invalid transitions are rejected with `409 Conflict`.

---

## 11. Detailed Workflow Descriptions

> **Gap addressed:** A-03 (Detailed Workflow Descriptions)

### 11.1 End-to-End Build and Deploy Workflow

**Preconditions:**
- OIM host is operational with BuildStream container running
- OAuth client is registered and JWT token is available
- Input files (Omnia input folder) are available

**Step-by-step flow:**

| Step | User Action                                     | API Call                                                     | Expected Response         | State Change                     |
|------|-------------------------------------------------|--------------------------------------------------------------|---------------------------|----------------------------------|
| 1    | Obtain JWT token                                 | `POST /api/v1/auth/token`                                    | `200` with `access_token` | —                                |
| 2    | Create a build Job                               | `POST /api/v1/jobs`                                          | `201` with `job_id`       | Job: → `CREATED`                 |
| 3    | Upload input files                               | Upload endpoint                                               | `200 OK`                  | —                                |
| 4    | Trigger create-local-repository stage            | `POST /jobs/{id}/stages/create-local-repository`             | `202 Accepted`            | Job: → `IN_PROGRESS`; Stage: `PENDING` → `IN_PROGRESS` |
| 5    | Poll for stage completion                        | `GET /jobs/{id}`                                              | `200` with stage states   | Stage: → `COMPLETED` (async)     |
| 6    | Trigger parse-catalog stage (upload catalog)     | `POST /jobs/{id}/stages/parse-catalog`                       | `200` with parsed results | Stage: → `COMPLETED`             |
| 7    | Trigger build-image stage                        | `POST /jobs/{id}/stages/build-image`                         | `202 Accepted`            | Stage: `PENDING` → `IN_PROGRESS` |
| 8    | Poll for build completion                        | `GET /jobs/{id}`                                              | `200` with stage states   | Stage: → `COMPLETED`; Image Group: → `BUILT` |
| 9    | Deploy image to nodes                            | `POST /jobs/{id}/deploy`                                     | `202 Accepted`            | Image Group: `BUILT` → `DEPLOYING` → `DEPLOYED` |
| 10   | PXE boot / restart nodes                         | `POST /jobs/{id}/restart`                                    | `202 Accepted`            | Image Group: `DEPLOYED` → `RESTARTING` → `RESTARTED` |
| 11   | Run validation tests                             | `POST /jobs/{id}/validate`                                   | `200` with test results   | Image Group: `RESTARTED` → `VALIDATING` → `PASSED`/`FAILED` |
| 12   | (If failed) Clean up images                      | `DELETE /jobs/{id}`                                          | `204 No Content`          | Image Group: `FAILED` → `CLEANED` |

**Postconditions:**
- Job is in `COMPLETED` state (if all stages passed)
- Image Group is in `PASSED` state (if validation succeeded)
- All state transitions have corresponding audit events

### 11.2 GitLab CI/CD Pipeline Workflow

| CI/CD Stage         | API Call                                           | Notes                          |
|---------------------|----------------------------------------------------|--------------------------------|
| `auth`              | `POST /api/v1/auth/token`                          | Obtain JWT token               |
| `create-job`        | `POST /api/v1/jobs`                                | Create build job               |
| `upload-inputs`     | `PUT /api/v1/jobs/{job_id}/upload` (Implicit)      | From GitLab repo artifacts     |
| `create-local-repo` | `POST /jobs/{id}/stages/create-local-repository`   | Trigger + poll until complete  |
| `parse-catalog`     | `POST /jobs/{id}/stages/parse-catalog`             | Upload catalog JSON            |
| `build-image`       | `POST /jobs/{id}/stages/build-image`               | Trigger + poll until complete  |
| `list-images`       | `GET /api/v1/images`                               | UI Selection (Deploy & CleanUp)|
| `deploy`            | `POST /jobs/{id}/deploy`                           | Deploy to target nodes         |
| `restart-nodes`     | `POST /jobs/{id}/restart`                          | PXE boot nodes                 |
| `validate`          | `POST /jobs/{id}/validate`                         | Run tests, check results       |
| `cleanup` (on fail) | `DELETE /jobs/{id}`                                | Cleanup failed images          |

### 11.3 Cleanup Workflow

**Preconditions:** Image Group exists in `FAILED` state.

| Step | User Action                                     | Expected Response                                 |
|------|-------------------------------------------------|---------------------------------------------------|
| 1    | Query Job to identify failed Image Group         | `200` with Image Group in `FAILED` state          |
| 2    | Call Delete API: `DELETE /jobs/{id}`              | `204 No Content`                                  |
| 3    | (If cleanup fails) Retry                         | System allows retry; Image Group remains in previous state |

### 11.4 Retry / Resume

- Individual failed stages are **not re-runnable** in this release (immutability constraint).
- To retry, the user creates a new Job and re-executes the full pipeline.
- The system provides clear error information to help diagnose the failure before retrying.

---

## 12. Error Handling

> **Gap addressed:** A-13 (Comprehensive Error Handling Guide), D-01 (Error Flagging Behavior)

### 12.1 Authentication Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Missing Authorization header              | `401`     | `AUTH_MISSING`           | Include Bearer token in request     |
| Expired JWT token                         | `401`     | `AUTH_TOKEN_EXPIRED`     | Request a new token                 |
| Invalid JWT signature                     | `401`     | `AUTH_TOKEN_INVALID`     | Verify token source and signing key |
| Insufficient scope                        | `403`     | `AUTH_SCOPE_INSUFFICIENT`| Request token with required scope   |
| Invalid Basic Auth credentials            | `401`     | `AUTH_CREDENTIALS_INVALID`| Verify Basic Auth credentials      |
| Max clients exceeded                      | `409`     | `AUTH_MAX_CLIENTS`       | Delete existing client first        |

### 12.2 Job Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Job not found                             | `404`     | `JOB_NOT_FOUND`          | Verify job_id                       |
| Job not owned by requesting client        | `403`     | `JOB_ACCESS_DENIED`      | Use correct client credentials      |
| Job in terminal state                     | `409`     | `JOB_STATE_TERMINAL`     | Create a new job                    |
| Duplicate idempotency key (different client)| `409`   | `IDEMPOTENCY_CONFLICT`   | Use a unique idempotency key       |

### 12.3 Stage Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Prerequisite stage not completed          | `409`     | `STAGE_PREREQUISITE_PENDING` | Complete prerequisite stages first |
| Stage already completed (immutable)       | `409`     | `STAGE_ALREADY_COMPLETED`| Stage cannot be re-run              |
| Required input files missing              | `400`     | `STAGE_INPUT_MISSING`    | Upload required input files         |
| Job state does not allow stage execution  | `409`     | `JOB_STATE_INVALID`      | Check job state before triggering   |

### 12.4 File Upload Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| File exceeds max size                     | `413`     | `FILE_TOO_LARGE`         | Reduce file size                    |
| Empty file uploaded                       | `400`     | `FILE_EMPTY`             | Upload a non-empty file             |
| Path traversal detected                   | `400`     | `FILE_PATH_TRAVERSAL`    | Remove `../` from file paths        |
| Invalid file format                       | `422`     | `FILE_FORMAT_INVALID`    | Use supported file format           |
| Invalid JSON content                      | `400`     | `FILE_JSON_INVALID`      | Fix JSON syntax                     |

### 12.5 Deployment and Image Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Image Group not found                     | `404`     | `IMAGE_GROUP_NOT_FOUND`  | Verify image_group_id               |
| Image Group not in deployable state       | `409`     | `IMAGE_NOT_DEPLOYABLE`   | Build must complete first           |
| Image Group already deployed              | `409`     | `IMAGE_ALREADY_DEPLOYED` | Cannot re-deploy; create new build  |
| Image not available for job               | `400`     | `IMAGE_JOB_MISMATCH`    | Verify Image Group belongs to Job   |
| Image Group not eligible for cleanup      | `409`     | `CLEANUP_STATE_INVALID`  | Only FAILED images can be cleaned   |
| Cleanup operation failed                  | `500`     | `CLEANUP_FAILED`         | Retry the cleanup operation         |

---

## 13. Customer-Facing Constraints

> **Gap addressed:** A-12 (Customer-Facing Constraints)

| #   | Constraint                                                                   |
|-----|-----------------------------------------------------------------------------|
| 1   | **Architecture:** Only x86_64 architecture is supported                      |
| 2   | **Concurrency:** Only one pipeline (build + deploy) may execute at a time    |
| 3   | **Upload size:** Maximum file upload size is 5 MB per file (configurable)    |
| 4   | **Archive size:** Maximum uncompressed archive size is 50 MB                  |
| 5   | **Archive entries:** Maximum 500 entries in an uploaded archive               |
| 6   | **Cluster:** Single-cluster deployment only                                   |
| 7   | **Deployment type:** Physical nodes only (no VM + physical hybrid)            |
| 8   | **OAuth clients:** Maximum 1 registered OAuth client                          |
| 9   | **Token lifetime:** JWT tokens expire after 3600 seconds (default)            |
| 10  | **Cleanup**: User-initiated via CleanUp API + automated cron for validation-failed images (24h) |
| 11  | **Retention limit**: Maximum 50 non-CLEANED Image Groups; build aborted if limit reached |

> **Decision (C-01):** Build and deploy execution is **sequential only** for this release. The BSpec v1.0 reference to concurrent execution is deferred.

---

## 14. Rate Limiting

> **Gap addressed:** A-16 (Rate Limiting Specification)

| API Category              | Rate Limit          | Key                  | Response on Exceed               |
|---------------------------|---------------------|----------------------|----------------------------------|
| File uploads              | 10 requests / min   | Per `client_id`      | `429 Too Many Requests` with `Retry-After` header |
| Stage triggers            | 5 requests / min    | Per `client_id`      | `429 Too Many Requests` with `Retry-After` header |
| Job listing / query       | 60 requests / min   | Per `client_id`      | `429 Too Many Requests` with `Retry-After` header |
| Token generation          | 10 requests / min   | Per `client_id`      | `429 Too Many Requests` with `Retry-After` header |
| Client registration       | 3 requests / min    | Per source IP        | `429 Too Many Requests` with `Retry-After` header |

---

## 15. Non-Functional Requirements

> **Gap addressed:** B-05 (Performance Requirements)

### 15.1 Performance

| Requirement                                              | Target                              |
|----------------------------------------------------------|-------------------------------------|
| API response time for synchronous operations              | P95 ≤ 500ms                        |
| Concurrent pipeline support                               | 1 pipeline (sequential execution)  |

### 15.2 Reliability

| Requirement                                              | Target                              |
|----------------------------------------------------------|-------------------------------------|
| Idempotent operations                                     | All write operations are idempotent |
| Audit trail                                               | All state transitions are logged   |
| Optimistic locking                                        | Version field on Job and Stage entities prevents concurrent modification |

### 15.3 Security

| Requirement                                              | Target                              |
|----------------------------------------------------------|-------------------------------------|
| API transport                                             | HTTPS (TLS, port 443)             |
| Authentication                                            | OAuth 2.0 client credentials + JWT |
| Credential storage                                        | Ansible Vault (encrypted at rest)  |
| Path traversal protection                                 | All file operations validated      |

---

## 16. Acceptance Criteria

> **Gap addressed:** A-14 (Testable Acceptance Criteria)

### 16.1 Feature 1 — Workflow Optimization

| AC ID    | Criterion                                                                                       |
|----------|-------------------------------------------------------------------------------------------------|
| AC-WF-01 | A Job can be created via API and returns a valid Job ID in UUID format                           |
| AC-WF-02 | The `create-local-repository` stage can be triggered and completes asynchronously                |
| AC-WF-03 | The `parse-catalog` stage accepts a valid JSON catalog file and returns parsed output            |
| AC-WF-04 | The `build-image` stage enforces prerequisite ordering and rejects out-of-order execution        |
| AC-WF-05 | Stages transition through the correct states (`PENDING` → `IN_PROGRESS` → `COMPLETED`)          |
| AC-WF-06 | A failed stage transitions the Job to `FAILED` state                                             |
| AC-WF-07 | Duplicate requests with the same `Idempotency-Key` return the original response                 |
| AC-WF-08 | A Job in terminal state rejects further stage execution with `409 Conflict`                       |
| AC-WF-09 | All state transitions produce audit events                                                       |
| AC-WF-10 | File uploads exceeding the size limit are rejected with `413`                                    |
| AC-WF-11 | Path traversal in file uploads is rejected with `400`                                            |
| AC-WF-12 | The complete build pipeline can be executed end-to-end                                            |

### 16.2 Feature 2 — Image Management

| AC ID    | Criterion                                                                                       |
|----------|-------------------------------------------------------------------------------------------------|
| AC-IM-01 | A built Image Group can be deployed to target nodes                                              |
| AC-IM-02 | Deployment transitions the Image Group through `DEPLOYING` → `DEPLOYED`                          |
| AC-IM-03 | Deployed nodes can be PXE-booted / restarted                                                     |
| AC-IM-04 | Node diff logic ensures only new nodes are PXE-booted                                            |
| AC-IM-05 | Validation tests run and return structured results                                                |
| AC-IM-06 | Images are tagged as `PASSED` or `FAILED` based on test results                                  |
| AC-IM-07 | Failed images can be cleaned up via the cleanup API                                               |
| AC-IM-08 | Cleanup removes all associated artifacts                                                         |
| AC-IM-09 | Cleanup failure does not leave Image Group in a corrupted state                                  |
| AC-IM-10 | Deploying an Image Group not in `BUILT` state is rejected with `409`                              |
| AC-IM-11 | Re-deploying an already deployed Image Group is rejected with `409`                               |

### 16.3 Authentication and Authorization

| AC ID    | Criterion                                                                                       |
|----------|-------------------------------------------------------------------------------------------------|
| AC-AU-01 | OAuth client can be registered with valid Basic Auth credentials                                 |
| AC-AU-02 | Client registration returns `client_id` and `client_secret`                                      |
| AC-AU-03 | JWT token can be obtained with valid client credentials                                          |
| AC-AU-04 | Protected endpoints reject requests without valid JWT tokens (`401`)                              |
| AC-AU-05 | Endpoints enforce scope requirements (`403` for insufficient scope)                               |
| AC-AU-06 | Expired tokens are rejected (`401`)                                                               |
| AC-AU-07 | Max client limit is enforced (`409` when exceeded)                                                |

---

## 17. Future Considerations

> **Gap addressed:** B-02, B-03, B-04 (Clarification / Deferred Items)

| Item ID | Feature                                  | Notes                                                        |
|---------|------------------------------------------|--------------------------------------------------------------|
| ~~DF-01~~ | ~~Automated scheduled cleanup~~         | **Moved to in-scope** — cron job every 24 hours for validation-failed images |
| DF-02   | Concurrent pipeline execution             | Support multiple simultaneous build/deploy pipelines          |
| DF-03   | "Promoted" image tagging                  | Ability to tag images as "promoted" for production use. Disposition: clarify whether this maps to `PASSED` or is a separate concept |
| DF-04   | Restart API with direct PXE mapping file  | Upload PXE mapping file via restart endpoint                 |
| DF-05   | Deploy via CSV mapping file               | Deploy using a CSV pointing to a mapping file                 |
| DF-06   | Input folder versioning in GitLab         | Auto-versioning of generated input files — clarify if implicit, pipeline-level, or deferred |
| DF-07   | Multi-cluster deployment                  | Support deployments across multiple clusters                  |
| DF-08   | Non-x86 architecture support              | ARM and other architectures                                   |
| DF-09   | Persistent database (PostgreSQL)          | Replace in-memory repositories with durable storage           |

---

## 18. Glossary

| Term               | Definition                                                                                        |
|--------------------|---------------------------------------------------------------------------------------------------|
| **BuildStream**    | FastAPI-based microservice providing a RESTful API for orchestrating Omnia OS image build workflows |
| **Job**            | A unit of work representing a complete build pipeline execution                                     |
| **Stage**          | A discrete step within a Job (e.g., `create-local-repository`, `parse-catalog`, `build-image`)     |
| **Image Group**    | A collection of OS images produced by a build pipeline, tracked through deployment and validation   |
| **OIM**            | Omnia Infrastructure Manager — the host machine running Omnia services                             |
| **PXE Boot**       | Preboot Execution Environment — network boot mechanism for deploying images to nodes               |
| **Artifact**       | A generated output file produced during a build stage                                              |
| **JWT**            | JSON Web Token — used for API authentication                                                       |
| **Idempotency Key**| A unique identifier (`Idempotency-Key` header) ensuring that repeated API calls produce the same result |
| **Optimistic Locking** | Version field on entities to detect and reject concurrent modifications                        |

---

## 19. Gap Analysis Traceability

This section maps each gap identified in the BSpec Gap Analysis Report to its resolution in this document.

| Gap ID | Topic                                    | Resolution                                        | Section          |
|--------|------------------------------------------|---------------------------------------------------|------------------|
| A-01   | Scope definition                          | In-Scope / Out-of-Scope tables added              | [2](#2-scope)    |
| A-02   | User personas                             | Four personas defined with roles and auth          | [3](#3-user-personas) |
| A-03   | Detailed workflow descriptions             | Step-by-step workflows with pre/postconditions    | [11](#11-detailed-workflow-descriptions) |
| A-04   | Job creation specification                 | Full API contract with request/response schemas   | [4.2](#42-job-creation) |
| A-05   | File upload specification                  | Upload rules, size limits, security constraints   | [4.5](#45-file-upload) |
| A-06   | Image building stage details               | Three stages defined with endpoints and behavior  | [4.6](#46-build-stages) |
| A-07   | Deployment API details                     | Deploy contract with validation and re-deploy rules | [5.2](#52-deploy) |
| A-08   | PXE boot / node restart details            | disable_pxe_boot, node diff logic specified       | [5.3](#53-pxe-boot--node-restart) |
| A-09   | Validation test results structure          | Full results schema with per-test fields          | [5.4](#54-testvalidate) |
| A-10   | Authentication / authorization             | OAuth 2.0 flow, scopes, per-persona access        | [6](#6-authentication-and-authorization) |
| A-11   | API input/output specifications            | Full endpoint table, headers, error format, codes | [7](#7-api-contract-summary) |
| A-12   | Customer-facing constraints                | 10 constraints enumerated                          | [13](#13-customer-facing-constraints) |
| A-13   | Comprehensive error handling               | ~25 error scenarios with codes and user actions   | [12](#12-error-handling) |
| A-14   | Testable acceptance criteria               | 30 individually traceable criteria                 | [16](#16-acceptance-criteria) |
| A-15   | Image Group state machine                  | Complete state machine with transitions            | [10](#10-image-group-state-machine) |
| A-16   | Rate limiting specification                | Per-API rate limits with response behavior         | [14](#14-rate-limiting) |
| B-01   | Automated cleanup disposition              | **In-scope**: cron-based auto-cleanup + user-initiated CleanUp API | [5.5](#55-cleanup) |
| B-02   | "Promoted" image status                    | Deferred; clarification needed                     | [17](#17-future-considerations) |
| B-03   | Input folder versioning in GitLab          | Deferred; clarification needed                     | [17](#17-future-considerations) |
| B-04   | "Good to have" deferred features           | Tracked in Future Considerations                   | [17](#17-future-considerations) |
| B-05   | Performance requirements                   | Performance section added                          | [15](#15-non-functional-requirements) |
| C-01   | Concurrent build & deploy execution        | Decision: sequential only for this release         | [13](#13-customer-facing-constraints) |
| C-02   | Automated vs. user-initiated cleanup       | Decision: **both** — user-initiated CleanUp API + automated cron for FAILED images | [5.5](#55-cleanup) |
| C-03   | Build stage names and count                | Three stages confirmed with kebab-case names       | [4.6](#46-build-stages) |
| D-01   | Error flagging behavior                    | Specific HTTP codes and error codes defined        | [12](#12-error-handling) |
| D-02   | "Minimum basic tests" definition           | Test categories and pass/fail criteria specified   | [5.4](#54-testvalidate) |
| D-03   | Cleanup failure handling                   | Failure behavior, retry, and state preservation specified | [5.5](#55-cleanup) |

---

*End of BuildStream BSpec v2.0*
