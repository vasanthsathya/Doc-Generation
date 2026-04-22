.. _victorialogs-config:

VictoriaLogs Configuration Reference
=====================================

This reference provides the configuration parameters for VictoriaLogs in ``telemetry_config.yml``. Use these parameters to size and configure the log management system for your environment.

victoria_logs_configurations Parameters
---------------------------------------

The ``victoria_logs_configurations`` section in ``telemetry_config.yml`` controls VictoriaLogs deployment settings.

Retention Period
----------------

**Parameter:** ``retention_period``

**Type:** Integer (hours)

**Default:** ``168`` (7 days)

**Range:** ``24`` to ``8760`` (1 day to 1 year)

**Description:** Specifies how long logs are retained before automatic deletion. VictoriaLogs automatically deletes log data older than the retention period during background merge operations.

**Example:**

.. code-block:: yaml

    victoria_logs_configurations:
      retention_period: 168  # 7 days

.. note::

   Retention is global and applies to all log streams uniformly. Per-stream retention is not supported.

.. note::

   Deletion is asynchronous during background merge operations. Disk space is reclaimed during the next merge cycle, not immediately at the retention boundary.

Storage Size
------------

**Parameter:** ``storage_size``

**Type:** Kubernetes PVC size format

**Default:** ``8Gi`` (per replica)

**Description:** Specifies the storage allocated per vlstorage replica. Total storage is ``storage_size × vlstorage_replica_count`` (default: 3 replicas = 24Gi total).

**Example:**

.. code-block:: yaml

    victoria_logs_configurations:
      storage_size: 8Gi  # per replica

.. warning::

   Storage under-provisioning can lead to data loss before the retention period. Use the sizing formula to calculate the required storage for your environment.

Storage Sizing Guidelines
-------------------------

Use the following formula to estimate the total storage required:

.. code-block:: text

    Total storage required = ingestion_rate_per_node × retention_days × node_count
                           = 140 MB/day × retention_days × node_count

**Per-replica storage:**

.. code-block:: text

    storage_per_replica = Total storage required / vlstorage_replica_count
                        = (140 MB/day × retention_days × node_count) / 3

**Sizing table for different cluster scales:**

.. csv-table:: VictoriaLogs Storage Sizing
   :file: ../../../Tables/victorialogs_storage_sizing.csv
   :header-rows: 1
   :widths: 15, 10, 10, 15, 20, 20

.. note::

   The ingestion rate of 140 MB/day is an empirical estimate based on VictoriaLogs compression ratio (~10:1 on structured JSON logs). Adjust this value based on your actual log volume.

Deployment Mode
----------------

VictoriaLogs is deployed in **cluster mode only**. Single-node deployment is not supported.

**Component replicas:**

* **vlstorage:** 3 replicas (StatefulSet with PVC-backed persistent storage)
* **vlinsert:** 2 replicas (Deployment with LoadBalancer service)
* **vlselect:** 2 replicas (Deployment with LoadBalancer service)
* **VLAgent:** 1 replica (Deployment with LoadBalancer service)

.. important::

   Cluster mode requires at least 2 Service Kubernetes worker nodes for pod anti-affinity distribution of vlstorage replicas.

Related Topics
---------------

* :doc:`index` - Telemetry overview
* :doc:`deploy_victorialogs` - Deploy VictoriaLogs cluster mode
* :doc:`configure_victorialogs_sources` - Configure log sources for VictoriaLogs
