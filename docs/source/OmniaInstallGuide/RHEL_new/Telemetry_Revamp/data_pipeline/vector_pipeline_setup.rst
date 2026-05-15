Vector Pipeline Setup
=====================

Using Omnia, you can deploy Vector as a high-performance data pipeline tool for collecting, transforming, and routing telemetry data from LDMS and OpenManage Enterprise (OME) sources to VictoriaMetrics and VictoriaLogs. The deployment includes Vector-LDMS and Vector-OME pods as Kafka consumers, vmagent-vector as a dedicated write-buffer for metrics, and vlagent-vector as a log forwarding agent.

Vector provides the following components:

- **Vector-LDMS:** Kafka consumer for LDMS metrics, consumes from the `ldms` topic and routes to VictoriaMetrics via vmagent-vector
- **Vector-OME:** Kafka consumer for OME telemetry, consumes from `ome.*` topics and routes metrics to VictoriaMetrics and logs to VictoriaLogs
- **vmagent-vector:** Dedicated vmagent instance as a write-buffer between Vector pods and vminsert. Accepts `prometheus_remote_write` on port 8429, buffers to disk, and forwards to vminsert. Separate from the existing scraper vmagent to isolate failure domains.
- **vlagent-vector:** Dedicated VictoriaLogs forwarding agent deployed as a log write-buffer for Vector pods. Accepts JSON Lines on an HTTP endpoint (port 9427), buffers to disk, and forwards to vlinsert. Required for Vector-OME log/event sinks.

For more details on Vector, see `Vector Documentation <https://vector.dev/docs/>`_

Vector enables the following data flows:

- **LDMS metrics:** LDMS Store (store_avro_kafka) → Kafka 'ldms' topic → Vector-LDMS → vmagent-vector → vminsert → VictoriaMetrics
- **OME metrics:** OME → Kafka 'ome.*' topics → Vector-OME → vmagent-vector → vminsert → VictoriaMetrics
- **OME logs:** OME → Kafka 'ome.*' topics → Vector-OME → vlagent-vector → vlinsert → VictoriaLogs

.. note:: Vector-iDRAC support is deferred to a future release. The current Dell iDRAC telemetry produces to a single `idrac` topic with mixed metrics and events, which is insufficient for proper Vector routing. Omnia will adopt the NERSC iDRAC collector in a future release to enable Vector-iDRAC support.

Prerequisites
---------------

* Ensure that the ``provision.yml`` playbook has been executed successfully with ``service_kube_control_plane`` and ``service_kube_node`` in the mapping file.
* Ensure that Kafka is deployed and operational via Strimzi operator.
* Ensure that VictoriaMetrics cluster mode is deployed with vminsert, vmstorage, and vmselect components.
* Ensure that VictoriaLogs cluster mode is deployed with vlinsert, vlstorage, and vlselect components (required for Vector-OME logs).

Steps
-------

1. Specify the following entries in the ``software_config.json``. If any entry is missing, Omnia skips Vector deployment and logs an informational message.
   For more information, see :doc:`../CreateLocalRepo/InputParameters`.

.. code-block:: json

    {"name": "service_k8s", "version": "1.34.1", "arch": ["x86_64"]}

2. Configure the ``telemetry_config.yml`` to enable Vector telemetry bridges:

   .. note:: Vector telemetry bridges are controlled by feature flags in ``telemetry_config.yml``. Set ``vector_ldms_support`` to enable Vector-LDMS, and ``vector_ome_support`` to enable Vector-OME.

    .. csv-table:: telemetry_config.yml
        :file: ../../../../Tables/telemetry_config.csv
        :header-rows: 1
        :keepspace:

3. For Vector-LDMS, ensure that LDMS is configured and the ``store_avro_kafka`` plugin is producing to the Kafka `ldms` topic. Vector-LDMS consumes from this topic.

4. For Vector-OME, ensure that OME is configured externally and producing to Kafka `ome.*` topics via the external mTLS listener (port 9094). Run the ``external_kafka_connect_details.yml`` playbook to configure OME connectivity.

5. Run the ``telemetry.yml`` playbook to deploy Vector components::

    cd /opt/omnia/telemetry
    ansible-playbook telemetry.yml

The playbook deploys the following components based on the configured feature flags:

- **vmagent-vector:** Dedicated vmagent instance as a write-buffer (deployed when any Vector pipeline is enabled)
- **Vector-LDMS:** Kafka consumer for LDMS metrics (deployed when ``vector_ldms_support=true``)
- **Vector-OME:** Kafka consumer for OME telemetry (deployed when ``vector_ome_support=true``)
- **vlagent-vector:** VictoriaLogs forwarding agent for logs (deployed when ``vector_ome_support=true``)
- **Kafka topics and ACLs:** For OME topics (deployed when ``vector_ome_support=true``)
- **KafkaUser resources:** For Vector-OME mTLS credentials (deployed when ``vector_ome_support=true``)

.. note:: Vector-LDMS reuses the existing ``kafkapump`` KafkaUser for mTLS credentials. Vector-OME requires a new KafkaUser (``vector-ome-user``) because OME is an external producer with a different security domain.

Verification
------------

After successful deployment, verify the Vector components:

1. Verify that the Vector pods are running::

    kubectl get pods -n telemetry -l app=vector

2. Verify that the vmagent-vector pod is running::

    kubectl get pods -n telemetry -l app=vmagent-vector

3. Verify that the vlagent-vector pod is running (if Vector-OME is enabled)::

    kubectl get pods -n telemetry -l app=vlagent-vector

4. Verify that Kafka consumer groups are registered::

    kubectl get kafkagroups -n telemetry

5. Verify data flow by checking Kafka topic offsets and Vector pod logs::

    kubectl logs -n telemetry <vector-pod-name> -c vector

6. Verify that metrics are reaching VictoriaMetrics by querying the VMUI or using PromQL queries.

7. Verify that logs are reaching VictoriaLogs by using LogsQL queries in the VictoriaLogs UI (if Vector-OME is enabled).

Troubleshooting
---------------

For common Vector telemetry issues and troubleshooting steps, see :doc:`../../troubleshootingguide` and refer to the `Vector Troubleshooting Documentation <https://vector.dev/docs/guides/troubleshooting/>`_.

Related Topics
--------------

* :doc:`../idrac_telemetry/idrac_configuration` - Service Cluster Telemetry Configuration
* :doc:`../ldms_telemetry/ldms_configuration` - LDMS Telemetry Configuration
* :doc:`../powerscale_telemetry/powerscale_configuration` - PowerScale Telemetry Configuration
* :doc:`../../../reference/telemetry/telemetry_config` - Telemetry Configuration Reference
