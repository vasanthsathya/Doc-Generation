.. _configure-victorialogs-sources:

.. note::
   This topic is pending SME validation. Content may change before publication.

Configure Log Sources for VictoriaLogs
======================================

This procedure guides you through configuring external log sources (network devices, storage systems, fabric managers) to send logs to VictoriaLogs for centralized log collection and analysis.

Prerequisites
-------------

Ensure the following prerequisites are met:

* VictoriaLogs cluster is deployed (see :doc:`deploy_victorialogs`)
* VLAgent endpoint information is recorded from deployment
* TLS CA certificate for VictoriaLogs is available
* Network connectivity exists from log sources to the Service Kubernetes cluster

Obtain Endpoint Information
----------------------------

#. Retrieve the VictoriaLogs ingestion endpoint and TLS CA certificate.

   Run the following command to get the VLAgent service details:

   .. code-block:: bash

       kubectl get svc vlagent -n telemetry

   Record the following endpoint information:

   * Syslog plaintext: ``<LoadBalancer-IP>:514``
   * Syslog TLS: ``<LoadBalancer-IP>:6514``
   * HTTP forwarder: ``https://vlinsert-victoria-logs-cluster.telemetry.svc.cluster.local:9481/insert/jsonline``

   .. important::

      Ensure that ``pod_external_ip_range`` is reachable from external log sources.

#. Extract the TLS CA certificate for encrypted connections.

   Retrieve the CA certificate from the ``victoria-tls-certs`` secret:

   .. code-block:: bash

       kubectl get secret victoria-tls-certs -n telemetry -o jsonpath='{.data.ca\.crt}' | base64 -d > victoria-ca.crt

   Use this certificate for TLS syslog connections.

Configure Syslog Sources
-------------------------

#. Configure syslog sources to send logs to VLAgent.

   For plaintext syslog (port 514):

   Configure your device or application to send syslog messages to the VLAgent endpoint:

   .. code-block:: text

       Syslog server: <LoadBalancer-IP>
       Port: 514
       Protocol: TCP or UDP
       Format: RFC 3164 or RFC 5424

   For TLS syslog (port 6514):

   Configure your device or application to send syslog messages over TLS:

   .. code-block:: text

       Syslog server: <LoadBalancer-IP>
       Port: 6514
       Protocol: TCP
       Format: RFC 5425 (TLS)
       CA certificate: victoria-ca.crt

   .. note::

      VLAgent provides platform-managed syslog receivers. No additional configuration is needed on the Omnia side.

   .. note::

      DNS mapping may be required in some devices for TLS certificate validation. Add the LoadBalancer IP to your device's DNS or hosts file.

   .. AI_REVIEW: Device-specific syslog configuration examples may need SME verification for accuracy

Configure HTTP Forwarding Sources
----------------------------------

#. Configure log sources that support HTTP forwarding.

   For applications or systems that support HTTP log forwarding, use the JSON Lines format:

   .. code-block:: text

       Endpoint: https://vlinsert-victoria-logs-cluster.telemetry.svc.cluster.local:9481/insert/jsonline
       Method: POST
       Format: JSON Lines (newline-delimited JSON)
       Authentication: TLS (CA certificate: victoria-ca.crt)

   Example JSON Lines format:

   .. code-block:: json

       {"timestamp":"2026-04-22T10:00:00Z","level":"INFO","message":"System started","host":"server1"}
       {"timestamp":"2026-04-22T10:00:01Z","level":"ERROR","message":"Connection failed","host":"server1"}

   .. note::

      The internal service name ``vlinsert-victoria-logs-cluster.telemetry.svc.cluster.local`` is only resolvable from within the Service Kubernetes cluster. For external access, use the LoadBalancer IP.

Verify Log Ingestion
-------------------

#. Verify that logs are appearing in VictoriaLogs.

   Query VictoriaLogs to confirm logs are being ingested:

   .. code-block:: bash

       curl --cacert victoria-ca.crt -s "https://<vlselect-LoadBalancer-IP>:9491/select/logsql/query?query={_time:5m}" | jq

   Replace ``<vlselect-LoadBalancer-IP>`` with the actual vlselect LoadBalancer IP.

   If logs are appearing in the query results, the log source configuration is successful.

Related Topics
---------------

* :doc:`index` - Telemetry overview
* :doc:`deploy_victorialogs` - Deploy VictoriaLogs cluster mode
* :doc:`query_victorialogs` - Query logs with VictoriaLogs
