

Run HPC Benchmarks
==================


Pull and run HPC benchmark containers across Slurm compute nodes using
Apptainer (formerly Singularity) to validate cluster performance.


Overview
--------


Running HPC benchmarks on a newly deployed cluster validates:

- Network fabric performance (latency, bandwidth)
- Compute throughput (FLOPS, memory bandwidth)
- GPU functionality and driver correctness
- MPI communication across nodes

This guide shows how to pull benchmark container images (SIF format) and submit
them as Slurm jobs using Apptainer.



Prerequisites
-------------


- Slurm is deployed and operational (see `Setup Slurm <setup_slurm.rst>`_).
- Apptainer is installed on compute nodes (included in ``software_config.json``
  with ``{"name": "apptainer"}``).
- NFS shared storage is available at ``/home`` or a dedicated benchmark
  directory (see `Configure Nfs <../Storage/configure_nfs.rst>`_).
- For GPU benchmarks: GPU drivers are installed (see `Slurm With Gpu <slurm_with_gpu.rst>`_).



Procedure
---------


#. **SSH to the Slurm login or control node**:


**Run on: omnia_core container**

.. code-block:: bash
      ssh root@<slurm-control-node-ip>



#. **Create a directory for benchmark images** on shared storage:


**Run on: Slurm control node**

.. code-block:: bash
      mkdir -p /home/benchmarks/images
      mkdir -p /home/benchmarks/results
      cd /home/benchmarks



#. **Pull the HPL (High Performance Linpack) benchmark container**:


**Run on: Slurm control node**

.. code-block:: bash
      apptainer pull images/hpl.sif docker://nvcr.io/nvidia/hpc-benchmarks:24.03



   !!! note

       For non-GPU clusters, use the standard HPL benchmark:


**Run on: Slurm control node**

.. code-block:: bash
          apptainer pull images/hpl-cpu.sif docker://ghcr.io/hpc-benchmarks/hpl:latest



#. **Pull the OSU Micro-Benchmarks container** for MPI testing:


**Run on: Slurm control node**

.. code-block:: bash
      apptainer pull images/osu-benchmarks.sif docker://ghcr.io/osu-benchmarks/osu-micro-benchmarks:latest



#. **Run the HPL benchmark** as a Slurm job:


**Run on: Slurm control node**

.. code-block:: bash
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



#. **Run GPU benchmarks** (NVIDIA):


**Run on: Slurm control node**

.. code-block:: bash
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



#. **Run OSU MPI latency benchmark**:


**Run on: Slurm control node**

.. code-block:: bash
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



#. **Monitor benchmark job status**:


**Run on: Slurm control node**

.. code-block:: bash
      squeue
      # Wait for completion, then check results
      ls -la /home/benchmarks/results/





Verification
------------


#. **Check benchmark job completed successfully**:


**Run on: Slurm control node**

.. code-block:: bash
      sacct --starttime=today --format=JobName,State,Elapsed,ExitCode



   All benchmark jobs should show ``COMPLETED`` state with exit code ``0:0``.

#. **Review HPL results**:


**Run on: Slurm control node**

.. code-block:: bash
      cat /home/benchmarks/results/hpl-*.out | grep -A5 "T/V"



#. **Review OSU latency results**:


**Run on: Slurm control node**

.. code-block:: bash
      cat /home/benchmarks/results/osu-latency-*.out



   Typical InfiniBand latency should be < 5 microseconds. Ethernet latency
   is typically 20-50 microseconds.



Next Steps
----------


- `Use Apptainer <../Containers/use_apptainer.rst>`_ -- Learn more about using Apptainer
  containers in your cluster.
- `Configure Infiniband <../Networking/configure_infiniband.rst>`_ -- Optimize network performance
  for HPC workloads.



Troubleshooting
---------------


**Apptainer pull fails with "permission denied"**
   Ensure the shared storage directory has correct permissions:


**Run on: Slurm control node**

.. code-block:: bash
      chmod 755 /home/benchmarks
      chown -R root:root /home/benchmarks



**Container fails to execute MPI**
   Verify MPI is installed on the host and accessible inside the container:


**Run on: Slurm compute node**

.. code-block:: bash
      which mpirun
      apptainer exec /home/benchmarks/images/hpl.sif which mpirun



**GPU not accessible inside container**
   Use the ``--nv`` flag with Apptainer for NVIDIA GPU access:


**Run on: Slurm compute node**

.. code-block:: bash
      apptainer exec --nv /home/benchmarks/images/hpl.sif nvidia-smi



**HPL gives poor performance numbers**
  - Verify the number of MPI ranks matches available cores.
  - Tune the HPL.dat input file for your problem size and node count.
  - Ensure memory is not oversubscribed.

**Job fails with "out of memory"**
   Reduce the problem size or request more nodes:


**Run on: Slurm control node**

.. code-block:: bash
      #SBATCH --mem=0  # Use all available memory on the node

