
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Network Spec 

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
 * Network Spec [ Network Spec ](network_spec.html) Table of contents 
 * [ Top-level structure ](#top-level-structure)
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

 * [ Top-level structure ](#top-level-structure)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Configuration ](omnia_config.html)

# network_spec.yml Reference[¶](#network_specyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/network_spec.yml`

This file defines all network segments used by the Omnia cluster: admin, BMC, compute, and public networks. Each network is described as an entry in the `Networks` list.

## Top-level structure[¶](#top-level-structure "Permanent link")

`network_spec.yml` contains a single top-level key, `Networks`, which is a YAML list of network definitions.

File: /opt/omnia/input/project_default/network_spec.yml
 
 
 Networks:
 - admin_network:
 ...
 - bmc_network:
 ...
 - compute_network:
 ...
 - public_network:
 ...
 

## admin_network parameters[¶](#admin_network-parameters "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`oim_nic_name` | String | Yes | (none) | Name of the network interface on the OIM connected to the admin network (e.g., `eno1`, `eth0`). 
`netmask_bits` | Integer | Yes | (none) | CIDR prefix length for the admin subnet (e.g., `20` for a `/20` subnet with 4094 usable addresses). 
`primary_oim_admin_ip` | String (IP) | Yes | (none) | Static IP address of the OIM on the admin network (e.g., `10.5.0.100`). Must be within the admin subnet. 
`primary_oim_bmc_ip` | String (IP) | No | (none) | IP address of the OIM's BMC/iDRAC interface. Used when the OIM itself has a BMC that should be managed. 
`dynamic_range` | String | Yes | (none) | DHCP range for dynamic IP assignment during node discovery. Format: `start_ip-end_ip` (e.g., `10.5.0.101-10.5.0.200`). 
`dns` | String (IP) | No | `primary_oim_admin_ip` | DNS server IP address assigned to provisioned nodes. Defaults to the OIM's admin IP if not specified. 
`mtu` | Integer | No | `1500` | Maximum Transmission Unit for the admin network. Standard Ethernet is 1500; set to 9216 for jumbo frames. 
`vlan_id` | Integer | No | (none) | 802.1Q VLAN ID for the admin network. Required for LOM and Hybrid topologies; omit for untagged Dedicated topology. 
 
## bmc_network parameters[¶](#bmc_network-parameters "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`oim_nic_name` | String | Yes | (none) | NIC on the OIM connected to the BMC network. May be the same as admin NIC in LOM/Hybrid topologies. 
`netmask_bits` | Integer | Yes | (none) | CIDR prefix length for the BMC subnet (e.g., `24`). 
`static_range` | String | No | (none) | Static IP range for BMC interfaces (e.g., `10.3.0.100-10.3.0.200`). 
`dynamic_range` | String | Yes | (none) | DHCP range for BMC discovery (e.g., `10.3.0.201-10.3.0.254`). 
`vlan_id` | Integer | No | (none) | 802.1Q VLAN ID for the BMC network. 
`reassignment_range` | String | No | (none) | IP range used when reassigning BMC addresses after discovery. 
 
## compute_network parameters (optional)[¶](#compute_network-parameters-optional "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`oim_nic_name` | String | No | (none) | NIC on the OIM connected to the compute network. Optional if the OIM does not participate in compute traffic. 
`netmask_bits` | Integer | No | (none) | CIDR prefix length for the compute subnet. 
`vlan_id` | Integer | No | (none) | VLAN ID for the compute network. 
`mtu` | Integer | No | `1500` | MTU for compute network. Set to `9216` for RDMA/RoCEv2 workloads. 
 
## public_network parameters (optional)[¶](#public_network-parameters-optional "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`oim_nic_name` | String | No | (none) | NIC on the OIM connected to the public/external network. 
`netmask_bits` | Integer | No | (none) | CIDR prefix length for the public subnet. 
`gateway` | String (IP) | No | (none) | Default gateway IP for internet/campus access. 
`dns` | String (IP) | No | (none) | External DNS server for public name resolution. 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/network_spec.yml
 
 
 Networks:
 - admin_network:
 oim_nic_name: "eno1"
 netmask_bits: 20
 primary_oim_admin_ip: "10.5.0.100"
 primary_oim_bmc_ip: "10.3.0.5"
 dynamic_range: "10.5.0.101-10.5.0.200"
 dns: "10.5.0.100"
 
 - bmc_network:
 oim_nic_name: "eno2"
 netmask_bits: 24
 dynamic_range: "10.3.0.201-10.3.0.254"
 static_range: "10.3.0.100-10.3.0.200"
 
 - compute_network:
 oim_nic_name: "enp175s0f0"
 netmask_bits: 24
 mtu: 9216
 
 - public_network:
 oim_nic_name: "enp175s0f1"
 netmask_bits: 24
 gateway: "192.168.1.1"
 dns: "8.8.8.8"
 

Note

 * In LOM topology, `admin_network` and `bmc_network` may share the same `oim_nic_name` with different `vlan_id` values.
 * The `dynamic_range` must not overlap with any static IPs assigned in the PXE mapping file.

Info

 * [Provision Config](provision_config.html) \-- Provisioning parameters that work alongside network configuration.
 * [Network Topologies](../SupportMatrix/network_topologies.html) \-- How topologies affect NIC and VLAN assignments.
 * [Nics](../SupportMatrix/nics.html) \-- Supported NIC models.

Back to top [ Previous Provision Config ](provision_config.html) [ Next Software Config ](software_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
