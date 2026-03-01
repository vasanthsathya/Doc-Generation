.. _how-to-buildstream-prepare:

Prepare BuildStreaM Configuration and Pipeline
==============================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Set up and configure BuildStreaM for automated build and validation workflows. This comprehensive procedure covers prerequisites, enabling BuildStreaM services, configuring credentials, and ensuring proper PXE mapping setup.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before beginning the BuildStreaM setup:

* Omnia 2.1.0.0 or later with core container 1.1 running
* Administrator access on the Omnia Infrastructure Manager (OIM) node
* PostgreSQL 12 or later for BuildStreaM database
* Network connectivity for external integrations
* Minimum 4 GB RAM and 2 CPU cores for BuildStreaM services
* 10 GB free disk space for BuildStreaM data and logs
* SSH access to omnia_core node for configuration

.. important::
   BuildStreaM requires a separate PostgreSQL database for storing transaction details and job metadata.

Procedure
---------

#. Verify system prerequisites.

Check that your system meets the minimum requirements:

.. code-block:: bash

   # Check system resources
   free -h
   df -h
   podman --version

#. Access the omnia_core node.

Use SSH to connect to the omnia_core node where configuration files are located:

.. code-block:: bash

   ssh omnia_core

#. Configure GitLab project settings.

Edit the GitLab configuration file to define project settings:

.. code-block:: bash

   cat /opt/omnia/input/project_default/gitlab_config.yml

The configuration should include:

.. code-block:: yaml

   # Project settings
   # Name of the GitLab project Omnia will create/manage
   gitlab_project_name: "omnia-catalog"
   # Visibility options: private | internal | public
   gitlab_project_visibility: "private"
   # Default branch used for repository and API operations
   gitlab_default_branch: "main"

.. note::
   Adjust the project name and visibility settings according to your requirements.

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

#. Run the prepare OIM playbook.

Execute the prepare_oim.yaml playbook to create BuildStreaM containers:

.. code-block:: bash

   cd /path/to/omnia
   ansible-playbook playbooks/prepare_oim.yml

This creates:
- BuildStreaM API container
- PostgreSQL database container
- BuildStreaM playbook watcher service

#. Configure BuildStreaM credentials.

Provide the required credentials for BuildStreaM authentication and access:

.. code-block:: yaml

   # Example credential configuration
   buildstream:
     oauth:
       client_id: buildstream-client
       client_secret: your-client-secret
       token_url: https://oauth-provider.com/oauth/token
       scope: "buildstream:read buildstream:write"

.. warning::
   Protect your OAuth client credentials. Store them in a secure location and use environment variables in production.

#. Update PXE mapping file.

Ensure the PXE mapping file is properly configured with node information:

.. code-block:: bash

   # Check current mapping file
   cat /opt/omnia/input/provision_config/mapping_file.yml

Verify the mapping includes all nodes that will participate in BuildStreaM builds:

.. code-block:: yaml

   nodes:
     - hostname: "compute-01"
       ip_address: "192.168.1.101"
       mac_address: "00:11:22:33:44:55"
       role: "compute"
     - hostname: "management-01"
       ip_address: "192.168.1.100"
       mac_address: "00:11:22:33:44:56"
       role: "management"

.. important::
   Reference Step 2: Create Mapping File with Node information for detailed mapping procedures.

#. Verify BuildStreaM services.

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

Result
------

BuildStreaM is now configured and ready for GitLab deployment. The system can process catalog files and execute build workflows through the automated pipeline system.

Verification
------------

Verify the setup completed successfully:

#. Check BuildStreaM service status:

.. code-block:: bash

   podman logs buildstream-api --tail 20

#. Validate database connectivity:

.. code-block:: bash

   podman exec buildstream-db psql -U buildstream -d buildstream -c "SELECT 1;"

#. Test configuration file access:

.. code-block:: bash

   ls -la /opt/omnia/input/project_default/gitlab_config.yml

#. Verify PXE mapping file integrity:

.. code-block:: bash

   python3 -c "import yaml; yaml.safe_load(open('/opt/omnia/input/provision_config/mapping_file.yml'))"

Expected output shows no errors for all verification steps.

Next Steps
----------

After completing the BuildStreaM configuration:

* **Deploy GitLab** - Install and configure GitLab for pipeline execution
* **Create initial catalog** - Define your first build catalog
* **Test pipeline execution** - Verify end-to-end workflow
* **Monitor build operations** - Set up monitoring and alerting

.. tip::
   Keep your BuildStreaM configuration files under version control. This makes it easier to track changes and roll back configurations if needed.

For detailed GitLab deployment procedures, see :doc:`how-to-gitlab-deployment`.

Related Topics
--------------

* :doc:`concept-overview`
* :doc:`how-to-gitlab-deployment`
* :doc:`how-to-update-catalog-pipeline`
