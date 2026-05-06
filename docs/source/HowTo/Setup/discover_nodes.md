# Discover Nodes

Run the Omnia discovery playbook to PXE-boot and register bare-metal servers using the mapping file. Discovery identifies each server, assigns its network configuration, and prepares it for OS provisioning.

## Overview

The `discovery.yml` playbook automates the following process:

 1. Reads the `pxe_mapping_file.csv` to identify target servers.
 2. Configures iDRAC/BMC settings on each server using Redfish APIs.
 3. Sets PXE boot as the first boot device.
 4. Powers on each server to trigger PXE boot.
 5. The server boots from the OIM's DHCP/TFTP services and registers with OpenCHAMI's State Manager Daemon (SMD).
 6. SMD records the server's hardware inventory, MAC addresses, and assigned IP addresses.

## Prerequisites

 * BMC/iDRAC interfaces on target servers are connected to the BMC network and have IP addresses assigned (either static or via existing DHCP).
 * Admin network NICs on target servers are cabled and connected to the admin network switch.

## Procedure

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

## Verification

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

## Next Steps

## Troubleshooting

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

Copyright © 2025 Dell Technologies. All rights reserved.