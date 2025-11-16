Step 12: Prepare Telemetry requirements
================================
Omnia enables stateless telemetry collection using both iDRAC Telemetry and LDMS (Lightweight Distributed Metric Service) in HPC environments. This approach ensures that telemetry components are dynamically provisioned without requiring modifications to the base image, providing flexible deployment and simplified lifecycle management.

* iDRAC Telemetry provides out-of-band system metrics from Dell servers, including power, thermal, and hardware health data. See :doc:`service_cluster_telemetry`.

* LDMS Telemetry collects in-band performance metrics such as CPU, memory, network, and I/O statistics from compute nodes. See :doc:`ldms_telemetry`.



.. toctree::
    :maxdepth: 1

    service_cluster_telemetry
    ldms_telemetry
    