# BuildStreaM Documentation Content Plan

## Overview
This content plan addresses the BuildStreaM build and validation automation solution documentation. The plan is derived from the BuildStreaM High-Level Design (HLD) document and detailed demo transcription to create comprehensive customer-facing documentation for Infrastructure/HPC Administrators and Platform Engineers.

---

### BuildStreaM Overview

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept                                      |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator, Platform Engineer/Cloud Architect |
| **Source Traceability**| HLD Section 3, Demo Transcription Lines 300-350 |
| **RST File**           | /docs/buildstream/concept-overview.rst |
| **Content Type**       | concepts/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.md` (Sections 3.1-3.3, 2.1.1)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.md` (Lines 300-350)

**Overview:**
Provide a high-level overview about BuildStreaM, highlighting level workflows, how it works, and how it can be used. This topic should be concise and easy to understand. Note that promote and validate images are not yet implemented.

**Content Requirements:**
- High-level explanation of BuildStreaM purpose and functionality
- Key workflows: catalog-driven builds, automated pipeline execution
- How it integrates with Omnia for build automation
- Current limitations: promote and validate images not implemented
- Expected outcomes: Understanding BuildStreaM capabilities and usage scenarios
- Important considerations: Single-user limitation, external dependencies

**Configuration Artifacts:**
- BuildStreaM purpose and functionality overview
- Pipeline workflow stages (high-level)
- Integration with Omnia (high-level)
- Catalog file structure overview

**Cross-References:**
- Prepare BuildStreaM Configuration and Pipeline
- GitLab Deployment
- Update Catalog and Check Pipeline

**Build Agent Instructions:**
- Create new RST file with concept topic structure
- Include high-level workflow information (no architectural diagrams)
- Add admonitions: note about current limitations (promote/validate not implemented)
- Cross-reference to configuration procedures
- SME validation required for technical accuracy
- AI_REVIEW: Verify overview matches practical workflows

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [x] Performance characteristics covered
- [ ] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Flag if additional demo transcripts needed
- [x] HLD provides comprehensive technical details
- [ ] Flag if SME interviews required for edge cases
- [ ] Flag if user feedback collection needed
- [x] Demo transcription provides practical context

---

### Prepare BuildStreaM Configuration and Pipeline

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| HLD Section 2.1, Demo Transcription 312-350 |
| **RST File**           | /docs/buildstream/how-to-prepare-buildstream.rst |
| **Content Type**       | how-to/buildstream/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.md` (Section 2.1 - Release 1.0 Features)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.md` (Lines 312-350)
- Omnia Documentation: Step 4: Provide Required Credentials for omnia
- Omnia Documentation: Step 5: Prepare the OIM
- Omnia Documentation: Step 2: Create Mapping File with Node information

**Customer Workflow Context:**
Comprehensive procedure for HPC administrators to prepare BuildStreaM configuration and pipeline. This covers prerequisites, enabling BuildStreaM, providing credentials, and ensuring PXE mapping is properly configured.

**Content Requirements:**
- **Subtopic 1: Prerequisites** - System requirements, dependencies, and pre-configuration steps
- **Subtopic 2: Enable BuildStreaM** - Configure build_stream_config and run prepare_oim.yaml playbook (Reference: Step 5: Prepare the OIM)
- **Subtopic 3: Provide Credentials** - Configure BuildStreaM credentials (Reference: Step 4: Provide Required Credentials for omnia)
- **Subtopic 4: PXE Mapping** - Ensure PXE mapping file is updated (Reference: Step 2: Create Mapping File with Node information)
- **GitLab Configuration Setup**: Configure gitlab_config.yml file located at /opt/omnia/input/project_default/gitlab_config.yml
- Expected outcomes: BuildStreaM services running and ready for GitLab deployment
- Critical warnings: Single-user limitation, external dependency requirements

**Configuration Artifacts:**
- build_stream_config.yaml configuration parameters
- prepare_oim.yaml playbook execution
- BuildStreaM credential configuration
- PXE mapping file updates
- gitlab_config.yml configuration with project settings:
  - gitlab_project_name: "omnia-catalog"
  - gitlab_project_visibility: "private" 
  - gitlab_default_branch: "main"
- Service validation commands
- Access method: ssh omnia_core to access configuration files

**Cross-References:**
- BuildStreaM Overview
- GitLab Deployment
- Update Catalog and Check Pipeline
- Omnia Installation Guide (referenced steps)

**Build Agent Instructions:**
- Create new RST file with procedure format
- Include all 4 subtopics with detailed steps
- Add admonitions: important for prerequisites, warning for credential security
- Include code blocks for configuration examples
- Cross-reference to Omnia documentation steps
- SME validation required for configuration accuracy
- AI_REVIEW: Verify configuration steps match HLD and demo transcription

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] HLD provides setup requirements
- [x] Demo transcription shows practical context
- [ ] Flag if SME interviews required for setup details
- [ ] Flag if user feedback collection needed
- [x] Unit tests provide validation scenarios

---

### GitLab Deployment

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| Demo Transcription 73-200, 378-450 |
| **RST File**           | /docs/buildstream/how-to-gitlab-deployment.rst |
| **Content Type**       | how-to/buildstream/ |

**Source File Locations:**
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.md` (Lines 73-200, 378-450)
- HLD: `docs/SOURCE MATERIALS/hld.md` (Section 2.1.1 - External API Contract)

**Customer Workflow Context:**
Guide for deploying GitLab as part of BuildStreaM integration. This covers GitLab installation, configuration, project creation, pipeline setup, and verification of runner status and job execution.

**Content Requirements:**
- **Prerequisites**: prepare.yaml playbook must be completed first
- **GitLab Installation**: Deploy GitLab on server using ansible-playbook gitlab.yml for fresh install
- **GitLab Configuration**: Configure gitlab_config.yml with project settings (project name, visibility, default branch)
- **Project Creation**: GitLab project and pipeline creation with repository structure
- **Pipeline Setup**: .gitlab-ci.yml pipeline file that invokes BuildStreaM REST APIs chronologically from GitLab runner
- **Repository Files**: README.MD and catalog_rhel.json files in the project
- **Runner Verification**: Verify GitLab runner is running as Podman container
- **Job Monitoring**: Verify all jobs are running through Build > Pipeline and Build > Jobs
- **Expected outcomes**: Functional GitLab instance with BuildStreaM integration ready
- **Important considerations**: Omnia does not support existing customer GitLab

**Configuration Artifacts:**
- gitlab_config.yml configuration file with project settings:
  - gitlab_project_name: "omnia-catalog"
  - gitlab_project_visibility: "private"
  - gitlab_default_branch: "main"
- GitLab installation command: cd /omnia/build_stream/gitlab && ansible-playbook gitlab.yml
- .gitlab-ci.yml pipeline file for BuildStreaM REST API invocation
- GitLab runner verification (Settings > CI/CD > Runners > Running Always > Podman Container)
- Job monitoring locations (Build > Pipeline, Build > Jobs)

**Cross-References:**
- BuildStreaM Overview
- Prepare BuildStreaM Configuration and Pipeline
- Update Catalog and Check Pipeline

**Build Agent Instructions:**
- Create new RST file with procedure format
- Document GitLab deployment workflow
- Include runner verification steps
- Add admonitions: warning about GitLab support limitations
- Include code blocks for verification commands
- Cross-reference to related procedures
- SME validation required for deployment accuracy
- AI_REVIEW: Verify deployment steps match demo transcription

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Demo transcription provides comprehensive GitLab workflow
- [x] HLD provides integration framework
- [ ] Flag if SME interviews required for advanced GitLab features
- [ ] Flag if user feedback collection needed
- [x] Unit tests provide validation scenarios

---

### Update Catalog and Check Pipeline

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| Demo Transcription 388-450 |
| **RST File**           | /docs/buildstream/how-to-update-catalog-pipeline.rst |
| **Content Type**       | how-to/buildstream/ |

**Source File Locations:**
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.md` (Lines 388-450)
- HLD: `docs/SOURCE MATERIALS/hld.md` (Section 3.1.4 - Functional Scope)

**Customer Workflow Context:**
Guide for updating BuildStreaM catalogs and monitoring pipeline execution. This covers catalog modifications, pipeline triggering, and verification of pipeline status through GitLab interface.

**Content Requirements:**
- **Catalog Update**: Modify catalog_rhel.json or other catalog files in GitLab repository
- **Pipeline Triggering**: Automatic pipeline triggering based on catalog changes
- **Pipeline Monitoring**: Monitor pipeline execution through GitLab Build > Pipeline interface
- **Job Verification**: Verify all jobs are running through Build > Jobs interface
- **Repository Access**: Access project files through Check and Code > Repository in GitLab
- **Expected outcomes**: Functional pipeline execution with catalog-driven builds
- **Important considerations**: Pipeline stages, error handling, and troubleshooting

**Configuration Artifacts:**
- Catalog update procedures for catalog_rhel.json
- Pipeline monitoring through GitLab Build > Pipeline interface
- Job verification through GitLab Build > Jobs interface
- Repository file access through GitLab Check > Code > Repository
- Status verification commands and procedures
- Error handling and troubleshooting steps

**Cross-References:**
- BuildStreaM Overview
- Prepare BuildStreaM Configuration and Pipeline
- GitLab Deployment

**Build Agent Instructions:**
- Create new RST file with procedure format
- Document catalog update workflow
- Include pipeline monitoring steps
- Add admonitions: tip about pipeline monitoring, warning about error handling
- Include code blocks for verification commands
- Cross-reference to related procedures
- SME validation required for pipeline accuracy
- AI_REVIEW: Verify pipeline procedures match demo transcription

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Demo transcription provides comprehensive GitLab workflow
- [x] HLD provides integration framework
- [ ] Flag if SME interviews required for advanced GitLab features
- [ ] Flag if user feedback collection needed
- [x] Unit tests provide validation scenarios

---

## Summary and Implementation Priority

### High Priority Topics (Implement First)
1. **BuildStreaM Overview** - Foundational concept understanding
2. **Prepare BuildStreaM Configuration and Pipeline** - Primary setup and configuration guide  
3. **GitLab Deployment** - Critical deployment workflow
4. **Update Catalog and Check Pipeline** - Essential operational procedure

### Cross-Reference Strategy
- All procedural guides should reference the BuildStreaM Overview
- GitLab Deployment should reference the configuration guide
- Update Catalog topic should reference all previous topics
- Consider creating a BuildStreaM index page to tie all topics together

### SME Validation Requirements
- Technical accuracy of overview descriptions
- Configuration procedure verification
- GitLab deployment workflow verification
- Pipeline update and monitoring procedures
- Integration workflow verification

### Content Gaps Identified
- Performance characteristics during builds (build times, resource usage)
- Advanced integration examples with CI/CD systems
- Detailed security considerations for API access
- Common mistakes and gotchas from field experience
- Advanced troubleshooting scenarios
- Real-world catalog examples

### Special Considerations
- BuildStreaM represents a separate workflow from traditional Omnia deployment
- Documentation should be organized as a separate section to avoid confusion
- GitLab deployment is a critical component and should be thoroughly documented
- Pipeline monitoring and error handling are essential customer workflows
- Catalog management is central to BuildStreaM functionality
- **Important**: Omnia does not support existing customer GitLab - only new GitLab deployments
- **Note**: Promote and validate images are not yet implemented


### High Priority Topics (Implement First)
1. **BuildStreaM Overview** - Foundational concept understanding
2. **Prepare BuildStreaM Configuration and Pipeline** - Primary setup and configuration guide  
3. **GitLab Deployment** - Critical deployment workflow
4. **Update Catalog and Check Pipeline** - Essential operational procedure

### Cross-Reference Strategy
- All procedural guides should reference the BuildStreaM Overview
- GitLab Deployment should reference the configuration guide
- Update Catalog topic should reference all previous topics
- Consider creating a BuildStreaM index page to tie all topics together

### SME Validation Requirements
- Technical accuracy of overview descriptions
- Configuration procedure verification
- GitLab deployment workflow verification
- Pipeline update and monitoring procedures
- Integration workflow verification

### Content Gaps Identified
- Performance characteristics during builds (build times, resource usage)
- Advanced integration examples with CI/CD systems
- Detailed security considerations for API access
- Common mistakes and gotchas from field experience
- Advanced troubleshooting scenarios
- Real-world catalog examples (4000-line catalog mentioned but not available)

This content plan provides a comprehensive foundation for documenting BuildStreaM, addressing all major customer workflows and operational requirements identified in the source materials.
