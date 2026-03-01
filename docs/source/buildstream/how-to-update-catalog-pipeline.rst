.. _how-to-buildstream-update-catalog-pipeline:

Update Catalog and Check Pipeline
=================================

Update BuildStreaM catalogs and monitor pipeline execution through GitLab. This procedure covers catalog modifications, automatic pipeline triggering, and verification of pipeline status and job execution.

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

1. Go to the GitLab project and open GitLab project.
2. Go to **Code** → **Repository**
3. Locate the catalog file ``catalog_rhel.json``.
4. Modify the ``catalog_rhel.json`` file to define your build requirements.
5. To trigger the pipeline, commit and push catalog changes.
6. Track the pipeline progress through the GitLab web interface:
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

After the pipeline is completed, you can check the overall pipeline status and job execution.

#. Verify job execution.

Check that all jobs are running correctly:

1. Navigate to **Build** → **Jobs**
2. Review the job list and status
3. Click on individual jobs to view:
   - Execution logs
   - Resource usage
   - Error messages (if any)
