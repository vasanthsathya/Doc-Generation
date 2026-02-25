# Omnia 2.1 Upgrade Content Plan

This content plan addresses the upgrade of Omnia core container from 2.0 to 2.1, including the new upgrade workflow, rollback procedures, and post-upgrade steps.

---

## Upgrade Workflow Overview

### Understanding Omnia Core Container Upgrade

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Concept                                      |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator              |
| **Source Traceability**| HLD Section 2, Engineering Notes, Demo Transcription, Unit Test |
| **RST File**           | /docs/upgrade/concept-omnia-core-upgrade.rst |
| **Content Type**       | upgrade/ (feature-specific directory) |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc`
- Engineering Notes: `docs/SOURCE MATERIALS/user_story.txt`  
- Demo Transcripts: `docs/SOURCE MATERIALS/demo_transcription.txt`
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt`

**Customer Workflow Context:**
Customers running Omnia 2.0 need to understand what the core container upgrade entails, why it's necessary, and what changes occur during the upgrade process. This provides the foundational knowledge before proceeding with the actual upgrade procedure.

**Content Requirements:**
- Definition of core container upgrade and its purpose
- Explanation of why upgrade is needed (new architecture, containerized OIM, LocalRepo, OpenCHAMI changes)
- Overview of the six-phase upgrade workflow
- Distinction between core container upgrade and full cluster reprovisioning
- Explanation of what data is preserved and what requires manual reconfiguration

**Configuration Artifacts:**
- Container images: omnia-core:1.0 → omnia-core:2.1
- Backup directory: /opt/omnia/backups/upgrade_<timestamp>
- Metadata file: /opt/omnia/.data/oim_metadata.yml

**Cross-References:**
- :doc:`../how-to/upgrade/perform-upgrade`
- :doc:`../how-to/upgrade/rollback-upgrade`
- :doc:`../reference/upgrade-commands`

**Build Agent Instructions:**
- Create new RST file with concept topic structure (no prerequisites section)
- Include sections: Definition → Why It Matters → How It Works
- Add cross-references to related upgrade topics
- Include note about cluster reprovisioning requirements for new features

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
- [ ] Flag if additional demo transcripts needed
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required for performance impact details
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required for security considerations
- [ ] Flag if engineering notes clarification required

---

## Upgrade Procedures

### Performing Omnia Core Container Upgrade

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator              |
| **Source Traceability**| HLD Section 3.2, Engineering Notes, Demo Transcription, Unit Test |
| **RST File**           | /docs/upgrade/how-to-perform-upgrade.rst |
| **Content Type**       | upgrade/ (feature-specific directory) |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc`
- Engineering Notes: `docs/SOURCE MATERIALS/user_story.txt`  
- Demo Transcripts: `docs/SOURCE MATERIALS/demo_transcription.txt`
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt`

**Customer Workflow Context:**
Administrators need to perform the actual upgrade from Omnia 2.0 to 2.1 using the new omnia.sh --upgrade command. This is a critical operation that requires careful preparation and execution.

**Content Requirements:**
- Prerequisites: omnia.sh 2.1 file, omnia 2.1 image present, 2.0 container running
- Step-by-step procedure for running ./omnia.sh --upgrade
- Phase 1: Pre-upgrade validation steps
- Phase 2: Approval gate with backup destination selection
- Phase 3: Backup creation process
- Phase 4: Container swap (1.0 → 2.1)
- Phase 5: Migration and apply (inside new container)
- Phase 6: Post-upgrade validation
- Step 2: Running upgrade_omnia.yml for input file migration
- Verification steps to confirm successful upgrade

**Configuration Artifacts:**
- Command: ./omnia.sh --upgrade
- Prerequisite command: ./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev
- Backup location: /opt/omnia/backups/upgrade_<timestamp>
- Migration playbook: /omnia/upgrade/upgrade_omnia.yml
- Lock file: /opt/omnia/.data/upgrade_in_progress.lock

**Cross-References:**
- :doc:`../concepts/upgrade/omnia-core-upgrade`
- :doc:`../how-to/upgrade/rollback-upgrade`
- :doc:`../troubleshooting/upgrade-issues`

**Build Agent Instructions:**
- Create new RST file with procedure structure (include prerequisites and verification)
- Follow source priority: Engineering Notes → Unit Tests → Demo Transcriptions → HLD
- Include numbered steps with exact commands
- Add verification step after main procedure
- Include warning about cluster reprovisioning for new features
- Add note about backup integrity and safety considerations

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
- [ ] Flag if additional demo transcripts needed
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required for performance impact
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required
- [ ] Flag if engineering notes clarification required

### Rolling Back Omnia Core Container Upgrade

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator              |
| **Source Traceability**| HLD Section 3.2.3, Engineering Notes, Demo Transcription, Unit Test |
| **RST File**           | /docs/upgrade/how-to-rollback-upgrade.rst |
| **Content Type**       | upgrade/ (feature-specific directory) |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc`
- Engineering Notes: `docs/SOURCE MATERIALS/user_story.txt`  
- Demo Transcripts: `docs/SOURCE MATERIALS/demo_transcription.txt`
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt`

**Customer Workflow Context:**
When an upgrade fails or causes issues, administrators need to rollback to the previous version (2.0) to restore cluster functionality. This is a critical recovery procedure.

**Content Requirements:**
- Prerequisites: Backup exists from previous upgrade
- Step-by-step procedure for running ./omnia.sh --rollback
- Rollback workflow steps:
  1. Validate backup exists
  2. Stop 2.1 container
  3. Execute rollback_omnia.yml to restore inputs
  4. Start 1.0 container
  5. Update metadata to omnia_version: 2.0.0
  6. Validate rollback success
- Verification steps to confirm successful rollback
- Guidance on when to use rollback vs. troubleshoot

**Configuration Artifacts:**
- Command: ./omnia.sh --rollback
- Rollback playbook: rollback_omnia.yml
- Backup location: /opt/omnia/backups/
- Metadata file: /opt/omnia/.data/oim_metadata.yml

**Cross-References:**
- :doc:`../concepts/upgrade/omnia-core-upgrade`
- :doc:`../how-to/upgrade/perform-upgrade`
- :doc:`../troubleshooting/upgrade-issues`

**Build Agent Instructions:**
- Create new RST file with procedure structure (include prerequisites and verification)
- Follow source priority: Engineering Notes → Unit Tests → Demo Transcriptions → HLD
- Include numbered steps with exact commands
- Add verification step after main procedure
- Include warning about data loss potential and backup importance
- Add note about rollback limitations and considerations

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
- [ ] Flag if additional demo transcripts needed
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required
- [ ] Flag if engineering notes clarification required

### Managing Input File Migration After Upgrade

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Procedure                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator              |
| **Source Traceability**| HLD Section 3.2.2, Engineering Notes, Demo Transcription, Unit Test |
| **RST File**           | /docs/upgrade/how-to-migrate-input-files.rst |
| **Content Type**       | upgrade/ (feature-specific directory) |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc`
- Engineering Notes: `docs/SOURCE MATERIALS/user_story.txt`  
- Demo Transcripts: `docs/SOURCE MATERIALS/demo_transcription.txt`
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt`

**Customer Workflow Context:**
After the core container upgrade, administrators need to migrate their 2.0 input files to 2.1 format to maintain cluster functionality. This is Step 2 of the upgrade process.

**Content Requirements:**
- Prerequisites: Core container upgrade completed, inside omnia_core container
- Step-by-step procedure for running upgrade_omnia.yml
- Explanation of input file transformations (2.0 → 2.1 format)
- New input parameters introduced in 2.1 (IB network, config sources)
- Manual reconfiguration steps for new fields
- Cluster reprovisioning guidance for new features
- Alternative option: Skip migration and reconfigure manually
- Verification steps to confirm successful migration

**Configuration Artifacts:**
- Migration playbook: ansible-playbook /omnia/upgrade/upgrade_omnia.yml
- Backup location: /opt/omnia/backups/upgrade_<timestamp>/input
- Lock file: /opt/omnia/.data/upgrade_in_progress.lock
- New input fields: IB network settings, config sources

**Cross-References:**
- :doc:`../how-to/upgrade/perform-upgrade`
- :doc:`../concepts/upgrade/omnia-core-upgrade`
- :doc:`../troubleshooting/upgrade-issues`

**Build Agent Instructions:**
- Create new RST file with procedure structure (include prerequisites and verification)
- Follow source priority: Engineering Notes → Unit Tests → Demo Transcriptions → HLD
- Include numbered steps with exact commands
- Add verification step after main procedure
- Include note about new input parameters and manual configuration
- Add warning about cluster reprovisioning requirements

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
- [ ] Flag if additional demo transcripts needed
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required for new parameter details
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required
- [ ] Flag if engineering notes clarification required

---

## Reference Materials

### Omnia Upgrade Command Reference

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Reference                                    |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator, Platform Engineer/Cloud Architect |
| **Source Traceability**| Engineering Notes, Unit Test, Demo Transcription |
| **RST File**           | /docs/upgrade/reference-upgrade-commands.rst |
| **Content Type**       | upgrade/ (feature-specific directory) |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc`
- Engineering Notes: `docs/SOURCE MATERIALS/user_story.txt`  
- Demo Transcripts: `docs/SOURCE MATERIALS/demo_transcription.txt`
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt`

**Customer Workflow Context:**
Administrators need quick reference information about the new upgrade-related commands introduced in Omnia 2.1, including syntax, options, and usage examples.

**Content Requirements:**
- ./omnia.sh --version command syntax and output
- ./omnia.sh --upgrade command syntax and options
- ./omnia.sh --rollback command syntax and options
- Command prerequisites and requirements
- Expected output formats and examples
- Common command options and parameters
- Error messages and their meanings

**Configuration Artifacts:**
- Commands: ./omnia.sh --version, --upgrade, --rollback
- Prerequisite: wget command for downloading omnia.sh
- Image build command: ./build_images.sh core core_tag=2.1

**Cross-References:**
- :doc:`../how-to/upgrade/perform-upgrade`
- :doc:`../how-to/upgrade/rollback-upgrade`
- :doc:`../concepts/upgrade/omnia-core-upgrade`

**Build Agent Instructions:**
- Create new RST file with reference structure
- Include command syntax tables and examples
- Follow source priority: Engineering Notes → Unit Tests → Demo Transcriptions → HLD
- Include parameter descriptions and usage examples
- Add cross-references to related how-to topics

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
- [ ] Flag if additional demo transcripts needed
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required
- [ ] Flag if engineering notes clarification required

---

## Troubleshooting

### Troubleshooting Omnia Upgrade Issues

| Field                  | Details                                      |
|------------------------|----------------------------------------------|
| **Topic Type**         | Troubleshooting                              |
| **Status**             | New Topic                                    |
| **Target Audience**    | Infrastructure/HPC Administrator              |
| **Source Traceability**| Engineering Notes, Demo Transcription, Unit Test |
| **RST File**           | /docs/upgrade/troubleshooting-upgrade-issues.rst |
| **Content Type**       | upgrade/ (feature-specific directory) |

**Source File Locations:**
- HLD: `docs/SOURCE MATERIALS/hld.doc`
- Engineering Notes: `docs/SOURCE MATERIALS/user_story.txt`  
- Demo Transcripts: `docs/SOURCE MATERIALS/demo_transcription.txt`
- Unit Tests: `docs/SOURCE MATERIALS/unit_test.txt`

**Customer Workflow Context:**
When upgrade procedures fail or encounter errors, administrators need systematic troubleshooting guidance to identify and resolve issues quickly.

**Content Requirements:**
- Common upgrade failure scenarios and solutions
- Image pull failures and resolution steps
- Backup creation failures and troubleshooting
- Container swap issues and recovery procedures
- Input file migration errors and fixes
- Validation failures and corrective actions
- Rollback failure scenarios and alternatives
- Error message explanations and remedies
- Performance issues during upgrade
- Network connectivity problems

**Configuration Artifacts:**
- Error messages from upgrade phases
- Log file locations and analysis
- Backup integrity checks
- Container health checks
- Validation command outputs

**Cross-References:**
- :doc:`../how-to/upgrade/perform-upgrade`
- :doc:`../how-to/upgrade/rollback-upgrade`
- :doc:`../reference/upgrade-commands`

**Build Agent Instructions:**
- Create new RST file with troubleshooting structure
- Follow source priority: Engineering Notes → Unit Tests → Demo Transcriptions → HLD
- Include symptom-cause-solution format
- Add verification steps for each resolution
- Include warnings about data protection and backup importance

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
- [ ] Flag if additional demo transcripts needed for error scenarios
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required for advanced troubleshooting
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required
- [ ] Flag if engineering notes clarification required

---

## Summary

This content plan addresses the complete Omnia 2.1 upgrade workflow with 5 comprehensive topics:

1. **Concept Topic**: Understanding the upgrade (no prerequisites)
2. **Procedure Topics**: 3 how-to guides with verification steps
3. **Reference Topic**: Command reference for quick lookup
4. **Troubleshooting Topic**: Systematic issue resolution

All topics follow the updated requirements:
- Concept topics exclude prerequisites sections
- Procedure topics include mandatory verification steps
- Source priority: Engineering Notes → Unit Tests → Demo Transcriptions → HLD
- Missing information marked with `<To be decided>` placeholders

The plan provides comprehensive coverage of the upgrade workflow while identifying gaps that require additional source materials or SME input.
