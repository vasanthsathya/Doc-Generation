=======================================================
Deploy iDRAC telemetry service on the service cluster
=======================================================

To deploy telemetry service on the service cluster and collect iDRAC telemetry data using Kafka, refer to the following guide.

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
* Ensure that ``discovery.yml`` playbook has been executed successfully with ``secvice_kube_node_x86_64`` in the ``functional_groups_config.yml``, and the ``bmc_group_data.csv`` file has been generated.
* Before running the ``telemetry.yml`` playbook for the service cluster, ensure that all the service K8s compute node are reachable and booted and have been configured in the service K8s cluster.

Steps
======

1. In the ``functional_groups_config.yml`` file, specify the service tag of the service kube node as the parent for the slurm nodes.
2. Fill up the ``omnia_config.yml`` and ``telemetry_config.yml``:

    .. csv-table:: omnia_config.yml
        :file: ../Tables/omnia_config_service_cluster.csv
        :header-rows: 1
        :keepspace: 

    .. csv-table:: telemetry_config.yml
        :file: ../Tables/telemetry_config.csv
        :header-rows: 1
        :keepspace:

3. Execute the ``telemetry.yml`` playbook. ::

    cd telemetry
    ansible-playbook telemetry.yml -i inventory

**Sample telemetry inventory**::

    [kube_control_plane]
    192.168.10.151 bmc_ip=172.10.5.73
    192.168.10.152 bmc_ip=172.10.5.74
    192.168.10.153 bmc_ip=172.10.5.75
    
.. note:: For all nodes in the ``kube_control_plane`` group, ensure that the BMC IP address is defined using the ``bmc_ip`` variable, in addition to the admin IP address.


Result
=======

The iDRAC telemetry pods along with the ``mysqldb``, ``activemq``, ``telemetry_receiver``, and ``kafka_pump`` containers will get deployed on the ``service_kube_node``.
The number of iDRAC telemetry pods deployed will be number of ``service_kube_nodes`` mentioned as parents in ``functional_groups_config.yml`` plus an extra telemetry pod to collect the metric data of OIM, management layer nodes, and the service cluster.


iDRAC telemetry logs collected by the Kafka pump
====================================================

After applying the ``telemetry.yml`` configuration using the Kafka collection type, iDRAC telemetry logs are published to a Kafka topic on the broker. To view the logs, do the following:

    1. Use the following command to view all telemetry pods: ::

        kubectl get pods -n telemetry

    2. Run the following command to access the Kafka pod from which you want to read the logs. ::

        kubectl exec <kafka-pod> -it  -n telemetry -- bash

    3. To read the telemetry logs from the Kafka pod, run the following Kafka console consumer script. For details on using the Kafka consumer, see the:  
       `Kafka console consumer documentation <https://docs.confluent.io/kafka/operations-tools/kafka-tools.html#kafka-console-consumer-sh>`_ ::

        kafka-console-consumer.sh
         --bootstrap-server localhost:9092
         --topic idrac_telemetry
         --from-beginning
         --consumer.config /tmp/client.properties

    .. note:: Metrics visualization using Grafana is not supported for iDRAC telemetry metrics on service cluster.


View iDRAC telemetry collected by VictoriaMetrics
=================================================

After applying the ``telemetry.yml`` configuration using the VictoriaMetrics collection type, follow these steps to verify and view the collected telemetry:

1. Run the following command to verify that the VictoriaMetrics pod is running::

       kubectl get pods -n telemetry -o wide -l app=victoriametrics

   .. image:: ../images/victoria_metrics_pod.png

2. Run the following command to verify that the VictoriaMetrics service is running::

       kubectl get service -n telemetry -o wide -l app=victoriametrics

   .. image:: ../images/victoria_metrics_service.png

3. Note the **External IP** and **port number** of the VictoriaMetrics service. The **External IP** and port number will be used to access the VictoriaMetrics UI (VMUI).

4. Access the VictoriaMetrics UI in a web browser using::

       http://<VictoriaMetrics service External-IP>:<VictoriaMetrics service port number>/vmui

5. Filter and view telemetry metrics using queries in **VMUI**.
   For example, the following query displays detailed temperature
   readings for each hardware component::

       {name="PowerEdge_TemperatureReading", FQDD!=""}

   .. image:: ../images/victoria_metrics_vmui.png
    

Accessing the ``mysqldb`` database
====================================

After ``telemetry.yml`` has been executed for the service cluster, you can check the mysqldb database inside the ``mysqldb`` container. To view these logs, do the following:

    1. Use the following command to get the names of all the telemetry pods: ::
        
        kubectl get pods -n telemetry -l app=idrac-telemetry

    .. note:: The ``idrac-telemetry-0`` pod will always be responsible for collecting the telemetry data of the management nodes (``oim``, ``service_kube_control_plane``, ``service_kube_node_x86_64``, ``login_node_x86_64``, etc.).

    2. Execute the following command: ::

        kubectl exec -it -n telemetry <iDRAC_telemetry_pod_name> -c mysqldb -- mysql -u <MYSQL_USER> -p

    3. When prompted, enter the mysql password to log in.

    4. To enter into the ``idrac_telemetry_db``, use the following command: ::

        use idrac_telemetrydb;

    5. To access the services table: ::
        
        Select * from services;