Step 13: Verify Slurm cluster and Kubernetes on the service cluster
============================================================================================================

**Slurm cluster**


After booting the nodes, verify the following to ensure slurm is deployed successfully: 
On slurm controller node

    * Verify if the required services are running. Run the following commands and confirm that each service is active (running):
    
    ::

          systemctl status munge
          systemctl status slurmctld
          systemctl status slurmdbd
          systemctl status mariadb

    * Verify the node status with sinfo:

          .. image:: ../../../../images/sinfo.jpg
   
          * Ensure that the worker nodes are listed and the node state should be idle.


**PAM Feature for Slurm**

Slurm PAM restricts SSH access to compute nodes for non-root users. You can log in only while their job is actively running on the node. After the job is completed, you are is automatically logged out.  

On login node: Switch to the LDAP user:
::
      ssh <ldap_user>@<login_node_hostname>
      sbatch job.sh

While the job is running, ssh as ``<ldap_user>`` to the slurm node where the job is running. After the job is completed, ``<ldap_user>`` is logged out.


**Kubernetes on the service cluster**

Run the following commands: 

:: 

    kubectl get pods -A -o wide
    kubectl get nodes -o wide
 