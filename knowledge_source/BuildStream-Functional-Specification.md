# BuildStream — Functional Specification

| Field                | Value                                                                 |
|----------------------|-----------------------------------------------------------------------|
| Version              | 1.1                                                                   |
| Date                 | 2026-05-02                                                            |
| Status               | Draft                                                                 |
| Capability ID        | 16427                                                                 |
| Capability Name      | NERSC Automated Tools NRE Milestone 4                                 |
| Derived From         | BuildStream BSpec v2.1, BuildStream BSpec Gap Analysis Report         |
| Spec Phase           | Phase 3 — Functional Specification (per Spec-Driven Development)      |
| Audience             | Engineering Team, QA, Technical Leads                                 |

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [References](#2-references)
3. [Definitions and Acronyms](#3-definitions-and-acronyms)
4. [User Personas](#4-user-personas)
5. [Scope Boundaries](#5-scope-boundaries)
6. [System Overview](#6-system-overview)
7. [Functional Requirements — Feature 1: Workflow Optimization](#7-functional-requirements--feature-1-workflow-optimization)
8. [Functional Requirements — Feature 2: Image Management](#8-functional-requirements--feature-2-image-management)
9. [Authentication and Authorization](#9-authentication-and-authorization)
10. [API Functional Contract Summary](#10-api-functional-contract-summary)
11. [Job Lifecycle and State Machine](#11-job-lifecycle-and-state-machine)
12. [Image Group State Machine](#12-image-group-state-machine)
13. [Build Stage State Machine](#13-build-stage-state-machine)
14. [User Workflows](#14-user-workflows)
15. [Data Flow Diagrams](#15-data-flow-diagrams)
16. [Input and Output Specifications](#16-input-and-output-specifications)
17. [Business Rules and Validations](#17-business-rules-and-validations)
18. [Customer-Facing Constraints](#18-customer-facing-constraints)
19. [Error Handling Specification](#19-error-handling-specification)
20. [Non-Functional Requirements](#20-non-functional-requirements)
21. [Acceptance Criteria](#21-acceptance-criteria)
22. [Open Items and Deferred Features](#22-open-items-and-deferred-features)
23. [Traceability Matrix](#23-traceability-matrix)

---

## 1. Purpose and Scope

### 1.1 Purpose

This Functional Specification defines **WHAT** the BuildStream system must do from an engineering perspective. It translates the BSpec (Business Specification) into actionable functional requirements for the engineering and QA teams. This document does **not** prescribe HOW to implement these requirements — that is the responsibility of the Engineering Specification (Phase 4).

### 1.2 Document Scope

This document covers the functional requirements for the two core features of BuildStream:

- **Feature 1: Workflow Optimization** — Automating the end-to-end build pipeline for Omnia OS images through a RESTful API.
- **Feature 2: Image Management** — Managing, deploying, validating, and cleaning up built images.

### 1.3 Intended Audience

| Audience             | Usage                                                           |
|----------------------|-----------------------------------------------------------------|
| Engineering Team     | Understand what functionality must be built                      |
| QA / Test Engineers  | Derive test specifications and test cases                        |
| Technical Leads      | Plan component decomposition and engineering spec                |
| Product Management   | Validate that functional requirements match business intent      |

---

## 2. References

| Document                                         | Version | Purpose                                |
|--------------------------------------------------|---------|----------------------------------------|
| BuildStream BSpec                                 | v2.0    | Business Specification (source)        |
| BuildStream BSpec Gap Analysis Report             | v1.0    | Gap identification and recommendations |
| Omnia Build Stream Bring-Up Sequence              | 2025    | System architecture and code flow      |
| Spec-Driven Development Approach                  | v1.0    | Process methodology                    |

---

## 3. Definitions and Acronyms

| Term               | Definition                                                                                        |
|--------------------|---------------------------------------------------------------------------------------------------|
| **BuildStream**    | FastAPI-based microservice providing a RESTful API for orchestrating Omnia OS image build workflows |
| **Job**            | A unit of work representing a complete build pipeline execution                                     |
| **Stage**          | A discrete step within a Job (e.g., create-local-repository, parse-catalog)                        |
| **Image Group**    | A collection of OS images produced by a build pipeline, tracked through deployment and validation   |
| **OIM**            | Omnia Infrastructure Manager — the host machine running Omnia services                             |
| **Pipeline Phase** | A logical grouping of stages within the build workflow                                              |
| **PXE Boot**       | Preboot Execution Environment — network boot mechanism for deploying images to nodes               |
| **Artifact**       | A generated output file produced during a build stage                                              |
| **NFS Queue**      | File-based asynchronous communication mechanism between BuildStream API and Omnia Core             |
| **JWT**            | JSON Web Token — used for API authentication                                                       |
| **Idempotency Key**| A unique identifier ensuring that repeated API calls produce the same result                       |

---

## 4. User Personas

The following personas interact with the BuildStream system. Each persona has distinct roles, access levels, and interaction patterns.

### 4.1 Platform Operator

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Role               | Primary user responsible for building and deploying Omnia OS images   |
| Interactions       | Full API access — create jobs, trigger stages, deploy, validate       |
| Authentication     | OAuth 2.0 client credentials (JWT bearer token)                       |
| Key Workflows      | End-to-end build pipeline, deployment, validation, cleanup            |

### 4.2 CI/CD Pipeline Agent

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Role               | Automated agent (e.g., GitLab CI/CD) that triggers build workflows    |
| Interactions       | Programmatic API access via scripts/pipelines                         |
| Authentication     | OAuth 2.0 client credentials (JWT bearer token)                       |
| Key Workflows      | Automated build triggers, status polling, artifact retrieval          |

### 4.3 Direct API Consumer

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Role               | Developer or tool integrating directly with the BuildStream API       |
| Interactions       | REST API calls via curl, Postman, or custom clients                   |
| Authentication     | OAuth 2.0 client credentials (JWT bearer token)                       |
| Key Workflows      | Job management, stage execution, status queries                       |

### 4.4 System Administrator

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Role               | Manages OIM infrastructure, container lifecycle, and credentials      |
| Interactions       | OAuth client registration, system configuration, cleanup              |
| Authentication     | Basic Auth (for client registration); JWT (for API operations)        |
| Key Workflows      | Client registration, system health checks, teardown                   |

---

## 5. Scope Boundaries

### 5.1 In-Scope (This Release)

| # | Item                                                                       |
|---|----------------------------------------------------------------------------|
| 1 | RESTful API for build pipeline orchestration                                |
| 2 | Job lifecycle management (create, query, delete)                            |
| 3 | Build stages: parse-catalog, generate-input-files, create-local-repository, build-image |
| 4 | OAuth 2.0 client credentials authentication with JWT tokens                 |
| 5 | Image building workflow (parse catalog, generate input files, build image)  |
| 6 | Image deployment via deploy API                                             |
| 7 | Node PXE boot / restart for image provisioning                              |
| 8 | Image validation (test execution and pass/fail tagging)                     |
| 9 | Image cleanup via CleanUp API (`DELETE /api/v1/jobs/{job_id}`) — S3 + NFS artifact deletion, CLEANED status transition |
| 10 | Configuration file upload via Upload API (`PUT /api/v1/jobs/{job_id}/upload`) with file allowlist, path traversal prevention, size limits |
| 11 | Pipeline decomposition: Build Pipeline (.gitlab-ci-build.yml), Deploy Pipeline (.gitlab-ci-deploy.yml), Cleanup Pipeline (.gitlab-ci-cleanup.yml) |
| 12 | Dynamic child pipeline generation for image selection with actual image_group names (e.g., 'image-build19') |
| 13 | Image group lifecycle tracking with state machine (BUILT → DEPLOYING → DEPLOYED → VALIDATING → PASSED/FAILED → CLEANED) |
| 14 | Database schema: image_groups and images tables with 1:1 Job-to-ImageGroup mapping |
| 15 | Semicolon-delimited S3 paths for EFI and legacy boot images (VARCHAR(512)) |
| 16 | Artifact storage and retrieval via `GET /api/v1/jobs/{job_id}/artifacts/{label}` |
| 17 | Images API (`GET /api/v1/images`) with status filtering and pagination |
| 18 | Idempotent API operations with Idempotency-Key header                       |
| 19 | Audit event logging for all state transitions                               |
| 20 | x86_64 and aarch64 architecture support                                     |
| 21 | Build pipeline summary filtering (displays only build-related stages)       |

### 5.2 Out-of-Scope (This Release)

| # | Item                                                                       |
|---|----------------------------------------------------------------------------|
| 1 | Multi-cluster deployments                                                   |
| 2 | Non-x86 architectures (ARM, etc.)                                           |
| 3 | VM + physical hybrid deployments                                            |
| ~~4~~ | ~~Automated scheduled cleanup~~ — **Moved to In-Scope** (cron-based cleanup of validation-failed images) |
| 5 | Concurrent/simultaneous pipeline execution                                  |
| 6 | "Promoted" image tagging                                                    |
| 7 | Direct PXE mapping file upload via restart API                              |
| 8 | Deploy via CSV pointing to a mapping file                                   |
| 9 | Persistent database storage (PostgreSQL) — currently in-memory              |
| 10| Scheduled or background synchronization                                     |

---

## 6. System Overview

### 6.1 System Context

BuildStream is a RESTful microservice that provides an API-driven workflow for building, deploying, validating, and managing Omnia OS images. It runs as a containerized service on the OIM host and communicates with the Omnia Core container for executing Ansible playbooks.

### 6.2 High-Level System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          Consumers                               │
│                                                                   │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│   │  Platform     │  │  GitLab      │  │  Direct API          │  │
│   │  Operator     │  │  CI/CD Agent │  │  Consumer            │  │
│   └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│          │                 │                      │               │
└──────────┼─────────────────┼──────────────────────┼───────────────┘
           │                 │                      │
           └─────────────────┼──────────────────────┘
                             │
                     HTTPS (port 443)
                             │
                             ▼
                ┌────────────────────────┐
                │   BuildStream API      │
                │   (REST / JSON)        │
                │                        │
                │  • Job Management      │
                │  • Build Stages        │
                │  • Image Deployment    │
                │  • Image Validation    │
                │  • Image Cleanup       │
                │  • Authentication      │
                └────────────┬───────────┘
                             │
                    Async (NFS Queue)
                             │
                             ▼
                ┌────────────────────────┐
                │   Omnia Core           │
                │                        │
                │  • Ansible Playbooks   │
                │  • Local Repo Setup    │
                │  • Image Building      │
                │  • PXE Boot Mgmt       │
                └────────────────────────┘
```

### 6.3 Core Feature Summary

| Feature                  | Description                                                                   |
|--------------------------|-------------------------------------------------------------------------------|
| **Workflow Optimization** | Automates the end-to-end build pipeline: input file management, local repository creation, catalog parsing, and image building through a sequenced set of API-driven stages |
| **Image Management**      | Provides APIs for deploying built images to target nodes, validating deployments via automated tests, and cleaning up failed or obsolete images |

---

## 7. Functional Requirements — Feature 1: Workflow Optimization

### FR-WF-01: Job Creation

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-WF-01                                                              |
| Priority           | Critical                                                              |
| BSpec Reference    | Workflow Optimization — API Workflow                                   |

**What the system must do:**

1. The system SHALL accept a request to create a new build Job.
2. The system SHALL assign a unique Job identifier (UUID format) to each new Job.
3. The system SHALL initialize the Job in a `CREATED` state.
4. The system SHALL create initial Stage entities in `PENDING` state for all stages in the build pipeline.
5. The system SHALL enforce idempotency — if a request with the same `Idempotency-Key` and `client_id` is received, the system SHALL return the original response without creating a duplicate Job.
6. The system SHALL record an audit event for every Job creation.
7. The system SHALL return the Job ID, initial state, and list of stages in the response.

**What inputs are accepted:**

| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `client_id`        | string   | Yes      | Identifier of the requesting client               |
| `client_name`      | string   | Yes      | Human-readable name of the requesting client       |

**What headers are required:**

| Header               | Required | Description                                           |
|----------------------|----------|-------------------------------------------------------|
| `Authorization`      | Yes      | Bearer JWT token                                       |
| `X-Client-Id`        | Yes      | Client identifier                                      |
| `X-Correlation-Id`   | Yes      | Unique request correlation ID                          |
| `Idempotency-Key`    | Yes      | Unique key for idempotent request deduplication        |

**What outputs are generated:**

| Field              | Type     | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `job_id`           | string   | Unique Job identifier (UUID)                           |
| `state`            | string   | Current Job state (`CREATED`)                          |
| `stages`           | array    | List of stage objects with name and state              |
| `created_at`       | datetime | Timestamp of Job creation                              |
| `client_id`        | string   | Owning client identifier                               |

---

### FR-WF-02: Job Query

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-WF-02                                                              |
| Priority           | High                                                                  |

**What the system must do:**

1. The system SHALL accept a request to retrieve the current status of a Job by its Job ID.
2. The system SHALL verify that the requesting client owns the Job.
3. The system SHALL return the Job state and the state of all associated Stages.
4. The system SHALL return `404 Not Found` if the Job does not exist.
5. The system SHALL return `403 Forbidden` if the requesting client does not own the Job.

**What outputs are generated:**

| Field              | Type     | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `job_id`           | string   | Job identifier                                         |
| `state`            | string   | Current Job state                                      |
| `stages`           | array    | All stages with their current states and metadata      |
| `created_at`       | datetime | Job creation timestamp                                 |
| `updated_at`       | datetime | Last state change timestamp                            |

---

### FR-WF-03: Job Deletion (Hard Delete with CleanUp)

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-WF-03                                                              |
| Priority           | High                                                                  |

**What the system must do:**

1. The system SHALL accept a delete request for a Job by its Job ID via `DELETE /api/v1/jobs/{job_id}`.
2. The system SHALL internally resolve the associated `image_group_id` using the 1:1 Job ↔ ImageGroup mapping.
3. The system SHALL query the `images` table to retrieve all `image_name` values (S3 paths) for the Image Group.
4. For each image path, the system SHALL execute `s3cmd del <image_path>` within the BuildStream container to delete the image from S3 storage.
5. The system SHALL remove all NFS artifact files for the Job (config files, catalog JSON, generated inputs, inventories).
6. The system SHALL transition the Image Group to `CLEANED` state and mark the Job as `CLEANED`.
7. The system SHALL return `204 No Content` on success.
8. The system SHALL return `404 Not Found` if the Job does not exist.
9. The system SHALL return `409 Conflict` if the Image Group is in an active state (`DEPLOYING`, `RESTARTING`, `VALIDATING`).
10. The system SHALL return `412 Precondition Failed` if the Job has already been cleaned.
11. The system SHALL record an audit event for cleanup operations (success and failure).

> **Note:** This is a hard delete operation that removes all artifacts and images, not a soft delete (tombstone). The Job and Image Group records are preserved in the database with `CLEANED` status for audit trail.

---

### FR-WF-04: File Upload

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-WF-04                                                              |
| Priority           | Critical                                                              |
| BSpec Reference    | Input folder stored in GitLab                                         |
| Gap Reference      | A-05                                                                  |

**What the system must do:**

1. The system SHALL accept file uploads as part of the build pipeline input.
2. The system SHALL validate uploaded file names and formats against an allowlist.
3. The system SHALL reject uploads that exceed the maximum file size (configurable, default 5 MB).
4. The system SHALL reject empty files.
5. The system SHALL reject file paths containing path traversal sequences (e.g., `../`).
6. Only uploaded files SHALL be overwritten — existing files not included in the upload SHALL be preserved (partial upload semantics).
7. The system SHALL store uploaded files in the designated input directory.

**What validations apply:**

| Validation                     | Behavior                                              |
|-------------------------------|-------------------------------------------------------|
| File size exceeds maximum      | Reject with `413 Payload Too Large`                   |
| Empty file                     | Reject with `400 Bad Request`                         |
| Path traversal detected        | Reject with `400 Bad Request`                         |
| Unsupported file format        | Reject with `422 Unprocessable Entity`                |

---

### FR-WF-05: Create Local Repository Stage

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-WF-05                                                              |
| Priority           | Critical                                                              |
| BSpec Reference    | Build Stage — getInputfiles / local repo                              |
| Gap Reference      | A-06                                                                  |

**What the system must do:**

1. The system SHALL accept a request to trigger the create-local-repository stage for a given Job.
2. The system SHALL validate that the Job exists and is in a state that allows stage execution.
3. The system SHALL validate that required input files exist in the input directory.
4. The system SHALL transition the Job state from `CREATED` to `IN_PROGRESS`.
5. The system SHALL transition the Stage state from `PENDING` to `IN_PROGRESS`.
6. The system SHALL submit a playbook execution request to the Omnia Core asynchronously.
7. The system SHALL return `202 Accepted` immediately (non-blocking).
8. The system SHALL update the Stage state to `COMPLETED` or `FAILED` upon receiving the playbook result.
9. The system SHALL record audit events for all state transitions.

**What outputs are generated (immediate response):**

| Field              | Type     | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `job_id`           | string   | Job identifier                                         |
| `stage`            | string   | Stage name (`create-local-repository`)                 |
| `status`           | string   | `accepted`                                             |
| `submitted_at`     | datetime | Submission timestamp                                   |
| `correlation_id`   | string   | Request correlation ID                                 |

---

### FR-WF-06: Parse Catalog Stage

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-WF-06                                                              |
| Priority           | Critical                                                              |
| BSpec Reference    | Build Stage — Parse                                                   |

**What the system must do:**

1. The system SHALL accept a catalog JSON file upload for a given Job.
2. The system SHALL validate the file has a `.json` extension.
3. The system SHALL validate the file contains valid JSON and is a dictionary (object) at the root.
4. The system SHALL validate the Job exists and is in a state that allows this stage.
5. The system SHALL process the catalog to generate adapter policy output files.
6. The system SHALL store generated artifacts in the artifact store.
7. The system SHALL transition the Stage through `PENDING` → `IN_PROGRESS` → `COMPLETED` (or `FAILED`).
8. The system SHALL record audit events for all state transitions.

**What inputs are accepted:**

| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `file`             | binary   | Yes      | Catalog JSON file (multipart upload)              |

**What validations apply:**

| Validation                     | Behavior                                              |
|-------------------------------|-------------------------------------------------------|
| Non-JSON file extension        | Reject with `400 Bad Request`                         |
| Invalid JSON content           | Reject with `400 Bad Request`                         |
| JSON root is not a dictionary  | Reject with `400 Bad Request`                         |
| Job not found                  | Reject with `404 Not Found`                           |
| Invalid Job state for stage    | Reject with `409 Conflict`                            |

---

### FR-WF-07: Build Image Stage

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-WF-07                                                              |
| Priority           | Critical                                                              |
| BSpec Reference    | Build Stage — buildImage                                              |
| Gap Reference      | A-06                                                                  |

**What the system must do:**

1. The system SHALL accept a request to trigger the image build stage for a given Job.
2. The system SHALL enforce sequential stage ordering — the build-image stage SHALL only execute after all prerequisite stages have completed successfully.
3. The system SHALL reject build requests if any prerequisite stage is in a `FAILED` or `PENDING` state.
4. The system SHALL transition the Stage through the standard state machine (`PENDING` → `IN_PROGRESS` → `COMPLETED` / `FAILED`).
5. The system SHALL produce one or more OS images as output artifacts.
6. The system SHALL tag successful builds with a build identifier for downstream reference.
7. The system SHALL record audit events for all state transitions.
8. A build stage SHALL NOT be re-run once completed (immutability).

**Sequential enforcement:**

```
Stage Order (mandatory sequence):
  1. create-local-repository  →  MUST be COMPLETED
  2. parse-catalog            →  MUST be COMPLETED
  3. build-image              →  CAN now execute
```

---

## 8. Functional Requirements — Feature 2: Image Management

### FR-IM-01: Image Deployment

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-IM-01                                                              |
| Priority           | Critical                                                              |
| BSpec Reference    | Deploy API                                                            |
| Gap Reference      | A-07                                                                  |

**What the system must do:**

1. The system SHALL accept a deployment request specifying a Job ID and Image Group identifier.
2. The system SHALL validate that the referenced Image Group exists.
3. The system SHALL validate that the Image Group is in a deployable state (`BUILT`).
4. The system SHALL validate that the Image Group belongs to the specified Job.
5. The system SHALL transition the Image Group state from `BUILT` to `DEPLOYING`, then to `DEPLOYED` upon completion.
6. The system SHALL return an error if the Image Group is not in a deployable state.
7. The system SHALL record audit events for deployment state transitions.

**What inputs are accepted:**

| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `job_id`           | string   | Yes      | Job identifier (path parameter)                   |
| `image_group_id`   | string   | Yes      | Image Group identifier to deploy                  |

**What validations apply:**

| Validation                       | Behavior                                            |
|---------------------------------|-----------------------------------------------------|
| Image Group does not exist       | `404 Not Found`                                     |
| Image Group not in BUILT state   | `409 Conflict` — not deployable                     |
| Image Group belongs to wrong Job | `400 Bad Request`                                   |
| Job does not exist               | `404 Not Found`                                     |

**Re-deployment semantics:**

- Re-deploying an Image Group that is already in `DEPLOYED` state SHALL be rejected with `409 Conflict`.
- A new deployment requires a new build.

---

### FR-IM-02: Node PXE Boot / Restart

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-IM-02                                                              |
| Priority           | High                                                                  |
| BSpec Reference    | Restart API — restart nodes from PXE mapping file                     |
| Gap Reference      | A-08                                                                  |

**What the system must do:**

1. The system SHALL accept a restart request to PXE boot target nodes after image deployment.
2. The system SHALL consume the PXE mapping file to determine which nodes to restart.
3. The system SHALL support a `disable_pxe_boot` option to skip PXE boot for specific scenarios.
4. The system SHALL implement node diff logic — only newly added nodes (not previously booted with the current image) SHALL be PXE-booted.
5. The system SHALL transition the Image Group state from `DEPLOYED` to `RESTARTING`, then to `RESTARTED` upon completion.
6. The system SHALL return status per-node (which nodes were restarted, which were skipped).
7. The system SHALL record audit events for restart operations.

**What inputs are accepted:**

| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `job_id`           | string   | Yes      | Job identifier (path parameter)                   |
| `disable_pxe_boot` | boolean | No       | If `true`, skip PXE boot (default: `false`)       |

---

### FR-IM-03: Image Validation (TestValidate)

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-IM-03                                                              |
| Priority           | Critical                                                              |
| BSpec Reference    | TestValidate — minimum basic tests                                    |
| Gap Reference      | A-09, D-02                                                            |

**What the system must do:**

1. The system SHALL accept a validation request to run automated tests against deployed images.
2. The system SHALL support an optional `test_suite` parameter to select which test suite to execute.
3. The system SHALL support an optional `timeout` parameter (with a sensible default).
4. The system SHALL transition the Image Group state from `RESTARTED` to `VALIDATING`.
5. The system SHALL execute minimum basic tests associated with each functional role on the deployed nodes.
6. The system SHALL tag images as `PASSED` or `FAILED` based on aggregate test results.
7. The system SHALL return a structured test results response.
8. The system SHALL record audit events for validation state transitions.

**What inputs are accepted:**

| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `job_id`           | string   | Yes      | Job identifier (path parameter)                   |
| `test_suite`       | string   | No       | Specific test suite to run (default: all basic)    |
| `timeout`          | integer  | No       | Timeout in seconds (default: system-defined)       |

**What outputs are generated (test results structure):**

| Field                    | Type     | Description                                           |
|--------------------------|----------|-------------------------------------------------------|
| `job_id`                 | string   | Job identifier                                         |
| `image_group_id`         | string   | Image Group tested                                     |
| `overall_status`         | string   | `PASSED` or `FAILED`                                   |
| `summary.total_tests`    | integer  | Total number of tests executed                         |
| `summary.passed`         | integer  | Number of tests passed                                 |
| `summary.failed`         | integer  | Number of tests failed                                 |
| `results[]`              | array    | Per-test results                                       |
| `results[].test_name`    | string   | Name of the test                                       |
| `results[].status`       | string   | `passed` or `failed`                                   |
| `results[].node`         | string   | Node identifier where test ran                         |
| `results[].failure_details` | string | Failure description (null if passed)                  |
| `results[].duration_ms`  | integer  | Test execution duration in milliseconds                |

---

### FR-IM-04: Image CleanUp (Manual)

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-IM-04                                                              |
| Priority           | High                                                                  |
| BSpec Reference    | CleanUp function                                                      |
| Gap Reference      | B-01, C-02, D-03                                                      |

**What the system must do:**

1. The system SHALL accept a delete request via `DELETE /api/v1/jobs/{job_id}`.
2. The system SHALL internally resolve the `image_group_id` using the 1:1 Job ↔ ImageGroup mapping (the caller provides only the `job_id`).
3. The system SHALL query the `images` table to retrieve all `image_name` values (S3 paths) for the Image Group.
4. For each image path, the system SHALL execute `s3cmd del <image_path>` to delete the image from S3 storage.
5. The system SHALL remove all NFS artifact files for the Job (config files, catalog JSON, generated inputs, inventories).
6. The system SHALL transition the Image Group to `CLEANED` state and mark the Job as `CLEANED`.
7. If cleanup fails, the system SHALL:
   - Return a clear error response with details of what failed.
   - Leave the Image Group in its previous state (no partial state corruption).
   - Allow the user to retry the cleanup operation.
8. The system SHALL record audit events for cleanup operations (success and failure).

**What inputs are accepted:**

| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `job_id`           | string   | Yes      | Job identifier (path parameter)                   |

**Cleanup failure behavior:**

| Scenario                        | System Behavior                                       |
|---------------------------------|-------------------------------------------------------|
| Cleanup succeeds                | Image Group and artifacts removed, `204 No Content`   |
| Cleanup partially fails (S3)    | Image Group remains in previous state, error returned  |
| Job not found                   | `404 Not Found`                                        |
| Image Group in active state     | `409 Conflict` — cleanup not allowed during active ops |
| Job already cleaned             | `412 Precondition Failed`                              |

---

### FR-IM-05: Automated CleanUp (Cron-Based)

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-IM-05                                                              |
| Priority           | High                                                                  |
| BSpec Reference    | Automated Cleanup                                                     |
| Gap Reference      | B-01                                                                  |

**What the system must do:**

1. The system SHALL run a cron job inside the BuildStream container every **24 hours** (configurable via `CLEANUP_INTERVAL_HOURS`).
2. The cron job SHALL query the `image_groups` table for all records with status `FAILED`.
3. For each `FAILED` Image Group, the cron job SHALL:
   a. Query the `images` table to retrieve all `image_name` values (S3 paths) for the Image Group.
   b. For each image path, execute `s3cmd del <image_path>` to remove the image from S3.
   c. Remove NFS artifact files for the associated Job.
   d. Transition the Image Group to `CLEANED` and the Job to `CLEANED`.
   e. Record an audit event with reason `auto_cleanup_validation_failed`.
4. If cleanup fails for a specific Image Group, the system SHALL log the error and continue with the next one. Failed cleanups SHALL be retried on the next cron cycle.

---

### FR-IM-06: Image Retention Limit

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-IM-06                                                              |
| Priority           | High                                                                  |
| BSpec Reference    | Retention Limit                                                       |

**What the system must do:**

1. The system SHALL enforce a maximum retention limit of **50** non-CLEANED Image Groups (configurable via `IMAGE_RETENTION_LIMIT`).
2. Before the `build-image` stage begins execution, the system SHALL check the current count of non-CLEANED Image Groups.
3. If the count equals or exceeds the limit, the system SHALL **abort** the build with error code `RETENTION_LIMIT_EXCEEDED`.
4. The error message SHALL instruct the user to clean up existing jobs via the CleanUp Pipeline.

---

---

## 9. Authentication and Authorization

### FR-AUTH-01: OAuth 2.0 Client Registration

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-AUTH-01                                                            |
| Priority           | Critical                                                              |
| Gap Reference      | A-10                                                                  |

**What the system must do:**

1. The system SHALL provide a client registration endpoint secured by Basic Authentication.
2. Basic Auth credentials SHALL be stored in an encrypted vault (Ansible Vault).
3. The system SHALL generate a unique `client_id` (UUID) and `client_secret` upon registration.
4. The `client_secret` SHALL be shown only once at registration time.
5. The system SHALL hash the `client_secret` using bcrypt before storage.
6. The system SHALL enforce a maximum client limit (configurable, default: 1 client).
7. The system SHALL store client records in an encrypted vault file.

**What inputs are accepted:**

| Field              | Type     | Required | Description                                      |
|--------------------|----------|----------|--------------------------------------------------|
| `client_name`      | string   | Yes      | Human-readable client name                        |
| `description`      | string   | No       | Optional description                              |
| `allowed_scopes`   | array    | Yes      | Scopes the client is authorized for               |

**What outputs are generated:**

| Field              | Type     | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `client_id`        | string   | Unique client identifier (UUID)                        |
| `client_secret`    | string   | Client secret (shown only once — save immediately)     |
| `client_name`      | string   | Client name                                            |
| `allowed_scopes`   | array    | Authorized scopes                                      |
| `created_at`       | datetime | Registration timestamp                                 |
| `expires_at`       | datetime | Expiration (null if no expiry)                         |

### FR-AUTH-02: Token Generation

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-AUTH-02                                                            |
| Priority           | Critical                                                              |

**What the system must do:**

1. The system SHALL accept a token request using `client_credentials` grant type.
2. The system SHALL verify the `client_id` and `client_secret` against stored records.
3. The system SHALL validate that requested scopes are a subset of the client's allowed scopes.
4. The system SHALL generate a signed JWT token containing: `client_id`, `client_name`, `scopes`, `token_id`, `exp`.
5. The system SHALL return the access token, token type, expiration time, and granted scopes.
6. Tokens SHALL expire after a configurable duration (default: 3600 seconds).

**What outputs are generated:**

| Field              | Type     | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `access_token`     | string   | Signed JWT token                                       |
| `token_type`       | string   | `bearer`                                               |
| `expires_in`       | integer  | Token lifetime in seconds                              |
| `scope`            | string   | Granted scopes                                         |

### FR-AUTH-03: Token Verification

| Attribute          | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| Requirement ID     | FR-AUTH-03                                                            |
| Priority           | Critical                                                              |

**What the system must do:**

1. Every protected API endpoint SHALL require a valid JWT bearer token in the `Authorization` header.
2. The system SHALL verify the token signature, expiration, and claims.
3. The system SHALL enforce scope requirements per endpoint.
4. The system SHALL return `401 Unauthorized` for missing, expired, or invalid tokens.
5. The system SHALL return `403 Forbidden` if the token does not contain the required scope.

### 9.1 Authorization Scopes

| Scope              | Description                                  | Persona Access                    |
|--------------------|----------------------------------------------|-----------------------------------|
| `jobs:read`        | Query job status                              | All personas                      |
| `jobs:write`       | Create and delete jobs                        | Platform Operator, CI/CD Agent    |
| `stages:execute`   | Trigger build stages                          | Platform Operator, CI/CD Agent    |
| `catalog:read`     | Parse catalog files                           | Platform Operator, CI/CD Agent    |
| `catalog:write`    | Upload catalog files                          | Platform Operator                 |
| `deploy:execute`   | Deploy images to nodes                        | Platform Operator                 |
| `admin:register`   | Register new OAuth clients                    | System Administrator              |

---

## 10. API Functional Contract Summary

The following table summarizes all API endpoints, their authentication requirements, and functional purpose.

| Method   | Endpoint                                              | Auth           | Scope Required    | Description                    |
|----------|-------------------------------------------------------|----------------|-------------------|--------------------------------|
| `GET`    | `/`                                                   | None           | —                 | Welcome / service info         |
| `GET`    | `/health`                                             | None           | —                 | Health check                   |
| `POST`   | `/api/v1/auth/register`                               | Basic Auth     | —                 | Register OAuth client          |
| `POST`   | `/api/v1/auth/token`                                  | None (creds in body) | —           | Generate JWT token             |
| `POST`   | `/api/v1/jobs`                                        | JWT            | `jobs:write`      | Create new Job                 |
| `GET`    | `/api/v1/jobs/{job_id}`                               | JWT            | `jobs:read`       | Get Job status                 |
| `DELETE` | `/api/v1/jobs/{job_id}`                               | JWT            | `jobs:write`      | Delete Job (hard delete with cleanup) |
| `POST`   | `/api/v1/jobs/{job_id}/stages/create-local-repository`| JWT            | `stages:execute`  | Trigger local repo stage       |
| `POST`   | `/api/v1/jobs/{job_id}/stages/parse-catalog`          | JWT            | `catalog:read`    | Parse catalog file             |
| `POST`   | `/api/v1/jobs/{job_id}/stages/build-image`            | JWT            | `stages:execute`  | Trigger image build            |
| `POST`   | `/api/v1/jobs/{job_id}/deploy`                        | JWT            | `deploy:execute`  | Deploy images to nodes         |
| `POST`   | `/api/v1/jobs/{job_id}/restart`                       | JWT            | `deploy:execute`  | PXE boot / restart nodes       |
| `POST`   | `/api/v1/jobs/{job_id}/validate`                      | JWT            | `stages:execute`  | Run validation tests           |

---

## 11. Job Lifecycle and State Machine

### 11.1 Job States

| State          | Description                                                        | Terminal? |
|----------------|--------------------------------------------------------------------|-----------|
| `CREATED`      | Job has been created, no stages have been executed                   | No        |
| `IN_PROGRESS`  | At least one stage has been triggered                                | No        |
| `COMPLETED`    | All stages have completed successfully                               | Yes       |
| `FAILED`       | One or more stages have failed                                       | Yes       |
| `CANCELLED`    | Job has been cancelled by the user                                   | Yes       |

### 11.2 Job State Transition Diagram

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
              (terminal states — no further transitions)
```

### 11.3 Valid Transitions

| Current State  | Allowed Transitions                 | Trigger                             |
|----------------|-------------------------------------|-------------------------------------|
| `CREATED`      | `IN_PROGRESS`, `CANCELLED`          | First stage triggered, or cancel    |
| `IN_PROGRESS`  | `COMPLETED`, `FAILED`, `CANCELLED`  | All stages done, stage failure, or cancel |
| `COMPLETED`    | *(none — terminal)*                 | —                                   |
| `FAILED`       | *(none — terminal)*                 | —                                   |
| `CANCELLED`    | *(none — terminal)*                 | —                                   |

**Business rule:** Any attempt to transition from a terminal state SHALL be rejected with `409 Conflict`.

---

## 12. Image Group State Machine

### 12.1 Image Group States

| State          | Description                                                        | Terminal? |
|----------------|--------------------------------------------------------------------|-----------|
| `BUILT`        | Image has been successfully built                                    | No        |
| `DEPLOYING`    | Image is being deployed to target nodes                              | No        |
| `DEPLOYED`     | Image has been deployed to nodes                                     | No        |
| `RESTARTING`   | Target nodes are being PXE-booted / restarted                       | No        |
| `RESTARTED`    | Nodes have been restarted with the new image                         | No        |
| `VALIDATING`   | Automated validation tests are running                               | No        |
| `PASSED`       | All validation tests passed                                          | Yes       |
| `FAILED`       | One or more validation tests failed                                  | Yes*      |
| `CLEANED`      | Image and artifacts have been cleaned up                             | Yes       |

*`FAILED` images are eligible for cleanup.

### 12.2 Image Group State Transition Diagram

```
┌───────┐
│ BUILT │
└───┬───┘
    │ deploy()
┌───▼──────┐
│DEPLOYING │
└───┬──────┘
    │ deployment complete
┌───▼──────┐
│DEPLOYED  │
└───┬──────┘
    │ restart()
┌───▼──────────┐
│ RESTARTING   │
└───┬──────────┘
    │ restart complete
┌───▼──────────┐
│ RESTARTED    │
└───┬──────────┘
    │ validate()
┌───▼──────────┐
│ VALIDATING   │
└───┬──────┬───┘
    │      │
  pass   fail
    │      │
┌───▼──┐ ┌▼──────┐
│PASSED│ │FAILED │──── cleanup() ──►┌────────┐
└──────┘ └───────┘                  │CLEANED │
                                    └────────┘
```

### 12.3 Valid Transitions

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

---

## 13. Build Stage State Machine

### 13.1 Stage States

| State          | Description                                     | Terminal? |
|----------------|-------------------------------------------------|-----------|
| `PENDING`      | Stage has not yet started                        | No        |
| `IN_PROGRESS`  | Stage is currently executing                     | No        |
| `COMPLETED`    | Stage finished successfully                      | Yes       |
| `FAILED`       | Stage finished with an error                     | Yes       |
| `SKIPPED`      | Stage was skipped (not applicable)               | Yes       |

### 13.2 Valid Transitions

| Current State  | Allowed Transitions        | Trigger                       |
|----------------|----------------------------|-------------------------------|
| `PENDING`      | `IN_PROGRESS`, `SKIPPED`   | Stage triggered, or skipped   |
| `IN_PROGRESS`  | `COMPLETED`, `FAILED`      | Execution result              |
| `COMPLETED`    | *(terminal)*               | —                             |
| `FAILED`       | *(terminal)*               | —                             |
| `SKIPPED`      | *(terminal)*               | —                             |

---

## 14. User Workflows

### 14.1 End-to-End Build and Deploy Workflow

**Preconditions:**
- OIM host is operational with BuildStream container running
- OAuth client is registered and JWT token is available
- Input files (Omnia input folder) are available

**Step-by-step flow:**

| Step | User Action                                     | System Response                                    | State Change                     |
|------|-------------------------------------------------|----------------------------------------------------|----------------------------------|
| 1    | `POST /api/v1/jobs`                             | Returns `201 Created` with `job_id` and stages     | Job: → `CREATED`                 |
| 2    | Upload input files                               | Returns `200 OK`                                   | —                                |
| 3    | `POST /jobs/{id}/stages/create-local-repository` | Returns `202 Accepted`                             | Job: `CREATED` → `IN_PROGRESS`; Stage: `PENDING` → `IN_PROGRESS` |
| 4    | Poll `GET /jobs/{id}` for stage completion       | Returns current state                              | Stage: `IN_PROGRESS` → `COMPLETED` (async) |
| 5    | `POST /jobs/{id}/stages/parse-catalog`           | Returns `200 OK` with parsed results               | Stage: `PENDING` → `COMPLETED`   |
| 6    | `POST /jobs/{id}/stages/build-image`             | Returns `202 Accepted`                             | Stage: `PENDING` → `IN_PROGRESS` |
| 7    | Poll `GET /jobs/{id}` for build completion       | Returns current state                              | Stage: `IN_PROGRESS` → `COMPLETED`; Image Group: → `BUILT` |
| 8    | `POST /jobs/{id}/deploy`                         | Returns `202 Accepted`                             | Image Group: `BUILT` → `DEPLOYING` → `DEPLOYED` |
| 9    | `POST /jobs/{id}/restart`                        | Returns `202 Accepted`                             | Image Group: `DEPLOYED` → `RESTARTING` → `RESTARTED` |
| 10   | `POST /jobs/{id}/validate`                       | Returns test results                               | Image Group: `RESTARTED` → `VALIDATING` → `PASSED`/`FAILED` |
| 11   | (If failed) `DELETE /jobs/{id}`                  | Returns `204 No Content`                           | Image Group: `FAILED` → `CLEANED` |

**Postconditions:**
- Job is in `COMPLETED` state (if all stages passed)
- Image Group is in `PASSED` state (if validation succeeded)
- All audit events recorded

### 14.2 GitLab CI/CD Pipeline Workflow

**Preconditions:**
- GitLab CI/CD pipeline configured with BuildStream API credentials
- Pipeline variables include `BUILDSTREAM_URL`, `CLIENT_ID`, `CLIENT_SECRET`

**Pipeline Architecture:**
The CI/CD workflow is decomposed into three independent pipelines:
1. **Build Pipeline**: Triggered by catalog/config changes. Initializes by implicitly calling the Upload API to sync catalog and configs, then executes build stages.
2. **Deploy Pipeline**: Triggered by PXE mapping changes. Initializes by implicitly calling the Upload API to sync configs, presents an Image Group selection UI (via dynamic child pipelines showing functional layers), and executes deploy stages.
3. **CleanUp Pipeline**: Triggered manually. Presents an Image Group selection UI and calls the CleanUp API to remove artifacts and images.

**Step-by-step flow (Build):**

| Step | CI/CD Stage               | API Call                                           | Notes                          |
|------|---------------------------|----------------------------------------------------|--------------------------------|
| 1    | `auth`                    | `POST /api/v1/auth/token`                          | Obtain JWT token               |
| 2    | `create-job`              | `POST /api/v1/jobs`                                | Create build job               |
| 3    | `upload-inputs`           | Upload input files                                  | From GitLab repo artifacts     |
| 4    | `create-local-repo`       | `POST /jobs/{id}/stages/create-local-repository`   | Trigger + poll until complete  |
| 5    | `parse-catalog`           | `POST /jobs/{id}/stages/parse-catalog`             | Upload catalog JSON            |
| 6    | `build-image`             | `POST /jobs/{id}/stages/build-image`               | Trigger + poll until complete  |
| 7    | `deploy`                  | `POST /jobs/{id}/deploy`                           | Deploy to target nodes         |
| 8    | `restart-nodes`           | `POST /jobs/{id}/restart`                          | PXE boot nodes                 |
| 9    | `validate`                | `POST /jobs/{id}/validate`                         | Run tests, check results       |
| 10   | `cleanup` (on failure)    | `DELETE /jobs/{id}`                                | Cleanup failed images          |

### 14.3 Direct API Workflow (Bypassing GitLab)

Same as 14.1. The user interacts directly with the BuildStream API using curl, Postman, or a custom client, following the same sequential stage execution pattern.

### 14.4 Cleanup Workflow

**Preconditions:**
- Image Group exists in `FAILED` state

**Flow:**

| Step | User Action                                     | System Response                                   |
|------|-------------------------------------------------|---------------------------------------------------|
| 1    | `GET /jobs/{id}` to identify failed Image Group  | Returns job with Image Group in `FAILED` state    |
| 2    | `DELETE /jobs/{id}`                              | Returns `204 No Content`                          |
| 3    | (If failed) Retry step 2                         | System allows retry                               |

### 14.5 Retry / Resume Workflow

**Preconditions:**
- A Job exists with one or more stages in `FAILED` state

**What the system supports:**
- The user MAY create a new Job to restart the pipeline from scratch.
- Individual failed stages are **not** re-runnable in this release (immutability constraint).
- The system provides clear error information to help diagnose the failure before retrying.

---

## 15. Data Flow Diagrams

### 15.1 Build Pipeline Data Flow

```
Input Files          Catalog JSON         Build Artifacts
(from user/GitLab)   (from user)          (generated)
     │                    │                     ▲
     ▼                    ▼                     │
┌─────────┐    ┌──────────────┐    ┌────────────────┐
│ Upload   │    │ Parse        │    │  Build Image   │
│ Stage    │───►│ Catalog      │───►│  Stage         │
│          │    │ Stage        │    │                │
└─────────┘    └──────────────┘    └────────┬───────┘
                                            │
                                            ▼
                                   ┌────────────────┐
                                   │ Image Group    │
                                   │ (BUILT)        │
                                   └────────┬───────┘
                                            │
                                            ▼
                                   ┌────────────────┐
                                   │ Deploy to      │
                                   │ Nodes          │
                                   └────────┬───────┘
                                            │
                                            ▼
                                   ┌────────────────┐
                                   │ PXE Boot       │
                                   │ Nodes          │
                                   └────────┬───────┘
                                            │
                                            ▼
                                   ┌────────────────┐
                                   │ Validate       │
                                   │ Images         │
                                   └────────┬───────┘
                                            │
                                       ┌────┴────┐
                                       ▼         ▼
                                   ┌──────┐  ┌──────┐
                                   │PASSED│  │FAILED│
                                   └──────┘  └──┬───┘
                                                │
                                                ▼
                                          ┌──────────┐
                                          │ Cleanup  │
                                          └──────────┘
```

### 15.2 Async Stage Execution Data Flow (NFS Queue)

```
┌──────────────────┐          ┌──────────────────────┐
│  BuildStream API │          │    Omnia Core         │
│                  │          │                       │
│  Stage triggered │          │                       │
│       │          │          │                       │
│       ▼          │          │                       │
│  Write request   │  NFS     │                       │
│  JSON to         │─────────►│  Read request JSON    │
│  requests/ dir   │  share   │       │               │
│                  │          │       ▼               │
│                  │          │  Execute Ansible      │
│                  │          │  playbook             │
│                  │          │       │               │
│  Poll results/   │  NFS     │       ▼               │
│  directory       │◄─────────│  Write result JSON    │
│       │          │  share   │  to results/ dir      │
│       ▼          │          │                       │
│  Update stage    │          │                       │
│  state           │          │                       │
└──────────────────┘          └──────────────────────┘
```

---

## 16. Input and Output Specifications

### 16.1 API Request/Response Format

All API requests and responses use JSON format (`Content-Type: application/json`) unless otherwise specified (e.g., multipart file uploads).

### 16.2 Standard Error Response Format

All error responses SHALL follow a consistent structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error description",
    "details": {
      "field": "Additional context if applicable"
    },
    "correlation_id": "request-correlation-id",
    "timestamp": "2026-04-07T10:00:00Z"
  }
}
```

### 16.3 Standard HTTP Status Codes

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

## 17. Business Rules and Validations

### 17.1 Job Business Rules

| Rule ID | Rule                                                                              |
|---------|-----------------------------------------------------------------------------------|
| BR-J01  | Each Job is owned by exactly one client, identified by `client_id`                 |
| BR-J02  | Only the owning client may query, modify, or delete a Job                          |
| BR-J03  | A Job in a terminal state (`COMPLETED`, `FAILED`, `CANCELLED`) cannot be modified  |
| BR-J04  | Idempotency: duplicate requests (same `Idempotency-Key` + `client_id`) return the original response |
| BR-J05  | Optimistic locking: concurrent modifications are detected and rejected via version field |
| BR-J06  | Job cleanup removes S3 images and NFS artifacts; DB records preserved with `CLEANED` status for audit |

### 17.2 Stage Business Rules

| Rule ID | Rule                                                                              |
|---------|-----------------------------------------------------------------------------------|
| BR-S01  | Stages within a Job must be executed in the defined sequential order               |
| BR-S02  | A stage cannot start if any prerequisite stage is not in `COMPLETED` state         |
| BR-S03  | A completed stage cannot be re-executed (immutability)                              |
| BR-S04  | A failed stage causes the Job to transition to `FAILED`                            |
| BR-S05  | Each stage execution generates at least one audit event                            |

### 17.3 Image Group Business Rules

| Rule ID | Rule                                                                              |
|---------|-----------------------------------------------------------------------------------|
| BR-IG01 | An Image Group can only be deployed if it is in `BUILT` state                      |
| BR-IG02 | An Image Group can only be validated if it is in `RESTARTED` state                 |
| BR-IG03 | `BUILT`, `PASSED`, and `FAILED` Image Groups are eligible for cleanup              |
| BR-IG04 | Re-deployment of an already deployed Image Group is not allowed                     |
| BR-IG05 | State transitions must follow the defined state machine — invalid transitions are rejected |

### 17.4 Authentication Business Rules

| Rule ID | Rule                                                                              |
|---------|-----------------------------------------------------------------------------------|
| BR-A01  | Maximum one OAuth client can be registered at a time                               |
| BR-A02  | The `client_secret` is displayed only at registration time and cannot be retrieved later |
| BR-A03  | JWT tokens expire after the configured duration (default 3600 seconds)             |
| BR-A04  | Expired tokens are rejected — the client must request a new token                  |
| BR-A05  | Requested scopes must be a subset of the client's allowed scopes                   |

---

## 18. Customer-Facing Constraints

| Constraint ID | Constraint                                                                   |
|---------------|-----------------------------------------------------------------------------|
| CON-01        | **Architecture**: Only x86_64 architecture is supported                      |
| CON-02        | **Concurrency**: Only one pipeline (build + deploy) may execute at a time (sequential execution) |
| CON-03        | **Upload size**: Maximum file upload size is 5 MB (configurable)             |
| CON-04        | **Archive size**: Maximum uncompressed archive size is 50 MB                  |
| CON-05        | **Archive entries**: Maximum 500 entries in an uploaded archive               |
| CON-06        | **Cluster**: Single-cluster deployment only                                   |
| CON-07        | **Deployment type**: Physical nodes only (no VM + physical hybrid)            |
| CON-08        | **OAuth clients**: Maximum 1 registered OAuth client                          |
| CON-09        | **Token lifetime**: JWT tokens expire after 3600 seconds (default)            |
| CON-10        | **Cleanup**: User-initiated via CleanUp API + automated cron for validation-failed images (24h) |
| CON-11        | **Retention limit**: Maximum 50 non-CLEANED Image Groups; build aborted if limit reached |

---

## 19. Error Handling Specification

### 19.1 Error Scenarios by Workflow

#### Authentication Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Missing Authorization header              | `401`     | `AUTH_MISSING`           | Include Bearer token in request     |
| Expired JWT token                         | `401`     | `AUTH_TOKEN_EXPIRED`     | Request a new token                 |
| Invalid JWT signature                     | `401`     | `AUTH_TOKEN_INVALID`     | Verify token source and signing key |
| Insufficient scope                        | `403`     | `AUTH_SCOPE_INSUFFICIENT`| Request token with required scope   |
| Invalid client credentials (registration) | `401`     | `AUTH_CREDENTIALS_INVALID`| Verify Basic Auth credentials      |
| Max clients exceeded                      | `409`     | `AUTH_MAX_CLIENTS`       | Delete existing client first        |

#### Job Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Job not found                             | `404`     | `JOB_NOT_FOUND`          | Verify job_id                       |
| Job not owned by requesting client        | `403`     | `JOB_ACCESS_DENIED`      | Use correct client credentials      |
| Job in terminal state                     | `409`     | `JOB_STATE_TERMINAL`     | Create a new job                    |
| Duplicate idempotency key (different client)| `409`   | `IDEMPOTENCY_CONFLICT`   | Use a unique idempotency key       |

#### Stage Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Prerequisite stage not completed          | `409`     | `STAGE_PREREQUISITE_PENDING` | Complete prerequisite stages first |
| Stage already completed (immutable)       | `409`     | `STAGE_ALREADY_COMPLETED`| Stage cannot be re-run              |
| Required input files missing              | `400`     | `STAGE_INPUT_MISSING`    | Upload required input files         |
| Job state does not allow stage execution  | `409`     | `JOB_STATE_INVALID`      | Check job state before triggering   |

#### File Upload Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| File exceeds max size                     | `413`     | `FILE_TOO_LARGE`         | Reduce file size                    |
| Empty file uploaded                       | `400`     | `FILE_EMPTY`             | Upload a non-empty file             |
| Path traversal detected                   | `400`     | `FILE_PATH_TRAVERSAL`    | Remove `../` from file paths        |
| Invalid file format                       | `422`     | `FILE_FORMAT_INVALID`    | Use supported file format           |
| Invalid JSON content                      | `400`     | `FILE_JSON_INVALID`      | Fix JSON syntax                     |

#### Deployment Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Image Group not found                     | `404`     | `IMAGE_GROUP_NOT_FOUND`  | Verify image_group_id               |
| Image Group not in deployable state       | `409`     | `IMAGE_NOT_DEPLOYABLE`   | Build must complete first           |
| Image Group already deployed              | `409`     | `IMAGE_ALREADY_DEPLOYED` | Cannot re-deploy; create new build  |
| Image not available for job               | `400`     | `IMAGE_JOB_MISMATCH`    | Verify Image Group belongs to Job   |

#### Cleanup Errors

| Scenario                                  | HTTP Code | Error Code               | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Image Group not eligible for cleanup      | `409`     | `CLEANUP_STATE_INVALID`  | Only FAILED images can be cleaned   |
| Cleanup operation failed                  | `500`     | `CLEANUP_FAILED`         | Retry the cleanup operation         |

### 19.2 Rate Limiting Responses

| Scenario                                  | HTTP Code | Response Header          | User Action                        |
|-------------------------------------------|-----------|--------------------------|-------------------------------------|
| Rate limit exceeded                       | `429`     | `Retry-After: <seconds>` | Wait and retry after indicated time |

---

## 20. Non-Functional Requirements

### 20.1 Performance

| Requirement                                              | Target                              |
|----------------------------------------------------------|-------------------------------------|
| API response time for synchronous operations (create, query, delete) | P95 ≤ 500ms           |
| Concurrent pipeline support                               | 1 pipeline (sequential execution)  |
| NFS result polling interval                               | Configurable (default: 5 seconds)  |

### 20.2 Reliability

| Requirement                                              | Target                              |
|----------------------------------------------------------|-------------------------------------|
| API availability                                          | Available when OIM host is running |
| Idempotent operations                                     | All write operations are idempotent |
| Audit trail                                               | All state transitions are logged   |

### 20.3 Security

| Requirement                                              | Target                              |
|----------------------------------------------------------|-------------------------------------|
| API transport                                             | HTTPS (TLS, port 443)             |
| Authentication                                            | OAuth 2.0 client credentials + JWT |
| Credential storage                                        | Ansible Vault (encrypted at rest)  |
| Path traversal protection                                 | All file operations validated      |
| NFS queue file permissions                                | `0600` (owner-only)               |

---

## 21. Acceptance Criteria

### 21.1 Feature 1: Workflow Optimization

| AC ID    | Criterion                                                                                       | Verification Method |
|----------|-------------------------------------------------------------------------------------------------|---------------------|
| AC-WF-01 | A Job can be created via API and returns a valid Job ID in UUID format                           | API test            |
| AC-WF-02 | The create-local-repository stage can be triggered and completes asynchronously                  | API test + polling  |
| AC-WF-03 | The parse-catalog stage accepts a valid JSON catalog file and returns parsed output              | API test            |
| AC-WF-04 | The build-image stage enforces prerequisite ordering and rejects out-of-order execution          | API test            |
| AC-WF-05 | Stages transition through the correct state machine states (PENDING → IN_PROGRESS → COMPLETED)  | API test + polling  |
| AC-WF-06 | A failed stage transitions the Job to FAILED state                                               | API test            |
| AC-WF-07 | Duplicate requests with the same Idempotency-Key return the original response (no duplicates)   | API test            |
| AC-WF-08 | A Job in terminal state rejects further stage execution with 409 Conflict                        | API test            |
| AC-WF-09 | All state transitions produce audit events                                                       | Log / audit check   |
| AC-WF-10 | File uploads exceeding the size limit are rejected with 413                                      | API test            |
| AC-WF-11 | Path traversal in file uploads is rejected with 400                                              | API test            |
| AC-WF-12 | The complete build pipeline can be executed end-to-end (create job → all stages → built image)   | Integration test    |

### 21.2 Feature 2: Image Management

| AC ID    | Criterion                                                                                       | Verification Method |
|----------|-------------------------------------------------------------------------------------------------|---------------------|
| AC-IM-01 | A built Image Group can be deployed to target nodes                                              | API test            |
| AC-IM-02 | Deployment transitions the Image Group through DEPLOYING → DEPLOYED states                       | API test + polling  |
| AC-IM-03 | Deployed nodes can be PXE-booted / restarted via the restart API                                 | API test            |
| AC-IM-04 | Node diff logic ensures only new nodes are PXE-booted                                            | API test            |
| AC-IM-05 | Validation tests run against deployed images and return structured results                       | API test            |
| AC-IM-06 | Images are tagged as PASSED or FAILED based on test results                                      | API test            |
| AC-IM-07 | Failed images can be cleaned up via user-initiated cleanup API                                   | API test            |
| AC-IM-08 | Cleanup removes all associated artifacts                                                         | API test + storage  |
| AC-IM-09 | Cleanup failure does not leave Image Group in a corrupted state                                  | API test            |
| AC-IM-10 | Deploying an Image Group not in BUILT state is rejected with 409                                 | API test            |
| AC-IM-11 | Re-deploying an already deployed Image Group is rejected with 409                                | API test            |

### 21.3 Authentication and Authorization

| AC ID    | Criterion                                                                                       | Verification Method |
|----------|-------------------------------------------------------------------------------------------------|---------------------|
| AC-AU-01 | OAuth client can be registered with valid Basic Auth credentials                                 | API test            |
| AC-AU-02 | Client registration returns client_id and client_secret                                          | API test            |
| AC-AU-03 | JWT token can be obtained with valid client credentials                                          | API test            |
| AC-AU-04 | Protected endpoints reject requests without valid JWT tokens (401)                               | API test            |
| AC-AU-05 | Endpoints enforce scope requirements (403 for insufficient scope)                                | API test            |
| AC-AU-06 | Expired tokens are rejected (401)                                                                | API test            |
| AC-AU-07 | Max client limit is enforced (409 when exceeded)                                                 | API test            |

---

## 22. Open Items and Deferred Features

### 22.1 Items Requiring Alignment (from Gap Analysis)

| Item ID | Topic                                    | Decision Needed                                              | Impact  |
|---------|------------------------------------------|--------------------------------------------------------------|---------|
| C-01    | Concurrent Build & Deploy Execution       | Confirmed: **Sequential only** for this release              | Architecture |
| C-02    | Automated vs. User-Initiated Cleanup      | Confirmed: **User-initiated only** for this release          | Feature scope |
| C-03    | Build Stage Names and Count               | Confirm final list of stages and canonical names (kebab-case) | API contract |

### 22.2 Deferred Features (Future Releases)

| Item ID | Feature                                  | Notes                                                        |
|---------|------------------------------------------|--------------------------------------------------------------|
| ~~DF-01~~ | ~~Automated scheduled cleanup~~         | **Moved to in-scope** — cron job every 24 hours for validation-failed images |
| DF-02   | Concurrent pipeline execution             | Support multiple simultaneous build/deploy pipelines          |
| DF-03   | "Promoted" image tagging                  | Ability to tag images as "promoted" for production use        |
| DF-04   | Restart API with direct PXE mapping file  | Upload PXE mapping file via restart endpoint                 |
| DF-05   | Deploy via CSV mapping file               | Deploy using a CSV pointing to a mapping file                 |
| DF-06   | Persistent database (PostgreSQL)          | Replace in-memory repositories with durable storage           |
| DF-07   | Multi-cluster deployment                  | Support deployments across multiple clusters                  |
| DF-08   | Non-x86 architecture support              | ARM and other architectures                                   |
| DF-09   | Input folder versioning in GitLab         | Automatic versioning of generated input files in GitLab       |

### 22.3 Items Requiring Clarification

| Item ID | Topic                                    | Question                                                     |
|---------|------------------------------------------|--------------------------------------------------------------|
| CL-01   | "Promoted" image status                   | Does "promoted" map to `PASSED`, or is it a separate concept? |
| CL-02   | Input folder versioning                   | Is GitLab commit implicit, pipeline-level, or deferred?       |
| CL-03   | Performance requirements location          | Where are authoritative performance targets documented?       |

---

## 23. Traceability Matrix

### 23.1 BSpec → Functional Requirements

| BSpec Item                              | Functional Requirement(s)             | Gap Reference |
|-----------------------------------------|---------------------------------------|---------------|
| Workflow Optimization — Job Creation     | FR-WF-01, FR-WF-02, FR-WF-03         | A-04          |
| Workflow Optimization — File Upload      | FR-WF-04                              | A-05          |
| Workflow Optimization — Build Stages     | FR-WF-05, FR-WF-06, FR-WF-07         | A-06          |
| Image Management — Deploy               | FR-IM-01                              | A-07          |
| Image Management — Restart/PXE Boot     | FR-IM-02                              | A-08          |
| Image Management — TestValidate         | FR-IM-03                              | A-09          |
| Image Management — Cleanup              | FR-IM-04                              | B-01, C-02    |
| Authentication                          | FR-AUTH-01, FR-AUTH-02, FR-AUTH-03     | A-10          |

### 23.2 Gap Analysis → Functional Spec Coverage

| Gap ID | Gap Topic                              | Addressed In                        | Status     |
|--------|----------------------------------------|-------------------------------------|------------|
| A-01   | Scope definition                        | Section 5                           | Addressed  |
| A-02   | User personas                           | Section 4                           | Addressed  |
| A-03   | Detailed workflow descriptions           | Section 14                          | Addressed  |
| A-04   | Job creation specification               | FR-WF-01                            | Addressed  |
| A-05   | File upload specification                | FR-WF-04                            | Addressed  |
| A-06   | Image building stage details             | FR-WF-05, FR-WF-06, FR-WF-07       | Addressed  |
| A-07   | Deployment API details                   | FR-IM-01                            | Addressed  |
| A-08   | PXE boot / node restart details          | FR-IM-02                            | Addressed  |
| A-09   | Validation test results structure        | FR-IM-03                            | Addressed  |
| A-10   | Authentication / authorization           | Section 9                           | Addressed  |
| A-11   | API input/output specifications          | Section 10, Section 16              | Addressed  |
| A-12   | Customer-facing constraints              | Section 18                          | Addressed  |
| A-13   | Comprehensive error handling             | Section 19                          | Addressed  |
| A-14   | Testable acceptance criteria             | Section 21                          | Addressed  |
| A-15   | Image Group state machine                | Section 12                          | Addressed  |
| A-16   | Rate limiting specification              | Section 18 (CON), Section 19.2      | Addressed  |
| B-01   | Automated cleanup disposition            | Section 22 (deferred)               | Addressed  |
| B-02   | "Promoted" image status                  | Section 22 (clarification needed)   | Addressed  |
| B-03   | Input folder versioning                  | Section 22 (deferred)               | Addressed  |
| B-04   | "Good to have" deferred features         | Section 22 (deferred)               | Addressed  |
| B-05   | Performance requirements                 | Section 20, Section 22              | Addressed  |
| C-01   | Concurrent build & deploy                | Section 5 (sequential), Section 22  | Addressed  |
| C-02   | Automated vs. user-initiated cleanup     | Section 5, FR-IM-04                 | Addressed  |
| C-03   | Build stage names and count              | Section 22 (alignment needed)       | Addressed  |
| D-01   | Error flagging behavior                  | Section 19                          | Addressed  |
| D-02   | "Minimum basic tests" definition         | FR-IM-03                            | Addressed  |
| D-03   | Cleanup failure handling                 | FR-IM-04                            | Addressed  |

---

## Document Approval

| Role                 | Name | Date | Signature |
|----------------------|------|------|-----------|
| Product Owner        |      |      |           |
| Engineering Lead     |      |      |           |
| QA Lead              |      |      |           |
| Technical Architect  |      |      |           |

---

*End of Functional Specification*
