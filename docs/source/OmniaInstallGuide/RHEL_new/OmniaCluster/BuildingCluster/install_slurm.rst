Step 10: Set up Slurm on nodes
==============

**Prerequisites**

* Fill the mandatory parameters in ``omnia_config.yml``: `Input parameters for the cluster <../schedulerinputparams.html#id13>`_
* Fill the parameters in ``storage_config.yml``: `Input parameters for the cluster <../schedulerinputparams.html#id13>`_
* Add ``slurm_custom`` to ``software_config.json`` and add ``slurm_custom`` subgroups.
* Add ``slurm_custom`` repository URL to ``user_repo_url_x86_64`` or ``user_repo_url_aarch64`` in ``local_repo_config.yml``.


**Setup Slurm:**

1. To download the artifacts required to set up Slurm on the nodes, run the ``local_repo.yml`` playbook.
2. Provide the slurm cluster information in the ``functional_groups_config.yml``: `Create groups and assign functional roles to the nodes <../../composable_roles.html>`_
3. To build diskless images for cluster nodes, run the ``build.image.yml`` playbook: `Build cluster node images <../../build_images.html>`_
4. To discover the potential cluster nodes, configure the boot script, and cloud-init based on the functional groups, run  the ``discovery.yml`` playbook: `Discover cluster nodes <../../Provision/index.html>`_

After booting the nodes, verify the following to ensure slurm is deployed successfully: 
On slurm controller node
    * Verify if the required services are running. Run the following commands and confirm that each service is active (running):
    
    ::
          systemctl status munge
          systemctl status slurmctld
          systemctl status slurmdbd
          systemctl status mariadb

    * Verify the node status with sinfo:
   
        * Ensure that the worker nodes are listed and the node state should be idle.


**PAM Feature for Slurm**

Slurm PAM restricts SSH access to compute nodes for non-root users. You can log in only while their job is actively running on the node. After the job is completed, you are is automatically logged out.  

On login node: Switch to the LDAP user:
::
      ssh <ldap_user>@<login_node_hostname>
      Run the job

While the job is running, ssh as ``<ldap_user>`` to the slurm node where the job is running. After the job is completed, ``<ldap_user>`` is logged out.
