
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Configure InfiniBand 

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
 * [ Prepare OIM ](../Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../Storage/configure_nfs.html)
 * Networking Networking 
 * Configure InfiniBand [ Configure InfiniBand ](configure_infiniband.html) Table of contents 
 * [ Overview ](#overview)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Overview ](#overview)

 1. [ Home ](../../index.html)
 2. [ How-to Guides ](../index.html)
 3. [ Networking ](configure_infiniband.html)

# Configure InfiniBand[¶](#configure-infiniband "Permanent link")

Set up InfiniBand (IB) high-speed interconnect on compute nodes with DOCA-OFED drivers, OpenSM subnet manager, and static IB IP assignment for low-latency MPI communication.

## Overview[¶](#overview "Permanent link")

InfiniBand provides the lowest latency and highest bandwidth interconnect for HPC workloads. Omnia automates the deployment of:

 * **DOCA-OFED driver** \-- NVIDIA's unified driver package for ConnectX InfiniBand HCAs.
 * **OpenSM** \-- Subnet manager that initializes the IB fabric and manages routing.
 * **Static IB IPs** \-- Assign persistent IPoIB (IP-over-InfiniBand) addresses for application-level communication.

## Prerequisites[¶](#prerequisites "Permanent link")

 * Compute nodes have NVIDIA ConnectX InfiniBand HCAs installed.
 * An InfiniBand switch connects all compute nodes.
 * Physical cabling (QSFP/QSFP56/OSFP) is in place between nodes and the IB switch.
 * `software_config.json` includes the IB/OFED software package.
 * Local repositories are synced with OFED packages (see [Create Local Repos](../Setup/create_local_repos.html)).

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure InfiniBand settings** in the network specification:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/network_spec.yml
 

Add the IB network configuration:

File: /opt/omnia/input/project_default/network_spec.yml
 
 
 ---
 ib_network:
 ib_nic_name: "ib0"
 static_range: "10.230.0.101-10.230.0.200"
 subnet: "10.230.0.0"
 netmask: "255.255.255.0"
 

 1. **Ensure OFED is listed in software_config.json** :

Run on: omnia_core container
 
 
 cat /opt/omnia/input/project_default/software_config.json | python3 -m json.tool
 

Verify the `softwares` list includes:

File: /opt/omnia/input/project_default/software_config.json
 
 
 {
 "softwares": [
 {"name": "doca_ofed"}
 ]
 }
 

 1. **Run the omnia.yml playbook** to deploy InfiniBand:

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook omnia.yml --ask-vault-pass
 

The playbook will:

 * Install DOCA-OFED packages on all compute nodes.
 * Load the `mlx5_core` and `mlx5_ib` kernel modules.
 * Configure IPoIB interfaces with static IP addresses.
 * Deploy and start OpenSM on a designated subnet manager node.

 * **(If needed) Manually configure IPoIB on a node** :

Run on: compute node
 
 
 # Load InfiniBand modules
 modprobe mlx5_core
 modprobe mlx5_ib
 modprobe ib_ipoib
 
 # Configure the IPoIB interface
 cat <<'EOF' > /etc/sysconfig/network-scripts/ifcfg-ib0
 DEVICE=ib0
 TYPE=InfiniBand
 BOOTPROTO=static
 IPADDR=10.230.0.101
 NETMASK=255.255.255.0
 ONBOOT=yes
 CONNECTED_MODE=yes
 EOF
 
 ifup ib0
 

 1. **Configure OpenSM** on the designated subnet manager node:

Run on: OpenSM node (typically the Slurm control node)
 
 
 dnf install -y opensm
 systemctl enable --now opensm
 

!!! note
 
 
 Only one node in the IB fabric should run OpenSM as the primary subnet
 manager. A second node can run OpenSM as a standby for HA.
 

## Verification[¶](#verification "Permanent link")

 1. **Verify the IB interface is up** on each compute node:

Run on: compute node
 
 
 ip addr show ib0
 

Expected: the interface shows the assigned IP address and `state UP`.

 1. **Check IB port state** :

Run on: compute node
 
 
 ibstat
 

Expected output:

Expected output on: compute node
 
 
 CA 'mlx5_0'
 Port 1:
 State: Active
 Physical state: LinkUp
 Rate: 200 (HDR)
 

 1. **Verify OpenSM is running** :

Run on: OpenSM node
 
 
 systemctl status opensm
 

 1. **Test IB connectivity** between two compute nodes:

Run on: compute node 1
 
 
 ping -c 5 10.230.0.102
 

 1. **Test RDMA bandwidth** :

On the server node:

Run on: compute node 1
 
 
 ib_write_bw
 

On the client node:

Run on: compute node 2
 
 
 ib_write_bw 10.230.0.101
 

 1. **Test RDMA latency** :

On the server node:

Run on: compute node 1
 
 
 ib_write_lat
 

On the client node:

Run on: compute node 2
 
 
 ib_write_lat 10.230.0.101
 

Expected InfiniBand latency: < 2 microseconds.

## Next Steps[¶](#next-steps "Permanent link")

 * [Run Hpc Benchmarks](../Slurm/run_hpc_benchmarks.html) \-- Run MPI benchmarks over the IB fabric.
 * [Configure Roce](configure_roce.html) \-- Configure RoCE as an alternative to InfiniBand.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**ib0 interface does not appear** Verify InfiniBand modules are loaded:

Run on: compute node
 
 
 lsmod | grep mlx5
 lsmod | grep ib_ipoib
 

Load missing modules:

Run on: compute node
 
 
 modprobe mlx5_core
 modprobe mlx5_ib
 modprobe ib_ipoib
 

**ibstat shows "Down" or "Initializing"** \- Check physical cable connections. \- Verify OpenSM is running somewhere in the fabric. \- Check for firmware issues:
 
 
 ```bash title="Run on: compute node"
 ibv_devinfo
 ```
 

**OpenSM fails to start** Check for port GUID conflicts:

Run on: OpenSM node
 
 
 journalctl -u opensm --no-pager -n 30
 

**Poor RDMA performance** \- Verify link rate (should be 100/200 Gbps for HDR):
 
 
 ```bash title="Run on: compute node"
 ibstat | grep Rate
 ```
 

 * Check for errors on the IB port:

Run on: compute node
 
 perfquery
 

 * Ensure `CONNECTED_MODE=yes` in the IPoIB interface configuration.

**IP address conflicts on IB network** Check for duplicate IPs:

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "ip addr show ib0 | grep inet"
 

Back to top [ Previous Configure PowerVault ](../Storage/configure_powervault.html) [ Next Configure RoCE ](configure_roce.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
