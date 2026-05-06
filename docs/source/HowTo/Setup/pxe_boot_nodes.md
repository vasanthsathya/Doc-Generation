# PXE Boot Nodes

Configure target servers for PXE boot and verify they are provisioned with the correct operating system image from the OIM.

## Overview

After discovery, target servers must PXE boot from the OIM to receive their operating system image. This guide covers:

 1. Setting the PXE boot order on target servers (via iDRAC or BIOS).
 2. Verifying nodes boot from the network and receive the correct image.
 3. Confirming nodes are provisioned and reachable on the admin network.

If you ran the `discovery.yml` playbook, PXE boot order is typically configured automatically via Redfish. This guide helps you verify or manually configure boot settings for servers that did not auto-configure.

## Prerequisites

 * Physical network cables connect each server's PXE NIC to the admin network switch.

## Procedure

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

## Verification

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

## Next Steps

## Troubleshooting

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

**Node provisions but is unreachable on the admin network** \- Check that the admin IP was correctly assigned by reviewing `/etc/sysconfig/network-scripts/` on the node (access via iDRAC virtual console). \- Verify the admin network switch port is in the correct VLAN.

**Provisioning takes too long ( > 30 minutes per node)** \- Check OIM network bandwidth to the admin switch. \- Verify MinIO/image-server performance:

 ```bash title="Run on: OIM host"
 podman stats --no-stream minio image-server
 ```

Copyright © 2025 Dell Technologies. All rights reserved.