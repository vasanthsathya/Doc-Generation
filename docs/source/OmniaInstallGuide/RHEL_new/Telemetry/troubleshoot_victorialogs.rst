.. _troubleshoot-victorialogs:

.. versionadded:: 2.2

.. note::
   This topic is pending SME validation. Content may change before publication.

Troubleshoot VictoriaLogs
==========================

Troubleshoot common issues with VictoriaLogs deployment, log ingestion, and querying to maintain observability of your cluster.

Prerequisites
-------------

Before troubleshooting VictoriaLogs:

* Ensure that VictoriaLogs cluster is deployed (see :doc:`deploy_victorialogs`)


Component Health Issues
------------------------

**VictoriaLogs Pods Not Reaching Healthy State**

If VictoriaLogs pods fail to reach a healthy state:

1. Check pod status and identify the failing component.

   .. code-block:: bash

      kubectl get pods -n telemetry

2. Check pod logs for error messages.

   .. code-block:: bash

      kubectl logs <pod-name> -n telemetry

3. Verify TLS certificate configuration.

   .. code-block:: bash

      kubectl get secret victoria-tls-certs -n telemetry

4. Check resource limits and ensure sufficient CPU and memory are allocated.

   .. code-block:: bash

      kubectl describe pod <pod-name> -n telemetry

.. note::
   VictoriaLogs cluster mode is relatively new in upstream. Pin to a tested release for production deployments.

Log Ingestion Issues
--------------------

**Logs Not Appearing in VictoriaLogs**

If logs from external sources do not appear in VictoriaLogs:

1. Verify log source configuration.

   * Confirm syslog forwarding is configured with the correct endpoint
   * Confirm HTTP forwarding uses the correct URL and format
   * Check device logs for connection errors

2. Check network connectivity to VLAgent.

   .. code-block:: bash

      telnet <LoadBalancer IP> 514
      telnet <LoadBalancer IP> 6514

3. Verify TLS handshake for encrypted sources.

   .. code-block:: bash

      openssl s_client -connect <LoadBalancer IP>:6514 -showcerts

4. Check VLAgent pod logs for ingestion errors.

   .. code-block:: bash

      kubectl logs vlagent -n telemetry

Query Access Issues
-------------------

**Query Endpoint Not Accessible**

If the query endpoint is not accessible:

1. Verify LoadBalancer service type.

   .. code-block:: bash

      kubectl get svc vlselect-victoria-logs-cluster -n telemetry

2. Check MetalLB configuration if LoadBalancer type is used.

   .. code-block:: bash

      kubectl get configmap config -n metallb-system

3. Verify TLS certificate SANs include the LoadBalancer IP.

   .. code-block:: bash

      openssl x509 -in victoria-ca.crt -text -noout

4. Check vlselect pod health.

   .. code-block:: bash

      kubectl get pods -n telemetry | grep vlselect

Storage Issues
--------------

**Storage Space Exhaustion**

If PVC storage is exhausted:

1. Check PVC utilization.

   .. code-block:: bash

      kubectl get pvc -n telemetry

2. Check vlstorage PVC usage.

   .. code-block:: bash

      kubectl exec -it <vlstorage-pod> -n telemetry -- df -h

3. Adjust retention period or storage size in ``telemetry_config.yml``.

   .. code-block:: yaml

      victoria_logs_configurations:
        retention_period: 168  # Reduce retention if needed
        storage_size: 16Gi     # Increase storage if needed

4. Redeploy telemetry configuration.

   .. code-block:: bash

      cd /opt/omnia/telemetry
      ansible-playbook discovery.yml

.. important::
   vlstorage PVCs persist after StatefulSet deletion. Manual cleanup is required during teardown.

Performance Issues
------------------

**High Query Latency**

If query performance is slow:

1. Check the time range in your query. Narrow the range for faster results.

   .. code-block:: text

      {time:1h}  # Use smaller time ranges

2. Verify vlselect pod health and resource usage.

   .. code-block:: bash

      kubectl top pods -n telemetry | grep vlselect

3. Check if vlselect pods are under heavy load.

   .. code-block:: bash

      kubectl describe pod <vlselect-pod> -n telemetry

4. Consider increasing vlselect replica count if query load is high.

.. AI_REVIEW::
   Troubleshooting steps require SME validation against real deployment scenarios. The steps above provide general guidance; actual resolution steps may vary based on specific deployment configurations.

Related Topics
--------------

* :doc:`deploy_victorialogs` — Deploy VictoriaLogs cluster mode
* :doc:`configure_victorialogs_sources` — Configure log sources for VictoriaLogs
* :doc:`query_victorialogs` — Query logs with VictoriaLogs
