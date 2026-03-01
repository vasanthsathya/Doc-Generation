.. _concept-buildstream-overview:

BuildStreaM Overview
====================

.. note::
   This topic is pending SME validation. Content may change before publication.

BuildStreaM is a build and validation automation solution that provides catalog-driven, policy-enforced lifecycle to build, validate, and promote Omnia-compatible images. This topic provides a high-level overview of BuildStreaM workflows, functionality, and usage scenarios.

.. contents:: On This Page
   :local:
   :depth: 2

What is BuildStreaM
-------------------

BuildStreaM (BSM) automates the build and validation process for HPC cluster images. It uses a catalog-driven approach where you define your build requirements in structured catalog files, and BuildStreaM executes automated pipelines to create and validate images according to your specifications.

The system provides:
- **Catalog-driven builds**: Define roles, packages, and validation requirements in YAML catalogs
- **Automated pipeline execution**: GitLab-based pipelines that trigger automatically from catalog changes
- **Integration with Omnia**: Leverages Omnia as the underlying build and validation engine
- **Policy enforcement**: Ensures all builds follow consistent validation procedures

Why BuildStreaM Matters
----------------------

BuildStreaM addresses key challenges in HPC cluster image management:

- **Automation**: Eliminates manual build and validation processes
- **Consistency**: Ensures all builds follow the same validation procedures
- **Traceability**: Provides complete audit trails for all build operations
- **Scalability**: Supports automated builds across multiple environments
- **Integration**: Works seamlessly with existing Omnia deployments

How BuildStreaM Works
---------------------

BuildStreaM follows a simple, workflow-based approach:

### Catalog-Driven Approach

You define your build requirements in catalog files that specify:

- **Roles**: Node types in your cluster (compute, management, storage)
- **Packages**: Software components and versions for each role
- **Validation dependencies**: Tests that must run for each role

### Automated Pipeline Execution

When you update a catalog file:

1. **Pipeline triggers automatically** based on catalog changes
2. **BuildStreaM processes** the catalog and generates build requirements
3. **Omnia executes** the actual build and validation operations
4. **Results are published** to artifact repositories

### Integration with Omnia

BuildStreaM acts as an orchestrator that:
- Sends build requests to Omnia
- Monitors build progress and validation results
- Manages build artifacts and reports
- Enforces build policies and procedures

Current Limitations
-------------------

BuildStreaM 1.0 has the following limitations:

- **Promote and validate images** are not yet implemented
- **Single-user support** - only one client/user at a time
- **External dependencies** - requires GitLab and PostgreSQL
- **No high availability** - no disaster recovery guarantees

.. note::
   Future releases will address these limitations and add additional features.

Expected Outcomes
-----------------

After implementing BuildStreaM, you can expect:

- **Faster build cycles** through automation
- **Consistent image quality** through enforced validation
- **Reduced manual effort** in build and validation processes
- **Better traceability** of all build operations
- **Scalable build processes** across multiple environments

Important Considerations
------------------------

Before using BuildStreaM, consider:

- **Single-user limitation** - only one build operation at a time
- **External dependencies** - requires GitLab, PostgreSQL, and artifact repositories
- **Network connectivity** - needs reliable connections to external services
- **Storage requirements** - build artifacts require significant storage space

Related Topics
--------------

* :doc:`how-to-prepare-buildstream`
* :doc:`how-to-gitlab-deployment`
* :doc:`how-to-update-catalog-pipeline`
