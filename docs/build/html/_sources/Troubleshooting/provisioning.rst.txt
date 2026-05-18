

Provisioning Issues
===================


Issues related to PXE booting, node discovery, cloud-init configuration, and
the ``discovery.yml`` playbook.


PXE boot failures
-----------------



NIC not set to PXE boot
~~~~~~~~~~~~~~~~~~~~~~~


???+ note "Symptom"

    The target node does not attempt a network boot. It boots directly to the
    local disk or enters the BIOS setup instead of requesting a PXE image from
    the OIM.

??? note "Cause"

    The node's BIOS/UEFI boot order does not include PXE/network boot, or PXE
    is disabled on the NIC connected to the admin network.

??? note "Resolution"

    #. Enter the node's BIOS/UEFI setup (press F2 during POST on Dell PowerEdge
       servers).
    #. Navigate to **System BIOS > Network Settings**.
    #. Enable **PXE Boot** on the NIC connected to the admin network.
    #. Navigate to **Boot Settings > BIOS Boot Settings** (or **UEFI Boot
       Settings**).
    #. Set **Network Boot** (PXE) as the first boot option.
    #. Save and exit BIOS. The node should now attempt PXE boot on the next
       restart.

    Alternatively, use ``racadm`` to configure remotely:


.. code-block:: bash

       racadm set NIC.NICConfig.1.LegacyBootProto PXE
       racadm set BIOS.BiosBootSettings.BootSeq NIC.Slot.1-1




Wrong MAC address in mapping file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


???+ note "Symptom"

    The node PXE boots but does not receive an IP address, or it receives an IP
    but is not recognized by OpenCHAMI.

??? note "Cause"

    The MAC address in ``/omnia/input/mapping_file.csv`` does not match the
    actual MAC address of the NIC being used for PXE boot.

??? note "Resolution"

    #. Verify the correct MAC address from iDRAC or the node's BIOS:


.. code-block:: bash

          # From iDRAC (using racadm)
          racadm getsysinfo | grep "MAC Address"



    #. Update the mapping file with the correct MAC:


.. code-block:: text

          # /omnia/input/mapping_file.csv
          AA:BB:CC:DD:EE:FF,compute-01,10.5.0.101



    #. Re-run the discovery playbook:


.. code-block:: bash

          ssh omnia_core
          cd /omnia
          ansible-playbook playbooks/discovery.yml




DHCP not serving IP addresses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


???+ note "Symptom"

    Nodes attempt PXE boot but fail with a DHCP timeout error:


.. code-block:: text

       PXE-E51: No DHCP or proxyDHCP offers were received



??? note "Cause"

    - The CoreDHCP container on the OIM is not running.
    - The DHCP range is exhausted.
    - A network misconfiguration prevents DHCP broadcasts from reaching the OIM.
    - Another DHCP server on the same network is interfering.

??? note "Resolution"

    #. Verify the CoreDHCP container is running:


.. code-block:: bash

          podman ps | grep coredhcp



       If it is not running, start it:


.. code-block:: bash

          podman start coredhcp



    #. Check CoreDHCP logs for errors:


.. code-block:: bash

          podman logs coredhcp



    #. Verify no rogue DHCP server exists on the admin network:


.. code-block:: bash

          nmap --script broadcast-dhcp-discover -e <admin_nic>



    #. Ensure the OIM's admin NIC is on the correct VLAN and subnet.


TFTP timeout during PXE boot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


???+ note "Symptom"

    The node receives a DHCP lease but fails to download the boot image:


.. code-block:: text

       PXE-E32: TFTP open timeout
       PXE-T02: TFTP packet timeout



??? note "Cause"

    - The TFTP service on the OIM is not running.
    - Firewall rules on the OIM are blocking TFTP traffic (UDP port 69).
    - The TFTP root directory does not contain the expected boot files.

??? note "Resolution"

    #. Verify the TFTP container is running:


.. code-block:: bash

          podman ps | grep tftp



    #. Check firewall rules:


.. code-block:: bash

          firewall-cmd --list-all | grep tftp



       If TFTP is not allowed:


.. code-block:: bash

          firewall-cmd --permanent --add-service=tftp
          firewall-cmd --reload



    #. Verify boot files exist in the TFTP root:


.. code-block:: bash

          ls /var/lib/tftpboot/




cloud-init issues
-----------------


???+ note "Symptom"

    Nodes boot the OS successfully but post-boot configuration fails. The node
    is accessible via console but network settings, hostname, or SSH keys are
    not configured correctly.

??? note "Cause"

    - The cloud-init data source is not configured.
    - The cloud-init configuration file has syntax errors.
    - The cloud-init service was disabled or removed from the OS image.

??? note "Resolution"

    #. Check cloud-init status on the affected node:


.. code-block:: bash

          cloud-init status --long



    #. Review cloud-init logs:


.. code-block:: bash

          cat /var/log/cloud-init.log
          cat /var/log/cloud-init-output.log



    #. Verify the data source configuration:


.. code-block:: bash

          cat /etc/cloud/cloud.cfg.d/



    #. If cloud-init was disabled, re-enable it:


.. code-block:: bash

          systemctl enable cloud-init
          cloud-init clean
          reboot




`discovery.yml` failures
------------------------


???+ note "Symptom"

    The ``discovery.yml`` playbook fails with errors related to OpenCHAMI, BMC
    connectivity, or inventory population.

??? note "Cause"

    - OpenCHAMI services (SMD, BSS) are not running on the OIM.
    - BMC/iDRAC credentials are incorrect.
    - The BMC network is unreachable from the OIM.

??? note "Resolution"

    #. Verify OpenCHAMI services are running:


.. code-block:: bash

          podman ps | grep ochami



    #. Test BMC connectivity:


.. code-block:: bash

          # Ping the BMC IP
          ping <bmc_ip>
   
          # Test Redfish API access
          curl -k -u <user>:<pass> https://<bmc_ip>/redfish/v1/Systems



    #. Verify BMC credentials in the configuration:


.. code-block:: bash

          ssh omnia_core
          ansible-vault view /omnia/input/credentials.yml



    #. Check discovery logs for detailed errors:


.. code-block:: bash

          cat /opt/omnia/log/core/playbooks/discovery.log




Nodes not appearing after discovery
-----------------------------------


???+ note "Symptom"

    After running ``discovery.yml`` successfully, the expected nodes do not
    appear in ``ochami-cli smd components list`` or ``sinfo``.

??? note "Cause"

    - The node's BMC did not respond during the discovery window.
    - The node's MAC address does not match any entry in the mapping file.
    - The node booted but failed cloud-init, so it did not register with the
      OIM.

??? note "Resolution"

    #. Check the OpenCHAMI inventory:


.. code-block:: bash

          ssh omnia_core
          ochami-cli smd components list



    #. Verify the node's BMC is responsive:


.. code-block:: bash

          ping <bmc_ip>
          curl -k -u <user>:<pass> https://<bmc_ip>/redfish/v1/Systems



    #. Re-run discovery for the specific node by power-cycling it via iDRAC:


.. code-block:: bash

          racadm -r <bmc_ip> -u <user> -p <pass> serveraction powercycle



    #. Monitor the discovery log in real time:


.. code-block:: bash

          tail -f /opt/omnia/log/core/playbooks/discovery.log




.. note::


   - :doc:`Discover Nodes <../HowTo/Setup/discover_nodes>` -- Full node discovery procedure.
   - :doc:`Pxe Boot Nodes <../HowTo/Setup/pxe_boot_nodes>` -- PXE boot configuration guide.
   - :doc:`Log Management <../Operations/log_management>` -- Log locations for deeper diagnosis.

