

Setup Telemetry
===============


Deploy the Omnia telemetry pipeline using ``telemetry.yml`` to collect,
aggregate, and visualize hardware and OS metrics from across the cluster.


Overview
--------


The Omnia telemetry pipeline collects metrics from multiple sources and stores
them for visualization in Grafana. Running ``telemetry.yml`` deploys:

- **iDRAC Telemetry Collector** -- Collects hardware metrics (temperatures,
  power, fan speeds) from Dell iDRAC via Redfish.
- **LDMS (Lightweight Distributed Metric Service)** -- Collects OS-level
  metrics (CPU, memory, I/O) from compute nodes.
- **Kafka** -- Message broker for streaming metrics.
- **VictoriaMetrics** -- Time-series database for metric storage.
- **Grafana** -- Visualization dashboards.

The telemetry services run as pods on the Kubernetes service cluster.



Prerequisites
-------------


- A Kubernetes service cluster is deployed (see
  :doc:`Setup Service K8S <../Kubernetes/setup_service_k8s>`).
- The Slurm cluster is deployed (for LDMS agent deployment on compute nodes).
- ``omnia_config.yml`` is configured with telemetry parameters.
- iDRAC credentials are configured (see
  :doc:`Configure Credentials <../Setup/configure_credentials>`).
- The K8s cluster has persistent storage available (NFS CSI or PowerScale CSI).



Procedure
---------


#. **Enter the omnia_core container**:


**Run on: OIM host**

.. code-block:: bash
      ssh omnia_core



#. **Configure telemetry parameters** in ``omnia_config.yml``:


**Run on: omnia_core container**

.. code-block:: bash
      vi /opt/omnia/input/project_default/omnia_config.yml




**File: /opt/omnia/input/project_default/omnia_config.yml**

.. code-block:: yaml
      ---
      # Telemetry configuration
      enable_telemetry: true
      telemetry_collection_interval: 60  # seconds
      grafana_admin_password: ""  # Set via credentials utility
   
      # iDRAC telemetry
      idrac_telemetry_enabled: true
      idrac_telemetry_metrics:
        - "SystemBoardInletTemp"
        - "SystemBoardExhaustTemp"
        - "TotalPower"
        - "CPUUsage"
        - "MemoryUsage"
        - "FanSpeed"
   
      # LDMS configuration
      ldms_enabled: true
      ldms_samplers:
        - "meminfo"
        - "vmstat"
        - "procstat"



#. **Run the telemetry playbook**:


**Run on: omnia_core container**

.. code-block:: bash
      cd /omnia
      ansible-playbook telemetry.yml --ask-vault-pass



   The playbook performs:

  - Deploys Kafka on the K8s service cluster.
  - Deploys VictoriaMetrics for time-series storage.
  - Deploys Grafana with pre-configured dashboards.
  - Deploys the iDRAC telemetry collector.
  - Installs and configures LDMS samplers on compute nodes.
  - Installs LDMS aggregators on the K8s cluster.
  - Configures data flow: LDMS/iDRAC → Kafka → VictoriaMetrics → Grafana.

   Execution time: **15-30 minutes**.

#. **Access the Grafana dashboard**:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl get svc -n telemetry | grep grafana



   Note the external IP (from MetalLB). Open a browser and navigate to:

   ``http://<grafana-external-ip>:3000``

   Default credentials:

  - Username: ``admin``
  - Password: (as configured in omnia_config.yml or credentials utility)



Verification
------------


#. **Verify telemetry pods are running**:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl get pods -n telemetry



   Expected pods:


**Expected output on: K8s control plane node**

.. code-block:: text
      NAME                                    READY   STATUS    RESTARTS
      grafana-xxxxxxxxxx-xxxxx                1/1     Running   0
      kafka-0                                 1/1     Running   0
      victoriametrics-xxxxxxxxxx-xxxxx        1/1     Running   0
      idrac-collector-xxxxxxxxxx-xxxxx        1/1     Running   0
      ldms-aggregator-xxxxxxxxxx-xxxxx        1/1     Running   0



#. **Verify LDMS agents on compute nodes**:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m shell -a "systemctl is-active ldmsd"



#. **Check Kafka topics** have telemetry data:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl exec -n telemetry kafka-0 -- kafka-topics.sh --list --bootstrap-server localhost:9092



#. **Verify VictoriaMetrics is receiving data**:


**Run on: K8s control plane node**

.. code-block:: bash
      VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
      kubectl exec -n telemetry $VM_POD -- curl -s "http://localhost:8428/api/v1/query?query=up" | python3 -m json.tool



#. **Verify Grafana dashboards** show data by opening the web UI and checking
   the pre-configured dashboards for active time-series data.



Next Steps
----------


- :doc:`Configure Ldms <configure_ldms>` -- Fine-tune LDMS sampler plugins.
- :doc:`Configure External Kafka <configure_external_kafka>` -- Use an external Kafka cluster.
- :doc:`Configure External Victoria <configure_external_victoria>` -- Use an external VictoriaMetrics
  instance.
- :doc:`Verify Telemetry <verify_telemetry>` -- End-to-end telemetry verification.



Troubleshooting
---------------


**Telemetry pods stuck in Pending**
   Check for persistent volume issues:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl describe pvc -n telemetry



**iDRAC collector shows errors**
   Verify iDRAC credentials and Redfish access:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl logs -n telemetry -l app=idrac-collector --tail=30



**LDMS agents not running on compute nodes**
   Re-deploy LDMS:


**Run on: omnia_core container**

.. code-block:: bash
      ansible slurm_node -m shell -a "systemctl restart ldmsd"



**Grafana shows "No data"**
  - Verify the VictoriaMetrics data source is configured in Grafana.
  - Check the time range in Grafana (default to "Last 1 hour").
  - Verify data is flowing through Kafka:


**Run on: K8s control plane node**

.. code-block:: bash
        kubectl exec -n telemetry kafka-0 -- kafka-console-consumer.sh \
          --bootstrap-server localhost:9092 --topic telemetry --from-beginning --max-messages 5



**Kafka pod CrashLoopBackOff**
   Check disk space on the K8s worker node:


**Run on: K8s worker node**

.. code-block:: bash
      df -h

