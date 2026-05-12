.. _buildstream-architecture:

BuildStream Architecture Overview
==================================

BuildStream provides a three-pipeline architecture that separates build, deployment, and validation workflows. This overview explains the key architectural concepts, components, and benefits for HPC infrastructure automation.

What Is BuildStream?
--------------------

BuildStream is a RESTful API service that automates the end-to-end workflow for building, deploying, validating, and managing Omnia OS images. It provides a programmatic interface for both human operators and CI/CD pipelines to orchestrate the image lifecycle through a decoupled, event-driven architecture.

Why BuildStream Architecture Matters
-------------------------------------

The three-pipeline architecture provides several key benefits:

**Independent Pipeline Execution**
- Build pipeline can run independently of deployment activities
- Deploy & Validate pipeline can be triggered separately based on infrastructure readiness
- CleanUp pipeline can be scheduled independently for maintenance

**Improved Resource Management**
- Separate pipelines allow better resource allocation and scheduling
- Failed deployments do not block new image builds
- Automated cleanup reduces manual intervention

**Enhanced Traceability**
- Job IDs persist across pipelines, providing complete lifecycle tracking
- Image Group lifecycle states provide clear visibility into deployment status
- Audit trails capture all state transitions and operations

**Scalability and Flexibility**
- Dynamic child pipeline generation for image selection
- Support for multiple image groups within a single job
- Easier integration with external CI/CD systems

How BuildStream Architecture Works
-----------------------------------

### Three-Pipeline Model

BuildStream organizes workflows into three distinct pipelines:

**Build Pipeline (``.gitlab-ci-build.yml``)**
- Triggered by catalog or configuration file changes
- Creates Job and Image Group entities
- Executes build stages: ``parse-catalog``, ``generate-input-files``, ``create-local-repository``, ``build-image``
- Establishes the 1:1 Job ID ↔ Image Group ID mapping
- Produces OS images as output artifacts

**Deploy & Validate Pipeline (``.gitlab-ci-deploy.yml``)**
- Triggered by PXE mapping file changes
- Selects existing Job ID via ``ListImages`` API
- Executes deployment stages: ``deploy``, ``restart``, ``validate``
- Manages Image Group lifecycle states
- Supports re-deployment with changed inputs

**CleanUp Pipeline (``.gitlab-ci-cleanup.yml``)**
- Triggered manually or via scheduled automation
- Selects existing Job ID for cleanup
- Executes cleanup stage to remove artifacts and images
- Transitions Image Group to ``CLEANED`` state
- Includes automated cron job for validation-failed images

### Job and Image Group Concepts

**Job**
- A unique unit of work representing a complete build pipeline execution
- Identified by a UUID v7 that persists across all three pipelines
- Contains stage execution history and attempt tracking
- Owned by a specific client with access control

**Image Group**
- A logical grouping of built OS images identified by an Image Group ID
- Maintains a strict 1:1 mapping with a Job ID
- Contains constituent images for different functional roles (e.g., ``slurm_node``, ``kube_control_plane``)
- Tracks lifecycle state from ``BUILT`` through deployment to ``CLEANED``

**Constituent Images**
- Individual OS images within an Image Group
- Each identified by a functional role name
- Stored in the ``images`` table with S3 path references
- Enable role-specific image management

### Image Group Lifecycle State Machine

Image Groups progress through the following states:

```
BUILT → DEPLOYING → DEPLOYED → RESTARTING → RESTARTED → VALIDATING → PASSED/FAILED → CLEANED
```

**State Descriptions:**

- ``BUILT``: Images successfully built, ready for deployment
- ``DEPLOYING``: Deployment in progress
- ``DEPLOYED``: Images deployed to target nodes
- ``RESTARTING``: PXE boot/restart in progress
- ``RESTARTED``: Nodes successfully restarted with new images
- ``VALIDATING``: Validation tests in progress
- ``PASSED``: All validation tests passed
- ``FAILED``: Validation tests failed or deployment error occurred
- ``CLEANED``: Artifacts and images removed via cleanup

### System Context

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

### REST API Endpoints

BuildStream provides the following API endpoints:

- ``PUT /api/v1/jobs/{job_id}/upload`` — Generic file upload for catalogs and configurations
- ``GET /api/v1/images`` — List built Image Groups with constituent image details
- ``POST /api/v1/jobs/{job_id}/stages/deploy`` — Initiate deployment to target nodes
- ``POST /api/v1/jobs/{job_id}/stages/restart`` — PXE boot with node diff handling and optional disable
- ``POST /api/v1/jobs/{job_id}/stages/validate`` — Post-deployment validation via Molecule
- ``DELETE /api/v1/jobs/{job_id}`` — Hard delete with artifact and image cleanup

### OAuth 2.0 Authentication

BuildStream uses OAuth 2.0 client credentials flow for authentication:

**Authentication Flow:**

1. Client registers with BuildStream API (System Administrator task)
2. Client receives ``client_id`` and ``client_secret``
3. Client requests JWT token from OAuth authorization server
4. Client includes JWT bearer token in ``Authorization`` header
5. BuildStream API validates token and processes request

**Benefits:**
- Enhanced security with token-based authentication
- Better integration with enterprise identity providers
- Token expiration and refresh capabilities
- Audit trail of authentication events

### Resume and Retry Capabilities

BuildStream provides intelligent execution management:

**Build Stage Resume:**
- Failed builds can be retried with smart resume
- Successfully built images are skipped on retry
- Attempt number tracking preserves audit trail
- Log files numbered by attempt for debugging

**Deploy Stage Re-run:**
- Deploy stages can be re-run after completion (inputs may change)
- Input hash tracking detects configuration changes
- Node diff logic prevents redundant PXE boots
- Supports adding nodes to existing deployments

**Stage Guard Logic:**
- Build stages: ``PENDING`` → Allow (initial), ``FAILED`` → Allow (retry), ``COMPLETED`` → Reject (immutable)
- Deploy stages: ``PENDING`` → Allow (initial), ``FAILED`` → Allow (retry), ``COMPLETED`` → Allow (re-run)
- Prevents invalid state transitions and data corruption

### Configuration Parameters

BuildStream configuration includes the following parameters:

- OAuth 2.0 client credentials (``client_id``, ``client_secret``)
- Image retention limit (maximum 50 non-CLEANED Image Groups)
- Storage backend selection (NFS or PowerScale)
- Automation framework configuration for Molecule validation
- Pipeline orchestration parameters for parent router

### GitLab CI/CD Pipeline Structure

BuildStream uses a parent router with dynamic child pipelines:

**Pipeline Files:**

- ``.gitlab-ci-build.yml`` — Build pipeline (catalog/config triggers)
- ``.gitlab-ci-deploy.yml`` — Deploy & Validate pipeline (PXE mapping triggers)
- ``.gitlab-ci-cleanup.yml`` — CleanUp pipeline (manual or scheduled triggers)
- ``.gitlab-ci.yml`` — Parent pipeline router

**Dynamic Child Pipelines:**

- Image selection via actual ``image_group`` names (e.g., ``image-build19``)
- Parent router dispatches to appropriate child pipeline
- Improved user experience with meaningful pipeline names

### Database Schema

BuildStream uses the following database schema:

- ``jobs`` table with ``pipeline_phase`` column
- ``image_groups`` table with strict 1:1 foreign key constraint to jobs
- ``images`` table for constituent image tracking
- ``job_stages`` table with ``attempt_number``, ``result_detail`` JSONB, and UNIQUE constraint

Benefits of BuildStream Architecture
------------------------------------

**Operational Efficiency**
- Independent pipeline execution reduces bottlenecks
- Automated cleanup reduces manual maintenance overhead
- Resume & Retry capabilities save time during failures

**Enhanced Flexibility**
- Dynamic child pipeline generation for complex workflows
- Support for multiple image groups per job
- Easier integration with external CI/CD systems

**Improved Observability**
- Complete lifecycle tracking with Job ID continuity
- Image Group state machine provides clear visibility
- Attempt number tracking preserves audit trails

**Better Resource Management**
- Separate pipelines enable better resource allocation
- Failed deployments do not block new builds
- Automated cleanup optimizes storage usage

**Future-Proof Architecture**
- Modular design supports future enhancements
- OAuth 2.0 authentication enables enterprise integration
- Extensible database schema supports new features

Related Topics
--------------

* :doc:`buildstream-api-reference`
* :doc:`buildstream-pipelines`
* :doc:`buildstream-resume-retry`
* :doc:`buildstream_tables`

.. note::
   This topic provides an architectural overview of BuildStream. For detailed API documentation, see :doc:`buildstream-api-reference`. For pipeline execution procedures, see :doc:`buildstream-pipelines`.

.. [SME VALIDATION REQUIRED: Verify all architectural details against actual BuildStream implementation]
