

Slurm with GPUs
===============


Configure GPU-enabled Slurm compute nodes with automatic driver installation
for NVIDIA (CUDA), AMD (ROCm), and Intel Gaudi accelerators.


Overview
--------


Omnia automatically detects GPU hardware on compute nodes and installs the
appropriate drivers and runtime libraries:

- **NVIDIA GPUs** -- CUDA toolkit and NVIDIA driver via the local CUDA
  repository.
- **AMD GPUs** -- ROCm runtime and driver.
- **Intel Gaudi** -- Habana Labs driver and runtime.

Slurm is configured with **GRES (Generic RESource)** definitions so jobs can
request specific GPU types and quantities.



Prerequisites
-------------


- Compute nodes with GPUs are provisioned and in the Slurm cluster.
- The ``software_config.json`` includes the GPU software stack:


**File: /opt/omnia/input/project_default/software_config.json**

.. code-block:: json
     {
         "softwares": [
             {"name": "slurm"},
             {"name": "cuda", "version": "12.2"},
             {"name": "rocm", "version": "6.0"}
         ]
     }



- Local repositories are synced with GPU packages (see
  `Create Local Repos <../Setup/create_local_repos.rst>`_).
- GPU nodes are assigned to the ``slurm_node`` functional group in the
  mapping file.



Procedure
---------


#. **Enter the omnia_core container**:


**Run on: OIM host**

.. code-block:: bash
      ssh omnia_core



#. **Verify GPU software is listed in software_config.json**:


**Run on: omnia_core container**

.. code-block:: bash
      cat /opt/omnia/input/project_default/software_config.json | python3 -m json.tool



#. **Configure GPU-related parameters in omnia_config.yml**:


**Run on: omnia_core container**

.. code-block:: bash
      vi /opt/omnia/input/project_default/omnia_config.yml



   GPU-related parameters:


**File: /opt/omnia/input/project_default/omnia_config.yml**

.. code-block:: yaml
      ---
      # GPU configuration
      cuda_toolkit_path: "/usr/local/cuda"
      rocm_install_path: "/opt/rocm"
   
      # Slurm GRES configuration (auto-detected if left empty)
      slurm_gres_config: ""



#. **Run the omnia.yml playbook** (or re-run if Slurm is already deployed):


**Run on: omnia_core container**

.. code-block:: bash
      cd /omnia
      ansible-playbook omnia.yml --ask-vault-pass



   The playbook will:

  - Detect GPU hardware on each compute node.
  - Install CUDA, ROCm, or Gaudi drivers as appropriate.
  - Generate ``gres.conf`` with GPU device mappings.
  - Update ``slurm.conf`` with GRES definitions.
  - Restart Slurm services to apply changes.

#. **Reconfigure Slurm** to load GRES definitions:


**Run on: Slurm control node**

.. code-block:: bash
      scontrol reconfigure





Verification
------------


#. **Verify GPU drivers are installed** on a compute node:

   For NVIDIA:


**Run on: GPU compute node**

.. code-block:: bash
      nvidia-smi



   Expected output shows GPU model, driver version, and memory usage.

   For AMD:


**Run on: GPU compute node**

.. code-block:: bash
      rocm-smi



   For Intel Gaudi:


**Run on: GPU compute node**

.. code-block:: bash
      hl-smi



#. **Check Slurm GRES configuration**:


**Run on: Slurm control node**

.. code-block:: bash
      scontrol show nodes | grep -i gres



   Expected output:


**Expected output on: Slurm control node**

.. code-block:: text
      Gres=gpu:nvidia_a100:4
      GresUsed=gpu:nvidia_a100:0



#. **Submit a GPU job**:


**Run on: Slurm control node**

.. code-block:: bash
      srun --gres=gpu:1 nvidia-smi



#. **Submit a multi-GPU batch job**:


**Run on: Slurm control node**

.. code-block:: bash
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



#. **Verify CUDA toolkit** (NVIDIA):


**Run on: GPU compute node**

.. code-block:: bash
      nvcc --version
      ls /usr/local/cuda/





Next Steps
----------


- `Run Hpc Benchmarks <run_hpc_benchmarks.rst>`_ -- Run GPU-accelerated benchmarks.
- `Use Apptainer <../Containers/use_apptainer.rst>`_ -- Run GPU containers with Apptainer.



Troubleshooting
---------------


**nvidia-smi reports "no devices found"**
  - Verify the GPU is physically seated and powered.
  - Check that the NVIDIA driver module is loaded:


**Run on: GPU compute node**

.. code-block:: bash
        lsmod | grep nvidia
        dmesg | grep -i nvidia



  - Reinstall the driver:


**Run on: GPU compute node**

.. code-block:: bash
        dnf reinstall nvidia-driver cuda-toolkit



**GRES not showing in scontrol**
   Check ``gres.conf`` on the compute node:


**Run on: GPU compute node**

.. code-block:: bash
      cat /etc/slurm/gres.conf



   The file should list each GPU device:


**Expected content on: GPU compute node**

.. code-block:: text
      NodeName=compute01 Name=gpu Type=nvidia_a100 File=/dev/nvidia[0-3]



**"Invalid GRES" error when submitting jobs**
   Ensure ``slurm.conf`` on the control node includes the ``GresTypes``
   directive:


**Run on: Slurm control node**

.. code-block:: bash
      grep GresTypes /etc/slurm/slurm.conf



   Expected: ``GresTypes=gpu``

**ROCm driver fails to install**
   Verify the ROCm repository was synced successfully:


**Run on: omnia_core container**

.. code-block:: bash
      curl -s http://localhost:8080/pulp/content/rocm/ | head

