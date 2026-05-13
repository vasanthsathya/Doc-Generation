---
title: AI Skill Document — BuildStream Documentation
aliases: [BuildStream Skill Doc, BuildStream Docs AI Rulebook]
tags: [documentation, ai, buildstream, omnia, rst, readthedocs, skill-document]
created: 2026-05-12
status: active
---

# Product Skill Document: BuildStream Documentation

> **Purpose:** This is the BuildStream-specific supplement to the main Omnia documentation AI skill system. BuildStream documentation has unique requirements and workflows that differ from general Omnia documentation. **This skill document should be used in conjunction with the main [SKILL.md](../omnia-doc-skill/SKILL.md) document.**
>
> **For general Omnia documentation rules**, refer to the main skill document. **For BuildStream-specific guidance**, use this document.

---

## Table of Contents

1. [Document Metadata](#1-document-metadata)
2. [BuildStream-Specific Rules](#2-buildstream-specific-rules)
3. [BuildStream Information Map](#3-buildstream-information-map)
4. [BuildStream Documentation Structure](#4-buildstream-documentation-structure)
5. [BuildStream Content Guidelines](#5-buildstream-content-guidelines)
6. [BuildStream Pipeline Stage Guidelines](#6-buildstream-pipeline-stage-guidelines)
7. [BuildStream Troubleshooting Guidelines](#7-buildstream-troubleshooting-guidelines)

---

## 1. Document Metadata

|| Field            | Value                                      |
||------------------|--------------------------------------------|
|| Product          | Omnia BuildStream                          |
|| Version          | 2.1.0.0-rc2                                |
|| Last Updated     | 2026-05-12                                 |
|| Owner            | Vasanth Sathya                             |
|| Focus Area       | CI/CD Pipeline Documentation                |
|| Target Users     | Infrastructure/HPC Administrators          |

---

## 2. BuildStream-Specific Rules

### 2.1 Primary Focus: CI/CD Pipeline Users

BuildStream documentation focuses on **CI/CD pipeline users**, not direct API users. The customer uses GitLab pipelines to execute BuildStream workflows, not direct API calls.

**Content Priorities:**
* Pipeline execution procedures (not API endpoint documentation)
* Catalog management and pipeline triggering
* Build and deploy pipeline stages
* Management operations (cleanup, resume, retry)
* Troubleshooting pipeline issues

**Content to Avoid:**
* Direct API endpoint examples and request/response formats
* API authentication details (unless for GitLab integration)
* Database internals and schema details
* Over-technical architecture diagrams

### 2.2 Documentation Structure

Each BuildStream topic must follow this structure:

**Overview → Prerequisites → Procedure → Verification**

* **Overview**: Brief description of what the topic covers
* **Prerequisites**: Requirements before beginning the procedure
* **Procedure**: Step-by-step instructions with embedded conceptual information
* **Verification**: Steps to verify successful completion

**No separate conceptual sections** - embed conceptual information within the procedure where relevant.

### 2.3 Pipeline Stage Accuracy

BuildStream pipeline stages must match the **official specifications exactly**:

**Build Pipeline Stages:**
1. create-local-repository
2. parse-catalog
3. generate-input-files
4. build-image

**Deploy Pipeline Stages:**
1. deploy
2. restart
3. validate

**Never use alternative stage names** or combine stages (e.g., avoid "deploy-and-validate").

### 2.4 Telemetry Documentation

BuildStream documentation **includes telemetry** as a monitoring capability. Do not remove telemetry documentation from BuildStream.

**Telemetry Files:**
* `initializing-telemetry.rst` - Telemetry service initialization
* `verifying-telemetry-services.rst` - Telemetry service verification

### 2.5 Image Groups Concept

BuildStream uses **Image Groups** and **Constituent Images** as core concepts:

* **Image Group**: 1:1 mapping with Job ID
* **Constituent Images**: Individual images within an Image Group
* **Functional Groups**: Map to Image Groups for deployment

Embed this concept explanation within pipeline execution documentation, not as a separate conceptual document.

---

## 3. BuildStream Information Map

### Content Type Decision Rules

When deciding where new BuildStream content belongs:

|| Question                                      | Answer → Section                          |
||-----------------------------------------------|-------------------------------------------|
|| Infrastructure setup and installation?         | `how-to/buildstream/setup/`                |
|| Build pipeline execution?                     | `how-to/buildstream/build/`                |
|| Deploy pipeline execution?                    | `how-to/buildstream/deploy/`               |
|| Management operations (cleanup, resume, retry)? | `how-to/buildstream/management/`          |
|| Monitoring and telemetry?                      | `how-to/buildstream/monitoring/`           |
|| Configuration parameters and tables?          | `reference/buildstream/`                   |
|| Troubleshooting known issues?                 | `troubleshooting/buildstream/`             |

### File Naming Conventions

|| Section                          | Naming Pattern                  | Examples                                      |
||----------------------------------|---------------------------------|-----------------------------------------------|
|| `how-to/buildstream/setup/`      | Gerund + noun, kebab-case       | `deploying-omnia-core.rst`                     |
|| `how-to/buildstream/build/`      | Gerund + noun, kebab-case       | `executing-build-pipeline.rst`                 |
|| `how-to/buildstream/deploy/`     | Gerund + noun, kebab-case       | `executing-deploy-pipeline.rst`                |
|| `how-to/buildstream/management/` | Gerund + noun, kebab-case       | `performing-cleanup-operations.rst`            |
|| `how-to/buildstream/monitoring/` | Gerund + noun, kebab-case       | `initializing-telemetry.rst`                    |
|| `reference/buildstream/`         | Noun phrase, kebab-case         | `catalog-schema.rst`, `pipeline-stages.rst`     |
|| `troubleshooting/buildstream/`   | Symptom or error, kebab-case    | `common-pipeline-issues.rst`                   |

---

## 4. BuildStream Documentation Structure

```
Buildstream/
├── how-to/buildstream/
│   ├── setup/
│   │   ├── deploying-omnia-core.rst
│   │   ├── preparing-oim-buildstream.rst
│   │   ├── deploying-gitlab-buildstream.rst
│   │   └── creating-pxe-mapping-file.rst
│   ├── build/
│   │   └── executing-build-pipeline.rst
│   ├── deploy/
│   │   ├── executing-deploy-pipeline.rst
│   │   └── configuring-pxe-boot.rst
│   ├── management/
│   │   ├── performing-cleanup-operations.rst
│   │   ├── resuming-pipelines.rst
│   │   └── retrying-pipelines.rst
│   └── monitoring/
│       ├── initializing-telemetry.rst
│       └── verifying-telemetry-services.rst
├── reference/buildstream/
│   ├── configuration-tables.rst
│   ├── catalog-schema.rst
│   ├── upload-validation-rules.rst
│   └── pipeline-stages.rst
├── troubleshooting/buildstream/
│   └── common-pipeline-issues.rst
└── index.rst
```

---

## 5. BuildStream Content Guidelines

### 5.1 Setup Phase Documentation

Setup documentation covers infrastructure preparation:

**deploying-omnia-core.rst**
* Deploy Omnia core container as prerequisite for BuildStream
* Include container installation, verification, and basic configuration

**preparing-oim-buildstream.rst**
* Deploy BuildStream containers and services on OIM
* Include BuildStream API container, playbook watcher service, PostgreSQL database
* Reference configuration tables for parameter guidance

**deploying-gitlab-buildstream.rst**
* Deploy GitLab as CI/CD automation engine
* Include GitLab installation, project setup, runner verification
* Emphasize dedicated GitLab instance for BuildStream

**creating-pxe-mapping-file.rst**
* Create PXE mapping file with node information
* Include functional groups and groups definitions
* Reference functional groups table for valid values

### 5.2 Build Phase Documentation

Build documentation covers pipeline execution:

**executing-build-pipeline.rst**
* Catalog management and pipeline execution
* Include all 4 build stages: create-local-repository, parse-catalog, generate-input-files, build-image
* Embed Image Groups concept explanation (1:1 Job ID mapping)
* Include pipeline monitoring through GitLab interface

### 5.3 Deploy Phase Documentation

Deploy documentation covers image deployment:

**executing-deploy-pipeline.rst**
* Deploy pipeline execution
* Include all 3 deploy stages: deploy, restart, validate
* Include deployment monitoring and verification

**configuring-pxe-boot.rst**
* PXE boot configuration for nodes
* Include set_pxe_boot.yml playbook usage
* Include node restart and image loading verification

### 5.4 Management Phase Documentation

Management documentation covers ongoing operations:

**performing-cleanup-operations.rst**
* Manual cleanup procedures
* Automated cleanup with 24-hour cron job
* 50 Image Group retention limit
* Include both manual and automated procedures

**resuming-pipelines.rst**
* Resume interrupted pipelines from last successful state
* Include stage-specific and full pipeline resume
* Emphasize Job ID preservation

**retrying-pipelines.rst**
* Retry failed pipelines after issue resolution
* Include stage-specific and full pipeline retry
* Distinguish from resume operations

### 5.5 Monitoring Phase Documentation

Monitoring documentation covers telemetry:

**initializing-telemetry.rst**
* iDRAC telemetry service initialization
* Include service cluster and external node configuration
* Reference telemetry configuration tables

**verifying-telemetry-services.rst**
* Telemetry service verification
* Include pod status, Kafka message flow, TLS connectivity
* Include VictoriaMetrics data viewing

### 5.6 Reference Documentation

Reference documentation provides lookup information:

**configuration-tables.rst**
* BuildStream configuration parameter tables
* Include all configuration file parameters

**catalog-schema.rst**
* Catalog schema structure and validation rules
* Include schema version 1.1, field definitions, supported values
* Include example catalog

**upload-validation-rules.rst**
* Upload validation rules and limits
* Include 5MB file limit, 50MB archive limit, 500 entry limit
* Include validation process and error messages

**pipeline-stages.rst**
* Pipeline stages reference
* Include build and deploy stage definitions
* Include stage execution order and dependencies
* Include state machine information

### 5.7 Troubleshooting Documentation

Troubleshooting documentation addresses known issues:

**common-pipeline-issues.rst**
* Build and deploy pipeline troubleshooting
* Organize by stage for easy lookup
* Include symptom, cause, and resolution for each issue

---

## 6. BuildStream Pipeline Stage Guidelines

### 6.1 Build Pipeline Stages

When documenting build pipeline stages, always use the exact stage names:

1. **create-local-repository**
   * Creates and configures local repository
   * Sets up package storage and metadata

2. **parse-catalog**
   * Parses and validates catalog file
   * Extracts build requirements

3. **generate-input-files**
   * Generates input files for image building
   * Creates configuration files for each functional group

4. **build-image**
   * Builds diskless images based on specifications
   * Installs packages and configures systems

### 6.2 Deploy Pipeline Stages

When documenting deploy pipeline stages, always use the exact stage names:

1. **deploy**
   * Deploys images to target nodes
   * Maps functional groups to image groups

2. **restart**
   * Restarts nodes to load deployed images
   * Uses BMC power commands

3. **validate**
   * Validates successful deployment
   * Checks node connectivity and image versions

### 6.3 Stage Documentation Rules

* **Never combine stages** (e.g., avoid "deploy-and-validate")
* **Never use alternative names** (e.g., avoid "initialization" for create-local-repository)
* **Always maintain stage order** in documentation
* **Include stage dependencies** when relevant
* **Reference pipeline-stages.rst** for detailed stage information

---

## 7. BuildStream Troubleshooting Guidelines

### 7.1 Troubleshooting Organization

Organize troubleshooting content by **pipeline stage** for easy lookup:

* Build Pipeline Issues
  * create-local-repository failures
  * parse-catalog failures
  * generate-input-files failures
  * build-image failures

* Deploy Pipeline Issues
  * deploy failures
  * restart failures
  * validate failures

### 7.2 Troubleshooting Format

Each troubleshooting entry should follow this format:

**Issue**: [Stage] is failing.

**Possible Cause**: This issue indicates one of the following problems:
- [Cause 1]
- [Cause 2]

**Resolution**:
1. [Step 1]
2. [Step 2]

### 7.3 Common BuildStream Issues

**Build Pipeline Issues:**
* Local repository configuration errors
* Catalog schema validation failures
* Input file generation permission errors
* Image build playbook failures

**Deploy Pipeline Issues:**
* PXE mapping file configuration errors
* BMC connectivity problems
* Image deployment failures
* Node boot validation failures

**Management Issues:**
* Cleanup operation failures
* Resume operation errors
* Retry operation failures

**Infrastructure Issues:**
* BuildStream API server failures
* GitLab runner connectivity problems
* PostgreSQL database issues
* Network connectivity problems

---

## 8. Integration with Main Skill Document

This BuildStream-specific skill document supplements the main Omnia documentation skill document. When generating BuildStream documentation:

1. **Use main SKILL.md for:**
   * General RST formatting conventions
   * Voice and tone guidelines
   * File structure templates
   * Code block conventions
   * Cross-reference rules

2. **Use this BuildStream skill for:**
   * BuildStream-specific content structure
   * Pipeline stage terminology
   * BuildStream information map
   * CI/CD pipeline focus
   * BuildStream troubleshooting organization

3. **When rules conflict:**
   * This BuildStream skill takes precedence for BuildStream-specific content
   * Main SKILL.md takes precedence for general documentation standards

---

## 9. Maintenance Log

|| Date       | Changes                                                                 |
||------------|-------------------------------------------------------------------------|
|| 2026-05-12 | Initial BuildStream skill document created based on comprehensive documentation review |
||            | Defined BuildStream-specific documentation structure and guidelines      |
||            | Established pipeline stage terminology and organization                 |
||            | Integrated with main Omnia documentation skill system                   |