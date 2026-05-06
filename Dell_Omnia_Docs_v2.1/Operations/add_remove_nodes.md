
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Add / Remove Nodes 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../index.html)

[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../index.html)

Overview 
 * [ Architecture ](../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Reference/Appendices/hostname_requirements.html)

Operations 
 * Add / Remove Nodes [ Add / Remove Nodes ](add_remove_nodes.html) Table of contents 
 * [ Adding compute nodes ](#adding-compute-nodes)

Troubleshooting 
 * [ General ](../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ Adding compute nodes ](#adding-compute-nodes)

 1. [ Home ](../index.html)
 2. [ Operations ](index.html)

# Add and Remove Nodes[¶](#add-and-remove-nodes "Permanent link")

Omnia supports dynamically scaling your Slurm cluster by adding new compute nodes or removing existing ones without disrupting running workloads. This procedure uses the `add_node` and `remove_node` playbooks from inside the `omnia_core` Podman container on the OIM.

## Adding compute nodes[¶](#adding-compute-nodes "Permanent link")

Use this procedure when new servers have been racked, cabled, and discovered by the OIM, and you want to include them in the Slurm cluster.

### Prerequisites[¶](#prerequisites "Permanent link")

 * The new nodes have been provisioned with an operating system via [Discover Nodes](../HowTo/Setup/discover_nodes.html) and [Pxe Boot Nodes](../HowTo/Setup/pxe_boot_nodes.html).
 * Network connectivity between the OIM and the new nodes is verified (SSH access works).
 * The Slurm cluster is already operational (`slurmctld` is running on the control node).

### Procedure[¶](#procedure "Permanent link")

 1. **Update the node mapping file.** Add the new node entries (MAC address, hostname, IP) to the mapping file used during initial deployment:

 
 
 # /omnia/input/mapping_file.csv
 AA:BB:CC:DD:EE:F1,compute-05,10.5.0.105
 AA:BB:CC:DD:EE:F2,compute-06,10.5.0.106
 

 1. **Access the omnia_core container** on the OIM:

 
 
 ssh omnia_core
 

 1. **Run the add_node playbook:**

 
 
 cd /omnia
 ansible-playbook playbooks/add_node.yml
 

The playbook will:

 * Install and configure `slurmd` on each new node.
 * Register the nodes with the Slurm controller.
 * Apply any GPU drivers or additional packages as specified in the configuration.

 * **Verify the new nodes** are visible to Slurm:

 
 
 sinfo
 

Expected output shows the new nodes in an `idle` state:
 
 
 PARTITION AVAIL TIMELIMIT NODES STATE NODELIST
 normal* up infinite 6 idle compute-[01-06]
 

## Removing compute nodes[¶](#removing-compute-nodes "Permanent link")

Use this procedure when decommissioning servers or temporarily removing nodes from the scheduling pool.

### Prerequisites[¶](#prerequisites_1 "Permanent link")

 * You have `root` or `sudo` access to the OIM.
 * No critical jobs are running on the nodes to be removed (or you are prepared to let them drain).

### Procedure[¶](#procedure_1 "Permanent link")

 1. **Drain the node** to allow running jobs to complete and prevent new jobs from being scheduled:

 
 
 scontrol update NodeName=compute-05 State=DRAIN Reason="Decommissioning"
 

Verify the node enters the `drained` state:
 
 
 sinfo -n compute-05
 
 
 
 PARTITION AVAIL TIMELIMIT NODES STATE NODELIST
 normal* up infinite 1 drained compute-05
 

 1. **Access the omnia_core container** on the OIM:

 
 
 ssh omnia_core
 

 1. **Run the remove_node playbook:**

 
 
 cd /omnia
 ansible-playbook playbooks/remove_node.yml -e "target_nodes=compute-05"
 

 1. **Update the mapping file.** Remove the decommissioned node entry from `/omnia/input/mapping_file.csv` to prevent it from being re-added in future operations.

 2. **Verify the node has been removed:**

 
 
 sinfo
 

The removed node should no longer appear in the node list.

## Verification[¶](#verification "Permanent link")

After adding or removing nodes, confirm the cluster state:

Run on: Slurm control node
 
 
 # Check overall cluster health
 sinfo
 
 # Verify controller sees all expected nodes
 scontrol show nodes | grep NodeName
 
 # Submit a test job to verify scheduling
 srun -N 1 hostname
 

Info

 * [Add Slurm Nodes](../HowTo/Slurm/add_slurm_nodes.html) \-- Detailed how-to for adding Slurm nodes.
 * [Remove Slurm Nodes](../HowTo/Slurm/remove_slurm_nodes.html) \-- Detailed how-to for removing Slurm nodes.
 * [Reprovision Cluster](reprovision_cluster.html) \-- Re-image nodes instead of just adding/removing them.

Back to top [ Previous Operations & Maintenance ](index.html) [ Next Reprovision Cluster ](reprovision_cluster.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
