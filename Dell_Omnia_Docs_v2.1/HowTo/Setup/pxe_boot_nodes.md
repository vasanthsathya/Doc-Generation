
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

PXE Boot Nodes 

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
 * PXE Boot Nodes [ PXE Boot Nodes ](pxe_boot_nodes.html) Table of contents 
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

# PXE Boot Nodes[¶](#pxe-boot-nodes "Permanent link")

Configure target servers for PXE boot and verify they are provisioned with the correct operating system image from the OIM.

## Overview[¶](#overview "Permanent link")

After discovery, target servers must PXE boot from the OIM to receive their operating system image. This guide covers:

 1. Setting the PXE boot order on target servers (via iDRAC or BIOS).
 2. Verifying nodes boot from the network and receive the correct image.
 3. Confirming nodes are provisioned and reachable on the admin network.

Note

If you ran the `discovery.yml` playbook, PXE boot order is typically configured automatically via Redfish. This guide helps you verify or manually configure boot settings for servers that did not auto-configure.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Discover Nodes](discover_nodes.html) procedure is complete.
 * The [Build Cluster Images](build_cluster_images.html) procedure is complete (boot images in MinIO).
 * The OIM's DHCP, TFTP, and HTTP services are running (verified via [Verify Oim Services](verify_oim_services.html)).
 * Physical network cables connect each server's PXE NIC to the admin network switch.

## Procedure[¶](#procedure "Permanent link")

 1. **Verify OIM boot services are running** :

Run on: OIM host
 
 
 systemctl is-active coredhcp.service
 systemctl is-active tftpd.service
 systemctl is-active image-server.service
 systemctl is-active bss.service
 

All services should report `active`.

 1. **(If needed) Manually set PXE boot order via iDRAC** :

a. Open a web browser and navigate to `https://<bmc-ip>`. b. Log in with iDRAC credentials. c. Go to **Configuration** > **BIOS Settings** > **Boot Settings**. d. Set **Boot Mode** to `UEFI`. e. Under **UEFI Boot Sequence** , move **Integrated NIC** (PXE) to the **first** position. f. Click **Apply** and reboot the server.

Alternatively, configure via Redfish from the OIM:

Run on: OIM host
 
 
 curl -sk -X PATCH \
 https://<bmc-ip>/redfish/v1/Systems/System.Embedded.1 \
 -u root:<bmc-password> \
 -H "Content-Type: application/json" \
 -d '{"Boot": {"BootSourceOverrideTarget": "Pxe", "BootSourceOverrideEnabled": "Continuous"}}'
 

 1. **Power-cycle the target servers** to initiate PXE boot:

Run on: OIM host
 
 
 # Using Redfish to power-cycle a single server
 curl -sk -X POST \
 https://<bmc-ip>/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset \
 -u root:<bmc-password> \
 -H "Content-Type: application/json" \
 -d '{"ResetType": "ForceRestart"}'
 

Or power-cycle all nodes from the omnia_core container:

Run on: omnia_core container
 
 
 # Power-cycle all discovered nodes
 ochami node power --action restart --all
 

 1. **Monitor the PXE boot process** :

 2. Watch the iDRAC virtual console for each server.

 3. The server should display `iPXE` boot messages followed by the OS installer.
 4. After installation, the server reboots into the provisioned OS.

 5. **Wait for provisioning to complete**. Provisioning typically takes **10-20 minutes** per node. Nodes will:

 6. PXE boot and download the boot image from the OIM.

 7. Install the operating system to local disk.
 8. Configure networking based on the mapping file.
 9. Reboot into the installed OS.

## Verification[¶](#verification "Permanent link")

 1. **Ping each provisioned node** from the OIM:

Run on: omnia_core container
 
 
 # Ping all nodes listed in the mapping file
 for ip in $(awk -F',' 'NR>1 {print $7}' /opt/omnia/input/project_default/pxe_mapping_file.csv); do
 echo -n "$ip: "
 ping -c 1 -W 2 $ip > /dev/null 2>&1 && echo "OK" || echo "UNREACHABLE"
 done
 

 1. **SSH into a provisioned node** to verify the OS is installed:

Run on: omnia_core container
 
 
 ssh root@10.5.0.101
 

Run on: provisioned node
 
 
 cat /etc/os-release
 hostname
 ip addr show
 

 1. **Verify node registration in OpenCHAMI** :

Run on: omnia_core container
 
 
 ochami node list
 

All nodes should show a `provisioned` or `ready` state.

## Next Steps[¶](#next-steps "Permanent link")

 * [Verify Cluster](verify_cluster.html) \-- Comprehensive cluster health check.
 * [Setup Slurm](../Slurm/setup_slurm.html) \-- Deploy Slurm on provisioned nodes.
 * [Setup Service K8S](../Kubernetes/setup_service_k8s.html) \-- Deploy Kubernetes on provisioned nodes.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Node does not PXE boot** \- Verify the NIC is configured for PXE boot in BIOS/UEFI settings. \- Check the physical network cable connection. \- Verify the server's boot mode matches the OIM's configuration (UEFI vs. Legacy).

**Node gets a DHCP address but fails to download the image** \- Check the TFTP service:
 
 
 ```bash title="Run on: OIM host"
 podman logs tftpd
 ```
 

 * Verify the image server is running:

Run on: OIM host
 
 podman logs image-server
 

**Node boots but gets the wrong OS** \- Verify the BSS configuration matches the expected image:
 
 
 ```bash title="Run on: omnia_core container"
 ochami bss list
 ```
 

 * Rebuild the image if necessary (see [Build Cluster Images](build_cluster_images.html)).

**Node provisions but is unreachable on the admin network** \- Check that the admin IP was correctly assigned by reviewing `/etc/sysconfig/network-scripts/` on the node (access via iDRAC virtual console). \- Verify the admin network switch port is in the correct VLAN.

**Provisioning takes too long ( > 30 minutes per node)** \- Check OIM network bandwidth to the admin switch. \- Verify MinIO/image-server performance:
 
 
 ```bash title="Run on: OIM host"
 podman stats --no-stream minio image-server
 ```
 

Back to top [ Previous Create Mapping File ](create_mapping_file.html) [ Next Build Cluster Images ](build_cluster_images.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
