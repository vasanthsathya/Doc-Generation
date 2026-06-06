

Telemetry Issues
================


Issues related to the telemetry pipeline: iDRAC metrics collection, LDMS
samplers, Kafka message streaming, VictoriaMetrics storage, and Grafana
dashboards.


iDRAC not sending telemetry data
--------------------------------


**Symptom**

No iDRAC metrics appear in VictoriaMetrics or Grafana dashboards. The
telemetry pipeline shows no incoming data from server BMCs.

**Cause**

- The iDRAC does not have a **Datacenter** license, which is required for
    telemetry streaming.
- Redfish telemetry subscriptions are not configured on the iDRAC.
- Network connectivity between the iDRAC BMC network and the telemetry
    collector is blocked.
- The iDRAC firmware is outdated and does not support Redfish telemetry.

**Resolution**

1. **Verify the iDRAC license** includes Datacenter features:

.. code-block:: bash

   racadm -r <bmc_ip> -u <user> -p <pass> license view

Look for ``iDRAC Datacenter License`` in the output. If not present,
install the appropriate license.

2. **Check Redfish telemetry support:**

.. code-block:: bash

   curl -k -u <user>:<pass> \
     https://<bmc_ip>/redfish/v1/TelemetryService

A ``404`` response indicates the firmware does not support telemetry.
Update iDRAC firmware to the latest version.

3. **Verify telemetry subscriptions:**

.. code-block:: bash

   curl -k -u <user>:<pass> \
     https://<bmc_ip>/redfish/v1/EventService/Subscriptions

4. **Test network connectivity** from the OIM to the BMC:

.. code-block:: bash

   ping <bmc_ip>
   curl -k https://<bmc_ip>/redfish/v1/

5. If subscriptions are missing, re-run the telemetry playbook:

.. code-block:: bash

   ssh omnia_core
   cd /omnia
   ansible-playbook playbooks/telemetry.yml




LDMS sampler failures
---------------------


**Symptom**

LDMS (Lightweight Distributed Metric Service) samplers on compute nodes are
not collecting or forwarding metrics. The ``ldmsd`` service may be in a
failed state.

**Cause**

- The ``ldmsd`` daemon is not running on the compute node.
- The sampler configuration references a metric set that is not available on
  the node (for example, GPU metrics on a non-GPU node).
- The aggregator endpoint is unreachable from the compute node.

**Resolution**

1. Check ``ldmsd`` status on the compute node:

.. code-block:: bash

   ssh <compute_node> systemctl status ldmsd

2. Review LDMS logs:

.. code-block:: bash

   ssh <compute_node> cat /var/log/ldmsd.log

3. Verify the sampler configuration:

.. code-block:: bash

   ssh <compute_node> cat /etc/ldms/ldmsd.conf

4. Test connectivity to the aggregator:

.. code-block:: bash

   ssh <compute_node> nc -zv <aggregator_ip> <aggregator_port>

5. Restart the LDMS daemon:

.. code-block:: bash

   ssh <compute_node> systemctl restart ldmsd




Kafka connection issues
-----------------------


**Symptom**

Telemetry data producers (iDRAC collectors, LDMS aggregators) cannot connect
to Kafka. Logs show connection refused or timeout errors.

**Cause**

- The Kafka container or service is not running.
- Kafka listeners are misconfigured (wrong advertised address or port).
- ZooKeeper (or KRaft controller) is not running.
- Firewall rules block Kafka ports (default: 9092).

**Resolution**

1. Verify Kafka is running:

.. code-block:: bash

   # If Kafka runs as a Podman container
   podman ps | grep kafka

   # If Kafka runs as a Kubernetes pod
   kubectl get pods -n telemetry | grep kafka

2. Check Kafka logs:

.. code-block:: bash

   podman logs kafka 2>&1 | tail -50

3. Verify Kafka listeners:

.. code-block:: bash

   # Test Kafka port
   nc -zv <kafka_host> 9092

4. Check ZooKeeper status:

.. code-block:: bash

   podman ps | grep zookeeper
   podman logs zookeeper 2>&1 | tail -50

5. If Kafka's advertised listeners are wrong, update the configuration:

.. code-block:: bash

   # In Kafka's server.properties or environment variables
   KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://<oim_ip>:9092

6. Restart Kafka:

.. code-block:: bash

   podman restart kafka




VictoriaMetrics not receiving data
----------------------------------


**Symptom**

VictoriaMetrics shows no recent data points. Grafana dashboards display
``No data`` or stale values.

**Cause**

- The VictoriaMetrics container is not running.
- The Kafka-to-VictoriaMetrics consumer is not running or is misconfigured.
- Disk space on the VictoriaMetrics storage volume is exhausted.
- Ingestion rate limits are rejecting data.

**Resolution**

1. Verify VictoriaMetrics is running:

.. code-block:: bash

   podman ps | grep victoria
   # or
   kubectl get pods -n telemetry | grep victoria

2. Check VictoriaMetrics health:

.. code-block:: bash

   curl http://<victoria_host>:8428/health

3. Verify data is being ingested:

.. code-block:: bash

   # Check the number of active time series
   curl http://<victoria_host>:8428/api/v1/status/tsdb

4. Check disk space:

.. code-block:: bash

   df -h <victoria_data_dir>

5. Check the Kafka consumer that feeds VictoriaMetrics:

.. code-block:: bash

   podman logs <kafka_consumer_container> 2>&1 | tail -50

6. If disk is full, increase storage or reduce retention:

.. code-block:: bash

   # Adjust retention period (e.g., 30 days)
   # Add to VictoriaMetrics startup flags: -retentionPeriod=30d




Grafana dashboards empty
------------------------


**Symptom**

Grafana is accessible but dashboards show no data, ``No data`` messages, or
broken panels.

**Cause**

- The VictoriaMetrics data source is not configured in Grafana.
- The data source URL is incorrect.
- VictoriaMetrics itself has no data (see above).
- Dashboard queries reference metric names that do not exist in the
  current data.

**Resolution**

1. Verify the Grafana data source:

- Navigate to **Grafana** > **Configuration** > **Data Sources**.
- Confirm a Prometheus-compatible data source points to
  ``http://<victoria_host>:8428``.
- Click **Test** to verify connectivity.

2. If no data source exists, add one:

.. code-block:: bash

   curl -X POST http://admin:admin@<grafana_host>:3000/api/datasources \
     -H 'Content-Type: application/json' \
     -d '{
       "name": "VictoriaMetrics",
       "type": "prometheus",
       "url": "http://<victoria_host>:8428",
       "access": "proxy",
       "isDefault": true
     }'

3. Verify metrics exist in VictoriaMetrics:

.. code-block:: bash

   curl 'http://<victoria_host>:8428/api/v1/label/__name__/values' | jq '.'

4. Re-import Omnia default dashboards if they are missing:

.. code-block:: bash

   ssh omnia_core
   cd /omnia
   ansible-playbook playbooks/telemetry.yml --tags grafana_dashboards




.. note::


   - :doc:`Setup Telemetry <../HowTo/Telemetry/setup_telemetry>` -- Telemetry pipeline setup.
   - :doc:`Verify Telemetry <../HowTo/Telemetry/verify_telemetry>` -- Verification procedures.
   - :doc:`Log Management <../Operations/log_management>` -- Log locations for telemetry services.

