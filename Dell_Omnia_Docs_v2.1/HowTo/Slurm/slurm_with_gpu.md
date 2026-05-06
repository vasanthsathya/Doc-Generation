
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Slurm with GPU 

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
 * Slurm with GPU [ Slurm with GPU ](slurm_with_gpu.html) Table of contents 
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

# Slurm with GPUs[¶](#slurm-with-gpus "Permanent link")

Configure GPU-enabled Slurm compute nodes with automatic driver installation for NVIDIA (CUDA), AMD (ROCm), and Intel Gaudi accelerators.

## Overview[¶](#overview "Permanent link")

Omnia automatically detects GPU hardware on compute nodes and installs the appropriate drivers and runtime libraries:

 * **NVIDIA GPUs** \-- CUDA toolkit and NVIDIA driver via the local CUDA repository.
 * **AMD GPUs** \-- ROCm runtime and driver.
 * **Intel Gaudi** \-- Habana Labs driver and runtime.

Slurm is configured with **GRES (Generic RESource)** definitions so jobs can request specific GPU types and quantities.

## Prerequisites[¶](#prerequisites "Permanent link")

 * Compute nodes with GPUs are provisioned and in the Slurm cluster.
 * The `software_config.json` includes the GPU software stack:

File: /opt/omnia/input/project_default/software_config.json
 
 
 {
 "softwares": [
 {"name": "slurm"},
 {"name": "cuda", "version": "12.2"},
 {"name": "rocm", "version": "6.0"}
 ]
 }
 

 * Local repositories are synced with GPU packages (see [Create Local Repos](../Setup/create_local_repos.html)).
 * GPU nodes are assigned to the `slurm_node` functional group in the mapping file.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Verify GPU software is listed in software_config.json** :

Run on: omnia_core container
 
 
 cat /opt/omnia/input/project_default/software_config.json | python3 -m json.tool
 

 1. **Configure GPU-related parameters in omnia_config.yml** :

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

GPU-related parameters:

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # GPU configuration
 cuda_toolkit_path: "/usr/local/cuda"
 rocm_install_path: "/opt/rocm"
 
 # Slurm GRES configuration (auto-detected if left empty)
 slurm_gres_config: ""
 

 1. **Run the omnia.yml playbook** (or re-run if Slurm is already deployed):

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook omnia.yml --ask-vault-pass
 

The playbook will:

 * Detect GPU hardware on each compute node.
 * Install CUDA, ROCm, or Gaudi drivers as appropriate.
 * Generate `gres.conf` with GPU device mappings.
 * Update `slurm.conf` with GRES definitions.
 * Restart Slurm services to apply changes.

 * **Reconfigure Slurm** to load GRES definitions:

Run on: Slurm control node
 
 
 scontrol reconfigure
 

## Verification[¶](#verification "Permanent link")

 1. **Verify GPU drivers are installed** on a compute node:

For NVIDIA:

Run on: GPU compute node
 
 
 nvidia-smi
 

Expected output shows GPU model, driver version, and memory usage.

For AMD:

Run on: GPU compute node
 
 
 rocm-smi
 

For Intel Gaudi:

Run on: GPU compute node
 
 
 hl-smi
 

 1. **Check Slurm GRES configuration** :

Run on: Slurm control node
 
 
 scontrol show nodes | grep -i gres
 

Expected output:

Expected output on: Slurm control node
 
 
 Gres=gpu:nvidia_a100:4
 GresUsed=gpu:nvidia_a100:0
 

 1. **Submit a GPU job** :

Run on: Slurm control node
 
 
 srun --gres=gpu:1 nvidia-smi
 

 1. **Submit a multi-GPU batch job** :

Run on: Slurm control node
 
 
 cat <<'EOF' > /tmp/gpu_test.sh
 #!/bin/bash
 #SBATCH --job-name=gpu_test
 #SBATCH --gres=gpu:2
 #SBATCH --nodes=1
 #SBATCH --time=00:05:00
 
 echo "Running on $(hostname)"
 echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
 nvidia-smi
 EOF
 
 sbatch /tmp/gpu_test.sh
 

 1. **Verify CUDA toolkit** (NVIDIA):

Run on: GPU compute node
 
 
 nvcc --version
 ls /usr/local/cuda/
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Run Hpc Benchmarks](run_hpc_benchmarks.html) \-- Run GPU-accelerated benchmarks.
 * [Use Apptainer](../Containers/use_apptainer.html) \-- Run GPU containers with Apptainer.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**nvidia-smi reports "no devices found"** \- Verify the GPU is physically seated and powered. \- Check that the NVIDIA driver module is loaded:
 
 
 ```bash title="Run on: GPU compute node"
 lsmod | grep nvidia
 dmesg | grep -i nvidia
 ```
 

 * Reinstall the driver:

Run on: GPU compute node
 
 dnf reinstall nvidia-driver cuda-toolkit
 

**GRES not showing in scontrol** Check `gres.conf` on the compute node:

Run on: GPU compute node
 
 
 cat /etc/slurm/gres.conf
 

The file should list each GPU device:

Expected content on: GPU compute node
 
 
 NodeName=compute01 Name=gpu Type=nvidia_a100 File=/dev/nvidia[0-3]
 

**"Invalid GRES" error when submitting jobs** Ensure `slurm.conf` on the control node includes the `GresTypes` directive:

Run on: Slurm control node
 
 
 grep GresTypes /etc/slurm/slurm.conf
 

Expected: `GresTypes=gpu`

**ROCm driver fails to install** Verify the ROCm repository was synced successfully:

Run on: omnia_core container
 
 
 curl -s http://localhost:8080/pulp/content/rocm/ | head
 

Back to top [ Previous Build Slurm Repo ](build_slurm_repo.html) [ Next Add Slurm Nodes ](add_slurm_nodes.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
