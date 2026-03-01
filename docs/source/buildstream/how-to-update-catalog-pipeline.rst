.. _how-to-buildstream-update-catalog-pipeline:

Update Catalog and Check Pipeline
=================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Update BuildStreaM catalogs and monitor pipeline execution through GitLab. This procedure covers catalog modifications, automatic pipeline triggering, and verification of pipeline status and job execution.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before updating catalogs and checking pipelines:

* GitLab deployment completed (see :doc:`how-to-gitlab-deployment`)
* BuildStreaM configuration completed (see :doc:`how-to-prepare-buildstream`)
* Access to GitLab project repository
* Understanding of catalog file structure
* GitLab web interface access

Procedure
---------

#. Access the GitLab project repository.

Navigate to the GitLab project and access the repository files:

1. Open GitLab project: https://gitlab.example.com/omnia-catalog
2. Go to **Check** → **Code** → **Repository**
3. Locate the catalog files (catalog_rhel.json and others)

#. Review current catalog structure.

Examine the existing catalog file to understand the current configuration:

.. code-block:: json

   {
     "catalog_version": "1.0",
     "description": "BuildStreaM catalog for RHEL-based images",
     "roles": [
       {
         "name": "compute-node",
         "description": "Standard compute node configuration",
         "packages": [
           {
             "name": "rocky-linux",
             "version": "8.8",
             "type": "os"
           },
           {
             "name": "slurm",
             "version": "23.02",
             "type": "scheduler"
           }
         ]
       }
     ]
   }

.. note::
   The catalog structure defines roles, packages, and build requirements for your HPC cluster images.

#. Update catalog files.

Modify the catalog_rhel.json file to define your build requirements:

.. code-block:: bash

   # Clone the repository locally for editing
   git clone https://gitlab.example.com/omnia-catalog.git
   cd omnia-catalog

   # Edit the catalog file
   vim catalog_rhel.json

Example updates:

.. code-block:: json

   {
     "catalog_version": "1.1",
     "description": "Updated BuildStreaM catalog with additional packages",
     "roles": [
       {
         "name": "compute-node",
         "description": "Enhanced compute node with additional software",
         "packages": [
           {
             "name": "rocky-linux",
             "version": "8.8",
             "type": "os"
           },
           {
             "name": "slurm",
             "version": "23.02.4",
             "type": "scheduler"
           },
           {
             "name": "openmpi",
             "version": "4.1.5",
             "type": "mpi"
           }
         ]
       },
       {
         "name": "management-node",
         "description": "Cluster management and control plane",
         "packages": [
           {
             "name": "rocky-linux",
             "version": "8.8",
             "type": "os"
           },
           {
             "name": "kubernetes",
             "version": "1.28.2",
             "type": "container-runtime"
           }
         ]
       }
     ]
   }

#. Commit and push catalog changes.

Save your changes and push them to trigger the pipeline:

.. code-block:: bash

   # Add the updated catalog
   git add catalog_rhel.json

   # Commit the changes
   git commit -m "Update catalog version 1.1 - add management node and openmpi"

   # Push to trigger pipeline
   git push origin main

.. tip::
   Any change to catalog files automatically triggers the BuildStreaM pipeline.

#. Monitor pipeline execution.

Track the pipeline progress through the GitLab web interface:

1. Navigate to **Build** → **Pipeline**
2. Click on the running pipeline to view details
3. Monitor each stage as it progresses:
   - **parse-catalog** - Validates catalog structure
   - **generate-input-files** - Creates build inputs
   - **prepare-repos** - Sets up repositories
   - **build-image** - Builds the images
   - **validate-image** - Runs validation tests

Expected pipeline status indicators:
- **Green checkmark**: Stage completed successfully
- **Red X**: Stage failed (click for error details)
- **Blue circle**: Stage currently running

#. Verify job execution.

Check that all jobs are running correctly:

1. Navigate to **Build** → **Jobs**
2. Review the job list and status
3. Click on individual jobs to view:
   - Execution logs
   - Resource usage
   - Error messages (if any)

Expected job output:

.. code-block:: text

   Job #1234
   Status: success
   Duration: 15m 32s
   Runner: gitlab-runner-podman

   Job log:
   [INFO] Starting BuildStreaM pipeline execution
   [INFO] Parsing catalog: catalog_rhel.json
   [INFO] Catalog validation successful
   [INFO] Generating input files for role: compute-node
   [INFO] Building image: compute-node-v1.1
   [INFO] Build completed successfully
   [INFO] Running validation tests
   [INFO] All tests passed

#. Review build artifacts.

Access the build artifacts generated by the pipeline:

1. Go to the pipeline details page
2. Click on **Download artifacts** if available
3. Review the generated files:
   - Build logs
   - Image manifests
   - Validation reports
   - SBOM (Software Bill of Materials)

Result
------

Your catalog has been updated and the BuildStreaM pipeline has executed successfully. The system has processed your catalog changes and built the specified images according to your requirements.

Verification
------------

Verify the catalog update and pipeline execution:

#. Check pipeline completion status:

.. code-block:: bash

   # Verify pipeline completed successfully
   curl -H "Authorization: Bearer <token>" \
        "https://gitlab.example.com/api/v4/projects/omnia-catalog/pipelines" | \
        jq '.[] | select(.status == "success")'

#. Validate catalog syntax:

.. code-block:: bash

   # Test catalog JSON syntax
   jq empty catalog_rhel.json

Expected output shows no syntax errors and successful pipeline completion.

#. Verify build artifacts:

.. code-block:: bash

   # Check if build artifacts exist
   ls -la /opt/omnia/artifacts/buildstream/

Expected output shows build artifacts:

.. code-block:: text

   job-20240301-001/
   ├── compute-node.img
   ├── management-node.img
   ├── validation-report.json
   └── build-manifest.json

Next Steps
----------

After successful catalog update and pipeline execution:

* **Test images** - Deploy the built images to test environments
* **Monitor performance** - Track build times and resource usage
* **Update other catalogs** - Apply similar changes to other catalog files
* **Set up monitoring** - Configure alerts for pipeline failures

.. caution::
   If a pipeline stage fails, review the job logs for error messages and fix the underlying issue before re-triggering the pipeline.

For GitLab deployment procedures, see :doc:`how-to-gitlab-deployment`.

Related Topics
--------------

* :doc:`concept-overview`
* :doc:`how-to-prepare-buildstream`
* :doc:`how-to-gitlab-deployment`
