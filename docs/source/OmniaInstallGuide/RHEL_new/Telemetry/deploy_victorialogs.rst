.. _deploy-victorialogs:

Deploy VictoriaLogs Cluster Mode
================================

This procedure guides you through deploying VictoriaLogs in cluster mode to enable centralized log management for your Omnia cluster. VictoriaLogs is deployed as a mandatory platform service alongside VictoriaMetrics.

Prerequisites
-------------

Ensure the following prerequisites are met before deploying VictoriaLogs:

* Omnia Infrastructure Manager (OIM) is deployed
* Service Kubernetes cluster is deployed with at least 2 worker nodes
* VictoriaMetrics is deployed (VictoriaLogs co-deploys with VictoriaMetrics)
* ``pod_external_ip_range`` is configured in ``omnia_config.yml``
* Storage provisioner is available for PVC provisioning

Configure VictoriaLogs Settings
------------------------------

#. Configure the ``telemetry_config.yml`` file to set VictoriaLogs parameters.

   Edit the ``telemetry_config.yml`` file and add the ``victoria_logs_configurations`` section:

   .. code-block:: yaml

       victoria_logs_configurations:
         retention_period: 168  # hours (7 days)
         storage_size: 8Gi      # per replica

   The ``retention_period`` specifies how long logs are retained before automatic deletion. The default is 168 hours (7 days).

   The ``storage_size`` specifies the storage allocated per vlstorage replica. The default is 8Gi per replica (24Gi total for 3 replicas).

   .. warning::

      Storage sizing must account for log volume and retention period. Use the sizing formula: ``140 MB/day × retention_days × node_count``. Storage under-provisioning can lead to data loss before the retention period.

#. Set the ``telemetry_collection_type`` to include ``victoria``.

   Edit the ``telemetry_config.yml`` file and ensure ``victoria`` is included in the collection type:

   .. code-block:: yaml

       telemetry_collection_type:
         - victoria

   .. note::

      VictoriaLogs shares the same deployment gate as VictoriaMetrics. Both are deployed when ``victoria`` is present in ``telemetry_collection_type``.

Deploy VictoriaLogs Cluster
---------------------------

#. Run the discovery playbook for telemetry deployment.

   Execute the discovery playbook to deploy the telemetry services:

   .. code-block:: bash

       cd /omnia
       ansible-playbook discovery.yml

   The playbook deploys VictoriaLogs in cluster mode with the following components:

   * 3 vlstorage replicas (persistent log storage)
   * 2 vlinsert replicas (log ingestion gateway)
   * 2 vlselect replicas (log query gateway)
   * 1 VLAgent replica (log forwarding agent)

   .. important::

      Cluster mode requires at least 2 Service Kubernetes worker nodes for pod anti-affinity distribution of vlstorage replicas.

Verify Deployment
-----------------

#. Verify that VictoriaLogs cluster components are healthy.

   Check the status of the VictoriaLogs pods in the ``telemetry`` namespace:

   .. code-block:: bash

       kubectl get pods -n telemetry

   Verify that the following pods are in the ``Running`` state:

   * ``vlstorage-victoria-logs-cluster-0``, ``vlstorage-victoria-logs-cluster-1``, ``vlstorage-victoria-logs-cluster-2``
   * ``vlinsert-victoria-logs-cluster-<hash>-<replica>``
   * ``vlselect-victoria-logs-cluster-<hash>-<replica>``
   * ``vlagent``

#. Verify that VLAgent is running with syslog receivers.

   Check the VLAgent service to confirm syslog receivers are exposed:

   .. code-block:: bash

       kubectl get svc vlagent -n telemetry

   The service should expose ports 514 (plaintext syslog) and 6514 (TLS syslog).

Record Endpoint Information
-----------------------------

#. Record the VictoriaLogs endpoint information for log source configuration.

   Retrieve the LoadBalancer IP addresses for the VictoriaLogs services:

   .. code-block:: bash

       kubectl get svc -n telemetry | grep victoria

   Record the following endpoint information:

   * ``vlinsert`` endpoint (log ingestion): ``https://<LoadBalancer-IP>:9481``
   * ``vlselect`` endpoint (log query): ``https://<LoadBalancer-IP>:9491``
   * ``vlagent`` syslog plaintext: ``<LoadBalancer-IP>:514``
   * ``vlagent`` syslog TLS: ``<LoadBalancer-IP>:6514``

   Store this information for configuring external log sources. See :doc:`configure_victorialogs_sources` for details on configuring log sources to send logs to VictoriaLogs.

Related Topics
---------------

* :doc:`index` - Telemetry overview
* :doc:`configure_victorialogs_sources` - Configure log sources for VictoriaLogs
* :doc:`victorialogs_config` - VictoriaLogs configuration reference
* :doc:`external_victoria` - Collect telemetry data from external client nodes to Victoria DB
