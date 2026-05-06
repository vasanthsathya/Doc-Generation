
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Omnia Config 

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
 * Omnia Config [ Omnia Config ](omnia_config.html) Table of contents 
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

# omnia_config.yml Reference[¶](#omnia_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/omnia_config.yml`

This file controls the deployment of Slurm, Kubernetes, and GPU software across cluster nodes.

## Parameter reference[¶](#parameter-reference "Permanent link")

### Scheduler settings[¶](#scheduler-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`scheduler_type` | String | No | `slurm` | Job scheduler to deploy. Accepted values: `slurm`, `k8s`, `slurm,k8s` (both). When set to `k8s`, Slurm components are skipped. 
`slurm_installation_type` | String | No | `nfs_share` | How Slurm binaries and configuration are distributed. Values: `nfs_share` (shared NFS mount), `configless` (slurmd fetches config from slurmctld at startup). 
`slurm_config_path` | String | No | (auto-generated) | Custom path to a user-provided `slurm.conf`. If omitted, Omnia generates a default configuration. See [Slurm Conf](../SampleFiles/slurm_conf.html). 
`restart_slurm_services` | Boolean | No | `true` | Whether to restart Slurm daemons after configuration changes during `omnia.yml` execution. 
 
### Kubernetes settings[¶](#kubernetes-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`k8s_version` | String | No | `1.29` | Kubernetes version to deploy. Must match a version available in the local repository. 
`k8s_cni` | String | No | `calico` | Container Network Interface plugin. Currently only `calico` is supported. 
`k8s_pod_network_cidr` | String | No | `10.244.0.0/16` | CIDR block for Kubernetes pod networking. Must not overlap with any physical network. 
`k8s_service_cidr` | String | No | `10.96.0.0/12` | CIDR block for Kubernetes ClusterIP services. 
`metallb_address_range` | String | No | (none) | IP range for MetalLB external load balancer assignments (e.g., `192.168.1.240-192.168.1.250`). Required if MetalLB is enabled. 
 
### GPU settings[¶](#gpu-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`enable_nvidia_gpu` | Boolean | No | `false` | Install NVIDIA GPU drivers and CUDA Toolkit on nodes with NVIDIA GPUs. 
`cuda_toolkit_version` | String | No | `12.4` | CUDA Toolkit version to install. Must be available in the configured repository. 
`enable_amd_gpu` | Boolean | No | `false` | Install ROCm and AMD GPU drivers on nodes with AMD Instinct GPUs. 
`rocm_version` | String | No | `6.1` | ROCm version to install. 
`enable_gpu_slurm_gres` | Boolean | No | `true` | Register GPUs as Slurm GRES (Generic Resources) for GPU-aware job scheduling. Only effective when `scheduler_type` includes `slurm`. 
 
### Miscellaneous settings[¶](#miscellaneous-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`login_node_required` | Boolean | No | `true` | Whether to configure a dedicated login node. If `false`, users SSH directly to the Slurm control node. 
`auth_server_required` | Boolean | No | `true` | Whether to deploy a centralized authentication server (OpenLDAP or FreeIPA). 
`nfs_client_params` | String | No | (none) | Additional NFS mount options applied to all client-side mounts (e.g., `vers=4.1,noatime`). 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 scheduler_type: "slurm,k8s"
 slurm_installation_type: "nfs_share"
 restart_slurm_services: true
 
 k8s_version: "1.29"
 k8s_cni: "calico"
 k8s_pod_network_cidr: "10.244.0.0/16"
 k8s_service_cidr: "10.96.0.0/12"
 metallb_address_range: "192.168.1.240-192.168.1.250"
 
 enable_nvidia_gpu: true
 cuda_toolkit_version: "12.4"
 enable_amd_gpu: false
 enable_gpu_slurm_gres: true
 
 login_node_required: true
 auth_server_required: true
 

Info

 * [Software Config](software_config.html) \-- Package-level software selection.
 * [Slurm Conf](../SampleFiles/slurm_conf.html) \-- Custom Slurm configuration.
 * [Ha Config](ha_config.html) \-- Kubernetes high-availability settings.
 * [Playbook Reference](../Playbooks/playbook_reference.html) \-- The `omnia.yml` playbook that consumes this file.

Back to top [ Previous Installed Software ](../SupportMatrix/installed_software.html) [ Next Provision Config ](provision_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
