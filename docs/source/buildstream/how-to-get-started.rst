.. _how-to-buildstream-get-started:

Getting Started with BuildStreaM
=================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Set up and configure BuildStreaM for automated build and validation workflows in your HPC environment. This procedure guides you through the initial setup, authentication configuration, and first build workflow.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before beginning the BuildStreaM setup:

* Omnia 2.1.0.0 or later with core container 1.1 running
* Administrator access on the Omnia Infrastructure Manager (OIM) node
* OAuth 2.0 provider for authentication
* Access to artifact repository for build storage
* Network connectivity for external integrations
* Minimum 4 GB RAM and 2 CPU cores for BuildStreaM services
* 10 GB free disk space for BuildStreaM data and logs

.. important::
   BuildStreaM requires a separate PostgreSQL database for storing transaction details and job metadata. Ensure you have PostgreSQL 12 or later available.

Procedure
---------

#. Enable BuildStreaM in Omnia configuration.

Edit the Omnia configuration file to enable BuildStreaM services:

.. code-block:: yaml

   buildstream:
     enabled: true
     postgres_host: localhost
     postgres_port: 5432
     postgres_db: buildstream
     postgres_user: buildstream
     api_port: 8080

.. note::
   Replace the PostgreSQL connection details with your actual database configuration.

#. Run the prepare OEM playbook to create BuildStreaM containers.

.. code-block:: bash

   cd /path/to/omnia
   ansible-playbook playbooks/prepare_oem.yml

This creates:
- BuildStreaM API container
- PostgreSQL database container
- BuildStreaM playbook watcher service

#. Configure OAuth 2.0 authentication.

Create an OAuth 2.0 client application in your identity provider:

.. code-block:: bash

   # Example OAuth 2.0 configuration
   oauth:
     client_id: buildstream-client
     client_secret: your-client-secret
     token_url: https://oauth-provider.com/oauth/token
     scope: "buildstream:read buildstream:write"

.. warning::
   Protect your OAuth client credentials. Store them in a secure location and use environment variables in production.

#. Verify BuildStreaM service status.

Check that all BuildStreaM services are running:

.. code-block:: bash

   podman ps | grep buildstream

Expected output shows running containers:

.. code-block:: text

   buildstream-api      Up   2 minutes ago
   buildstream-db       Up   2 minutes ago
   buildstream-runner   Up   2 minutes ago

#. Test API connectivity.

Verify that the BuildStreaM API is accessible:

.. code-block:: bash

   curl -X GET "http://localhost:8080/api/v1/health" \
        -H "Authorization: Bearer <your-oauth-token>"

Expected response:

.. code-block:: json

   {
     "status": "healthy",
     "version": "1.0.0",
     "services": {
       "api": "running",
       "database": "connected",
       "orchestrator": "ready"
     }
   }

#. Create your first catalog.

Create a basic catalog file to define your build requirements:

.. code-block:: yaml

   # catalog.yaml
   catalog_version: "1.0"
   description: "HPC Cluster Build Catalog"
   
   roles:
     - name: "compute-node"
       description: "Standard compute node configuration"
       packages:
         - name: "rocky-linux"
           version: "8.8"
         - name: "slurm"
           version: "23.02"
         - name: "openmpi"
           version: "4.1.5"
   
   validation_dependencies:
     - name: "basic-validation"
       required_for: ["compute-node"]

#. Submit your first build job.

Use the BuildStreaM API to submit a build job:

.. code-block:: bash

   curl -X POST "http://localhost:8080/api/v1/jobs" \
        -H "Authorization: Bearer <your-oauth-token>" \
        -H "Content-Type: application/json" \
        -d '{
          "catalog_path": "/path/to/catalog.yaml",
          "build_options": {
            "parallel_validation": false,
            "generate_sbom": true
          }
        }'

Expected response:

.. code-block:: json

   {
     "job_id": "job-20240301-001",
     "status": "submitted",
     "stages": [
       "parse-catalog",
       "generate-input-files", 
       "prepare-repos",
       "build-image",
       "validate-image",
       "validate-image-on-test",
       "promote"
     ]
   }

Result
------

BuildStreaM is now configured and ready to automate your build and validation workflows. The system will process your catalog and execute the defined build stages in sequence.

Verification
------------

Verify the setup completed successfully:

#. Check job status using the job ID returned from submission:

.. code-block:: bash

   curl -X GET "http://localhost:8080/api/v1/jobs/job-20240301-001" \
        -H "Authorization: Bearer <your-oauth-token>"

#. Monitor build progress in the BuildStreaM logs:

.. code-block:: bash

   podman logs buildstream-api -f

#. Verify that build artifacts are created in the artifact repository.

.. code-block:: bash

   ls -la /opt/omnia/artifacts/buildstream/

Expected output shows build artifacts and validation reports:

.. code-block:: text

   job-20240301-001/
   ├── compute-node.img
   ├── compute-node.sbom
   ├── validation-report.json
   └── build-manifest.json

Next Steps
----------

After completing the initial setup:

* **Configure advanced catalogs**: Define multiple roles and complex validation dependencies
* **Set up GitLab integration**: Enable automated pipeline triggering based on catalog changes
* **Configure monitoring**: Set up alerts for build failures and performance issues
* **Review security settings**: Implement additional authentication and authorization as needed

.. tip::
   Keep your BuildStreaM configuration files under version control. This makes it easier to track changes and roll back configurations if needed.

For detailed troubleshooting guidance, see :doc:`../troubleshooting/buildstream-issues`.

Related Topics
--------------

* :doc:`concept-architecture`
* :doc:`how-to-configure-catalogs`
* :doc:`how-to-gitlab-integration`
* :doc:`../reference/api/buildstream`
