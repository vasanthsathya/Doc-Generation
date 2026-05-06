
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

PXE Mapping File 

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
 * PXE Mapping File [ PXE Mapping File ](pxe_mapping_file.html) Table of contents 
 * [ Column reference ](#column-reference)
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

 * [ Column reference ](#column-reference)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Sample Files ](pxe_mapping_file.html)

# PXE Mapping File (CSV)[¶](#pxe-mapping-file-csv "Permanent link")

File path: Specified by `pxe_mapping_file_path` in `provision_config.yml` (e.g., `/opt/omnia/input/project_default/pxe_mapping.csv`)

The PXE mapping file is a CSV that assigns each physical server to a functional group, hostname, and set of network addresses. Omnia reads this file during `discovery.yml` and `omnia.yml` to determine which role each server plays and how it is addressed on the network.

## Column reference[¶](#column-reference "Permanent link")

Column | Required | Description 
---|---|--- 
`FUNCTIONAL_GROUP_NAME` | Yes | The role this node plays in the cluster. Must match a group name in `software_config.json`. Values: `slurm_control_node`, `slurm_node`, `login_node`, `kube_control_plane`, `kube_node`, `auth_server`. 
`GROUP_NAME` | Yes | A logical sub-group for organizing nodes (e.g., `gpu_nodes`, `cpu_nodes`, `storage_nodes`). Used for Ansible inventory grouping. 
`SERVICE_TAG` | Yes | Dell service tag of the server (7-character alphanumeric string found on the server chassis or in iDRAC). Used for unique node identification. 
`PARENT_SERVICE_TAG` | No | Service tag of the parent chassis for multi-node systems (e.g., C6620, C6625). Leave blank for standalone servers. 
`HOSTNAME` | Yes | Hostname to assign to the node. Must comply with hostname rules (see [Hostname Requirements](../Appendices/hostname_requirements.html)). 
`ADMIN_MAC` | Yes | MAC address of the admin network NIC (used for PXE boot). Format: `AA:BB:CC:DD:EE:FF`. 
`ADMIN_IP` | Yes | Static IP address on the admin network. Must be within the admin subnet defined in `network_spec.yml` and outside the `dynamic_range`. 
`BMC_MAC` | No | MAC address of the BMC/iDRAC interface. Used for BMC discovery and address assignment. 
`BMC_IP` | No | Static IP address for the BMC/iDRAC interface. Must be within the BMC subnet. 
 
## Sample file[¶](#sample-file "Permanent link")

Sample pxe_mapping_file.csv
 
 
 FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,PARENT_SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
 slurm_control_node,slurm_head,ABC1234,,slurm-ctrl-01,EC:2A:72:34:56:01,10.5.0.10,,10.3.0.10
 slurm_node,gpu_nodes,DEF5678,,slurm-gpu-01,EC:2A:72:34:56:02,10.5.0.11,,10.3.0.11
 slurm_node,gpu_nodes,GHI9012,,slurm-gpu-02,EC:2A:72:34:56:03,10.5.0.12,,10.3.0.12
 slurm_node,cpu_nodes,JKL3456,,slurm-cpu-01,EC:2A:72:34:56:04,10.5.0.13,,10.3.0.13
 login_node,login,MNO7890,,login-01,EC:2A:72:34:56:05,10.5.0.14,,10.3.0.14
 kube_control_plane,k8s_cp,PQR1234,,kube-cp-01,EC:2A:72:34:56:06,10.5.0.20,,10.3.0.20
 kube_control_plane,k8s_cp,STU5678,,kube-cp-02,EC:2A:72:34:56:07,10.5.0.21,,10.3.0.21
 kube_control_plane,k8s_cp,VWX9012,,kube-cp-03,EC:2A:72:34:56:08,10.5.0.22,,10.3.0.22
 kube_node,k8s_workers,YZA3456,,kube-wk-01,EC:2A:72:34:56:09,10.5.0.23,,10.3.0.23
 kube_node,k8s_workers,BCD7890,,kube-wk-02,EC:2A:72:34:56:0A,10.5.0.24,,10.3.0.24
 auth_server,auth,EFG1234,,auth-01,EC:2A:72:34:56:0B,10.5.0.30,,10.3.0.30
 

## Annotated breakdown[¶](#annotated-breakdown "Permanent link")

**Slurm control node**

Example: Slurm control node
 
 
 slurm_control_node,slurm_head,ABC1234,,slurm-ctrl-01,EC:2A:72:34:56:01,10.5.0.10,,10.3.0.10
 

 * Runs `slurmctld` and `slurmdbd`.
 * Exactly one node should have this functional group per Slurm cluster.
 * `PARENT_SERVICE_TAG` is empty (standalone server).

**Slurm compute nodes**

Example: Slurm compute nodes
 
 
 slurm_node,gpu_nodes,DEF5678,,slurm-gpu-01,EC:2A:72:34:56:02,10.5.0.11,,10.3.0.11
 slurm_node,cpu_nodes,JKL3456,,slurm-cpu-01,EC:2A:72:34:56:04,10.5.0.13,,10.3.0.13
 

 * Runs `slurmd`.
 * `GROUP_NAME` distinguishes GPU-equipped nodes (`gpu_nodes`) from CPU-only nodes (`cpu_nodes`). This grouping can be used in Slurm partitions.

**Login node**

Example: Login node
 
 
 login_node,login,MNO7890,,login-01,EC:2A:72:34:56:05,10.5.0.14,,10.3.0.14
 

 * Provides interactive SSH access for users to submit jobs.
 * Does not run `slurmd`; configured as a Slurm client only.

**Kubernetes control plane**

Example: Kubernetes control plane
 
 
 kube_control_plane,k8s_cp,PQR1234,,kube-cp-01,EC:2A:72:34:56:06,10.5.0.20,,10.3.0.20
 

 * Runs the Kubernetes API server, etcd, scheduler, and controller-manager.
 * For HA, use 3 control plane nodes (see [Ha Config](../Configuration/ha_config.html)).

**Kubernetes worker nodes**

Example: Kubernetes worker nodes
 
 
 kube_node,k8s_workers,YZA3456,,kube-wk-01,EC:2A:72:34:56:09,10.5.0.23,,10.3.0.23
 

 * Runs `kubelet` and `kube-proxy`; hosts application pods.

**Multi-node chassis example (C6620)**

Example: Multi-node chassis (C6620)
 
 
 slurm_node,cpu_nodes,SLD1234,CHASSIS01,sled-01,EC:2A:72:34:56:10,10.5.0.40,,10.3.0.40
 slurm_node,cpu_nodes,SLD5678,CHASSIS01,sled-02,EC:2A:72:34:56:11,10.5.0.41,,10.3.0.41
 

 * `PARENT_SERVICE_TAG` identifies the shared chassis.
 * Each sled has its own service tag, hostname, and network addresses.

## Validation rules[¶](#validation-rules "Permanent link")

Rule | Description 
---|--- 
Unique `SERVICE_TAG` | No two rows may share the same service tag. 
Unique `HOSTNAME` | Each hostname must be unique across the entire file. 
Unique `ADMIN_IP` | Admin IP addresses must not overlap with each other or with the OIM's admin IP. 
Unique `ADMIN_MAC` | Each admin MAC address must be unique. 
Valid `FUNCTIONAL_GROUP_NAME` | Must be one of the recognized group names listed above. 
Hostname format | Lowercase, no domain suffix, RFC 952/1123 compliant. See [Hostname Requirements](../Appendices/hostname_requirements.html). 
IP within subnet | `ADMIN_IP` must fall within the admin network subnet and outside the `dynamic_range`. `BMC_IP` must fall within the BMC subnet. 
 
Note

The `input_validator.yml` playbook validates the PXE mapping file before provisioning begins. Any violations produce a descriptive error message identifying the offending row and column.

Info

 * [Provision Config](../Configuration/provision_config.html) \-- Where the mapping file path is specified.
 * [Software Config](../Configuration/software_config.html) \-- Software packages per functional group.
 * [Hostname Requirements](../Appendices/hostname_requirements.html) \-- Hostname rules.

Back to top [ Previous BuildStreaM Config ](../Configuration/buildstream_config.html) [ Next slurm.conf ](slurm_conf.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
