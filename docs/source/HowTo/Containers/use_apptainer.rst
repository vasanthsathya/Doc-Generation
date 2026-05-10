

Use Apptainer
=============


Pull and run containerized HPC applications across Slurm compute nodes using
Apptainer (formerly Singularity), with SIF images stored on NFS shared
storage.


Overview
--------


Apptainer is the standard container runtime for HPC environments. Unlike
Docker, Apptainer:

- Runs without a daemon or root privileges.
- Integrates natively with Slurm job scheduling.
- Supports GPU pass-through (``--nv`` for NVIDIA, ``--rocm`` for AMD).
- Uses SIF (Singularity Image Format) images that are single-file,
  read-only, and easily shared via NFS.

The workflow is:

#. Pull a container image (Docker or SIF format) to shared NFS storage.
#. Submit Slurm jobs that execute commands inside the container.
#. All compute nodes access the same SIF image via NFS -- no per-node
   image installation required.



Prerequisites
-------------


- Apptainer is installed on compute nodes (included via
  ``software_config.json`` with ``{"name": "apptainer"}``).
- NFS shared storage is configured (see `Configure Nfs <../Storage/configure_nfs.rst>`_).
- Slurm is deployed and functional (see `Setup Slurm <../Slurm/setup_slurm.rst>`_).
- For GPU containers: GPU drivers installed (see
  `Slurm With Gpu <../Slurm/slurm_with_gpu.rst>`_).



Procedure
---------


#. **Verify Apptainer is installed** on compute nodes:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m shell -a "apptainer --version"



#. **Create a shared images directory** on NFS:


**Run on: Slurm control node or login node**

.. code-block:: bash
      mkdir -p /home/containers/images
      chmod 755 /home/containers/images



#. **Pull a Docker image** and convert to SIF:


**Run on: Slurm control node or login node**

.. code-block:: bash
      apptainer pull /home/containers/images/ubuntu.sif docker://ubuntu:22.04



#. **Pull an HPC application container**:


**Run on: Slurm control node or login node**

.. code-block:: bash
      # Example: GROMACS molecular dynamics
      apptainer pull /home/containers/images/gromacs.sif docker://nvcr.io/hpc/gromacs:2023.2
   
      # Example: TensorFlow for AI workloads
      apptainer pull /home/containers/images/tensorflow.sif docker://nvcr.io/nvidia/tensorflow:24.01-tf2-py3



#. **Run an interactive container** on a compute node:


**Run on: Slurm control node**

.. code-block:: bash
      srun -N 1 --pty apptainer shell /home/containers/images/ubuntu.sif



   This opens an interactive shell inside the container on a compute node.

#. **Run a batch job** with Apptainer:


**Run on: Slurm control node**

.. code-block:: bash
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



#. **Run a GPU container** with Apptainer:


**Run on: Slurm control node**

.. code-block:: bash
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



#. **Build a custom SIF image** from a definition file:


**Run on: Slurm control node**

.. code-block:: bash
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





Verification
------------


#. **Verify SIF images are accessible** from all compute nodes:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m shell -a "ls -la /home/containers/images/"



#. **Run a quick test** across multiple nodes:


**Run on: Slurm control node**

.. code-block:: bash
      srun -N 2 apptainer exec /home/containers/images/ubuntu.sif hostname



#. **Verify GPU access** inside containers:


**Run on: Slurm control node**

.. code-block:: bash
      srun -N 1 --gres=gpu:1 apptainer exec --nv /home/containers/images/tensorflow.sif nvidia-smi



#. **Check job output**:


**Run on: Slurm control node**

.. code-block:: bash
      cat /home/containers/results/*.out





Next Steps
----------


- `Deploy Additional Packages <deploy_additional_packages.rst>`_ -- Install additional packages alongside
  containers.
- `Run Hpc Benchmarks <../Slurm/run_hpc_benchmarks.rst>`_ -- Run benchmark containers.



Troubleshooting
---------------


**"apptainer: command not found"**
   Verify Apptainer is installed:


**Run on: compute node**

.. code-block:: bash
      dnf install -y apptainer



**Pull fails with "permission denied"**
  - Ensure the NFS directory has write permissions.
  - Apptainer uses ``/tmp`` for build cache; ensure sufficient space:


**Run on: compute node**

.. code-block:: bash
        df -h /tmp
        export APPTAINER_TMPDIR=/scratch/tmp



**GPU not accessible inside container**
  - Use ``--nv`` for NVIDIA or ``--rocm`` for AMD GPUs.
  - Verify the host GPU driver is compatible with the container's CUDA
     version.

**SIF image corrupted**
   Re-pull the image:


**Run on: Slurm control node**

.. code-block:: bash
      rm /home/containers/images/broken.sif
      apptainer pull /home/containers/images/fixed.sif docker://source-image



**MPI inside container fails**
   Ensure the MPI version inside the container is compatible with the host
   MPI. Use ``--bind`` to mount the host MPI libraries:


**Run on: Slurm control node**

.. code-block:: bash
      srun -N 2 apptainer exec --bind /usr/lib64/openmpi:/host-mpi \
        /home/containers/images/app.sif mpirun -np 8 /app/benchmark

