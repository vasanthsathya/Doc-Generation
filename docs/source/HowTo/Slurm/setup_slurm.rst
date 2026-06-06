

Setup Slurm
===========


Deploy the Slurm workload manager across your provisioned cluster using the
``omnia.yml`` playbook. This configures a Slurm controller, compute nodes,
and optional login nodes for HPC job scheduling.


Overview
--------


The ``omnia.yml`` playbook deploys and configures Slurm across nodes defined
in your mapping file. It performs the following:

#. Installs Slurm packages (``slurmctld``, ``slurmd``, ``munge``) from local
   repositories.
#. Generates ``slurm.conf`` based on discovered hardware (CPUs, memory, GPUs).
#. Configures Munge authentication across all Slurm nodes.
#. Sets up MariaDB for Slurm accounting.
#. Starts and enables Slurm services on all nodes.






Prerequisites
-------------


- Nodes are provisioned and reachable (see :doc:`Verify Cluster <../Setup/verify_cluster>`).
- The ``omnia_config.yml`` input file is configured with Slurm parameters.
- The ``pxe_mapping_file.csv`` has nodes assigned to ``slurm_control_node``
  and ``slurm_node`` functional groups.
- Local repositories are synced (see :doc:`Create Local Repos <../Setup/create_local_repos>`).
- Encrypted credentials are configured (see
  :doc:`Configure Credentials <../Setup/configure_credentials>`).



Procedure
---------


1. Enter the omnia_core container:

.. code-block:: bash
   :caption: Run on: OIM host

   ssh omnia_core



2. Review and edit omnia_config.yml:

.. code-block:: bash
   :caption: Run on: omnia_core container

   vi /opt/omnia/input/project_default/omnia_config.yml



   Key Slurm-related parameters:


.. code-block:: yaml
   :caption: File: /opt/omnia/input/project_default/omnia_config.yml

   ---
   # Slurm configuration
   slurm_installation_type: "nfs_share"
   enable_omnia_nfs: true

   # MariaDB for Slurm accounting
   mariadb_password: ""  # Set via credentials utility

   # Optional: Slurm partitions
   slurm_partition_name: "normal"
   slurm_default_partition: true



3. Run the omnia.yml playbook:

.. code-block:: bash
   :caption: Run on: omnia_core container

   cd /omnia
   ansible-playbook omnia.yml --ask-vault-pass



   The playbook will:

  - Install Slurm packages on all designated nodes.
  - Generate and distribute ``slurm.conf``.
  - Configure and start Munge on all Slurm nodes.
  - Set up MariaDB for accounting on the control node.
  - Start ``slurmctld`` on the control node.
  - Start ``slurmd`` on all compute nodes.


   Execution time: **20-40 minutes** depending on cluster size.

4. Monitor playbook progress. Watch for successful completion of each
   role:

  - ``slurm/common`` -- Package installation on all nodes
  - ``slurm/control`` -- Controller daemon setup
  - ``slurm/compute`` -- Compute daemon setup
  - ``slurm/login`` -- Login node configuration (if applicable)






Verification
------------


1. Check Slurm controller status:

.. code-block:: bash
   :caption: Run on: Slurm control node

   systemctl status slurmctld

2. Check compute daemon status on a compute node:

.. code-block:: bash
   :caption: Run on: Slurm compute node

   systemctl status slurmd

3. View the cluster partition and node status:

.. code-block:: bash
   :caption: Run on: Slurm control node

   sinfo

Expected output:

.. code-block:: text
   :caption: Expected output on: Slurm control node

   PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
   normal*      up   infinite      2   idle compute[01-02]

4. Run a test job:

.. code-block:: bash
   :caption: Run on: Slurm control node

   srun -N 2 hostname



5. Verify Munge authentication:

.. code-block:: bash
   :caption: Run on: Slurm control node

   munge -n | ssh <compute-node> unmunge

Expected: successful decode with no errors.

6. Check Slurm accounting:

.. code-block:: bash
   :caption: Run on: Slurm control node

   sacctmgr show cluster





Next Steps
----------


- :doc:`Add Slurm Nodes <add_slurm_nodes>` -- Add more compute nodes to the cluster.
- :doc:`Slurm With Gpu <slurm_with_gpu>` -- Configure GPU support.
- :doc:`Configure Nfs <../Storage/configure_nfs>` -- Set up shared NFS storage.
- :doc:`Setup Openldap <../Authentication/setup_openldap>` -- Configure user authentication.






Troubleshooting
---------------


**slurmctld fails to start**
Check the Slurm controller log:

.. code-block:: bash
   :caption: Run on: Slurm control node

   journalctl -u slurmctld --no-pager -n 50
   cat /var/log/slurm/slurmctld.log



**Compute nodes show "down" in sinfo**
- Verify ``slurmd`` is running on the affected node:

.. code-block:: bash
   :caption: Run on: affected compute node

   systemctl status slurmd
   journalctl -u slurmd --no-pager -n 20

- Check Munge is running:

.. code-block:: bash
   :caption: Run on: affected compute node

   systemctl status munge

- Resume the node:

.. code-block:: bash
   :caption: Run on: Slurm control node

   scontrol update nodename=<node> state=resume



**Munge authentication failure**
Ensure the Munge key is identical on all nodes:

.. code-block:: bash
   :caption: Run on: omnia_core container

   ansible slurm_cluster -m shell -a "md5sum /etc/munge/munge.key"

All nodes should report the same MD5 hash.

**MariaDB connection error**
Check MariaDB is running on the control node:

.. code-block:: bash
   :caption: Run on: Slurm control node

   systemctl status mariadb
   mysql -u slurm -p -e "SHOW DATABASES;"

