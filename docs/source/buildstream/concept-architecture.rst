.. _concept-buildstream-architecture:

BuildStreaM Architecture Overview
=================================

.. note::
   This topic is pending SME validation. Content may change before publication.

BuildStreaM is a build and validation automation solution that provides a catalog-driven, policy-enforced lifecycle to build, validate, and promote Omnia-compatible images. This topic explains the modular monolith architecture and how BuildStreaM integrates with Omnia for automated build and validation workflows.

.. contents:: On This Page
   :local:
   :depth: 2

What is BuildStreaM
-------------------

BuildStreaM (BSM) implements a **modular monolith** architecture where domain capabilities are exposed as API endpoints backed by Python modules. All modules are co-deployed and share the same process/runtime while maintaining strict logical boundaries and well-defined interfaces.

The system provides:
- **Catalog-driven builds**: Source-of-truth input that defines roles, packages, architectures, and validation dependencies
- **Stage-gated flow**: Enforcement that stages must execute in the defined order
- **Policy enforcement**: Automated validation and promotion workflows
- **Integration with Omnia**: Leverages Omnia as the authoritative build/deploy backend

Why BuildStreaM Matters
------------------------

BuildStreaM addresses key challenges in HPC cluster image management:

- **Automation**: Eliminates manual build and validation processes
- **Consistency**: Ensures all builds follow the same validation procedures
- **Traceability**: Provides complete audit trails for all build operations
- **Scalability**: Supports multiple concurrent build operations with proper resource management
- **Integration**: Seamlessly works with existing Omnia deployments

How BuildStreaM Works
---------------------

### Architectural Components

BuildStreaM consists of several key components that work together to provide automated build and validation workflows:

**API Facade**
- Single external entry point providing request validation and authentication
- Handles OAuth 2.0 Client Credentials and Bearer token authentication
- Routes requests to appropriate internal modules

**Workflow Orchestrator**
- Central component that enforces stage gating and idempotency
- Provides admission control and async task dispatch
- Handles consistent error handling across all operations

**Core Domain Modules**
- **Catalog Manager**: Catalog parsing, normalization, and input generation
- **Build Module**: Wrapper invoking Omnia for image building and artifact publishing
- **Validate Module**: Wrapper invoking Omnia for image correctness checks and test suite execution
- **Promote Module**: Policy enforcement and promotion of validated images

**Shared Modules**
- **Notification & Approval Module**: Approval workflows and notifications
- **Observability & Telemetry Modules**: Logs, metrics, and traces

**Data Plane**
- **Artifact Repository**: Immutable storage for images, manifests, and validation reports
- **Metadata Store**: Persistent metadata for job tracking and state management
- **Cache**: Optional caching for derived/recomputable data

### Workflow Stages

BuildStreaM implements a stage-gated workflow where each stage must complete successfully before the next stage begins:

1. **ParseCatalog**: Validates catalog structure and extracts build requirements
2. **GenerateInputFiles**: Creates input files for Omnia build processes
3. **PrepareRepos**: Sets up local and remote repositories for build operations
4. **BuildImage**: Executes Omnia build workflows to create images
5. **ValidateImage**: Runs validation tests on built images
6. **ValidateImageOnTest**: Deploys images to test environment for validation
7. **Promote**: Marks validated images as approved baselines

### Integration Points

BuildStreaM integrates with several external systems:

**Omnia Integration**
- BuildStreaM acts as an orchestrator that invokes Omnia for actual build and validation operations
- Omnia provides the core build, validation, and deployment capabilities
- BuildStreaM manages the workflow and tracks progress

**GitLab Integration**
- Provides source control management for catalogs and pipeline definitions
- Enables automated pipeline triggering based on catalog changes
- Offers web interface for monitoring build progress and results

**External Dependencies**
- **Artifact Repository**: Stores build artifacts and validation reports
- **Metadata Store**: Maintains job state and tracking information
- **OAuth Token Service**: Provides authentication and authorization

System Limitations
-------------------

BuildStreaM has several limitations that customers should be aware of:

**Single-User Support**
- Baseline supports a single client/user
- Multi-tenant or multi-user access is a roadmap item
- No role-based access control in baseline

**Performance Constraints**
- Default maximum of 1 concurrent build operation
- No queueing for overflow requests (requests beyond limits are rejected)
- Build times depend on external capacity (Omnia, testbed availability)

**Operational Constraints**
- No high availability or disaster recovery guarantees
- No production deployment automation (build and validation only)
- No cloud image target support in baseline

.. note::
   BuildStreaM represents a separate workflow from traditional Omnia deployment. The documentation is organized as a separate section to avoid confusion with standard Omnia deployment procedures.

Related Topics
--------------

* :doc:`how-to-get-started`
* :doc:`how-to-configure-catalogs`
* :doc:`../reference/api/buildstream`
