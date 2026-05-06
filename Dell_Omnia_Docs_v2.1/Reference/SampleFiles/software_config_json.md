
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

software_config.json 

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
 * [ Omnia Config ](../Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](pxe_mapping_file.html)
 * software_config.json [ software_config.json ](software_config_json.html) Table of contents 
 * [ Scenario 1: Slurm-only cluster ](#scenario-1-slurm-only-cluster)
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

 * [ Scenario 1: Slurm-only cluster ](#scenario-1-slurm-only-cluster)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Sample Files ](pxe_mapping_file.html)

# software_config.json Sample Files[¶](#software_configjson-sample-files "Permanent link")

File path: `/opt/omnia/input/project_default/software_config.json`

This page provides complete, annotated `software_config.json` examples for common deployment scenarios. Copy the scenario that best matches your deployment and modify as needed.

## Scenario 1: Slurm-only cluster[¶](#scenario-1-slurm-only-cluster "Permanent link")

Deploys a traditional HPC cluster with Slurm scheduling, NVIDIA GPU support, and LDMS telemetry on compute nodes. No Kubernetes.

Sample software_config.json: Slurm-only cluster
 
 
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
 "functional_group_name": "login_node",
 "software": [
 {"name": "slurm", "version": "23.11"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "auth_server",
 "software": [
 {"name": "openldap"},
 {"name": "node_exporter"}
 ]
 }
 ]
 

**Scenario 1 component summary**

Group | Installed Software 
---|--- 
`slurm_control_node` | Slurm 23.11 (slurmctld, slurmdbd), Node Exporter 
`slurm_node` | Slurm 23.11 (slurmd), NVIDIA GPU drivers/CUDA, LDMS samplers, Node Exporter 
`login_node` | Slurm 23.11 (client tools), Node Exporter 
`auth_server` | OpenLDAP, Node Exporter 
 
## Scenario 2: Slurm + Kubernetes (full deployment)[¶](#scenario-2-slurm-kubernetes-full-deployment "Permanent link")

Production-grade deployment with Slurm for HPC compute and Kubernetes for platform services, monitoring, and storage.

Sample software_config.json: Slurm + Kubernetes
 
 
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
 {"name": "beegfs_client"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "login_node",
 "software": [
 {"name": "slurm", "version": "23.11"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "kube_control_plane",
 "software": [
 {"name": "kubernetes", "version": "1.29"},
 {"name": "calico"},
 {"name": "metallb"},
 {"name": "nfs_csi"},
 {"name": "telemetry"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "kube_node",
 "software": [
 {"name": "kubernetes", "version": "1.29"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "auth_server",
 "software": [
 {"name": "openldap"},
 {"name": "node_exporter"}
 ]
 }
 ]
 

**Scenario 2 component summary**

Group | Installed Software 
---|--- 
`slurm_control_node` | Slurm 23.11 (slurmctld, slurmdbd), Node Exporter 
`slurm_node` | Slurm 23.11 (slurmd), NVIDIA GPU, LDMS, BeeGFS client, Node Exporter 
`login_node` | Slurm 23.11 (client), Node Exporter 
`kube_control_plane` | K8s 1.29, Calico, MetalLB, NFS CSI, Telemetry stack, Node Exporter 
`kube_node` | K8s 1.29, Node Exporter 
`auth_server` | OpenLDAP, Node Exporter 
 
## Scenario 3: Kubernetes + telemetry only (no Slurm)[¶](#scenario-3-kubernetes-telemetry-only-no-slurm "Permanent link")

Deploys a Kubernetes cluster with the full telemetry pipeline for infrastructure monitoring without a job scheduler.

Sample software_config.json: Kubernetes + telemetry only
 
 
 [
 {
 "functional_group_name": "kube_control_plane",
 "software": [
 {"name": "kubernetes", "version": "1.29"},
 {"name": "calico"},
 {"name": "metallb"},
 {"name": "nfs_csi"},
 {"name": "telemetry"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "kube_node",
 "software": [
 {"name": "kubernetes", "version": "1.29"},
 {"name": "node_exporter"}
 ]
 }
 ]
 

**Scenario 3 component summary**

Group | Installed Software 
---|--- 
`kube_control_plane` | K8s 1.29, Calico, MetalLB, NFS CSI, Telemetry stack (Kafka, VictoriaMetrics, Grafana), Node Exporter 
`kube_node` | K8s 1.29, Node Exporter 
 
## Scenario 4: AMD GPU compute nodes[¶](#scenario-4-amd-gpu-compute-nodes "Permanent link")

Slurm cluster with AMD Instinct GPU nodes instead of NVIDIA.

Sample software_config.json: AMD GPU compute nodes
 
 
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
 {"name": "amd_gpu"},
 {"name": "ldms"},
 {"name": "node_exporter"}
 ]
 },
 {
 "functional_group_name": "login_node",
 "software": [
 {"name": "slurm", "version": "23.11"},
 {"name": "node_exporter"}
 ]
 }
 ]
 

Note

 * The `version` field is optional. When omitted, Omnia installs the default version bundled with the release.
 * Every `functional_group_name` must match an entry in the PXE mapping CSV (see [Pxe Mapping File](pxe_mapping_file.html)).
 * Groups not listed in the JSON receive only base OS packages.

Info

 * [Software Config](../Configuration/software_config.html) \-- Full schema reference.
 * [Pxe Mapping File](pxe_mapping_file.html) \-- PXE mapping CSV that defines functional groups.
 * [Installed Software](../SupportMatrix/installed_software.html) \-- Complete software bill of materials.

Back to top [ Previous slurmdbd.conf ](slurmdbd_conf.html) [ Next Minimum Nodes ](../ClusterRequirements/minimum_nodes.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
