# Setup Slurm

Deploy the Slurm workload manager across your provisioned cluster using the `omnia.yml` playbook. This configures a Slurm controller, compute nodes, and optional login nodes for HPC job scheduling.

## Overview

The `omnia.yml` playbook deploys and configures Slurm across nodes defined in your mapping file. It performs the following:

 1. Installs Slurm packages (`slurmctld`, `slurmd`, `munge`) from local repositories.
 2. Generates `slurm.conf` based on discovered hardware (CPUs, memory, GPUs).
 3. Configures Munge authentication across all Slurm nodes.
 4. Sets up MariaDB for Slurm accounting.
 5. Starts and enables Slurm services on all nodes.

## Prerequisites

 * The `omnia_config.yml` input file is configured with Slurm parameters.
 * The `pxe_mapping_file.csv` has nodes assigned to `slurm_control_node` and `slurm_node` functional groups.

## Procedure

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

## Verification

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

## Next Steps

## Troubleshooting

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

Copyright © 2025 Dell Technologies. All rights reserved.