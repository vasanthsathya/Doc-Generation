

Telemetry from OME & SFM
========================


Collect telemetry data from Dell OpenManage Enterprise (OME) and Smart Fabric
Manager (SFM) in addition to direct iDRAC and LDMS metrics.


Overview
--------


OpenManage Enterprise (OME) aggregates hardware health, alerts, and inventory
data from all Dell servers it manages. Smart Fabric Manager (SFM) provides
network fabric metrics from Dell switches. By integrating OME and SFM
telemetry into Omnia's pipeline, you get:

- Aggregated server health dashboards from OME.
- Network fabric metrics (port throughput, errors) from SFM.
- Correlated views of compute + network performance in Grafana.



Prerequisites
-------------


- OME is deployed and managing the Dell servers in your cluster.
- SFM is deployed and managing Dell networking switches (optional).
- The :doc:`Setup Telemetry <setup_telemetry>` procedure is complete.
- Network connectivity from the K8s service cluster to OME and SFM
  management IPs.
- OME API credentials (read-only user recommended).



Procedure
---------


#. **Enter the omnia_core container**:


**Run on: OIM host**

.. code-block:: bash
      ssh omnia_core



#. **Configure OME telemetry** in ``omnia_config.yml``:


**Run on: omnia_core container**

.. code-block:: bash
      vi /opt/omnia/input/project_default/omnia_config.yml




**File: /opt/omnia/input/project_default/omnia_config.yml**

.. code-block:: yaml
      ---
      # OME telemetry configuration
      ome_telemetry_enabled: true
      ome_ip: "10.5.1.50"
      ome_port: 443
      ome_username: "omnia_readonly"
      ome_password: ""  # Set via credentials utility
      ome_collection_interval: 300  # seconds
   
      # SFM telemetry configuration (optional)
      sfm_telemetry_enabled: true
      sfm_ip: "10.5.1.51"
      sfm_port: 443
      sfm_username: "omnia_readonly"
      sfm_password: ""  # Set via credentials utility
      sfm_collection_interval: 300



#. **Set OME/SFM credentials** using the credential utility:


**Run on: omnia_core container**

.. code-block:: bash
      cd /omnia/utils/credential_utility
      ansible-playbook get_config_credentials.yml --tags telemetry



#. **Verify OME API access** from the K8s cluster:


**Run on: K8s control plane node**

.. code-block:: bash
      curl -sk https://10.5.1.50/api/SessionService/Sessions \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"UserName":"omnia_readonly","Password":"YourPassword","SessionType":"API"}'



#. **Run the telemetry playbook** to deploy the OME/SFM collectors:


**Run on: omnia_core container**

.. code-block:: bash
      cd /omnia
      ansible-playbook telemetry.yml --ask-vault-pass



   The playbook will:

  - Deploy an OME telemetry collector pod on the K8s cluster.
  - Deploy an SFM telemetry collector pod (if enabled).
  - Configure collectors to push metrics to Kafka.
  - Import pre-built Grafana dashboards for OME and SFM data.



Verification
------------


#. **Verify OME/SFM collector pods are running**:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl get pods -n telemetry | grep -E "ome|sfm"



#. **Check collector logs** for successful data collection:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl logs -n telemetry -l app=ome-collector --tail=20
      kubectl logs -n telemetry -l app=sfm-collector --tail=20



#. **Verify OME metrics in VictoriaMetrics**:


**Run on: K8s control plane node**

.. code-block:: bash
      VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
      kubectl exec -n telemetry $VM_POD -- \
        curl -s "http://localhost:8428/api/v1/query?query=ome_device_health"



#. **Check Grafana dashboards** for OME/SFM panels:

   Open Grafana and navigate to the **OME Overview** and **SFM Fabric Health**
   dashboards.



Next Steps
----------


- :doc:`Verify Telemetry <verify_telemetry>` -- End-to-end telemetry verification.
- :doc:`Configure Ldms <configure_ldms>` -- Add LDMS metrics alongside OME data.



Troubleshooting
---------------


**OME collector returns "authentication failed"**
   Verify credentials:


**Run on: K8s control plane node**

.. code-block:: bash
      curl -sk https://10.5.1.50/api/SessionService/Sessions \
        -X POST -H "Content-Type: application/json" \
        -d '{"UserName":"omnia_readonly","Password":"YourPassword","SessionType":"API"}'



**OME collector returns "connection refused"**
   Check network connectivity:


**Run on: K8s worker node**

.. code-block:: bash
      curl -sk https://10.5.1.50/api/ApplicationService/Info



**SFM metrics not appearing**
   Verify SFM is accessible and the API version is supported:


**Run on: K8s worker node**

.. code-block:: bash
      curl -sk https://10.5.1.51/api/



**Certificate errors with OME/SFM**
   If using self-signed certificates, configure the collectors to skip
   TLS verification (development only) or import the CA certificate.
