Collect telemetry data from Smart Fabric Manager to Victoria DB (cluster mode)
=============================================================================

This section describes how to configure Smart Fabric Manager to securely stream
telemetry metrics to the Service Kubernetes cluster.

This procedure assumes that VictoriaMetrics is deployed in **cluster mode** in the
``telemetry`` namespace of the Service Kubernetes cluster.
For more information, see the `VictoriaMetrics cluster mode documentation
<https://docs.victoriametrics.com/victoriametrics/cluster-victoriametrics/>`_.

Prerequisites
-------------

Make sure the following prerequisites are met:

* A Service Kubernetes cluster is running with VictoriaMetrics deployed in the
  ``telemetry`` namespace.
* External access to VictoriaMetrics is available through the following
  LoadBalancer ports:

  * ``8480`` for ingesting data
  * ``8481`` for querying data

Steps
-----

1. Log in to the Omnia core container and go to the VictoriaMetrics certificate
   directory::

      ssh omnia_core
      cd /opt/omnia/telemetry/victoria-certs/

2. Add the LoadBalancer IP addresses for the VictoriaMetrics insert and select
   services to the ``/etc/hosts`` file::

      echo "10.xx.xx.xx vminsert.telemetry.svc.cluster.local" >> /etc/hosts
      echo "10.xx.xx.xx vmselect.telemetry.svc.cluster.local" >> /etc/hosts

3. Log in to Smart Fabric Manager for SONiC.

4. In the left navigation pane, select **Observability**, and then select the
   **Settings** tab.

5. Under **Prometheus Remote Pump**, select the option button next to
   ``vminsert-target``, and then select **Edit**.

6. In the **URL** field, enter the following endpoint::

      https://vminsert.telemetry.svc.cluster.local:8480/insert/0/prometheus/api/v1/write
