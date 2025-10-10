Sample Files
=============

Inventory file for service K8s cluster
------------------------------------------

.. caution:: All the file contents mentioned below are case sensitive.

::

             

        #AI Scheduler: Kubernetes

        [kube_control_plane]

        10.5.0.201
        10.5.0.202
        10.5.0.203 

        


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
        {"name": "default_packages", "arch": ["x86_64","aarch64"]},
        {"name": "openldap", "arch": ["x86_64"]},
        {"name": "nfs", "arch": ["x86_64","aarch64"]},
        {"name": "slurm_custom", "arch": ["x86_64","aarch64"]},
        {"name": "service_k8s", "version": "1.31.4", "arch": ["x86_64"]},
        {"name": "ucx", "version": "1.15.0", "arch": ["x86_64"]},
        {"name": "openmpi", "version": "4.1.6", "arch": ["x86_64"]}
    ],
    "slurm_custom": [
        {"name": "slurm_control_node"},
        {"name": "slurm_node"},
        {"name": "login_node"},
        {"name": "login_compiler_node"}
    ],
    "service_k8s": [
        {"name": "service_kube_control_plane"},
        {"name": "service_etcd"},
        {"name": "service_kube_node"}
    ]
 
    } 
 

pxe_mapping_file.csv
------------------------------------

::

    FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
    slurm_control_node_x86_64,grp0,ABCD12,slurm_control_node1,xx:yy:zz:aa:bb:cc,172.16.107.52,xx:yy:zz:aa:bb:dd,172.17.107.52
    slurm_node_x86_64,grp1,ABCD34,slurm_node1,aa:bb:cc:dd:ee:ff,172.16.107.43,aa:bb:cc:dd:ee:gg,172.17.107.43
    slurm_node_x86_64,grp1,ABFG34,slurm_node2,aa:bb:cc:dd:ee:ff,172.16.107.44,aa:bb:cc:dd:ff:gg,172.17.107.44
    login_compiler_node_x86_64,grp6,ABCD78,login_compiler_node1,aa:bb:cc:dd:ee:gg,172.16.107.41,aa:bb:cc:dd:ee:bb,172.17.107.41
    login_compiler_node_x86_64,grp6,ABFG78,login_compiler_node2,aa:bb:cc:dd:ee:gg,172.16.107.42,aa:bb:cc:dd:ee:bb,172.17.107.42
    service_kube_node_x86_64,grp3,ABCD56,service_kube_node1,xx:yy:zz:aa:bb:dd,172.16.107.54,xx:yy:zz:aa:bb:ff,172.17.107.54
    service_kube_node_x86_64,grp3,ABFG56,service_kube_node2,xx:aa:zz:aa:bb:dd,172.16.107.55,xx:aa:zz:aa:bb:ff,172.17.107.55