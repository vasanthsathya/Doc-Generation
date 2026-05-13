.. _how-to-buildstream-build-pipeline:

Building Omnia Images with BuildStreaM
=======================================

Build Omnia OS images using the BuildStreaM build pipeline. This procedure covers the GitLab CI/CD workflow for building images through catalog updates, with an alternative direct API method for advanced users.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before building images with BuildStreaM:

* Deploy and configure BuildStreaM container on OIM node (see :doc:`prepare_oim_buildstream`)
* Complete GitLab deployment for BuildStreaM (see :doc:`how-to-gitlab-deployment`)
* Verify access to the GitLab project repository
* Ensure input files are available in the build directory

Build Pipeline Overview
-----------------------

The BuildStreaM build pipeline automates the end-to-end image build process through sequential stages:

**Build Stages**

BuildStreaM executes the following build stages in mandatory sequential order:

.. list-table:: Build Pipeline Stages
   :widths: 30 70
   :header-rows: 1

   * - Stage
     - Description
   * - ``create-local-repository``
     - Creates a local package repository from input files via Ansible playbook
   * - ``parse-catalog``
     - Uploads and parses a Dell catalog JSON file to generate adapter policy output
   * - ``build-image``
     - Builds the OS image using the local repository and parsed catalog output

**Sequential Enforcement**

Each stage must complete successfully before the next stage can begin:

```
create-local-repository → MUST be COMPLETED
parse-catalog → MUST be COMPLETED  
build-image → CAN now execute
```

**Pipeline Architecture**

BuildStreaM uses a three-pipeline architecture:

* **BUILD Pipeline** — Prepare → Build → Verify stages
* **DEPLOY Pipeline** — Prepare → Deploy → Verify stages  
* **CLEANUP Pipeline** — Cleanup stage only

The ``pipeline_type`` parameter in the catalog metadata determines which child pipeline is triggered.

Procedure
---------

**GitLab CI/CD Workflow**

#. **Navigate to the GitLab project URL**

   Navigate to:

   .. code-block:: text

      https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

#. **Locate the catalog file**

   Go to **Code** → **Repository** and locate the catalog file ``catalog_rhel.json``.

#. **Configure the catalog for build pipeline**

   Modify the ``catalog_rhel.json`` file to set the pipeline type to build:

   .. code-block:: json

      {
        "metadata": {
          "pipeline_type": "build"
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

   .. note:: Ensure that the catalog file is updated with valid functional group names, architecture types, operating system types and versions, and package types. The pipeline fails if invalid details are provided.

#. **Commit and push catalog changes**

   Commit and push the catalog changes to trigger the BUILD pipeline automatically.

   BuildStreaM uses a three-pipeline architecture (parent router + dynamic child pipelines). The parent pipeline analyzes the catalog and triggers the BUILD child pipeline based on the ``pipeline_type: build`` parameter.

**Alternative: Direct API Access**

For advanced users who require direct API access instead of GitLab CI/CD, see the `BuildStreaM API Documentation <https://developer.dell.com/apis/ea677050-f49b-49e1-a4b9-1cdd563415d9/versions/2.1.0/docs/Introduction.md>`_ for detailed API endpoints and technical specifications.

Verification
------------

After the build pipeline completes, verify the results:

#. **Check Pipeline Status**

   Navigate to **Build** → **Pipelines** in GitLab to confirm the pipeline status is ``passed``.

#. **Review Job Logs**

   Click on individual jobs to view execution logs and resource usage.

Troubleshooting
---------------

**Stage Fails with Prerequisite Error**

If a stage fails with ``STAGE_PREREQUISITE_PENDING``, ensure that all preceding stages have completed successfully before retrying.

**Catalog Validation Error**

If the catalog validation fails, verify that:

* The file has a ``.json`` extension
* The content is valid JSON
* The root element is a dictionary
* All required fields are present

**Immutability Constraint**

A completed build stage cannot be re-run. If you need to rebuild, create a new job.

Related Topics
--------------

* :doc:`how-to-buildstream-deploy-pipeline`
* :doc:`how-to-buildstream-validate-pipeline`
* :doc:`managing-buildstream-catalogs-and-pipelines`
* :doc:`buildstream-architecture`