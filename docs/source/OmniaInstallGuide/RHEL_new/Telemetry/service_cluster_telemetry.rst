=======================================================
Configure deployment required for iDRAC telemetry service
=======================================================

To deploy iDRAC telemetry service on the service cluster and collect iDRAC telemetry data using Kafka, refer to the following guide.

Prerequisites
===============

* Redfish must be enabled in iDRAC.
* If the internet connection is required on the service Kube node, configure it after the node is booted. 
* All service cluster nodes should have access to the Internet.
* iDRAC firmware must be updated to the latest version. 
* Datacenter license must be installed on the nodes.
* Ensure that the correct node service tags are being displayed on the iDRAC interface. Otherwise, telemetry data cannot be collected by the ``idrac_telemetry_receiver`` container.
* For telemetry collection on service cluster, all BMC (iDRAC) IPs must be reachable from the service cluster nodes.
* Ensure that the ``service_k8s_cluster.yml`` playbook has been executed successfully and Kubernetes on the service K8s controller node is up and running.
* Ensure that ``discovery.yml`` playbook has been executed successfully with ``service_kube_node_x86_64`` in the ``functional_groups_config.yml``, and the ``bmc_group_data.csv`` file has been generated.
* Before running the ``telemetry.yml`` playbook for the service cluster, ensure that all the service K8s compute node are reachable and booted and have been configured in the service K8s cluster.

Steps
======

1. In the mapping file, specify the service tag of the service kube node as the parent for the slurm nodes.
2. Fill up the ``omnia_config.yml`` and ``telemetry_config.yml``:

    .. csv-table:: omnia_config.yml
        :file: ../Tables/omnia_config_service_cluster.csv
        :header-rows: 1
        :keepspace: 

    .. csv-table:: telemetry_config.yml
        :file: ../Tables/telemetry_config.csv
        :header-rows: 1
        :keepspace:


**Sample telemetry inventory**::

    [kube_control_plane]
    192.168.10.151 bmc_ip=172.10.5.73
    192.168.10.152 bmc_ip=172.10.5.74
    192.168.10.153 bmc_ip=172.10.5.75
    
.. note:: For all nodes in the ``kube_control_plane`` group, ensure that the BMC IP address is defined using the ``bmc_ip`` variable, in addition to the admin IP address.


