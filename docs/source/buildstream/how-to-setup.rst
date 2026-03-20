.. _how-to-buildstream-setup:

Getting Started with BuildStreaM
=================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Enable BuildStreaM in your Omnia environment to automate image lifecycle management through catalog-driven workflows. This guide covers the initial setup from configuration through first pipeline execution.

Prerequisites
-------------

Before enabling BuildStreaM:

* Omnia 2.1 core container must be up and running
* Sufficient system resources for BuildStreaM (minimum 4 GB RAM, 2 CPU cores, 20 GB free disk space)
* Network connectivity for BuildStreaM services
* Administrator access to the Omnia Infrastructure Manager (OIM)

.. important::
   BuildStreaM requires a dedicated PostgreSQL container for metadata storage. Ensure your environment has sufficient resources for additional containers.

Procedure
---------

#. Enable BuildStreaM in the Omnia configuration file.

   .. code-block:: bash

      cd /opt/omnia/config
      sudo vi omnia.yml

   Add the BuildStreaM configuration section:

   .. code-block:: yaml

      buildstream:
        enabled: true
        postgres_host: localhost
        postgres_port: 5432
        postgres_database: buildstream
        postgres_user: buildstream
        api_port: 8080

   Save the configuration file and exit the editor.

#. Run the prepare-oem playbook to create BuildStreaM containers.

   .. code-block:: bash

      cd /omnia
      ansible-playbook prepare_oem.yml

   This playbook performs the following tasks:
   * Creates the BuildStreaM container
   * Creates the PostgreSQL container for metadata storage
   * Creates the Playbook Watcher service
   * Configures network connectivity between services

   .. note::
      The container creation may take 5-10 minutes to complete.

#. Configure GitLab integration settings.

   Navigate to ``/opt/omnia/input/project_default/gitlab_config.yml`` and update the configuration:

   .. code-block:: yaml

      gitlab_host: <gitlab_server_ip>
      project_name: <project_name>
      visibility: private
      main_branch: main

   Replace the placeholder values with your specific GitLab configuration:
   * ``gitlab_host``: IP address of the GitLab server
   * ``project_name``: Name for your BuildStreaM project
   * ``visibility``: ``private`` or ``public`` (default: private)
   * ``main_branch``: Git branch name (default: main)

#. Run the GitLab installation playbook.

   .. code-block:: bash

      cd /omnia/gitlab
      ansible-playbook gitlab.yml

   This playbook installs GitLab and creates the BuildStreaM project structure.

Verification
------------

Verify BuildStreaM is running correctly:

#. Check the BuildStreaM container status.

   .. code-block:: bash

      docker ps | grep buildstream

   Expected output should show the BuildStreaM container running:

   .. code-block:: text

      abc123def456   buildstream:latest   "python -m buildstream"   2 hours ago   Up 2 hours   buildstream-core

#. Check the PostgreSQL container status.

   .. code-block:: bash

      docker ps | grep postgres

   Expected output should show the PostgreSQL container running:

   .. code-block:: text

      xyz789abc012   postgres:13   "docker-entrypoint.s…"   2 hours ago   Up 2 hours   buildstream-postgres

#. Verify API accessibility.

   .. code-block:: bash

      curl -k https://localhost:8080/api/v1/health

   Expected output should show API health status:

   .. code-block:: text

      {"status": "healthy", "version": "1.0.0"}

Result
------

BuildStreaM is now enabled and running in your Omnia environment. The GitLab project has been created with a default catalog file, and the API endpoints are accessible for automation.

Next Steps
----------

* Configure the BuildStreaM catalog for your specific requirements
* Deploy GitLab for BuildStreaM integration
* Update the catalog to trigger your first build pipeline

**Related topics:**
* :doc:`concept-overview`
* :doc:`how-to-gitlab-deployment`
* :doc:`how-to-catalog-configuration`
