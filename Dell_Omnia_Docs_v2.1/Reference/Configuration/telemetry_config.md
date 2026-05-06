
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Telemetry Config 

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
 * [ Prepare OIM ](../../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](omnia_config.html)
 * Telemetry Config [ Telemetry Config ](telemetry_config.html) Table of contents 
 * [ General telemetry settings ](#general-telemetry-settings)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ General telemetry settings ](#general-telemetry-settings)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Configuration ](omnia_config.html)

# telemetry_config.yml Reference[¶](#telemetry_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/telemetry_config.yml`

This file configures the Omnia telemetry pipeline: iDRAC metric collection, Kafka message streaming, VictoriaMetrics time-series storage, Grafana dashboards, and LDMS node-level samplers.

## General telemetry settings[¶](#general-telemetry-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`enable_telemetry` | Boolean | No | `false` | Master switch for the telemetry pipeline. When `false`, all telemetry components are skipped. 
`telemetry_entry_node` | String | Conditional | (none) | Hostname or IP of the node where telemetry services (Kafka, VictoriaMetrics, Grafana) are deployed. Required when `enable_telemetry` is `true`. 
 
## Kafka settings[¶](#kafka-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`kafka_broker_port` | Integer | No | `9092` | Port on which Kafka listens for producer/consumer connections. 
`kafka_topic_idrac` | String | No | `idrac_telemetry` | Kafka topic name for iDRAC telemetry data. 
`kafka_topic_ldms` | String | No | `ldms_telemetry` | Kafka topic name for LDMS node-level metrics. 
`kafka_retention_hours` | Integer | No | `168` | Number of hours to retain messages in Kafka topics (default: 7 days). 
`kafka_log_dir` | String | No | `/var/lib/kafka/data` | Directory for Kafka commit logs. Ensure sufficient disk space. 
 
## VictoriaMetrics settings[¶](#victoriametrics-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`victoriametrics_port` | Integer | No | `8428` | HTTP port for VictoriaMetrics query and ingestion API. 
`victoriametrics_retention` | String | No | `6` | Data retention period in months. Older data is automatically purged. 
`victoriametrics_storage_path` | String | No | `/var/lib/victoria-metrics` | Persistent data directory for VictoriaMetrics. 
 
## Grafana settings[¶](#grafana-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`grafana_port` | Integer | No | `3000` | HTTP port for the Grafana web interface. 
`grafana_admin_user` | String | No | `admin` | Grafana administrator username. 
`grafana_admin_password` | String | No | (vault-managed) | Grafana administrator password. Set via `credentials_utility.yml`. 
 
## iDRAC telemetry settings[¶](#idrac-telemetry-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`enable_idrac_telemetry` | Boolean | No | `true` | Collect power, thermal, and health metrics from iDRAC via Redfish. Only effective when `enable_telemetry` is `true`. 
`idrac_telemetry_interval` | Integer | No | `300` | Collection interval in seconds (default: 5 minutes). 
`idrac_username` | String | Conditional | (none) | iDRAC username for Redfish API access. Set via `credentials_utility.yml`. 
`idrac_password` | String | Conditional | (vault-managed) | iDRAC password. Set via `credentials_utility.yml`. 
 
## LDMS settings[¶](#ldms-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`enable_ldms` | Boolean | No | `true` | Enable LDMS metric samplers on compute nodes. Only effective when `enable_telemetry` is `true`. 
`ldms_samplers` | List | No | `[meminfo, vmstat, procstat, procnetdev]` | List of LDMS sampler plugins to activate. See [Ldms Metrics](../Metrics/ldms_metrics.html) for the full catalog. 
`ldms_sample_interval` | Integer | No | `10` | Sampling interval in seconds. 
`ldms_aggregator_port` | Integer | No | `10001` | Port for the LDMS aggregator daemon. 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/telemetry_config.yml
 
 
 enable_telemetry: true
 telemetry_entry_node: "kube-cp-01"
 
 kafka_broker_port: 9092
 kafka_retention_hours: 168
 
 victoriametrics_port: 8428
 victoriametrics_retention: "6"
 
 grafana_port: 3000
 
 enable_idrac_telemetry: true
 idrac_telemetry_interval: 300
 
 enable_ldms: true
 ldms_samplers:
 - meminfo
 - vmstat
 - procstat
 - procnetdev
 ldms_sample_interval: 10
 

Info

 * [Idrac Metrics](../Metrics/idrac_metrics.html) \-- iDRAC metric catalog.
 * [Ldms Metrics](../Metrics/ldms_metrics.html) \-- LDMS sampler metric catalog.
 * [Gpu Metrics](../Metrics/gpu_metrics.html) \-- GPU metric catalog.
 * [Ports](../ClusterRequirements/ports.html) \-- Ports used by telemetry services.

Back to top [ Previous Software Config ](software_config.html) [ Next Storage Config ](storage_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
