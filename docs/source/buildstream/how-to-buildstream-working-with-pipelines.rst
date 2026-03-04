.. _how-to-buildstream-working-with-pipelines:

Working with BuildStreaM Pipelines
==================================

Manage day-to-day BuildStreaM pipeline operations, including modifying catalogs, triggering pipeline execution, and monitoring results. This guide covers the complete workflow from catalog changes to deployment verification.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before working with BuildStreaM pipelines, ensure you have:

* BuildStreaM enabled and configured in Omnia
* GitLab integration set up and operational
* Understanding of catalog structure and definitions
* Access to the GitLab project and repository
* Basic knowledge of CI/CD pipeline concepts

Catalog Modification Workflow
-----------------------------

Modify BuildStreaM catalogs to update your HPC infrastructure configurations.

#. Clone the BuildStreaM GitLab repository.

   .. code-block:: bash

      git clone http://192.168.1.100/omnia-buildstream/omnia-buildstream.git
      cd omnia-buildstream

#. Create a feature branch for your changes.

   .. code-block:: bash

      git checkout -b update-compute-role

   This practice allows you to test changes before affecting production.

#. Edit the catalog file.

   .. code-block:: bash

      vi catalog.yml

   Common catalog modifications include:

   * **Adding new roles**: Define new node types or configurations
   * **Updating package versions**: Upgrade software components
   * **Modifying validation rules**: Add or change test requirements
   * **Adjusting parameters**: Fine-tune configuration values

   Example modification:

   .. code-block:: yaml

      catalog:
        version: "1.1"  # Updated version
        roles:
          - name: "compute-node"
            description: "Standard compute node with GPU support"
            packages:
              - name: "rocky-linux"
                version: "8.9"  # Updated from 8.8
                arch: "x86_64"
              - name: "nvidia-driver"
                version: "535.104"  # New GPU package
                arch: "x86_64"
        validation:
          - name: "gpu-validation"
            type: "hardware"
            required: true

#. Validate catalog syntax.

   .. code-block:: bash

      python scripts/validate_catalog.py catalog.yml

   Expected output for valid catalog:

   .. code-block:: text

      ✓ Catalog syntax is valid
      ✓ All required fields present
      ✓ Package versions available
      ✓ Validation rules properly formatted

#. Commit and push your changes.

   .. code-block:: bash

      git add catalog.yml
      git commit -m "Update catalog: add GPU support to compute role"
      git push origin update-compute-role

#. Create a merge request (optional).

   In GitLab, create a merge request to review changes before merging to main branch.

   This provides additional validation and approval workflow for production changes.

Pipeline Triggering and Monitoring
----------------------------------

Monitor pipeline execution after catalog changes.

#. Observe automatic pipeline trigger.

   After pushing catalog changes, GitLab automatically triggers a new pipeline.

   Navigate to **CI/CD** > **Pipelines** to see the new pipeline execution.

#. Monitor stage execution.

   Click on the running pipeline to view individual stage progress:

   * **local_repo**: Repository setup and package synchronization
   * **build_image**: Container image construction
   * **discovery**: Node discovery and hardware inventory
   * **authentication**: Security configuration and access setup
   * **registration**: Node registration with cluster management

   Each stage shows:
   * Execution status (running, passed, failed)
   * Execution time and resource usage
   * Log output and error messages

#. Review stage details.

   Click on individual stages to view detailed information:

   * **Logs**: Real-time output from stage execution
   * **Artifacts**: Generated files and reports
   * **Dependencies**: Relationship to other stages

   Example stage log output:

   .. code-block:: text

      [build_image] Starting image build for compute-node role
      [build_image] Downloading rocky-linux-8.9 base image
      [build_image] Installing nvidia-driver-535.104
      [build_image] Configuring GPU support
      [build_image] Image build completed successfully
      [build_image] Pushing to registry: registry.company.com/omnia/compute-node:1.1

#. Handle pipeline failures.

   If a stage fails:

   1. **Review error logs**: Click on the failed stage to examine error messages
   2. **Identify root cause**: Look for common issues like package conflicts, network problems, or configuration errors
   3. **Fix the issue**: Update catalog or configuration as needed
   4. **Retry the pipeline**: Use the **Retry** button in GitLab or push a new commit

   Common failure scenarios:
   * **Package not found**: Update package name or version in catalog
   * **Network timeout**: Check connectivity to package repositories
   * **Validation failure**: Fix catalog syntax or validation rules

Manual Pipeline Control
-----------------------

Control pipeline execution manually when automatic triggering is not desired.

#. Pause automatic triggers.

   To prevent automatic pipeline execution during maintenance:

   .. code-block:: yaml

      # In .gitlab-ci.yml
      workflow:
        rules:
          - if: $CI_COMMIT_BRANCH == "main"
            when: manual  # Require manual trigger
          - when: never

#. Trigger manual pipeline execution.

   In GitLab, use the **Run Pipeline** button:

   1. Navigate to **CI/CD** > **Pipelines**
   2. Click **Run Pipeline**
   3. Select branch and variables
   4. Click **Run Pipeline** to start execution

#. Control specific stage execution.

   Use GitLab's manual job controls for selective stage execution:

   .. code-block:: yaml

      build_image:
        stage: build_image
        script:
          - ./scripts/build_image.sh
        when: manual  # Require manual trigger
        allow_failure: true

Pipeline Status Interpretation
-----------------------------

Understand different pipeline states and their meanings.

**Pipeline States**

* **pending**: Waiting for runner to become available
* **running**: Currently executing stages
* **success**: All stages completed successfully
* **failed**: One or more stages failed
* **canceled**: Pipeline was manually stopped
* **skipped**: Pipeline was skipped due to rules or conditions

**Stage States**

* **created**: Stage is created but not started
* **waiting**: Waiting for dependencies or resources
* **running**: Stage is currently executing
* **success**: Stage completed successfully
* **failed**: Stage failed with errors
* **canceled**: Stage was manually canceled

**Status Indicators**

In GitLab UI, status indicators use color coding:

* **Green**: Success or passed
* **Red**: Failure or error
* **Blue**: Running or in progress
* **Gray**: Canceled, skipped, or pending

Deployment Verification
-----------------------

Verify that pipeline deployments are successful and operational.

#. Check deployment status.

   After pipeline completion, verify deployment in your HPC environment:

   .. code-block:: bash

      # Check node status
      omnia-cli nodes list

      Expected output:

      .. code-block:: text

      NODE_NAME      STATUS    ROLE          LAST_SEEN
      compute-01     ready     compute-node  2024-03-04 10:30
      compute-02     ready     compute-node  2024-03-04 10:29
      login-01       ready     login-node    2024-03-04 10:28

#. Validate node functionality.

   Test that deployed nodes are functioning correctly:

   .. code-block:: bash

      # Test connectivity
      ping compute-01

      # Test services
      ssh compute-01 "systemctl status omnia-agent"

      # Test GPU functionality (if applicable)
      ssh compute-01 "nvidia-smi"

#. Review deployment artifacts.

   Access pipeline artifacts for detailed deployment information:

   1. Navigate to pipeline details in GitLab
   2. Click **Download** artifacts for relevant stages
   3. Review deployment logs, configuration files, and test results

   Common artifacts include:
   * **Deployment logs**: Detailed execution logs
   * **Configuration files**: Applied configurations
   * **Test results**: Validation and test outcomes
   * **Inventory files**: Node inventory and status

Advanced Pipeline Operations
----------------------------

Perform advanced pipeline operations for complex scenarios.

#. Rollback failed deployments.

   If a deployment causes issues, rollback to a previous working state:

   .. code-block:: bash

      # Identify previous successful pipeline
      git log --oneline --grep="deploy" | head -5

      # Revert to previous catalog version
      git revert HEAD~1

      # Push rollback
      git push origin main

   The new pipeline will deploy the previous catalog configuration.

#. Perform staged deployments.

   For large environments, use staged deployment approach:

   1. **Development**: Test catalog changes in development environment
   2. **Staging**: Deploy to staging environment for validation
   3. **Production**: Deploy to production after successful staging validation

   Use GitLab environments to manage staged deployments:

   .. code-block:: yaml

      deploy_staging:
        stage: deploy
        script:
          - ./scripts/deploy.sh staging
        environment:
          name: staging
          url: https://staging.omnia.company.com

      deploy_production:
        stage: deploy
        script:
          - ./scripts/deploy.sh production
        environment:
          name: production
          url: https://omnia.company.com
        when: manual

#. Monitor pipeline performance.

   Track pipeline execution metrics to identify optimization opportunities:

   * **Execution time**: Monitor how long pipelines take to complete
   * **Resource usage**: Track CPU, memory, and network utilization
   * **Success rate**: Monitor pipeline success and failure rates
   * **Bottlenecks**: Identify stages that cause delays

   Use GitLab's built-in monitoring or external tools like Prometheus.

Pipeline Optimization
---------------------

Optimize pipeline performance and reliability.

#. Reduce pipeline execution time.

   Strategies to improve pipeline speed:

   * **Cache dependencies**: Cache package downloads and build artifacts
   * **Parallel execution**: Run independent stages in parallel where possible
   * **Optimize catalog size**: Minimize unnecessary package inclusions
   * **Use efficient base images**: Start with optimized base containers

   Example caching configuration:

   .. code-block:: yaml

      cache:
        paths:
          - .cache/
          - downloads/
        key: "$CI_COMMIT_REF_SLUG"

#. Improve reliability.

   Enhance pipeline reliability with these practices:

   * **Idempotent operations**: Ensure stages can be safely retried
   * **Graceful error handling**: Implement proper error recovery
   * **Resource limits**: Set appropriate timeouts and resource constraints
   * **Health checks**: Verify system health before pipeline execution

   Example error handling:

   .. code-block:: yaml

      build_image:
        stage: build_image
        script:
          - ./scripts/build_image.sh || {
              echo "Build failed, cleaning up..."
              ./scripts/cleanup.sh
              exit 1
            }
        timeout: 2h
        retry: 2

.. AI_REVIEW: Pipeline optimization strategies based on CI/CD best practices - verify against specific BuildStreaM performance characteristics

Troubleshooting Common Issues
----------------------------

Resolve common pipeline operational issues.

**Catalog validation failures**

   Symptoms: Pipeline fails at early stages with catalog errors

   Solutions:
   * Validate catalog syntax before committing
   * Check package availability and versions
   * Verify validation rule syntax
   * Review catalog documentation for requirements

**Runner resource exhaustion**

   Symptoms: Pipelines stuck in pending state or fail with resource errors

   Solutions:
   * Monitor runner resource utilization
   * Scale runner resources or add additional runners
   * Optimize pipeline resource usage
   * Implement resource limits and monitoring

**Network connectivity issues**

   Symptoms: Stages fail with timeout or connection errors

   Solutions:
   * Verify network connectivity to external resources
   * Check firewall and security group configurations
   * Implement retry logic for network operations
   * Use local package mirrors when possible

**Authentication failures**

   Symptoms: Pipelines fail with permission or authentication errors

   Solutions:
   * Verify GitLab access tokens are valid
   * Check service account permissions
   * Update expired credentials
   * Review authentication configuration

Best Practices
--------------

Follow these best practices for effective pipeline management:

**Change Management**

* Use feature branches for catalog changes
* Implement peer review for production changes
* Maintain change logs and documentation
* Test changes in development before production

**Monitoring and Alerting**

* Set up alerts for pipeline failures
* Monitor key performance metrics
* Regularly review pipeline execution patterns
* Implement proactive issue detection

**Security**

* Use least-privilege access for service accounts
* Regularly rotate access tokens and credentials
* Audit pipeline configurations and permissions
* Implement security scanning in pipelines

**Documentation**

* Maintain comprehensive catalog documentation
* Document common procedures and troubleshooting steps
* Keep pipeline configurations under version control
* Provide training for team members on BuildStreaM workflows

Related Topics
--------------

* :doc:`concepts-buildstream-catalog`
* :doc:`how-to-buildstream-managing-gitlab-integration`
* :doc:`troubleshooting-buildstream-pipeline-failures`
