.. _buildstream-architecture:

BuildStreaM Architecture Overview
==================================

BuildStream provides a three-pipeline architecture that separates build, deployment, and validation workflows. This overview explains the key architectural concepts, components, and benefits for HPC infrastructure automation.

What Is BuildStreaM?
--------------------

BuildStreaM is an automation service that manages the end-to-end workflow for building, deploying, and validating Omnia OS images. It provides a catalog-driven interface for orchestrating the image lifecycle through a decoupled, event-driven architecture.

Why BuildStreaM Architecture Matters
-------------------------------------

The three-pipeline architecture provides several key benefits:

**Independent Pipeline Execution**

   - Build pipeline can run independently of deployment activities
   - Deploy and Validate pipeline can be triggered separately based on infrastructure readiness
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

Three-Pipeline Model
~~~~~~~~~~~~~~~~~~~~

BuildStreaM organizes workflows into three distinct pipelines:

**Build Pipeline (``/de.gitlab-ci-build.yml``)**

   - Triggered by catalog or configuration file changes
   - Creates Job and Image Group entities
   - Executes build stages: ``parse-catalog``, ``generate-input-files``, ``create-local-repository``, ``build-image``
   - Establishes the 1:1 Job ID ↔ Image Group ID mapping
   - Produces OS images as output artifacts

**Deploy and Validate Pipeline (``.gitlab-ci-deploy.yml``)**

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

Job and Image Group Concepts
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Job**

   - A unique unit of work representing a complete build pipeline execution
   - Identified by a unique ID that persists across all three pipelines
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
   - Enable role-specific image management

Image Group Lifecycle State Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


OAuth 2.0 Authentication
~~~~~~~~~~~~~~~~~~~~~~~

BuildStreaM uses OAuth 2.0 client credentials flow for authentication:

**Authentication Flow:**

1. Client registers with BuildStreaM API (System Administrator task)
2. Client receives client credentials
3. Client requests access token from OAuth authorization server
4. Client includes access token in Authorization header
5. BuildStreaM API validates token and processes request

**Benefits:**

   - Enhanced security with token-based authentication
   - Better integration with enterprise identity providers
   - Token expiration and refresh capabilities
   - Audit trail of authentication events

Resume and Retry Capabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BuildStreaM provides intelligent execution management:

**Build Stage Resume:**

   - Failed builds can be retried with smart resume
   - Successfully built images are skipped on retry
   - Attempt number tracking preserves audit trail
   - Log files numbered by attempt for debugging

**Deploy Stage Re-run:**

   - Deploy stages can be re-run after completion (inputs may change)
   - Configuration change detection
   - Prevents redundant PXE boots
   - Supports adding nodes to existing deployments

**Stage Execution Logic:**

   - Build stages: Completed stages cannot be re-run (immutable)
   - Deploy stages: Completed stages can be re-run (inputs may change)
   - Prevents invalid state transitions and data corruption

GitLab CI/CD Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BuildStreaM integrates with GitLab CI/CD for automated pipeline execution:

**Pipeline Structure:**

   - Parent pipeline router analyzes catalog and triggers appropriate child pipeline
   - Build pipeline triggered by catalog changes
   - Deploy and Validate pipeline triggered by PXE mapping changes
   - CleanUp pipeline triggered manually or on schedule

**Dynamic Child Pipelines:**

   - Parent router dispatches to appropriate child pipeline based on pipeline type
   - Improved user experience with meaningful pipeline names

Related Topics
--------------

* :doc:`managing-buildstream-catalogs-and-pipelines`
* :doc:`buildstream-resume-retry`
* :doc:`buildstream_tables`

.. note::
   This topic provides an architectural overview of BuildStreaM. For pipeline execution procedures, see :doc:`managing-buildstream-catalogs-and-pipelines`.
