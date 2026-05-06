
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Discover Nodes 

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
 * [ Prepare OIM ](prepare_oim.html)
 * Discover Nodes [ Discover Nodes ](discover_nodes.html) Table of contents 
 * [ Overview ](#overview)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../Networking/configure_infiniband.html)
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
 3. [ Setup ](prepare_oim.html)

# Discover Nodes[¶](#discover-nodes "Permanent link")

Run the Omnia discovery playbook to PXE-boot and register bare-metal servers using the mapping file. Discovery identifies each server, assigns its network configuration, and prepares it for OS provisioning.

## Overview[¶](#overview "Permanent link")

The `discovery.yml` playbook automates the following process:

 1. Reads the `pxe_mapping_file.csv` to identify target servers.
 2. Configures iDRAC/BMC settings on each server using Redfish APIs.
 3. Sets PXE boot as the first boot device.
 4. Powers on each server to trigger PXE boot.
 5. The server boots from the OIM's DHCP/TFTP services and registers with OpenCHAMI's State Manager Daemon (SMD).
 6. SMD records the server's hardware inventory, MAC addresses, and assigned IP addresses.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Prepare Oim](prepare_oim.html) procedure is complete (OpenCHAMI and DHCP are running).
 * The [Build Cluster Images](build_cluster_images.html) procedure is complete (boot images are in MinIO).
 * The [Create Mapping File](create_mapping_file.html) procedure is complete.
 * The [Configure Credentials](configure_credentials.html) procedure is complete (BMC credentials configured).
 * BMC/iDRAC interfaces on target servers are connected to the BMC network and have IP addresses assigned (either static or via existing DHCP).
 * Admin network NICs on target servers are cabled and connected to the admin network switch.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Verify the mapping file is in place** :

Run on: omnia_core container
 
 
 cat /opt/omnia/input/project_default/pxe_mapping_file.csv
 

 1. **Run the discovery playbook** :

Run on: omnia_core container
 
 
 cd /omnia/discovery
 ansible-playbook discovery.yml --ask-vault-pass
 

The playbook will:

 * Connect to each server's BMC/iDRAC using Redfish.
 * Configure network boot settings.
 * Set PXE as the first boot device.
 * Power-cycle the servers.
 * Wait for each server to PXE boot and register with SMD.

!!! note
 
 
 Discovery can take **30-60 minutes** depending on the number of nodes.
 Each server must complete a full PXE boot cycle.
 

 1. **Monitor discovery progress** by watching the Ansible output. Each node will progress through these stages:

 2. `Configuring BMC` \-- Setting iDRAC boot options

 3. `Powering on` \-- Sending power-on command via Redfish
 4. `Waiting for PXE boot` \-- Node is booting from network
 5. `Registered` \-- Node appeared in SMD inventory

## Verification[¶](#verification "Permanent link")

 1. **List discovered nodes in OpenCHAMI** :

Run on: omnia_core container
 
 
 ochami node list
 

Expected output shows all nodes from the mapping file with their service tags, MAC addresses, and assigned IPs.

 1. **Check SMD inventory** :

Run on: omnia_core container
 
 
 ochami smd status
 

 1. **Verify node count matches the mapping file** :

Run on: omnia_core container
 
 
 # Count discovered nodes
 ochami node list | wc -l
 
 # Count entries in mapping file (excluding header)
 tail -n +2 /opt/omnia/input/project_default/pxe_mapping_file.csv | wc -l
 

 1. **Ping each discovered node** on the admin network:

Run on: omnia_core container
 
 
 # Example: ping a specific node
 ping -c 3 10.5.0.101
 

 1. **Check Ansible inventory** was populated:

Run on: omnia_core container
 
 
 ansible-inventory --list | python3 -m json.tool | head -50
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Pxe Boot Nodes](pxe_boot_nodes.html) \-- Ensure all nodes complete provisioning.
 * [Verify Cluster](verify_cluster.html) \-- Verify the cluster is operational.
 * [Setup Slurm](../Slurm/setup_slurm.html) \-- Deploy Slurm on discovered nodes.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Node not discovered (missing from SMD)** \- Verify the BMC IP is reachable from the OIM:
 
 
 ```bash title="Run on: OIM host"
 ping -c 3 <bmc-ip>
 ```
 

 * Check iDRAC web UI for boot errors.
 * Verify the `ADMIN_MAC` in the mapping file matches the PXE NIC.

**BMC connection refused** \- Confirm BMC credentials are correct in the encrypted credentials file. \- Verify iDRAC is not locked out (too many failed login attempts). \- Check that Redfish is enabled in iDRAC settings.

**PXE boot timeout** \- Verify DHCP is running on the OIM:
 
 
 ```bash title="Run on: OIM host"
 systemctl status coredhcp.service
 ```
 

 * Check TFTP service:

Run on: OIM host
 
 systemctl status tftpd.service
 

 * Verify the admin network switch is configured with the correct VLAN.

**Some nodes discover but others do not** \- Check for MAC address typos in the mapping file. \- Verify the physical cabling on failed nodes. \- Check for IP conflicts on the admin network:
 
 
 ```bash title="Run on: OIM host"
 arping -D -I <admin-nic> <admin-ip>
 ```
 

**Discovery playbook fails at BMC configuration step** \- Ensure iDRAC firmware is up to date (minimum 5.x for PowerEdge 15th gen). \- Verify Redfish API is accessible:
 
 
 ```bash title="Run on: OIM host"
 curl -sk https://<bmc-ip>/redfish/v1/ -u <user>:<pass>
 ```
 

Back to top [ Previous Deploy Omnia Core ](deploy_omnia_core.html) [ Next Create Mapping File ](create_mapping_file.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
