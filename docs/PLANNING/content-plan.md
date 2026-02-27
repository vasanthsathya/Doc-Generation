# Omnia 2.0 to 2.1 Upgrade Content Plan

## Overview
This content plan addresses the upgrade of Omnia core container from version 2.0 to 2.1 within the Omnia Infrastructure Manager (OIM). The plan is derived from HLD documentation, unit tests, demo transcriptions, and user stories to create comprehensive customer-facing documentation.

---

### Omnia Core Container Upgrade Overview

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept                                      |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator, Platform Engineer/Cloud Architect |
| **Source Traceability**| HLD Section 2, User Story Section 1-3, Demo Transcription 1-50 |
| **RST File**           | /docs/upgrade/concept-core-upgrade.rst |
| **Content Type**       | concepts/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc` (Sections 1-2)
- User Story: `docs/SOURCE MATERIALS/user_story.txt` (Lines 1-27)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.txt` (Lines 1-50)

**Customer Workflow Context:**
Customers need to understand what the Omnia 2.1 upgrade entails, why it's necessary, and what changes it introduces to their existing Omnia 2.0 deployment. This topic provides the foundational understanding before proceeding with the actual upgrade process.

**Content Requirements:**
- Prerequisite understanding of Omnia architecture and OIM components
- Key concepts: core container upgrade, input file migration, backup strategy
- Expected outcomes: Understanding upgrade scope, limitations, and benefits
- Important considerations: Two-step upgrade process, cluster reprovisioning requirements

**Configuration Artifacts:**
- Core container versions (1.0 → 1.1)
- Omnia version mapping (2.0.0.0 → 2.1.0.0)
- Backup directory structure: `/opt/omnia/backups/upgrade_<timestamp>`

**Cross-References:**
- How-to upgrade guide
- Rollback procedures
- Backup and recovery concepts

**Build Agent Instructions:**
- Create new RST file with concept topic structure
- Include overview of upgrade architecture and components
- Add admonitions: note about two-step process, warning about cluster reprovisioning
- Cross-reference to upgrade how-to guide
- SME validation required for technical accuracy
- AI_REVIEW: Verify upgrade scope matches HLD specifications

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if additional demo transcripts needed
- [x] Unit tests provide practical validation
- [ ] Flag if SME interviews required
- [ ] Flag if user feedback collection needed
- [x] HLD provides comprehensive technical details
- [x] User story clarifies customer objectives

---

### Upgrading Omnia Core Container from 2.0 to 2.1

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| HLD Section 3.2, Unit Test Lines 25-27, Demo Transcription 55-87 |
| **RST File**           | /docs/upgrade/how-to-upgrade-core.rst |
| **Content Type**       | how-to/upgrade/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc` (Section 3.2 - Upgrade Workflow Phases)
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt` (Lines 25-27)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.txt` (Lines 55-87)

**Customer Workflow Context:**
Step-by-step guide for HPC administrators to perform the actual upgrade from Omnia 2.0 to 2.1. This is the primary operational procedure that customers will follow to upgrade their existing Omnia deployment.

**Content Requirements:**
- Prerequisites: omnia.sh 2.1 version, Omnia 2.1 image availability
- Key steps: Pre-upgrade validation, approval gate, backup creation, container swap
- Expected outcomes: Successful core container upgrade to 2.1
- Critical warnings: Backup verification, rollback procedures

**Configuration Artifacts:**
- Commands: `./omnia.sh --upgrade`, `wget https://raw.githubusercontent.com/dell/omnia/refs/heads/pub/q1_dev/omnia.sh`
- Image build: `./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev`
- Backup path: `/opt/omnia/backups/upgrade_<timestamp>`
- Metadata file: `/opt/omnia/.data/oim_metadata.yml`

**Cross-References:**
- Upgrade concept overview
- Input file migration guide
- Rollback procedures
- Troubleshooting upgrade issues

**Build Agent Instructions:**
- Create new RST file with step-by-step procedure format
- Include all six upgrade phases with detailed steps
- Add admonitions: note about prerequisites, warning about backup verification, tip about rollback availability
- Include code blocks for all commands
- Cross-reference to input migration guide
- SME validation required for procedural accuracy
- AI_REVIEW: Verify steps match unit test workflow

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Unit tests provide complete workflow
- [x] Demo transcription shows practical execution
- [ ] Flag if SME interviews required for edge cases
- [ ] Flag if user feedback collection needed
- [x] HLD provides comprehensive workflow details

---

### Migrating Input Files After Core Container Upgrade

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| HLD Section 3.2.5, Unit Test Lines 42-49, Demo Transcription 204-244 |
| **RST File**           | /docs/upgrade/how-to-migrate-inputs.rst |
| **Content Type**       | how-to/upgrade/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc` (Section 3.2.5 - Migration and Apply)
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt` (Lines 42-49)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.txt` (Lines 204-244)

**Customer Workflow Context:**
Second step of the upgrade process where customers migrate their existing 2.0 input files to the 2.1 format. This is critical for preserving customer configurations while enabling new 2.1 features.

**Content Requirements:**
- Prerequisites: Successful core container upgrade, access to backup files
- Key steps: Run upgrade_omnia.yml, validate migrated inputs, manual configuration updates
- Expected outcomes: Input files compatible with Omnia 2.1 format
- Important considerations: New parameter requirements, manual intervention needs

**Configuration Artifacts:**
- Playbook command: `ansible-playbook /omnia/upgrade/upgrade_omnia.yml`
- Input file locations: `/opt/omnia/input/`, backup directory
- Lock file: `/opt/omnia/.data/upgrade_in_progress.lock`
- New 2.1 parameters: IB network, config sources

**Cross-References:**
- Core container upgrade guide
- Input file reference documentation
- Cluster reprovisioning guide
- Troubleshooting input migration issues

**Build Agent Instructions:**
- Create new RST file with procedure format
- Document both automatic migration and manual reconfiguration options
- Include admonitions: note about new parameters, warning about lock file removal
- Add code blocks for playbook commands
- Cross-reference to input file reference
- SME validation required for parameter accuracy
- AI_REVIEW: Verify migration steps match demo workflow

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [ ] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Unit tests provide migration workflow
- [x] Demo transcription shows practical execution
- [ ] Flag if SME interviews required for parameter details
- [ ] Flag if user feedback collection needed
- [x] HLD provides technical migration details

---

### Rolling Back Omnia Core Container Upgrade

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| HLD Section 3.2.3, Unit Test Lines 61-68, Demo Transcription 296-327 |
| **RST File**           | /docs/upgrade/how-to-rollback-upgrade.rst |
| **Content Type**       | how-to/upgrade/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc` (Section 3.2.3 - Rollback Workflow)
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt` (Lines 61-68)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.txt` (Lines 296-327)

**Customer Workflow Context:**
Procedures for reverting an Omnia 2.1 upgrade back to 2.0 in case of upgrade failures or issues. Critical for maintaining system stability and providing administrators with recovery options.

**Content Requirements:**
- Prerequisites: Failed upgrade, available backup files, rollback access
- Key steps: Validate backup, stop 1.1 container, restore inputs, start 1.0 container
- Expected outcomes: System restored to Omnia 2.0 state with original configurations
- Critical warnings: Data loss potential, service interruption

**Configuration Artifacts:**
- Command: `./omnia.sh --rollback`
- Rollback playbook: `rollback_omnia.yml`
- Backup location: `/opt/omnia/backups/`
- Metadata version: `omnia_version: 2.0.0.0`

**Cross-References:**
- Upgrade procedures
- Backup and recovery concepts
- Troubleshooting upgrade failures
- System recovery procedures

**Build Agent Instructions:**
- Create new RST file with rollback procedure format
- Document all six rollback steps with validation checks
- Include admonitions: warning about service interruption, note about backup validation
- Add code blocks for rollback commands
- Cross-reference to upgrade procedures
- SME validation required for recovery accuracy
- AI_REVIEW: Verify rollback steps match HLD workflow

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Unit tests provide rollback workflow
- [x] Demo transcription shows practical execution
- [ ] Flag if SME interviews required for edge cases
- [ ] Flag if user feedback collection needed
- [x] HLD provides comprehensive rollback details

---

### Omnia CLI Reference - Upgrade Commands

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Reference                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator, Platform Engineer |
| **Source Traceability**| HLD Section 3.2, Unit Test Lines 14-18, Demo Transcription 29-35 |
| **RST File**           | /docs/reference/cli/omnia-upgrade.rst |
| **Content Type**       | reference/cli/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc` (Section 3.2 - Command references)
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt` (Lines 14-18)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.txt` (Lines 29-35)

**Customer Workflow Context:**
Complete reference documentation for the new Omnia CLI commands introduced in 2.1 for upgrade, rollback, and version management. Essential for administrators who need to understand command syntax, options, and usage.

**Content Requirements:**
- Prerequisites: Command access, proper permissions
- Key commands: `omnia.sh --upgrade`, `omnia.sh --rollback`, `omnia.sh --version`
- Expected outcomes: Understanding command usage and options
- Important considerations: Command dependencies, error conditions

**Configuration Artifacts:**
- Command syntax and parameters
- Output formats and examples
- Error codes and messages
- Version detection logic

**Cross-References:**
- Upgrade procedures
- Rollback procedures
- Troubleshooting command issues

**Build Agent Instructions:**
- Create new RST file with CLI reference format
- Document all three new commands with syntax, options, and examples
- Include admonitions: note about version requirements, warning about command conflicts
- Add code blocks for command examples
- Cross-reference to procedural guides
- SME validation required for command accuracy
- AI_REVIEW: Verify command syntax matches implementation

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Unit tests provide command usage
- [x] Demo transcription shows practical execution
- [ ] Flag if SME interviews required for advanced options
- [ ] Flag if user feedback collection needed
- [x] HLD provides command framework

---

### Troubleshooting Omnia Upgrade Issues

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Troubleshooting                              |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator             |
| **Source Traceability**| HLD Section 3.2.4, Unit Test Lines 36-39, Demo Transcription 324-327 |
| **RST File**           | /docs/troubleshooting/upgrade-issues.rst |
| **Content Type**       | troubleshooting/ |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc` (Section 3.2.4 - Install Conflict Handling)
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt` (Lines 36-39)
- Demo Transcription: `docs/SOURCE MATERIALS/demo_transcription.txt` (Lines 324-327)

**Customer Workflow Context:**
Common issues and solutions that administrators may encounter during the Omnia upgrade process. Critical for resolving upgrade failures and preventing system downtime.

**Content Requirements:**
- Prerequisites: Understanding of upgrade process, system access
- Common issues: Upgrade conflicts, backup failures, container swap problems
- Resolution steps: Diagnostic procedures, recovery actions, prevention measures
- Critical warnings: Data protection, service continuity

**Configuration Artifacts:**
- Error messages and codes
- Diagnostic commands
- Recovery procedures
- Prevention strategies

**Cross-References:**
- Upgrade procedures
- Rollback procedures
- System diagnostics

**Build Agent Instructions:**
- Create new RST file with troubleshooting format
- Document common upgrade issues with symptoms, causes, and solutions
- Include admonitions: warning about data loss, tip about prevention
- Add code blocks for diagnostic commands
- Cross-reference to procedural guides
- SME validation required for troubleshooting accuracy
- AI_REVIEW: Verify solutions address real upgrade issues

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [x] Unit tests identify common issues
- [x] Demo transcription shows practical problems
- [ ] Flag if SME interviews required for edge cases
- [ ] Flag if user feedback collection needed
- [x] HLD provides conflict handling details

---

## Summary and Implementation Priority

### High Priority Topics (Implement First)
1. **Omnia Core Container Upgrade Overview** - Foundational concept understanding
2. **Upgrading Omnia Core Container from 2.0 to 2.1** - Primary procedural guide
3. **Omnia CLI Reference - Upgrade Commands** - Essential command documentation

### Medium Priority Topics
4. **Migrating Input Files After Core Container Upgrade** - Critical second-step procedure
5. **Rolling Back Omnia Core Container Upgrade** - Important recovery procedure

### Lower Priority Topics
6. **Troubleshooting Omnia Upgrade Issues** - Support documentation, can be refined based on user feedback

### Cross-Reference Strategy
- All procedural guides should reference the concept overview
- CLI reference should be cross-referenced from all procedural guides
- Troubleshooting should be referenced from all upgrade procedures
- Consider creating an upgrade index page to tie all topics together

### SME Validation Requirements
- Technical accuracy of upgrade workflow phases
- Command syntax and parameter validation
- Input file migration details
- Rollback procedure verification
- Error handling and recovery procedures

### Content Gaps Identified
- Performance characteristics during upgrade (downtime, resource usage)
- Integration examples with existing monitoring systems
- Detailed security considerations for upgrade process
- Common mistakes and gotchas from field experience
- Advanced troubleshooting scenarios

This content plan provides a comprehensive foundation for documenting the Omnia 2.0 to 2.1 upgrade process, addressing all major customer workflows and operational requirements identified in the source materials.
