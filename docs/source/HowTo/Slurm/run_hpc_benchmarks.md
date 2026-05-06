# Run HPC Benchmarks

Pull and run HPC benchmark containers across Slurm compute nodes using Apptainer (formerly Singularity) to validate cluster performance.

## Overview

Running HPC benchmarks on a newly deployed cluster validates:

 * Network fabric performance (latency, bandwidth)
 * Compute throughput (FLOPS, memory bandwidth)
 * GPU functionality and driver correctness
 * MPI communication across nodes

This guide shows how to pull benchmark container images (SIF format) and submit them as Slurm jobs using Apptainer.

## Prerequisites

 * Apptainer is installed on compute nodes (included in `software_config.json` with `{"name": "apptainer"}`).

## Procedure

 1. **SSH to the Slurm login or control node** :

Run on: omnia_core container

 ssh root@<slurm-control-node-ip>

 1. **Create a directory for benchmark images** on shared storage:

Run on: Slurm control node

 mkdir -p /home/benchmarks/images
 mkdir -p /home/benchmarks/results
 cd /home/benchmarks

 1. **Pull the HPL (High Performance Linpack) benchmark container** :

Run on: Slurm control node

 apptainer pull images/hpl.sif docker://nvcr.io/nvidia/hpc-benchmarks:24.03

!!! note

 For non-GPU clusters, use the standard HPL benchmark:

 ```bash title="Run on: Slurm control node"
 apptainer pull images/hpl-cpu.sif docker://ghcr.io/hpc-benchmarks/hpl:latest
 ```

 1. **Pull the OSU Micro-Benchmarks container** for MPI testing:

Run on: Slurm control node

 apptainer pull images/osu-benchmarks.sif docker://ghcr.io/osu-benchmarks/osu-micro-benchmarks:latest

 1. **Run the HPL benchmark** as a Slurm job:

Run on: Slurm control node

 cat <<'EOF' > /home/benchmarks/run_hpl.sh
 #!/bin/bash
 #SBATCH --job-name=hpl-benchmark
 #SBATCH --nodes=2
 #SBATCH --ntasks-per-node=4
 #SBATCH --time=01:00:00
 #SBATCH --output=results/hpl-%j.out

 cd /home/benchmarks
 apptainer exec images/hpl.sif mpirun -np 8 /usr/local/bin/xhpl
 EOF

 sbatch /home/benchmarks/run_hpl.sh

 1. **Run GPU benchmarks** (NVIDIA):

Run on: Slurm control node

 cat <<'EOF' > /home/benchmarks/run_gpu_bench.sh
 #!/bin/bash
 #SBATCH --job-name=gpu-benchmark
 #SBATCH --nodes=1
 #SBATCH --gres=gpu:1
 #SBATCH --time=00:30:00
 #SBATCH --output=results/gpu-%j.out

 cd /home/benchmarks
 apptainer exec --nv images/hpl.sif nvidia-smi
 apptainer exec --nv images/hpl.sif /usr/local/bin/cuda_bandwidthTest
 EOF

 sbatch /home/benchmarks/run_gpu_bench.sh

 1. **Run OSU MPI latency benchmark** :

Run on: Slurm control node

 cat <<'EOF' > /home/benchmarks/run_osu_latency.sh
 #!/bin/bash
 #SBATCH --job-name=osu-latency
 #SBATCH --nodes=2
 #SBATCH --ntasks-per-node=1
 #SBATCH --time=00:10:00
 #SBATCH --output=results/osu-latency-%j.out

 cd /home/benchmarks
 apptainer exec images/osu-benchmarks.sif mpirun -np 2 /usr/local/bin/osu_latency
 EOF

 sbatch /home/benchmarks/run_osu_latency.sh

 1. **Monitor benchmark job status** :

Run on: Slurm control node

 squeue
 # Wait for completion, then check results
 ls -la /home/benchmarks/results/

## Verification

 1. **Check benchmark job completed successfully** :

Run on: Slurm control node

 sacct --starttime=today --format=JobName,State,Elapsed,ExitCode

All benchmark jobs should show `COMPLETED` state with exit code `0:0`.

 1. **Review HPL results** :

Run on: Slurm control node

 cat /home/benchmarks/results/hpl-*.out | grep -A5 "T/V"

 1. **Review OSU latency results** :

Run on: Slurm control node

 cat /home/benchmarks/results/osu-latency-*.out

Typical InfiniBand latency should be < 5 microseconds. Ethernet latency is typically 20-50 microseconds.

## Next Steps

## Troubleshooting

**Apptainer pull fails with "permission denied"** Ensure the shared storage directory has correct permissions:

Run on: Slurm control node

 chmod 755 /home/benchmarks
 chown -R root:root /home/benchmarks

**Container fails to execute MPI** Verify MPI is installed on the host and accessible inside the container:

Run on: Slurm compute node

 which mpirun
 apptainer exec /home/benchmarks/images/hpl.sif which mpirun

**GPU not accessible inside container** Use the `--nv` flag with Apptainer for NVIDIA GPU access:

Run on: Slurm compute node

 apptainer exec --nv /home/benchmarks/images/hpl.sif nvidia-smi

**HPL gives poor performance numbers** \- Verify the number of MPI ranks matches available cores. \- Tune the HPL.dat input file for your problem size and node count. \- Ensure memory is not oversubscribed.

**Job fails with "out of memory"** Reduce the problem size or request more nodes:

Run on: Slurm control node

 #SBATCH --mem=0 # Use all available memory on the node

Copyright © 2025 Dell Technologies. All rights reserved.