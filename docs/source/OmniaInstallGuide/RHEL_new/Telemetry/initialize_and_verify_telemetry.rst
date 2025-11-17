Step 14: Initialize and verify telemetry
============================================

To initiate the telemetry on the service cluster, run the ``telemetry.yml`` playbook.::

    cd telemetry
    ansible-playbook telemetry.yml -i inventory

Verify Telemetry-Related Pods Are Running
==========================================

To verify that the iDRAC Telemetry, Kafka, LDMS, and VictoriaMetrics pods are running, do the following:::

1. Run the following command:::

    kubectl get pods -n telemetry

2. Ensure that the following pods are in the running state in the output:

    * iDRAC Telemetry pods
    * Kafka broker, controller, and operator pods
    * LDMS aggregator and store pods
    * VictoriaMetrics and vmagent pods

The following is the sample output file:

+-----------------------------------------------+---------+-----------+-------------+-------+
| NAME | READY | STATUS | RESTARTS | AGE |
+===============================================+=========+===========+=============+=======+
| bridge-bridge-66779c8b65-zx2xm | 1/1 | Running | 0 | 93m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| idrac-telemetry-0 | 5/5 | Running | 0 | 91m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| kafka-broker-0 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| kafka-broker-1 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| kafka-broker-2 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| kafka-controller-3 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| kafka-controller-4 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| kafka-controller-5 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| kafka-entity-operator-7ffd8c769d-rz756 | 2/2 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| nersc-ldms-aggr-0 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| nersc-ldms-store-r7525-0 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| strimzi-cluster-operator-64574988c8-bsg9t | 1/1 | Running | 0 | 19h |
+-----------------------------------------------+---------+-----------+-------------+-------+
| victoria-metric-0 | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| victoria-tls-test-ng727 | 0/1 | Completed | 0 | 23m |
+-----------------------------------------------+---------+-----------+-------------+-------+
| vmagent-7c796b8b8c-pg5cq | 1/1 | Running | 0 | 95m |
+-----------------------------------------------+---------+-----------+-------------+-------+


Verify Kubernetis Telemetry Services attached to telemetry 
----------------------------------------------------------

To verify kubernetis telmetry services attached to the iDRAC Telemetry, Kafka, LDMS, and VictoriaMetrics pods, do the following:

1. Run the following command::

    kubectl get svc -n telemetry

2. Ensure the following services entries exist:

    * idrac-telemetry-service
    * kafka-broker-0
    * kafka-broker-1
    * kafka-broker-2
    * kafka-kafka-bootstrap
    * kafka-kafka-brokers
    * kafka-kafka-external-bootstrap
    * nersc-ldms-aggr
    * nersc-ldms-store
    * victoria-loadbalancer

The following is the sample output file:

+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| NAME | TYPE | CLUSTER-IP | EXTERNAL-IP | PORT(S) | AGE |
+===========================================+===============+================+================+==============================================+=======+
| bridge-bridge-lb | LoadBalancer | 10.233.10.224 | 10.11.0.100 | 8080:31647/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| bridge-bridge-service | ClusterIP | 10.233.2.215 | <none> | 8080/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| idrac-telemetry-service | ClusterIP | None | <none> | 3306/TCP,33060/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| kafka-broker-0 | LoadBalancer | 10.233.38.88 | 10.11.0.103 | 9094:31488/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| kafka-broker-1 | LoadBalancer | 10.233.33.216 | 10.11.0.104 | 9094:30711/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| kafka-broker-2 | LoadBalancer | 10.233.43.167 | 10.11.0.105 | 9094:32093/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| kafka-kafka-bootstrap | ClusterIP | 10.233.25.54 | <none> | 9091/TCP,9092/TCP,9093/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| kafka-kafka-brokers | ClusterIP | None | <none> | 9090/TCP,9091/TCP,8443/TCP,9092/TCP,9093/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| kafka-kafka-external-bootstrap | LoadBalancer | 10.233.25.116 | 10.11.0.102 | 9094:32333/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| nersc-ldms-aggr | ClusterIP | 10.233.35.123 | <none> | 6001/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| nersc-ldms-store | ClusterIP | None | <none> | 6001/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+
| victoria-loadbalancer | LoadBalancer | 10.233.35.99 | 10.11.0.101 | 8443:32667/TCP | 95m |
+-------------------------------------------+---------------+----------------+----------------+----------------------------------------------+-------+


Verify iDRAC Telemetry Messages in Kafka
-------------------------------------------

To verify that iDRAC telemetry data is being successfully published to the `idrac_telemetry`` Kafka topic, do the following:

1. Create a Kafka consumer using the following command::

    curl -X POST http://10.11.0.100:8080/consumers/idrac-consumer-group \
      -H 'content-type: application/vnd.kafka.v2+json' \
      -d '{
            "name": "idrac-consumer-1",
            "format": "json",
            "auto.offset.reset": "earliest"
          }'

2. Subscribe the consumer to the telemetry topic using the following command::

    curl -X POST http://10.11.0.100:8080/consumers/idrac-consumer-group/instances/idrac-consumer-1/subscription \
      -H 'content-type: application/vnd.kafka.v2+json' \
      -d '{"topics": ["idrac_telemetry"]}'

3. Consume messages from the topic using the following command::
  
    curl -X GET http://10.11.0.100:8080/consumers/idrac-consumer-group/instances/idrac-consumer-1/records \
      -H 'accept: application/vnd.kafka.json.v2+json' | jq '.'

    If telemetry is flowing correctly, the output contains JSON-formatted iDRAC telemetry records.

Verify LDMS Messages in Kafka
-----------------------------

To verify that LDMS telemetry data is being successfully published to the ``ldms`` Kafka topic, do the following:

1. Create a Kafka consumer using the following command::

    curl -X POST http://10.11.0.100:8080/consumers/ldms-consumer-group \
      -H 'content-type: application/vnd.kafka.v2+json' \
      -d '{
            "name": "ldms-consumer-1",
            "format": "json",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": true
          }'

2. Subscribe the consumer to the LDMS topic using the following command::

    curl -X POST http://10.11.0.100:8080/consumers/ldms-consumer-group/instances/ldms-consumer-1/subscription \
      -H 'content-type: application/vnd.kafka.v2+json' \
      -d '{"topics": ["ldms"]}'

3. Consume messages from the topic using the following command::

    curl -X GET http://10.11.0.100:8080/consumers/ldms-consumer-group/instances/ldms-consumer-1/records \
      -H 'accept: application/vnd.kafka.json.v2+json' | jq '.'

    If telemetry is flowing correctly, the output contains JSON-formatted LDMS telemetry records.


Verify Kafka TLS Connectivity
-----------------------------

If you encounter issues with Kafka TLS connectivity, run the Kafka TLS test job to verify that
certificates, truststores, keystores, and mTLS communication are functioning correctly::

    kubectl apply -f kafka.tls_test_job.yaml

After the job completes, check the logs to confirm that the TLS connection is successful::

    kubectl logs kafka-tls-test-xxx -n telemetry


Verify VictoriaMetrics TLS Connectivity
---------------------------------------

If you encounter issues accessing VictoriaMetrics over TLS, run the VictoriaMetrics TLS test job to
verify that certificates and secure connectivity are functioning correctly::

    kubectl apply -f victoria-tls-test-job.yaml

After the job completes, check the logs to confirm that the TLS connection is successful::

    kubectl logs victoria-tls-test-xxx -n telemetry



View LDMS telemetry collected by Kafka
=========================================

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

View iDRAC telemetry collected by Kafka
-----------------------------------------------------
        


View iDRAC telemetry collected by VictoriaMetrics
---------------------------------------------------

After applying the ``telemetry.yml`` configuration using the VictoriaMetrics collection type, follow these steps to verify and view the collected telemetry:

1. Run the following command to verify that the VictoriaMetrics pod is running::

       kubectl get pods -n telemetry -o wide -l app=victoriametrics

   .. image:: ../images/victoria_metrics_pod.png

2. Run the following command to verify that the VictoriaMetrics service is running::

       kubectl get service -n telemetry -o wide -l app=victoriametrics

   .. image:: ../images/victoria_metrics_service.png

3. Note the **External IP** and **port number** of the VictoriaMetrics service. The external IP and port number will be used to access the VictoriaMetrics UI (VMUI).

4. Access the VMUI in a web browser using::

       http://<external IP>:8428/vmui

5. Filter and view telemetry metrics using queries in VMUI.
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