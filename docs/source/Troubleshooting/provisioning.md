# Provisioning Issues

Issues related to PXE booting, node discovery, cloud-init configuration, and the `discovery.yml` playbook.

## PXE boot failures

### NIC not set to PXE boot

The target node does not attempt a network boot. It boots directly to the local disk or enters the BIOS setup instead of requesting a PXE image from the OIM.

The node's BIOS/UEFI boot order does not include PXE/network boot, or PXE is disabled on the NIC connected to the admin network.

 1. Enter the node's BIOS/UEFI setup (press F2 during POST on Dell PowerEdge servers).
 2. Navigate to **System BIOS > Network Settings**.
 3. Enable **PXE Boot** on the NIC connected to the admin network.
 4. Navigate to **Boot Settings > BIOS Boot Settings** (or **UEFI Boot Settings**).
 5. Set **Network Boot** (PXE) as the first boot option.
 6. Save and exit BIOS. The node should now attempt PXE boot on the next restart.

Alternatively, use `racadm` to configure remotely:

 racadm set NIC.NICConfig.1.LegacyBootProto PXE
 racadm set BIOS.BiosBootSettings.BootSeq NIC.Slot.1-1

### Wrong MAC address in mapping file

The node PXE boots but does not receive an IP address, or it receives an IP but is not recognized by OpenCHAMI.

The MAC address in `/omnia/input/mapping_file.csv` does not match the actual MAC address of the NIC being used for PXE boot.

 1. Verify the correct MAC address from iDRAC or the node's BIOS:

 # From iDRAC (using racadm)
 racadm getsysinfo | grep "MAC Address"

 1. Update the mapping file with the correct MAC:

 # /omnia/input/mapping_file.csv
 AA:BB:CC:DD:EE:FF,compute-01,10.5.0.101

 1. Re-run the discovery playbook:

 ssh omnia_core
 cd /omnia
 ansible-playbook playbooks/discovery.yml

### DHCP not serving IP addresses

Nodes attempt PXE boot but fail with a DHCP timeout error:

 PXE-E51: No DHCP or proxyDHCP offers were received

 * The CoreDHCP container on the OIM is not running.
 * The DHCP range is exhausted.
 * A network misconfiguration prevents DHCP broadcasts from reaching the OIM.
 * Another DHCP server on the same network is interfering.

 1. Verify the CoreDHCP container is running:

 podman ps | grep coredhcp

If it is not running, start it:

 podman start coredhcp

 1. Check CoreDHCP logs for errors:

 podman logs coredhcp

 1. Verify no rogue DHCP server exists on the admin network:

 nmap --script broadcast-dhcp-discover -e <admin_nic>

 1. Ensure the OIM's admin NIC is on the correct VLAN and subnet.

### TFTP timeout during PXE boot

The node receives a DHCP lease but fails to download the boot image:

 PXE-E32: TFTP open timeout
 PXE-T02: TFTP packet timeout

 * The TFTP service on the OIM is not running.
 * Firewall rules on the OIM are blocking TFTP traffic (UDP port 69).
 * The TFTP root directory does not contain the expected boot files.

 1. Verify the TFTP container is running:

 podman ps | grep tftp

 1. Check firewall rules:

 firewall-cmd --list-all | grep tftp

If TFTP is not allowed:

 firewall-cmd --permanent --add-service=tftp
 firewall-cmd --reload

 1. Verify boot files exist in the TFTP root:

 ls /var/lib/tftpboot/

## cloud-init issues

Nodes boot the OS successfully but post-boot configuration fails. The node is accessible via console but network settings, hostname, or SSH keys are not configured correctly.

 * The cloud-init data source is not configured.
 * The cloud-init configuration file has syntax errors.
 * The cloud-init service was disabled or removed from the OS image.

 1. Check cloud-init status on the affected node:

 cloud-init status --long

 1. Review cloud-init logs:

 cat /var/log/cloud-init.log
 cat /var/log/cloud-init-output.log

 1. Verify the data source configuration:

 cat /etc/cloud/cloud.cfg.d/

 1. If cloud-init was disabled, re-enable it:

 systemctl enable cloud-init
 cloud-init clean
 reboot

## `discovery.yml` failures

The `discovery.yml` playbook fails with errors related to OpenCHAMI, BMC connectivity, or inventory population.

 * OpenCHAMI services (SMD, BSS) are not running on the OIM.
 * BMC/iDRAC credentials are incorrect.
 * The BMC network is unreachable from the OIM.

 1. Verify OpenCHAMI services are running:

 podman ps | grep ochami

 1. Test BMC connectivity:

 # Ping the BMC IP
 ping <bmc_ip>

 # Test Redfish API access
 curl -k -u <user>:<pass> https://<bmc_ip>/redfish/v1/Systems

 1. Verify BMC credentials in the configuration:

 ssh omnia_core
 ansible-vault view /omnia/input/credentials.yml

 1. Check discovery logs for detailed errors:

 cat /opt/omnia/log/core/playbooks/discovery.log

## Nodes not appearing after discovery

After running `discovery.yml` successfully, the expected nodes do not appear in `ochami-cli smd components list` or `sinfo`.

 * The node's BMC did not respond during the discovery window.
 * The node's MAC address does not match any entry in the mapping file.
 * The node booted but failed cloud-init, so it did not register with the OIM.

 1. Check the OpenCHAMI inventory:

 ssh omnia_core
 ochami-cli smd components list

 1. Verify the node's BMC is responsive:

 ping <bmc_ip>
 curl -k -u <user>:<pass> https://<bmc_ip>/redfish/v1/Systems

 1. Re-run discovery for the specific node by power-cycling it via iDRAC:

 racadm -r <bmc_ip> -u <user> -p <pass> serveraction powercycle

 1. Monitor the discovery log in real time:

 tail -f /opt/omnia/log/core/playbooks/discovery.log

Copyright © 2025 Dell Technologies. All rights reserved.