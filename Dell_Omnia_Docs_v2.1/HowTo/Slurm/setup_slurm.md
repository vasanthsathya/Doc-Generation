
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Set Up Slurm 

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
 * Set Up Slurm [ Set Up Slurm ](setup_slurm.html) Table of contents 
 * [ Overview ](#overview)
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
 3. [ Slurm ](setup_slurm.html)

# Setup Slurm[¶](#setup-slurm "Permanent link")

Deploy the Slurm workload manager across your provisioned cluster using the `omnia.yml` playbook. This configures a Slurm controller, compute nodes, and optional login nodes for HPC job scheduling.

## Overview[¶](#overview "Permanent link")

The `omnia.yml` playbook deploys and configures Slurm across nodes defined in your mapping file. It performs the following:

 1. Installs Slurm packages (`slurmctld`, `slurmd`, `munge`) from local repositories.
 2. Generates `slurm.conf` based on discovered hardware (CPUs, memory, GPUs).
 3. Configures Munge authentication across all Slurm nodes.
 4. Sets up MariaDB for Slurm accounting.
 5. Starts and enables Slurm services on all nodes.

## Prerequisites[¶](#prerequisites "Permanent link")

 * Nodes are provisioned and reachable (see [Verify Cluster](../Setup/verify_cluster.html)).
 * The `omnia_config.yml` input file is configured with Slurm parameters.
 * The `pxe_mapping_file.csv` has nodes assigned to `slurm_control_node` and `slurm_node` functional groups.
 * Local repositories are synced (see [Create Local Repos](../Setup/create_local_repos.html)).
 * Encrypted credentials are configured (see [Configure Credentials](../Setup/configure_credentials.html)).

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Review and edit omnia_config.yml** :

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

Key Slurm-related parameters:

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # Slurm configuration
 slurm_installation_type: "nfs_share"
 enable_omnia_nfs: true
 
 # MariaDB for Slurm accounting
 mariadb_password: "" # Set via credentials utility
 
 # Optional: Slurm partitions
 slurm_partition_name: "normal"
 slurm_default_partition: true
 

 1. **Run the omnia.yml playbook** :

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook omnia.yml --ask-vault-pass
 

The playbook will:

 * Install Slurm packages on all designated nodes.
 * Generate and distribute `slurm.conf`.
 * Configure and start Munge on all Slurm nodes.
 * Set up MariaDB for accounting on the control node.
 * Start `slurmctld` on the control node.
 * Start `slurmd` on all compute nodes.

Execution time: **20-40 minutes** depending on cluster size.

 1. **Monitor playbook progress**. Watch for successful completion of each role:

 2. `slurm/common` \-- Package installation on all nodes

 3. `slurm/control` \-- Controller daemon setup
 4. `slurm/compute` \-- Compute daemon setup
 5. `slurm/login` \-- Login node configuration (if applicable)

## Verification[¶](#verification "Permanent link")

 1. **Check Slurm controller status** :

Run on: Slurm control node
 
 
 systemctl status slurmctld
 

 1. **Check compute daemon status on a compute node** :

Run on: Slurm compute node
 
 
 systemctl status slurmd
 

 1. **View the cluster partition and node status** :

Run on: Slurm control node
 
 
 sinfo
 

Expected output:

Expected output on: Slurm control node
 
 
 PARTITION AVAIL TIMELIMIT NODES STATE NODELIST
 normal* up infinite 2 idle compute[01-02]
 

 1. **Run a test job** :

Run on: Slurm control node
 
 
 srun -N 2 hostname
 

 1. **Verify Munge authentication** :

Run on: Slurm control node
 
 
 munge -n | ssh <compute-node> unmunge
 

Expected: successful decode with no errors.

 1. **Check Slurm accounting** :

Run on: Slurm control node
 
 
 sacctmgr show cluster
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Add Slurm Nodes](add_slurm_nodes.html) \-- Add more compute nodes to the cluster.
 * [Slurm With Gpu](slurm_with_gpu.html) \-- Configure GPU support.
 * [Configure Nfs](../Storage/configure_nfs.html) \-- Set up shared NFS storage.
 * [Setup Openldap](../Authentication/setup_openldap.html) \-- Configure user authentication.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**slurmctld fails to start** Check the Slurm controller log:

Run on: Slurm control node
 
 
 journalctl -u slurmctld --no-pager -n 50
 cat /var/log/slurm/slurmctld.log
 

**Compute nodes show "down" in sinfo** \- Verify `slurmd` is running on the affected node:
 
 
 ```bash title="Run on: affected compute node"
 systemctl status slurmd
 journalctl -u slurmd --no-pager -n 20
 ```
 

 * Check Munge is running:

Run on: affected compute node
 
 systemctl status munge
 

 * Resume the node:

Run on: Slurm control node
 
 scontrol update nodename=<node> state=resume
 

**Munge authentication failure** Ensure the Munge key is identical on all nodes:

Run on: omnia_core container
 
 
 ansible slurm_cluster -m shell -a "md5sum /etc/munge/munge.key"
 

All nodes should report the same MD5 hash.

**MariaDB connection error** Check MariaDB is running on the control node:

Run on: Slurm control node
 
 
 systemctl status mariadb
 mysql -u slurm -p -e "SHOW DATABASES;"
 

Back to top [ Previous Verify Cluster ](../Setup/verify_cluster.html) [ Next Build Slurm Repo ](build_slurm_repo.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
