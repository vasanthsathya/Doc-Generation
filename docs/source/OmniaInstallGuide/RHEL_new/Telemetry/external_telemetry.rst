===========================================
Collect Telemetry Data from External Nodes
===========================================

This section describes how to create a Kafka topic in the Omnia Service Kubernetes cluster
and configure an external telemetry producer to stream metrics securely into the Service Clusters using mutual TLS (mTLS).

This procedure assumes that Kafka is deployed using Strimzi inside the telemetry namespace of the service cluster. For more details, see
`Strimzi Kafka Operator Documentation <https://strimzi.io/docs/operators/latest/overview>`_


Prerequisites
---------------

Ensure the following prerequisites are met before proceeding:

* Kafka is deployed using Strimzi in the ``telemetry`` namespace.
* External access to Kafka is available through a LoadBalancer on port ``9094``.
* mTLS authentication is configured and a KafkaUser identity (``kafkapump``) exists.
* A Kafka Pump is available outside the Kubernetes cluster, running on Podman or Docker.


Create a Kafka Topic
-------------------------

1. Create a file named ``kafka.topic_name.yaml`` with the parameters such as topic name, number of partitions, 
   replication factor, and retention policies::

       apiVersion: kafka.strimzi.io/v1beta2
       kind: KafkaTopic
       metadata:
         name: topic_name
         namespace: telemetry
         labels:
           strimzi.io/cluster: "kafka"
       spec:
         partitions: 2
         replicas: 2
         config:
           cleanup.policy: delete

   Replace ``topic_name`` with the desired Kafka topic name.

2. On the Service Kube Control plane, run::

       kubectl apply -f kafka.topic_name.yaml

3. To verify that the topic was created, run the following command::

       kubectl get kafkatopics -n telemetry


Establish Secure Connection
------------------------------

1. On the external client host, create a working directory::

       mkdir -p ~/kafka-mtls-test
       cd ~/kafka-mtls-test

2. Retrieve the Kafka LoadBalancer IP::

       kubectl get svc -n telemetry kafka-kafka-external-bootstrap -o wide

   Optionally, to export the IP for later use, run the following command.::

       export KAFKA_LB_IP=$(kubectl get svc kafka-kafka-external-bootstrap -n telemetry -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
       echo "Kafka Load Balancer: ${KAFKA_LB_IP}:9094"

   You can reuse ``${KAFKA_LB_IP}:9094`` in all Kafka client commands.

3. Run the following commands to extract certificates required for mTLS::

       kubectl get secret kafka-cluster-ca-cert -n telemetry -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt
       kubectl get secret kafkapump -n telemetry -o jsonpath='{.data.user\.crt}' | base64 -d > user.crt
       kubectl get secret kafkapump -n telemetry -o jsonpath='{.data.user\.key}' | base64 -d > user.key

4. Run the following commands to create Java truststore and keystore::

       keytool -import -trustcacerts -alias kafka-ca -file ca.crt \
         -keystore kafka.truststore.jks -storepass changeit -noprompt

       openssl pkcs12 -export -in user.crt -inkey user.key \
         -out kafkapump.p12 -name kafkapump -password pass:changeit

       keytool -importkeystore \
         -srckeystore kafkapump.p12 -srcstoretype PKCS12 -srcstorepass changeit \
         -destkeystore kafka.keystore.jks -deststorepass changeit -noprompt

.. note::  The steps for converting certificates into JKS format are required **only for Java-based Kafka clients**. If your client does not use a Java keystore (JKS), these conversion steps are not necessary.


5. Create the client SSL configuration file::

       cat > producer-mtls.properties << 'EOF'
       security.protocol=SSL
       ssl.truststore.location=/certs/kafka.truststore.jks
       ssl.truststore.password=changeit
       ssl.keystore.location=/certs/kafka.keystore.jks
       ssl.keystore.password=changeit
       ssl.key.password=changeit
       ssl.endpoint.identification.algorithm=
       EOF

6. Run a Kafka tools container with certificates mounted::

       podman run -it --rm \
         --name kafka-mtls-producer \
         -v ~/kafka-mtls-test:/certs:ro \
         apache/kafka:4.1.0 bash


Produce and Verify Telemetry Data
----------------------------------------

1. Inside the Kafka tools container container, produce test data to the Kafka topic that you have created::

       /opt/kafka/bin/kafka-console-producer.sh \
         --bootstrap-server ${KAFKA_LB_IP}:9094 \
         --topic <kafka topic> \
         --producer.config /certs/producer-mtls.properties

   Type messages such as::

       {"event":"test1","source":"manual","ts":"2025-11-20T08:55:00Z"}
       {"event":"test2","source":"manual","ts":"2025-11-20T08:56:00Z"}
       hello world
      

2. In a new terminal, verify if the messages are recieved::

       /opt/kafka/bin/kafka-console-consumer.sh \
         --bootstrap-server ${KAFKA_LB_IP}:9094 \
         --consumer.config /certs/producer-mtls.properties \
         --topic <kafka topic> \
         --group <kafka topic>-consumer-group \
         --from-beginning

   You can view the messages in JSON format.

