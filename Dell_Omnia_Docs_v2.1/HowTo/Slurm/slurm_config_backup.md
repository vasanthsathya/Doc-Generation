
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Config Backup 

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
 * [ Set Up Slurm ](setup_slurm.html)
 * Config Backup [ Config Backup ](slurm_config_backup.html) Table of contents 
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

# Slurm Config Backup[¶](#slurm-config-backup "Permanent link")

Back up, rollback, and clean up Slurm configuration files to safeguard against configuration errors and enable rapid recovery.

## Overview[¶](#overview "Permanent link")

Maintaining Slurm configuration backups is critical for:

 * **Recovery** \-- Quickly restore a working configuration after a bad change.
 * **Auditing** \-- Track configuration changes over time.
 * **Rollback** \-- Revert to a known-good state during troubleshooting.

This guide covers backing up `slurm.conf`, `gres.conf`, `cgroup.conf`, and related files on the Slurm control node.

## Prerequisites[¶](#prerequisites "Permanent link")

 * A working Slurm cluster deployed via [Setup Slurm](setup_slurm.html).
 * `root` or `sudo` access to the Slurm control node.

## Procedure[¶](#procedure "Permanent link")

### Backup[¶](#backup "Permanent link")

 1. **Create a backup directory** on the Slurm control node:

Run on: Slurm control node
 
 
 mkdir -p /opt/slurm_backup
 

 1. **Create a timestamped backup** of all Slurm configuration files:

Run on: Slurm control node
 
 
 BACKUP_DIR="/opt/slurm_backup/$(date +%Y%m%d_%H%M%S)"
 mkdir -p "$BACKUP_DIR"
 
 cp /etc/slurm/slurm.conf "$BACKUP_DIR/"
 cp /etc/slurm/gres.conf "$BACKUP_DIR/" 2>/dev/null
 cp /etc/slurm/cgroup.conf "$BACKUP_DIR/" 2>/dev/null
 cp /etc/slurm/topology.conf "$BACKUP_DIR/" 2>/dev/null
 cp /etc/slurm/job_container.conf "$BACKUP_DIR/" 2>/dev/null
 cp /etc/munge/munge.key "$BACKUP_DIR/"
 
 echo "Backup created: $BACKUP_DIR"
 ls -la "$BACKUP_DIR/"
 

 1. **(Optional) Create an automated backup** using a cron job:

Run on: Slurm control node
 
 
 cat <<'EOF' > /etc/cron.daily/slurm_backup.sh
 #!/bin/bash
 BACKUP_DIR="/opt/slurm_backup/$(date +%Y%m%d_%H%M%S)"
 mkdir -p "$BACKUP_DIR"
 cp /etc/slurm/*.conf "$BACKUP_DIR/"
 cp /etc/munge/munge.key "$BACKUP_DIR/"
 # Keep only last 30 days of backups
 find /opt/slurm_backup -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
 EOF
 
 chmod +x /etc/cron.daily/slurm_backup.sh
 

### Rollback[¶](#rollback "Permanent link")

 1. **List available backups** :

Run on: Slurm control node
 
 
 ls -lt /opt/slurm_backup/
 

 1. **Restore from a backup** :

Run on: Slurm control node
 
 
 # Select the backup to restore (e.g., the most recent)
 RESTORE_DIR=$(ls -dt /opt/slurm_backup/*/ | head -1)
 echo "Restoring from: $RESTORE_DIR"
 
 # Stop Slurm services
 systemctl stop slurmctld
 
 # Restore configuration files
 cp "$RESTORE_DIR/slurm.conf" /etc/slurm/slurm.conf
 cp "$RESTORE_DIR/gres.conf" /etc/slurm/gres.conf 2>/dev/null
 cp "$RESTORE_DIR/cgroup.conf" /etc/slurm/cgroup.conf 2>/dev/null
 
 # Restart Slurm
 systemctl start slurmctld
 

 1. **Verify the restored configuration** :

Run on: Slurm control node
 
 
 scontrol show config | head -20
 sinfo
 

 1. **Distribute the restored config to compute nodes** if needed:

Run on: omnia_core container
 
 
 ansible slurm_node -m copy -a "src=/etc/slurm/slurm.conf dest=/etc/slurm/slurm.conf"
 ansible slurm_node -m service -a "name=slurmd state=restarted"
 

### Cleanup[¶](#cleanup "Permanent link")

 1. **Remove old backups** to free disk space:

Run on: Slurm control node
 
 
 # Remove backups older than 30 days
 find /opt/slurm_backup -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
 
 # Or remove all backups except the most recent 5
 ls -dt /opt/slurm_backup/*/ | tail -n +6 | xargs rm -rf
 

 1. **Check remaining backups and disk usage** :

Run on: Slurm control node
 
 
 du -sh /opt/slurm_backup
 ls -lt /opt/slurm_backup/
 

## Verification[¶](#verification "Permanent link")

 1. **Verify the current configuration is valid** :

Run on: Slurm control node
 
 
 slurmctld -t
 

If no errors are reported, the configuration is syntactically valid.

 1. **Verify all nodes are healthy** after a rollback:

Run on: Slurm control node
 
 
 sinfo
 scontrol ping
 

 1. **Diff the current config against a backup** to see changes:

Run on: Slurm control node
 
 
 diff /etc/slurm/slurm.conf /opt/slurm_backup/<latest>/slurm.conf
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Add Slurm Nodes](add_slurm_nodes.html) \-- Add new nodes (remember to back up before changes).
 * [Remove Slurm Nodes](remove_slurm_nodes.html) \-- Remove nodes (back up first).

## Troubleshooting[¶](#troubleshooting "Permanent link")

**slurmctld fails to start after rollback** The backup may reference nodes that no longer exist. Edit `slurm.conf` to match the current cluster state:

Run on: Slurm control node
 
 
 vi /etc/slurm/slurm.conf
 slurmctld -t # Test config
 

**Munge key mismatch after rollback** Ensure the Munge key is consistent across all nodes. If you restored the Munge key from backup, redistribute it:

Run on: omnia_core container
 
 
 ansible slurm_cluster -m copy -a "src=/etc/munge/munge.key dest=/etc/munge/munge.key owner=munge group=munge mode=0400"
 ansible slurm_cluster -m service -a "name=munge state=restarted"
 

**Backup directory runs out of space** Reduce the retention period or move backups to external storage:

Run on: Slurm control node
 
 
 du -sh /opt/slurm_backup
 # Adjust the cron cleanup period as needed
 

Back to top [ Previous Remove Slurm Nodes ](remove_slurm_nodes.html) [ Next Run HPC Benchmarks ](run_hpc_benchmarks.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
