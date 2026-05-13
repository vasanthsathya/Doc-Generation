.. _concept-buildstream-overview:

Omnia BuildStreaM: Catalog-Driven Build Automation
==================================================

Omnia BuildStreaM provides a comprehensive automation solution for managing infrastructure build workflows. It uses a catalog-driven approach where you define your build requirements in a structured catalog file, and BuildStreaM executes automated pipelines to create and deploy images according to your specifications.

BuildStreaM supports three pipeline types that can be executed through GitLab:

* **Build Pipeline**: Creates diskless images based on catalog specifications (automatically triggered on catalog commit)
* **Deploy Pipeline**: Deploys built images to target cluster nodes (automatically triggered on PXE mapping file update)
* **Clean Pipeline**: Removes old Image Groups based on retention policy (manual trigger only)

BuildStreaM addresses the key challenges in HPC cluster image management:

   - **Automation**: Eliminates manual build and deployment processes
   - **Integration**: Works seamlessly with existing Omnia deployments
   - **Traceability**: Provides complete audit trails for all build operations

To build your own custom workflows, you can use the BuildStreaM REST API. The BuildStreaM API documentation is available at `Omnia BuildStreaM API Documentation <https://developer.dell.com/apis/ea677050-f49b-49e1-a4b9-1cdd563415d9/versions/2.1.0/docs/Introduction.md>`_.

.. toctree::
   :maxdepth: 1
   :caption: BuildStreaM Documentation

   how-to/buildstream/setup/deploying-omnia-core
   how-to/buildstream/setup/creating-pxe-mapping-file
   how-to/buildstream/setup/preparing-oim-buildstream
   how-to/buildstream/setup/deploying-gitlab-buildstream
   how-to/buildstream/build/executing-build-pipeline
   how-to/buildstream/deploy/executing-deploy-pipeline
   how-to/buildstream/management/configuring-pxe-boot
   how-to/buildstream/management/performing-cleanup-operations
   how-to/buildstream/management/retrying-pipelines
   how-to/buildstream/monitoring/initializing-telemetry
   how-to/buildstream/monitoring/verifying-telemetry-services
   reference/buildstream/configuration-tables
   reference/buildstream/catalog-schema
   reference/buildstream/upload-validation-rules
   troubleshooting/buildstream/common-pipeline-issues
   


