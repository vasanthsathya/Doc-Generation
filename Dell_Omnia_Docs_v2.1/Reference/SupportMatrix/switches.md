
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Switches 

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
 * [ Servers ](servers.html)
 * Switches [ Switches ](switches.html) Table of contents 
 * [ Switch support matrix ](#switch-support-matrix)
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

 * [ Switch support matrix ](#switch-support-matrix)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Support Matrix ](servers.html)

# Supported Switches[¶](#supported-switches "Permanent link")

Omnia v2.1 supports the following Dell PowerSwitch models for admin, BMC, and high-speed data networks.

## Switch support matrix[¶](#switch-support-matrix "Permanent link")

Model | Ports | Speed | OS | Notes 
---|---|---|---|--- 
Dell PowerSwitch S5248F-ON | 48 x 25 GbE + 4 x 100 GbE + 2 x 100 GbE | 25/100 GbE | OS10 Enterprise | Top-of-rack switch for admin and compute networks. Part of the S5200 series. 
Dell PowerSwitch Z9332F-ON | 32 x 400 GbE QSFP-DD | 100/400 GbE | OS10 Enterprise | Spine / aggregation switch for high-speed fabrics. Supports breakout to 4 x 100 GbE per port. 
Dell PowerSwitch Z9264F-ON | 64 x 100 GbE QSFP28 | 100 GbE | OS10 Enterprise | Spine / aggregation switch for 100 GbE fabrics. Supports breakout to 4 x 25 GbE per port. 
 
## Operating system requirements[¶](#operating-system-requirements "Permanent link")

Switch OS | Requirement 
---|--- 
**OS10 Enterprise Edition** | Required for automated VLAN and port configuration by Omnia. Omnia uses REST API and SSH to configure switch ports, VLANs, and LAGs. 
**SONiC** | Omnia does **not** automate SONiC switch configuration. If using SONiC, VLANs, port channels, and IP routing must be configured manually before running `discovery.yml`. 
 
Warning

Omnia's switch automation playbooks assume OS10 Enterprise Edition. Running these playbooks against SONiC-based switches will fail. Configure SONiC switches manually using the SONiC CLI or config_db.json.

## Recommended switch roles[¶](#recommended-switch-roles "Permanent link")

Network | Recommended Switch | Configuration 
---|---|--- 
Admin network | S5248F-ON (S5200 series) | 1 GbE or 25 GbE access ports; one VLAN per admin subnet. 
BMC network | S5248F-ON (S5200 series) | Dedicated VLAN for iDRAC/BMC traffic. Can share the same physical switch as admin using VLAN separation. 
Compute / data network | Z9332F-ON or Z9264F-ON | 100 GbE or 400 GbE ports for MPI, NCCL, and storage traffic. Configure jumbo frames (MTU 9216) for RDMA workloads. 
Public / external network | S5248F-ON (S5200 series) | Uplink to campus or internet gateway. 
 
## VLAN configuration summary[¶](#vlan-configuration-summary "Permanent link")

VLAN Purpose | Typical VLAN ID | Tagged / Untagged | Description 
---|---|---|--- 
Admin | 100 | Untagged | Server management and Omnia provisioning traffic. 
BMC | 200 | Tagged | iDRAC/BMC out-of-band management traffic. 
Compute | 300 | Tagged or Untagged | High-speed data plane for MPI and storage I/O. 
Public | 400 | Tagged | Internet-facing or campus-facing traffic (optional). 
 
Note

VLAN IDs shown above are examples. Use values that conform to your datacenter standards. Configure matching VLANs in `network_spec.yml` ([Network Spec](../Configuration/network_spec.html)).

## Switch firmware[¶](#switch-firmware "Permanent link")

Keep all switches on the same firmware train. Consult the [Dell Networking Support](https://www.dell.com/support/home/) page for the latest recommended OS10 version for each switch model.

Info

 * [Nics](nics.html) \-- NIC models connected to these switches.
 * [Network Topologies](network_topologies.html) \-- How switches integrate into Omnia network topologies.
 * [Network Spec](../Configuration/network_spec.html) \-- VLAN and subnet configuration.

Back to top [ Previous NICs ](nics.html) [ Next Storage ](storage.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
