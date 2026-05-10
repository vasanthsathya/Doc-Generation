

Update Catalog & Pipelines
==========================


Update the BuildStreaM catalog file to modify your cluster configuration and
trigger CI/CD pipeline runs to apply changes.


Overview
--------


The BuildStreaM catalog is a declarative YAML file that defines your entire
cluster configuration:

- Node assignments and roles.
- Software stacks and versions.
- Network configuration.
- Storage and authentication settings.

When you update the catalog and push changes to GitLab, a CI/CD pipeline
automatically validates the changes and (optionally) applies them to the
cluster.



Prerequisites
-------------


- GitLab is deployed and configured (see `Deploy Gitlab <deploy_gitlab.md>`_).
- The BuildStreaM catalog repository is initialized.
- A GitLab Runner is registered and active.
- You have Git access to the catalog repository.



Procedure
---------


#. **Clone the catalog repository** (if not already cloned):


.. code-block:: bash title="Run on: omnia_core container"

      cd /opt/omnia
      git clone http://<oim-ip>:8082/root/buildstream-catalog.git
      cd buildstream-catalog



#. **Edit the catalog file**:


.. code-block:: bash title="Run on: omnia_core container"

      vi catalog.yml



   Example catalog structure:


.. code-block:: yaml title="File: /opt/omnia/buildstream-catalog/catalog.yml"

      ---
      catalog_version: "2.1.0"
      cluster_name: "omnia-prod"
   
      # Operating system
      os:
        type: "rhel"
        version: "8.8"
        iso_path: "/opt/omnia/iso/RHEL-8.8-x86_64-dvd.iso"
   
      # Networks
      networks:
        admin:
          nic: "eno1"
          subnet: "10.5.0.0/24"
          gateway: "10.5.0.1"
          range: "10.5.0.100-10.5.0.200"
        bmc:
          nic: "eno2"
          subnet: "10.3.0.0/24"
          range: "10.3.0.100-10.3.0.200"
   
      # Node groups
      node_groups:
        slurm_control:
          role: "slurm_control_node"
          nodes:
            - service_tag: "ABCDEF1"
              admin_ip: "10.5.0.101"
              bmc_ip: "10.3.0.101"
        slurm_compute:
          role: "slurm_node"
          nodes:
            - service_tag: "ABCDEF2"
              admin_ip: "10.5.0.102"
              bmc_ip: "10.3.0.102"
            - service_tag: "ABCDEF3"
              admin_ip: "10.5.0.103"
              bmc_ip: "10.3.0.103"
   
      # Software stacks
      software:
        - slurm
        - cuda
        - apptainer
        - openldap
   
      # Telemetry
      telemetry:
        enabled: true
        idrac: true
        ldms: true



#. **Make your changes**. Common modifications include:

  - Adding new nodes to a ``node_groups`` section.
  - Changing the software stack.
  - Updating network ranges.
  - Enabling/disabling telemetry.

#. **Commit and push the changes**:


.. code-block:: bash title="Run on: omnia_core container"

      cd /opt/omnia/buildstream-catalog
      git add catalog.yml
      git commit -m "Add 2 new compute nodes to slurm cluster"
      git push origin main



#. **Monitor the pipeline** in GitLab:

   Open the GitLab web UI and navigate to:
   **CI/CD** > **Pipelines**

   The pipeline runs through the following stages:

  - **validate** -- Checks catalog syntax and validates input files.
  - **provision** -- Discovers and provisions new/changed nodes (manual
     trigger).
  - **configure** -- Applies Slurm/K8s/telemetry configuration (manual
     trigger).
  - **verify** -- Runs health checks on the updated cluster.

#. **Manually trigger deployment stages**:

   In the GitLab pipeline view, click the **Play** button next to the
   ``provision`` and ``configure`` stages to execute them.

#. **Review pipeline artifacts and logs**:

   Click on a completed job to view its logs. Download artifacts from the
   **Artifacts** section if available.



Verification
------------


#. **Verify the pipeline completed successfully**:

   In GitLab, navigate to **CI/CD** > **Pipelines**. The latest pipeline
   should show all stages with green checkmarks.

#. **Verify catalog changes were applied**:


.. code-block:: bash title="Run on: omnia_core container"

      # Check if new nodes were provisioned
      ochami node list
   
      # Check Slurm configuration
      ssh <slurm-control-ip> sinfo



#. **Run the verification stage** to confirm cluster health:


.. code-block:: bash title="Run on: omnia_core container"

      ansible all -m ping





Next Steps
----------


- `Buildstream Troubleshooting <buildstream_troubleshooting.md>`_ -- Debug pipeline failures.
- `Deploy Gitlab <deploy_gitlab.md>`_ -- Update GitLab or runner configuration.



Troubleshooting
---------------


**Pipeline fails at "validate" stage**
   Check the job logs for validation errors. Common issues:

  - YAML syntax errors in ``catalog.yml``
  - Missing required fields
  - IP address conflicts

   Fix the catalog and push a new commit.

**Pipeline fails at "provision" stage**
  - Check that BMC IPs are reachable for new nodes.
  - Verify credentials are configured.
  - Review the Ansible playbook output in the job logs.

**Pipeline fails at "configure" stage**
  - Check that provisioned nodes are reachable.
  - Verify the Vault password is available to the runner.
  - Review Ansible output for specific task failures.

**Git push is rejected**
   Check GitLab authentication:


.. code-block:: bash title="Run on: omnia_core container"

      git remote -v
      # Ensure URL is correct and credentials are configured



**Pipeline not triggered on push**
   Verify ``.gitlab-ci.yml`` exists in the repository root and the runner
   is active:


.. code-block:: bash title="Run on: OIM host"

      podman exec gitlab-runner gitlab-runner list

