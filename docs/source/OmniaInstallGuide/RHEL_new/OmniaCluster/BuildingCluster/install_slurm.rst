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
2. To build diskless images for cluster nodes, run the ``build.image.yml`` playbook: `Build cluster node images <../../build_images.html>`_
3. To discover the potential cluster nodes, configure the boot script, and cloud-init based on the functional groups, run  the ``discovery.yml`` playbook: `Discover cluster nodes <../../Provision/index.html>`_
4. After successfully executing the ``discovery.yml`` playbook, PXE boot the nodes in the following sequence:

   1. Boot the  **slurm controller node** first, before booting any other nodes in the cluster.
   2. Once the **slurm controller node** is up and running, you may simultaneously boot the **slurm nodes**, **login** and **login compiler** nodes.


**Slurm with GPU:**

**Prerequisites**

* You must have the ``user_repo`` which is compiled with nvml and cgroup-v2. If slum-nodes have GPU then you must provide atleast one ``login_compiler_node``.


