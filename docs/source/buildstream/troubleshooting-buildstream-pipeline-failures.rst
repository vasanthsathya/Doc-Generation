.. _troubleshooting-buildstream-pipeline-failures:

Troubleshooting BuildStreaM Pipeline Failures
===============================================

Diagnose and resolve common BuildStreaM pipeline failures, including identifying failed stages, reading error logs, and taking corrective action. This guide helps you systematically troubleshoot pipeline issues and restore normal operations.

.. contents:: On This Page
   :local:
   :depth: 2

Common Pipeline Failure Symptoms
--------------------------------

BuildStreaM pipeline failures typically manifest in these ways:

**Pipeline stuck in pending state**
* Pipeline never starts execution
* Runner shows as offline or busy
* Jobs remain in queued status indefinitely

**Stage execution failures**
* One or more stages fail with error messages
* Pipeline stops at specific stage
* Subsequent stages are not executed

**Infrastructure connectivity issues**
* Network timeouts during stage execution
* Authentication failures with external services
* Resource exhaustion or unavailability

**Catalog-related failures**
* Catalog validation errors
* Package download failures
* Configuration syntax errors

Systematic Troubleshooting Approach
-----------------------------------

Follow this systematic approach to diagnose and resolve pipeline failures.

#. Identify the failure point.

   Navigate to your GitLab project and examine the pipeline status:

   1. Go to **CI/CD** > **Pipelines**
   2. Click on the failed pipeline
   3. Identify which stage failed and note the error message

#. Collect diagnostic information.

   Gather relevant information for troubleshooting:

   .. code-block:: bash

      # Pipeline details
      curl -H "Private-Token: [GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/projects/[PROJECT_ID]/pipelines/[PIPELINE_ID]"

      # Job details
      curl -H "Private-Token: [GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/projects/[PROJECT_ID]/jobs/[JOB_ID]"

      # Runner status
      curl -H "Private-Token: [GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/runners"

#. Analyze error patterns.

   Review error logs to identify patterns and root causes:

   * **Recurring errors**: Same error across multiple pipelines
   * **Intermittent failures**: Errors that occur sporadically
   * **Environment-specific**: Failures only in certain environments

#. Implement corrective actions.

   Apply appropriate fixes based on the identified issue:

   * **Configuration fixes**: Update catalog or pipeline configuration
   * **Infrastructure fixes**: Resolve network or resource issues
   * **Authentication fixes**: Update credentials or permissions

Pipeline Stuck in Pending State
--------------------------------

**Symptoms**: Pipeline created but never starts execution, jobs remain in queued status.

**Causes and Solutions**:

**GitLab runner offline**

   Check runner status:

   .. code-block:: bash

      curl -H "Private-Token: [GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/runners"

   If runner is offline:

   .. code-block:: bash

      # Restart GitLab runner service
      sudo systemctl restart gitlab-runner

      # Check runner logs
      sudo journalctl -u gitlab-runner -f

   Verify runner configuration:

   .. code-block:: bash

      sudo gitlab-runner list
      sudo gitlab-runner verify

**Insufficient runner resources**

   Monitor runner resource utilization:

   .. code-block:: bash

      # Check system resources
      top
      free -h
      df -h

   Scale runner resources:

   .. code-block:: bash

      # Update runner configuration
      sudo vi /etc/gitlab-runner/config.toml

   Add resource limits:

   .. code-block:: toml

      [[runners]]
        name = "buildstream-runner"
        url = "http://192.168.1.100/"
        token = "[RUNNER_TOKEN]"
        executor = "docker"
        [runners.docker]
          memory = "4g"
          memory_swap = "4g"
          cpus = "2"

**Network connectivity issues**

   Test connectivity between GitLab and runner:

   .. code-block:: bash

      # Test GitLab connectivity
      ping 192.168.1.100
      telnet 192.168.1.100 443

   # Test DNS resolution
      nslookup 192.168.1.100

   Check firewall rules:

   .. code-block:: bash

      sudo iptables -L -n
      sudo ufw status

Stage Execution Failures
------------------------

**Symptoms**: Pipeline starts but fails at specific stage with error messages.

**Local Repo Stage Failures**

   **Common errors**:
   * Repository creation failures
   * Package synchronization issues
   * Network connectivity to package repositories

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check repository access
      curl -I http://repo.company.com/
      
      # Test package availability
      yum repolist
      dnf repolist

   **Solutions**:
   * Update repository URLs in catalog
   * Check network connectivity to repositories
   * Verify repository authentication credentials

**Build Image Stage Failures**

   **Common errors**:
   * Base image download failures
   * Package installation conflicts
   * Insufficient disk space during build

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check disk space
      df -h /var/lib/docker
      
      # Test base image pull
      docker pull rockylinux:8.8
      
      # Check Docker daemon status
      sudo systemctl status docker

   **Solutions**:
   * Clean up unused Docker images and containers
   * Increase disk space for build operations
   * Fix package conflicts in catalog definitions

**Discovery Stage Failures**

   **Common errors**:
   * Node connectivity issues
   * BMC (Baseboard Management Controller) access problems
   * Hardware inventory failures

   **Troubleshooting steps**:

   .. code-block:: bash

      # Test node connectivity
      ping compute-01
      
      # Check BMC access
      ipmitool -I lanplus -H 192.168.1.50 -U admin -P password power status

   **Solutions**:
   * Verify network connectivity to target nodes
   * Check BMC credentials and permissions
   * Ensure nodes are powered on and accessible

**Authentication Stage Failures**

   **Common errors**:
   * Certificate validation failures
   * Authentication service unavailable
   * Permission denied errors

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check certificate validity
      openssl x509 -in /etc/ssl/certs/omnia.crt -text -noout
      
      # Test authentication service
      curl -k https://localhost:8080/api/v1/health

   **Solutions**:
   * Update expired certificates
   * Restart authentication services
   * Verify service account permissions

Catalog-Related Failures
------------------------

**Symptoms**: Pipeline fails early with catalog validation or syntax errors.

**Catalog Validation Errors**

   **Common errors**:
   * YAML syntax errors
   * Missing required fields
   * Invalid package versions

   **Troubleshooting steps**:

   .. code-block:: bash

      # Validate catalog syntax
      python -c "import yaml; yaml.safe_load(open('catalog.yml'))"
      
      # Check catalog structure
      python scripts/validate_catalog.py catalog.yml

   **Solutions**:
   * Fix YAML syntax errors
   * Add missing required fields
   * Update package versions to available versions

**Package Download Failures**

   **Common errors**:
   * Package not found in repositories
   * Network timeouts during download
   * Authentication failures with package repositories

   **Troubleshooting steps**:

   .. code-block:: bash

      # Test package availability
      yum info rocky-linux-release
      dnf search kubernetes
      
      # Test repository access
      curl -I http://repo.company.com/rocky/8/BaseOS/x86_64/os/

   **Solutions**:
   * Update package names and versions in catalog
   * Check repository connectivity and authentication
   * Use alternative repositories or mirrors

Infrastructure Connectivity Issues
---------------------------------

**Symptoms**: Intermittent failures, timeout errors, network-related issues.

**Network Timeouts**

   **Troubleshooting steps**:

   .. code-block:: bash

      # Test network connectivity
      ping -c 4 8.8.8.8
      traceroute 192.168.1.100
      
      # Check network latency
      mtr 192.168.1.100

   **Solutions**:
   * Increase timeout values in pipeline configuration
   * Optimize network routing and configuration
   * Use local package mirrors to reduce latency

**Service Unavailability**

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check service status
      sudo systemctl status omnia-api
      sudo systemctl status gitlab-runsvr
      
      # Check port availability
      netstat -tlnp | grep :8080
      ss -tlnp | grep :443

   **Solutions**:
   * Restart failed services
   * Check service logs for error details
   * Verify service dependencies are running

Authentication and Authorization Issues
--------------------------------------

**Symptoms**: Permission denied errors, authentication failures, access control issues.

**GitLab Token Issues**

   **Troubleshooting steps**:

   .. code-block:: bash

      # Test GitLab API access
      curl -H "Private-Token: [TOKEN]" "http://192.168.1.100/api/v4/user"
      
      # Check token expiration
      curl -H "Private-Token: [TOKEN]" "http://192.168.1.100/api/v4/personal_access_tokens"

   **Solutions**:
   * Regenerate expired or invalid tokens
   * Update BuildStreaM configuration with new tokens
   * Verify token has required permissions (api scope)

**Service Account Permissions**

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check service account permissions
      kubectl auth can-i create pods --as=system:serviceaccount:omnia:buildstream
      
      # Test API access
      curl -k -H "Authorization: Bearer [TOKEN]" https://localhost:8080/api/v1/jobs

   **Solutions**:
   * Update service account permissions
   * Grant required roles and permissions
   * Verify RBAC configuration

Resource Exhaustion Issues
--------------------------

**Symptoms**: Pipeline failures due to insufficient resources, memory errors, disk space issues.

**Memory Issues**

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check memory usage
      free -h
      cat /proc/meminfo
      
      # Monitor process memory
      ps aux --sort=-%mem | head

   **Solutions**:
   * Increase available memory
   * Optimize pipeline memory usage
   * Add swap space if needed

**Disk Space Issues**

   **Troubleshooting steps**:

   .. code-block:: bash

      # Check disk usage
      df -h
      du -sh /var/lib/docker
      
      # Clean up old artifacts
      docker system prune -a

   **Solutions**:
   * Clean up unused files and containers
   * Increase disk space
   * Implement artifact cleanup policies

Advanced Troubleshooting Techniques
------------------------------------

**Pipeline Debug Mode**

   Enable debug logging for detailed troubleshooting:

   .. code-block:: yaml

      # In .gitlab-ci.yml
      variables:
        DEBUG: "true"
        LOG_LEVEL: "debug"

   **Manual Stage Execution**

   Run individual stages manually for isolated testing:

   .. code-block:: bash

      # Execute specific stage
      gitlab-runner exec docker build_image

   **Health Check Automation**

   Implement automated health checks:

   .. code-block:: bash

      #!/bin/bash
      # health_check.sh
      
      # Check BuildStreaM API
      if ! curl -f -s https://localhost:8080/api/v1/health > /dev/null; then
          echo "BuildStreaM API unhealthy"
          exit 1
      fi
      
      # Check GitLab runner
      if ! gitlab-runner list > /dev/null; then
          echo "GitLab runner unavailable"
          exit 1
      fi
      
      echo "All systems healthy"

Preventive Measures
-------------------

Implement these preventive measures to reduce pipeline failures:

**Regular Health Monitoring**

   Set up automated health checks:

   .. code-block:: yaml

      # health_check_pipeline.yml
      stages:
        - health_check
      
      health_check:
        stage: health_check
        script:
          - ./scripts/health_check.sh
        schedule:
          - cron: "0 */6 * * *"  # Every 6 hours

**Resource Monitoring**

   Monitor system resources and set alerts:

   * CPU utilization > 80%
   * Memory usage > 90%
   * Disk space < 10%
   * Network latency > 100ms

**Configuration Validation**

   Validate configurations before deployment:

   .. code-block:: bash

      # Pre-deployment validation
      python scripts/validate_config.py
      python scripts/validate_catalog.py
      python scripts/test_connectivity.py

**Backup and Recovery**

   Maintain backups of critical configurations:

   * Catalog files
   * Pipeline configurations
   * Service credentials
   * System configurations

Escalation Procedures
---------------------

Follow these escalation procedures for persistent issues:

**Level 1: Basic Troubleshooting**
* Apply common fixes from this guide
* Restart services and clear caches
* Verify basic connectivity and permissions

**Level 2: Advanced Investigation**
* Collect detailed logs and diagnostics
* Review system performance metrics
* Test with minimal configurations

**Level 3: SME Escalation**
* Contact BuildStreaM development team
* Provide complete diagnostic information
* Document issue reproduction steps

**Information to Collect for Escalation**

When escalating issues, collect this information:

.. code-block:: bash

   # System information
   uname -a
   cat /etc/os-release
   
   # Service status
   sudo systemctl status omnia-api
   sudo systemctl status gitlab-runner
   
   # Recent logs
   sudo journalctl -u omnia-api --since "1 hour ago"
   sudo journalctl -u gitlab-runner --since "1 hour ago"
   
   # Pipeline details
   curl -H "Private-Token: [TOKEN]" \
       "http://192.168.1.100/api/v4/projects/[PROJECT_ID]/pipelines/[PIPELINE_ID]"

Related Topics
--------------

* :doc:`how-to-buildstream-working-with-pipelines`
* :doc:`how-to-buildstream-managing-gitlab-integration`
* :doc:`concepts-buildstream-architecture`
