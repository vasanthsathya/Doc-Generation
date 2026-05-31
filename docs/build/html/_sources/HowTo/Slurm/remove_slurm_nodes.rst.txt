

Remove Slurm Nodes
==================


Safely remove compute nodes from a running Slurm cluster without disrupting
active workloads.


Overview
--------


Removing a node from a Slurm cluster involves:

#. Draining the node so no new jobs are scheduled on it.
#. Waiting for any running jobs to complete (or canceling them).
#. Removing the node from ``slurm.conf`` on the control node.
#. Stopping Slurm services on the target node.
#. Reconfiguring the Slurm controller.



Prerequisites
-------------


- A working Slurm cluster deployed via :doc:`Setup Slurm <setup_slurm>`.
- ``root`` or ``sudo`` access to the Slurm control node and the target
  compute node(s).
- Identify which node(s) to remove (hostname and IP address).



Procedure
---------


#. **Drain the target node** to prevent new jobs from being scheduled:


**Run on: Slurm control node**

.. code-block:: bash

      scontrol update nodename=<node-to-remove> state=drain reason="Decommissioning"



#. **Verify the node is draining** and check for running jobs:


**Run on: Slurm control node**

.. code-block:: bash

      sinfo -n <node-to-remove>
      squeue -w <node-to-remove>



   Wait for all jobs on the node to complete. If immediate removal is needed,
   cancel running jobs:


**Run on: Slurm control node**

.. code-block:: bash

      # Cancel all jobs on the target node
      scancel -w <node-to-remove>



#. **Set the node to down**:


**Run on: Slurm control node**

.. code-block:: bash

      scontrol update nodename=<node-to-remove> state=down reason="Removed from cluster"



#. **Stop Slurm services on the target node**:


**Run on: node being removed**

.. code-block:: bash

      systemctl stop slurmd
      systemctl disable slurmd
      systemctl stop munge
      systemctl disable munge



#. **Remove the node from slurm.conf** on the control node:


**Run on: Slurm control node**

.. code-block:: bash

      vi /etc/slurm/slurm.conf



   Remove or comment out the ``NodeName=`` line for the target node. Also
   update the ``PartitionName=`` line to remove the node from the ``Nodes=``
   list.

#. **Reconfigure Slurm** to apply changes:


**Run on: Slurm control node**

.. code-block:: bash

      scontrol reconfigure



#. **(Optional) Remove the node from the mapping file**:


**Run on: omnia_core container**

.. code-block:: bash

      vi /opt/omnia/input/project_default/pxe_mapping_file.csv



   Remove or comment out the row for the decommissioned node.



Verification
------------


#. **Confirm the node is no longer in the cluster**:


**Run on: Slurm control node**

.. code-block:: bash

      sinfo
      scontrol show nodes



   The removed node should no longer appear.

#. **Run a test job** to confirm remaining nodes are functional:


**Run on: Slurm control node**

.. code-block:: bash

      srun -N 1 hostname



#. **Verify no orphaned jobs** reference the removed node:


**Run on: Slurm control node**

.. code-block:: bash

      squeue -t all





Next Steps
----------


- :doc:`Add Slurm Nodes <add_slurm_nodes>` -- Add replacement nodes if needed.
- :doc:`Slurm Config Backup <slurm_config_backup>` -- Back up the updated Slurm configuration.



Troubleshooting
---------------


**Node still appears in sinfo after removal**
   Ensure you ran ``scontrol reconfigure`` after editing ``slurm.conf``:


**Run on: Slurm control node**

.. code-block:: bash

      scontrol reconfigure



**Jobs were running on the removed node**
   If jobs were not properly drained, they may show as ``FAILED`` or
   ``NODE_FAIL`` in the accounting:


**Run on: Slurm control node**

.. code-block:: bash

      sacct --starttime=today --state=FAILED,NODE_FAIL



   Resubmit affected jobs as needed.

**slurm.conf syntax error after editing**
   Validate the configuration:


**Run on: Slurm control node**

.. code-block:: bash

      slurmd -C  # Show computed node configuration
      slurmctld -t  # Test configuration file syntax



**Cannot connect to the removed node to stop services**
   If the node is unreachable, the Slurm controller will time it out
   automatically. Simply remove it from ``slurm.conf`` and reconfigure.
