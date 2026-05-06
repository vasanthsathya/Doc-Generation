
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Provision Config 

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
 * [ Prepare OIM ](../../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](omnia_config.html)
 * Provision Config [ Provision Config ](provision_config.html) Table of contents 
 * [ Parameter reference ](#parameter-reference)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Parameter reference ](#parameter-reference)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Configuration ](omnia_config.html)

# provision_config.yml Reference[¶](#provision_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/provision_config.yml`

This file controls the provisioning behavior of the OIM, including PXE boot mapping, timezone, domain name, and OS image settings.

## Parameter reference[¶](#parameter-reference "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`pxe_mapping_file_path` | String | Yes | (none) | Absolute path to the PXE mapping CSV file that maps service tags to functional groups, hostnames, and network addresses. See [Pxe Mapping File](../SampleFiles/pxe_mapping_file.html) for the file format. 
`timezone` | String | No | `UTC` | IANA timezone string applied to all provisioned nodes (e.g., `America/New_York`, `Asia/Kolkata`). See [Timezones](../Appendices/timezones.html) for the full list. 
`domain_name` | String | No | `omnia.test` | DNS domain name assigned to all provisioned nodes. Must be a valid FQDN suffix (e.g., `hpc.example.com`). Do not include a leading dot. 
`repo_store_path` | String | No | `/opt/omnia/repo_store` | Local directory on the OIM where Pulp-mirrored repositories are stored. Must have sufficient disk space (see [Disk Space](../ClusterRequirements/disk_space.html)). 
`language` | String | No | `en-US` | System locale for provisioned nodes. 
`iso_file_path` | String | No | (none) | Absolute path to the RHEL 10.0 ISO on the OIM. Used by `build_image_x86_64.yml` and `build_image_aarch64.yml` to construct the provisioning image. 
`default_lease_time` | Integer | No | `86400` | DHCP lease duration in seconds for provisioned nodes. 
`provision_password` | String | Yes | (none) | Root password for provisioned nodes. Set via `credentials_utility.yml` \-- do not store in plain text. 
`provision_os` | String | No | `rhel` | Operating system to provision. Currently only `rhel` is supported in Omnia v2.1. 
`provision_os_version` | String | No | `10.0` | Version of the operating system to provision. 
`bmc_network` | Mapping | No | (see below) | BMC/iDRAC network configuration. Contains sub-keys for IP range and credentials. 
`bmc_network.bmc_static_range` | String | No | (none) | Static IP range for BMC interfaces (e.g., `10.3.0.100-10.3.0.200`). 
`bmc_network.bmc_dynamic_range` | String | No | (none) | Dynamic (DHCP) IP range for BMC discovery (e.g., `10.3.0.201-10.3.0.254`). 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/provision_config.yml
 
 
 pxe_mapping_file_path: "/opt/omnia/input/project_default/pxe_mapping.csv"
 timezone: "America/Chicago"
 domain_name: "hpc.example.com"
 repo_store_path: "/opt/omnia/repo_store"
 language: "en-US"
 iso_file_path: "/opt/omnia/iso/rhel-10.0-x86_64-dvd.iso"
 default_lease_time: 86400
 provision_os: "rhel"
 provision_os_version: "10.0"
 

Note

The `provision_password` parameter must be set using the `credentials_utility.yml` playbook. It is stored in an Ansible vault and is never written to `provision_config.yml` in plain text.

Info

 * [Pxe Mapping File](../SampleFiles/pxe_mapping_file.html) \-- PXE mapping CSV format.
 * [Timezones](../Appendices/timezones.html) \-- Valid timezone values.
 * [Hostname Requirements](../Appendices/hostname_requirements.html) \-- Hostname rules for provisioned nodes.
 * [Network Spec](network_spec.html) \-- Network configuration that complements provisioning.

Back to top [ Previous Omnia Config ](omnia_config.html) [ Next Network Spec ](network_spec.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
