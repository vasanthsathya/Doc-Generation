

Discover Nodes
==============


Run the Omnia discovery playbook to PXE-boot and register bare-metal servers
using the mapping file. Discovery identifies each server, assigns its network
configuration, and prepares it for OS provisioning.


Overview
--------


The ``discovery.yml`` playbook automates the following process:

#. Reads the ``pxe_mapping_file.csv`` to identify target servers.
#. Configures iDRAC/BMC settings on each server using Redfish APIs.
#. Sets PXE boot as the first boot device.
#. Powers on each server to trigger PXE boot.
#. The server boots from the OIM's DHCP/TFTP services and registers with
   OpenCHAMI's State Manager Daemon (SMD).
#. SMD records the server's hardware inventory, MAC addresses, and assigned
   IP addresses.



Prerequisites
-------------


- The `Prepare Oim <prepare_oim.rst>`_ procedure is complete (OpenCHAMI and DHCP are
  running).
- The `Build Cluster Images <build_cluster_images.rst>`_ procedure is complete (boot images are in
  MinIO).
- The `Create Mapping File <create_mapping_file.rst>`_ procedure is complete.
- The `Configure Credentials <configure_credentials.rst>`_ procedure is complete (BMC credentials
  configured).
- BMC/iDRAC interfaces on target servers are connected to the BMC network and
  have IP addresses assigned (either static or via existing DHCP).
- Admin network NICs on target servers are cabled and connected to the admin
  network switch.



Procedure
---------


#. **Enter the omnia_core container**:


**Run on: OIM host**

.. code-block:: bash
      ssh omnia_core



#. **Verify the mapping file is in place**:


**Run on: omnia_core container**

.. code-block:: bash
      cat /opt/omnia/input/project_default/pxe_mapping_file.csv



#. **Run the discovery playbook**:


**Run on: omnia_core container**

.. code-block:: bash
      cd /omnia/discovery
      ansible-playbook discovery.yml --ask-vault-pass



   The playbook will:

  - Connect to each server's BMC/iDRAC using Redfish.
  - Configure network boot settings.
  - Set PXE as the first boot device.
  - Power-cycle the servers.
  - Wait for each server to PXE boot and register with SMD.

   !!! note

       Discovery can take **30-60 minutes** depending on the number of nodes.
       Each server must complete a full PXE boot cycle.

#. **Monitor discovery progress** by watching the Ansible output. Each node
   will progress through these stages:

  - ``Configuring BMC`` -- Setting iDRAC boot options
  - ``Powering on`` -- Sending power-on command via Redfish
  - ``Waiting for PXE boot`` -- Node is booting from network
  - ``Registered`` -- Node appeared in SMD inventory



Verification
------------


#. **List discovered nodes in OpenCHAMI**:


**Run on: omnia_core container**

.. code-block:: bash
      ochami node list



   Expected output shows all nodes from the mapping file with their service
   tags, MAC addresses, and assigned IPs.

#. **Check SMD inventory**:


**Run on: omnia_core container**

.. code-block:: bash
      ochami smd status



#. **Verify node count matches the mapping file**:


**Run on: omnia_core container**

.. code-block:: bash
      # Count discovered nodes
      ochami node list | wc -l
   
      # Count entries in mapping file (excluding header)
      tail -n +2 /opt/omnia/input/project_default/pxe_mapping_file.csv | wc -l



#. **Ping each discovered node** on the admin network:


**Run on: omnia_core container**

.. code-block:: bash
      # Example: ping a specific node
      ping -c 3 10.5.0.101



#. **Check Ansible inventory** was populated:


**Run on: omnia_core container**

.. code-block:: bash
      ansible-inventory --list | python3 -m json.tool | head -50





Next Steps
----------


- `Pxe Boot Nodes <pxe_boot_nodes.rst>`_ -- Ensure all nodes complete provisioning.
- `Verify Cluster <verify_cluster.rst>`_ -- Verify the cluster is operational.
- `Setup Slurm <../Slurm/setup_slurm.rst>`_ -- Deploy Slurm on discovered nodes.



Troubleshooting
---------------


**Node not discovered (missing from SMD)**
  - Verify the BMC IP is reachable from the OIM:


**Run on: OIM host**

.. code-block:: bash
        ping -c 3 <bmc-ip>



  - Check iDRAC web UI for boot errors.
  - Verify the ``ADMIN_MAC`` in the mapping file matches the PXE NIC.

**BMC connection refused**
  - Confirm BMC credentials are correct in the encrypted credentials file.
  - Verify iDRAC is not locked out (too many failed login attempts).
  - Check that Redfish is enabled in iDRAC settings.

**PXE boot timeout**
  - Verify DHCP is running on the OIM:


**Run on: OIM host**

.. code-block:: bash
        systemctl status coredhcp.service



  - Check TFTP service:


**Run on: OIM host**

.. code-block:: bash
        systemctl status tftpd.service



  - Verify the admin network switch is configured with the correct VLAN.

**Some nodes discover but others do not**
  - Check for MAC address typos in the mapping file.
  - Verify the physical cabling on failed nodes.
  - Check for IP conflicts on the admin network:


**Run on: OIM host**

.. code-block:: bash
        arping -D -I <admin-nic> <admin-ip>



**Discovery playbook fails at BMC configuration step**
  - Ensure iDRAC firmware is up to date (minimum 5.x for PowerEdge 15th gen).
  - Verify Redfish API is accessible:


**Run on: OIM host**

.. code-block:: bash
        curl -sk https://<bmc-ip>/redfish/v1/ -u <user>:<pass>

