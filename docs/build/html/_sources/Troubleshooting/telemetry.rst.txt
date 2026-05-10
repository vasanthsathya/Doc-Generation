

Telemetry Issues
================


Issues related to the telemetry pipeline: iDRAC metrics collection, LDMS
samplers, Kafka message streaming, VictoriaMetrics storage, and Grafana
dashboards.


iDRAC not sending telemetry data
--------------------------------


???+ note "Symptom"

    No iDRAC metrics appear in VictoriaMetrics or Grafana dashboards. The
    telemetry pipeline shows no incoming data from server BMCs.

??? note "Cause"

    - The iDRAC does not have a **Datacenter** license, which is required for
      telemetry streaming.
    - Redfish telemetry subscriptions are not configured on the iDRAC.
    - Network connectivity between the iDRAC BMC network and the telemetry
      collector is blocked.
    - The iDRAC firmware is outdated and does not support Redfish telemetry.

??? note "Resolution"

    #. **Verify the iDRAC license** includes Datacenter features:


.. code-block:: bash

          racadm -r <bmc_ip> -u <user> -p <pass> license view



       Look for ``iDRAC Datacenter License`` in the output. If not present,
       install the appropriate license.

    #. **Check Redfish telemetry support:**


.. code-block:: bash

          curl -k -u <user>:<pass> \
            https://<bmc_ip>/redfish/v1/TelemetryService



       A ``404`` response indicates the firmware does not support telemetry.
       Update iDRAC firmware to the latest version.

    #. **Verify telemetry subscriptions:**


.. code-block:: bash

          curl -k -u <user>:<pass> \
            https://<bmc_ip>/redfish/v1/EventService/Subscriptions



    #. **Test network connectivity** from the OIM to the BMC:


.. code-block:: bash

          ping <bmc_ip>
          curl -k https://<bmc_ip>/redfish/v1/



    #. If subscriptions are missing, re-run the telemetry playbook:


.. code-block:: bash

          ssh omnia_core
          cd /omnia
          ansible-playbook playbooks/telemetry.yml




LDMS sampler failures
---------------------


???+ note "Symptom"

    LDMS (Lightweight Distributed Metric Service) samplers on compute nodes are
    not collecting or forwarding metrics. The ``ldmsd`` service may be in a
    failed state.

??? note "Cause"

    - The ``ldmsd`` daemon is not running on the compute node.
    - The sampler configuration references a metric set that is not available on
      the node (for example, GPU metrics on a non-GPU node).
    - The aggregator endpoint is unreachable from the compute node.

??? note "Resolution"

    #. Check ``ldmsd`` status on the compute node:


.. code-block:: bash

          ssh <compute_node> systemctl status ldmsd



    #. Review LDMS logs:


.. code-block:: bash

          ssh <compute_node> cat /var/log/ldmsd.log



    #. Verify the sampler configuration:


.. code-block:: bash

          ssh <compute_node> cat /etc/ldms/ldmsd.conf



    #. Test connectivity to the aggregator:


.. code-block:: bash

          ssh <compute_node> nc -zv <aggregator_ip> <aggregator_port>



    #. Restart the LDMS daemon:


.. code-block:: bash

          ssh <compute_node> systemctl restart ldmsd




Kafka connection issues
-----------------------


???+ note "Symptom"

    Telemetry data producers (iDRAC collectors, LDMS aggregators) cannot connect
    to Kafka. Logs show connection refused or timeout errors.

??? note "Cause"

    - The Kafka container or service is not running.
    - Kafka listeners are misconfigured (wrong advertised address or port).
    - ZooKeeper (or KRaft controller) is not running.
    - Firewall rules block Kafka ports (default: 9092).

??? note "Resolution"

    #. Verify Kafka is running:


.. code-block:: bash

          # If Kafka runs as a Podman container
          podman ps | grep kafka
   
          # If Kafka runs as a Kubernetes pod
          kubectl get pods -n telemetry | grep kafka



    #. Check Kafka logs:


.. code-block:: bash

          podman logs kafka 2>&1 | tail -50



    #. Verify Kafka listeners:


.. code-block:: bash

          # Test Kafka port
          nc -zv <kafka_host> 9092



    #. Check ZooKeeper status:


.. code-block:: bash

          podman ps | grep zookeeper
          podman logs zookeeper 2>&1 | tail -50



    #. If Kafka's advertised listeners are wrong, update the configuration:


.. code-block:: bash

          # In Kafka's server.properties or environment variables
          KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://<oim_ip>:9092



    #. Restart Kafka:


.. code-block:: bash

          podman restart kafka




VictoriaMetrics not receiving data
----------------------------------


???+ note "Symptom"

    VictoriaMetrics shows no recent data points. Grafana dashboards display
    ``No data`` or stale values.

??? note "Cause"

    - The VictoriaMetrics container is not running.
    - The Kafka-to-VictoriaMetrics consumer is not running or is misconfigured.
    - Disk space on the VictoriaMetrics storage volume is exhausted.
    - Ingestion rate limits are rejecting data.

??? note "Resolution"

    #. Verify VictoriaMetrics is running:


.. code-block:: bash

          podman ps | grep victoria
          # or
          kubectl get pods -n telemetry | grep victoria



    #. Check VictoriaMetrics health:


.. code-block:: bash

          curl http://<victoria_host>:8428/health



    #. Verify data is being ingested:


.. code-block:: bash

          # Check the number of active time series
          curl http://<victoria_host>:8428/api/v1/status/tsdb



    #. Check disk space:


.. code-block:: bash

          df -h <victoria_data_dir>



    #. Check the Kafka consumer that feeds VictoriaMetrics:


.. code-block:: bash

          podman logs <kafka_consumer_container> 2>&1 | tail -50



    #. If disk is full, increase storage or reduce retention:


.. code-block:: bash

          # Adjust retention period (e.g., 30 days)
          # Add to VictoriaMetrics startup flags: -retentionPeriod=30d




Grafana dashboards empty
------------------------


???+ note "Symptom"

    Grafana is accessible but dashboards show no data, ``No data`` messages, or
    broken panels.

??? note "Cause"

    - The VictoriaMetrics data source is not configured in Grafana.
    - The data source URL is incorrect.
    - VictoriaMetrics itself has no data (see above).
    - Dashboard queries reference metric names that do not exist in the
      current data.

??? note "Resolution"

    #. Verify the Grafana data source:

      - Navigate to **Grafana > Configuration > Data Sources**.
      - Confirm a Prometheus-compatible data source points to
         ``http://<victoria_host>:8428``.
      - Click **Test** to verify connectivity.

    #. If no data source exists, add one:


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



    #. Verify metrics exist in VictoriaMetrics:


.. code-block:: bash

          curl 'http://<victoria_host>:8428/api/v1/label/__name__/values' | jq '.'



    #. Re-import Omnia default dashboards if they are missing:


.. code-block:: bash

          ssh omnia_core
          cd /omnia
          ansible-playbook playbooks/telemetry.yml --tags grafana_dashboards




.. note::


   - `Setup Telemetry <../HowTo/Telemetry/setup_telemetry.rst>`_ -- Telemetry pipeline setup.
   - `Verify Telemetry <../HowTo/Telemetry/verify_telemetry.rst>`_ -- Verification procedures.
   - `Log Management <../Operations/log_management.rst>`_ -- Log locations for telemetry services.

