# Slurm Config Backup

Back up, rollback, and clean up Slurm configuration files to safeguard against configuration errors and enable rapid recovery.

## Overview

Maintaining Slurm configuration backups is critical for:

 * **Recovery** \-- Quickly restore a working configuration after a bad change.
 * **Auditing** \-- Track configuration changes over time.
 * **Rollback** \-- Revert to a known-good state during troubleshooting.

This guide covers backing up `slurm.conf`, `gres.conf`, `cgroup.conf`, and related files on the Slurm control node.

## Prerequisites

 * `root` or `sudo` access to the Slurm control node.

## Procedure

### Backup

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

### Rollback

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

### Cleanup

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

## Verification

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

## Next Steps

## Troubleshooting

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

Copyright © 2025 Dell Technologies. All rights reserved.