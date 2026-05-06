
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

External Kafka 

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
 * External Kafka [ External Kafka ](configure_external_kafka.html) Table of contents 
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

# Configure External Kafka[¶](#configure-external-kafka "Permanent link")

Replace Omnia's built-in Kafka deployment with an external Kafka cluster for telemetry data streaming.

## Overview[¶](#overview "Permanent link")

By default, Omnia deploys a single-node Kafka instance on the K8s service cluster. For production environments with high metric volumes or existing Kafka infrastructure, you can configure Omnia to use an external Kafka cluster.

Benefits of external Kafka:

 * Higher throughput and replication for fault tolerance.
 * Integration with existing data pipelines.
 * Centralized message broker management.

## Prerequisites[¶](#prerequisites "Permanent link")

 * An external Kafka cluster (version 3.x or later) is operational and accessible from the K8s service cluster.
 * Kafka topics for telemetry are created (or auto-create is enabled).
 * Network connectivity between the OIM, K8s cluster, and the Kafka brokers.
 * The [Setup Telemetry](setup_telemetry.html) procedure has been reviewed (understand the default telemetry architecture).

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure external Kafka** in `omnia_config.yml`:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # External Kafka configuration
 kafka_external: true
 kafka_bootstrap_servers: "kafka-broker1.example.com:9092,kafka-broker2.example.com:9092,kafka-broker3.example.com:9092"
 kafka_telemetry_topic: "omnia-telemetry"
 kafka_idrac_topic: "omnia-idrac"
 kafka_ldms_topic: "omnia-ldms"
 
 # Optional: Kafka authentication
 kafka_security_protocol: "SASL_PLAINTEXT" # or "PLAINTEXT", "SSL", "SASL_SSL"
 kafka_sasl_mechanism: "PLAIN"
 kafka_sasl_username: "omnia-telemetry"
 kafka_sasl_password: "" # Set via credentials utility
 

 1. **Create the required Kafka topics** on the external cluster (if auto-create is disabled):

Run on: external Kafka broker
 
 
 kafka-topics.sh --create \
 --bootstrap-server localhost:9092 \
 --topic omnia-telemetry \
 --partitions 6 \
 --replication-factor 3
 
 kafka-topics.sh --create \
 --bootstrap-server localhost:9092 \
 --topic omnia-idrac \
 --partitions 3 \
 --replication-factor 3
 
 kafka-topics.sh --create \
 --bootstrap-server localhost:9092 \
 --topic omnia-ldms \
 --partitions 6 \
 --replication-factor 3
 

 1. **Run the telemetry playbook** to reconfigure:

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook telemetry.yml --ask-vault-pass
 

The playbook will:

 * Skip deploying the built-in Kafka pod.
 * Configure iDRAC and LDMS collectors to publish to the external Kafka.
 * Configure VictoriaMetrics consumer to read from the external Kafka.

## Verification[¶](#verification "Permanent link")

 1. **Verify Kafka connectivity** from the K8s cluster:

Run on: K8s control plane node
 
 
 kubectl run kafka-test --image=bitnami/kafka:latest --restart=Never -- \
 kafka-topics.sh --list --bootstrap-server kafka-broker1.example.com:9092
 kubectl logs kafka-test
 kubectl delete pod kafka-test
 

 1. **Verify topics have data** :

Run on: external Kafka broker
 
 
 kafka-console-consumer.sh \
 --bootstrap-server localhost:9092 \
 --topic omnia-telemetry \
 --from-beginning \
 --max-messages 5
 

 1. **Verify no built-in Kafka pod** is running:

Run on: K8s control plane node
 
 
 kubectl get pods -n telemetry | grep kafka
 

Should show no locally deployed Kafka pods.

 1. **Verify data reaches VictoriaMetrics** :

Run on: K8s control plane node
 
 
 VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
 kubectl exec -n telemetry $VM_POD -- curl -s "http://localhost:8428/api/v1/query?query=up"
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Configure External Victoria](configure_external_victoria.html) \-- Use an external VictoriaMetrics.
 * [Verify Telemetry](verify_telemetry.html) \-- End-to-end verification.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Collectors cannot connect to Kafka** Verify network connectivity:

Run on: K8s worker node
 
 
 telnet kafka-broker1.example.com 9092
 

**SASL authentication failure** Verify credentials are correct in the configuration. Check Kafka broker logs for authentication errors.

**Data not appearing in topics** Check collector logs:

Run on: K8s control plane node
 
 
 kubectl logs -n telemetry -l app=idrac-collector --tail=30
 kubectl logs -n telemetry -l app=ldms-aggregator --tail=30
 

**Consumer lag is high** Check consumer group status:

Run on: external Kafka broker
 
 
 kafka-consumer-groups.sh \
 --bootstrap-server localhost:9092 \
 --group omnia-victoria-consumer \
 --describe
 

Back to top [ Previous Configure LDMS ](configure_ldms.html) [ Next External VictoriaMetrics ](configure_external_victoria.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
