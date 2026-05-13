.. _pipeline-stages-reference:

Pipeline Stages Reference
==========================

Reference documentation for BuildStream pipeline stages, including build stages, deploy stages, and their execution order.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStream pipelines are organized into sequential stages that perform specific tasks in the image creation and deployment process. Pipeline stages are executed in order, with each stage completing before the next begins.

* **Build Pipeline Stages**: create-local-repository, parse-catalog, generate-input-files, build-image
* **Deploy Pipeline Stages**: deploy, restart, validate
* **Stage Dependencies**: Each stage depends on successful completion of previous stages

Build Pipeline Stages
----------------------

Stage 1: create-local-repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Creates and configures the local repository for storing build artifacts and packages.

**Key Actions**:
* Configures local repository settings
* Sets up package storage directories
* Initializes repository metadata
* Configures repository access controls

**Dependencies**: None (first stage)

**Outputs**: Configured local repository ready for package storage

**Failure Impact**: Pipeline cannot proceed without local repository

Stage 2: parse-catalog
~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Parses and validates the catalog file to extract build requirements.

**Key Actions**:
* Reads catalog JSON file
* Validates catalog schema
* Extracts image group definitions
* Validates functional group assignments
* Checks architecture and OS version compatibility

**Dependencies**: create-local-repository

**Outputs**: Parsed and validated catalog data structure

**Failure Impact**: Build requirements cannot be determined without catalog parsing

Stage 3: generate-input-files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Generates input files and configuration data needed for image building.

**Key Actions**:
* Creates Ansible playbook input files
* Generates configuration files for each functional group
* Creates package installation lists
* Generates network configuration files
* Prepares storage configuration files

**Dependencies**: parse-catalog

**Outputs**: Complete set of input files for image building

**Failure Impact**: Image building cannot proceed without generated input files

Stage 4: build-image
~~~~~~~~~~~~~~~~~~~~

**Purpose**: Builds the diskless images based on catalog specifications and generated input files.

**Key Actions**:
* Executes image build playbooks
* Installs specified packages
* Configures system settings
* Creates functional group-specific images
* Generates image metadata

**Dependencies**: generate-input-files

**Outputs**: Built diskless images ready for deployment

**Failure Impact**: Deployment cannot proceed without successfully built images

Deploy Pipeline Stages
----------------------

Stage 1: deploy
~~~~~~~~~~~~~~~

**Purpose**: Deploys built images to target cluster nodes based on PXE mapping file.

**Key Actions**:
* Identifies target nodes from PXE mapping file
* Maps functional groups to image groups
* Copies images to deployment locations
* Configures network boot parameters
* Sets up deployment metadata

**Dependencies**: build-image (from build pipeline)

**Outputs**: Images deployed to target nodes

**Failure Impact**: Nodes cannot boot with deployed images

Stage 2: restart
~~~~~~~~~~~~~~~

**Purpose**: Restarts target nodes to load the deployed images.

**Key Actions**:
* Sends BMC power commands to restart nodes
* Verifies node shutdown
* Initiates PXE boot process
* Monitors node startup progress

**Dependencies**: deploy

**Outputs**: Nodes restarted and booting from deployed images

**Failure Impact**: Nodes may continue running old images or fail to boot

Stage 3: validate
~~~~~~~~~~~~~~~~~

**Purpose**: Validates that nodes successfully booted with the correct deployed images.

**Key Actions**:
* Checks node connectivity
* Verifies running image version
* Validates functional group assignment
* Performs basic system health checks
* Generates validation report

**Dependencies**: restart

**Outputs**: Validation status for each deployed node

**Failure Impact**: Deployment success cannot be confirmed without validation

Stage Execution Order
---------------------

Build Pipeline Execution Order::

    create-local-repository → parse-catalog → generate-input-files → build-image

Deploy Pipeline Execution Order::

    deploy → restart → validate

Complete Pipeline Flow::

    [Build Pipeline]
    create-local-repository → parse-catalog → generate-input-files → build-image
    ↓
    [Deploy Pipeline]
    deploy → restart → validate

Stage State Machine
-------------------

Each pipeline stage progresses through the following states:

* **PENDING**: Stage is queued and waiting to execute
* **RUNNING**: Stage is currently executing
* **COMPLETED**: Stage completed successfully
* **FAILED**: Stage failed with error
* **SKIPPED**: Stage was skipped (conditional execution)

Stage Relationships
--------------------

**Build Stage Dependencies**:
* parse-catalog requires create-local-repository
* generate-input-files requires parse-catalog
* build-image requires generate-input-files

**Deploy Stage Dependencies**:
* deploy requires build-image completion
* restart requires deploy completion
* validate requires restart completion

**Cross-Pipeline Dependencies**:
* Deploy pipeline requires build pipeline completion
* All build stages must complete before deploy stages begin

Troubleshooting by Stage
------------------------

**create-local-repository failures**:
* Check disk space availability
* Verify repository configuration parameters
* Review local_repo_config.yml settings

**parse-catalog failures**:
* Validate catalog JSON syntax
* Verify catalog schema version
* Check functional group names against supported values

**generate-input-files failures**:
* Verify catalog parsing completed successfully
* Check input file generation permissions
* Review configuration file templates

**build-image failures**:
* Verify local repository is accessible
* Check package availability in repository
* Review build playbook logs for specific errors

**deploy failures**:
* Verify PXE mapping file configuration
* Check BMC connectivity from OIM
* Verify image availability for deployment

**restart failures**:
* Verify BMC credentials and permissions
* Check network connectivity to BMCs
* Verify iDRAC firmware versions

**validate failures**:
* Check network connectivity to nodes
* Verify nodes completed boot process
* Review cloud-init logs on target nodes

Related Topics
--------------

* :doc:`../build/executing-build-pipeline` - Execute Build Pipeline
* :doc:`../deploy/executing-deploy-pipeline` - Execute Deploy Pipeline
* :doc:`../../troubleshooting/buildstream/common-pipeline-issues` - Troubleshooting Guide