
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Prepare OIM 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../../index.html)

[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../../index.html)

Overview 
 * [ Architecture ](../../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * Prepare OIM [ Prepare OIM ](prepare_oim.html) Table of contents 
 * [ Overview ](#overview)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Overview ](#overview)

 1. [ Home ](../../index.html)
 2. [ How-to Guides ](../index.html)
 3. [ Setup ](prepare_oim.html)

# Prepare the OIM[¶](#prepare-the-oim "Permanent link")

Prepare the Omnia Infrastructure Manager (OIM) by deploying the core management services: OpenCHAMI (provisioning), Pulp (repository management), and optionally BuildStreaM and Omnia Auth containers.

## Overview[¶](#overview "Permanent link")

The `prepare_oim.yml` playbook configures the OIM host with all services required for bare-metal provisioning and cluster management. It reads your `network_spec.yml` and `provision_config.yml` input files and deploys:

 * **OpenCHAMI** \-- Node discovery, state management, and boot script services.
 * **Pulp** \-- RPM repository management and synchronization.
 * **CoreDHCP** \-- DHCP service for PXE boot on the admin network.
 * **MinIO** \-- S3-compatible object storage for boot images and artifacts.
 * **Registry** \-- Local container image registry.
 * **BuildStreaM** _(optional)_ \-- CI/CD pipeline services.
 * **Omnia Auth** _(optional)_ \-- Centralized authentication container.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Deploy Omnia Core](deploy_omnia_core.html) procedure is complete.
 * The [Configure Inputs](configure_inputs.html) procedure is complete (`network_spec.yml` and `provision_config.yml` are configured).
 * The [Configure Credentials](configure_credentials.html) procedure is complete (encrypted credentials file exists).
 * The OIM has at least 2 NICs connected to the admin and BMC networks.
 * Network switches are configured with the appropriate VLANs.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Review and edit network_spec.yml** (if not already done):

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/network_spec.yml
 

Ensure the admin and BMC network parameters match your physical network:

File: /opt/omnia/input/project_default/network_spec.yml
 
 
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
 

 1. **Review and edit provision_config.yml** (if not already done):

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/provision_config.yml
 

File: /opt/omnia/input/project_default/provision_config.yml
 
 
 ---
 timezone: "America/Chicago"
 language: "en-US"
 iso_file_path: "/opt/omnia/iso/RHEL-8.8-x86_64-dvd.iso"
 default_lease_time: 86400
 pxe_mapping_file_path: "/opt/omnia/input/project_default/pxe_mapping_file.csv"
 

 1. **Run the prepare_oim playbook** :

Run on: omnia_core container
 
 
 cd /omnia/prepare_oim
 ansible-playbook prepare_oim.yml
 

!!! note
 
 
 If your credentials file is encrypted with Ansible Vault, add the
 `--ask-vault-pass` flag:
 
 ```bash title="Run on: omnia_core container"
 ansible-playbook prepare_oim.yml --ask-vault-pass
 ```
 

The playbook performs the following tasks:

 * Validates input files.
 * Configures network interfaces on the OIM.
 * Deploys OpenCHAMI services (SMD, BSS, CoreDHCP, TFTP).
 * Deploys Pulp for RPM repository management.
 * Deploys MinIO for S3-compatible object storage.
 * Sets up the local container registry.
 * Optionally deploys BuildStreaM and Omnia Auth containers.

Execution time: **15-30 minutes** depending on network speed and hardware.

## Verification[¶](#verification "Permanent link")

 1. **Check the omnia.target service tree** :

Run on: OIM host
 
 
 systemctl list-dependencies omnia.target
 

Expected service tree:

Expected output on: OIM host
 
 
 omnia.target
 ├─minio.service
 ├─omnia_auth.service
 ├─omnia_core.service
 ├─pulp.service
 ├─registry.service
 └─openchami.target
 ├─bss.service
 ├─coredhcp.service
 ├─cloud-init-server.service
 ├─dnsmasq.service
 ├─hydra.service
 ├─image-server.service
 ├─opaal.service
 ├─smd.service
 └─tftpd.service
 

 1. **Verify all services are active** :

Run on: OIM host
 
 
 systemctl status omnia_core.service
 systemctl status openchami.target
 

 1. **Test OpenCHAMI CLI** :

Run on: omnia_core container
 
 
 ochami --help
 

This should display the OpenCHAMI command-line help, confirming the CLI is installed and the services are accessible.

 1. **Verify Pulp is running** :

Run on: OIM host
 
 
 podman ps --filter name=pulp
 

 1. **Verify MinIO is accessible** :

Run on: omnia_core container
 
 
 s3cmd ls
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Verify Oim Services](verify_oim_services.html) \-- Detailed verification of all OIM services.
 * [Create Local Repos](create_local_repos.html) \-- Sync RPM repositories via Pulp.
 * [Build Cluster Images](build_cluster_images.html) \-- Build OS images for cluster nodes.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Playbook fails with "network interface not found"** Verify the `nic_name` in `network_spec.yml` matches the actual interface names on the OIM:

Run on: OIM host
 
 
 ip link show
 

**OpenCHAMI services fail to start** Check the OpenCHAMI container logs:

Run on: OIM host
 
 
 podman logs smd
 podman logs bss
 podman logs coredhcp
 

**Pulp container fails to start** Ensure sufficient disk space is available (Pulp requires significant storage for repository synchronization):

Run on: OIM host
 
 
 df -h /var/lib/containers
 

**Port conflicts** Ensure no other services are listening on ports used by OIM services (DHCP: 67, TFTP: 69, HTTP: 80/8080, MinIO: 9000):

Run on: OIM host
 
 
 ss -tlnp | grep -E ':(67|69|80|8080|9000)\b'
 

**Playbook fails at credentials step** Ensure you pass `--ask-vault-pass` and enter the correct Vault password.

Back to top [ Previous How-to Guides ](../index.html) [ Next Configure Inputs ](configure_inputs.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
