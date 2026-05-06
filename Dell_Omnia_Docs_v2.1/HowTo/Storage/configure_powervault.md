
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Configure PowerVault 

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
 * [ Configure NFS ](configure_nfs.html)
 * Configure PowerVault [ Configure PowerVault ](configure_powervault.html) Table of contents 
 * [ Overview ](#overview)
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
 3. [ Storage ](configure_nfs.html)

# Configure PowerVault[¶](#configure-powervault "Permanent link")

Integrate Dell PowerVault ME5 iSCSI storage with your Omnia cluster for block-level storage on the Slurm controller, providing high-performance local storage with multipath redundancy.

## Overview[¶](#overview "Permanent link")

Dell PowerVault ME5 provides iSCSI block storage that can be mapped to Slurm controller or compute nodes as local disks. This is useful for:

 * Slurm spool and state directories requiring high I/O throughput.
 * MariaDB (Slurm accounting database) storage.
 * Scratch storage for compute nodes.

Omnia configures:

 * iSCSI initiator on the target node(s).
 * Multipath I/O (DM-Multipath) for path redundancy.
 * Automatic LUN discovery and attachment.

## Prerequisites[¶](#prerequisites "Permanent link")

 * A Dell PowerVault ME5 storage array is configured and accessible on the admin or storage network.
 * iSCSI target ports on the PowerVault are configured with IP addresses.
 * A volume (LUN) is created on the PowerVault and mapped to the target host.
 * Network connectivity between the Slurm controller and the PowerVault iSCSI ports.
 * The PowerVault management IP is accessible for initial configuration.

## Procedure[¶](#procedure "Permanent link")

 1. **Install iSCSI and multipath packages** on the Slurm controller:

Run on: Slurm control node
 
 
 dnf install -y iscsi-initiator-utils device-mapper-multipath
 

 1. **Configure the iSCSI initiator name** :

Run on: Slurm control node
 
 
 cat /etc/iscsi/initiatorname.iscsi
 

If the initiator name is not set, generate one:

Run on: Slurm control node
 
 
 echo "InitiatorName=$(iscsi-iname)" > /etc/iscsi/initiatorname.iscsi
 

 1. **Configure DM-Multipath** :

Run on: Slurm control node
 
 
 cat <<'EOF' > /etc/multipath.conf
 defaults {
 polling_interval 10
 path_grouping_policy multibus
 find_multipaths yes
 no_path_retry 5
 user_friendly_names yes
 }
 
 devices {
 device {
 vendor "DellEMC"
 product "ME5"
 path_grouping_policy group_by_prio
 path_checker tur
 failback immediate
 no_path_retry queue
 }
 }
 EOF
 
 systemctl enable --now multipathd
 

 1. **Discover iSCSI targets** on the PowerVault:

Run on: Slurm control node
 
 
 iscsiadm -m discovery -t sendtargets -p 10.5.2.100:3260
 iscsiadm -m discovery -t sendtargets -p 10.5.2.101:3260
 

Replace `10.5.2.100` and `10.5.2.101` with your PowerVault iSCSI portal IPs.

 1. **Log in to the iSCSI targets** :

Run on: Slurm control node
 
 
 iscsiadm -m node --login
 

 1. **Start and enable the iSCSI service** :

Run on: Slurm control node
 
 
 systemctl enable --now iscsid
 systemctl enable --now iscsi
 

 1. **Verify multipath devices** :

Run on: Slurm control node
 
 
 multipath -ll
 

Expected output shows multipath devices with multiple paths:

Expected output on: Slurm control node
 
 
 mpath0 (360000000000000001) dm-0 DellEMC,ME5
 size=500G features='1 queue_if_no_path' hwhandler='0' wp=rw
 |-+- policy='round-robin 0' prio=1 status=active
 | `- 3:0:0:0 sda 8:0 active ready running
 `-+- policy='round-robin 0' prio=1 status=enabled
 `- 4:0:0:0 sdb 8:16 active ready running
 

 1. **Create a filesystem and mount the LUN** :

Run on: Slurm control node
 
 
 mkfs.xfs /dev/mapper/mpath0
 mkdir -p /var/spool/slurm
 mount /dev/mapper/mpath0 /var/spool/slurm
 

Add to `/etc/fstab` for persistence:

Run on: Slurm control node
 
 
 echo "/dev/mapper/mpath0 /var/spool/slurm xfs defaults,_netdev 0 0" >> /etc/fstab
 

## Verification[¶](#verification "Permanent link")

 1. **Verify iSCSI sessions** :

Run on: Slurm control node
 
 
 iscsiadm -m session
 

 1. **Verify multipath status** :

Run on: Slurm control node
 
 
 multipath -ll
 

All paths should show `active ready running`.

 1. **Verify the mount** :

Run on: Slurm control node
 
 
 df -h /var/spool/slurm
 

 1. **Test I/O performance** :

Run on: Slurm control node
 
 
 dd if=/dev/zero of=/var/spool/slurm/test bs=1M count=1024 oflag=direct
 rm /var/spool/slurm/test
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Configure Nfs](configure_nfs.html) \-- Configure NFS for shared storage across compute nodes.
 * [Setup Slurm](../Slurm/setup_slurm.html) \-- Deploy Slurm using the PowerVault storage for spool data.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**iSCSI discovery returns no targets** Verify network connectivity to the PowerVault iSCSI ports:

Run on: Slurm control node
 
 
 ping -c 3 10.5.2.100
 telnet 10.5.2.100 3260
 

**Multipath shows no paths** Check that iSCSI sessions are active:

Run on: Slurm control node
 
 
 iscsiadm -m session
 multipath -v3
 

**Path shows "failed faulty"** Check network connectivity on the failed path:

Run on: Slurm control node
 
 
 iscsiadm -m session -P 3 | grep -E "Target|iface|State"
 

**LUN not visible after login** Rescan SCSI buses:

Run on: Slurm control node
 
 
 iscsiadm -m session --rescan
 multipath -r
 

**Performance is below expectations** \- Verify jumbo frames are enabled on the iSCSI network:
 
 
 ```bash title="Run on: Slurm control node"
 ip link show | grep mtu
 ```
 

 * Ensure multipath load balancing is active (multiple paths `running`).

Back to top [ Previous Configure NFS ](configure_nfs.html) [ Next Configure InfiniBand ](../Networking/configure_infiniband.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
