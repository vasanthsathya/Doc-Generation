

Verify Cluster
==============


Perform end-to-end verification of your provisioned cluster, including Slurm
job scheduling, Kubernetes services, and basic node health checks.


Overview
--------


After provisioning and configuring your cluster, verify that:

#. All nodes are reachable and report the expected hostname and OS.
#. Slurm (if deployed) can schedule and run jobs across compute nodes.
#. Kubernetes (if deployed) has all control-plane and worker nodes ready.
#. Authentication and storage services are operational.



Prerequisites
-------------


- Nodes are provisioned and reachable (see `Pxe Boot Nodes <pxe_boot_nodes.md>`_).
- Slurm and/or Kubernetes have been deployed (see
  `Setup Slurm <../Slurm/setup_slurm.md>`_ or
  `Setup Service K8S <../Kubernetes/setup_service_k8s.md>`_).



Procedure
---------



Verify Node Connectivity
~~~~~~~~~~~~~~~~~~~~~~~~


#. **Ping all nodes** from the omnia_core container:


.. code-block:: bash title="Run on: omnia_core container"

      ansible all -m ping



   Expected output for each node:


.. code-block:: text title="Expected output on: omnia_core container"

      10.5.0.101 | SUCCESS => {
          "ping": "pong"
      }



#. **Check OS version on all nodes**:


.. code-block:: bash title="Run on: omnia_core container"

      ansible all -m shell -a "cat /etc/os-release | grep PRETTY_NAME"



#. **Check hostnames are correctly set**:


.. code-block:: bash title="Run on: omnia_core container"

      ansible all -m shell -a "hostname"





Verify Slurm
~~~~~~~~~~~~


#. **SSH to the Slurm control node** and check the cluster status:


.. code-block:: bash title="Run on: omnia_core container"

      ssh root@<slurm-control-node-ip>




.. code-block:: bash title="Run on: Slurm control node"

      sinfo



   Expected output:


.. code-block:: text title="Expected output on: Slurm control node"

      PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
      normal*      up   infinite      2   idle compute[01-02]



   All nodes should show ``idle`` state. If any show ``down`` or ``drain``,
   investigate further.

#. **Run a test job** across all compute nodes:


.. code-block:: bash title="Run on: Slurm control node"

      srun -N 2 hostname



   Expected output shows the hostnames of the compute nodes that executed the
   job:


.. code-block:: text title="Expected output on: Slurm control node"

      compute01
      compute02



#. **Submit a batch job**:


.. code-block:: bash title="Run on: Slurm control node"

      cat <<'EOF' > /tmp/test_job.sh
      #!/bin/bash
      #SBATCH --job-name=test
      #SBATCH --nodes=1
      #SBATCH --time=00:01:00
      echo "Hello from $(hostname) at $(date)"
      EOF
   
      sbatch /tmp/test_job.sh




.. code-block:: bash title="Run on: Slurm control node"

      # Check job status
      squeue
   
      # View job output after completion
      cat slurm-*.out



#. **Verify Slurm accounting**:


.. code-block:: bash title="Run on: Slurm control node"

      sacct --starttime=today





Verify Kubernetes
~~~~~~~~~~~~~~~~~


#. **Check Kubernetes node status** from a control-plane node:


.. code-block:: bash title="Run on: omnia_core container"

      ssh root@<k8s-control-plane-ip>




.. code-block:: bash title="Run on: K8s control plane node"

      kubectl get nodes



   Expected output:


.. code-block:: text title="Expected output on: K8s control plane node"

      NAME          STATUS   ROLES           AGE   VERSION
      k8s-cp01      Ready    control-plane   1h    v1.28.x
      k8s-cp02      Ready    control-plane   1h    v1.28.x
      k8s-cp03      Ready    control-plane   1h    v1.28.x
      k8s-worker01  Ready    <none>          1h    v1.28.x



   All nodes should show ``Ready`` status.

#. **Verify core Kubernetes components**:


.. code-block:: bash title="Run on: K8s control plane node"

      kubectl get pods -A



   All system pods (``kube-system``, ``calico-system``, ``metallb-system``)
   should be ``Running``.

#. **Test pod scheduling**:


.. code-block:: bash title="Run on: K8s control plane node"

       kubectl run test-pod --image=busybox --restart=Never -- echo "Hello from K8s"
       kubectl logs test-pod
       kubectl delete pod test-pod





Verification
------------


Use the following summary checklist:


.. list-table::
   :header-rows: 1
   :widths: auto

   * - Check
     - Command
     - Expected Result
   * - All nodes reachable
     - ``ansible all -m ping``
     - All return ``pong``
   * - Slurm nodes idle
     - ``sinfo``
     - All nodes ``idle``
   * - Slurm job runs
     - ``srun -N 2 hostname``
     - Hostnames printed
   * - K8s nodes ready
     - ``kubectl get nodes``
     - All ``Ready``
   * - K8s pods running
     - ``kubectl get pods -A``
     - All ``Running``



Next Steps
----------


- `Slurm With Gpu <../Slurm/slurm_with_gpu.md>`_ -- Configure GPU support for Slurm.
- `Setup Telemetry <../Telemetry/setup_telemetry.md>`_ -- Deploy monitoring and telemetry.
- `Setup Openldap <../Authentication/setup_openldap.md>`_ -- Set up centralized
  authentication.
- `Configure Nfs <../Storage/configure_nfs.md>`_ -- Configure shared NFS storage.



Troubleshooting
---------------


**Ansible ping fails for some nodes**
  - Verify SSH keys are deployed:


.. code-block:: bash title="Run on: omnia_core container"

        ssh-copy-id root@<node-ip>



  - Check network connectivity:


.. code-block:: bash title="Run on: omnia_core container"

        ping -c 3 <node-ip>



**Slurm nodes show "down" state**
   Check the Slurm daemon on the affected compute node:


.. code-block:: bash title="Run on: affected compute node"

      systemctl status slurmd
      journalctl -u slurmd --no-pager -n 20



   Resume the node from the control node:


.. code-block:: bash title="Run on: Slurm control node"

      scontrol update nodename=<node> state=resume



**Kubernetes node shows "NotReady"**
   Check kubelet status on the affected node:


.. code-block:: bash title="Run on: affected K8s node"

      systemctl status kubelet
      journalctl -u kubelet --no-pager -n 20



**Slurm srun hangs**
  - Verify ``munge`` is running on all Slurm nodes:


.. code-block:: bash title="Run on: omnia_core container"

        ansible slurm_cluster -m shell -a "systemctl is-active munge"



  - Check firewall rules allow Slurm traffic (ports 6817-6819):


.. code-block:: bash title="Run on: omnia_core container"

        ansible slurm_cluster -m shell -a "firewall-cmd --list-ports"

