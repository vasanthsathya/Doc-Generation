# Telemetry Issues

Issues related to the telemetry pipeline: iDRAC metrics collection, LDMS samplers, Kafka message streaming, VictoriaMetrics storage, and Grafana dashboards.

## iDRAC not sending telemetry data

No iDRAC metrics appear in VictoriaMetrics or Grafana dashboards. The telemetry pipeline shows no incoming data from server BMCs.

 * The iDRAC does not have a **Datacenter** license, which is required for telemetry streaming.
 * Redfish telemetry subscriptions are not configured on the iDRAC.
 * Network connectivity between the iDRAC BMC network and the telemetry collector is blocked.
 * The iDRAC firmware is outdated and does not support Redfish telemetry.

 1. **Verify the iDRAC license** includes Datacenter features:

 racadm -r <bmc_ip> -u <user> -p <pass> license view

Look for `iDRAC Datacenter License` in the output. If not present, install the appropriate license.

 1. **Check Redfish telemetry support:**

 curl -k -u <user>:<pass> \
 https://<bmc_ip>/redfish/v1/TelemetryService

A `404` response indicates the firmware does not support telemetry. Update iDRAC firmware to the latest version.

 1. **Verify telemetry subscriptions:**

 curl -k -u <user>:<pass> \
 https://<bmc_ip>/redfish/v1/EventService/Subscriptions

 1. **Test network connectivity** from the OIM to the BMC:

 ping <bmc_ip>
 curl -k https://<bmc_ip>/redfish/v1/

 1. If subscriptions are missing, re-run the telemetry playbook:

 ssh omnia_core
 cd /omnia
 ansible-playbook playbooks/telemetry.yml

## LDMS sampler failures

LDMS (Lightweight Distributed Metric Service) samplers on compute nodes are not collecting or forwarding metrics. The `ldmsd` service may be in a failed state.

 * The `ldmsd` daemon is not running on the compute node.
 * The sampler configuration references a metric set that is not available on the node (for example, GPU metrics on a non-GPU node).
 * The aggregator endpoint is unreachable from the compute node.

 1. Check `ldmsd` status on the compute node:

 ssh <compute_node> systemctl status ldmsd

 1. Review LDMS logs:

 ssh <compute_node> cat /var/log/ldmsd.log

 1. Verify the sampler configuration:

 ssh <compute_node> cat /etc/ldms/ldmsd.conf

 1. Test connectivity to the aggregator:

 ssh <compute_node> nc -zv <aggregator_ip> <aggregator_port>

 1. Restart the LDMS daemon:

 ssh <compute_node> systemctl restart ldmsd

## Kafka connection issues

Telemetry data producers (iDRAC collectors, LDMS aggregators) cannot connect to Kafka. Logs show connection refused or timeout errors.

 * The Kafka container or service is not running.
 * Kafka listeners are misconfigured (wrong advertised address or port).
 * ZooKeeper (or KRaft controller) is not running.
 * Firewall rules block Kafka ports (default: 9092).

 1. Verify Kafka is running:

 # If Kafka runs as a Podman container
 podman ps | grep kafka

 # If Kafka runs as a Kubernetes pod
 kubectl get pods -n telemetry | grep kafka

 1. Check Kafka logs:

 podman logs kafka 2>&1 | tail -50

 1. Verify Kafka listeners:

 # Test Kafka port
 nc -zv <kafka_host> 9092

 1. Check ZooKeeper status:

 podman ps | grep zookeeper
 podman logs zookeeper 2>&1 | tail -50

 1. If Kafka's advertised listeners are wrong, update the configuration:

 # In Kafka's server.properties or environment variables
 KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://<oim_ip>:9092

 1. Restart Kafka:

 podman restart kafka

## VictoriaMetrics not receiving data

VictoriaMetrics shows no recent data points. Grafana dashboards display `No data` or stale values.

 * The VictoriaMetrics container is not running.
 * The Kafka-to-VictoriaMetrics consumer is not running or is misconfigured.
 * Disk space on the VictoriaMetrics storage volume is exhausted.
 * Ingestion rate limits are rejecting data.

 1. Verify VictoriaMetrics is running:

 podman ps | grep victoria
 # or
 kubectl get pods -n telemetry | grep victoria

 1. Check VictoriaMetrics health:

 curl http://<victoria_host>:8428/health

 1. Verify data is being ingested:

 # Check the number of active time series
 curl http://<victoria_host>:8428/api/v1/status/tsdb

 1. Check disk space:

 df -h <victoria_data_dir>

 1. Check the Kafka consumer that feeds VictoriaMetrics:

 podman logs <kafka_consumer_container> 2>&1 | tail -50

 1. If disk is full, increase storage or reduce retention:

 # Adjust retention period (e.g., 30 days)
 # Add to VictoriaMetrics startup flags: -retentionPeriod=30d

## Grafana dashboards empty

Grafana is accessible but dashboards show no data, `No data` messages, or broken panels.

 * The VictoriaMetrics data source is not configured in Grafana.
 * The data source URL is incorrect.
 * VictoriaMetrics itself has no data (see above).
 * Dashboard queries reference metric names that do not exist in the current data.

 1. Verify the Grafana data source:

 2. Navigate to **Grafana > Configuration > Data Sources**.

 3. Confirm a Prometheus-compatible data source points to `http://<victoria_host>:8428`.
 4. Click **Test** to verify connectivity.

 5. If no data source exists, add one:

 curl -X POST http://admin:admin@<grafana_host>:3000/api/datasources \
 -H 'Content-Type: application/json' \
 -d '{
 "name": "VictoriaMetrics",
 "type": "prometheus",
 "url": "http://<victoria_host>:8428",
 "access": "proxy",
 "isDefault": true
 }'

 1. Verify metrics exist in VictoriaMetrics:

 curl 'http://<victoria_host>:8428/api/v1/label/__name__/values' | jq '.'

 1. Re-import Omnia default dashboards if they are missing:

 ssh omnia_core
 cd /omnia
 ansible-playbook playbooks/telemetry.yml --tags grafana_dashboards

Copyright © 2025 Dell Technologies. All rights reserved.