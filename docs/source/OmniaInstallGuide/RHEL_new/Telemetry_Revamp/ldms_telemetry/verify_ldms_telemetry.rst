Verify LDMS Telemetry
======================

This section outlines the steps to validate LDMS telemetry services.

Verify LDMS Messages in Kafka
-----------------------------

To verify that LDMS telemetry data is being successfully published to the ``ldms`` Kafka topic, do the following:

1. Log in to the Service Kubernetes Control plane.

2. Create a Kafka consumer using the following command::

    KAFKA_LB_IP=<external load balancer IP of the bridge-bridge-lb service>
    curl -X POST http://$KAFKA_LB_IP:8080/consumers/ldms-consumer-group \
    -H 'content-type: application/vnd.kafka.v2+json' \
    -d '{
            "name": "ldms-consumer-1",
            "format": "json",
            "auto.offset.reset": "latest",
            "enable.auto.commit": true
        }'

3. Subscribe the consumer to the LDMS topic using the following command::

    curl -X POST http://$KAFKA_LB_IP:8080/consumers/ldms-consumer-group/instances/ldms-consumer-1/subscription \
    -H 'content-type: application/vnd.kafka.v2+json' \
    -d '{"topics": ["ldms"]}'

4. Consume messages from the topic using the following command::

    while true; do curl -X GET http://$KAFKA_LB_IP:8080/consumers/ldms-consumer-group/instances/ldms-consumer-1/records \
    -H 'accept: application/vnd.kafka.json.v2+json' | jq '.' ;  sleep 2; done

If telemetry is flowing correctly, the output contains JSON-formatted LDMS telemetry records.

.. note:: When new nodes are added, ensure the nodes are up and cloud-init has completed successfully (check /var/log/cloud-init-output.log on each node). Then, create a new Kafka consumer group with a unique name (e.g., ldms-new-nodes-group) to verify metrics from the newly added nodes. Wait 2-3 minutes after discovery completes before checking.
