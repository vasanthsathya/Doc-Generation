.. _query-victorialogs:

.. note::
   This topic is pending SME validation. Content may change before publication.

Query Logs with VictoriaLogs
=============================

This procedure guides you through querying logs stored in VictoriaLogs to troubleshoot issues, analyze system behavior, and investigate events across the cluster.

Prerequisites
-------------

Ensure the following prerequisites are met:

* VictoriaLogs cluster is deployed
* Logs are ingested from one or more sources
* vlselect endpoint information is available

Access Query Interface
----------------------

#. Access the VictoriaLogs query interface.

   VictoriaLogs provides multiple methods for querying logs:

   * **Built-in web UI** (if configured)
   * **HTTP API** via vlselect endpoint
   * **Command-line tools** using curl or similar

   For HTTP API access, use the vlselect endpoint:

   .. code-block:: text

       https://vlselect-victoria-logs-cluster.telemetry.svc.cluster.local:9491

   Replace the service name with the LoadBalancer IP for external access.

   .. important::

      TLS is required for all external query access. Use the CA certificate from the ``victoria-tls-certs`` secret.

LogsQL Query Basics
-------------------

VictoriaLogs uses LogsQL (VictoriaLogs Query Language) for searching, filtering, and aggregating log data. LogsQL syntax differs from other log query languages.

#. Use basic LogsQL query syntax.

   A basic LogsQL query has the following format:

   .. code-block:: text

       {filter_expression} | pipe_commands

   Examples:

   .. code-block:: text

       # Search for all logs from the last 5 minutes
       {_time:5m}

       # Search for error logs
       {_level:ERROR}

       # Search for logs from a specific host
       {host="server1"}

   .. note::

      LogsQL is VictoriaLogs query language. Syntax differs from other log query languages.

Common Query Patterns
--------------------

#. Search for specific error messages.

   .. code-block:: bash

       curl --cacert victoria-ca.crt -s "https://<vlselect-IP>:9491/select/logsql/query?query={_level:ERROR}" | jq

#. Filter by log level.

   .. code-block:: bash

       curl --cacert victoria-ca.crt -s "https://<vlselect-IP>:9491/select/logsql/query?query={_level:WARN}" | jq

#. Query logs from specific hosts or devices.

   .. code-block:: bash

       curl --cacert victoria-ca.crt -s "https://<vlselect-IP>:9491/select/logsql/query?query={host=\"server1\"}" | jq

#. Aggregate and analyze log data.

   .. code-block:: bash

       curl --cacert victoria-ca.crt -s "https://<vlselect-IP>:9491/select/logsql/stats_query?query={_level:ERROR} | stats by (_level)" | jq

   .. AI_REVIEW: LogsQL query syntax examples require SME verification against VictoriaLogs documentation

Export Results
--------------

#. Export query results if needed.

   Use curl to query and save results to a file:

   .. code-block:: bash

       curl --cacert victoria-ca.crt -s "https://<vlselect-IP>:9491/select/logsql/query?query={_time:1h}" > logs.json

   The results are returned in JSON format for further processing or analysis.

   .. note::

      Query latency depends on time range and data volume. Large time ranges may result in slower query performance.

Related Topics
---------------

* :doc:`index` - Telemetry overview
* :doc:`configure_victorialogs_sources` - Configure log sources for VictoriaLogs
* :doc:`external_victoria` - Collect telemetry data from external client nodes to Victoria DB
