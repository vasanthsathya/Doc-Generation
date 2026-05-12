.. _how-to-buildstream-validate-pipeline:

Validating Omnia Deployments with BuildStreaM
==============================================

Validate deployed Omnia OS images using the BuildStreaM validate pipeline. This procedure covers running validation tests, monitoring test execution, and interpreting test results.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before validating deployments with BuildStreaM:

* Complete the deploy pipeline successfully (see :doc:`how-to-buildstream-deploy-pipeline`)
* Verify the image group is in ``RESTARTED`` state
* Ensure target nodes are booted and accessible
* Install Molecule test framework on OIM host (via ``setup_env.sh`` during ``prepare_oim``)
* Clone and configure the automation repository
* Set up OAuth 2.0 client credentials (if OAuth authentication is enabled)

Validate Pipeline Overview
---------------------------

The BuildStreaM validate pipeline executes automated tests to verify cluster deployment, network connectivity, and service health on provisioned target nodes.

**Validate Stage**

BuildStreaM executes the following validate stage:

| Stage | API Endpoint | Description |
|-------|-------------|-------------|
| ``validate`` | ``POST /api/v1/jobs/{job_id}/validate`` | Runs Molecule-based infrastructure tests on deployed nodes |

**Image Group Lifecycle**

The image group transitions through the following states during validation:

```
RESTARTED → VALIDATING → PASSED/FAILED
```

**Test Framework**

BuildStreaM uses Molecule with pytest-testinfra for validation:

* **Molecule** — Test framework for infrastructure testing
* **pytest-testinfra** — Test utility for verifying server state
* **automation_library** — Core test utilities and scenarios
* Test scenarios exist in the automation repository for various functional roles

**Test Execution**

The validate stage:

* Executes minimum basic tests associated with each functional role on deployed nodes
* Tags the image group as ``PASSED`` or ``FAILED`` based on aggregate test results
* A test suite passes only if all individual tests pass; any failure causes the overall status to be ``FAILED``

Procedure
---------

#. **Execute Validation Tests**

   Trigger the validate stage to run automated tests on deployed nodes.

   .. code-block:: bash

      curl -X POST https://<oim_host>:5001/api/v1/jobs/{job_id}/validate \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>" \
        -H "Content-Type: application/json" \
        -d '{
          "test_suite": "basic",
          "timeout": 600
        }'

   | Field | Type | Required | Default | Description |
   |-------|------|----------|---------|-------------|
   | ``test_suite`` | string | No | All basic tests | Specific test suite to run |
   | ``timeout`` | integer | No | System-defined (600s) | Timeout in seconds |

   The image group transitions: ``RESTARTED → VALIDATING``.

   .. code-block:: json

      {
        "job_id": "uuid",
        "stage": "validate",
        "status": "accepted",
        "submitted_at": "2026-04-08T12:00:00Z",
        "correlation_id": "string"
      }

#. **Monitor Validation Progress**

   Query the job status to monitor validation progress.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/jobs/{job_id} \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

   The response shows the current state of the validate stage.

#. **Retrieve Test Results**

   After validation completes, retrieve the test results.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/jobs/{job_id}/artifacts/validate_results \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

   The response includes detailed test results:

   .. code-block:: json

      {
        "job_id": "uuid",
        "test_suite": "basic",
        "overall_status": "PASSED",
        "tests_executed": 15,
        "tests_passed": 15,
        "tests_failed": 0,
        "execution_time_seconds": 420,
        "test_details": [
          {
            "test_name": "network_connectivity",
            "status": "PASSED",
            "execution_time_seconds": 5,
            "message": "All network interfaces are up"
          },
          {
            "test_name": "service_availability",
            "status": "PASSED",
            "execution_time_seconds": 10,
            "message": "All required services are running"
          }
        ],
        "log_path": "/opt/omnia/build_stream_root/artifacts/{job_id}/validate/attempt_1/molecule_output.log",
        "report_path": "/opt/omnia/build_stream_root/artifacts/{job_id}/validate/attempt_1/test_report.html"
      }

#. **Access Detailed Reports**

   Access the detailed test reports and logs for deeper analysis.

   * **Molecule Output Log**: Full stdout/stderr from test execution
   * **Test Report JSON**: Machine-readable test results
   * **Test Report HTML**: Human-readable HTML report
   * **JUnit XML**: JUnit XML format for CI integration

   .. code-block:: bash

      # View molecule output log
      cat /opt/omnia/build_stream_root/artifacts/{job_id}/validate/attempt_1/molecule_output.log

      # Open HTML report in browser
      firefox /opt/omnia/build_stream_root/artifacts/{job_id}/validate/attempt_1/test_report.html

**Alternative: GitLab CI/CD Pipeline**

When using GitLab CI/CD, validation executes automatically as part of the pipeline:

#. The DEPLOY pipeline includes a Verify stage that runs validation tests
#. Navigate to **Build** → **Pipelines** in GitLab
#. Click on the running pipeline to view validation stage status
#. Access test artifacts and reports from the pipeline job page

Verification
------------

After validation completes, verify the results:

#. **Check Image Group Status**

   Confirm that the image group is in ``PASSED`` state.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/images \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

#. **Review Test Summary**

   Review the test summary to ensure all critical tests passed.

   * Check overall status: ``PASSED`` or ``FAILED``
   * Review test execution count and pass/fail ratio
   * Examine execution time to identify performance issues

#. **Analyze Failed Tests**

   If any tests failed, analyze the failure details:

   * Review individual test failure messages
   * Check molecule output log for error details
   * Examine HTML report for test-specific information
   * Verify node state and service status manually if needed

Troubleshooting
---------------

**Validation Stage Not Triggered**

When the validate stage fails with ``UPSTREAM_STAGE_NOT_COMPLETE``, verify that the deploy and restart stages have completed successfully before triggering validation.

**Tests Fail with Connectivity Errors**

When tests fail due to connectivity issues:

* Verify network connectivity between OIM host and target nodes
* Check that SSH authentication is working correctly
* Ensure target nodes are booted and accessible
* Review firewall rules and security group settings

**Molecule Execution Fails**

When Molecule test execution fails:

* Verify that Molecule is installed on the OIM host: ``/opt/omnia/automation/.venv/bin/python3 -m molecule --version``
* Check that the automation repository is correctly cloned
* Review the molecule output log for specific error messages
* Ensure that ``omnia_test_config.yml`` is configured for local execution mode

**Test Timeout**

When tests timeout:

* Increase the ``timeout`` parameter in the validate request
* Review test execution time to identify slow tests
* Check resource utilization on target nodes
* Verify that target nodes are not overloaded

Related Topics
--------------

* :doc:`how-to-buildstream-build-pipeline`
* :doc:`how-to-buildstream-deploy-pipeline`
* :doc:`buildstream-troubleshooting`
* :doc:`how-to-update-catalog-pipeline`
* :doc:`buildstream-architecture`