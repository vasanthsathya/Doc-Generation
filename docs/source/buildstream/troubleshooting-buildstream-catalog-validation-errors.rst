.. _troubleshooting-buildstream-catalog-validation-errors:

Troubleshooting BuildStreaM Catalog Validation Errors
======================================================

Resolve catalog validation errors that prevent BuildStreaM pipeline execution. Catalog validation failures occur when catalog files contain syntax errors, missing required fields, invalid package definitions, or schema violations.

.. contents:: On This Page
   :local:
   :depth: 2

Understanding Catalog Validation
---------------------------------

BuildStreaM enforces strict catalog validation to ensure reliable deployments:

**Validation Stages**

   Catalog validation occurs at multiple stages:

   1. **Syntax Validation**: YAML syntax and structure validation
   2. **Schema Validation**: Compliance with catalog schema definitions
   3. **Package Validation**: Package availability and version verification
   4. **Dependency Validation**: Package dependency resolution
   5. **Architecture Validation**: Hardware and software compatibility checks

**Validation Error Types**

   Common validation error categories:

   * **Syntax Errors**: YAML parsing failures, indentation issues
   * **Schema Errors**: Missing required fields, invalid data types
   * **Package Errors**: Invalid package names, unavailable versions
   * **Dependency Errors**: Unresolvable package dependencies
   * **Architecture Errors**: Unsupported architectures or configurations

Common Validation Error Messages
---------------------------------

**YAML Syntax Errors**

   ``yaml.scanner.ScannerError: while scanning for the next token``
   
   **Cause**: Invalid YAML syntax, typically indentation or formatting issues
   
   **Example**:
   
   .. code-block:: yaml

      # Invalid YAML - inconsistent indentation
      catalog:
        version: "1.0"
          metadata:  # Incorrect indentation
            name: "test-catalog"

   **Solution**: Fix YAML syntax and indentation

**Missing Required Fields**

   ``ValidationError: Missing required field 'version' in catalog``
   
   **Cause**: Required catalog fields are missing or incorrectly named
   
   **Example**:
   
   .. code-block:: yaml

      # Invalid catalog - missing version field
      catalog:
        metadata:
          name: "test-catalog"
        # Missing: version: "1.0"

   **Solution**: Add missing required fields

**Invalid Package Versions**

   ``PackageValidationError: Package 'rocky-linux' version '9.0' not found``
   
   **Cause**: Specified package version does not exist in repositories
   
   **Example**:
   
   .. code-block:: yaml

      # Invalid package version
      packages:
        rocky-linux:
          version: "9.0"  # Version doesn't exist

   **Solution**: Use valid package versions

**Unresolvable Dependencies**

   ``DependencyError: Package 'kubernetes' requires 'containerd' >= 1.6.0``
   
   **Cause**: Package dependencies cannot be resolved with available packages
   
   **Example**:
   
   .. code-block:: yaml

      # Unresolvable dependency
      roles:
        - name: "compute-node"
          packages:
            - name: "kubernetes"
              version: "1.30.0"  # Requires newer containerd
            - name: "containerd"
              version: "1.5.0"   # Too old for kubernetes 1.30.0

   **Solution**: Align package versions to resolve dependencies

Systematic Troubleshooting Process
-----------------------------------

Follow this systematic process to diagnose and fix catalog validation errors:

#. Identify the validation error type.

   Examine the error message to determine the specific validation failure:

   .. code-block:: bash

      # Check pipeline logs for validation errors
      curl -H "Private-Token: [GITLAB_TOKEN]" \
           "http://gitlab.company.com/api/v4/projects/[PROJECT_ID]/jobs/[JOB_ID]/trace"

#. Isolate the problematic catalog section.

   Locate the specific section causing the validation failure:

   .. code-block:: bash

      # Validate specific catalog sections
      python scripts/validate_catalog_section.py catalog.yml roles
      python scripts/validate_catalog_section.py catalog.yml packages

#. Fix the identified issue.

   Apply the appropriate fix based on the error type:

   * **Syntax errors**: Fix YAML formatting and indentation
   * **Schema errors**: Add missing fields or correct data types
   * **Package errors**: Update package names or versions
   * **Dependency errors**: Resolve package version conflicts

#. Re-validate the catalog.

   Test the fix before committing:

   .. code-block:: bash

      python scripts/validate_catalog.py catalog.yml

#. Test the fix in a controlled environment.

   Create a test branch and validate the pipeline:

   .. code-block:: bash

      git checkout -b fix-catalog-validation
      # Apply fixes
      git add catalog.yml
      git commit -m "Fix catalog validation: [description of fix]"
      git push origin fix-catalog-validation

YAML Syntax Issues
------------------

**Common YAML Syntax Problems**

**Indentation Errors**

   **Problem**: Inconsistent or incorrect indentation

   .. code-block:: yaml

      # Incorrect - mixed spaces and tabs
      catalog:
      	  version: "1.0"  # Tab character
        metadata:          # Spaces
          name: "test"

   **Solution**: Use consistent spaces (2 or 4 spaces) for indentation

   .. code-block:: yaml

      # Correct - consistent spaces
      catalog:
        version: "1.0"
        metadata:
          name: "test"

**Quoting Issues**

   **Problem**: Missing quotes around string values

   .. code-block:: yaml

      # Incorrect - unquoted special characters
      catalog:
        version: 1.0.0  # Should be quoted
        description: HPC catalog for production # Should be quoted

   **Solution**: Quote string values, especially those with special characters

   .. code-block:: yaml

      # Correct - properly quoted
      catalog:
        version: "1.0.0"
        description: "HPC catalog for production"

**List Formatting Errors**

   **Problem**: Incorrect list formatting

   .. code-block:: yaml

      # Incorrect - inconsistent list formatting
      packages:
        - name: rocky-linux
          version: "8.8"
        -name: kubernetes  # Missing space after dash
          version: "1.28.2"

   **Solution**: Use consistent list formatting

   .. code-block:: yaml

      # Correct - consistent list formatting
      packages:
        - name: rocky-linux
          version: "8.8"
        - name: kubernetes
          version: "1.28.2"

Schema Validation Issues
------------------------

**Missing Required Fields**

   **Problem**: Required catalog fields are missing

   **Common missing fields**:
   * `version` in catalog metadata
   * `name` in role definitions
   * `packages` in role definitions
   * `type` in validation definitions

   **Solution**: Add all required fields according to the catalog schema

   .. code-block:: yaml

      # Complete catalog structure with all required fields
      catalog:
        version: "1.0"  # Required
        metadata:
          name: "test-catalog"  # Required
          description: "Test catalog for validation"
        roles:
          - name: "compute-node"  # Required
            description: "Compute node configuration"
            packages:  # Required
              - name: "rocky-linux"
                version: "8.8"
            validation:
              - name: "basic-connectivity"  # Required
                type: "network"  # Required
                required: true

**Invalid Data Types**

   **Problem**: Fields contain incorrect data types

   **Example**:
   
   .. code-block:: yaml

      # Incorrect - wrong data types
      catalog:
        version: 1.0  # Should be string
        metadata:
          private: "true"  # Should be boolean
        roles:
          - name: compute-node  # Should be quoted string

   **Solution**: Use correct data types for all fields

   .. code-block:: yaml

      # Correct - proper data types
      catalog:
        version: "1.0"
        metadata:
          private: true
        roles:
          - name: "compute-node"

Package Validation Issues
-------------------------

**Invalid Package Names**

   **Problem**: Package names don't exist in repositories

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check package availability
      yum search rocky-linux
      dnf search kubernetes
      apt-cache search nvidia-driver

   **Solution**: Use correct package names

   .. code-block:: yaml

      # Correct package names
      packages:
        rocky-linux:
          version: "8.8"
        kubernetes:
          version: "1.28.2"
        nvidia-driver:
          version: "535.104"

**Unavailable Package Versions**

   **Problem**: Specified package versions don't exist

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check available versions
      yum --showduplicates list rocky-linux-release
      dnf --showduplicates list kubernetes
      apt-cache policy nvidia-driver

   **Solution**: Use available package versions

   .. code-block:: yaml

      # Use available versions
      packages:
        rocky-linux:
          version: "8.8"  # Available version
        kubernetes:
          version: "1.28.2"  # Available version

**Repository Configuration Issues**

   **Problem**: Package repositories are not accessible

   **Troubleshooting steps**:

   .. code-block:: bash

      # Test repository connectivity
      curl -I http://repo.company.com/rocky/8/BaseOS/
      yum repolist
      dnf repolist

   **Solution**: Fix repository configuration

   .. code-block:: yaml

      # Correct repository configuration
      packages:
        rocky-linux:
          repositories:
            - name: "baseos"
              url: "http://repo.company.com/rocky/8/BaseOS"
              gpg_key: "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial"

Dependency Resolution Issues
---------------------------

**Circular Dependencies**

   **Problem**: Packages have circular dependencies

   **Example**:
   
   .. code-block:: yaml

      # Circular dependency example
      packages:
        package-a:
          dependencies: ["package-b"]
        package-b:
          dependencies: ["package-a"]

   **Solution**: Break circular dependencies or use compatible versions

**Version Conflicts**

   **Problem**: Package versions have conflicting dependencies

   **Example**:
   
   .. code-block:: yaml

      # Version conflict example
      roles:
        - name: "compute-node"
          packages:
            - name: "kubernetes"
              version: "1.30.0"  # Requires containerd >= 1.6.0
            - name: "containerd"
              version: "1.5.0"   # Too old for kubernetes 1.30.0

   **Solution**: Align package versions

   .. code-block:: yaml

      # Aligned versions
      roles:
        - name: "compute-node"
          packages:
            - name: "kubernetes"
              version: "1.28.2"  # Compatible with containerd 1.5.0
            - name: "containerd"
              version: "1.5.0"

Architecture Validation Issues
------------------------------

**Unsupported Architectures**

   **Problem**: Specified architectures are not supported

   **Example**:
   
   .. code-block:: yaml

      # Unsupported architecture
      roles:
        - name: "compute-node"
          architecture: "armv7"  # Not supported

   **Solution**: Use supported architectures

   .. code-block:: yaml

      # Supported architectures
      roles:
        - name: "compute-node"
          architecture: "x86_64"  # Supported

**Hardware Compatibility Issues**

   **Problem**: Package requirements don't match available hardware

   **Example**:
   
   .. code-block:: yaml

      # Hardware compatibility issue
      roles:
        - name: "gpu-compute"
          packages:
            - name: "nvidia-driver"
              version: "535.104"
              requires_gpu: true  # Hardware doesn't have GPU

   **Solution**: Match packages to available hardware

   .. code-block:: yaml

      # Hardware-compatible configuration
      roles:
        - name: "compute-node"  # Non-GPU configuration
          packages:
            - name: "rocky-linux"
              version: "8.8"

Advanced Troubleshooting Techniques
------------------------------------

**Debug Mode Validation**

   Enable detailed validation logging:

   .. code-block:: bash

      # Enable debug validation
      python scripts/validate_catalog.py --debug catalog.yml

   **Partial Validation**

   Validate specific sections to isolate issues:

   .. code-block:: bash

      # Validate specific sections
      python scripts/validate_catalog.py --section roles catalog.yml
      python scripts/validate_catalog.py --section packages catalog.yml

   **Schema Comparison**

   Compare catalog against schema definition:

   .. code-block:: bash

      # Compare with schema
      python scripts/compare_schema.py catalog.yml catalog_schema.json

.. AI_REVIEW: Advanced validation scripts referenced - verify actual script availability and functionality

Preventive Measures
-------------------

**Catalog Validation Tools**

   Use automated validation tools:

   .. code-block:: yaml

      # .pre-commit-config.yaml
      repos:
        - repo: local
          hooks:
            - id: validate-catalog
              name: Validate BuildStreaM catalog
              entry: python scripts/validate_catalog.py
              language: system
              files: catalog\.yml$

**IDE Integration**

   Configure IDE validation for YAML files:

   * Install YAML language server extensions
   * Enable real-time syntax checking
   * Configure schema validation for catalog files

**Pre-commit Hooks**

   Set up pre-commit validation:

   .. code-block:: bash

      # Install pre-commit hooks
      pre-commit install

      # Run validation before commit
      pre-commit run --all-files

**Continuous Integration Validation**

   Add validation to CI/CD pipeline:

   .. code-block:: yaml

      # .gitlab-ci.yml
      validate_catalog:
        stage: validate
        script:
          - python scripts/validate_catalog.py catalog.yml
        rules:
          - changes:
              - catalog.yml

Best Practices
--------------

**Catalog Development**

   * Use YAML linting tools for syntax checking
   * Validate catalogs after each change
   * Test catalogs in development environments
   * Maintain catalog documentation and examples

**Version Control**

   * Use feature branches for catalog changes
   * Implement peer review for catalog updates
   * Maintain change logs for catalog modifications
   * Tag stable catalog versions

**Testing**

   * Test catalogs with multiple scenarios
   * Validate against different architectures
   * Test package availability across repositories
   * Monitor validation performance

**Documentation**

   * Document catalog structure and conventions
   * Maintain examples of common catalog patterns
   * Provide troubleshooting guides for common issues
   * Keep validation error messages clear and actionable

Related Topics
--------------

* :doc:`concepts-buildstream-catalog`
* :doc:`how-to-buildstream-working-with-pipelines`
* :doc:`troubleshooting-buildstream-pipeline-failures`
