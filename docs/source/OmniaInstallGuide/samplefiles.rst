Sample Files
=============

Inventory file for service K8s cluster
------------------------------------------

.. caution:: All the file contents mentioned below are case sensitive.

::

             

        #AI Scheduler: Kubernetes

        [kube_control_plane]

        10.5.1.101

        [etcd]

        10.5.1.101

        [kube_node]

        10.5.1.102

        10.5.1.103

        10.5.1.104

        10.5.1.105

        10.5.1.106


Inventory file for PXE boot order
---------------------------------

::

    [bmc]
    10.3.0.1
    10.3.0.2

software_config.json for RHEL
-------------------------------------------

::

    {
    "cluster_os_type": "rhel",
    "cluster_os_version": "10.0",
    "repo_config": "always",
    "softwares": [
        {"name": "cuda", "version": "13.0.1"},
        {"name": "ofed", "version": "24.10-3.2.5.0"},
        {"name": "openldap"},
        {"name": "nfs"},
        {"name": "slurm"},
        {"name": "service_k8s", "version": "1.31.4"},
        {"name": "ucx", "version": "1.15.0"},
        {"name": "openmpi", "version": "4.1.6"},
        {"name": "csi_driver_powerscale", "version":"v2.14.0"}        
    ],
    "slurm": [
        {"name": "slurm_control_node"},
        {"name": "slurm_node"},
        {"name": "login_node"}
    ]

    }

pxe_mapping_file.csv
------------------------------------

::

    FUNCTIONAL_GROUP_NAME,SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
    slurm_controller_node_x86_64,x1000c1s7b1n0,n1,xx:yy:zz:aa:bb:cc,10.5.0.101,xx:yy:zz:aa:bb:dd,10.3.0.101
    slurm_node_x86_64,x1000c1s7b1n1,n2,aa:bb:cc:dd:ee:ff,10.5.0.102,aa:bb:cc:dd:ee:gg,10.3.0.102