

Configure Inputs
================


Configure Omnia's input files to define your cluster topology, software stack,
and deployment preferences. Input files are YAML and JSON templates located at
``/opt/omnia/input/project_default/`` inside the ``omnia_core`` container.


Overview
--------


Omnia uses a set of input files to drive every playbook. Before running any
provisioning or deployment playbook, you must:

#. Copy the example templates from ``/omnia/examples/input_template/`` to the
   working input directory.
#. Edit each file to match your environment (network ranges, software
   selections, cluster layout).
#. Optionally run the ``input_validator`` to catch configuration errors early.

The most important input files are:

- ``software_config.json`` -- Defines which software stacks to deploy.
- ``network_spec.yml`` -- Network configuration for admin, BMC, and compute
  networks.
- ``provision_config.yml`` -- Provisioning parameters (OS image, timezone,
  kernel options).
- ``omnia_config.yml`` -- Cluster-level configuration (Slurm, K8s, storage).



Prerequisites
-------------


- The `Deploy Omnia Core <deploy_omnia_core.rst>`_ procedure is complete and ``omnia_core`` is
  running.
- You have planned your network topology (IP ranges, VLANs, subnets).
- You know which software stacks you want to deploy (Slurm, Kubernetes,
  telemetry, etc.).



Procedure
---------


#. **Enter the omnia_core container**:


**Run on: OIM host**

.. code-block:: bash
      ssh omnia_core



#. **Copy the example templates** to the input directory:


**Run on: omnia_core container**

.. code-block:: bash
      cp /omnia/examples/input_template/* /opt/omnia/input/project_default/



   !!! note

       If files already exist in the destination, this command will overwrite
       them. Back up any previously customized files before copying.

#. **Edit the software configuration**:


**Run on: omnia_core container**

.. code-block:: bash
      vi /opt/omnia/input/project_default/software_config.json



   Example ``software_config.json``:


**File: /opt/omnia/input/project_default/software_config.json**

.. code-block:: json
      {
          "cluster_os_type": "rhel",
          "cluster_os_version": "8.8",
          "repo_config": "partial",
          "softwares": [
              {"name": "slurm"},
              {"name": "openldap"},
              {"name": "cuda", "version": "12.2"},
              {"name": "apptainer"}
          ]
      }



   Key parameters:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      - - Parameter
        - Description
      - - ``cluster_os_type``
        - Target OS: ``rhel`` or ``rocky``
      - - ``cluster_os_version``
        - OS version for provisioned nodes (e.g., ``8.8``, ``9.2``)
      - - ``repo_config``
        - Repository strategy: ``partial`` (Omnia-managed repos only),
          ``always`` (sync all repos), ``never`` (skip repo config)
      - - ``softwares``
        - List of software stacks to install on compute nodes

#. **Edit the network specification**:


**Run on: omnia_core container**

.. code-block:: bash
      vi /opt/omnia/input/project_default/network_spec.yml



   Example ``network_spec.yml``:


**File: /opt/omnia/input/project_default/network_spec.yml**

.. code-block:: yaml
      ---
      admin_network:
        nic_name: "eno1"
        static_range: "10.5.0.100-10.5.0.200"
        dynamic_range: "10.5.0.201-10.5.0.254"
        subnet: "10.5.0.0"
        netmask: "255.255.255.0"
        gateway: "10.5.0.1"
   
      bmc_network:
        nic_name: "eno2"
        static_range: "10.3.0.100-10.3.0.200"
        dynamic_range: "10.3.0.201-10.3.0.254"
        subnet: "10.3.0.0"
        netmask: "255.255.255.0"



#. **Edit the provision configuration**:


**Run on: omnia_core container**

.. code-block:: bash
      vi /opt/omnia/input/project_default/provision_config.yml



   Example ``provision_config.yml``:


**File: /opt/omnia/input/project_default/provision_config.yml**

.. code-block:: yaml
      ---
      timezone: "America/Chicago"
      language: "en-US"
      iso_file_path: "/opt/omnia/iso/RHEL-8.8-x86_64-dvd.iso"
      default_lease_time: 86400
      pxe_mapping_file_path: "/opt/omnia/input/project_default/pxe_mapping_file.csv"



#. **Edit the Omnia configuration** (for Slurm/K8s parameters):


**Run on: omnia_core container**

.. code-block:: bash
      vi /opt/omnia/input/project_default/omnia_config.yml



   Example ``omnia_config.yml``:


**File: /opt/omnia/input/project_default/omnia_config.yml**

.. code-block:: yaml
      ---
      mariadb_password: ""
      k8s_version: "1.28"
      k8s_cni: "calico"
      slurm_installation_type: "nfs_share"
      enable_omnia_nfs: true



#. **(Optional) Run the input validator** to check your configuration:


**Run on: omnia_core container**

.. code-block:: bash
      cd /omnia
      ansible-playbook input_validator.yml



   The validator checks for:

  - Missing required fields.
  - IP address format and range conflicts.
  - Valid software names and versions.
  - Consistent network configuration.



Verification
------------


#. **List all input files** and confirm they are populated:


**Run on: omnia_core container**

.. code-block:: bash
      ls -la /opt/omnia/input/project_default/



#. **Review the software configuration**:


**Run on: omnia_core container**

.. code-block:: bash
      cat /opt/omnia/input/project_default/software_config.json | python3 -m json.tool



#. **Validate YAML syntax** for each YAML input file:


**Run on: omnia_core container**

.. code-block:: bash
      python3 -c "import yaml; yaml.safe_load(open('/opt/omnia/input/project_default/network_spec.yml'))"



   No output means the YAML is syntactically valid.



Next Steps
----------


- `Configure Credentials <configure_credentials.rst>`_ -- Set up encrypted credentials for provisioning.
- `Prepare Oim <prepare_oim.rst>`_ -- Prepare OIM services (OpenCHAMI, Pulp, etc.).



Troubleshooting
---------------


**input_validator fails with "missing required field"**
   Open the indicated file and ensure all required fields are present. Refer to
   the example templates in ``/omnia/examples/input_template/`` for the complete
   list of required fields.

**JSON syntax error in software_config.json**
   Validate JSON syntax:


**Run on: omnia_core container**

.. code-block:: bash
      python3 -m json.tool /opt/omnia/input/project_default/software_config.json



**Network range overlap**
   Ensure ``admin_network`` and ``bmc_network`` use different subnets.
   Static and dynamic ranges within each network must not overlap.

**Template files not found in /omnia/examples/input_template/**
   Verify the Omnia repository version. Templates are available in v2.1.0.0
   and later. Pull the latest code if necessary:


**Run on: OIM host**

.. code-block:: bash
      cd /opt/omnia && git pull

