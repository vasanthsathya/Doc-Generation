# BuildStreaM Content Plan

> **Phase:** COLLECT - Information gathering and planning  
> **Generated:** 2026-03-04  
> **Sources:** HLD v1.0, Demo Transcription (2026-02-26)  
> **Skill Document:** SKILL_COLLECT.md

---

## Executive Summary

This content plan addresses the documentation requirements for **BuildStreaM**, a new automation solution that extends Omnia's capabilities with catalog-driven, policy-enforced CI/CD workflows. BuildStreaM replaces manual image configuration with automated build → validate → promote pipelines.

**Key Customer Impact:** BuildStreaM fundamentally changes how customers deploy and manage Omnia clusters by introducing GitLab-based pipeline automation instead of manual playbook execution. This requires a separate documentation section that explains the new workflow while maintaining clear separation from traditional Omnia deployment methods.

---

## Content Requirements Overview

### Primary Documentation Sections

1. **BuildStreaM Overview** - High-level introduction to the new automation approach
2. **BuildStreaM Concepts** - Core architecture and workflow understanding  
3. **BuildStreaM Getting Started** - Initial setup and configuration
4. **BuildStreaM How-To Guides** - Step-by-step procedures for common tasks
5. **BuildStreaM Reference** - Configuration parameters and API documentation
6. **BuildStreaM Troubleshooting** - Common issues and resolution procedures

---

## Detailed Content Plan

### 1. BuildStreaM Overview

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Overview                                     |
| **Status**             | New Topic                                    |
| **Target Audience**    | Evaluator/Decision Maker, Platform Engineer/Cloud Architect |
| **Source Traceability**| HLD Section 2 (Introduction), Demo Transcription 0:19-21:45 |
| **RST File**           | `/buildstream/overview-buildstream.rst`      |
| **Content Type**       | `overview/`                                  |

**Customer Workflow Context:**
Customers evaluating BuildStreaM need to understand what this new automation approach offers compared to traditional Omnia deployment. They need to grasp the value proposition of catalog-driven pipelines and GitLab integration before investing in setup and configuration.

**Content Requirements:**
- **Prerequisite information:** Understanding of traditional Omnia deployment workflows
- **Key concepts:** Catalog-driven automation, stage-gated workflows, GitLab integration
- **Expected outcomes:** Faster deployment, reduced manual errors, consistent configurations
- **Important considerations:** Separate workflow from traditional Omnia, requires GitLab infrastructure

**Configuration Artifacts:**
- `buildstream_enabled` parameter in `omnia.yml`
- GitLab server host IP configuration
- Project name and visibility settings

**Cross-References:**
- :doc:`../concepts/buildstream-architecture`
- :doc:`../getting-started/buildstream-prerequisites`
- :doc:`../how-to/buildstream/enabling-buildstream`

**Build Agent Instructions:**
- Create new RST file following overview template structure
- Include comparison table: BuildStreaM vs Traditional Omnia deployment
- Add architecture diagram from HLD (Diagram-3-03)
- Include value proposition section with customer benefits
- Add "When to Use BuildStreaM" decision guide

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if additional demo transcripts needed for common mistakes
- [ ] Flag if performance benchmarks available
- [ ] Flag if security review documentation required
- [ ] Flag if SME validation required for comparison table

---

### 2. BuildStreaM Architecture Concepts

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept                                      |
| **Status**             | New Topic                                    |
| **Target Audience**    | Platform Engineer/Cloud Architect, Infrastructure/HPC Administrator |
| **Source Traceability**| HLD Section 3 (Solution Architecture), Diagrams 3-01, 3-02, 3-03 |
| **RST File**           | `/buildstream/concepts-buildstream-architecture.rst` |
| **Content Type**       | `concepts/`                                  |

**Customer Workflow Context:**
Platform engineers need to understand BuildStreaM's modular monolith architecture, component interactions, and data flow to integrate it with existing infrastructure and plan capacity requirements.

**Content Requirements:**
- **Prerequisite information:** Understanding of microservices vs monolith architectures, GitLab CI/CD concepts
- **Key concepts:** Modular monolith pattern, API Facade, Workflow Orchestrator, stage-gated flows
- **Expected outcomes:** Clear understanding of system boundaries and integration points
- **Important considerations:** Single deployable unit, OAuth 2.0 authentication, admission control

**Configuration Artifacts:**
- API endpoints: `/api/v1/jobs`, `/api/v1/auth/token`, `/register`
- OAuth 2.0 Client Credentials configuration
- Admission control parameters: `max_concurrent_builds`, `max_parallel_validations`

**Cross-References:**
- :doc:`../overview-buildstream`
- :doc:`../reference/buildstream-api-endpoints`
- :doc:`../how-to/buildstream/configuring-authentication`

**Build Agent Instructions:**
- Create concept topic explaining modular monolith architecture
- Include all three architecture diagrams from HLD with proper captions
- Explain component interactions using HLD Section 3.1 (Component Interactions)
- Detail security model (OAuth 2.0, API Facade protections)
- Add data flow explanation for build → validate → promote workflow

**Gap Analysis:**
- [x] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if performance testing results available
- [ ] Flag if integration examples with existing GitLab instances needed
- [ ] Flag if SME validation required for architecture explanations

---

### 3. BuildStreaM Catalog Management

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept                                      |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator, Platform Engineer/Cloud Architect |
| **Source Traceability**| HLD Section 1 (Glossary: Catalog), Demo Transcription 5:48-6:12 |
| **RST File**           | `/buildstream/concepts-buildstream-catalog.rst` |
| **Content Type**       | `concepts/`                                  |

**Customer Workflow Context:**
Customers need to understand the catalog as the single source of truth for defining roles, packages, architectures, and validation dependencies. This is fundamental to how BuildStreaM automates the entire build lifecycle.

**Content Requirements:**
- **Prerequisite information:** Understanding of YAML configuration, package management concepts
- **Key concepts:** Catalog as SSoT, roles, packages, validation dependencies, stage-gated enforcement
- **Expected outcomes:** Ability to create and modify catalog definitions for custom workflows
- **Important considerations:** Catalog changes trigger automatic pipeline execution, schema validation requirements

**Configuration Artifacts:**
- Catalog file structure (4000+ lines mentioned in demo)
- `gitlab.yaml` playbook for catalog upload
- Catalog validation schema requirements
- Pipeline trigger mechanisms

**Cross-References:**
- :doc:`../how-to/buildstream/managing-catalogs`
- :doc:`../reference/buildstream-catalog-schema`
- :doc:`../troubleshooting/buildstream/catalog-validation-errors`

**Build Agent Instructions:**
- Create concept topic explaining catalog-driven approach
- Explain catalog structure: function layers, package layers
- Detail how catalog changes trigger pipeline execution (Demo 11:08-11:40)
- Include catalog validation requirements and common schema errors
- Add example catalog snippet (not full 4000-line file)

**Gap Analysis:**
- [x] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if sample catalog file available for examples
- [ ] Flag if catalog validation error patterns documented
- [ ] Flag if performance impact of large catalogs known

---

### 4. Enabling BuildStreaM in Omnia

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator            |
| **Source Traceability**| Demo Transcription 8:43-9:15, 18:44-21:32 |
| **RST File**           | `/buildstream/how-to-buildstream-enabling-buildstream.rst` |
| **Content Type**       | `how-to/`                                    |

**Customer Workflow Context:**
Customers need to enable BuildStreaM in their existing Omnia deployment, which involves updating configuration files and running the prepare OEM playbook to set up the BuildStreaM infrastructure.

**Content Requirements:**
- **Prerequisite information:** Working Omnia control plane, GitLab server access, administrator privileges
- **Key concepts:** BuildStreaM configuration parameters, container setup, Postgres database
- **Expected outcomes:** BuildStreaM containers running, GitLab project created, initial catalog uploaded
- **Important considerations:** Postgres container for API transaction storage, separate from traditional workflow

**Configuration Artifacts:**
- `buildstream_enabled: true` in `omnia.yml`
- GitLab host IP configuration
- Project name and visibility (private/public)
- Main branch specification
- `gitlab.yaml` playbook execution

**Cross-References:**
- :doc:`../concepts-buildstream-architecture`
- :doc:`../getting-started-buildstream-prerequisites`
- :doc:`../how-to-buildstream-configuring-gitlab-integration`

**Build Agent Instructions:**
- Create step-by-step how-to guide for enabling BuildStreaM
- Include configuration file editing steps with exact parameter names
- Detail `prepare-oem` playbook execution and expected outcomes
- Explain container setup: BuildStreaM container, Postgres container, playbook watcher service
- Add verification steps to confirm successful setup

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if common setup errors documented
- [ ] Flag if container resource requirements known
- [ ] Flag if Postgres configuration details needed

---

### 5. Managing GitLab Integration

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator            |
| **Source Traceability**| Demo Transcription 4:04-5:20, 10:15-18:14 |
| **RST File**           | `/buildstream/how-to-buildstream-managing-gitlab-integration.rst` |
| **Content Type**       | `how-to/`                                    |

**Customer Workflow Context:**
Customers need to understand how BuildStreaM integrates with GitLab, including project creation, pipeline configuration, and monitoring pipeline execution stages.

**Content Requirements:**
- **Prerequisite information:** GitLab basics, CI/CD pipeline concepts, BuildStreaM enabled
- **Key concepts:** GitLab projects, pipeline stages, runners, catalog-driven triggers
- **Expected outcomes:** Ability to monitor pipelines, understand stage execution, troubleshoot failures
- **Important considerations:** Pipeline stages replace manual playbook execution, runners must be online

**Configuration Artifacts:**
- GitLab project settings (private/public)
- `.gitlab-ci.yml` pipeline definition file
- Pipeline stages: local repo, build image, discovery, authentication, registration
- GitLab runner configuration and status

**Cross-References:**
- :doc:`../concepts-buildstream-catalog`
- :doc:`../reference/buildstream-pipeline-stages`
- :doc:`../troubleshooting/buildstream/pipeline-failures`

**Build Agent Instructions:**
- Create how-to guide for GitLab integration management
- Explain project creation and configuration (Demo 4:04-5:20)
- Detail pipeline stages and their correspondence to traditional playbooks (Demo 7:14-7:54)
- Include pipeline monitoring procedures (Demo 10:15-12:56)
- Add runner status verification and troubleshooting

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if pipeline failure patterns documented
- [ ] Flag if runner configuration details needed
- [ ] Flag if performance metrics for pipelines available

---

### 6. Working with BuildStreaM Pipelines

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator            |
| **Source Traceability**| Demo Transcription 11:08-15:22 |
| **RST File**           | `/buildstream/how-to-buildstream-working-with-pipelines.rst` |
| **Content Type**       | `how-to/`                                    |

**Customer Workflow Context:**
Customers need to understand the day-to-day workflow of using BuildStreaM pipelines, including modifying catalogs, triggering pipeline execution, and monitoring results.

**Content Requirements:**
- **Prerequisite information:** GitLab basics, catalog understanding, BuildStreaM enabled
- **Key concepts:** Catalog-driven pipeline triggers, stage monitoring, manual verification
- **Expected outcomes:** Ability to modify catalogs, trigger pipelines, monitor execution, verify results
- **Important considerations:** Catalog changes auto-trigger pipelines, manual verification still required

**Configuration Artifacts:**
- Catalog file modification workflow
- Pipeline monitoring interface (GitLab pipelines/jobs)
- Stage status indicators (passed/failed)
- Manual verification procedures for completed deployments

**Cross-References:**
- :doc:`../concepts-buildstream-catalog`
- :doc:`../how-to-buildstream-managing-gitlab-integration`
- :doc:`../troubleshooting/buildstream/pipeline-stage-failures`

**Build Agent Instructions:**
- Create step-by-step pipeline workflow guide
- Explain catalog modification and commit process (Demo 11:08-11:40)
- Detail pipeline monitoring and stage status interpretation (Demo 12:19-13:00)
- Include manual verification procedures for successful deployments (Demo 15:02-15:22)
- Add decision points for when to intervene vs. when to let pipeline run

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if pipeline performance metrics available
- [ ] Flag if automated verification procedures documented
- [ ] Flag if rollback procedures needed

---

### 7. BuildStreaM Configuration Reference

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Reference                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator, Platform Engineer/Cloud Architect |
| **Source Traceability**| HLD Section 3.1 (Constraints), Demo Transcription 8:43-9:15 |
| **RST File**           | `/buildstream/reference-buildstream-configuration.rst` |
| **Content Type**       | `reference/`                                 |

**Customer Workflow Context:**
Administrators need a comprehensive reference for all BuildStreaM configuration parameters, their accepted values, defaults, and interdependencies.

**Content Requirements:**
- **Prerequisite information:** Understanding of YAML configuration, Omnia configuration files
- **Key concepts:** Configuration parameters, validation rules, admission control settings
- **Expected outcomes:** Complete reference for all BuildStreaM-specific configuration options
- **Important considerations:** Parameter dependencies, validation requirements, security implications

**Configuration Artifacts:**
- `buildstream_enabled` parameter
- GitLab integration parameters (host, project name, visibility, branch)
- Admission control parameters (`max_concurrent_builds`, `max_parallel_validations`)
- OAuth 2.0 configuration parameters
- API endpoint configuration

**Cross-References:**
- :doc:`../how-to-buildstream-enabling-buildstream`
- :doc:`../reference/omnia-yml` (main configuration reference)
- :doc:`../concepts-buildstream-architecture`

**Build Agent Instructions:**
- Create comprehensive configuration reference table
- Include parameter name, type, accepted values, defaults, and descriptions
- Add parameter dependency notes and validation requirements
- Include security considerations for sensitive parameters
- Add example configuration snippets for common scenarios

**Gap Analysis:**
- [ ] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if complete parameter specification available
- [ ] Flag if validation error messages documented
- [ ] Flag if performance impact of parameters known

---

### 8. BuildStreaM API Reference

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Reference                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Platform Engineer/Cloud Architect           |
| **Source Traceability**| HLD Section 2.1.1 (External API contract summary) |
| **RST File**           | `/buildstream/reference/buildstream-api.rst` |
| **Content Type**       | `reference/api/`                             |

**Customer Workflow Context:**
Platform engineers need complete API documentation for integrating BuildStreaM with external systems and automation tools.

**Content Requirements:**
- **Prerequisite information:** REST API concepts, OAuth 2.0 authentication
- **Key concepts:** API endpoints, request/response formats, authentication flow
- **Expected outcomes:** Complete API reference for external integrations
- **Important considerations:** Authentication requirements, rate limiting (admission control), error handling

**Configuration Artifacts:**
- Base URI: `https://<HOST_ADDRESS>:<PORT_NUM>/api/v1/`
- OAuth 2.0 endpoints: `POST /register`, `POST /auth/token`
- Job management endpoints: `POST /jobs`, `GET /jobs/{jobId}`, `DELETE /jobs/{jobId}`
- Stage endpoints: `POST /jobs/{jobId}/stages/*`
- Catalog endpoints: `GET /jobs/{jobId}/catalog/roles`

**Cross-References:**
- :doc:`../concepts-buildstream-architecture`
- :doc:`../how-to-buildstream-configuring-authentication`
- :doc:`../reference/buildstream-configuration`

**Build Agent Instructions:**
- Create comprehensive API reference following REST API documentation standards
- Document all endpoints from HLD Section 2.1.1 with request/response examples
- Include OAuth 2.0 authentication flow documentation
- Add error response codes and troubleshooting information
- Include rate limiting and admission control details

**Gap Analysis:**
- [ ] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if OpenAPI specification available
- [ ] Flag if API testing examples documented
- [ ] Flag if integration patterns with common tools needed

---

### 9. Troubleshooting BuildStreaM Pipeline Failures

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Troubleshooting                             |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator            |
| **Source Traceability**| Demo Transcription 12:56-13:16, 15:30-15:53 |
| **RST File**           | `/buildstream/troubleshooting-buildstream-pipeline-failures.rst` |
| **Content Type**       | `troubleshooting/`                           |

**Customer Workflow Context:**
Administrators need guidance on diagnosing and resolving pipeline failures, including identifying failed stages, reading error logs, and taking corrective action.

**Content Requirements:**
- **Prerequisite information:** BuildStreaM basics, GitLab interface familiarity
- **Key concepts:** Pipeline stages, failure identification, error analysis, recovery procedures
- **Expected outcomes:** Ability to troubleshoot common pipeline failures and take appropriate corrective action
- **Important considerations:** Different failure types require different resolution approaches

**Configuration Artifacts:**
- Pipeline stage failure indicators
- Error log locations and formats
- Common error messages and their meanings
- Recovery procedures for different failure types

**Cross-References:**
- :doc:`../how-to-buildstream-working-with-pipelines`
- :doc:`../concepts-buildstream-architecture`
- :doc:`../troubleshooting-buildstream-catalog-validation-errors`

**Build Agent Instructions:**
- Create troubleshooting guide organized by symptom/failure type
- Include step-by-step diagnostic procedures (Demo 12:56-13:16)
- Document common failure scenarios and resolution steps
- Add error message reference with explanations
- Include when to escalate vs. when to self-resolve

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if comprehensive error message catalog available
- [ ] Flag if escalation procedures documented
- [ ] Flag if failure rate statistics known

---

### 10. Troubleshooting BuildStreaM Catalog Validation Errors

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Troubleshooting                             |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator            |
| **Source Traceability**| HLD Section 3.1 (Data Governance: Schema conformance) |
| **RST File**           | `/buildstream/troubleshooting-buildstream-catalog-validation-errors.rst` |
| **Content Type**       | `troubleshooting/`                           |

**Customer Workflow Context:**
Administrators need help resolving catalog validation errors that prevent pipeline execution, including schema violations, missing required fields, and formatting issues.

**Content Requirements:**
- **Prerequisite information:** YAML syntax, catalog structure understanding
- **Key concepts:** Schema validation, catalog structure, error message interpretation
- **Expected outcomes:** Ability to identify and fix common catalog validation errors
- **Important considerations:** Schema validation is strict; failures block pipeline execution

**Configuration Artifacts:**
- Catalog schema requirements
- Common validation error messages
- YAML syntax requirements
- Catalog structure validation rules

**Cross-References:**
- :doc:`../concepts-buildstream-catalog`
- :doc:`../reference-buildstream-catalog-schema`
- :doc:`../how-to-buildstream-managing-catalogs`

**Build Agent Instructions:**
- Create troubleshooting guide focused on catalog validation issues
- Document common schema validation errors and fixes
- Include YAML syntax troubleshooting
- Add catalog structure validation procedures
- Include examples of valid vs. invalid catalog entries

**Gap Analysis:**
- [x] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if catalog schema documentation available
- [ ] Flag if validation error message catalog exists
- [ ] Flag if catalog testing tools available

---

## Implementation Priority

### High Priority (Must Have for Release)
1. **BuildStreaM Overview** - Customer understanding and adoption
2. **Enabling BuildStreaM in Omnia** - Core setup procedure
3. **BuildStreaM Architecture Concepts** - Technical understanding
4. **Managing GitLab Integration** - Daily operations
5. **Working with BuildStreaM Pipelines** - Core workflow
6. **Troubleshooting Pipeline Failures** - Issue resolution

### Medium Priority (Should Have for Release)
7. **BuildStreaM Catalog Management** - Advanced configuration
8. **BuildStreaM Configuration Reference** - Complete reference
9. **Troubleshooting Catalog Validation Errors** - Specific issues

### Low Priority (Nice to Have for Release)
10. **BuildStreaM API Reference** - Developer/integration focus

---

## Build Agent Implementation Notes

### Directory Structure
Create dedicated `/buildstream/` directory with:
- `index.rst` - Parent index file
- `overview-buildstream.rst` - Overview topic
- `concepts-*.rst` - Concept topics
- `how-to-*.rst` - Procedure topics  
- `reference-*.rst` - Reference topics
- `troubleshooting-*.rst` - Troubleshooting topics

### Cross-Reference Strategy
- Maintain clear separation from traditional Omnia documentation
- Use cross-references to avoid content duplication
- Reference existing Omnia concepts where applicable
- Create BuildStreaM-specific concepts for new workflows

### Content Development Approach
1. Start with high-priority overview and setup topics
2. Develop core workflow procedures (GitLab integration, pipelines)
3. Add reference materials and troubleshooting as needed
4. Review for consistency with existing Omnia documentation style

### Quality Assurance
- Apply SKILL_CHECK.md validation procedures
- Ensure all RST files follow template structure
- Verify all cross-references are valid
- Test all procedures against actual BuildStreaM behavior

---

## Summary

This content plan provides a comprehensive approach to documenting BuildStreaM, addressing the fundamental shift from manual Omnia deployment to automated, catalog-driven pipelines. The plan prioritizes customer understanding and successful adoption while maintaining technical accuracy and operational guidance.

The separate BuildStreaM section ensures clear distinction from traditional workflows while leveraging existing Omnia documentation patterns and cross-references where appropriate.
