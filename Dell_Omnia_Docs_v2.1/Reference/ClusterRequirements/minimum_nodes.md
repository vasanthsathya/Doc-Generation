
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Minimum Nodes 

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
 * [ PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * Minimum Nodes [ Minimum Nodes ](minimum_nodes.html) Table of contents 
 * [ Node count summary ](#node-count-summary)
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

 * [ Node count summary ](#node-count-summary)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Cluster Requirements ](minimum_nodes.html)

# Minimum Node Counts[¶](#minimum-node-counts "Permanent link")

This page lists the minimum number of servers required for each Omnia deployment scenario. The OIM (management node) is always required in addition to the cluster nodes listed below.

## Node count summary[¶](#node-count-summary "Permanent link")

Deployment Scenario | Min. Nodes | Node Breakdown 
---|---|--- 
**Slurm-only (Path A)** | 4 | 1 OIM + 1 Slurm control + 1 Slurm compute + 1 login node 
**Full deployment (Path B)** | 8 | 1 OIM + 1 Slurm control + 1 Slurm compute + 1 login + 3 K8s control plane + 1 K8s worker (auth server may be co-located) 
**K8s + Telemetry only (Path C)** | 5 | 1 OIM + 3 K8s control plane + 1 K8s worker 
**BuildStreaM (Path D)** | 8+ | 1 OIM + 1 Slurm control + 1 Slurm compute + 1 login + 3 K8s control plane + 1 K8s worker (GitLab and runners on K8s) 
 
## Detailed breakdown by role[¶](#detailed-breakdown-by-role "Permanent link")

Node Role | Slurm Only | Full | K8s + Tel. | BuildStreaM | Notes 
---|---|---|---|---|--- 
OIM | 1 | 1 | 1 | 1 | Always exactly 1. Cannot be co-located with cluster roles. 
slurm_control_node | 1 | 1 | \-- | 1 | Runs slurmctld, slurmdbd, MariaDB. 
slurm_node | 1+ | 1+ | \-- | 1+ | Compute nodes. Scale out as needed. 
login_node | 1 | 1 | \-- | 1 | Optional but recommended. Can be omitted; users then SSH to the control node. 
kube_control_plane | \-- | 3 | 3 | 3 | 3 required for HA quorum. 1 is acceptable for non-HA (development only). 
kube_node | \-- | 1+ | 1+ | 1+ | Worker nodes for K8s pods. 
auth_server | 0--1 | 0--1 | \-- | 0--1 | Optional dedicated node. Authentication can run on an existing Slurm or K8s node. 
 
## Scaling guidelines[¶](#scaling-guidelines "Permanent link")

Cluster Size | Recommendation 
---|--- 
< 50 nodes | Standard OIM (4 cores, 32 GB RAM). Single Slurm control node. 
50--200 nodes | Upgraded OIM (8 cores, 64 GB RAM). Consider dedicated auth server. 
200--500 nodes | High-spec OIM (16 cores, 128 GB RAM). Dedicated login node(s). Add K8s workers for monitoring load. 
500+ nodes | Multiple login nodes. External NFS or PowerScale for /home. Increase Pulp storage. Consider external etcd for K8s HA. 
 
Note

The OIM must remain a dedicated, standalone server. Do not co-locate Slurm or Kubernetes roles on the OIM -- this is unsupported and will cause resource contention with the management services.

Info

 * [Disk Space](disk_space.html) \-- Disk requirements per node role.
 * [Ports](ports.html) \-- Network ports required per role.
 * [Ha Config](../Configuration/ha_config.html) \-- Kubernetes HA settings.

Back to top [ Previous software_config.json ](../SampleFiles/software_config_json.html) [ Next Disk Space ](disk_space.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
