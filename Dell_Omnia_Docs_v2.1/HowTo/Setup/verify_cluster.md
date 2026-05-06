
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Verify Cluster 

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
 * [ Prepare OIM ](prepare_oim.html)
 * Verify Cluster [ Verify Cluster ](verify_cluster.html) Table of contents 
 * [ Overview ](#overview)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
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
 3. [ Setup ](prepare_oim.html)

# Verify Cluster[¶](#verify-cluster "Permanent link")

Perform end-to-end verification of your provisioned cluster, including Slurm job scheduling, Kubernetes services, and basic node health checks.

## Overview[¶](#overview "Permanent link")

After provisioning and configuring your cluster, verify that:

 1. All nodes are reachable and report the expected hostname and OS.
 2. Slurm (if deployed) can schedule and run jobs across compute nodes.
 3. Kubernetes (if deployed) has all control-plane and worker nodes ready.
 4. Authentication and storage services are operational.

## Prerequisites[¶](#prerequisites "Permanent link")

 * Nodes are provisioned and reachable (see [Pxe Boot Nodes](pxe_boot_nodes.html)).
 * Slurm and/or Kubernetes have been deployed (see [Setup Slurm](../Slurm/setup_slurm.html) or [Setup Service K8S](../Kubernetes/setup_service_k8s.html)).

## Procedure[¶](#procedure "Permanent link")

### Verify Node Connectivity[¶](#verify-node-connectivity "Permanent link")

 1. **Ping all nodes** from the omnia_core container:

Run on: omnia_core container
 
 
 ansible all -m ping
 

Expected output for each node:

Expected output on: omnia_core container
 
 
 10.5.0.101 | SUCCESS => {
 "ping": "pong"
 }
 

 1. **Check OS version on all nodes** :

Run on: omnia_core container
 
 
 ansible all -m shell -a "cat /etc/os-release | grep PRETTY_NAME"
 

 1. **Check hostnames are correctly set** :

Run on: omnia_core container
 
 
 ansible all -m shell -a "hostname"
 

### Verify Slurm[¶](#verify-slurm "Permanent link")

 1. **SSH to the Slurm control node** and check the cluster status:

Run on: omnia_core container
 
 
 ssh root@<slurm-control-node-ip>
 

Run on: Slurm control node
 
 
 sinfo
 

Expected output:

Expected output on: Slurm control node
 
 
 PARTITION AVAIL TIMELIMIT NODES STATE NODELIST
 normal* up infinite 2 idle compute[01-02]
 

All nodes should show `idle` state. If any show `down` or `drain`, investigate further.

 1. **Run a test job** across all compute nodes:

Run on: Slurm control node
 
 
 srun -N 2 hostname
 

Expected output shows the hostnames of the compute nodes that executed the job:

Expected output on: Slurm control node
 
 
 compute01
 compute02
 

 1. **Submit a batch job** :

Run on: Slurm control node
 
 
 cat <<'EOF' > /tmp/test_job.sh
 #!/bin/bash
 #SBATCH --job-name=test
 #SBATCH --nodes=1
 #SBATCH --time=00:01:00
 echo "Hello from $(hostname) at $(date)"
 EOF
 
 sbatch /tmp/test_job.sh
 

Run on: Slurm control node
 
 
 # Check job status
 squeue
 
 # View job output after completion
 cat slurm-*.out
 

 1. **Verify Slurm accounting** :

Run on: Slurm control node
 
 
 sacct --starttime=today
 

### Verify Kubernetes[¶](#verify-kubernetes "Permanent link")

 1. **Check Kubernetes node status** from a control-plane node:

Run on: omnia_core container
 
 
 ssh root@<k8s-control-plane-ip>
 

Run on: K8s control plane node
 
 
 kubectl get nodes
 

Expected output:

Expected output on: K8s control plane node
 
 
 NAME STATUS ROLES AGE VERSION
 k8s-cp01 Ready control-plane 1h v1.28.x
 k8s-cp02 Ready control-plane 1h v1.28.x
 k8s-cp03 Ready control-plane 1h v1.28.x
 k8s-worker01 Ready <none> 1h v1.28.x
 

All nodes should show `Ready` status.

 1. **Verify core Kubernetes components** :

Run on: K8s control plane node
 
 
 kubectl get pods -A
 

All system pods (`kube-system`, `calico-system`, `metallb-system`) should be `Running`.

 1. **Test pod scheduling** :

Run on: K8s control plane node
 
 kubectl run test-pod --image=busybox --restart=Never -- echo "Hello from K8s"
 kubectl logs test-pod
 kubectl delete pod test-pod
 

## Verification[¶](#verification "Permanent link")

Use the following summary checklist:

Check | Command | Expected Result 
---|---|--- 
All nodes reachable | `ansible all -m ping` | All return `pong` 
Slurm nodes idle | `sinfo` | All nodes `idle` 
Slurm job runs | `srun -N 2 hostname` | Hostnames printed 
K8s nodes ready | `kubectl get nodes` | All `Ready` 
K8s pods running | `kubectl get pods -A` | All `Running` 
 
## Next Steps[¶](#next-steps "Permanent link")

 * [Slurm With Gpu](../Slurm/slurm_with_gpu.html) \-- Configure GPU support for Slurm.
 * [Setup Telemetry](../Telemetry/setup_telemetry.html) \-- Deploy monitoring and telemetry.
 * [Setup Openldap](../Authentication/setup_openldap.html) \-- Set up centralized authentication.
 * [Configure Nfs](../Storage/configure_nfs.html) \-- Configure shared NFS storage.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Ansible ping fails for some nodes** \- Verify SSH keys are deployed:
 
 
 ```bash title="Run on: omnia_core container"
 ssh-copy-id root@<node-ip>
 ```
 

 * Check network connectivity:

Run on: omnia_core container
 
 ping -c 3 <node-ip>
 

**Slurm nodes show "down" state** Check the Slurm daemon on the affected compute node:

Run on: affected compute node
 
 
 systemctl status slurmd
 journalctl -u slurmd --no-pager -n 20
 

Resume the node from the control node:

Run on: Slurm control node
 
 
 scontrol update nodename=<node> state=resume
 

**Kubernetes node shows "NotReady"** Check kubelet status on the affected node:

Run on: affected K8s node
 
 
 systemctl status kubelet
 journalctl -u kubelet --no-pager -n 20
 

**Slurm srun hangs** \- Verify `munge` is running on all Slurm nodes:
 
 
 ```bash title="Run on: omnia_core container"
 ansible slurm_cluster -m shell -a "systemctl is-active munge"
 ```
 

 * Check firewall rules allow Slurm traffic (ports 6817-6819):

Run on: omnia_core container
 
 ansible slurm_cluster -m shell -a "firewall-cmd --list-ports"
 

Back to top [ Previous Verify OIM Services ](verify_oim_services.html) [ Next Set Up Slurm ](../Slurm/setup_slurm.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
