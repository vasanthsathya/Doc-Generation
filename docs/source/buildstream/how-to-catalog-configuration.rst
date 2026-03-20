.. _how-to-buildstream-catalog-configuration:

Step 4: Configuring BuildStreaM Catalogs
=========================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Configure the BuildStreaM catalog to define your software packages, roles, and validation dependencies for automated image building. The catalog serves as the single source of truth for all build requirements and drives the automated pipeline execution.

Prerequisites
-------------

Before configuring the BuildStreaM catalog:

* GitLab deployment must be complete (see :doc:`how-to-gitlab-deployment`)
* You must have access to the GitLab project URL
* BuildStreaM containers must be running and accessible
* Network connectivity to the GitLab instance

Procedure
---------

1. Access the GitLab project code repository.

   .. code-block:: bash

      # Navigate to the GitLab project URL
      https://<gitlab host ip>/<gitlab project name>

2. Locate and examine the default catalog file.

   The project contains a ``catalog_rhel.json`` file with the default BuildStreaM catalog structure. Click on the file to view its contents.

3. Understand the catalog structure.

   The catalog consists of two main layers:

   **Functional Layer**
   * Defines roles that represent target node personas
   * Each role combines: OS + drivers + cluster stack + validation suites
   * Specifies the complete software stack for each node type

   **Package Layer**
   * Contains versioned software components
   * Defines dependencies between packages
   * Specifies build parameters and constraints

4. Modify role definitions for your environment.

   Edit the ``roles`` section in the catalog file:

   .. code-block:: json

      {
        "roles": {
          "compute-node": {
            "description": "HPC compute node with Slurm support",
            "os": "rhel-8.6",
            "drivers": ["nvidia-470", " mellanox-5.4"],
            "cluster_stack": ["slurm-22.05", "openmpi-4.1"],
            "validation_suites": ["hpc-benchmark", "network-test"]
          },
          "login-node": {
            "description": "Login and compilation node",
            "os": "rhel-8.6", 
            "drivers": ["mellanox-5.4"],
            "cluster_stack": ["slurm-22.05-client", "openmpi-4.1"],
            "validation_suites": ["user-access-test"]
          }
        }
      }

5. Update package specifications.

   Edit the ``packages`` section to define your software components:

   .. code-block:: json

      {
        "packages": {
          "rhel-8.6": {
            "type": "os",
            "version": "8.6",
            "source": "rhel-repository",
            "checksum": "sha256:abc123..."
          },
          "nvidia-470": {
            "type": "driver",
            "version": "470.82.01",
            "source": "nvidia-repository",
            "dependencies": ["rhel-8.6"],
            "checksum": "sha256:def456..."
          },
          "slurm-22.05": {
            "type": "cluster_stack",
            "version": "22.05.3",
            "source": "build-from-source",
            "dependencies": ["rhel-8.6"],
            "build_parameters": {
              "configure_options": "--with-pmix=/opt/pmix"
            }
          }
        }
      }

6. Configure validation dependency declarations.

   Define which validation suites must run for each role:

   .. code-block:: json

      {
        "validation_dependencies": {
          "compute-node": {
            "required": ["hpc-benchmark", "network-test"],
            "optional": ["performance-test"]
          },
          "login-node": {
            "required": ["user-access-test"],
            "optional": []
          }
        }
      }

7. Save the catalog file to trigger the pipeline.

   Click **Commit changes** in the GitLab interface to save your modifications. This automatically triggers the BuildStreaM pipeline to process the updated catalog.

Verification
------------

Verify the catalog configuration is working correctly:

1. Check that the pipeline was triggered.

   Navigate to **CI/CD** → **Pipelines** in GitLab. You should see a new pipeline running with the status "running" or "passed".

2. Verify the catalog parsing stage completed successfully.

   In the pipeline view, check that the ``parse-catalog`` job completed without errors.

3. Confirm input files were generated.

   Check the pipeline logs for successful ``generate-input-files`` job completion.

Result
------

Your BuildStreaM catalog is now configured with your custom roles, packages, and validation dependencies. The pipeline will automatically process the catalog and generate the necessary input files for image building.

Next Steps
----------

* Monitor the pipeline execution progress
* Verify image building stages complete successfully
* Update the catalog again to test pipeline modifications

**Related topics:**
* :doc:`concept-overview`
* :doc:`how-to-gitlab-deployment`
* :doc:`how-to-catalog-pipeline-update`
