

Configure LDMS
==============


Fine-tune LDMS (Lightweight Distributed Metric Service) sampler plugins and
aggregation configuration for custom metric collection on compute nodes.


Overview
--------


LDMS runs two types of daemons:

- **Samplers** (on compute nodes) -- Collect OS-level metrics at regular
  intervals.
- **Aggregators** (on K8s service cluster) -- Collect samples from all compute
  nodes and forward them to the storage backend (Kafka/VictoriaMetrics).

This guide shows how to configure sampler plugins (``meminfo``, ``vmstat``,
``procstat``, and others) and adjust aggregation parameters.



Prerequisites
-------------


- The :doc:`Setup Telemetry <setup_telemetry>` procedure is complete (LDMS is deployed).
- LDMS agents are running on compute nodes.
- Aggregators are running on the K8s service cluster.



Procedure
---------


#. **Review available LDMS sampler plugins**:


   .. code-block:: bash
      :caption: Run on: compute node

         ldms_ls -h localhost -p 411 -v



   Common sampler plugins:

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      - - Plugin
        - Metrics Collected
      - - ``meminfo``
        - Memory usage (MemTotal, MemFree, Buffers, Cached, SwapTotal, etc.)
      - - ``vmstat``
        - Virtual memory statistics (page faults, swaps, context switches)
      - - ``procstat``
        - Per-CPU usage statistics (user, system, idle, iowait)
      - - ``lustre_client``
        - Lustre filesystem client statistics
      - - ``ibnet``
        - InfiniBand network counters
      - - ``slurm_sampler``
        - Slurm job-level metrics

#. **Configure sampler plugins** on a compute node:


   .. code-block:: bash
      :caption: Run on: compute node

         vi /etc/ldms/ldmsd.conf



   Example sampler configuration:


**File: /etc/ldms/ldmsd.conf on compute node**

.. code-block:: text

      # Transport and authentication
      auth_add name=munge plugin=munge

      # Listen for connections
      listen xprt=sock port=411 auth=munge

      # Load sampler plugins
      load name=meminfo
      config name=meminfo producer=${HOSTNAME} instance=${HOSTNAME}/meminfo \
             schema=meminfo component_id=${COMPONENT_ID}
      start name=meminfo interval=10000000

      load name=vmstat
      config name=vmstat producer=${HOSTNAME} instance=${HOSTNAME}/vmstat \
             schema=vmstat component_id=${COMPONENT_ID}
      start name=vmstat interval=10000000

      load name=procstat
      config name=procstat producer=${HOSTNAME} instance=${HOSTNAME}/procstat \
             schema=procstat component_id=${COMPONENT_ID}
      start name=procstat interval=10000000



   !!! note

       The ``interval`` is in microseconds. ``10000000`` = 10 seconds.

#. **Restart the LDMS sampler daemon** after configuration changes:


   .. code-block:: bash
      :caption: Run on: compute node

         systemctl restart ldmsd



#. **Configure the LDMS aggregator** on the K8s cluster:


   .. code-block:: bash
      :caption: Run on: K8s control plane node

         kubectl edit configmap -n telemetry ldms-aggregator-config



   Example aggregator configuration:


**ConfigMap: ldms-aggregator-config in telemetry namespace**

.. code-block:: text

      # Authentication
      auth_add name=munge plugin=munge

      # Listen for downstream connections
      listen xprt=sock port=411 auth=munge

      # Add each compute node as a producer
      prdcr_add name=compute01 host=10.5.0.101 port=411 xprt=sock \
                auth=munge type=active interval=30000000
      prdcr_start name=compute01

      prdcr_add name=compute02 host=10.5.0.102 port=411 xprt=sock \
                auth=munge type=active interval=30000000
      prdcr_start name=compute02

      # Start the updater to collect from all producers
      updtr_add name=all_nodes interval=30000000 offset=100000
      updtr_prdcr_add name=all_nodes regex=.*
      updtr_start name=all_nodes



#. **Restart the aggregator pod**:


   .. code-block:: bash
      :caption: Run on: K8s control plane node

         kubectl rollout restart deployment -n telemetry ldms-aggregator



#. **(Bulk configuration) Deploy to all compute nodes** via Ansible:


   .. code-block:: bash
      :caption: Run on: omnia_core container

         ansible slurm_node -m copy -a "src=/tmp/ldmsd.conf dest=/etc/ldms/ldmsd.conf"
         ansible slurm_node -m service -a "name=ldmsd state=restarted"





Verification
------------


#. **Verify sampler data** on a compute node:


   .. code-block:: bash
      :caption: Run on: compute node

         ldms_ls -h localhost -p 411 -v



   Expected: list of active metric sets (meminfo, vmstat, procstat).

#. **Query specific metrics**:


   .. code-block:: bash
      :caption: Run on: compute node

         ldms_ls -h localhost -p 411 -l -v | grep MemFree



#. **Verify the aggregator is collecting** from compute nodes:


   .. code-block:: bash
      :caption: Run on: K8s control plane node

         AGG_POD=$(kubectl get pod -n telemetry -l app=ldms-aggregator -o jsonpath='{.items[0].metadata.name}')
         kubectl exec -n telemetry $AGG_POD -- ldms_ls -h localhost -p 411 -v



#. **Verify data reaches VictoriaMetrics**:


   .. code-block:: bash
      :caption: Run on: K8s control plane node

         VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
         kubectl exec -n telemetry $VM_POD -- curl -s "http://localhost:8428/api/v1/query?query=meminfo_MemFree"





Next Steps
----------


- :doc:`Verify Telemetry <verify_telemetry>` -- End-to-end telemetry verification.
- :doc:`Configure External Kafka <configure_external_kafka>` -- Route LDMS data through external Kafka.



Troubleshooting
---------------


**ldmsd fails to start**
   Check configuration syntax:


   .. code-block:: bash
      :caption: Run on: compute node

         ldmsd -c /etc/ldms/ldmsd.conf -F -v DEBUG 2>&1 | head -50



**"Connection refused" from aggregator to sampler**
   Verify the sampler is listening:


   .. code-block:: bash
      :caption: Run on: compute node

         ss -tlnp | grep 411



   Check firewall:


   .. code-block:: bash
      :caption: Run on: compute node

         firewall-cmd --add-port=411/tcp --permanent
         firewall-cmd --reload



**Munge authentication failure**
   Ensure the Munge key is the same on compute nodes and aggregator:


   .. code-block:: bash
      :caption: Run on: omnia_core container

         ansible slurm_node -m shell -a "md5sum /etc/munge/munge.key"



**Metrics not appearing in VictoriaMetrics**
   Check the Kafka-to-VictoriaMetrics consumer logs:


   .. code-block:: bash
      :caption: Run on: K8s control plane node

         kubectl logs -n telemetry -l app=kafka-consumer --tail=30

