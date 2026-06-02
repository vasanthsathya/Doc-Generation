

Verify Telemetry
================


Perform an end-to-end verification of the Omnia telemetry pipeline from data
collection through storage to visualization.


Overview
--------


A complete telemetry verification traces the data flow through every stage:

#. **Collection** -- iDRAC collectors and LDMS samplers are generating metrics.
#. **Transport** -- Kafka topics are receiving messages.
#. **Storage** -- VictoriaMetrics is ingesting and storing time-series data.
#. **Visualization** -- Grafana dashboards display live data.



Prerequisites
-------------


- The :doc:`Setup Telemetry <setup_telemetry>` procedure is complete.
- The K8s service cluster is running with telemetry pods.
- LDMS agents are deployed on compute nodes.
- Grafana is accessible via the browser.



Procedure
---------



Stage 1: Verify Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Check iDRAC collector** is retrieving metrics:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

      kubectl logs -n telemetry -l app=idrac-collector --tail=10



   Look for successful metric retrieval messages.

#. **Check LDMS samplers** are running on compute nodes:

   .. code-block:: bash
      :caption: Run on: omnia_core container

      ansible slurm_node -m shell -a "systemctl is-active ldmsd"



#. **Query LDMS metrics** locally on a compute node:

   .. code-block:: bash
      :caption: Run on: compute node

      ldms_ls -h localhost -p 411 -v



   Should list active metric sets.



Stage 2: Verify Transport (Kafka)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **List Kafka topics**:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

      KAFKA_POD=$(kubectl get pod -n telemetry -l app=kafka -o jsonpath='{.items[0].metadata.name}')
      kubectl exec -n telemetry $KAFKA_POD -- kafka-topics.sh --list --bootstrap-server localhost:9092



#. **Check topic message counts**:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

      kubectl exec -n telemetry $KAFKA_POD -- kafka-run-class.sh kafka.tools.GetOffsetShell \
        --broker-list localhost:9092 --topic omnia-telemetry



   Message offsets should be increasing.

#. **Read sample messages** from a topic:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

      kubectl exec -n telemetry $KAFKA_POD -- kafka-console-consumer.sh \
        --bootstrap-server localhost:9092 \
        --topic omnia-telemetry \
        --from-beginning \
        --max-messages 3





Stage 3: Verify Storage (VictoriaMetrics)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Check VictoriaMetrics health**:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

      VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
      kubectl exec -n telemetry $VM_POD -- curl -s http://localhost:8428/health



   Expected: ``OK``

#. **Query stored metrics**:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

      kubectl exec -n telemetry $VM_POD -- \
        curl -s "http://localhost:8428/api/v1/query?query=up" | python3 -m json.tool



#. **Check active time series count**:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

      kubectl exec -n telemetry $VM_POD -- \
        curl -s "http://localhost:8428/api/v1/status/tsdb" | python3 -c "
        import sys, json
        data = json.load(sys.stdin)
        print(f'Active time series: {data.get(\"data\", {}).get(\"totalSeries\", \"unknown\")}')
        "



#. **Query a specific metric** (e.g., iDRAC temperature):

   .. code-block:: bash
      :caption: Run on: K8s control plane node

       kubectl exec -n telemetry $VM_POD -- \
         curl -s "http://localhost:8428/api/v1/query?query=idrac_SystemBoardInletTemp"





Stage 4: Verify Visualization (Grafana)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Get the Grafana external IP**:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

       kubectl get svc -n telemetry grafana



#. **Open Grafana** in a browser: ``http://<grafana-ip>:3000``

#. **Verify data sources**:

    Navigate to **Configuration** > **Data Sources**. The VictoriaMetrics
    data source should show a green "Data source is working" indicator.

#. **Check pre-configured dashboards**:

    Navigate to **Dashboards** > **Browse**. Verify the following dashboards
    exist and show data:

    - **Cluster Overview** -- Node status, overall health
    - **iDRAC Metrics** -- Temperatures, power, fan speeds
    - **LDMS Metrics** -- CPU, memory, I/O per node
    - **Network Fabric** -- (if SFM is configured) port throughput



Verification
------------


Use this checklist to confirm the entire pipeline is operational:


.. list-table::
   :header-rows: 1
   :widths: auto

   * - Stage
     - Check
     - Expected Result
   * - Collection
     - ``ldms_ls -h localhost -p 411``
     - Active metric sets
   * - Collection
     - iDRAC collector pod logs
     - Successful retrieval
   * - Transport
     - Kafka topic list
     - Topics exist
   * - Transport
     - Console consumer
     - Messages readable
   * - Storage
     - ``/health`` endpoint
     - ``OK``
   * - Storage
     - ``/api/v1/query?query=up``
     - Non-empty results
   * - Visualization
     - Grafana data source test
     - Green indicator
   * - Visualization
     - Dashboard shows graphs
     - Data within last hour



Next Steps
----------


- :doc:`Configure Ldms <configure_ldms>` -- Fine-tune metric collection.
- :doc:`Configure External Kafka <configure_external_kafka>` -- Scale the transport layer.
- :doc:`Configure External Victoria <configure_external_victoria>` -- Scale the storage layer.



Troubleshooting
---------------


**No data at any stage**
   Start from the collection stage and trace forward:

  #. Are LDMS/iDRAC collectors running?
  #. Are Kafka topics receiving messages?
  #. Is VictoriaMetrics ingesting data?
  #. Is Grafana configured with the correct data source?

**Data gap in Grafana (intermittent)**
  - Check for pod restarts:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

       kubectl get pods -n telemetry -o wide



  - Check K8s node resources (CPU/memory):

   .. code-block:: bash
      :caption: Run on: K8s control plane node

       kubectl top nodes
       kubectl top pods -n telemetry



**Metrics have stale timestamps**
  - Verify NTP is synchronized on all nodes:

   .. code-block:: bash
      :caption: Run on: omnia_core container

       ansible all -m shell -a "chronyc tracking | grep 'System time'"



**VictoriaMetrics running out of disk**
   Check retention settings and disk usage:

   .. code-block:: bash
      :caption: Run on: K8s control plane node

       kubectl exec -n telemetry $VM_POD -- df -h /victoria-metrics-data

