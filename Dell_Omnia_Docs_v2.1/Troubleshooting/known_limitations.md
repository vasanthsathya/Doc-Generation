
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Known Limitations 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../index.html)

[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../index.html)

Overview 
 * [ Architecture ](../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](general.html)
 * Known Limitations [ Known Limitations ](known_limitations.html) Table of contents 
 * [ Supported operating systems ](#supported-operating-systems)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ Supported operating systems ](#supported-operating-systems)

 1. [ Home ](../index.html)
 2. [ Troubleshooting ](index.html)

# Known Limitations[¶](#known-limitations "Permanent link")

Current limitations and constraints of Omnia v2.1.0. Review this page before planning your deployment to ensure your environment is compatible.

## Supported operating systems[¶](#supported-operating-systems "Permanent link")

Omnia supports the following operating systems on the OIM and cluster nodes:

Component | Supported OS | Notes 
---|---|--- 
**OIM (management node)** | RHEL 8.8, 8.9, 9.2, 9.4; Rocky Linux 8.x, 9.x | RHEL requires an active subscription for package repositories. 
**Slurm cluster nodes** | RHEL 8.8, 8.9, 9.2, 9.4; Rocky Linux 8.x, 9.x | The OIM and cluster nodes do not need to run the same OS version. 
**Kubernetes cluster nodes** | RHEL 8.8, 8.9, 9.2, 9.4; Rocky Linux 8.x, 9.x | Same as Slurm cluster nodes. 
 
Note

Ubuntu, SUSE, and other Linux distributions are **not supported** in this release. Debian-based systems are on the roadmap for a future version.

## Hardware requirements[¶](#hardware-requirements "Permanent link")

Minimum hardware specifications for each component:

Component | CPU | RAM | Disk | Network 
---|---|---|---|--- 
**OIM** | 4 cores | 32 GB | 256 GB SSD | 2+ NICs 
**Slurm control node** | 4 cores | 16 GB | 100 GB | 1+ NIC 
**Slurm compute node** | 2+ cores | 8 GB | 50 GB | 1+ NIC 
**Kubernetes control plane** | 4 cores | 16 GB | 100 GB | 1+ NIC 
**Kubernetes worker** | 2+ cores | 8 GB | 50 GB | 1+ NIC 
 
Important

For clusters exceeding 100 nodes, the OIM should have 8+ cores and 64 GB RAM to handle Pulp repository synchronization and parallel Ansible execution.

## Single OIM (no management-plane HA)[¶](#single-oim-no-management-plane-ha "Permanent link")

Omnia uses a **single OIM** as the management and control point for the entire cluster. There is no built-in high-availability (HA) mechanism for the OIM itself.

**Implications:**

 * If the OIM goes down, you cannot run Omnia playbooks, provision new nodes, or manage the cluster until the OIM is restored.
 * Running Slurm and Kubernetes clusters **continue to operate** independently of the OIM. Existing workloads are not affected by an OIM outage.
 * The OIM is a single point of failure for management operations only, not for compute workloads.

**Mitigation:**

 * Deploy the OIM on hardware with redundant power supplies and RAID storage.
 * Take regular backups of the OIM configuration:

 
 
 # Back up critical Omnia configuration
 tar czf /backup/omnia_config_$(date +%Y%m%d).tar.gz /omnia/input/
 

 * Minimize OIM reboots (see [Best Practices Checklist](../Operations/best_practices_checklist.html)).
 * Document the OIM rebuild procedure for disaster recovery.

## Network topology constraints[¶](#network-topology-constraints "Permanent link")

Omnia requires specific network configurations:

 * **Minimum two networks:** An admin network (for OIM-to-node communication and provisioning) and a BMC network (for iDRAC out-of-band management).
 * **Flat Layer 2 for PXE:** PXE boot requires Layer 2 adjacency between the OIM and the target nodes on the admin network. PXE does not work across routed Layer 3 boundaries without a DHCP relay.
 * **No overlapping subnets:** The admin, BMC, compute, and public networks must use non-overlapping IP ranges.
 * **VLAN support required:** The network switches must support VLANs to segregate the different network types.

Constraint | Detail 
---|--- 
**PXE boot** | Requires Layer 2 adjacency on the admin network. Use DHCP relay if nodes are on a different subnet. 
**InfiniBand** | Requires a dedicated InfiniBand fabric. Omnia configures the IB interfaces but does not manage the fabric switches. 
**RoCE** | Requires switches that support Priority Flow Control (PFC) and ECN for lossless Ethernet. 
**Public network** | Optional. Required only if cluster nodes need direct internet access or external user access. 
 
## Known incompatibilities[¶](#known-incompatibilities "Permanent link")

Component | Limitation 
---|--- 
**Docker** | Omnia uses Podman exclusively. Docker is not supported on the OIM and may conflict with Podman if installed. 
**NetworkManager with static IPs** | On some RHEL 9.x configurations, NetworkManager may override static IP assignments configured by Omnia. Ensure `NM_CONTROLLED=no` is set on interfaces managed by Omnia. 
**SELinux (disabled)** | Omnia requires SELinux in `enforcing` or `permissive` mode. Disabling SELinux entirely (`SELINUX=disabled`) is not recommended and may cause unexpected behavior. 
**Slurm + Kubernetes on same node** | Running both `slurmd` and `kubelet` on the same physical node is **not supported**. Nodes must be assigned to either the Slurm cluster or the Kubernetes cluster, not both. 
**IPv6-only networks** | Omnia currently supports IPv4 only. IPv6-only or dual-stack configurations are not tested or supported. 
**Secure Boot** | PXE provisioning with Secure Boot enabled is not supported in this release. Disable Secure Boot in the node BIOS before provisioning. 
 
## Other limitations[¶](#other-limitations "Permanent link")

 * **Maximum tested cluster size:** Omnia has been tested with clusters of up to 500 nodes. Larger deployments may require tuning Ansible parallelism and Pulp repository performance.
 * **Single Slurm cluster per OIM:** Each OIM manages one Slurm cluster. To manage multiple Slurm clusters, deploy separate OIMs.
 * **No live migration:** Omnia does not support live migration of running workloads between nodes. Workloads must be drained before node maintenance.
 * **Telemetry retention:** Default telemetry data retention is 90 days. Adjust the VictoriaMetrics `-retentionPeriod` flag if longer retention is needed.

Info

 * [Release Notes](../Overview/release_notes.html) \-- Release notes with version-specific changes and fixes.
 * [Prerequisites Checklist](../GetStarted/prerequisites_checklist.html) \-- Full prerequisite list.
 * [Network Topologies](../Overview/network_topologies.html) \-- Supported network configurations.

Back to top [ Previous BuildStreaM ](buildstream.html) [ Next Contributing to Omnia ](../Contributing/index.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
