=======================================================
Configure Deployment Required for iDRAC Telemetry Service
=======================================================

To deploy iDRAC telemetry service on the service cluster, do the following:

Prerequisites
--------------

* Redfish must be enabled in iDRAC.
* If the internet connection is required on the service Kube node, configure it after the node is booted. 
* iDRAC firmware must be updated to the latest version. 
* Datacenter license must be installed on the nodes.
* Ensure that the correct node service tags are being displayed on the iDRAC interface. Otherwise, telemetry data cannot be collected by the ``idrac_telemetry_receiver`` container.
* For telemetry collection on service cluster, all BMC (iDRAC) IPs must be reachable from the service cluster nodes.
* Ensure that ``discovery.yml`` playbook has been executed successfully with both ``service_kube_control_plane_x86_64`` and  ``service_kube_node_x86_64`` in the mapping file, and the ``bmc_group_data.csv`` file has been generated.
* Before running the ``telemetry.yml`` playbook for the service cluster, ensure that all the service K8s compute node are reachable and booted and have been configured in the service K8s cluster.

Steps
-----------

1. In the mapping file, ensure that the service tag of the service kube node specified as the parent for the slurm nodes.
2. Fill up the ``omnia_config.yml``:

    .. csv-table:: omnia_config.yml
        :file: ../../../Tables/omnia_config_service_cluster.csv
        :header-rows: 1
        :keepspace: 
3. Ensure that the ``telemetry_config.yml`` has the entries specific to iDRAC telemetry support, Victoria, and Kafka based on your requirement.

    .. csv-table:: telemetry_config.yml
        :file: ../../../Tables/telemetry_config.csv
        :header-rows: 1
        :keepspace:

