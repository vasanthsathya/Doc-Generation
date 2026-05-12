# BuildStream Release 2 Documentation Gap Analysis and Content Plan

**Phase:** COLLECT - Information gathering and planning  
**Skill Document:** .windsurf\skills\skill-collect-json\skill_collect-json.md  
**Source Specifications:** BuildStream BSpec v2.0, Functional Spec v1.1, Engineering Spec (HLD) v1.3, Component Specs  
**Capability ID:** 16427  
**Capability Name:** NERSC Automated Tools NRE Milestone 4  
**Generated:** 2026-05-11

---

## Executive Summary

This document provides a gap analysis between existing BuildStream documentation (Release 1) and the new BuildStream Release 2 specifications, followed by a targeted content plan to address only the NEW and CHANGED features.

**Key Finding:** The existing documentation covers BuildStream Release 1 (monolithic pipeline), while the new specifications describe BuildStream Release 2 (three-pipeline architecture with significant API and architectural enhancements). This represents a major architectural evolution.

---

## Existing BuildStream Documentation (Release 1)

### Current Documentation Structure
Located in: `docs/source/Buildstream/`

| File | Content | Status |
|------|---------|--------|
| `index.rst` | Overview and toctree | Keep, needs update for Release 2 |
| `omnia_startup_buildstream.rst` | Omnia core container deployment | Keep (no changes needed) |
| `composable_roles_buildstream.rst` | Composable roles | Keep (no changes needed) |
| `prepare_oim_buildstream.rst` | OIM preparation for BuildStream | **Update** for Release 2 changes |
| `how-to-gitlab-deployment.rst` | GitLab deployment | **Update** for Release 2 pipeline architecture |
| `how-to-update-catalog-pipeline.rst` | Catalog update and pipeline execution | **Update** for Release 2 pipeline changes |
| `set_pxe_boot_order_buildstream.rst` | PXE boot setup | Keep (may need minor updates) |
| `buildstream_telemetry_1.rst` | Telemetry | Keep (no changes needed) |
| `buildstream_verify_telmetry_1.rst` | Telemetry verification | Keep (no changes needed) |
| `buildstream_tables.rst` | Configuration tables | **Update** for new Release 2 parameters |
| `buildstream_troubleshooting.rst` | Troubleshooting | **Update** for Release 2 error codes and scenarios |

### What Release 1 Documentation Covers
- Basic BuildStream setup and installation
- Monolithic GitLab CI/CD pipeline
- Catalog-driven image building
- Basic deployment workflow
- PXE boot configuration
- Telemetry setup
- Basic troubleshooting for Release 1 pipeline stages

---

## BuildStream Release 2 - New and Changed Features

### Major Architectural Changes

| Feature | Release 1 | Release 2 | Impact |
|---------|-----------|-----------|--------|
| **Pipeline Architecture** | Monolithic single pipeline | Three-pipeline architecture (Build, Deploy & Validate, CleanUp) | Major - requires new documentation |
| **Job Lifecycle** | Simple job tracking | Job/Image Group lifecycle with state machines | Major - requires new documentation |
| **API Surface** | Limited API endpoints | Comprehensive REST API (6+ new endpoints) | Major - requires new API documentation |
| **Authentication** | Basic auth | OAuth 2.0 with JWT tokens | Major - requires new authentication documentation |
| **Resume & Retry** | Not available | Intelligent resume and retry capabilities | Major - requires new documentation |
| **Database Schema** | Simple schema | Enhanced schema with jobs, image_groups, images, job_stages tables | Minor - internal, may need config doc updates |
| **Image Management** | Basic tracking | Image Group management with constituent images | Major - requires new documentation |
| **Cleanup** | Manual only | Automated cleanup + manual CleanUp API | Minor - requires update to existing cleanup docs |

### New REST APIs (Release 2)
- `PUT /api/v1/jobs/{job_id}/upload` - Generic file upload
- `GET /api/v1/images` - List built Image Groups with constituent images
- `POST /api/v1/jobs/{job_id}/stages/deploy` - Deploy API
- `POST /api/v1/jobs/{job_id}/stages/restart` - PXE boot with node diff handling
- `POST /api/v1/jobs/{job_id}/stages/validate` - Validation via Molecule
- `DELETE /api/v1/jobs/{job_id}` - Hard delete with cleanup

### New Capabilities
- Image Group lifecycle management (BUILT → DEPLOYING → DEPLOYED → RESTARTING → RESTARTED → VALIDATING → PASSED/FAILED → CLEANED)
- Constituent images per functional role
- Resume & Retry with intelligent stage guards
- Automated cleanup cron job
- Image retention limits
- Input hash tracking for deploy stages

---

## Gap Analysis

### Critical Gaps (New Content Required)

1. **BuildStream Release 2 Architecture Overview**
   - Three-pipeline architecture explanation
   - Job/Image Group lifecycle concepts
   - State machine documentation
   - Differences from Release 1

2. **BuildStream Release 2 API Reference**
   - Complete REST API documentation
   - OAuth 2.0 authentication flow
   - Request/response schemas
   - Error codes and handling

3. **Resume and Retry Capability**
   - Stage guard logic
   - Build stage resume (smart skip)
   - Deploy stage re-run (input hash tracking)
   - Attempt number tracking

4. **Image Group Management**
   - Image Group concepts and lifecycle
   - Constituent images per role
   - ListImages API usage
   - Image selection for deployment

5. **Release 2 Pipeline Workflows**
   - Build pipeline (Release 2 version)
   - Deploy & Validate pipeline (new)
   - CleanUp pipeline (new)
   - Pipeline orchestration and triggers

### Content Requiring Updates

1. **prepare_oim_buildstream.rst**
   - Add OAuth client setup
   - Add automation repo cloning for Molecule
   - Update for Release 2 container configurations
   - Add new configuration parameters

2. **how-to-gitlab-deployment.rst**
   - Update for three-pipeline GitLab CI/CD configuration
   - Add parent pipeline router explanation
   - Update for dynamic child pipeline generation
   - Add OAuth integration

3. **how-to-update-catalog-pipeline.rst**
   - Update for Release 2 build pipeline stages
   - Add new stage names and sequences
   - Update for Image Group concepts
   - Add pipeline type selection (BUILD vs DEPLOY)

4. **buildstream_tables.rst**
   - Add new Release 2 configuration parameters
   - Add OAuth configuration parameters
   - Add image retention limit parameters
   - Add storage backend selection (NFS vs PowerScale)

5. **buildstream_troubleshooting.rst**
   - Add Release 2 error codes
   - Add three-pipeline troubleshooting
   - Add OAuth authentication issues
   - Add Image Group state troubleshooting
   - Add Resume & Retry troubleshooting

6. **index.rst**
   - Add Release 2 overview
   - Reorganize to separate Release 1 vs Release 2 content
   - Add migration guide from Release 1 to Release 2

### Content That Remains Valid (No Changes Needed)

1. **omnia_startup_buildstream.rst** - Omnia core deployment unchanged
2. **composable_roles_buildstream.rst** - Composable roles unchanged
3. **set_pxe_boot_order_buildstream.rst** - PXE boot setup unchanged (minor API changes possible)
4. **buildstream_telemetry_1.rst** - Telemetry unchanged
5. **buildstream_verify_telmetry_1.rst** - Telemetry verification unchanged

---

## Revised Content Plan

### New Topics (Release 2 Specific)

#### Topic 1: BuildStream Release 2 Architecture Overview

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept / Overview                          |
| **Status**             | New Topic                                    |
| **Target Audience**    | Primary: Infrastructure/HPC Administrator, Secondary: Platform Engineer/Cloud Architect, Tertiary: Evaluator/Decision Maker |
| **Source Traceability**| BSpec §1 (Introduction), Functional Spec §6 (System Overview), HLD §2 (Introduction), HLD §3 (Solution Architecture) |
| **RST File**           | docs/source/Buildstream/buildstream-release2-architecture.rst |
| **Content Type**       | Buildstream/ (existing directory)            |

**Customer Workflow Context:**
Customers upgrading from Release 1 or new to Release 2 need to understand the architectural changes, three-pipeline model, and new Job/Image Group concepts.

**Content Requirements:**
- Release 2 vs Release 1 architectural comparison
- Three-pipeline architecture explanation (Build, Deploy & Validate, CleanUp)
- Job and Image Group lifecycle concepts
- State machine overview
- Benefits and migration considerations
- System context diagram for Release 2

**Configuration Artifacts:**
- None (conceptual topic)

**Cross-References:**
- :doc:`buildstream-release2-api-reference`
- :doc:`buildstream-release2-pipelines`
- :doc:`buildstream-release2-migration-guide`

**Build Agent Instructions:**
- Create new RST file in existing Buildstream directory
- Use comparison table for Release 1 vs Release 2
- Include three-pipeline architecture diagram
- Add migration considerations section
- Target 1000-1500 words

---

#### Topic 2: BuildStream Release 2 API Reference

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Reference                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Primary: Platform Engineer/Cloud Architect, Secondary: Infrastructure/HPC Administrator |
| **Source Traceability**| BSpec §7 (API Contract Summary), Functional Spec §10 (API Functional Contract), API Spec v2.0, Component 2 Spec |
| **RST File**           | docs/source/Buildstream/buildstream-release2-api-reference.rst |
| **Content Type**       | Buildstream/ (existing directory)            |

**Customer Workflow Context:**
Platform Engineers need complete API documentation for integrating Release 2 features into CI/CD pipelines.

**Content Requirements:**
- OAuth 2.0 authentication flow
- New API endpoints documentation:
  - PUT /api/v1/jobs/{job_id}/upload
  - GET /api/v1/images
  - POST /api/v1/jobs/{job_id}/stages/deploy
  - POST /api/v1/jobs/{job_id}/stages/restart
  - POST /api/v1/jobs/{job_id}/stages/validate
  - DELETE /api/v1/jobs/{job_id}
- Request/response schemas
- Error codes and handling
- Rate limiting (if applicable)

**Configuration Artifacts:**
- Complete API endpoint specifications
- OAuth 2.0 flow documentation
- Error code reference table

**Cross-References:**
- :doc:`buildstream-release2-architecture`
- :doc:`buildstream-release2-pipelines`

**Build Agent Instructions:**
- Create new RST file in existing Buildstream directory
- Use http-domain directive for API documentation
- Include OAuth 2.0 flow diagram
- Add authentication setup section
- Target 1500-2000 words

---

#### Topic 3: BuildStream Resume and Retry

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept / How-To                             |
| **Status**             | New Topic                                    |
| **Target Audience**    | Primary: Infrastructure/HPC Administrator     |
| **Source Traceability**| Component 4 Spec (Resume & Retry), HLD §4.1.6 (Resume & Retry capabilities) |
| **RST File**           | docs/source/Buildstream/buildstream-resume-retry.rst |
| **Content Type**       | Buildstream/ (existing directory)            |

**Customer Workflow Context:**
Platform Operators need to understand how Resume & Retry works to save time during failed builds and deployments.

**Content Requirements:**
- Resume & Retry purpose and benefits
- Stage execution patterns (Build vs Deploy stages)
- Build stage resume logic (smart skip existing images)
- Deploy stage re-run logic (input hash tracking)
- Stage guard decision logic
- Attempt number tracking and audit trail
- Log file preservation

**Configuration Artifacts:**
- Stage guard logic rules
- Attempt number tracking
- Log file naming patterns

**Cross-References:**
- :doc:`buildstream-release2-pipelines`
- :doc:`buildstream_troubleshooting` (update)

**Build Agent Instructions:**
- Create new RST file in existing Buildstream directory
- Include stage guard decision tree
- Add build stage resume flowchart
- Include timeline example with retries
- Target 800-1200 words

---

#### Topic 4: BuildStream Release 2 Pipelines

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | How-To                                       |
| **Status**             | New Topic                                    |
| **Target Audience**    | Primary: Infrastructure/HPC Administrator     |
| **Source Traceability**| BSpec §4-5 (Features), Functional Spec §7-8 (Feature Requirements), HLD §3.2 (Control Flow) |
| **RST File**           | docs/source/Buildstream/buildstream-release2-pipelines.rst |
| **Content Type**       | Buildstream/ (existing directory)            |

**Customer Workflow Context:**
Platform Operators need step-by-step instructions for executing Release 2 pipelines (Build, Deploy & Validate, CleanUp).

**Content Requirements:**
- Build Pipeline workflow (Release 2 version)
- Deploy & Validate Pipeline workflow (new)
- CleanUp Pipeline workflow (new)
- Pipeline orchestration and triggers
- Job ID continuity across pipelines
- Image Group selection and deployment

**Configuration Artifacts:**
- Pipeline stage sequences
- GitLab CI/CD pipeline configurations
- API endpoints per pipeline

**Cross-References:**
- :doc:`buildstream-release2-architecture`
- :doc:`buildstream-release2-api-reference`
- :doc:`how-to-update-catalog-pipeline` (update)

**Build Agent Instructions:**
- Create new RST file in existing Buildstream directory
- Include three-pipeline workflow diagram
- Add step-by-step instructions for each pipeline
- Include GitLab CI/CD configuration examples
- Target 1200-1800 words

---

#### Topic 5: BuildStream Release 2 Migration Guide

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | How-To / Guide                              |
| **Status**             | New Topic                                    |
| **Target Audience**    | Primary: Infrastructure/HPC Administrator, Secondary: System Administrator |
| **Source Traceability**| HLD §4.1.3.6 (Upgrade Scenarios), migration requirements from specs |
| **RST File**           | docs/source/Buildstream/buildstream-release2-migration.rst |
| **Content Type**       | Buildstream/ (existing directory)            |

**Customer Workflow Context:**
Existing Release 1 users need guidance on migrating to Release 2, including database migrations, configuration updates, and workflow changes.

**Content Requirements:**
- Pre-migration checklist
- Database migration steps (Alembic)
- Configuration file updates
- GitLab CI/CD pipeline updates
- OAuth client setup
- Verification steps
- Rollback procedures

**Configuration Artifacts:**
- Migration checklist
- Configuration parameter changes
- Database migration commands

**Cross-References:**
- :doc:`buildstream-release2-architecture`
- :doc:`prepare_oim_buildstream` (update)
- :doc:`buildstream_troubleshooting` (update)

**Build Agent Instructions:**
- Create new RST file in existing Buildstream directory
- Include migration checklist
- Add step-by-step migration procedure
- Include verification steps
- Add rollback procedure
- Target 1000-1500 words

---

### Topics Requiring Updates

#### Update 1: prepare_oim_buildstream.rst

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Status**             | Update Existing                              |
| **Source Traceability**| HLD §4.1.3 (Component Design), Component 5 Spec (Phase 2) |
| **Changes Required**   | Add OAuth client setup, automation repo cloning, Molecule setup, new config parameters |

**Specific Updates:**
- Add OAuth 2.0 client registration steps
- Add automation repo cloning for Molecule validation
- Add setup_env.sh execution for test dependencies
- Add new Release 2 configuration parameters to config file sections
- Add storage backend selection (NFS vs PowerScale)
- Update verification steps to include new services

---

#### Update 2: how-to-gitlab-deployment.rst

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Status**             | Update Existing                              |
| **Source Traceability**| HLD §3.2.3 (Deploy & Validate Pipeline), Component 2 Spec |
| **Changes Required**   | Update for three-pipeline GitLab CI/CD, OAuth integration, dynamic child pipelines |

**Specific Updates:**
- Update GitLab CI/CD configuration for three-pipeline architecture
- Add parent pipeline router explanation
- Add dynamic child pipeline generation for image selection
- Add OAuth integration steps
- Update pipeline stage names for Release 2
- Add pipeline type selection (BUILD vs DEPLOY vs CLEANUP)

---

#### Update 3: how-to-update-catalog-pipeline.rst

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Status**             | Update Existing                              |
| **Source Traceability**| BSpec §4 (Feature 1), HLD §3.2.2 (Build Pipeline Flow) |
| **Changes Required**   | Update for Release 2 build pipeline stages, Image Group concepts |

**Specific Updates:**
- Update build pipeline stage sequence for Release 2
- Add Image Group concept explanation
- Update stage names (parse-catalog, generate-input-files, create-local-repository, build-image)
- Add Job ID and Image Group ID relationship
- Update pipeline monitoring for Release 2 stages
- Add reference to new deploy pipeline workflow

---

#### Update 4: buildstream_tables.rst

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Status**             | Update Existing                              |
| **Source Traceability**| HLD §4.1.3.4 (Configuration Processing), Component Specs |
| **Changes Required**   | Add new Release 2 configuration parameters, OAuth parameters, retention limits |

**Specific Updates:**
- Add OAuth 2.0 configuration parameters
- Add image retention limit parameters
- Add storage backend selection parameters
- Add automation framework configuration parameters
- Update existing parameter descriptions for Release 2 changes

---

#### Update 5: buildstream_troubleshooting.rst

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Status**             | Update Existing                              |
| **Source Traceability**| BSpec §12 (Error Handling), Functional Spec §19 (Error Handling), Component Specs |
| **Changes Required**   | Add Release 2 error codes, three-pipeline troubleshooting, OAuth issues, state machine issues |

**Specific Updates:**
- Add Release 2 specific error codes (IMAGE_GROUP_NOT_FOUND, IMAGE_NOT_DEPLOYABLE, etc.)
- Add OAuth authentication troubleshooting
- Add three-pipeline troubleshooting
- Add Image Group state troubleshooting
- Add Resume & Retry troubleshooting
- Add new stage troubleshooting (deploy, restart, validate)
- Keep existing Release 1 troubleshooting for backward compatibility

---

#### Update 6: index.rst

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Status**             | Update Existing                              |
| **Source Traceability**| Overall document organization                |
| **Changes Required**   | Reorganize for Release 2 content, add migration guide reference |

**Specific Updates:**
- Add Release 2 overview section
- Reorganize toctree to group Release 2 content
- Add migration guide reference
- Add architectural comparison note
- Maintain Release 1 content for backward compatibility

---

## Implementation Priority

### Phase 1: Critical New Content (High Priority)
1. BuildStream Release 2 Architecture Overview
2. BuildStream Release 2 Migration Guide
3. BuildStream Release 2 API Reference

### Phase 2: Operational New Content (Medium Priority)
4. BuildStream Release 2 Pipelines
5. BuildStream Resume and Retry

### Phase 3: Content Updates (Medium Priority)
6. Update prepare_oim_buildstream.rst
7. Update how-to-gitlab-deployment.rst
8. Update how-to-update-catalog-pipeline.rst

### Phase 4: Configuration and Troubleshooting Updates (Low Priority)
9. Update buildstream_tables.rst
10. Update buildstream_troubleshooting.rst
11. Update index.rst

---

## Additional Source Requirements

### Demo Transcripts
- [ ] Need demo transcripts showing Release 2 three-pipeline workflow
- [ ] Need demo transcripts showing OAuth authentication flow
- [ ] Need demo transcripts showing Resume & Retry in action
- [ ] Need demo transcripts showing migration from Release 1 to Release 2

### Unit Tests
- [ ] Need unit test examples for new API endpoints
- [ ] Need unit test examples for state machine transitions
- [ ] Need unit test examples for stage guard logic

### SME Interviews
- [ ] Need SME clarification on migration complexity and risks
- [ ] Need SME clarification on backward compatibility approach
- [ ] Need SME clarification on OAuth setup complexity

### User Feedback
- [ ] Need user feedback on Release 1 pain points to address in Release 2 docs
- [ ] Need user feedback on migration concerns

---

## Conclusion

This revised content plan focuses specifically on the NEW and CHANGED features in BuildStream Release 2, avoiding duplication of existing Release 1 documentation. The plan prioritizes:

1. **Architecture understanding** (Release 2 overview, migration guide)
2. **New API documentation** (comprehensive API reference)
3. **New capabilities** (Resume & Retry, three-pipeline workflows)
4. **Updates to existing content** (configuring for Release 2, updating workflows)

The plan maintains existing Release 1 documentation where it remains valid, ensuring backward compatibility while providing clear guidance for adopting Release 2 features.

**Total New Topics:** 5  
**Total Updates:** 6  
**Estimated Effort:** Medium-High (due to architectural changes)

