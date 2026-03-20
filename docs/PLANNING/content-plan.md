# Omnia Documentation Content Plan
# Generated: 2026-03-20
# Phase: COLLECT
# Source Documents: HLD (BuildStreaM), Demo Transcription

---

## Executive Summary

This content plan addresses the documentation needs for **BuildStreaM**, a catalog-driven automation solution for image lifecycle management that complements Omnia's existing capabilities.

The plan is structured to serve the primary target audience: Infrastructure/HPC Administrators, following the updated skill document requirements that support only Concept and How-To content types, with no separate getting-started topics.

---

## BuildStreaM Documentation Topics

### BuildStreaM Overview and Concepts

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept                                      |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| HLD Sections 1-3, Demo Transcription 8:17-8:43 |
| **RST File**           | `/docs/buildstream/concept-overview.rst` |
| **Content Type**       | Feature-specific structure                    |

**Customer Workflow Context:**
Administrators need to understand what BuildStreaM is, why it exists, and how it complements Omnia's existing capabilities. This addresses the "what is this and should I care?" question for administrators evaluating BuildStreaM adoption.

**Content Requirements:**
- Clear definition of BuildStreaM and its relationship to Omnia
- Key benefits: catalog-driven approach, CI/CD integration, compliance gates
- Architecture overview showing modular monolith design
- Primary workflow: ParseCatalog → GenerateInputFiles → PrepareRepos → BuildImage → ValidateImage → ValidateImageOnTest → Promote
- Multi-architecture support (x86_64, aarch64)
- OAuth 2.0 Client Credentials authentication model
- BuildStreaM REST API overview and integration points

**Configuration Artifacts:**
- Base URI: `https://<HOST_ADDRESS>:<PORT_NUM>/api/v1/`
- OAuth endpoints: `/register`, `/auth/token`
- Core functional endpoints (13 endpoints listed in HLD)
- BuildStreaM container requirements
- PostgreSQL database requirements

**Cross-References:**
- BuildStreaM Setup Guide
- BuildStreaM GitLab Deployment Guide
- BuildStreaM Catalog Configuration Guide

**Build Agent Instructions:**
- Create new concept RST file following SKILL_BUILD.md example structure
- Use the BuildStreaM concept example from SKILL_BUILD.md §7.1 as template
- Include architecture overview and key benefits
- Add REST API overview section
- Include cross-references to related how-to topics
- Flag for SME validation of technical accuracy

**File Path Decision:**
**Decision**: Feature-specific structure
**Rationale**: 
- [X] This is part of a major feature (BuildStreaM)
- [ ] This is general content not tied to a major feature
- [X] Feature-specific structure provides better user navigation and maintenance
- [ ] General structure is more appropriate for standalone content
**Resulting File Path**: `/docs/buildstream/concept-overview.rst`

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
- [ ] Flag if additional demo transcripts needed for real-world scenarios
- [ ] Flag if additional unit tests needed for common issues
- [ ] Flag if SME interviews required for performance characteristics
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required for API details
- [ ] Flag if engineering notes clarification required

---

### BuildStreaM Setup and Getting Started

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | How-to                                       |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| Demo Transcription 8:43-11:24, HLD Section 3 |
| **RST File**           | `/docs/buildstream/how-to-setup.rst` |
| **Content Type**       | Feature-specific structure                    |

**Customer Workflow Context:**
Administrators need step-by-step instructions to enable and configure BuildStreaM in their Omnia environment, from initial configuration through first pipeline execution. This integrates getting-started content directly into the setup procedure.

**Content Requirements:**
- Prerequisites: Omnia 2.1 core container up and running
- Step 1: Enable BuildStreaM in omnia.yml configuration
- Step 2: Run prepare-oem playbook to create BuildStreaM container and Postgres
- Step 3: Configure GitLab integration (gitlab_host, project_name, private/public, main_branch)
- Step 4: Run gitlab.yaml playbook to install GitLab instance
- Step 5: Verify GitLab project creation and pipeline setup
- Step 6: Access default catalog template in GitLab code repository
- Step 7: Modify catalog to trigger pipeline
- Verification steps after each major operation

**Configuration Artifacts:**
- `omnia.yml` - BuildStreaM configuration section
- `gitlab.yaml` - GitLab installation playbook
- GitLab variables: gitlab_host, project_name, visibility, main_branch
- Default catalog file location in GitLab
- BuildStreaM container configuration parameters

**Cross-References:**
- BuildStreaM Overview
- BuildStreaM GitLab Deployment Guide
- BuildStreaM Catalog Configuration Guide

**Build Agent Instructions:**
- Create new how-to RST file following SKILL_BUILD.md step writing rules
- Use numbered steps with imperative verbs
- Include verification step after main procedure
- Use `.. code-block:: bash` for all commands
- Include prerequisite checklist
- Add expected results and next steps
- Follow the BuildStreaM GitLab deployment example structure from SKILL_BUILD.md §7.1
- Integrate getting-started content directly into setup procedure

**File Path Decision:**
**Decision**: Feature-specific structure
**Rationale**: 
- [X] This is part of a major feature (BuildStreaM)
- [ ] This is general content not tied to a major feature
- [X] Feature-specific structure provides better user navigation and maintenance
- [ ] General structure is more appropriate for standalone content
**Resulting File Path**: `/docs/buildstream/how-to-setup.rst`

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
- [x] Demo transcripts provide workflow details
- [ ] Flag if additional unit tests needed for edge cases
- [ ] Flag if SME interviews required for common mistakes
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required for container requirements
- [ ] Flag if engineering notes clarification required

---

### BuildStreaM GitLab Deployment Guide

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | How-to                                       |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| Demo Transcription 4:40-8:32, HLD Section 3 |
| **RST File**           | `/docs/buildstream/how-to-gitlab-deployment.rst` |
| **Content Type**       | Feature-specific structure                    |

**Customer Workflow Context:**
Administrators need detailed instructions to deploy GitLab as the automation engine for BuildStreaM, including installation, project setup, runner verification, and service validation.

**Content Requirements:**
- Prerequisites: BuildStreaM container, PostgreSQL container, Playbook Watcher service
- Step 1: SSH to omnia_core container
- Step 2: Update gitlab_config.yml file
- Step 3: Navigate to GitLab directory
- Step 4: Run gitlab.yml playbook
- Step 5: Download and import certificate to browser
- Step 6: Verify GitLab project access
- Step 7: Verify runner status through GitLab web interface
- Expected results and next steps

**Configuration Artifacts:**
- `/opt/omnia/input/project_default/gitlab_config.yml`
- `/omnia/gitlab/gitlab.yml` playbook
- GitLab project structure files: README.MD, catalog_rhel.json, .gitlab-ci.yml
- Certificate location: `/root/gitlab-certs/ca.crt`
- GitLab runner verification steps

**Cross-References:**
- BuildStreaM Overview
- BuildStreaM Setup Guide
- BuildStreaM Catalog Configuration Guide

**Build Agent Instructions:**
- Create new how-to RST file using the exact example from SKILL_BUILD.md §7.1
- Follow the step-by-step structure with verification
- Include all code blocks with proper language specification
- Use the GitLab configuration table reference
- Include the BuildStream project image
- Add important note about dedicated GitLab instance
- Follow all step writing rules from SKILL_BUILD.md §5.3

**File Path Decision:**
**Decision**: Feature-specific structure
**Rationale**: 
- [X] This is part of a major feature (BuildStreaM)
- [ ] This is general content not tied to a major feature
- [X] Feature-specific structure provides better user navigation and maintenance
- [ ] General structure is more appropriate for standalone content
**Resulting File Path**: `/docs/buildstream/how-to-gitlab-deployment.rst`

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Demo transcripts provide complete workflow
- [ ] Flag if additional unit tests needed for verification steps
- [ ] Flag if SME interviews required for performance considerations
- [ ] Flag if user feedback collection needed
- [x] HLD provides architecture context
- [x] Engineering notes provide configuration details

---

### BuildStreaM Catalog Configuration Guide

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | How-to                                       |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| Demo Transcription 5:48-6:12, HLD Section 2 |
| **RST File**           | `/docs/buildstream/how-to-catalog-configuration.rst` |
| **Content Type**       | Feature-specific structure                    |

**Customer Workflow Context:**
Administrators need to understand how to configure the BuildStreaM catalog to define their software packages, roles, and validation dependencies for automated image building.

**Content Requirements:**
- Prerequisites: GitLab deployment complete, access to GitLab project
- Step 1: Access GitLab project code repository
- Step 2: Locate and examine default catalog file
- Step 3: Understand catalog structure (functional layers and package layers)
- Step 4: Modify role definitions (OS + drivers + cluster stack + validation suites)
- Step 5: Update package specifications (versioned software components)
- Step 6: Configure validation dependency declarations
- Step 7: Save changes to trigger pipeline
- Step 8: Verify pipeline execution

**Configuration Artifacts:**
- Catalog file structure (JSON format)
- Role definitions with package dependencies
- Package version specifications
- Validation dependency syntax
- Catalog automation script references
- Pipeline trigger mechanisms

**Cross-References:**
- BuildStreaM Overview
- BuildStreaM GitLab Deployment Guide
- BuildStreaM Setup Guide

**Build Agent Instructions:**
- Create new how-to RST file following SKILL_BUILD.md conventions
- Include step-by-step catalog modification process
- Use numbered steps with imperative verbs
- Include verification of pipeline triggering
- Add sample catalog structure explanations
- Include expected results and next steps
- Use `.. code-block:: json` for catalog examples

**File Path Decision:**
**Decision**: Feature-specific structure
**Rationale**: 
- [X] This is part of a major feature (BuildStreaM)
- [ ] This is general content not tied to a major feature
- [X] Feature-specific structure provides better user navigation and maintenance
- [ ] General structure is more appropriate for standalone content
**Resulting File Path**: `/docs/buildstream/how-to-catalog-configuration.rst`

**Gap Analysis:**
- [x] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Demo transcripts provide catalog context
- [ ] Flag if additional unit tests needed for validation examples
- [ ] Flag if SME interviews required for common configuration errors
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required for catalog schema
- [ ] Flag if engineering notes clarification required

---

### BuildStreaM Catalog Update and Pipeline Execution

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | How-to                                       |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| Demo Transcription 10:50-11:24               |
| **RST File**           | `/docs/buildstream/how-to-catalog-pipeline-update.rst` |
| **Content Type**       | Feature-specific structure                    |

**Customer Workflow Context:**
Administrators need to understand how to update the BuildStreaM catalog and automatically trigger pipeline execution for image building and deployment.

**Content Requirements:**
- Prerequisites: Catalog configuration complete, GitLab access
- Step 1: Navigate to GitLab code repository
- Step 2: Locate catalog file in project
- Step 3: Make desired changes to catalog configuration
- Step 4: Commit changes to GitLab repository
- Step 5: Verify automatic pipeline triggering
- Step 6: Monitor pipeline execution progress
- Step 7: Verify build completion and image availability
- Step 8: Troubleshoot common pipeline issues

**Configuration Artifacts:**
- GitLab repository access methods
- Catalog file modification procedures
- Pipeline monitoring interface
- Build verification steps
- Common pipeline error resolutions

**Cross-References:**
- BuildStreaM Catalog Configuration Guide
- BuildStreaM GitLab Deployment Guide
- BuildStreaM Overview

**Build Agent Instructions:**
- Create new how-to RST file following SKILL_BUILD.md step writing rules
- Include verification steps for pipeline execution
- Use numbered steps with imperative verbs
- Include expected results and troubleshooting information
- Add next steps for image deployment
- Use `.. code-block:: bash` for GitLab commands

**File Path Decision:**
**Decision**: Feature-specific structure
**Rationale**: 
- [X] This is part of a major feature (BuildStreaM)
- [ ] This is general content not tied to a major feature
- [X] Feature-specific structure provides better user navigation and maintenance
- [ ] General structure is more appropriate for standalone content
**Resulting File Path**: `/docs/buildstream/how-to-catalog-pipeline-update.rst`

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
- [x] Demo transcripts provide complete workflow
- [ ] Flag if additional unit tests needed for error scenarios
- [ ] Flag if SME interviews required for common issues
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required for pipeline mechanics
- [ ] Flag if engineering notes clarification required

---

## Implementation Priority and Dependencies

### High Priority (Phase 1)
1. **BuildStreaM Overview** - Foundation for all other BuildStreaM content
2. **BuildStreaM Setup Guide** - Critical for customer adoption (includes getting-started)
3. **BuildStreaM GitLab Deployment Guide** - Essential for BuildStreaM functionality
4. **BuildStreaM Catalog Configuration Guide** - Key for customer customization

### Medium Priority (Phase 2)
1. **BuildStreaM Catalog Update and Pipeline Execution** - Advanced operational content

### Dependencies
- BuildStreaM content depends on having a working BuildStreaM installation for validation
- GitLab deployment content requires access to BuildStreaM test environment
- All content requires SME review before publication
- Content must follow updated SKILL_BUILD.md conventions (Concept and How-To only)
- No separate getting-started topics - integrated into setup procedures

---

## Cross-Reference Strategy

### BuildStreaM Content Network
```
BuildStreaM Overview
├── Setup Guide (includes getting-started)
├── GitLab Deployment Guide
├── Catalog Configuration Guide
└── Catalog Update and Pipeline Execution
```

### Integration Points
- BuildStreaM Setup Guide references Omnia installation prerequisites
- GitLab Deployment Guide includes integration examples with external CI/CD systems
- All BuildStreaM content references existing Omnia infrastructure concepts
- Catalog Configuration references BuildStreaM API for automation

---

## Quality Assurance Requirements

### SME Review Required
All content requires SME review before publication, with special attention to:
- BuildStreaM architecture and API accuracy
- GitLab deployment procedures and configuration
- Catalog schema and pipeline mechanics
- Integration examples and troubleshooting scenarios

### Validation Requirements
- BuildStreaM procedures must be validated against working BuildStreaM installation
- GitLab deployment steps must be tested in test environment
- All configuration examples must be syntax-checked
- Pipeline execution examples must be verified

### User Testing
- Setup guides should be tested by non-expert users
- GitLab deployment scenarios should be validated with real installations
- Catalog configuration examples should be tested with common use cases

---

## Success Metrics

### Documentation Quality Metrics
- All prerequisite checklists are complete and accurate
- All command examples are syntactically correct and tested
- All cross-references resolve to valid content
- All content follows updated SKILL_BUILD.md conventions

### Customer Success Metrics
- Customers can successfully enable BuildStreaM without additional support
- Administrators can deploy GitLab for BuildStreaM without issues
- Catalog configuration workflows are intuitive and error-free
- Faster time-to-first-success for new BuildStreaM adopters

### Operational Metrics
- Reduction in support tickets for documented BuildStreaM scenarios
- Higher BuildStreaM adoption rates
- Improved customer satisfaction with documentation quality
- Fewer configuration errors in BuildStreaM deployments

---

## Conclusion

This content plan provides a comprehensive roadmap for creating customer-focused documentation for BuildStreaM using the updated skill document requirements. The plan addresses the needs of the primary target audience (Infrastructure/HPC Administrators) while ensuring technical accuracy and practical usability.

The plan has been updated to reflect the simplified content structure (Concept and How-To only) and follows the new examples and conventions defined in SKILL_BUILD.md. All topics are designed to be self-contained and ready for the Build Agent to implement in the BUILD phase.

**Key Changes from Previous Version:**
- No separate getting-started topics - integrated into setup procedures
- All content uses feature-specific structure (`/docs/buildstream/`)
- Updated file naming conventions to match skill document requirements
- Enhanced content organization guidelines followed

The Build Agent should use this plan as the primary input for the BUILD phase, creating each topic according to the specifications provided and following the updated skill document requirements.
