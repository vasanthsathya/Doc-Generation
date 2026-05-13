.. _deploying-gitlab-buildstream:

Step 4: Deploy GitLab for BuildStream
================================

Deploy GitLab as the CI/CD automation engine for BuildStream, providing a three-pipeline architecture for build, deploy, and cleanup operations. This procedure covers GitLab installation, project setup with pipeline configuration files, input folder structure, and runner verification.

BuildStream uses a **three-pipeline architecture** in GitLab:

* **Build Pipeline** (``.gitlab-ci-build.yml``): Triggered by catalog/config changes, creates images and establishes Job ID to Image Group ID mapping
* **Deploy Pipeline** (``.gitlab-ci-deploy.yml``): Triggered by PXE mapping changes, deploys images to cluster nodes
* **Cleanup Pipeline** (``.gitlab-ci-cleanup.yml``): Triggered manually, removes old Image Groups based on retention policy

The pipelines are coordinated by a **parent router** (``.gitlab-ci.yml``) that uses file change detection to dispatch to the appropriate child pipeline.

Prerequisites
-------------

Before deploying GitLab for BuildStreaM:

* Ensure that Omnia BuildStreaM container, PostgreSQL container, and Playbook Watcher service are deployed on the OIM node (see :doc:`preparing-oim-buildstream`)
* The node where GitLab will be deployed must have Internet connectivity.
* A dedicated node is required for BuildStreaM GitLab deployment.
* The node must have sufficient system resources for BuildStreaM (minimum 4 GB RAM, 2 CPU cores, 20 GB free disk space)
* GitLab requires a minimum of 2 CPU cores. More cores may be needed for production workloads.
* OIM node must be accessible from the GitLab node.
* Ensure that BuildStream API server (BuildStream container) is reachable from the GitLab node.
* Ensure that appStream and Base OS repositories are configured and accessible from the GitLab node.
* Ensure that on the GitLab node, SELinux is disabled.

.. important::
   Omnia uses a dedicated GitLab instance for BuildStreaM. This procedure provisions a new GitLab instance specifically configured for BuildStreaM. Currently, existing GitLab setups configured for other purposes are not supported.

Procedure
---------

1. Use SSH to connect to the ``omnia_core`` container.

   .. code-block:: bash

      ssh omnia_core

2. Navigate to ``/opt/omnia/input/project_default/gitlab_config.yml`` and update the ``gitlab_config.yml`` file. Use the :doc:`../../../reference/buildstream/configuration-tables` for reference.
    
   .. code-block:: bash

      cat /opt/omnia/input/project_default/gitlab_config.yml

3. Ensure that the BuildStream input configuration files are properly configured in ``/opt/omnia/input/project_default/``. The following files will be automatically copied to the GitLab project ``input/`` folder:

   * ``local_repo_config.yml`` - Local repository configuration
   * ``network_spec.yml`` - Network configuration  
   * ``provision_config.yml`` - Provision configuration
   * ``storage_config.yml`` - Storage configuration
   * ``telemetry_config.yml`` - Telemetry configuration

   For detailed parameter descriptions, see :doc:`../../../reference/buildstream/configuration-tables`.

4. Navigate to the GitLab directory.

   .. code-block:: bash

      cd /omnia/gitlab

5. Run the ``gitlab.yml`` playbook:

   .. code-block:: bash

      ansible-playbook gitlab.yml

6. When it prompts you to enter the GitLab password, enter the password. Note the password as it is required to access the GitLab project and instance.

This ``gitlab.yml`` playbook performs the following tasks:

- Installs the GitLab instance on the host specified in the ``gitlab_config.yml`` file.
- In the GitLab instance, creates a project with the specified name, visibility, and default branch as configured in the ``gitlab_config.yml`` file.
- Installs GitLab runner as a Podman container.
- Generates a self-signed CA certificate for GitLab on the GitLab node at ``/root/gitlab-certs/ca.crt``
- Adds the project with the following files:
  - **Pipeline Configuration Files**:
    - ``.gitlab-ci.yml`` - Parent router pipeline that dispatches to child pipelines
    - ``.gitlab-ci-build.yml`` - Build pipeline for creating images
    - ``.gitlab-ci-deploy.yml`` - Deploy pipeline for deploying images to nodes
    - ``.gitlab-ci-cleanup.yml`` - Cleanup pipeline for removing old Image Groups
    - ``.gitlab-ci-deploy-child-template.yml`` - Dynamic child pipeline template for deploy operations
  - **Catalog File**:
    - ``catalog_rhel.json`` - Default catalog file containing build definitions for RHEL images
  - **Input Folder**:
    - ``input/`` - Directory containing all BuildStream input configuration files
    The input folder includes the following configuration files (see :doc:`../../../reference/buildstream/configuration-tables` for detailed parameter descriptions):
      - ``local_repo_config.yml`` - Local repository configuration
      - ``network_spec.yml`` - Network configuration
      - ``provision_config.yml`` - Provision configuration
      - ``pxe_mapping_file.csv`` - PXE mapping file for node information
      - ``storage_config.yml`` - Storage configuration
      - ``telemetry_config.yml`` - Telemetry configuration

.. image:: ../../../../images/buildstream_project.png
   :alt: BuildStream project structure
   
.. note::
   The installation may take 10-15 minutes to complete.

7. To avoid **Not Secure** warnings when accessing the GitLab instance, download and import the certificate generated in step 4 to the browser.

Verification
------------
After the installation of GitLab complete, verify the following:

.. TODO:: Add screenshot: GitLab project URL access showing the project page

1. Verify you can access the GitLab project URL.

   .. code-block:: text

      https://<gitlab_host>:<gitlab_https_port>/root/<gitlab_project_name>

   .. TODO:: Add screenshot: GitLab project structure showing pipeline files, catalog, and input folder

   The project should contain:

   * **Pipeline Configuration Files**:
     
     - ``.gitlab-ci.yml`` — Parent router pipeline that dispatches to child pipelines
     - ``.gitlab-ci-build.yml`` — Build pipeline for creating images
     - ``.gitlab-ci-deploy.yml`` — Deploy pipeline for deploying images to nodes
     - ``.gitlab-ci-cleanup.yml`` — Cleanup pipeline for removing old Image Groups
     - ``.gitlab-ci-deploy-child-template.yml`` — Dynamic child pipeline template for deploy operations
   
   * **Catalog File**:
     
     - ``catalog_rhel.json`` — Default catalog file containing build definitions for RHEL images
   
   * **Input Folder**:
     
     - ``input/`` — Directory containing all BuildStream input configuration files
     - ``input/local_repo_config.yml`` — Local repository configuration
     - ``input/network_spec.yml`` — Network configuration
     - ``input/provision_config.yml`` — Provision configuration
     - ``input/pxe_mapping_file.csv`` — PXE mapping file for node information
     - ``input/storage_config.yml`` — Storage configuration
     - ``input/telemetry_config.yml`` — Telemetry configuration

2. Verify runner status through GitLab web interface:

   .. TODO:: Add screenshot: GitLab Settings → CI/CD → Runners section showing green status indicator

   1. Navigate to **Settings** → **CI/CD**.
   2. Expand **Runners** section.
   3. Verify the runner shows a **green** status indicator.
   4. Confirm runner is set to **Running Always** with **Podman Container**.

Input Folder Structure
----------------------

The ``input/`` folder in the GitLab project contains all the configuration files required for BuildStream operations. These files are automatically copied to the GitLab repository during the initial GitLab setup and are used by the BuildStream pipelines to configure the build and deploy processes.

**Input File Purposes**:

* **local_repo_config.yml**: Configures the local repository for storing build artifacts and packages
* **network_spec.yml**: Defines network configuration for cluster communication
* **provision_config.yml**: Contains provision configuration for cluster setup
* **pxe_mapping_file.csv**: Maps nodes to functional groups for deployment
* **storage_config.yml**: Configures storage backend (NFS or PowerScale)
* **telemetry_config.yml**: Sets up telemetry and monitoring configuration

**Input Folder Usage**:

The input folder files are used by BuildStream pipelines in the following ways:

* **Build Pipeline**: Reads configuration files to generate input files for image building
* **Deploy Pipeline**: Uses PXE mapping file to determine target nodes for deployment
* **Configuration Updates**: Modified input files can trigger corresponding pipeline stages
* **Parameter Reference**: For detailed parameter descriptions and allowed values, see :doc:`../../../reference/buildstream/configuration-tables`

.. note::
   The input folder structure ensures that all required configuration is centrally managed in the GitLab repository, enabling version control and collaboration on BuildStream configuration changes.

Next Steps
----------

After completing GitLab deployment, update the catalog file to automatically trigger the build pipeline. See :doc:`../build/executing-build-pipeline`.


