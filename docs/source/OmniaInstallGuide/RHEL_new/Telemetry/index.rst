Step 8: Configure Telemetry Requirements
========================================

Omnia enables stateless telemetry collection using both iDRAC Telemetry and LDMS
(Lightweight Distributed Metric Service) in HPC environments. This design ensures that
telemetry components are dynamically provisioned without requiring modifications to the
base image, providing flexible deployment and simplified lifecycle management.

* **iDRAC Telemetry** provides out-of-band system metrics from Dell servers, including
  power, thermal, and hardware health information. The iDRAC Telemetry data can be collected
  and streamed to **Kafka** or **VictoriaMetrics**, depending on the deployment needs.

* **LDMS Telemetry** collects in-band performance metrics such as CPU, memory,
  network, and I/O statistics from compute nodes. The LDMS Telemetry data can be collected
  and streamed to **Kafka**.




.. toctree::
    :maxdepth: 1

    service_cluster_telemetry
    ldms_telemetry
    