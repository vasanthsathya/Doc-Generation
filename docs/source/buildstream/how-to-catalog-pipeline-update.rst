.. _how-to-buildstream-catalog-pipeline-update:

Updating BuildStreaM Catalogs and Triggering Pipelines
======================================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Update the BuildStreaM catalog and automatically trigger pipeline execution for image building and deployment. This workflow covers catalog modification, pipeline triggering, execution monitoring, and build verification.

Prerequisites
-------------

Before updating the BuildStreaM catalog:

* Catalog configuration must be complete (see :doc:`how-to-catalog-configuration`)
* GitLab project must be accessible
* BuildStreaM containers must be running
* Previous pipeline execution must have completed successfully

Procedure
---------

1. Navigate to the GitLab code repository.

   .. code-block:: bash

      # Access the GitLab project
      https://<gitlab host ip>/<gitlab project name>

2. Locate the catalog file in the project.

   Click on ``catalog_rhel.json`` to open the catalog editor.

3. Make desired changes to the catalog configuration.

   Common modifications include:
   * Adding new roles or packages
   * Updating package versions
   * Modifying validation dependencies
   * Changing build parameters

   Example: Update a package version:

   .. code-block:: json

      {
        "packages": {
          "slurm-22.05": {
            "type": "cluster_stack",
            "version": "22.05.4",  // Updated from 22.05.3
            "source": "build-from-source",
            "dependencies": ["rhel-8.6"],
            "build_parameters": {
              "configure_options": "--with-pmix=/opt/pmix"
            }
          }
        }
      }

4. Commit changes to the GitLab repository.

   Click **Commit changes** and provide a descriptive commit message:

   .. code-block:: text

      Update Slurm version to 22.05.4 for improved performance

5. Verify automatic pipeline triggering.

   Navigate to **CI/CD** → **Pipelines**. You should see a new pipeline automatically triggered with the status "running".

6. Monitor pipeline execution progress.

   The pipeline executes through these stages:
   * **parse-catalog**: Validates catalog structure and syntax
   * **generate-input-files**: Creates Omnia-compatible input files
   * **prepare-repos**: Sets up local and image repositories
   * **build-image**: Creates stateless image artifacts
   * **validate-image**: Performs static image validation
   * **validate-image-on-test**: Deploys and tests on testbed
   * **promote**: Marks validated images as baseline

7. Check individual job status and logs.

   Click on each job to view:
   * Execution logs
   * Error messages (if any)
   * Resource utilization
   * Completion status

8. Verify build completion and image availability.

   After the pipeline completes successfully:

   a. Check the artifact repository for new images:

      .. code-block:: bash

         # List recent build artifacts
         curl -k https://<buildstream_host>:8080/api/v1/jobs/<job_id>/artifacts

   b. Verify image metadata:

      .. code-block:: bash

         # Check image details
         curl -k https://<buildstream_host>:8080/api/v1/images/<image_id>

9. Troubleshoot common pipeline issues.

   **If parse-catalog fails:**
   * Check JSON syntax in catalog file
   * Verify all package dependencies exist
   * Validate role definitions

   **If build-image fails:**
   * Check repository connectivity
   * Verify build parameters are correct
   * Review build logs for specific errors

   **If validate-image-on-test fails:**
   * Check testbed connectivity
   * Verify test environment resources
   * Review validation test logs

Verification
------------

Verify the catalog update and pipeline execution completed successfully:

1. Confirm pipeline status is "passed".

   .. code-block:: text

      Pipeline #42 passed in 25 minutes

2. Verify all stages completed successfully.

   Each stage should show a green checkmark with no error messages.

3. Check that new images are available.

   .. code-block:: bash

      # List available images
      curl -k https://<buildstream_host>:8080/api/v1/images | jq '.[] | select(.created > "2024-01-01")'

4. Test image deployment (optional).

   Deploy the new image to a test node to verify functionality:

   .. code-block:: bash

      # Deploy test image
      omnia deploy --image <new_image_id> --test-node test01

Result
------

Your BuildStreaM catalog has been successfully updated and the pipeline has executed to build new images according to your specifications. The images are now available for deployment in your Omnia cluster.

Next Steps
----------

* Deploy the new images to production nodes
* Monitor image performance in the cluster
* Update the catalog again for additional changes as needed

**Related topics:**
* :doc:`how-to-catalog-configuration`
* :doc:`how-to-gitlab-deployment`
* :doc:`concept-overview`
