Step 16: Verify Telemetry Services deployed on the cluster
=========================================================

This section outlines the steps to validate telemetry services and their components, including checking pod status, 
verifying message flow, confirming TLS connectivity, and reviewing collected telemetry data.


Verify Telemetry-Related Pods Are Running
-------------------------------------------

To verify that the iDRAC Telemetry, Kafka, LDMS, and VictoriaMetrics pods are running, do the following:::

1. Run the following command:::

    kubectl get pods -n telemetry

2. Ensure that the following pods are in the running state in the output:

    * iDRAC Telemetry pods
    * Kafka broker, controller, and operator pods
    * LDMS aggregator and store pods
    * VictoriaMetrics and vmagent pods

The following is the sample output file:

.. image:: ../../../images/verify_telemetry_pods.png

Verify Kubernetes Telemetry Services attached to telemetry 
----------------------------------------------------------

To verify kubernetes telmetry services attached to the iDRAC Telemetry, Kafka, LDMS, and VictoriaMetrics pods, do the following:

1. Run the following command::

    kubectl get svc -n telemetry

2. Ensure the following services entries exist:

    * bridge-bridge-lb
    * bridge-bridge-service
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

.. image:: ../../../images/verify_kube_telemetry.png


Verify iDRAC Telemetry Messages in Kafka
-------------------------------------------

To verify that iDRAC telemetry data is being successfully published to the ``idrac`` Kafka topic, do the following:

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
      -d '{"topics": ["idrac"]}'

3. Consume messages from the topic using the following command::
  
    curl -X GET http://10.11.0.100:8080/consumers/idrac-consumer-group/instances/idrac-consumer-1/records \
      -H 'accept: application/vnd.kafka.json.v2+json' | jq '.'

If telemetry metrics are collected correctly, the output contains JSON-formatted iDRAC telemetry records.

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
To verify TLS connectivity for Kafka, run the Kafka TLS test job to verify that
certificates, truststores, keystores, and mTLS communication are functioning correctly::

    kubectl apply -f kafka.tls_test_job.yaml

After the job completes, check the logs to confirm that the TLS connection is successful::

    kubectl logs kafka-tls-test-xxx -n telemetry


Verify VictoriaMetrics TLS Connectivity
---------------------------------------

To verify TLS connectivity for VictoriaMetrics, run the VictoriaMetrics TLS test job to
verify that certificates and secure connectivity are functioning correctly::

    kubectl apply -f victoria-tls-test-job.yaml

After the job completes, check the logs to confirm that the TLS connection is successful::

    kubectl logs victoria-tls-test-xxx -n telemetry    


View collected iDRAC telemetry data using Victoria Metrics UI (VMUI)
---------------------------------------------------------------------

After applying the ``telemetry.yml`` configuration using the VictoriaMetrics collection type, follow these steps to verify and view the collected telemetry:

1. Run the following command to verify that the VictoriaMetrics pod is running::

       kubectl get pods -n telemetry -o wide -l app=victoriametrics

   .. image:: ../../../images/victoria_metrics_pod.png

2. Run the following command to verify that the VictoriaMetrics service is running::

       kubectl get service -n telemetry -o wide -l app=victoriametrics

   .. image:: ../../../images/victoria_metrics_service.png

3. Note the **External IP** and **port number** of the VictoriaMetrics service. The external IP and port number will be used to access the VictoriaMetrics UI (VMUI).

4. Access the VMUI in a web browser using::

       http://<external IP>:8428/vmui

5. Filter and view telemetry metrics using queries in VMUI.
   For example, the following query displays detailed temperature
   readings for each hardware component::

       {name="PowerEdge_TemperatureReading", FQDD!=""}

   .. image:: ../../../images/victoria_metrics_vmui.png


Accessing the ``mysqldb`` database
------------------------------------

After ``telemetry.yml`` has been executed for the service cluster, you can check the mysqldb database inside the ``mysqldb`` container. To view these logs, do the following:

    1. Use the following command to get the names of all the telemetry pods: ::
        
        kubectl get pods -n telemetry -l app=idrac-telemetry

    .. note:: The ``idrac-telemetry-0`` pod will always be responsible for collecting the telemetry data of the management nodes (``oim``, ``service_kube_control_plane_x86_64``, ``service_kube_node_x86_64``, ``login_node_x86_64``, etc.).

    2. Execute the following command: ::

        kubectl exec -it -n telemetry <iDRAC_telemetry_pod_name> -c mysqldb -- mysql -u <MYSQL_USER> -p

    3. When prompted, enter the mysql password to log in.

    4. To enter into the ``idrac_telemetry_db``, use the following command: ::

        use idrac_telemetrydb;

    5. To access the services table: ::
        
        Select * from services;