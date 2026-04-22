.. _query-victorialogs:

.. versionadded:: 2.2

.. note::
   This topic is pending SME validation. Content may change before publication.

Query Logs with VictoriaLogs
============================

Query logs stored in VictoriaLogs to troubleshoot issues, analyze system behavior, and investigate events across the cluster. VictoriaLogs uses LogsQL (Log Query Language) for searching and filtering log data.

Prerequisites
-------------

Before querying logs:

* Ensure that VictoriaLogs cluster is deployed (see :doc:`deploy_victorialogs`)
* Ensure that logs are ingested from one or more sources (see :doc:`configure_victorialogs_sources`)
* Ensure that you have the vlselect endpoint information

Access Query Interface
---------------------

VictoriaLogs provides multiple interfaces for querying logs:

**HTTP API**

Use the HTTP API to query logs programmatically or from the command line.

.. code-block:: bash

   curl -k https://<LoadBalancer IP>:9491/select/logsql/query -d 'query="<query>"'

Replace ``<LoadBalancer IP>`` with the external IP of the vlselect service and ``<query>`` with your LogsQL query.

**Built-in Web UI**

If configured, access the VictoriaLogs web UI through a browser at ``https://<LoadBalancer IP>:9491``.

.. important::
   TLS is required for all external query access. Use ``-k`` with curl to bypass certificate verification for self-signed certificates during testing.

LogsQL Query Basics
-------------------

LogsQL is VictoriaLogs query language. It uses a simple syntax for filtering and searching log data.

**Basic Query Syntax**

A basic LogsQL query consists of filter expressions that match log fields.

.. code-block:: text

   {_stream="device-01"}
   {_msg="error"}
   {level="error"}

**Time Range Filtering**

Filter logs by time range using the ``time:`` filter.

.. code-block:: text

   {time:1h}               # Last 1 hour
   {time:24h}              # Last 24 hours
   {time:7d}               # Last 7 days
   {time:"2024-01-01"}     # Specific date

**Field Filtering**

Filter by specific log fields.

.. code-block:: text

   {_stream="device-01"}
   {_msg="connection"}
   {level="error"}
   {host="server-01"}

Common Query Patterns
---------------------

**Search for Specific Error Messages**

Find logs containing specific error text.

.. code-block:: text

   {_msg="error"}
   {_msg=~"connection.*failed"}  # Regex match

**Filter by Log Level**

Filter logs by severity level.

.. code-block:: text

   {level="error"}
   {level="warning"}
   {level="info"}

**Query Logs from Specific Hosts**

Find logs from specific devices or hosts.

.. code-block:: text

   {_stream="device-01"}
   {host="server-01"}

**Combine Multiple Filters**

Combine multiple filters using logical operators.

.. code-block:: text

   {level="error"} AND {_stream="device-01"}
   {level="warning"} OR {level="error"}
   {_msg=~"error"} AND {time:1h}

**Aggregate and Analyze Log Data**

Use aggregation functions to analyze log patterns.

.. code-block:: text

   stats by (_stream) count()
   stats by (level) count()
   stats by (host) count()

.. AI_REVIEW::
   LogsQL query syntax examples require SME verification against VictoriaLogs documentation. The examples above provide general guidance; actual syntax may vary by VictoriaLogs version.

Export Results
--------------

Export query results to a file for further analysis.

.. code-block:: bash

   curl -k https://<LoadBalancer IP>:9491/select/logsql/query -d 'query="<query>"' > results.json

The results are returned in JSON format.

.. note::
   Query latency depends on time range and data volume. Narrow the time range for faster results.

Related Topics
--------------

* :doc:`deploy_victorialogs` — Deploy VictoriaLogs cluster mode
* :doc:`configure_victorialogs_sources` — Configure log sources for VictoriaLogs
* :doc:`troubleshoot_victorialogs` — Troubleshoot VictoriaLogs issues
