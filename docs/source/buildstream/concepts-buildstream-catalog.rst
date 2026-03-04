.. _concepts-buildstream-catalog:

BuildStreaM Catalog Management
===============================

The BuildStreaM catalog serves as the single source of truth for defining roles, packages, architectures, and validation dependencies. This catalog-driven approach replaces manual configuration with automated, policy-enforced definitions that drive the entire build lifecycle.

.. contents:: On This Page
   :local:
   :depth: 2

What is a BuildStreaM Catalog
--------------------------------

A BuildStreaM catalog is a structured YAML file that defines all aspects of your HPC infrastructure deployment. It contains:

* **Roles**: Named configurations for different node types (compute, storage, login nodes)
* **Packages**: Software components with specific versions and architectures
* **Validation dependencies**: Tests and checks that must be passed for deployment
* **Architecture definitions**: Hardware and software architecture specifications

The catalog acts as the authoritative source that drives automated pipeline execution, ensuring consistent and repeatable deployments across your infrastructure.

Catalog Structure
------------------

A BuildStreaM catalog follows a hierarchical structure with these main sections:

**Catalog Metadata**

   Basic information about the catalog:

   .. code-block:: yaml

      catalog:
        version: "1.0"
        metadata:
          name: "enterprise-hpc-catalog"
          description: "Enterprise HPC infrastructure catalog"
          author: "infrastructure-team@company.com"
          created: "2024-03-04"
          modified: "2024-03-04"

**Roles Section**

   Defines node configurations and their characteristics:

   .. code-block:: yaml

        roles:
          - name: "compute-node"
            description: "Standard compute node with GPU support"
            architecture: "x86_64"
            packages:
              - name: "rocky-linux"
                version: "8.8"
                source: "baseos"
              - name: "nvidia-driver"
                version: "535.104"
                source: "nvidia"
              - name: "kubernetes"
                version: "1.28.2"
                source: "kubernetes"
            validation:
              - name: "gpu-validation"
                type: "hardware"
                required: true
              - name: "kubernetes-health"
                type: "service"
                required: true

          - name: "storage-node"
            description: "High-performance storage node"
            architecture: "x86_64"
            packages:
              - name: "rocky-linux"
                version: "8.8"
                source: "baseos"
              - name: "beegfs-client"
                version: "7.3.2"
                source: "beegfs"
              - name: "lustre-client"
                version: "2.15.3"
                source: "lustre"

**Packages Section**

   Detailed package definitions and sources:

   .. code-block:: yaml

        packages:
          rocky-linux:
            type: "os"
            architectures: ["x86_64", "aarch64"]
            repositories:
              - name: "baseos"
                url: "http://repo.company.com/rocky/8/BaseOS"
                gpg_key: "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial"
              - name: "appstream"
                url: "http://repo.company.com/rocky/8/AppStream"
                gpg_key: "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial"

          nvidia-driver:
            type: "driver"
            architectures: ["x86_64"]
            repositories:
              - name: "nvidia"
                url: "http://repo.company.com/nvidia/8/x86_64"
                gpg_key: "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-nvidia"

**Validation Section**

   Defines tests and validation requirements:

   .. code-block:: yaml

        validation:
          gpu-validation:
            type: "hardware"
            description: "Validate GPU hardware and drivers"
            test_script: "scripts/validate_gpu.sh"
            timeout: 300
            required: true
          
          kubernetes-health:
            type: "service"
            description: "Validate Kubernetes cluster health"
            test_script: "scripts/validate_k8s.sh"
            timeout: 600
            required: true
            dependencies:
              - "network-connectivity"
              - "dns-resolution"

Catalog as Single Source of Truth
----------------------------------

The catalog serves as the authoritative source for all deployment decisions:

**Policy Enforcement**

   All deployment decisions must reference the catalog:

   * Package versions are specified in catalog definitions
   * Node configurations are defined through catalog roles
   * Validation requirements are enforced through catalog rules
   * Architecture constraints are defined in catalog specifications

**Consistency Guarantees**

   The catalog ensures deployment consistency:

   * All nodes of the same role receive identical configurations
   * Package versions are consistent across the infrastructure
   * Validation requirements are uniformly applied
   * Architecture compliance is automatically enforced

**Change Management**

   Catalog changes follow a controlled process:

   1. **Modification**: Update catalog definitions in GitLab repository
   2. **Validation**: Automated catalog validation checks syntax and structure
   3. **Pipeline Trigger**: Changes automatically trigger deployment pipelines
   4. **Deployment**: Updated configurations are applied to infrastructure
   5. **Verification**: Validation tests ensure successful deployment

Catalog-Driven Pipeline Execution
---------------------------------

Catalog changes automatically trigger BuildStreaM pipeline execution:

**Trigger Mechanisms**

   Pipeline execution is triggered by:

   * **Commits to catalog files**: Any change to catalog.yml triggers pipeline
   * **Merge requests**: Changes merged to main branch trigger deployment
   * **Manual triggers**: Administrators can manually trigger pipeline execution
   * **Scheduled triggers**: Regular pipeline execution for maintenance and updates

**Stage Execution**

   Pipeline stages use catalog information:

   * **Parse Catalog**: Catalog definitions are parsed and validated
   * **Generate Input Files**: Catalog data is converted to deployment inputs
   * **Build Image**: Images are built according to catalog package definitions
   * **Validate Image**: Images are validated against catalog requirements
   * **Deploy**: Infrastructure is configured according to catalog roles

**Validation Integration**

   Catalog validation rules are integrated throughout the pipeline:

   * **Schema Validation**: Catalog structure is validated against defined schemas
   * **Package Validation**: Package availability and versions are verified
   * **Dependency Validation**: Package dependencies are checked for conflicts
   * **Architecture Validation**: Hardware compatibility is verified

Catalog Validation Requirements
-------------------------------

BuildStreaM enforces strict catalog validation to ensure reliability:

**Schema Validation**

   Catalog files must conform to defined schemas:

   .. code-block:: yaml

      # Schema validation rules
      required_fields:
        catalog: ["version", "metadata", "roles"]
        roles: ["name", "description", "packages"]
        packages: ["name", "version", "source"]
        validation: ["name", "type", "required"]

      field_validation:
        version: "semantic_version_pattern"
        architecture: "supported_architectures"
        package_source: "valid_repository_url"

**Package Availability**

   All specified packages must be available:

   * Repository accessibility is verified
   * Package versions must exist in repositories
   * Package dependencies must be resolvable
   * Architecture compatibility is validated

**Validation Rule Compliance**

   Validation rules must be properly defined:

   * Test scripts must exist and be executable
   * Timeout values must be reasonable
   * Required validations must have corresponding tests
   * Validation dependencies must be resolvable

Catalog Management Best Practices
---------------------------------

Follow these best practices for effective catalog management:

**Version Control**

   * Maintain catalog version numbers using semantic versioning
   * Use descriptive commit messages for catalog changes
   * Create feature branches for significant catalog updates
   * Tag releases for stable catalog versions

**Modular Design**

   * Split large catalogs into manageable modules
   * Use inheritance for common package sets
   * Create reusable validation rule definitions
   * Maintain separate catalogs for different environments

**Documentation**

   * Document catalog structure and conventions
   * Maintain change logs for catalog updates
   * Provide examples for common configuration patterns
   * Document validation requirements and test procedures

**Testing and Validation**

   * Test catalog changes in development environments
   * Validate catalog syntax before committing changes
   * Run comprehensive validation tests
   * Monitor pipeline execution for catalog-related issues

**Security and Compliance**

   * Review catalog changes for security implications
   * Validate package sources and integrity
   * Ensure compliance with organizational policies
   * Regularly audit catalog contents and dependencies

Catalog Examples
----------------

**Basic Compute Node Catalog**

   .. code-block:: yaml

      catalog:
        version: "1.0"
        metadata:
          name: "basic-compute-catalog"
          description: "Basic compute node configuration"
        
        roles:
          - name: "compute-node"
            description: "Basic compute node"
            packages:
              - name: "rocky-linux"
                version: "8.8"
              - name: "kubernetes"
                version: "1.28.2"
            validation:
              - name: "basic-connectivity"
                type: "network"
                required: true

**Advanced GPU Compute Catalog**

   .. code-block:: yaml

      catalog:
        version: "2.0"
        metadata:
          name: "gpu-compute-catalog"
          description: "GPU-enabled compute node configuration"
        
        roles:
          - name: "gpu-compute"
            description: "High-performance GPU compute node"
            packages:
              - name: "rocky-linux"
                version: "8.8"
              - name: "nvidia-driver"
                version: "535.104"
              - name: "cuda-toolkit"
                version: "12.2"
              - name: "kubernetes"
                version: "1.28.2"
              - name: "nvidia-device-plugin"
                version: "0.14"
            validation:
              - name: "gpu-hardware-check"
                type: "hardware"
                required: true
              - name: "cuda-compatibility"
                type: "software"
                required: true
              - name: "kubernetes-gpu-integration"
                type: "integration"
                required: true

Catalog Troubleshooting
-----------------------

**Common Catalog Issues**

   **Syntax Errors**
   
   Symptoms: Pipeline fails with YAML parsing errors
   
   Solutions:
   * Validate YAML syntax before committing
   * Use YAML linting tools
   * Check for proper indentation and spacing

   **Package Not Found**
   
   Symptoms: Pipeline fails during package installation
   
   Solutions:
   * Verify package names and versions
   * Check repository accessibility
   * Update package sources in catalog

   **Validation Failures**
   
   Symptoms: Pipeline fails during validation stage
   
   Solutions:
   * Check validation script existence and permissions
   * Verify validation rule definitions
   * Review validation dependencies

**Debugging Techniques**

   Use these techniques to debug catalog issues:

   .. code-block:: bash

      # Validate catalog syntax
      python -c "import yaml; yaml.safe_load(open('catalog.yml'))"
      
      # Check package availability
      python scripts/check_packages.py catalog.yml
      
      # Test validation rules
      python scripts/test_validation.py catalog.yml

.. AI_REVIEW: Catalog validation scripts referenced - verify actual script availability and functionality

Related Topics
--------------

* :doc:`overview-buildstream`
* :doc:`how-to-buildstream-working-with-pipelines`
* :doc:`troubleshooting-buildstream-catalog-validation-errors`
