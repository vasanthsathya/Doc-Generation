
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Storage 

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
 * [ Servers ](servers.html)
 * Storage [ Storage ](storage.html) Table of contents 
 * [ Storage support matrix ](#storage-support-matrix)
 * Configuration Configuration 
 * [ Omnia Config ](../Configuration/omnia_config.html)
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

 * [ Storage support matrix ](#storage-support-matrix)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Support Matrix ](servers.html)

# Supported Storage[¶](#supported-storage "Permanent link")

Omnia v2.1 supports the following Dell storage platforms for shared filesystems and persistent volumes.

## Storage support matrix[¶](#storage-support-matrix "Permanent link")

Platform | Version | Protocol | Notes 
---|---|---|--- 
Dell PowerScale (Isilon) | OneFS 9.x | NFS, SMB | Scale-out NAS; ideal for shared home directories and scratch filesystems. Omnia configures NFS client mounts on cluster nodes. 
Dell PowerVault ME5 | ME5 Series | iSCSI, FC, SAS | Block storage; suitable for databases, boot volumes, and high-IOPS workloads. Omnia configures iSCSI initiators on target nodes. 
 
## PowerScale (OneFS) integration[¶](#powerscale-onefs-integration "Permanent link")

Parameter | Description 
---|--- 
OneFS version | 9.x (9.4 or later recommended) 
Access zone | Configure a dedicated access zone for HPC exports to isolate permissions and authentication. 
Protocol | NFS v3 or NFS v4.x -- configured in `storage_config.yml` (see [Storage Config](../Configuration/storage_config.html)). 
Authentication | Local, LDAP, or Active Directory. Must match the cluster authentication method configured in `security_config.yml`. 
SMB support | Supported for Windows or mixed-OS clients. Not used by default in Omnia HPC deployments. 
 
Note

Omnia mounts PowerScale NFS exports on cluster nodes using the mount parameters specified in `storage_config.yml`. The PowerScale cluster itself must be configured and operational before running `omnia.yml`.

## PowerVault ME5 integration[¶](#powervault-me5-integration "Permanent link")

Parameter | Description 
---|--- 
Series | ME5012, ME5024, ME5084 
Protocol | iSCSI (default for Omnia integration), Fibre Channel, SAS 
Volumes | Pre-create LUNs and map them to host groups before running Omnia storage playbooks. 
Multipath | DM-Multipath (`device-mapper-multipath`) is recommended for redundancy and load balancing. 
Configuration | `storage_config.yml` specifies the PowerVault management IP, volume mappings, and mount points. 
 
## BeeGFS parallel filesystem[¶](#beegfs-parallel-filesystem "Permanent link")

In addition to Dell storage appliances, Omnia supports BeeGFS as a software- defined parallel filesystem running on cluster nodes.

Component | Description 
---|--- 
BeeGFS version | Consult `local_repo_config.yml` for the configured version. 
Server roles | Management, metadata, and storage services can run on dedicated nodes or co-located with compute nodes. 
Client | Omnia installs the BeeGFS client on designated nodes and mounts the filesystem at the path specified in `storage_config.yml`. 
 
Info

 * [Storage Config](../Configuration/storage_config.html) \-- Storage configuration parameters.
 * [Beegfs Server Setup](../Appendices/beegfs_server_setup.html) \-- BeeGFS server setup reference.
 * [Disk Space](../ClusterRequirements/disk_space.html) \-- Disk space requirements for storage nodes.

Back to top [ Previous Switches ](switches.html) [ Next Installed Software ](installed_software.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
