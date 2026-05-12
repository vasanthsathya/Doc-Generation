.. _how-to-buildstream-deploy-pipeline:

Deploying Omnia Images with BuildStreaM
========================================

Deploy built Omnia OS images to target nodes using the BuildStreaM deploy pipeline. This procedure covers deploying images, PXE booting nodes, and monitoring the deployment process.

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
* Set up OAuth 2.0 client credentials (if OAuth authentication is enabled)

Deploy Pipeline Overview
------------------------

The BuildStreaM deploy pipeline manages image deployment through sequential stages:

**Deploy Stages**

BuildStreaM executes the following deploy stages:

| Stage | API Endpoint | Description |
|-------|-------------|-------------|
| ``deploy`` | ``POST /api/v1/jobs/{job_id}/deploy`` | Deploys built images to target nodes via Ansible playbook |
| ``pxe_boot`` | ``POST /api/v1/jobs/{job_id}/restart`` | PXE boots target nodes after image deployment |

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

#. **Deploy Images to Target Nodes**

   Deploy the built images to the target nodes.

   .. code-block:: bash

      curl -X POST https://<oim_host>:5001/api/v1/jobs/{job_id}/deploy \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>" \
        -H "Content-Type: application/json" \
        -d '{
          "image_group_id": "<image_group_id>"
        }'

   BuildStreaM validates that the image group exists, belongs to the specified job, and is in ``BUILT`` state.

   .. code-block:: json

      {
        "job_id": "uuid",
        "image_group_id": "<image_group_id>",
        "status": "DEPLOYING",
        "submitted_at": "2026-04-08T11:00:00Z"
      }

   The image group transitions: ``BUILT → DEPLOYING → DEPLOYED``.

#. **Monitor Deploy Status**

   Query the job status to monitor deployment progress.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/jobs/{job_id} \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

   The response shows the current state of the deploy stage.

#. **PXE Boot Target Nodes**

   After deployment completes, PXE boot the target nodes to provision the images.

   .. code-block:: bash

      curl -X POST https://<oim_host>:5001/api/v1/jobs/{job_id}/restart \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>" \
        -H "Content-Type: application/json" \
        -d '{
          "disable_pxe_boot": false
        }'

   | Field | Type | Required | Default | Description |
   |-------|------|----------|---------|-------------|
   | ``disable_pxe_boot`` | boolean | No | ``false`` | If ``true``, skip PXE boot for this restart request |

   The system consumes the PXE mapping file to determine target nodes and uses node diff logic to only PXE-boot newly added nodes.

   The image group transitions: ``DEPLOYED → RESTARTING → RESTARTED``.

#. **Monitor PXE Boot Status**

   Query the job status to monitor PXE boot progress.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/jobs/{job_id} \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

   The response includes per-node status showing which nodes were restarted and which were skipped.

**Alternative: GitLab CI/CD Pipeline**

To trigger the deploy pipeline using GitLab CI/CD:

#. Navigate to the GitLab project URL: ``https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>``
#. Go to **Code** → **Repository**
#. Locate the catalog file ``catalog_rhel.json``
#. Set ``pipeline_type`` to ``deploy`` in the catalog metadata
#. Commit and push the catalog changes to trigger the DEPLOY pipeline

Verification
------------

After the deploy pipeline completes, verify the deployment:

#. **Check Image Group Status**

   Confirm that the image group is in ``RESTARTED`` state.

   .. code-block:: bash

      curl -X GET https://<oim_host>:5001/api/v1/images \
        -H "Authorization: Bearer <jwt_token>" \
        -H "X-Client-Id: <client_id>"

#. **Verify Node Connectivity**

   Check that target nodes are reachable and responding.

   .. code-block:: bash

      ping <node_ip_address>

#. **Check Node Status**

   Verify that nodes have booted with the deployed image.

   .. code-block:: bash

      ssh <node_ip_address> "cat /etc/os-release"

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
* :doc:`how-to-update-catalog-pipeline`
* :doc:`buildstream-architecture`
* :doc:`buildstream-pipelines`