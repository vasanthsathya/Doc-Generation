
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Verify Telemetry 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../../index.html)

[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../../index.html)

Overview 
 * [ Architecture ](../../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](../Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](setup_telemetry.html)
 * Verify Telemetry [ Verify Telemetry ](verify_telemetry.html) Table of contents 
 * [ Overview ](#overview)
 * Containers Containers 
 * [ Use Apptainer ](../Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Overview ](#overview)

 1. [ Home ](../../index.html)
 2. [ How-to Guides ](../index.html)
 3. [ Telemetry ](setup_telemetry.html)

# Verify Telemetry[¶](#verify-telemetry "Permanent link")

Perform an end-to-end verification of the Omnia telemetry pipeline from data collection through storage to visualization.

## Overview[¶](#overview "Permanent link")

A complete telemetry verification traces the data flow through every stage:

 1. **Collection** \-- iDRAC collectors and LDMS samplers are generating metrics.
 2. **Transport** \-- Kafka topics are receiving messages.
 3. **Storage** \-- VictoriaMetrics is ingesting and storing time-series data.
 4. **Visualization** \-- Grafana dashboards display live data.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Setup Telemetry](setup_telemetry.html) procedure is complete.
 * The K8s service cluster is running with telemetry pods.
 * LDMS agents are deployed on compute nodes.
 * Grafana is accessible via the browser.

## Procedure[¶](#procedure "Permanent link")

### Stage 1: Verify Collection[¶](#stage-1-verify-collection "Permanent link")

 1. **Check iDRAC collector** is retrieving metrics:

Run on: K8s control plane node
 
 
 kubectl logs -n telemetry -l app=idrac-collector --tail=10
 

Look for successful metric retrieval messages.

 1. **Check LDMS samplers** are running on compute nodes:

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "systemctl is-active ldmsd"
 

 1. **Query LDMS metrics** locally on a compute node:

Run on: compute node
 
 
 ldms_ls -h localhost -p 411 -v
 

Should list active metric sets.

### Stage 2: Verify Transport (Kafka)[¶](#stage-2-verify-transport-kafka "Permanent link")

 1. **List Kafka topics** :

Run on: K8s control plane node
 
 
 KAFKA_POD=$(kubectl get pod -n telemetry -l app=kafka -o jsonpath='{.items[0].metadata.name}')
 kubectl exec -n telemetry $KAFKA_POD -- kafka-topics.sh --list --bootstrap-server localhost:9092
 

 1. **Check topic message counts** :

Run on: K8s control plane node
 
 
 kubectl exec -n telemetry $KAFKA_POD -- kafka-run-class.sh kafka.tools.GetOffsetShell \
 --broker-list localhost:9092 --topic omnia-telemetry
 

Message offsets should be increasing.

 1. **Read sample messages** from a topic:

Run on: K8s control plane node
 
 
 kubectl exec -n telemetry $KAFKA_POD -- kafka-console-consumer.sh \
 --bootstrap-server localhost:9092 \
 --topic omnia-telemetry \
 --from-beginning \
 --max-messages 3
 

### Stage 3: Verify Storage (VictoriaMetrics)[¶](#stage-3-verify-storage-victoriametrics "Permanent link")

 1. **Check VictoriaMetrics health** :

Run on: K8s control plane node
 
 
 VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
 kubectl exec -n telemetry $VM_POD -- curl -s http://localhost:8428/health
 

Expected: `OK`

 1. **Query stored metrics** :

Run on: K8s control plane node
 
 
 kubectl exec -n telemetry $VM_POD -- \
 curl -s "http://localhost:8428/api/v1/query?query=up" | python3 -m json.tool
 

 1. **Check active time series count** :

Run on: K8s control plane node
 
 
 kubectl exec -n telemetry $VM_POD -- \
 curl -s "http://localhost:8428/api/v1/status/tsdb" | python3 -c "
 import sys, json
 data = json.load(sys.stdin)
 print(f'Active time series: {data.get(\"data\", {}).get(\"totalSeries\", \"unknown\")}')
 "
 

 1. **Query a specific metric** (e.g., iDRAC temperature):

Run on: K8s control plane node
 
 kubectl exec -n telemetry $VM_POD -- \
 curl -s "http://localhost:8428/api/v1/query?query=idrac_SystemBoardInletTemp"
 

### Stage 4: Verify Visualization (Grafana)[¶](#stage-4-verify-visualization-grafana "Permanent link")

 1. **Get the Grafana external IP** :

Run on: K8s control plane node
 
 kubectl get svc -n telemetry grafana
 

 2. **Open Grafana** in a browser: `http://<grafana-ip>:3000`

 3. **Verify data sources** :

Navigate to **Configuration** > **Data Sources**. The VictoriaMetrics data source should show a green "Data source is working" indicator.

 4. **Check pre-configured dashboards** :

Navigate to **Dashboards** > **Browse**. Verify the following dashboards exist and show data:

 * **Cluster Overview** \-- Node status, overall health
 * **iDRAC Metrics** \-- Temperatures, power, fan speeds
 * **LDMS Metrics** \-- CPU, memory, I/O per node
 * **Network Fabric** \-- (if SFM is configured) port throughput

## Verification[¶](#verification "Permanent link")

Use this checklist to confirm the entire pipeline is operational:

Stage | Check | Expected Result 
---|---|--- 
Collection | `ldms_ls -h localhost -p 411` | Active metric sets 
Collection | iDRAC collector pod logs | Successful retrieval 
Transport | Kafka topic list | Topics exist 
Transport | Console consumer | Messages readable 
Storage | `/health` endpoint | `OK` 
Storage | `/api/v1/query?query=up` | Non-empty results 
Visualization | Grafana data source test | Green indicator 
Visualization | Dashboard shows graphs | Data within last hour 
 
## Next Steps[¶](#next-steps "Permanent link")

 * [Configure Ldms](configure_ldms.html) \-- Fine-tune metric collection.
 * [Configure External Kafka](configure_external_kafka.html) \-- Scale the transport layer.
 * [Configure External Victoria](configure_external_victoria.html) \-- Scale the storage layer.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**No data at any stage** Start from the collection stage and trace forward:

 1. Are LDMS/iDRAC collectors running?
 2. Are Kafka topics receiving messages?
 3. Is VictoriaMetrics ingesting data?
 4. Is Grafana configured with the correct data source?

**Data gap in Grafana (intermittent)** \- Check for pod restarts:
 
 
 ```bash title="Run on: K8s control plane node"
 kubectl get pods -n telemetry -o wide
 ```
 

 * Check K8s node resources (CPU/memory):

Run on: K8s control plane node
 
 kubectl top nodes
 kubectl top pods -n telemetry
 

**Metrics have stale timestamps** \- Verify NTP is synchronized on all nodes:
 
 
 ```bash title="Run on: omnia_core container"
 ansible all -m shell -a "chronyc tracking | grep 'System time'"
 ```
 

**VictoriaMetrics running out of disk** Check retention settings and disk usage:

Run on: K8s control plane node
 
 
 kubectl exec -n telemetry $VM_POD -- df -h /victoria-metrics-data
 

Back to top [ Previous Set Up Telemetry ](setup_telemetry.html) [ Next Telemetry from OME ](telemetry_from_ome.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
