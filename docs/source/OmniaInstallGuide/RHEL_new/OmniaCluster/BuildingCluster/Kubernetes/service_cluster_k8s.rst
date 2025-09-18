==========================================
Set up Kubernetes on the service cluster
==========================================

With Omnia, you can deploy a service Kubernetes cluster on the designated service nodes to efficiently distribute workload and manage resources for telemetry data collection. 
This setup reduces the processing load on the OIM node and enhances overall scalability. Each ``service_kube_node`` is responsible for collecting telemetry data from its assigned subset of compute nodes.
Federated way of telemetry data collection improves efficiency for large-scale clusters.

Prerequisites
==============

* To deploy Kubernetes on service cluster, ensure that ``service_k8s`` is added under ``softwares`` in the ``/opt/omnia/input/project_default/software_config.json``. Refer the sample config file below: ::

    {
        "cluster_os_type": "rhel",
        "cluster_os_version": "10.0",
        "repo_config": "always",
        "softwares": [
            {"name": "cuda", "version": "13.0.1", "arch": ["x86_64","aarch64"]},
            {"name": "ofed", "version": "24.10-3.2.5.0", "arch": ["x86_64"]},
            {"name": "openldap", "arch": ["x86_64"]},
            {"name": "nfs", "arch": ["x86_64","aarch64"]},
            {"name": "service_k8s","version": "1.31.4", "arch": ["x86_64"]},
            {"name": "slurm", "arch": ["x86_64","aarch64"]}
        ],
        "slurm": [
            {"name": "slurm_control_node"},
            {"name": "slurm_node"},
            {"name": "login_node"}
        ],
        "service_k8s": [
            {"name": "service_kube_control_plane"},
            {"name": "service_etcd"},
            {"name": "service_kube_node"}
        ]
    }

* Ensure that there are a minimum of  three ``kube_control_planes``.

* Ensure that the ``kube_control_planes`` has a full-featured RHEL operating system (OS) installed. 

* Ensure that the ``kube_control_planes`` has internet access and Git installed. If Git is not installed, use the following command to install it.

    ::

        dnf install git -y

* The ``kube_control_planes`` has internet access to download necessary packages for cluster deployment and configuration.
* The ``kube_control_planes`` must have two active Network Interface Cards (NICs):  

  * One connected to the public network.  
  * One dedicated to internal cluster communication. 
* If you want to use a NFS share for the omnia shared path, ensure the following:

  * The NFS share has 755 permissions and ``no_root_squash`` is enabled on the mounted NFS share. 
  * Edit the ``/etc/exports`` file on the NFS server to include the ``no_root_squash`` option for the exported path.
    
    ::
        
        /<your_exported_path>  *(rw,sync,no_root_squash,no_subtree_check)

* Ensure that the following ``kube_control_planes`` hostname prerequisites are met.

    .. include:: ../../Appendices/hostnamereqs.rst

Steps
=======

1. Run ``local_repo.yml`` playbook to download the artifacts required to set up Kubernetes on the service cluster nodes.

2. Fill in the service cluster details in the ``functional_groups_config.yml``.

.. csv-table:: functional_groups_config.yml
   :file: ../../../../../Tables/service_k8s_roles.csv
   :header-rows: 1
   :keepspace:

3. Fill  the ``omnia_config.yml``,  ``high_availability_config.yml`` (for `service cluster HA <../../HighAvailability/service_cluster_ha.html>`_), and ``storage_config.yml``. The nfs_name mentioned in ``storage_config.yml`` should match the ``nfs_storage_name`` of the entries for the ``service_k8s_cluster`` in ``omnia_config.yml`` where deployment is set to true.
   See the following sample:

    ::

        nfs_client_params:
        -{
           nfs_name: "nfs_storage_default"
           server_ip: "", # Provide the IP of the NFS server
           server_share_path: "", # Provide server share path of the NFS Server
           client_share_path: /home,
           client_mount_options: "nosuid,rw,sync,hard,intr",
           nfs_server: false,
        }
       

.. csv-table:: omnia_config.yml
   :file: ../../../../Tables/scheduler_k8s_rhel.csv
   :header-rows: 1
   :keepspace:

.. csv-table:: high_availability_config.yml
   :file: ../../../../Tables/service_k8s_high_availability.csv
   :header-rows: 1
   :keepspace:

4. Run ansible-playbook ``service_k8s_cluster.yml``.


5. Run ``build.image.yml`` playbook to build diskless images for cluster nodes. 

6. Run ``discovery.yml`` playbook to discover the potential cluster nodes, configure the boot script, and cloud-init based on the functional groups.
   After successfully running the ``discovery.yml`` playbook, you can either manually PXE boot the nodes or use the ``set_pxe_boot.yml`` playbook. PXE booting allows the nodes to load diskless images from the Omnia Infrastructure Manager (OIM). For detailed steps on using ``set_pxe_boot.yml``, see Set PXE Boot Order.


Playbook execution
====================

Once all the required input files are filled up, use the below commands to set up Kubernetes on the service cluster: ::

    cd scheduler
    ansible-playbook service_k8s_cluster.yml - i <ivn>

In the command above, ``<ivn>`` refers to the inventory. See the following sample:

    ::

        [Inventory]
        10.5.0.201  
        10.5.0.202 
        10.5.0.203 


Additional installations
=========================

After deploying Kubernetes, you can install the following additional packages on top of the Kubernetes stack on the service cluster:

1. **nfs-client-provisioner**

        * NFS subdir external provisioner is an automatic provisioner that use your existing and already configured external NFS server to support dynamic provisioning of Kubernetes Persistent Volumes via Persistent Volume Claims.
        * The nfs_name mentioned in ``storage_config.yml`` should match the ``nfs_storage_name`` of the entries for the ``service_k8s_cluster``.
        * Use the same NFS server IP provided during ``omnia_startup.sh`` execution. 
        * Path is mentioned in ``/omnia/k8s_pvc_data`` under ``{{ nfs_server_share_path }}``.

    Click `here <https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner>`_ for more information.


3. **CSI-driver-for-PowerScale**

    The CSI Driver for Dell PowerScale (formerly known as Isilon) is a Container Storage Interface (CSI) plugin that enables Kubernetes to provision and manage persistent storage using PowerScale.
    It enables Kubernetes clusters to dynamically provision, bind, expand, snapshot, and manage volumes on a PowerScale node.
    Omnia installs the multus plugin as part of ``omnia.yml`` or ``scheduler.yml`` execution.

    Click `here <../../../../AdvancedConfigurations/PowerScale_CSI.html>`_ for more information.

Next step
===========

To know how to deploy the iDRAC telemetry containers on the service cluster, `click here <../../../../../Telemetry/service_cluster_telemetry.html>`_.