.. _deploy-victorialogs:

.. versionadded:: 2.2

Deploy VictoriaLogs Cluster Mode
=================================

Deploy VictoriaLogs in cluster mode to enable centralized log management for your Omnia cluster. This procedure guides you through configuring telemetry settings and deploying VictoriaLogs alongside VictoriaMetrics.

Prerequisites
-------------

Before deploying VictoriaLogs:

* Ensure that Omnia Infrastructure Manager (OIM) is deployed
* Ensure that Service Kubernetes cluster is deployed with at least 2 worker nodes
* Ensure that VictoriaMetrics deployment is configured (VictoriaLogs co-deploys with VictoriaMetrics)
* Ensure that ``pod_external_ip_range`` is configured in ``omnia_config.yml``
* Ensure that a storage provisioner is available for PVC provisioning

.. important::
   Cluster mode requires at least 2 Service Kubernetes worker nodes for pod anti-affinity rules to function correctly.

.. note::
   VictoriaLogs shares the same deployment gate as VictoriaMetrics. Both deploy when ``victoria`` is included in ``telemetry_collection_type``.

Configure VictoriaLogs Settings
-------------------------------

1. Navigate to the telemetry configuration directory.

   .. code-block:: bash

      cd /opt/omnia/input/project_default

2. Open the ``telemetry_config.yml`` file for editing.

   .. code-block:: bash

      vi telemetry_config.yml

3. Configure the ``victoria_logs_configurations`` section.

   .. code-block:: yaml

      victoria_logs_configurations:
        retention_period: 168  # hours (7 days)
        storage_size: 8Gi      # per replica

   * Set ``retention_period`` to the number of hours to retain logs (default: 168 hours / 7 days)
   * Set ``storage_size`` to the storage allocated per vlstorage replica (default: 8Gi)

.. warning::
   Storage sizing must account for log volume and retention period. Use the sizing formula: (140 MB/day × retention_days × node_count) / 3 replicas.

4. Set ``telemetry_collection_type`` to include ``victoria``.

   .. code-block:: yaml

      telemetry_collection_type:
        - victoria

.. note::
   To deploy both VictoriaMetrics and VictoriaLogs, use ``victoria,kafka`` for ``telemetry_collection_type``.

5. Save and close the file.

Deploy VictoriaLogs Cluster
---------------------------

1. Navigate to the telemetry playbooks directory.

   .. code-block:: bash

      cd /opt/omnia/telemetry

2. Run the discovery playbook for telemetry deployment.

   .. code-block:: bash

      ansible-playbook discovery.yml

This playbook deploys the following components:

* **VictoriaLogs Cluster**: 3 vlstorage replicas, 2 vlinsert replicas, 2 vlselect replicas
* **VLAgent**: Log collection agent with syslog receivers on ports 514 (plaintext) and 6514 (TLS)
* **TLS Certificates**: Self-signed certificates for secure communication

.. note::
   The deployment may take 10-15 minutes to complete.

Verify Deployment
-----------------

1. Check the status of VictoriaLogs pods.

   .. code-block:: bash

      kubectl get pods -n telemetry

   Verify that the following pods are running and healthy:

   * ``vlstorage-victoria-logs-cluster-0``, ``vlstorage-victoria-logs-cluster-1``, ``vlstorage-victoria-logs-cluster-2``
   * ``vlinsert-victoria-logs-cluster-0``, ``vlinsert-victoria-logs-cluster-1``
   * ``vlselect-victoria-logs-cluster-0``, ``vlselect-victoria-logs-cluster-1``
   * ``vlagent``

2. Verify that the LoadBalancer services are created.

   .. code-block:: bash

      kubectl get svc -n telemetry

   Verify that the following services have external IPs:

   * ``vlinsert-victoria-logs-cluster`` (ingestion endpoint)
   * ``vlselect-victoria-logs-cluster`` (query endpoint)
   * ``vlagent`` (syslog receivers)

3. Verify TLS connectivity.

   .. code-block:: bash

      openssl s_client -connect <LoadBalancer IP>:6514 -showcerts

   Replace ``<LoadBalancer IP>`` with the external IP of the vlagent service.

Record Endpoint Information
----------------------------

After successful deployment, record the following endpoint information for log source configuration:

* **Syslog plaintext**: ``<LoadBalancer IP>:514``
* **Syslog TLS**: ``<LoadBalancer IP>:6514``
* **HTTP forwarder**: ``https://<LoadBalancer IP>:9481/insert/jsonline``
* **Query endpoint**: ``https://<LoadBalancer IP>:9491``

.. note::
   Store this information securely. You will need it when configuring external log sources to send logs to VictoriaLogs.

Verification
------------

After recording endpoint information, verify the VictoriaLogs deployment is fully functional:

1. Test log ingestion by sending a test syslog message to VLAgent.

   .. code-block:: bash

      echo "test message" | nc -u <LoadBalancer IP> 514

2. Verify the test message appears in VictoriaLogs query results.

   .. code-block:: bash

      curl -k https://<LoadBalancer IP>:9491/select/logsql/query -d 'query="{_msg=\"test message\"}"'

3. Confirm the query returns the test log entry, indicating successful ingestion and query functionality.

Related Topics
--------------

* :doc:`victorialogs_config` — VictoriaLogs configuration reference
* :doc:`configure_victorialogs_sources` — Configure log sources for VictoriaLogs
* :doc:`query_victorialogs` — Query logs with VictoriaLogs
* :doc:`troubleshoot_victorialogs` — Troubleshoot VictoriaLogs issues
