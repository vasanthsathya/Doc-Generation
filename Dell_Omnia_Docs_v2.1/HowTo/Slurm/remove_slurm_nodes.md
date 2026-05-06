
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Remove Slurm Nodes 

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
 * Remove Slurm Nodes [ Remove Slurm Nodes ](remove_slurm_nodes.html) Table of contents 
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

# Remove Slurm Nodes[¶](#remove-slurm-nodes "Permanent link")

Safely remove compute nodes from a running Slurm cluster without disrupting active workloads.

## Overview[¶](#overview "Permanent link")

Removing a node from a Slurm cluster involves:

 1. Draining the node so no new jobs are scheduled on it.
 2. Waiting for any running jobs to complete (or canceling them).
 3. Removing the node from `slurm.conf` on the control node.
 4. Stopping Slurm services on the target node.
 5. Reconfiguring the Slurm controller.

## Prerequisites[¶](#prerequisites "Permanent link")

 * A working Slurm cluster deployed via [Setup Slurm](setup_slurm.html).
 * `root` or `sudo` access to the Slurm control node and the target compute node(s).
 * Identify which node(s) to remove (hostname and IP address).

## Procedure[¶](#procedure "Permanent link")

 1. **Drain the target node** to prevent new jobs from being scheduled:

Run on: Slurm control node
 
 
 scontrol update nodename=<node-to-remove> state=drain reason="Decommissioning"
 

 1. **Verify the node is draining** and check for running jobs:

Run on: Slurm control node
 
 
 sinfo -n <node-to-remove>
 squeue -w <node-to-remove>
 

Wait for all jobs on the node to complete. If immediate removal is needed, cancel running jobs:

Run on: Slurm control node
 
 
 # Cancel all jobs on the target node
 scancel -w <node-to-remove>
 

 1. **Set the node to down** :

Run on: Slurm control node
 
 
 scontrol update nodename=<node-to-remove> state=down reason="Removed from cluster"
 

 1. **Stop Slurm services on the target node** :

Run on: node being removed
 
 
 systemctl stop slurmd
 systemctl disable slurmd
 systemctl stop munge
 systemctl disable munge
 

 1. **Remove the node from slurm.conf** on the control node:

Run on: Slurm control node
 
 
 vi /etc/slurm/slurm.conf
 

Remove or comment out the `NodeName=` line for the target node. Also update the `PartitionName=` line to remove the node from the `Nodes=` list.

 1. **Reconfigure Slurm** to apply changes:

Run on: Slurm control node
 
 
 scontrol reconfigure
 

 1. **(Optional) Remove the node from the mapping file** :

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/pxe_mapping_file.csv
 

Remove or comment out the row for the decommissioned node.

## Verification[¶](#verification "Permanent link")

 1. **Confirm the node is no longer in the cluster** :

Run on: Slurm control node
 
 
 sinfo
 scontrol show nodes
 

The removed node should no longer appear.

 1. **Run a test job** to confirm remaining nodes are functional:

Run on: Slurm control node
 
 
 srun -N 1 hostname
 

 1. **Verify no orphaned jobs** reference the removed node:

Run on: Slurm control node
 
 
 squeue -t all
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Add Slurm Nodes](add_slurm_nodes.html) \-- Add replacement nodes if needed.
 * [Slurm Config Backup](slurm_config_backup.html) \-- Back up the updated Slurm configuration.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Node still appears in sinfo after removal** Ensure you ran `scontrol reconfigure` after editing `slurm.conf`:

Run on: Slurm control node
 
 
 scontrol reconfigure
 

**Jobs were running on the removed node** If jobs were not properly drained, they may show as `FAILED` or `NODE_FAIL` in the accounting:

Run on: Slurm control node
 
 
 sacct --starttime=today --state=FAILED,NODE_FAIL
 

Resubmit affected jobs as needed.

**slurm.conf syntax error after editing** Validate the configuration:

Run on: Slurm control node
 
 
 slurmd -C # Show computed node configuration
 slurmctld -t # Test configuration file syntax
 

**Cannot connect to the removed node to stop services** If the node is unreachable, the Slurm controller will time it out automatically. Simply remove it from `slurm.conf` and reconfigure.

Back to top [ Previous Add Slurm Nodes ](add_slurm_nodes.html) [ Next Config Backup ](slurm_config_backup.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
