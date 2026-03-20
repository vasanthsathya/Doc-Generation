.. _concept-buildstream-overview:

Omnia BuildStreaM: Catalog-Driven Build Automation
==================================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Omnia BuildStreaM provides a comprehensive automation solution for managing infrastructure build workflows. It uses a catalog-driven approach where you define your build requirements in a structured catalog file, and BuildStreaM executes automated pipelines to create and deploy images according to your specifications.

BuildStreaM addresses the key challenges in HPC cluster image management:

   - **Automation**: Eliminates manual build and deployment processes
   - **Integration**: Works seamlessly with existing Omnia deployments
   - **Traceability**: Provides complete audit trails for all build operations
   
To build your own custom workflows, you can use the BuildStreaM REST API. The BuildStreaM API documentation is available at `Omnia BuildStreaM API Documentation <https://developer.dell.com/apis/ea677050-f49b-49e1-a4b9-1cdd563415d9/versions/2.1.0/docs/Introduction.md>`_.

How BuildStreaM Works
--------------------

BuildStreaM implements a **modular monolith** architecture where domain capabilities are exposed as API endpoints backed by Python modules. All modules are co-deployed and share the same process/runtime while maintaining strict logical boundaries and well-defined interfaces.

**Primary Workflow**

BuildStreaM orchestrates the image lifecycle through a stage-gated workflow:

```
ParseCatalog → GenerateInputFiles → PrepareRepos → BuildImage → ValidateImage → ValidateImageOnTest → Promote
```

**Stage Descriptions**

- **ParseCatalog**: Fetches and validates catalog and creates ``jobId`` + intermediate JSONs
- **GenerateInputFiles**: Produces Omnia-compliant input files
- **PrepareRepos**: Ensures required local/image repositories exist via CreateLocalRepo/UpdateLocalRepo + CreateImageRepo
- **BuildImage**: Creates stateless image artifacts
- **ValidateImage**: Performs static image validation for correctness (structure/format and metadata sanity checks)
- **ValidateImageOnTest**: Deploys and validates images on testbed using minimal tests
- **Promote**: Marks validated images as the approved baseline (invoked internally in R1)

**Architecture Components**

- **API Facade**: Single external entry point providing request validation and OAuth 2.0 Client Credentials authentication
- **Workflow Orchestrator**: Centralizes orchestration, stage guarding, idempotency enforcement, and error handling
- **Core Modules**: Implement domain logic (Catalog Manager, Build Module, Validate Module, Promote Module)
- **Infrastructure/Data Plane**: Houses Artifact Repository, Metadata Store, and Cache
- **External**: OMNIA executes build and validation logic; provisions images to HPC target environment

**Authentication Model**

BuildStreaM uses OAuth 2.0 Client Credentials for machine-to-machine authentication:

- **Base URI**: ``https://<HOST_ADDRESS>:<PORT_NUM>/api/v1/``
- **OAuth Endpoints**: ``POST /register``, ``POST /auth/token``
- **Access Method**: Bearer token presented in ``Authorization: Bearer <token>`` header

**Multi-Architecture Support**

BuildStreaM supports multiple CPU architectures for image building:
- x86_64 (standard 64-bit Intel/AMD)
- aarch64 (ARM 64-bit)

**Security and Compliance**

BuildStreaM includes enterprise-grade security features:
- OAuth 2.0 Client Credentials authentication
- OS-protected encrypted secrets file
- Audit logging with correlation IDs
- SBOM generation and CVE checking
- License policy enforcement
- Secure deserialization and path traversal defenses

.. toctree::
   :maxdepth: 1
   :caption: BuildStreaM Deployment Workflow

   how-to-setup
   how-to-gitlab-deployment
   how-to-catalog-configuration
   how-to-catalog-pipeline-update
