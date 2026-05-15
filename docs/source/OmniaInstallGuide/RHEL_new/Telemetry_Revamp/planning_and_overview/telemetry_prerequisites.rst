Telemetry Prerequisites
=======================

This section consolidates the prerequisites for configuring various telemetry sources.

iDRAC Telemetry Prerequisites
------------------------------

To deploy iDRAC telemetry service on the service cluster, the following prerequisites must be met:

* Redfish must be enabled in iDRAC.
* If an internet connection is required on the service Kube node, configure it after the node is booted.
* iDRAC firmware must be updated to the latest version.
* Datacenter license must be installed on the nodes.
* Ensure that the correct node service tags are displayed on the iDRAC interface. Otherwise, telemetry data cannot be collected by the ``idrac_telemetry_receiver`` container.
* For telemetry collection on service cluster, all BMC (iDRAC) IPs must be reachable from the service cluster nodes. If the service cluster does not have direct access to the BMC network, configure routing from OIM.
* Ensure that the ``provision.yml`` playbook has been executed successfully with both ``service_kube_control_plane_x86_64`` and  ``service_kube_node_x86_64`` in the mapping file, and the ``bmc_group_data.csv`` file has been generated.
* Before running the ``telemetry.yml`` playbook for the service cluster, ensure that all the service K8s compute nodes are reachable and booted and have been configured in the service K8s cluster.

LDMS Telemetry Prerequisites
----------------------------

To configure LDMS telemetry, the following prerequisites must be met:

* Ensure that the ``provision.yml`` playbook has been executed successfully with ``service_kube_control_plane`` and ``service_kube_node`` in the mapping file.

PowerScale Telemetry Prerequisites
----------------------------------

To configure PowerScale telemetry, the following prerequisites must be met:

* Ensure that the ``provision.yml`` playbook has been executed successfully with ``service_kube_control_plane`` and ``service_kube_node`` in the mapping file.
* For Omnia-orchestrated mode, ensure the service Kubernetes cluster has sufficient resources to run CSM Metrics, OpenTelemetry Collector, CSI Driver, and cert-manager.
* For operator-provided mode, ensure the external OpenTelemetry Collector endpoint is accessible from the service cluster over TLS.
* Ensure network connectivity between the PowerScale cluster and the Omnia log agent for syslog integration.

Vector Telemetry Prerequisites
-------------------------------

To configure Vector telemetry, the following prerequisites must be met:

* Ensure that the ``provision.yml`` playbook has been executed successfully with ``service_kube_control_plane`` and ``service_kube_node`` in the mapping file.
* Ensure that Kafka is deployed and operational via Strimzi operator.
* Ensure that VictoriaMetrics cluster mode is deployed with vminsert, vmstorage, and vmselect components.
* Ensure that VictoriaLogs cluster mode is deployed with vlinsert, vlstorage, and vlselect components (required for Vector-OME logs).

SFM Telemetry Prerequisites
---------------------------

To configure SFM telemetry integration with VictoriaMetrics, the following prerequisites must be met:

* Ensure that Secure Shell (SSH) is enabled on the Smart Fabric Manager (SFM) virtual machine.
* Ensure that the ``pod_external_ip_range`` parameter is set in the ``omnia_config.yml`` file for the Service Kubernetes cluster and it is reachable from the SFM network.
* Ensure VictoriaMetrics (Cluster Mode) is installed and running in the Service Kubernetes cluster.
* External access to VictoriaMetrics is available through the following LoadBalancer ports:

  * ``8480`` for ingesting data
  * ``8481`` for querying data

OME Telemetry Prerequisites
---------------------------

To configure OME telemetry integration with Kafka, the following prerequisites must be met:

* Ensure that the ``pod_external_ip_range`` parameter is set in the ``omnia_config.yml`` file for the Service Kubernetes cluster and it is reachable from the OpenManage Enterprise appliance network.
* Ensure Kafka is installed and running in the Service Kubernetes cluster.
* External access to Kafka is available through the following LoadBalancer ports:

  * ``9094`` for ingesting and querying data.

External Kafka Integration Prerequisites
----------------------------------------

To configure external Kafka integration, the following prerequisites must be met:

* A Service Kubernetes cluster is running with Kafka deployed via Strimzi in the ``telemetry`` namespace.
* External access to Kafka is available through a LoadBalancer on port ``9094``.
* A Kafka Pump is available outside the Service Kubernetes cluster, deployed as a container using Kubernetes, Podman, or Docker.

External VictoriaMetrics Integration Prerequisites
--------------------------------------------------

To configure external VictoriaMetrics integration, the following prerequisites must be met:

* A Service Kubernetes cluster is running with VictoriaMetrics deployed in the ``telemetry`` namespace.
* External access to VictoriaMetrics is available through:

  * LoadBalancer port ``8480`` for ingesting (inserting) data.
  * LoadBalancer port ``8481`` for querying data.

External VictoriaLogs Integration Prerequisites
-----------------------------------------------

To configure external VictoriaLogs integration, the following prerequisites must be met:

* Ensure that VictoriaLogs cluster is deployed.
* Ensure that you have recorded VLAgent endpoint information
* Ensure that you have the TLS CA certificate for VictoriaLogs
* Ensure that network connectivity exists from log sources to the Service Kubernetes cluster

.. important::
   Ensure that ``pod_external_ip_range`` in ``omnia_config.yml`` is reachable from external log sources.
