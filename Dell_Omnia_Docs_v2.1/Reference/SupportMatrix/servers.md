
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Servers 

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
 * Servers [ Servers ](servers.html) Table of contents 
 * [ Intel-based servers ](#intel-based-servers)
 * Configuration Configuration 
 * [ Omnia Config ](../Configuration/omnia_config.html)
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

 * [ Intel-based servers ](#intel-based-servers)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Support Matrix ](servers.html)

# Supported Servers[¶](#supported-servers "Permanent link")

Omnia v2.1 supports the following Dell PowerEdge server models as cluster nodes (OIM, Slurm, and Kubernetes). Servers are grouped by CPU architecture.

## Intel-based servers[¶](#intel-based-servers "Permanent link")

Model | CPU Generation | Form Factor | Notes 
---|---|---|--- 
PowerEdge R660 | Intel 4th/5th Gen Xeon Scalable | 1U rack | Dual-socket; suitable for OIM, Slurm control, or login nodes. 
PowerEdge R760 | Intel 4th/5th Gen Xeon Scalable | 2U rack | Dual-socket; general-purpose compute and storage. 
PowerEdge R760xa | Intel 4th/5th Gen Xeon Scalable | 2U rack | GPU-accelerated variant; supports up to 4 double-width GPUs. 
PowerEdge R770 | Intel 5th Gen Xeon Scalable | 2U rack | Dual-socket; next-generation general-purpose compute. 
PowerEdge C6620 | Intel 4th/5th Gen Xeon Scalable | 2U multi-node (4 sleds) | High-density; 4 independent dual-socket sleds per 2U chassis. 
PowerEdge XE9680 | Intel 4th/5th Gen Xeon Scalable | 6U rack | AI/ML optimized; supports up to 8 NVIDIA GPUs (SXM5 or PCIe). 
PowerEdge XR7620 | Intel 4th/5th Gen Xeon Scalable | 1U short-depth | Edge-optimized; ruggedized, suitable for edge HPC deployments. 
PowerEdge XR8620t | Intel 4th/5th Gen Xeon Scalable | 2U short-depth | Edge-optimized; supports GPU accelerators in edge environments. 
PowerEdge XR8000r | Intel 4th/5th Gen Xeon Scalable | Modular | Modular edge platform with configurable sled options. 
 
## AMD-based servers[¶](#amd-based-servers "Permanent link")

Model | CPU Generation | Form Factor | Notes 
---|---|---|--- 
PowerEdge R6615 | AMD EPYC 4th Gen (Genoa) | 1U rack | Single-socket; cost-effective for OIM or lightweight compute. 
PowerEdge R7615 | AMD EPYC 4th Gen (Genoa) | 2U rack | Single-socket; extended storage capacity. 
PowerEdge R6625 | AMD EPYC 4th Gen (Genoa) | 1U rack | Dual-socket; high core density for parallel workloads. 
PowerEdge R7625 | AMD EPYC 4th Gen (Genoa) | 2U rack | Dual-socket; balanced compute and storage. 
PowerEdge R7725 | AMD EPYC 4th Gen (Genoa) | 2U rack | Dual-socket; GPU-ready with PCIe Gen5 expansion. 
PowerEdge C6625 | AMD EPYC 4th Gen (Genoa) | 2U multi-node | High-density; multiple independent compute sleds per chassis. 
 
## ARM-based servers (Grace CPU)[¶](#arm-based-servers-grace-cpu "Permanent link")

Model | CPU | Form Factor | Notes 
---|---|---|--- 
PowerEdge R770-G | NVIDIA Grace CPU (ARM, AArch64) | 2U rack | ARM architecture; requires `build_image_aarch64.yml` for image creation. Uses separate OS image from x86_64 nodes. 
 
Note

ARM nodes require provisioning with the `build_image_aarch64.yml` playbook. The x86_64 image built by `build_image_x86_64.yml` is **not** compatible with ARM-based servers.

## Server role compatibility[¶](#server-role-compatibility "Permanent link")

Server Model | OIM | Slurm Control | Slurm Node | Login Node | K8s Control | K8s Node 
---|---|---|---|---|---|--- 
R660 / R6615 / R6625 | Yes | Yes | Yes | Yes | Yes | Yes 
R760 / R7615 / R7625 | Yes | Yes | Yes | Yes | Yes | Yes 
R760xa / R7725 | \-- | \-- | Yes | \-- | \-- | Yes 
R770 | Yes | Yes | Yes | Yes | Yes | Yes 
C6620 / C6625 | \-- | Yes | Yes | \-- | Yes | Yes 
XE9680 | \-- | \-- | Yes | \-- | \-- | Yes 
XR7620 / XR8620t / XR8000r | \-- | Yes | Yes | \-- | Yes | Yes 
R770-G (ARM) | \-- | \-- | Yes | \-- | \-- | Yes 
 
Info

 * [Operating Systems](operating_systems.html) \-- Supported operating system versions per server.
 * [Nics](nics.html) \-- Supported network interface cards.
 * [Minimum Nodes](../ClusterRequirements/minimum_nodes.html) \-- Minimum node counts per deployment scenario.

Back to top [ Previous Reference ](../index.html) [ Next Operating Systems ](operating_systems.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
