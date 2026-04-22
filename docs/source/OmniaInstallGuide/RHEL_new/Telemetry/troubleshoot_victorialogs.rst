.. _troubleshoot-victorialogs:

.. note::
   This topic is pending SME validation. Content may change before publication.

Troubleshooting VictoriaLogs
============================

This section provides common issues and solutions for VictoriaLogs deployment, log ingestion, and querying.

Component Health Issues
-----------------------

**Issue: VictoriaLogs components not reaching healthy state**

#. Check pod status and logs.

   .. code-block:: bash

       kubectl get pods -n telemetry
       kubectl logs <pod-name> -n telemetry

   Look for error messages in the pod logs that indicate the cause of the failure.

#. Verify TLS certificate configuration.

   Ensure that the ``victoria-tls-certs`` secret exists and contains the correct certificates:

   .. code-block:: bash

       kubectl get secret victoria-tls-certs -n telemetry

   Verify that the certificates include VictoriaLogs SANs (vlinsert, vlselect, vlstorage).

#. Check resource limits.

   Verify that the pods are not resource-constrained:

   .. code-block:: bash

       kubectl describe pod <pod-name> -n telemetry

   Look for OOMKilled or resource limit errors.

Log Ingestion Issues
--------------------

**Issue: Logs not appearing in VictoriaLogs**

#. Verify log source configuration.

   Ensure that your log sources are configured to send logs to the correct VLAgent endpoint (port 514 for plaintext, port 6514 for TLS).

#. Check network connectivity to VLAgent.

   Verify that the log sources can reach the Service Kubernetes cluster:

   .. code-block:: bash

       telnet <VLAgent-LoadBalancer-IP> 514

   Replace ``<VLAgent-LoadBalancer-IP>`` with the actual LoadBalancer IP.

#. Verify TLS handshake for encrypted sources.

   For TLS syslog connections, ensure that the CA certificate is correctly configured on the log source:

   .. code-block:: bash

       openssl s_client -connect <VLAgent-LoadBalancer-IP>:6514 -CAfile victoria-ca.crt

Query Access Issues
--------------------

**Issue: Query endpoint not accessible**

#. Verify LoadBalancer service type.

   Ensure that the vlselect service is of type LoadBalancer:

   .. code-block:: bash

       kubectl get svc vlselect -n telemetry

#. Check MetalLB configuration.

   If using MetalLB for LoadBalancer services, verify that MetalLB is functioning correctly:

   .. code-block:: bash

       kubectl get pods -n metallb-system

#. Verify TLS certificate SANs.

   Ensure that the TLS certificates include the correct SANs for vlselect:

   .. code-block:: bash

       openssl x509 -in victoria-ca.crt -text -noout | grep -A1 "Subject Alternative Name"

Storage Issues
--------------

**Issue: Storage space exhaustion**

#. Check PVC utilization.

   .. code-block:: bash

       kubectl get pvc -n telemetry
       kubectl exec -it <vlstorage-pod> -n telemetry -- df -h

   Replace ``<vlstorage-pod>`` with the actual vlstorage pod name.

#. Adjust retention period or storage size.

   If storage is exhausted, consider adjusting the ``retention_period`` or ``storage_size`` parameters in ``telemetry_config.yml`` and redeploying.

   See :doc:`victorialogs_config` for configuration details.

Performance Issues
-------------------

**Issue: High query latency**

#. Check time range in query.

   Large time ranges can result in slower query performance. Reduce the time range in your LogsQL query.

#. Verify vlselect pod health.

   .. code-block:: bash

       kubectl get pods -n telemetry | grep vlselect

   Ensure that all vlselect pods are in the ``Running`` state.

   .. note::

      VictoriaLogs cluster mode is relatively new in upstream. Pin to a tested release for production deployments.

   .. important::

      vlstorage PVCs persist after StatefulSet deletion. Manual cleanup is required during teardown to release storage resources.

Related Topics
---------------

* :doc:`index` - Telemetry overview
* :doc:`deploy_victorialogs` - Deploy VictoriaLogs cluster mode
* :doc:`configure_victorialogs_sources` - Configure log sources for VictoriaLogs
* :doc:`query_victorialogs` - Query logs with VictoriaLogs

.. AI_REVIEW: Troubleshooting steps require SME validation against real deployment scenarios
