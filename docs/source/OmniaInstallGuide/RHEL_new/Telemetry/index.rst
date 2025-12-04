Step 8: Configure telemetry requirements
========================================

Omnia enables telemetry collection using both iDRAC Telemetry and LDMS
(Lightweight Distributed Metric Service) in HPC environments. This design ensures that
telemetry components are dynamically provisioned with stateless provisioning tool, 
providing flexible deployment and simplified lifecycle management.

* **iDRAC Telemetry** provides out-of-band system metrics from Dell servers, including
  power, thermal, and hardware health information. The iDRAC Telemetry data can be collected
  and streamed to **Kafka** or **VictoriaMetrics**, depending on the deployment needs.

* **LDMS Telemetry** collects in-band performance metrics such as CPU, memory,
  network, and I/O statistics from compute nodes. The LDMS Telemetry data can be collected
  and streamed to **Kafka**.

.. note::

   The ``idrac_telemetry_support`` should be set to ``false`` if the Service Kubernetes cluster is not part of the deployment and the ``service_k8s`` entry is not included in the ``software_config.json`` file.


.. toctree::
    :maxdepth: 1

    service_cluster_telemetry
    ldms_telemetry
    