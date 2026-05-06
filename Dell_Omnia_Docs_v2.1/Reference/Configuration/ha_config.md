
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

HA Config 

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
 * HA Config [ HA Config ](ha_config.html) Table of contents 
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

# high_availability_config.yml Reference[¶](#high_availability_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/high_availability_config.yml` (also referred to as `ha_config.yml`)

This file configures Kubernetes control plane high availability (HA) using a virtual IP address and load-balanced API servers.

## Parameter reference[¶](#parameter-reference "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`ha_enabled` | Boolean | No | `false` | Enable Kubernetes control plane high availability. When `true`, multiple `kube_control_plane` nodes share a virtual IP. 
`ha_virtual_ip` | String (IP) | Conditional | (none) | Virtual IP address for the Kubernetes API server. Clients and worker nodes connect to this IP instead of a single control plane node. Required when `ha_enabled` is `true`. Must be on the same subnet as the control plane nodes' admin network. 
`ha_load_balancer` | String | No | `kube-vip` | Load balancer technology for the control plane virtual IP. Accepted values: `kube-vip`. Additional options may be supported in future releases. 
`ha_control_plane_port` | Integer | No | `6443` | Port on which the Kubernetes API server listens. The virtual IP forwards traffic to this port on all control plane nodes. 
`ha_etcd_external` | Boolean | No | `false` | Use an external etcd cluster instead of the embedded etcd that runs on each control plane node. When `true`, provide etcd endpoints via `ha_etcd_endpoints`. 
`ha_etcd_endpoints` | List | Conditional | `[]` | List of external etcd endpoints (e.g., `["https://10.5.0.10:2379", "https://10.5.0.11:2379"]`). Required when `ha_etcd_external` is `true`. 
 
## HA architecture overview[¶](#ha-architecture-overview "Permanent link")

Component | Description 
---|--- 
**kube-vip** | Runs as a static pod on each control plane node. One node is elected leader and holds the virtual IP. If the leader fails, another control plane node takes over within seconds. 
**Virtual IP** | A floating IP that is always routable to the current leader. All `kubelet` and `kubectl` connections target this IP. 
**etcd** | By default, each control plane node runs its own etcd instance (stacked topology). Alternatively, an external etcd cluster can be specified. 
 
## Prerequisites[¶](#prerequisites "Permanent link")

 * Minimum **3 control plane nodes** for a quorum-based HA deployment.
 * The `ha_virtual_ip` must be a free IP on the admin network subnet -- it must not be assigned to any physical server or DHCP range.
 * All control plane nodes must have L2 connectivity on the admin network for ARP-based virtual IP failover.

## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/high_availability_config.yml
 
 
 ha_enabled: true
 ha_virtual_ip: "10.5.0.250"
 ha_load_balancer: "kube-vip"
 ha_control_plane_port: 6443
 ha_etcd_external: false
 

Info

 * [Omnia Config](omnia_config.html) \-- Kubernetes deployment settings.
 * [Minimum Nodes](../ClusterRequirements/minimum_nodes.html) \-- Minimum node counts for HA deployments.
 * [Ports](../ClusterRequirements/ports.html) \-- Kubernetes ports including the API server.

Back to top [ Previous Security Config ](security_config.html) [ Next Local Repo Config ](local_repo_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
