Step 11: Set up Slurm on nodes
==============

**Prerequisites**

* Provide the Slurm 25.05.2 user repository.
* Fill the mandatory parameters in ``omnia_config.yml``: `Input parameters for the cluster <../schedulerinputparams.html#id13>`_
* Fill the parameters in ``storage_config.yml``: `Input parameters for the cluster <../schedulerinputparams.html#id13>`_
* Add ``slurm_custom`` to ``software_config.json`` and add ``slurm_custom`` subgroups.
* Add ``slurm_custom`` repository URL to ``user_repo_url_x86_64`` or ``user_repo_url_aarch64`` in ``local_repo_config.yml``.


**Setup Slurm:**

1. To download the artifacts required to set up Slurm on the nodes, run the ``local_repo.yml`` playbook.
2. To build diskless images for cluster nodes, run build_image_x86_64.yml or build_image_aarch64.yml: `Build cluster node images <../../build_images.html>`_
3. To discover the potential cluster nodes, configure the boot script, and cloud-init based on the functional groups, run  the ``discovery.yml`` playbook: `Discover cluster nodes <../../Provision/index.html>`_
4. After successfully executing the ``discovery.yml`` playbook, you can PXE boot the slurm node, login node, and login compiler node simultaneously.

.. note:: If you want to deploy only Slurm clusters (``slurm_custom``), the ``idrac_telemetry_support`` parameter must be set to ``false`` in the ``telemetry_config.yml`` file. Omnia is Validated for Slurm version 25.05. If you use any other version, some functionality like PAM may not work.

**Slurm with GPU:**

**Prerequisites**

* You must have the ``user_repo`` which is compiled with nvml and cgroup-v2. If slurm-nodes have GPU then you must provide at least one ``login_compiler_node``.


.. note:: If the iDRAC of a Slurm node is not accessible through OIM—because of issues such as an incorrect iDRAC port configuration or invalid credentials—the node configuration specified in ``/etc/slurm/slurm.conf`` for ``NodeName`` will default to: ``Sockets=1 CoresPerSocket=1 ThreadsPerCore=1 RealMemory=3774873``. Update ``slurm.conf`` with the correct hardware values and run ``scontrol reconfigure`` to apply the changes.


Post Installation
----------------------

A helper script is provided to simplify pulling container images on cluster nodes. By default, the script downloads the hpcbenchmarks container from the site Pulp registry, but it can also be used to pull any other approved images available in Pulp.

1. Verify if required paths exist. ::

    ls -l /hpc_tools/scripts
    ls -ld /hpc_tools/container_images

 The following should be available:
 
 * ``download_container_image.sh``
 * ``container_image.list``

 If missing, NFS is not mounted.

2. Verify if Apptainer is installed. :: 

    apptainer --version

3. Update image list (optional): By default, the list includes the HPC benchmarks image. To retrieve additional images from Pulp, add them to this list. ::

    vi /hpc_tools/scripts/container_image.list

 Format: ::
        
        <registry>/<namespace>/<image>:<tag>

 Example: ::

        docker.io/library/ubuntu:22.04

4. Run the download script. ::

    /hpc_tools/scripts/download_container_image.sh

 The script retrieves images from the Pulp mirror and saves them to ``/hpc_tools/container_images``.

5. Verify the downloaded images. ::

        ls -lh /hpc_tools/container_images
        apptainer inspect /hpc_tools/container_images/<image>.sif

6. Run a container (example). ::

        apptainer exec /hpc_tools/container_images/hpc-benchmarks_25.09.sif --help




    



