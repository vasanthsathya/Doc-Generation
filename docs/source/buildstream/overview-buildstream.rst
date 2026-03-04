.. _overview-buildstream:

BuildStreaM Overview
====================

BuildStreaM is a catalog-driven automation solution that extends Omnia's capabilities with policy-enforced CI/CD workflows. BuildStreaM replaces manual image configuration with automated build → validate → promote pipelines, enabling faster deployment and consistent configurations across HPC clusters.

.. contents:: On This Page
   :local:
   :depth: 2

What BuildStreaM Does
---------------------

BuildStreaM automates the complete lifecycle from build → validate → promote using:

- **Catalog as single source of truth**: Regularly updated package metadata, dependency rules, and role configurations
- **End-to-end test automation**: Stage-gated workflows and service APIs for build, validation and promotion
- **Compliance & policy gates**: SBOM generation, CVE/license checks, and optional signing/attestation to block non-compliant releases
- **Multi-arch support**: Images for x86_64, aarch64, and other architectures
- **Observability**: Structured logs for each stage

BuildStreaM vs Traditional Omnia Deployment
-------------------------------------------

| Aspect | Traditional Omnia | BuildStreaM |
|--------|-------------------|-------------|
| **Workflow** | Manual playbook execution | Automated CI/CD pipelines |
| **Configuration** | Manual file editing | Catalog-driven definitions |
| **Process** | Step-by-step manual intervention | Pipeline automation with stage gates |
| **Validation** | Manual testing and verification | Automated validation stages |
| **Scalability** | Limited by manual processes | Scales with pipeline automation |
| **Consistency** | Variable based on admin skill | Consistent catalog-driven results |
| **Error Recovery** | Manual rollback procedures | Pipeline-based rollback capabilities |

Key Benefits
-------------

BuildStreaM provides significant advantages for HPC infrastructure management:

- **Reduced deployment effort**: Automates repetitive setup tasks and eliminates manual configuration errors
- **Faster time-to-production**: Pipeline automation accelerates the build and deployment process
- **Enhanced reliability**: Stage-gated workflows ensure proper validation before promotion
- **Consistent configurations**: Catalog-driven approach eliminates configuration drift
- **Improved compliance**: Automated policy gates and validation ensure compliance requirements are met

When to Use BuildStreaM
----------------------

BuildStreaM is ideal for environments that:

- Require frequent image updates and configuration changes
- Need consistent deployment across multiple clusters
- Have compliance requirements that mandate automated validation
- Want to reduce manual intervention in deployment processes
- Need to scale deployment operations efficiently

**Consider traditional Omnia deployment when:**

- You have simple, static deployment requirements
- Your environment has limited CI/CD infrastructure
- You prefer direct manual control over each deployment step
- Your compliance requirements can be met with manual processes

Architecture Overview
--------------------

BuildStreaM implements a modular monolith architecture with the following key components:

- **API Facade**: Single external entry point providing authentication and routing
- **Workflow Orchestrator**: Central component that enforces stage gating and manages job execution
- **Catalog Manager**: Handles catalog parsing, normalization, and input generation
- **Build Module**: Wrapper invoking Omnia for image building and artifact publishing
- **Validate Module**: Wrapper invoking Omnia for image correctness checks and test suite execution
- **Promote Module**: Policy enforcement and promotion of validated images

.. AI_REVIEW: Architecture diagram reference from HLD Section 3 - verify diagram availability and placement

Getting Started with BuildStreaM
--------------------------------

To start using BuildStreaM:

1. Ensure you have a working Omnia control plane deployment
2. Set up a GitLab server for pipeline automation
3. Enable BuildStreaM in your Omnia configuration
4. Configure your catalog definitions
5. Run the initial setup playbooks

For detailed setup instructions, see :doc:`how-to-buildstream-enabling-buildstream`.

Prerequisites
-------------

Before using BuildStreaM, ensure you have:

- A working Omnia control plane deployment
- GitLab server with administrator access
- Sufficient network connectivity between Omnia and GitLab
- Understanding of CI/CD pipeline concepts
- Administrator privileges on the Omnia control plane

.. note:: BuildStreaM requires a separate GitLab instance and is not compatible with traditional Omnia deployment workflows.

Related Topics
--------------

* :doc:`concepts-buildstream-architecture`
* :doc:`how-to-buildstream-enabling-buildstream`
* :doc:`concepts-buildstream-catalog`
