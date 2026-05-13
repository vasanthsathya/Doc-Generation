.. _how-to-buildstream-validate-pipeline:

Validating Omnia Deployments with BuildStreaM
==============================================

Validate deployed Omnia OS images using the BuildStreaM validate pipeline. This procedure covers the GitLab CI/CD workflow for validating deployments through catalog updates, with an alternative direct API method for advanced users.

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

Validate Pipeline Overview
---------------------------

The BuildStreaM validate pipeline executes automated tests to verify cluster deployment, network connectivity, and service health on provisioned target nodes.

**Validate Stage**

BuildStreaM executes the following validate stage:

.. list-table:: Validate Pipeline Stage
   :widths: 30 70
   :header-rows: 1

   * - Stage
     - Description
   * - ``validate``
     - Runs Molecule-based infrastructure tests on deployed nodes

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

**GitLab CI/CD Workflow**

When using GitLab CI/CD, validation executes automatically as part of the DEPLOY pipeline:

#. **Configure the catalog for deploy pipeline with validation**

   The DEPLOY pipeline includes a Verify stage that runs validation tests automatically. Ensure your catalog is configured with ``pipeline_type: deploy``.

   .. code-block:: json

      {
        "metadata": {
          "pipeline_type": "deploy"
        },
        "images": [
          {
            "name": "rhel-10.0-compute",
            "functional_group": "compute",
            "architecture": "x86_64",
            "os_type": "RHEL",
            "os_version": "10.0",
            "package_type": "image"
          }
        ]
      }

#. **Navigate to GitLab to monitor validation**

   After committing and pushing catalog changes:
   
   #. Navigate to **Build** → **Pipelines** in GitLab
   #. Click on the running pipeline to view validation stage status
   #. Access test artifacts and reports from the pipeline job page

   The validation stage executes automatically after deployment completes, running Molecule-based infrastructure tests on the deployed nodes.

**Alternative: Direct API Access**

For advanced users who require direct API access instead of GitLab CI/CD, see the `BuildStreaM API Documentation <https://developer.dell.com/apis/ea677050-f49b-49e1-a4b9-1cdd563415d9/versions/2.1.0/docs/Introduction.md>`_ for detailed API endpoints and technical specifications.

Verification
------------

After validation completes, verify the results:

#. **Check Pipeline Status**

   Navigate to **Build** → **Pipelines** in GitLab to confirm the pipeline status is ``passed``.

#. **Review Test Results**

   Access test artifacts and reports from the pipeline job page.

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
* :doc:`managing-buildstream-catalogs-and-pipelines`
* :doc:`buildstream-architecture`