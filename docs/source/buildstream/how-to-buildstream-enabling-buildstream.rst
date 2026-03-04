.. _how-to-buildstream-enabling-buildstream:

Enabling BuildStreaM in Omnia
=============================

Enable BuildStreaM in your existing Omnia deployment to activate catalog-driven, automated CI/CD workflows. This procedure sets up the BuildStreaM infrastructure and integrates it with your GitLab instance.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before enabling BuildStreaM, ensure you have:

* A working Omnia control plane deployment
* GitLab server with administrator access
* Network connectivity between Omnia control plane and GitLab server
* Sufficient disk space for BuildStreaM containers and Postgres database
* Administrator privileges on the Omnia control plane
* Understanding of CI/CD pipeline concepts

.. important:: BuildStreaM requires a dedicated GitLab instance and cannot share existing GitLab installations used for other purposes.

Configuration
-------------

Configure BuildStreaM parameters in your Omnia configuration file.

#. Navigate to the Omnia configuration directory.

   .. code-block:: bash

      cd /opt/omnia/config

#. Open the Omnia configuration file for editing.

   .. code-block:: bash

      sudo vi omnia.yml

#. Add the BuildStreaM configuration section.

   .. code-block:: yaml

      # BuildStreaM Configuration
      buildstream:
        enabled: true
        gitlab:
          host: "192.168.1.100"  # GitLab server IP address
          project_name: "omnia-buildstream"
          visibility: "private"   # or "public"
          main_branch: "main"
        api:
          base_uri: "https://localhost:8080/api/v1"
          port: 8080
        admission_control:
          max_concurrent_builds: 1
          max_parallel_validations: 1

.. note:: Replace the GitLab host IP address with your actual GitLab server address.

#. Save the configuration file and exit the editor.

Container Setup
--------------

BuildStreaM requires several containers to be deployed on the control plane.

#. Run the prepare OEM playbook to set up BuildStreaM infrastructure.

   .. code-block:: bash

      cd /opt/omnia
      ansible-playbook playbooks/prepare-oem.yml -i inventory

   The playbook will create the following containers:
   
   * BuildStreaM container - Main application container
   * Postgres container - Database for API transaction storage
   * Playbook watcher service - Monitors and executes playbook operations

#. Verify the containers are running.

   .. code-block:: bash

      podman ps

   You should see output similar to:

   .. code-block:: text

      CONTAINER ID  IMAGE                           COMMAND               CREATED         STATUS             PORTS                     NAMES
      a1b2c3d4e5f6  omnia-buildstream:latest        ./buildstream         2 minutes ago   Up 2 minutes       0.0.0.0:8080->8080/tcp    buildstream
      f6e5d4c3b2a1  postgres:13                     postgres -D /var/l...  2 minutes ago   Up 2 minutes       0.0.0.0:5432->5432/tcp    buildstream-db
      b2a1c3d4e5f6  omnia-playbook-watcher:latest   ./watcher             2 minutes ago   Up 2 minutes                                 playbook-watcher

GitLab Integration Setup
------------------------

Configure GitLab integration to enable pipeline automation.

#. Create the GitLab integration configuration file.

   .. code-block:: bash

      sudo vi /opt/omnia/config/gitlab.yaml

#. Add the GitLab configuration.

   .. code-block:: yaml

      gitlab_integration:
        server_url: "http://192.168.1.100"
        access_token: "[TO BE PROVIDED: GitLab access token]"
        project_config:
          name: "omnia-buildstream"
          description: "BuildStreaM automation pipelines"
          visibility: "private"
          default_branch: "main"
        pipeline_config:
          enabled: true
          auto_trigger: true
          stages:
            - local_repo
            - build_image
            - discovery
            - authentication
            - registration

.. AI_REVIEW: GitLab access token generation process - verify against GitLab documentation

#. Run the GitLab integration playbook.

   .. code-block:: bash

      cd /opt/omnia
      ansible-playbook playbooks/gitlab.yaml -i inventory

   This playbook will:
   
   * Create the GitLab project
   * Set up the pipeline configuration
   * Upload the initial catalog file
   * Configure the GitLab runner

Initial Catalog Setup
---------------------

Set up the initial catalog that defines your build configurations.

#. Navigate to the BuildStreaM configuration directory.

   .. code-block:: bash

      cd /opt/omnia/buildstream/config

#. Create a basic catalog file.

   .. code-block:: bash

      sudo vi catalog.yml

#. Add basic catalog structure.

   .. code-block:: yaml

      catalog:
        version: "1.0"
        metadata:
          name: "omnia-base-catalog"
          description: "Base catalog for Omnia BuildStreaM"
        
        roles:
          - name: "compute-node"
            description: "Standard compute node configuration"
            packages:
              - name: "rocky-linux"
                version: "8.8"
                arch: "x86_64"
              - name: "omnia-drivers"
                version: "2.1.0"
                arch: "x86_64"
              - name: "kubernetes"
                version: "1.28"
                arch: "x86_64"
        
        validation:
          - name: "basic-connectivity"
            type: "network"
          - name: "service-health"
            type: "container"

.. note:: This is a minimal catalog example. Your actual catalog will be more comprehensive with additional roles, packages, and validation rules.

#. Upload the catalog to GitLab.

   .. code-block:: bash

      cd /opt/omnia/buildstream
      python scripts/upload_catalog.py --config ../config/catalog.yml

   The script will upload the catalog to your GitLab project and trigger the initial pipeline.

Verification
------------

Verify that BuildStreaM is properly configured and running.

#. Check the BuildStreaM API status.

   .. code-block:: bash

      curl -k https://localhost:8080/api/v1/health

   Expected output:

   .. code-block:: text

      {"status": "healthy", "version": "1.0.0", "services": ["api", "orchestrator", "catalog"]}

#. Verify GitLab project creation.

   .. code-block:: bash

      curl -H "Private-Token: [YOUR_GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/projects?search=omnia-buildstream"

   Expected output should show your project details.

#. Check pipeline status in GitLab.

   Navigate to your GitLab instance and verify that:
   
   * The project exists with the correct name
   * The initial catalog file is present
   * A pipeline is running or has completed
   * The GitLab runner is online and active

#. Test BuildStreaM job creation.

   .. code-block:: bash

      curl -k -X POST https://localhost:8080/api/v1/jobs \
           -H "Content-Type: application/json" \
           -H "Authorization: Bearer [YOUR_ACCESS_TOKEN]" \
           -d '{"catalog": "omnia-base-catalog", "target": "test"}'

   Expected output:

   .. code-block:: text

      {"jobId": "job-12345", "status": "created", "catalog": "omnia-base-catalog"}

Troubleshooting
---------------

If you encounter issues during setup:

**BuildStreaM containers not starting**

   Check the container logs:

   .. code-block:: bash

      podman logs buildstream
      podman logs buildstream-db

   Common issues:
   * Insufficient disk space
   * Port conflicts (8080, 5432)
   * Configuration file syntax errors

**GitLab integration failures**

   Verify GitLab connectivity:

   .. code-block:: bash

      ping 192.168.1.100
      curl -I http://192.168.1.100

   Check GitLab token permissions:
   * Token must have `api` scope
   * Token must have project creation permissions

**Pipeline not triggering**

   Check the GitLab runner status:

   .. code-block:: bash

      curl -H "Private-Token: [YOUR_GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/projects/[PROJECT_ID]/runners"

   Ensure the runner is online and has the correct tags.

Next Steps
-----------

After successfully enabling BuildStreaM:

1. Configure your detailed catalog definitions for your specific requirements
2. Set up additional validation rules and test suites
3. Configure admission control parameters for your environment
4. Set up monitoring and alerting for BuildStreaM operations
5. Train your team on the new BuildStreaM workflow

For detailed information on managing catalogs and pipelines, see:
* :doc:`concepts-buildstream-catalog`
* :doc:`how-to-buildstream-managing-gitlab-integration`
* :doc:`how-to-buildstream-working-with-pipelines`

Related Topics
--------------

* :doc:`concepts-buildstream-architecture`
* :doc:`reference-buildstream-configuration`
* :doc:`troubleshooting-buildstream-pipeline-failures`
