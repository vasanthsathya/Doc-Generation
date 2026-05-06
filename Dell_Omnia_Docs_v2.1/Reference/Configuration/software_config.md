
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Software Config 

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
 * Software Config [ Software Config ](software_config.html) Table of contents 
 * [ Schema ](#schema)
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

 * [ Schema ](#schema)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Configuration ](omnia_config.html)

# software_config.json Reference[¶](#software_configjson-reference "Permanent link")

File path: `/opt/omnia/input/project_default/software_config.json`

This file defines which software packages are installed on each functional group of nodes. It is a JSON array where each element maps a functional group to a list of software packages.

## Schema[¶](#schema "Permanent link")

`software_config.json` is a JSON array of objects. Each object represents one functional group and specifies the software packages to install on nodes belonging to that group.

File: /opt/omnia/input/project_default/software_config.json
 
 
 [
 {
 "functional_group_name": "<group_name>",
 "software": [
 {
 "name": "<package_name>",
 "version": "<version>"
 }
 ]
 }
 ]
 

## Field reference[¶](#field-reference "Permanent link")

Field | Type | Required | Description 
---|---|---|--- 
`functional_group_name` | String | Yes | Name of the functional group as defined in the PXE mapping CSV (e.g., `slurm_control_node`, `slurm_node`, `kube_control_plane`, `kube_node`, `login_node`, `auth_server`). 
`software` | Array | Yes | List of software package objects to install on nodes in this group. 
`software[].name` | String | Yes | Package or component name. Must match a package known to the Omnia software catalog (see table below). 
`software[].version` | String | No | Specific version to install. If omitted, the default version bundled with Omnia v2.1 is used. 
 
## Supported software packages[¶](#supported-software-packages "Permanent link")

Package Name | Applicable Groups | Description 
---|---|--- 
`slurm` | `slurm_control_node`, `slurm_node`, `login_node` | Slurm workload manager (slurmctld, slurmd, or client tools depending on group). 
`kubernetes` | `kube_control_plane`, `kube_node` | Kubernetes cluster components (kubeadm, kubelet, kubectl). 
`calico` | `kube_control_plane` | Calico CNI plugin for pod networking. 
`metallb` | `kube_control_plane` | MetalLB bare-metal load balancer. 
`nfs_csi` | `kube_control_plane` | NFS CSI driver for persistent volume provisioning. 
`nvidia_gpu` | `slurm_node`, `kube_node` | NVIDIA GPU drivers and CUDA Toolkit. 
`amd_gpu` | `slurm_node`, `kube_node` | AMD ROCm GPU drivers. 
`openldap` | `auth_server` | OpenLDAP authentication server. 
`freeipa` | `auth_server` | FreeIPA identity management (alternative to OpenLDAP). 
`beegfs_client` | `slurm_node`, `kube_node` | BeeGFS parallel filesystem client. 
`telemetry` | `kube_control_plane`, `kube_node` | Telemetry stack (Kafka, VictoriaMetrics, Grafana). 
`ldms` | `slurm_node` | LDMS metric samplers for OS-level telemetry. 
`node_exporter` | All groups | Prometheus-compatible node metrics exporter. 
 
## Usage example[¶](#usage-example "Permanent link")

See [Software Config Json](../SampleFiles/software_config_json.html) for complete annotated examples covering Slurm-only, Slurm + K8s, and telemetry-only scenarios.

File: /opt/omnia/input/project_default/software_config.json
 
 
 [
 {
 "functional_group_name": "slurm_control_node",
 "software": [
 {"name": "slurm", "version": "23.11"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "slurm_node",
 "software": [
 {"name": "slurm", "version": "23.11"},
 {"name": "nvidia_gpu"},
 {"name": "ldms"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "kube_control_plane",
 "software": [
 {"name": "kubernetes", "version": "1.29"},
 {"name": "calico"},
 {"name": "metallb"},
 {"name": "nfs_csi"}
 ]
 }
 ]
 

Note

 * The `functional_group_name` must exactly match the value in the `FUNCTIONAL_GROUP_NAME` column of the PXE mapping CSV.
 * If a functional group has no entry in `software_config.json`, only the base OS packages are installed on those nodes.
 * Invalid package names cause `input_validator.yml` to fail with a descriptive error.

Info

 * [Software Config Json](../SampleFiles/software_config_json.html) \-- Complete sample files for different scenarios.
 * [Pxe Mapping File](../SampleFiles/pxe_mapping_file.html) \-- PXE mapping CSV that defines functional groups.
 * [Local Repo Config](local_repo_config.html) \-- Repository sources for these packages.

Back to top [ Previous Network Spec ](network_spec.html) [ Next Telemetry Config ](telemetry_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
