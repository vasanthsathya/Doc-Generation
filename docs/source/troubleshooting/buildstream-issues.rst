.. _troubleshooting-buildstream-issues:

BuildStreaM Troubleshooting
==========================

.. note::
   This topic is pending SME validation. Content may change before publication.

Common issues and solutions for BuildStreaM build and validation workflows. Use this guide to diagnose and resolve problems with BuildStreaM operations.

.. contents:: On This Page
   :local:
   :depth: 2

BuildStreaM Service Issues
---------------------------

### BuildStreaM API Not Responding

**Symptoms:**
- API requests timeout or return connection errors
- GitLab pipeline cannot connect to BuildStreaM
- Health check endpoint returns 503 status

**Common Causes:**
- BuildStreaM API container not running
- Network connectivity issues
- Authentication service unavailable

**Solutions:**

1. Check BuildStreaM container status:

.. code-block:: bash

   podman ps | grep buildstream

2. Restart BuildStreaM services if needed:

.. code-block:: bash

   podman restart buildstream-api
   podman restart buildstream-db

3. Verify network connectivity:

.. code-block:: bash

   curl -I http://localhost:8080/api/v1/health

4. Check service logs for errors:

.. code-block:: bash

   podman logs buildstream-api --tail 50

**Prevention:**
- Monitor service health with automated alerts
- Set up proper logging and monitoring
- Implement service restart policies

### Database Connection Errors

**Symptoms:**
- API returns 500 errors with database connection messages
- Job submission fails with database errors
- Authentication failures

**Common Causes:**
- PostgreSQL container not running
- Database connection parameters incorrect
- Database disk space exhausted

**Solutions:**

1. Check PostgreSQL container status:

.. code-block:: bash

   podman ps | grep postgres

2. Verify database connectivity:

.. code-block:: bash

   podman exec -it buildstream-db psql -U buildstream -d buildstream -c "SELECT 1;"

3. Check database disk space:

.. code-block:: bash

   podman exec buildstream-db df -h

4. Review database configuration:

.. code-block:: bash

   grep -E "(host|port|database|user)" /opt/omnia/config/buildstream.yaml

**Prevention:**
- Monitor database disk usage
- Set up automated database backups
- Implement connection pooling

Build and Validation Issues
---------------------------

### Catalog Validation Failures

**Symptoms:**
- Job submission fails with catalog validation errors
- Pipeline stops at parse-catalog stage
- Schema validation errors in GitLab CI

**Common Causes:**
- Invalid YAML syntax in catalog
- Missing required fields
- Package version format incorrect
- Circular dependencies in roles

**Solutions:**

1. Validate catalog syntax:

.. code-block:: bash

   python3 -c "import yaml; yaml.safe_load(open('catalog.yaml'))"

2. Use BuildStreaM catalog validator:

.. code-block:: bash

   curl -X POST "http://localhost:8080/api/v1/catalog/validate" \
        -H "Authorization: Bearer <token>" \
        -H "Content-Type: application/json" \
        -d @catalog.yaml

3. Check for circular dependencies:

.. code-block:: bash

   python3 /opt/omnia/buildstream/scripts/check-deps.py catalog.yaml

4. Verify package version format:

.. code-block:: bash

   grep -E "version:" catalog.yaml | grep -v -E "^\d+\.\d+\.\d+"

**Prevention:**
- Use catalog generation scripts
- Implement pre-commit validation hooks
- Test catalogs in development environment

### Build Image Stage Failures

**Symptoms:**
- Pipeline fails at build-image stage
- Image build timeouts
- Insufficient disk space errors
- Package download failures

**Common Causes:**
- Insufficient build resources
- Network connectivity to package repositories
- Disk space exhaustion
- Corrupted package sources

**Solutions:**

1. Check system resources:

.. code-block:: bash

   free -h
   df -h /opt/omnia/artifacts

2. Verify network connectivity:

.. code-block:: bash

   curl -I https://download.rockylinux.org

3. Review build logs for specific errors:

.. code-block:: bash

   curl -H "Authorization: Bearer <token>" \
        "http://localhost:8080/api/v1/jobs/job-id/stages/build-image"

4. Clean up old build artifacts:

.. code-block:: bash

   find /opt/omnia/artifacts -name "*.tmp" -mtime +7 -delete

**Prevention:**
- Monitor resource usage during builds
- Implement build artifact cleanup policies
- Use local package mirrors

### Validation Test Failures

**Symptoms:**
- Pipeline fails at validation stages
- Test timeout errors
- Validation environment issues

**Common Causes:**
- Test environment not properly configured
- Validation test suite errors
- Resource constraints in test environment
- Network connectivity issues in test environment

**Solutions:**

1. Check validation test environment:

.. code-block:: bash

   podman ps | grep testbed

2. Review validation test logs:

.. code-block:: bash

   curl -H "Authorization: Bearer <token>" \
        "http://localhost:8080/api/v1/jobs/job-id/stages/validate-image"

3. Run validation tests manually:

.. code-block:: bash

   cd /opt/omnia/validation/tests
   python3 run_tests.py --role compute-node

4. Check test environment resources:

.. code-block:: bash

   podman exec testbed-node free -h

**Prevention:**
- Regular maintenance of test environment
- Monitor test execution times
- Implement test environment health checks

GitLab Integration Issues
-------------------------

### Pipeline Not Triggering

**Symptoms:**
- Catalog changes don't trigger GitLab pipelines
- GitLab runner not picking up jobs
- Webhook failures

**Common Causes:**
- GitLab runner offline
- Webhook configuration issues
- GitLab CI configuration errors
- Network connectivity between GitLab and BuildStreaM

**Solutions:**

1. Check GitLab runner status:

.. code-block:: bash

   podman ps | grep gitlab-runner

2. Verify runner is online in GitLab UI:
   - Navigate to **Settings** → **CI/CD** → **Runners**
   - Ensure runner shows green status

3. Check webhook configuration:

.. code-block:: bash

   curl -X POST "http://localhost:8080/webhook/test" \
        -H "Content-Type: application/json" \
        -d '{"event": "push"}'

4. Review GitLab CI configuration:

.. code-block:: bash

   cat .gitlab-ci.yml

**Prevention:**
- Monitor runner health
- Test webhook connectivity regularly
- Implement runner failover

### Pipeline Authentication Failures

**Symptoms:**
- Pipeline fails with authentication errors
- BuildStreaM API calls return 401 errors
- Token expiration issues

**Common Causes:**
- OAuth token expired
- Incorrect token configuration
- GitLab runner authentication issues

**Solutions:**

1. Refresh OAuth token:

.. code-block:: bash

   curl -X POST "https://oauth-provider.com/oauth/token" \
        -d "grant_type=client_credentials&client_id=buildstream-client&client_secret=<secret>"

2. Update GitLab CI configuration with new token:

.. code-block:: bash

   gitlab-ci register --non-interactive \
        --url "https://gitlab.example.com" \
        --registration-token "<token>" \
        --executor "shell"

3. Verify token permissions:

.. code-block:: bash

   curl -H "Authorization: Bearer <token>" \
        "https://gitlab.example.com/api/v4/user"

**Prevention:**
- Implement token rotation policies
- Use environment variables for tokens
- Monitor token expiration

Performance Issues
------------------

### Slow Build Performance

**Symptoms:**
- Build stages taking longer than expected
- Resource utilization high
- Build timeouts

**Common Causes:**
- Insufficient system resources
- Network bandwidth limitations
- Large package downloads
- Concurrent build limitations

**Solutions:**

1. Monitor system resources:

.. code-block:: bash

   top
   iostat -x 1
   sar -n DEV 1

2. Optimize build configuration:

.. code-block:: yaml

   build_options:
     parallel_validation: true
     cache_enabled: true
     timeout: 7200

3. Check network performance:

.. code-block:: bash

   iperf3 -c package-repo.example.com

4. Implement build caching:

.. code-block:: bash

   mkdir -p /opt/omnia/cache
   chmod 755 /opt/omnia/cache

**Prevention:**
- Monitor performance metrics
- Implement resource scaling
- Use local package mirrors

### High Memory Usage

**Symptoms:**
- BuildStreaM services consuming excessive memory
- Out of memory errors
- System swapping

**Common Causes:**
- Memory leaks in BuildStreaM services
- Large catalog processing
- Concurrent build operations
- Insufficient system memory

**Solutions:**

1. Monitor memory usage:

.. code-block:: bash

   ps aux --sort=-%mem | head
   podman stats

2. Restart services with memory limits:

.. code-block:: bash

   podman stop buildstream-api
   podman run -d --memory=4g --name buildstream-api buildstream-api:latest

3. Optimize catalog processing:

.. code-block:: yaml

   catalog_processing:
     batch_size: 100
     memory_limit: "2GB"

**Prevention:**
- Set memory limits on containers
- Monitor memory usage trends
- Implement memory leak detection

General Troubleshooting
-----------------------

### Log Analysis

Collect and analyze logs for troubleshooting:

1. System logs:

.. code-block:: bash

   journalctl -u buildstream --since "1 hour ago"

2. Container logs:

.. code-block:: bash

   podman logs buildstream-api --since "1 hour ago"
   podman logs buildstream-db --since "1 hour ago"

3. GitLab runner logs:

.. code-block:: bash

   podman logs gitlab-runner --since "1 hour ago"

4. Application logs:

.. code-block:: bash

   tail -f /opt/omnia/logs/buildstream.log

### Diagnostic Commands

Use these commands for comprehensive diagnostics:

.. code-block:: bash

   # System health check
   /opt/omnia/buildstream/scripts/health-check.sh

   # Service status check
   /opt/omnia/buildstream/scripts/service-status.sh

   # Performance diagnostics
   /opt/omnia/buildstream/scripts/perf-check.sh

### Contact Support

If issues persist after troubleshooting:

1. Collect diagnostic information:

.. code-block:: bash

   /opt/omnia/buildstream/scripts/collect-diagnostics.sh

2. Create support ticket with:
   - BuildStreaM version
   - Error messages and logs
   - System configuration
   - Steps to reproduce

3. Include correlation IDs from API responses for faster resolution.

.. tip::
   Keep a troubleshooting log to track recurring issues and their solutions. This helps identify patterns and prevent future problems.

For additional help, see :doc:`../../buildstream/concept-architecture` and :doc:`../../buildstream/how-to-get-started`.

Related Topics
--------------

* :doc:`../../buildstream/concept-architecture`
* :doc:`../../buildstream/how-to-get-started`
* :doc:`../../buildstream/how-to-gitlab-integration`
* :doc:`../../reference/api/buildstream`
