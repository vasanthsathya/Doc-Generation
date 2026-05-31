

Add Slurm Nodes
===============


Dynamically add new compute nodes to a running Slurm cluster without
disrupting existing workloads.


Overview
--------


Omnia supports dynamic node addition to expand a running Slurm cluster. The
process involves:

#. Provisioning the new server(s) using the standard Omnia workflow.
#. Adding the new node(s) to the mapping file.
#. Running the add-node playbook to configure Slurm on the new nodes and
   update the controller's ``slurm.conf``.



Prerequisites
-------------


- A working Slurm cluster deployed via :doc:`Setup Slurm <setup_slurm>`.
- New server(s) are physically racked, cabled, and have BMC connectivity.
- The new server(s) have been provisioned and are reachable on the admin
  network.
- New node entries have been added to the ``pxe_mapping_file.csv``.



Procedure
---------


#. **Update the mapping file** with new node entries:


**Run on: omnia_core container**

.. code-block:: bash

      vi /opt/omnia/input/project_default/pxe_mapping_file.csv



   Add new rows for each new compute node:


**File: /opt/omnia/input/project_default/pxe_mapping_file.csv**

.. code-block:: text

      slurm_node,slurm_cluster,NEWSVCTG1,,,aa:bb:cc:dd:ee:10,10.5.0.110,aa:bb:cc:dd:ff:10,10.3.0.110
      slurm_node,slurm_cluster,NEWSVCTG2,,,aa:bb:cc:dd:ee:11,10.5.0.111,aa:bb:cc:dd:ff:11,10.3.0.111



#. **Provision the new nodes** if not already provisioned:


**Run on: omnia_core container**

.. code-block:: bash

      cd /omnia/discovery
      ansible-playbook discovery.yml --ask-vault-pass



#. **Run the add-node playbook**:


**Run on: omnia_core container**

.. code-block:: bash

      cd /omnia
      ansible-playbook omnia.yml --ask-vault-pass --limit "new_nodes"



   !!! note

       If a dedicated ``add_node.yml`` playbook is available in your Omnia
       version, use it instead:


**Run on: omnia_core container**

.. code-block:: bash

          ansible-playbook utils/add_node.yml --ask-vault-pass \
            -e "target_nodes=10.5.0.110,10.5.0.111"



#. **Update the Slurm configuration** on the control node to include the new
   nodes:


**Run on: Slurm control node**

.. code-block:: bash

      # Reconfigure Slurm to pick up new nodes
      scontrol reconfigure





Verification
------------


#. **Check that new nodes appear in the cluster**:


**Run on: Slurm control node**

.. code-block:: bash

      sinfo



   New nodes should appear in the ``normal`` partition with ``idle`` state.

#. **Run a test job on the new nodes**:


**Run on: Slurm control node**

.. code-block:: bash

      srun -w <new-node-hostname> hostname



#. **Verify Munge authentication** on the new nodes:


**Run on: Slurm control node**

.. code-block:: bash

      munge -n | ssh <new-node-ip> unmunge



#. **Check slurmd is running** on the new nodes:


**Run on: new compute node**

.. code-block:: bash

      systemctl status slurmd





Next Steps
----------


- :doc:`Slurm With Gpu <slurm_with_gpu>` -- Configure GPU support on the new nodes if they have
  GPUs.
- :doc:`Configure Nfs <../Storage/configure_nfs>` -- Mount shared storage on new nodes.
- :doc:`Setup Openldap <../Authentication/setup_openldap>` -- Ensure LDAP clients are
  configured on new nodes.



Troubleshooting
---------------


**New nodes show "down" in sinfo**
  - Verify ``slurmd`` is running:


**Run on: new compute node**

.. code-block:: bash

        systemctl status slurmd
        journalctl -u slurmd --no-pager -n 20



  - Check that ``slurm.conf`` on the new node matches the control node's
     version:


**Run on: new compute node**

.. code-block:: bash

        grep "SlurmctldHost" /etc/slurm/slurm.conf



  - Resume the node from the controller:


**Run on: Slurm control node**

.. code-block:: bash

        scontrol update nodename=<node> state=resume reason="added"



**Munge key mismatch**
   Re-distribute the Munge key from the control node:


**Run on: omnia_core container**

.. code-block:: bash

      ansible new_nodes -m copy -a "src=/etc/munge/munge.key dest=/etc/munge/munge.key owner=munge group=munge mode=0400"
      ansible new_nodes -m service -a "name=munge state=restarted"



**New nodes not in Ansible inventory**
   Re-run discovery or manually add the nodes to the Ansible inventory:


**Run on: omnia_core container**

.. code-block:: bash

      ochami node list

