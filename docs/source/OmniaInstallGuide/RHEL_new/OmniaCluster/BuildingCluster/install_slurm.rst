Step 11: Set up Slurm on nodes
==============

**Prerequisites**

* Provide the Slurm 25.05.2 user repository.
.. note:: If any Slurm nodes (Slurm controller, compute nodes, login nodes, or login/compile nodes) have an InfiniBand interface and ``ib_network`` details are defined in network_spec.yml (`Update the Input Parameters for Discovering the Nodes <../../Provision/provisionparams.html>`_), the Slurm user repository must be built without UCX support.
        Specifically: 

        * The Slurm user repository **must NOT include** the following packages: ucx, ucx-devel, openmpi, openmpi-devel.

        * Slurm itself must be compiled without UCX support.

        After running ``discovery.yml`` and PXE-booting the nodes, DOCA-OFED is installed on nodes that have Mellanox InfiniBand cards. A static IP is assigned to the InfiniBand interface only if the interface is up. If the interface is down, the user must bring it up to enable IP assignment.
        
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