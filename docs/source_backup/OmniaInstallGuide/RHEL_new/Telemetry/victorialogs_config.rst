.. _victorialogs-config:

.. versionadded:: 2.2

VictoriaLogs Configuration Reference
=====================================

This topic provides a reference for all VictoriaLogs configuration parameters in ``telemetry_config.yml``. Use these parameters to correctly size and configure the log management system for your environment.

.. note::
   VictoriaLogs is deployed in cluster mode only. Single-node mode is not supported for production environments.

victoria_logs_configurations Parameters
---------------------------------------

The ``victoria_logs_configurations`` section in ``telemetry_config.yml`` defines the storage and retention settings for VictoriaLogs.

.. code-block:: yaml

   victoria_logs_configurations:
     retention_period: 168  # hours (7 days)
     storage_size: 8Gi      # per replica

Retention Period
~~~~~~~~~~~~~~~~

The ``retention_period`` parameter specifies how long VictoriaLogs retains log data before automatic deletion.

* **Type**: Integer (hours)
* **Default**: 168 (7 days)
* **Accepted values**: 24-8760 (1 day to 1 year)
* **Configuration location**: ``telemetry_config.yml``

.. note::
   Retention is global and applies to all log streams uniformly. Deletion occurs asynchronously during background merge operations.

Storage Size
~~~~~~~~~~~~

The ``storage_size`` parameter specifies the storage allocated for each VictoriaLogs vlstorage replica.

* **Type**: Kubernetes PVC size format
* **Default**: 8Gi (per replica)
* **Accepted values**: Must be specified in the form of ``X[Ki|Mi|Gi|Ti|Pi|Ei]``
* **Configuration location**: ``telemetry_config.yml``

**Total Storage Calculation:**

VictoriaLogs cluster mode uses 3 vlstorage replicas. Calculate total storage as follows::

   Total storage = storage_size × 3 replicas

Example::

   storage_size: 8Gi
   Total storage = 8Gi × 3 = 24Gi

.. warning::
   Storage under-provisioning can lead to data loss before the retention period is reached. Calculate storage requirements based on expected log volume and retention needs.

Storage Sizing Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following formula to estimate storage requirements::

   Required storage = (140 MB/day × retention_days × node_count) / 3 replicas

**Example:**

For a 100-node cluster with 7-day retention::

   Required storage = (140 MB/day × 7 days × 100 nodes) / 3 replicas
   Required storage = 98,000 MB / 3
   Required storage ≈ 32,667 MB ≈ 32 Gi

In this example, set ``storage_size`` to at least ``11Gi`` (32 Gi / 3 replicas).

Deployment Mode
~~~~~~~~~~~~~~~

VictoriaLogs is deployed in cluster mode only for production environments. Cluster mode provides high availability and scalability.

**Cluster Mode Specifications:**

* **vlstorage replicas**: 3 (storage nodes)
* **vlinsert replicas**: 2 (ingestion nodes)
* **vlselect replicas**: 2 (query nodes)
* **VLAgent**: 1 replica (log collection agent)

**Cluster Mode Benefits:**

* High availability (no single point of failure)
* Horizontal scalability (scale components independently)
* Better performance (4x ingestion, 2x query speed)
* Production-ready architecture

.. important::
   Cluster mode requires at least 2 Service Kubernetes worker nodes for pod anti-affinity rules to function correctly.

Related Topics
--------------

* :doc:`deploy_victorialogs` — Deploy VictoriaLogs cluster mode
* :doc:`configure_victorialogs_sources` — Configure log sources for VictoriaLogs
* :doc:`query_victorialogs` — Query logs with VictoriaLogs
* :doc:`troubleshoot_victorialogs` — Troubleshoot VictoriaLogs issues
