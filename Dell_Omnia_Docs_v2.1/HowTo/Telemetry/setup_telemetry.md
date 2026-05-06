
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Set Up Telemetry 

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
 * Set Up Telemetry [ Set Up Telemetry ](setup_telemetry.html) Table of contents 
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

# Setup Telemetry[¶](#setup-telemetry "Permanent link")

Deploy the Omnia telemetry pipeline using `telemetry.yml` to collect, aggregate, and visualize hardware and OS metrics from across the cluster.

## Overview[¶](#overview "Permanent link")

The Omnia telemetry pipeline collects metrics from multiple sources and stores them for visualization in Grafana. Running `telemetry.yml` deploys:

 * **iDRAC Telemetry Collector** \-- Collects hardware metrics (temperatures, power, fan speeds) from Dell iDRAC via Redfish.
 * **LDMS (Lightweight Distributed Metric Service)** \-- Collects OS-level metrics (CPU, memory, I/O) from compute nodes.
 * **Kafka** \-- Message broker for streaming metrics.
 * **VictoriaMetrics** \-- Time-series database for metric storage.
 * **Grafana** \-- Visualization dashboards.

The telemetry services run as pods on the Kubernetes service cluster.

## Prerequisites[¶](#prerequisites "Permanent link")

 * A Kubernetes service cluster is deployed (see [Setup Service K8S](../Kubernetes/setup_service_k8s.html)).
 * The Slurm cluster is deployed (for LDMS agent deployment on compute nodes).
 * `omnia_config.yml` is configured with telemetry parameters.
 * iDRAC credentials are configured (see [Configure Credentials](../Setup/configure_credentials.html)).
 * The K8s cluster has persistent storage available (NFS CSI or PowerScale CSI).

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure telemetry parameters** in `omnia_config.yml`:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # Telemetry configuration
 enable_telemetry: true
 telemetry_collection_interval: 60 # seconds
 grafana_admin_password: "" # Set via credentials utility
 
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
 

 1. **Run the telemetry playbook** :

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook telemetry.yml --ask-vault-pass
 

The playbook performs:

 * Deploys Kafka on the K8s service cluster.
 * Deploys VictoriaMetrics for time-series storage.
 * Deploys Grafana with pre-configured dashboards.
 * Deploys the iDRAC telemetry collector.
 * Installs and configures LDMS samplers on compute nodes.
 * Installs LDMS aggregators on the K8s cluster.
 * Configures data flow: LDMS/iDRAC → Kafka → VictoriaMetrics → Grafana.

Execution time: **15-30 minutes**.

 1. **Access the Grafana dashboard** :

Run on: K8s control plane node
 
 
 kubectl get svc -n telemetry | grep grafana
 

Note the external IP (from MetalLB). Open a browser and navigate to:

`http://<grafana-external-ip>:3000`

Default credentials:

 * Username: `admin`
 * Password: (as configured in omnia_config.yml or credentials utility)

## Verification[¶](#verification "Permanent link")

 1. **Verify telemetry pods are running** :

Run on: K8s control plane node
 
 
 kubectl get pods -n telemetry
 

Expected pods:

Expected output on: K8s control plane node
 
 
 NAME READY STATUS RESTARTS
 grafana-xxxxxxxxxx-xxxxx 1/1 Running 0
 kafka-0 1/1 Running 0
 victoriametrics-xxxxxxxxxx-xxxxx 1/1 Running 0
 idrac-collector-xxxxxxxxxx-xxxxx 1/1 Running 0
 ldms-aggregator-xxxxxxxxxx-xxxxx 1/1 Running 0
 

 1. **Verify LDMS agents on compute nodes** :

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "systemctl is-active ldmsd"
 

 1. **Check Kafka topics** have telemetry data:

Run on: K8s control plane node
 
 
 kubectl exec -n telemetry kafka-0 -- kafka-topics.sh --list --bootstrap-server localhost:9092
 

 1. **Verify VictoriaMetrics is receiving data** :

Run on: K8s control plane node
 
 
 VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
 kubectl exec -n telemetry $VM_POD -- curl -s "http://localhost:8428/api/v1/query?query=up" | python3 -m json.tool
 

 1. **Verify Grafana dashboards** show data by opening the web UI and checking the pre-configured dashboards for active time-series data.

## Next Steps[¶](#next-steps "Permanent link")

 * [Configure Ldms](configure_ldms.html) \-- Fine-tune LDMS sampler plugins.
 * [Configure External Kafka](configure_external_kafka.html) \-- Use an external Kafka cluster.
 * [Configure External Victoria](configure_external_victoria.html) \-- Use an external VictoriaMetrics instance.
 * [Verify Telemetry](verify_telemetry.html) \-- End-to-end telemetry verification.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Telemetry pods stuck in Pending** Check for persistent volume issues:

Run on: K8s control plane node
 
 
 kubectl describe pvc -n telemetry
 

**iDRAC collector shows errors** Verify iDRAC credentials and Redfish access:

Run on: K8s control plane node
 
 
 kubectl logs -n telemetry -l app=idrac-collector --tail=30
 

**LDMS agents not running on compute nodes** Re-deploy LDMS:

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "systemctl restart ldmsd"
 

**Grafana shows "No data"** \- Verify the VictoriaMetrics data source is configured in Grafana. \- Check the time range in Grafana (default to "Last 1 hour"). \- Verify data is flowing through Kafka:
 
 
 ```bash title="Run on: K8s control plane node"
 kubectl exec -n telemetry kafka-0 -- kafka-console-consumer.sh \
 --bootstrap-server localhost:9092 --topic telemetry --from-beginning --max-messages 5
 ```
 

**Kafka pod CrashLoopBackOff** Check disk space on the K8s worker node:

Run on: K8s worker node
 
 
 df -h
 

Back to top [ Previous Replicate LDAP ](../Authentication/replicate_ldap.html) [ Next Verify Telemetry ](verify_telemetry.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
