
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

External VictoriaMetrics 

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
 * External VictoriaMetrics [ External VictoriaMetrics ](configure_external_victoria.html) Table of contents 
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

# Configure External VictoriaMetrics[¶](#configure-external-victoriametrics "Permanent link")

Replace Omnia's built-in VictoriaMetrics deployment with an external VictoriaMetrics instance for telemetry data storage.

## Overview[¶](#overview "Permanent link")

For organizations with existing monitoring infrastructure or requirements for a dedicated time-series database, Omnia can be configured to write telemetry data to an external VictoriaMetrics instance instead of deploying one on the K8s service cluster.

Benefits:

 * Centralized metric storage across multiple clusters.
 * Dedicated compute and storage resources for time-series data.
 * Integration with existing Grafana instances and alerting rules.

## Prerequisites[¶](#prerequisites "Permanent link")

 * An external VictoriaMetrics instance (single-node or cluster mode) is operational and accessible.
 * The VictoriaMetrics write endpoint (`/api/v1/write`) is reachable from the K8s service cluster.
 * The [Setup Telemetry](setup_telemetry.html) procedure has been reviewed.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure external VictoriaMetrics** in `omnia_config.yml`:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # External VictoriaMetrics configuration
 victoriametrics_external: true
 victoriametrics_write_url: "http://victoria.example.com:8428/api/v1/write"
 victoriametrics_read_url: "http://victoria.example.com:8428"
 
 # Optional: authentication
 victoriametrics_auth_enabled: false
 victoriametrics_username: ""
 victoriametrics_password: ""
 
 # Optional: custom labels added to all metrics
 victoriametrics_extra_labels:
 cluster: "omnia-prod"
 datacenter: "dc1"
 

 1. **Verify connectivity** to the external VictoriaMetrics:

Run on: K8s control plane node
 
 
 curl -s http://victoria.example.com:8428/api/v1/status/tsdb
 

Expected: JSON response with database statistics.

 1. **Run the telemetry playbook** to reconfigure:

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook telemetry.yml --ask-vault-pass
 

The playbook will:

 * Skip deploying the built-in VictoriaMetrics pod.
 * Configure Kafka consumers to write to the external VictoriaMetrics.
 * Update Grafana data source to point to the external instance.

 * **Update Grafana data source** (if not automatically configured):

Run on: K8s control plane node
 
 
 GRAFANA_POD=$(kubectl get pod -n telemetry -l app=grafana -o jsonpath='{.items[0].metadata.name}')
 kubectl exec -n telemetry $GRAFANA_POD -- \
 curl -s -X POST http://localhost:3000/api/datasources \
 -H "Content-Type: application/json" \
 -u admin:YourGrafanaPassword \
 -d '{
 "name": "VictoriaMetrics External",
 "type": "prometheus",
 "url": "http://victoria.example.com:8428",
 "access": "proxy",
 "isDefault": true
 }'
 

## Verification[¶](#verification "Permanent link")

 1. **Verify data is being written** to the external VictoriaMetrics:

Run on: any node with curl
 
 
 curl -s "http://victoria.example.com:8428/api/v1/query?query=up" | python3 -m json.tool
 

 1. **Check metric count** on the external instance:

Run on: any node with curl
 
 
 curl -s "http://victoria.example.com:8428/api/v1/status/tsdb" | python3 -m json.tool
 

 1. **Verify no built-in VictoriaMetrics pod** is running:

Run on: K8s control plane node
 
 
 kubectl get pods -n telemetry | grep victoriametrics
 

 1. **Verify Grafana dashboards** show data from the external instance by opening the Grafana web UI and checking the data source configuration.

## Next Steps[¶](#next-steps "Permanent link")

 * [Verify Telemetry](verify_telemetry.html) \-- End-to-end telemetry verification.
 * [Telemetry From Ome](telemetry_from_ome.html) \-- Add OME telemetry to the external instance.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Write endpoint returns 403 or 401** Verify authentication credentials are correct:

Run on: K8s control plane node
 
 
 curl -s -u user:password \
 "http://victoria.example.com:8428/api/v1/query?query=up"
 

**Connection timeout to external VictoriaMetrics** Check network connectivity and firewall rules:

Run on: K8s worker node
 
 
 curl -v http://victoria.example.com:8428/health
 

**Grafana shows "No data" with external source** \- Verify the data source URL in Grafana settings. \- Check that the external VictoriaMetrics is receiving data:
 
 
 ```bash title="Run on: any node"
 curl -s "http://victoria.example.com:8428/api/v1/series?match[]={cluster='omnia-prod'}"
 ```
 

**Metrics have wrong labels** Check the `victoriametrics_extra_labels` configuration in `omnia_config.yml`.

Back to top [ Previous External Kafka ](configure_external_kafka.html) [ Next Use Apptainer ](../Containers/use_apptainer.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
