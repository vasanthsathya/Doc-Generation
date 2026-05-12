.. _how-to-buildstream-update-catalog-pipeline:

Updating BuildStreaM Catalogs and Managing Pipelines
====================================================

Update the ``catalog_rhel.json`` file to trigger BuildStreaM pipelines and monitor execution through GitLab. This procedure covers catalog modifications, pipeline type selection, and GitLab CI/CD integration.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before updating catalogs and managing pipelines:

* Deploy and configure BuildStreaM container on OIM node (see :doc:`prepare_oim_buildstream`)
* Complete GitLab deployment for BuildStreaM (see :doc:`how-to-gitlab-deployment`)
* Verify access to the GitLab project repository

BuildStreaM Catalog Structure
----------------------------------------

BuildStreaM uses an enhanced catalog structure with support for pipeline type selection:

**Pipeline Type Selection**

   The catalog metadata includes a ``pipeline_type`` parameter that determines which child pipeline is triggered:

   - ``build`` - Triggers the BUILD pipeline (see :doc:`how-to-buildstream-build-pipeline`)
   - ``deploy`` - Triggers the DEPLOY pipeline (see :doc:`how-to-buildstream-deploy-pipeline`)
   - ``cleanup`` - Triggers the CLEANUP pipeline (removes stale artifacts)

**OAuth Authentication Configuration**

   If OAuth 2.0 is enabled in the BuildStreaM configuration, include the following parameters in the catalog metadata:

   - ``oauth_enabled`` - Set to ``true`` to enable OAuth authentication
   - ``oauth_client_id`` - OAuth client identifier (configured in ``omnia_auth.service``)
   - ``oauth_token_url`` - OAuth token endpoint URL (typically ``https://<oim_host>:<auth_port>/oauth/token``)
   - ``oauth_scope`` - OAuth token scope (e.g., ``buildstream:read buildstream:write``)

   For OAuth configuration details, see :doc:`buildstream-architecture`.

**Catalog Example**

   .. code-block:: json

      {
        "metadata": {
          "pipeline_type": "build",
          "oauth_enabled": true,
          "oauth_client_id": "buildstream-client",
          "oauth_token_url": "https://oim.example.com:8443/oauth/token",
          "oauth_scope": "buildstream:read buildstream:write"
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

Procedure
---------

#. **Navigate to the GitLab project URL**

   Navigate to:

   .. code-block:: text

      https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

#. **Locate the catalog file**

   Go to **Code** → **Repository** and locate the catalog file ``catalog_rhel.json``.

#. **Modify the catalog file**

   Modify the ``catalog_rhel.json`` file to define your build requirements.

   .. note:: Ensure that the catalog file is updated with valid functional group names, architecture types, operating system types and versions, and package types. The pipeline fails if invalid details are provided.

   The following are the supported values:
      - **Functional group names**: For supported functional group names, see :ref:`functional-groups-section`.
      - **Architecture type**: ``x86_64`` and ``aarch64``.
      - **OS type**: ``RHEL``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **OS version**: ``10.0``, see :ref:`supported OS types and versions <redhat-support-matrix>`.
      - **Package types**: ``rpm``, ``rpm_repo``, ``image``, ``iso``, ``tarball``, ``pip_module``, ``git``, ``manifest``.

#. **Set the pipeline type**

   Configure the ``pipeline_type`` parameter in the catalog metadata to trigger the appropriate pipeline:

   - Set to ``build`` to trigger the build pipeline
   - Set to ``deploy`` to trigger the deploy pipeline
   - Set to ``cleanup`` to trigger the cleanup pipeline

#. **Commit and push catalog changes**

   To trigger the pipeline, commit and push catalog changes.

   .. note::
      BuildStreaM uses a three-pipeline architecture (parent router + dynamic child pipelines). The parent pipeline (``.gitlab-ci.yml``) analyzes the catalog and triggers the appropriate child pipeline (BUILD, DEPLOY, or CLEANUP) based on the ``pipeline_type`` parameter.
      Each child pipeline processes the catalog entries independently and executes the corresponding workflow stages.
      BuildStreaM pipeline behaviour is controlled by the GitLab CI/CD configuration in your environment.

Monitoring Pipeline Execution
-----------------------------

#. **Track pipeline progress through GitLab**

   The following image shows the BuildStreaM pipeline currently running and the stages being executed:

   .. image:: ../images/buildstream_pipeline_running.png

   Perform the following steps to track the pipeline progress through the GitLab web interface:

   a. Navigate to **Build** → **Pipeline**.
   b. Click on the running pipeline to view details.
   c. Monitor the parent pipeline status and the triggered child pipeline:

      **Parent Pipeline Stages**:
         - **parse-catalog**: Parses catalog file and determines pipeline type
         - **trigger-child-pipeline**: Triggers the appropriate child pipeline based on ``pipeline_type``

      **Child Pipeline Stages**:
         - **BUILD Pipeline**: Prepare → Build → Verify
         - **DEPLOY Pipeline**: Prepare → Deploy → Verify
         - **CLEANUP Pipeline**: Cleanup

#. **Review stage status**

   The following image shows each stage of the BuildStreaM pipeline and its status:

   .. image:: ../images/buildstream_pipeline_stages.png

   Expected pipeline status indicators:
      - |success| **Green checkmark**: Stage completed successfully
      - |failed| **Red X**: Stage failed (click for error details)
      - |running| **Blue circle**: Stage currently running

.. |success| image:: ../images/Icons/green_check.png
.. |failed| image:: ../images/Icons/red_x.png
.. |running| image:: ../images/Icons/blue_circle.png

#. **Check overall pipeline status**

   The following image shows overall pipeline status:

   .. image:: ../images/buildstream_pipeline_passed.png

Verification
------------

After the pipeline is completed, you can check the overall pipeline status and job execution.

1. Navigate to **Build** → **Pipelines**
2. Review the job list and status.
3. Click on individual jobs to view:
      - Execution logs
      - Resource usage
      - Error messages (if any)

Next Steps
-----------

After successful execution of the pipeline:

* For build pipelines, proceed to deployment (see :doc:`how-to-buildstream-deploy-pipeline`)
* For deploy pipelines, proceed to validation (see :doc:`how-to-buildstream-validate-pipeline`)
* Manually PXE boot the nodes to deploy the images if needed
* Use the PXE boot utility to deploy the images. See :doc:`set_pxe_boot_order_buildstream` for detailed instructions.

.. note::
   BuildStreaM uses a three-pipeline architecture with parent router and dynamic child pipelines. For detailed information on pipeline architecture and GitLab configuration, see :doc:`buildstream-pipelines`. For OAuth configuration details, see :doc:`buildstream-architecture`.

Related Topics
--------------

* :doc:`how-to-buildstream-build-pipeline`
* :doc:`how-to-buildstream-deploy-pipeline`
* :doc:`how-to-buildstream-validate-pipeline`
* :doc:`buildstream-architecture`
* :doc:`buildstream-pipelines`
