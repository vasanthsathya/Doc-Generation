
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Use Apptainer 

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
 * Use Apptainer [ Use Apptainer ](use_apptainer.html) Table of contents 
 * [ Overview ](#overview)
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
 3. [ Containers ](use_apptainer.html)

# Use Apptainer[¶](#use-apptainer "Permanent link")

Pull and run containerized HPC applications across Slurm compute nodes using Apptainer (formerly Singularity), with SIF images stored on NFS shared storage.

## Overview[¶](#overview "Permanent link")

Apptainer is the standard container runtime for HPC environments. Unlike Docker, Apptainer:

 * Runs without a daemon or root privileges.
 * Integrates natively with Slurm job scheduling.
 * Supports GPU pass-through (`--nv` for NVIDIA, `--rocm` for AMD).
 * Uses SIF (Singularity Image Format) images that are single-file, read-only, and easily shared via NFS.

The workflow is:

 1. Pull a container image (Docker or SIF format) to shared NFS storage.
 2. Submit Slurm jobs that execute commands inside the container.
 3. All compute nodes access the same SIF image via NFS -- no per-node image installation required.

## Prerequisites[¶](#prerequisites "Permanent link")

 * Apptainer is installed on compute nodes (included via `software_config.json` with `{"name": "apptainer"}`).
 * NFS shared storage is configured (see [Configure Nfs](../Storage/configure_nfs.html)).
 * Slurm is deployed and functional (see [Setup Slurm](../Slurm/setup_slurm.html)).
 * For GPU containers: GPU drivers installed (see [Slurm With Gpu](../Slurm/slurm_with_gpu.html)).

## Procedure[¶](#procedure "Permanent link")

 1. **Verify Apptainer is installed** on compute nodes:

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "apptainer --version"
 

 1. **Create a shared images directory** on NFS:

Run on: Slurm control node or login node
 
 
 mkdir -p /home/containers/images
 chmod 755 /home/containers/images
 

 1. **Pull a Docker image** and convert to SIF:

Run on: Slurm control node or login node
 
 
 apptainer pull /home/containers/images/ubuntu.sif docker://ubuntu:22.04
 

 1. **Pull an HPC application container** :

Run on: Slurm control node or login node
 
 
 # Example: GROMACS molecular dynamics
 apptainer pull /home/containers/images/gromacs.sif docker://nvcr.io/hpc/gromacs:2023.2
 
 # Example: TensorFlow for AI workloads
 apptainer pull /home/containers/images/tensorflow.sif docker://nvcr.io/nvidia/tensorflow:24.01-tf2-py3
 

 1. **Run an interactive container** on a compute node:

Run on: Slurm control node
 
 
 srun -N 1 --pty apptainer shell /home/containers/images/ubuntu.sif
 

This opens an interactive shell inside the container on a compute node.

 1. **Run a batch job** with Apptainer:

Run on: Slurm control node
 
 
 cat <<'EOF' > /home/containers/run_gromacs.sh
 #!/bin/bash
 #SBATCH --job-name=gromacs-test
 #SBATCH --nodes=2
 #SBATCH --ntasks-per-node=4
 #SBATCH --time=02:00:00
 #SBATCH --output=/home/containers/results/gromacs-%j.out
 
 apptainer exec /home/containers/images/gromacs.sif \
 mpirun -np 8 gmx_mpi mdrun -s input.tpr -deffnm output
 EOF
 
 sbatch /home/containers/run_gromacs.sh
 

 1. **Run a GPU container** with Apptainer:

Run on: Slurm control node
 
 
 cat <<'EOF' > /home/containers/run_tensorflow.sh
 #!/bin/bash
 #SBATCH --job-name=tf-test
 #SBATCH --nodes=1
 #SBATCH --gres=gpu:1
 #SBATCH --time=01:00:00
 #SBATCH --output=/home/containers/results/tf-%j.out
 
 apptainer exec --nv /home/containers/images/tensorflow.sif \
 python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
 EOF
 
 sbatch /home/containers/run_tensorflow.sh
 

 1. **Build a custom SIF image** from a definition file:

Run on: Slurm control node
 
 
 cat <<'EOF' > /home/containers/custom.def
 Bootstrap: docker
 From: ubuntu:22.04
 
 %post
 apt-get update
 apt-get install -y python3 python3-pip
 pip3 install numpy scipy
 
 %runscript
 python3 "$@"
 EOF
 
 apptainer build /home/containers/images/custom.sif /home/containers/custom.def
 

## Verification[¶](#verification "Permanent link")

 1. **Verify SIF images are accessible** from all compute nodes:

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "ls -la /home/containers/images/"
 

 1. **Run a quick test** across multiple nodes:

Run on: Slurm control node
 
 
 srun -N 2 apptainer exec /home/containers/images/ubuntu.sif hostname
 

 1. **Verify GPU access** inside containers:

Run on: Slurm control node
 
 
 srun -N 1 --gres=gpu:1 apptainer exec --nv /home/containers/images/tensorflow.sif nvidia-smi
 

 1. **Check job output** :

Run on: Slurm control node
 
 
 cat /home/containers/results/*.out
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Deploy Additional Packages](deploy_additional_packages.html) \-- Install additional packages alongside containers.
 * [Run Hpc Benchmarks](../Slurm/run_hpc_benchmarks.html) \-- Run benchmark containers.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**"apptainer: command not found"** Verify Apptainer is installed:

Run on: compute node
 
 
 dnf install -y apptainer
 

**Pull fails with "permission denied"** \- Ensure the NFS directory has write permissions. \- Apptainer uses `/tmp` for build cache; ensure sufficient space:
 
 
 ```bash title="Run on: compute node"
 df -h /tmp
 export APPTAINER_TMPDIR=/scratch/tmp
 ```
 

**GPU not accessible inside container** \- Use `--nv` for NVIDIA or `--rocm` for AMD GPUs. \- Verify the host GPU driver is compatible with the container's CUDA version.

**SIF image corrupted** Re-pull the image:

Run on: Slurm control node
 
 
 rm /home/containers/images/broken.sif
 apptainer pull /home/containers/images/fixed.sif docker://source-image
 

**MPI inside container fails** Ensure the MPI version inside the container is compatible with the host MPI. Use `--bind` to mount the host MPI libraries:

Run on: Slurm control node
 
 
 srun -N 2 apptainer exec --bind /usr/lib64/openmpi:/host-mpi \
 /home/containers/images/app.sif mpirun -np 8 /app/benchmark
 

Back to top [ Previous External VictoriaMetrics ](../Telemetry/configure_external_victoria.html) [ Next Deploy Additional Packages ](deploy_additional_packages.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
