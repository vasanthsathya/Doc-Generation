.. _how-to-buildstream-deploy-pipeline:

Deploying Omnia Images with BuildStreaM
========================================

Deploy built Omnia OS images to target nodes using the BuildStreaM deploy pipeline. This procedure covers the GitLab CI/CD workflow for deploying images through catalog updates, with an alternative direct API method for advanced users.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before deploying images with BuildStreaM:

* Complete the build pipeline successfully (see :doc:`how-to-buildstream-build-pipeline`)
* Verify the image group is in ``BUILT`` state
* Ensure target nodes are discovered and available in the inventory
* Configure PXE boot infrastructure

Deploy Pipeline Overview
------------------------

The BuildStreaM deploy pipeline manages image deployment through sequential stages:

**Deploy Stages**

BuildStreaM executes the following deploy stages:

.. list-table:: Deploy Pipeline Stages
   :widths: 30 70
   :header-rows: 1

   * - Stage
     - Description
   * - ``deploy``
     - Deploys built images to target nodes via Ansible playbook
   * - ``pxe_boot``
     - PXE boots target nodes after image deployment

**Image Group Lifecycle**

The image group transitions through the following states during deployment:

```
BUILT → DEPLOYING → DEPLOYED → RESTARTING → RESTARTED
```

**Sequential Enforcement**

Each deploy stage must complete successfully before the next stage can begin:

```
deploy → MUST be COMPLETED
pxe_boot → CAN now execute
```

**Pipeline Architecture**

The deploy pipeline is part of the BuildStreaM three-pipeline architecture:

* **DEPLOY Pipeline** — Prepare → Deploy → Verify stages
* The ``pipeline_type`` parameter in the catalog metadata triggers the DEPLOY pipeline

Procedure
---------

**GitLab CI/CD Workflow**

#. **Navigate to the GitLab project URL**

   Navigate to:

   .. code-block:: text

      https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

#. **Locate the catalog file**

   Go to **Code** → **Repository** and locate the catalog file ``catalog_rhel.json``.

#. **Configure the catalog for deploy pipeline**

   Modify the ``catalog_rhel.json`` file to set the pipeline type to deploy:

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

#. **Commit and push catalog changes**

   Commit and push the catalog changes to trigger the DEPLOY pipeline automatically.

   BuildStreaM uses a three-pipeline architecture (parent router + dynamic child pipelines). The parent pipeline analyzes the catalog and triggers the DEPLOY child pipeline based on the ``pipeline_type: deploy`` parameter.

**Alternative: Direct API Access**

For advanced users who require direct API access instead of GitLab CI/CD, see the `BuildStreaM API Documentation <https://developer.dell.com/apis/ea677050-f49b-49e1-a4b9-1cdd563415d9/versions/2.1.0/docs/Introduction.md>`_ for detailed API endpoints and technical specifications.

Verification
------------

After the deploy pipeline completes, verify the deployment:

#. **Check Pipeline Status**

   Navigate to **Build** → **Pipelines** in GitLab to confirm the pipeline status is ``passed``.

#. **Review Job Logs**

   Click on individual jobs to view execution logs and resource usage.

Troubleshooting
---------------

**Image Group Not Deployable**

When deployment fails with ``IMAGE_NOT_DEPLOYABLE``, verify that the image group is in ``BUILT`` state before attempting deployment.

**Image Already Deployed**

When you receive ``IMAGE_ALREADY_DEPLOYED``, re-deploying an image group that is already in ``DEPLOYED`` state is not permitted. Create a new deployment with a new build.

**PXE Boot Fails**

When PXE boot fails, verify the following:

* The PXE mapping file is correctly configured
* Target nodes are configured for network boot
* Network connectivity exists between OIM and target nodes
* DHCP and TFTP services are operational

**Node Diff Logic**

The restart API uses node diff logic to only PXE-boot newly added nodes. To force PXE boot on all nodes, create a new deployment.

Related Topics
--------------

* :doc:`how-to-buildstream-build-pipeline`
* :doc:`how-to-buildstream-validate-pipeline`
* :doc:`set_pxe_boot_order_buildstream`
* :doc:`managing-buildstream-catalogs-and-pipelines`
* :doc:`buildstream-architecture`