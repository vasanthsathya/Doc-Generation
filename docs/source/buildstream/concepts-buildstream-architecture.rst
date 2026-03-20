.. _concepts-buildstream-architecture:



BuildStreaM Architecture Concepts

=================================



BuildStreaM implements a modular monolith architecture that provides catalog-driven automation while maintaining clear component boundaries and well-defined interfaces. This architecture enables BuildStreaM to function as a single deployable unit while supporting complex workflow orchestration.



.. contents:: On This Page

   :local:

   :depth: 2



Modular Monolith Pattern

------------------------



BuildStreaM uses a modular monolith architectural style where:



- **Single deployable unit**: All modules are co-deployed and share the same process/runtime

- **Strict logical boundaries**: Modules maintain clear interfaces and separation of concerns

- **In-process communication**: Modules communicate via function calls rather than network requests

- **Shared state management**: State is managed centrally through the Orchestrator and data stores



This approach provides the operational simplicity of a monolith while maintaining the architectural clarity of microservices.



Core Components

---------------



BuildStreaM consists of several key components that work together to provide automated build, validation, and promotion workflows:



API Facade

~~~~~~~~~~



The API Facade serves as the single external entry point for BuildStreaM:



- **Authentication**: Enforces OAuth 2.0 Client Credentials authentication

- **Request validation**: Validates and normalizes incoming requests

- **Routing**: Directs requests to appropriate internal modules

- **Rate limiting**: Implements admission control to prevent resource exhaustion



.. AI_REVIEW: OAuth 2.0 implementation details inferred from HLD - verify against Engineering Notes



Workflow Orchestrator

~~~~~~~~~~~~~~~~~~~~~



The Workflow Orchestrator is the central coordination component:



- **Stage gating**: Enforces that operations must follow the defined sequence

- **Idempotency**: Ensures repeated requests do not create duplicate work

- **Async task management**: Handles long-running operations and job tracking

- **Error handling**: Provides consistent error handling and recovery procedures



**Stage-gated flow enforcement**: BuildStreaM enforces strict order: ParseCatalog → GenerateInputFiles → PrepareRepos → BuildImage → ValidateImage → ValidateImageOnTest → Promote. Out-of-order requests are rejected with `412 Precondition Failed`.



Domain Modules

~~~~~~~~~~~~~~



BuildStreaM includes several domain modules that implement specific business logic:



Catalog Manager

^^^^^^^^^^^^^^^



The Catalog Manager handles all catalog-related operations:



- **Catalog parsing**: Processes and validates catalog files

- **Normalization**: Converts catalog data into internal formats

- **Input generation**: Creates input files for downstream processes

- **Schema validation**: Ensures catalog compliance with defined schemas



Build Module

^^^^^^^^^^^^



The Build Module wraps Omnia's image building capabilities:



- **Image building**: Invokes Omnia for container image construction

- **Artifact publishing**: Manages publication of build artifacts

- **Repository preparation**: Handles CreateLocalRepo, UpdateLocalRepo, and CreateImageRepo operations

- **Build orchestration**: Coordinates build processes across multiple targets



Validate Module

^^^^^^^^^^^^^^^^



The Validate Module manages image validation processes:



- **Static validation**: Performs image correctness checks (structure, metadata, basic sanity)

- **Test execution**: Runs validation suites on testbed environments

- **Report generation**: Creates detailed validation reports

- **Result aggregation**: Combines results from multiple validation steps



Promote Module

^^^^^^^^^^^^^^



The Promote Module handles promotion workflows:



- **Policy enforcement**: Applies promotion policies and gates

- **Approval workflows**: Manages approval processes for promotions

- **Baseline management**: Maintains approved image baselines

- **Channel management**: Manages promotion channels and environments



.. AI_REVIEW: Promote Module details marked as [NOT R1] in HLD - verify current implementation status



Shared Modules

~~~~~~~~~~~~~~



BuildStreaM includes shared modules that provide cross-cutting capabilities:



Notification & Approval Module

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Provides notification and approval workflows:



- **Approval management**: Handles approval processes for promotions

- **Notification system**: Sends notifications for workflow events

- **User management**: Manages user permissions and access



.. note:: The Notification & Approval Module is marked as [NOT R1] in the current release scope.



Observability & Telemetry Modules

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Handles monitoring and telemetry:



- **Structured logging**: Provides structured logs for events and transitions

- **Metrics collection**: Collects and reports performance metrics

- **Distributed tracing**: Tracks requests across component boundaries



.. note:: Full observability features are marked as [NOT R1] in the current release scope.



Infrastructure and Data Plane

-----------------------------



BuildStreaM relies on several infrastructure components for data storage and management:



Artifact Repository

~~~~~~~~~~~~~~~~~~~



Provides immutable storage for large artifacts:



- **Image storage**: Stores container images and build artifacts

- **Metadata storage**: Maintains SBOMs, manifests, and validation reports

- **Version control**: Ensures artifact immutability and version tracking

- **Access control**: Manages access to stored artifacts



Metadata Store

~~~~~~~~~~~~~



Provides durable structured storage for metadata:



- **Job tracking**: Stores job and workflow execution metadata

- **Candidate management**: Maintains candidate image information

- **Baseline tracking**: Manages approved baseline information

- **Audit logging**: Stores immutable audit events



Cache

~~~~



Provides optional caching for derived data:



- **Performance optimization**: Caches frequently accessed data

- **Derived data**: Stores computed results like dependency closures

- **Best-effort storage**: Cache data can be safely lost and recomputed

- **Security**: Never stores secrets or sensitive information in cache



.. note:: Cache implementation is marked as [NOT R1] in the current release scope.



Security Model

--------------



BuildStreaM implements a comprehensive security model:



Authentication

~~~~~~~~~~~~~~



BuildStreaM uses OAuth 2.0 Client Credentials for authentication:



- **Machine-to-machine**: Designed for automation client access

- **Token-based**: Uses Bearer tokens for API access

- **Secure storage**: Stores credentials in OS-protected encrypted files

- **Memory-only access**: Secrets are loaded into memory only during runtime



Authorization

~~~~~~~~~~~~~



BuildStreaM implements role-based access control:



- **Scoped credentials**: Different credentials for different runtime roles

- **Least privilege**: Each component has minimal required permissions

- **ACL enforcement**: Store access controls protect sensitive data

- **Audit trails**: All privileged operations generate audit events



Data Protection

~~~~~~~~~~~~~~~



BuildStreaM includes several data protection mechanisms:



- **Immutable artifacts**: Published artifacts cannot be modified

- **Audit events**: All stage transitions generate immutable audit records

- **Error sanitization**: External error messages do not reveal sensitive details

- **Secure logging**: Structured logs with redaction rules for sensitive data



API Architecture

----------------



BuildStreaM exposes a RESTful API with the following characteristics:



Base URI

~~~~~~~~



All API endpoints are accessed via:



```

https://<HOST_ADDRESS>:<PORT_NUM>/api/v1/

```



Authentication Endpoints

~~~~~~~~~~~~~~~~~~~~~~~



OAuth 2.0 Client Credentials endpoints:



- `POST /register`: Register new client credentials

- `POST /auth/token`: Obtain access tokens



Functional Endpoints

~~~~~~~~~~~~~~~~~~~~~



Core workflow endpoints:



- `POST /jobs`: Create new workflow jobs

- `GET /jobs/{jobId}`: Retrieve job status and details

- `DELETE /jobs/{jobId}`: Cancel or remove jobs



Stage Endpoints

~~~~~~~~~~~~~~



Individual workflow stage endpoints:



- `POST /jobs/{jobId}/stages/parse-catalog`: Parse catalog definitions

- `POST /jobs/{jobId}/stages/generate-input-files`: Generate input files

- `POST /jobs/{jobId}/stages/create-image-repository`: Create image repository

- `POST /jobs/{jobId}/stages/build-image`: Build images

- `POST /jobs/{jobId}/stages/create-local-repository`: Create local repository

- `POST /jobs/{jobId}/stages/update-local-repository`: Update local repository

- `POST /jobs/{jobId}/stages/validate-image`: Validate images

- `POST /jobs/{jobId}/stages/validate-image-on-test`: Validate on testbed



Catalog Endpoints

~~~~~~~~~~~~~~~~



Catalog-related endpoints:



- `GET /jobs/{jobId}/catalog/roles`: Retrieve catalog roles

- `GET /jobs/{jobId}/catalog/roles/packages`: Retrieve role packages



.. AI_REVIEW: API endpoint details from HLD Section 2.1.1 - verify against actual implementation



Integration Points

------------------



BuildStreaM integrates with several external systems:



Omnia Integration

~~~~~~~~~~~~~~~~~



BuildStreaM uses Omnia as the build and validation backend:



- **Build operations**: Invokes Omnia for image building and provisioning

- **Validation operations**: Uses Omnia for image correctness checks

- **Resource management**: Leverages Omnia's resource management capabilities

- **Compatibility**: Maintains compatibility with existing Omnia workflows



GitLab Integration

~~~~~~~~~~~~~~~~~~



BuildStreaM integrates with GitLab for pipeline automation:



- **Project management**: Creates and manages GitLab projects

- **Pipeline execution**: Triggers and monitors GitLab CI/CD pipelines

- **Source control**: Manages catalog files in GitLab repositories

- **Runner management**: Coordinates GitLab runner operations



HPC Cluster Integration

~~~~~~~~~~~~~~~~~~~~~~~



BuildStreaM deploys to HPC cluster environments:



- **Target deployment**: Final deployment target for validated images

- **Resource provisioning**: Manages compute, storage, and network resources

- **Workload management**: Integrates with HPC workload schedulers

- **Monitoring**: Provides observability for deployed systems



Related Topics

--------------



* :doc:`overview-buildstream`

* :doc:`concepts-buildstream-catalog`

* :doc:`reference-buildstream-api`

