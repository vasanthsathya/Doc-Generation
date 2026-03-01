.. _how-to-buildstream-configure-catalogs:

Configuring BuildStreaM Catalogs
=================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Create and manage BuildStreaM catalogs that define roles, packages, and validation dependencies for automated build workflows. This procedure covers catalog structure, role definitions, and validation configurations.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before configuring BuildStreaM catalogs:

* BuildStreaM installed and running (see :doc:`how-to-get-started`)
* Understanding of your HPC cluster requirements
* Package sources and versions identified
* Validation test suites available
* GitLab integration configured (recommended)

Procedure
---------

#. Understand catalog structure.

BuildStreaM catalogs use a hierarchical structure:

.. code-block:: yaml

   catalog_version: "1.0"
   description: "Description of the catalog purpose"
   
   roles:
     # Role definitions here
   
   packages:
     # Package definitions here
   
   validation_dependencies:
     # Validation dependencies here

.. note::
   The catalog version should follow semantic versioning (major.minor.patch).

#. Define packages.

Specify all software packages that will be used in your builds:

.. code-block:: yaml

   packages:
     - name: "rocky-linux"
       type: "os"
       version: "8.8"
       source: "https://download.rockylinux.org/8.8/isos/x86_64/"
       checksum: "sha256:abc123..."
       
     - name: "kubernetes"
       type: "container-runtime"
       version: "1.28.2"
       source: "https://kubernetes.io/releases/"
       dependencies:
         - "containerd"
         - "cri-tools"
       
     - name: "slurm"
       type: "scheduler"
       version: "23.02.4"
       source: "https://download.schedmd.com/slurm/"
       config_files:
         - "slurm.conf"
         - "cgroup.conf"

.. tip::
   Use the catalog generation script to automatically populate package information from repositories.

#. Define roles.

Create roles that represent different node types in your cluster:

.. code-block:: yaml

   roles:
     - name: "compute-node"
       description: "Standard compute node with Slurm worker"
       packages:
         - name: "rocky-linux"
           version: "8.8"
         - name: "slurm"
           version: "23.02.4"
         - name: "openmpi"
           version: "4.1.5"
       configuration:
         slurm_config:
           node_type: "compute"
           cpus: 64
           memory: "256GB"
         network_config:
           ib_network: true
           mtu: 2048
       
     - name: "management-node"
       description: "Cluster management and control plane"
       packages:
         - name: "rocky-linux"
           version: "8.8"
         - name: "kubernetes"
           version: "1.28.2"
         - name: "etcd"
           version: "3.5.9"
       configuration:
         kubernetes_config:
           role: "control-plane"
           pod_network: "10.244.0.0/16"

.. important::
   Each role must include at least one OS package. The OS package determines the base image for the role.

#. Configure validation dependencies.

Define validation requirements for each role:

.. code-block:: yaml

   validation_dependencies:
     - name: "basic-validation"
       description: "Basic functionality tests"
       required_for: ["compute-node", "management-node"]
       tests:
         - name: "boot-test"
           description: "Verify node boots successfully"
           timeout: 300
         - name: "network-test"
           description: "Verify network connectivity"
           timeout: 120
       
     - name: "slurm-validation"
       description: "Slurm scheduler integration tests"
       required_for: ["compute-node"]
       tests:
         - name: "slurm-daemon-test"
           description: "Verify slurmctld and slurmd start"
           timeout: 180
         - name: "job-submission-test"
           description: "Verify job submission works"
           timeout: 600
       
     - name: "kubernetes-validation"
       description: "Kubernetes cluster tests"
       required_for: ["management-node"]
       tests:
         - name: "api-server-test"
           description: "Verify Kubernetes API server responds"
           timeout: 120
         - name: "pod-scheduling-test"
           description: "Verify pod scheduling works"
           timeout: 300

#. Add custom configuration parameters.

Include role-specific configuration parameters:

.. code-block:: yaml

   roles:
     - name: "storage-node"
       description: "Node with storage configuration"
       packages:
         - name: "rocky-linux"
           version: "8.8"
         - name: "ceph"
           version: "17.2.6"
       configuration:
         storage_config:
           backend: "ceph"
           osd_devices: ["/dev/sdb", "/dev/sdc"]
           network_config:
             public_network: "10.0.1.0/24"
             cluster_network: "10.0.2.0/24"
         ceph_config:
           fs_type: "xfs"
           crush_rule: "default"

.. note::
   Configuration parameters are passed to the build scripts and can be referenced in Ansible playbooks.

#. Validate catalog syntax.

Use the BuildStreaM catalog validator to check your catalog:

.. code-block:: bash

   curl -X POST "http://localhost:8080/api/v1/catalog/validate" \
        -H "Authorization: Bearer <your-oauth-token>" \
        -H "Content-Type: application/json" \
        -d @catalog.yaml

Expected successful response:

.. code-block:: json

   {
     "valid": true,
     "errors": [],
     "warnings": [
       "Package 'openmpi' has optional dependencies not specified"
     ]
   }

#. Test catalog with a build job.

Submit a test build to verify your catalog works correctly:

.. code-block:: bash

   curl -X POST "http://localhost:8080/api/v1/jobs" \
        -H "Authorization: Bearer <your-oauth-token>" \
        -H "Content-Type: application/json" \
        -d '{
          "catalog_path": "/path/to/your/catalog.yaml",
          "build_options": {
            "dry_run": true,
            "validate_only": true
          }
        }'

Result
------

Your BuildStreaM catalog is now configured and ready for automated builds. The catalog defines all the components needed to build and validate your HPC cluster images.

Verification
------------

Verify the catalog configuration is correct:

#. Check that all packages are accessible and have valid checksums:

.. code-block:: bash

   # Test package download
   curl -I "https://download.rockylinux.org/8.8/isos/x86_64/Rocky-8.8-x86_64-minimal.iso"

#. Validate role dependencies:

.. code-block:: bash

   # Check for circular dependencies
   python3 /opt/omnia/buildstream/scripts/check-deps.py catalog.yaml

#. Test validation dependency coverage:

.. code-block:: bash

   # Ensure all roles have required validations
   curl -X GET "http://localhost:8080/api/v1/catalog/validation-coverage" \
        -H "Authorization: Bearer <your-oauth-token>" \
        -d '{"catalog_path": "/path/to/your/catalog.yaml"}'

Expected output shows 100% coverage:

.. code-block:: json

   {
     "coverage": "100%",
     "uncovered_roles": [],
     "missing_validations": []
   }

Next Steps
----------

After configuring your catalog:

* **Create multiple catalogs**: Separate catalogs for different environments (dev, test, prod)
* **Set up catalog versioning**: Use semantic versioning for catalog changes
* **Configure automated testing**: Integrate catalog validation in your CI/CD pipeline
* **Document custom configurations**: Create reference documentation for your specific configurations

.. tip::
   Use the catalog generation script to create catalogs from existing configurations:

   .. code-block:: bash

      python3 /opt/omnia/buildstream/scripts/generate-catalog.py \
         --source-dir /path/to/existing/configs \
         --output catalog.yaml

For troubleshooting catalog issues, see :doc:`../troubleshooting/buildstream-issues`.

Related Topics
--------------

* :doc:`concept-architecture`
* :doc:`how-to-get-started`
* :doc:`how-to-gitlab-integration`
* :doc:`../reference/api/buildstream`
