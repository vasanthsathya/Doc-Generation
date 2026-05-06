
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Storage Config 

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
 * [ Servers ](../SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](omnia_config.html)
 * Storage Config [ Storage Config ](storage_config.html) Table of contents 
 * [ NFS configuration ](#nfs-configuration)
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

 * [ NFS configuration ](#nfs-configuration)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Configuration ](omnia_config.html)

# storage_config.yml Reference[¶](#storage_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/storage_config.yml`

This file configures shared storage for the cluster, including NFS mounts, BeeGFS parallel filesystem settings, and Dell PowerScale/PowerVault integration.

## NFS configuration[¶](#nfs-configuration "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`nfs_client_params` | String | No | `nosuid,rw,sync,hard,intr` | Default NFS mount options applied to all NFS client mounts. 
`nfs_shares` | List | No | `[]` | List of NFS export definitions. Each entry defines a server path, client mount point, and options. 
`nfs_shares[].server` | String | Yes | (none) | IP address or hostname of the NFS server (e.g., `10.5.0.100` or `nfs.hpc.example.com`). 
`nfs_shares[].server_path` | String | Yes | (none) | Export path on the NFS server (e.g., `/exports/home`). 
`nfs_shares[].client_mount_path` | String | Yes | (none) | Mount point on the cluster nodes (e.g., `/home`). 
`nfs_shares[].mount_options` | String | No | Value of `nfs_client_params` | Per-share mount options that override the global default. 
 
## BeeGFS configuration[¶](#beegfs-configuration "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`beegfs_enabled` | Boolean | No | `false` | Enable BeeGFS client installation and configuration on cluster nodes. 
`beegfs_mgmt_server` | String | Conditional | (none) | IP address or hostname of the BeeGFS management server. Required when `beegfs_enabled` is `true`. 
`beegfs_mount_path` | String | No | `/mnt/beegfs` | Local mount point for the BeeGFS filesystem on client nodes. 
`beegfs_client_config_path` | String | No | `/etc/beegfs/beegfs-client.conf` | Path to the BeeGFS client configuration file. 
`beegfs_connInterfacesFile` | String | No | (none) | Path to a file listing network interfaces for BeeGFS communication (one interface per line). 
`beegfs_connNetFilterFile` | String | No | (none) | Path to a file listing allowed subnets for BeeGFS traffic. 
 
## PowerScale configuration[¶](#powerscale-configuration "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`powerscale_enabled` | Boolean | No | `false` | Enable PowerScale NFS export mounting on cluster nodes. 
`powerscale_server` | String | Conditional | (none) | SmartConnect zone name or IP of the PowerScale cluster. Required when `powerscale_enabled` is `true`. 
`powerscale_exports` | List | Conditional | `[]` | List of PowerScale NFS exports to mount. Each entry uses the same schema as `nfs_shares[]`. 
 
## PowerVault ME5 configuration[¶](#powervault-me5-configuration "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`powervault_enabled` | Boolean | No | `false` | Enable PowerVault ME5 iSCSI volume mapping on cluster nodes. 
`powervault_mgmt_ip` | String | Conditional | (none) | Management IP address of the PowerVault ME5 controller. Required when `powervault_enabled` is `true`. 
`powervault_volumes` | List | Conditional | `[]` | List of volume-to-host mappings. Each entry specifies a LUN, target nodes, and a mount point. 
`powervault_volumes[].volume_name` | String | Yes | (none) | Name of the pre-created PowerVault volume/LUN. 
`powervault_volumes[].mount_path` | String | Yes | (none) | Local mount point on the target node(s). 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/storage_config.yml
 
 
 nfs_client_params: "nosuid,rw,sync,hard,intr"
 nfs_shares:
 - server: "10.5.0.100"
 server_path: "/exports/home"
 client_mount_path: "/home"
 - server: "10.5.0.100"
 server_path: "/exports/scratch"
 client_mount_path: "/scratch"
 mount_options: "rw,sync,noatime"
 
 beegfs_enabled: false
 
 powerscale_enabled: true
 powerscale_server: "powerscale-sc.hpc.example.com"
 powerscale_exports:
 - server_path: "/ifs/data/hpc"
 client_mount_path: "/data"
 
 powervault_enabled: false
 

Info

 * [Storage](../SupportMatrix/storage.html) \-- Supported storage platforms.
 * [Beegfs Server Setup](../Appendices/beegfs_server_setup.html) \-- BeeGFS server setup.
 * [Disk Space](../ClusterRequirements/disk_space.html) \-- Disk space requirements.

Back to top [ Previous Telemetry Config ](telemetry_config.html) [ Next Security Config ](security_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
