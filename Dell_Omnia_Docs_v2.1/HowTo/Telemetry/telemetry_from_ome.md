
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Telemetry from OME 

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
 * Telemetry from OME [ Telemetry from OME ](telemetry_from_ome.html) Table of contents 
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

# Telemetry from OME & SFM[¶](#telemetry-from-ome-sfm "Permanent link")

Collect telemetry data from Dell OpenManage Enterprise (OME) and Smart Fabric Manager (SFM) in addition to direct iDRAC and LDMS metrics.

## Overview[¶](#overview "Permanent link")

OpenManage Enterprise (OME) aggregates hardware health, alerts, and inventory data from all Dell servers it manages. Smart Fabric Manager (SFM) provides network fabric metrics from Dell switches. By integrating OME and SFM telemetry into Omnia's pipeline, you get:

 * Aggregated server health dashboards from OME.
 * Network fabric metrics (port throughput, errors) from SFM.
 * Correlated views of compute + network performance in Grafana.

## Prerequisites[¶](#prerequisites "Permanent link")

 * OME is deployed and managing the Dell servers in your cluster.
 * SFM is deployed and managing Dell networking switches (optional).
 * The [Setup Telemetry](setup_telemetry.html) procedure is complete.
 * Network connectivity from the K8s service cluster to OME and SFM management IPs.
 * OME API credentials (read-only user recommended).

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure OME telemetry** in `omnia_config.yml`:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # OME telemetry configuration
 ome_telemetry_enabled: true
 ome_ip: "10.5.1.50"
 ome_port: 443
 ome_username: "omnia_readonly"
 ome_password: "" # Set via credentials utility
 ome_collection_interval: 300 # seconds
 
 # SFM telemetry configuration (optional)
 sfm_telemetry_enabled: true
 sfm_ip: "10.5.1.51"
 sfm_port: 443
 sfm_username: "omnia_readonly"
 sfm_password: "" # Set via credentials utility
 sfm_collection_interval: 300
 

 1. **Set OME/SFM credentials** using the credential utility:

Run on: omnia_core container
 
 
 cd /omnia/utils/credential_utility
 ansible-playbook get_config_credentials.yml --tags telemetry
 

 1. **Verify OME API access** from the K8s cluster:

Run on: K8s control plane node
 
 
 curl -sk https://10.5.1.50/api/SessionService/Sessions \
 -X POST \
 -H "Content-Type: application/json" \
 -d '{"UserName":"omnia_readonly","Password":"YourPassword","SessionType":"API"}'
 

 1. **Run the telemetry playbook** to deploy the OME/SFM collectors:

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook telemetry.yml --ask-vault-pass
 

The playbook will:

 * Deploy an OME telemetry collector pod on the K8s cluster.
 * Deploy an SFM telemetry collector pod (if enabled).
 * Configure collectors to push metrics to Kafka.
 * Import pre-built Grafana dashboards for OME and SFM data.

## Verification[¶](#verification "Permanent link")

 1. **Verify OME/SFM collector pods are running** :

Run on: K8s control plane node
 
 
 kubectl get pods -n telemetry | grep -E "ome|sfm"
 

 1. **Check collector logs** for successful data collection:

Run on: K8s control plane node
 
 
 kubectl logs -n telemetry -l app=ome-collector --tail=20
 kubectl logs -n telemetry -l app=sfm-collector --tail=20
 

 1. **Verify OME metrics in VictoriaMetrics** :

Run on: K8s control plane node
 
 
 VM_POD=$(kubectl get pod -n telemetry -l app=victoriametrics -o jsonpath='{.items[0].metadata.name}')
 kubectl exec -n telemetry $VM_POD -- \
 curl -s "http://localhost:8428/api/v1/query?query=ome_device_health"
 

 1. **Check Grafana dashboards** for OME/SFM panels:

Open Grafana and navigate to the **OME Overview** and **SFM Fabric Health** dashboards.

## Next Steps[¶](#next-steps "Permanent link")

 * [Verify Telemetry](verify_telemetry.html) \-- End-to-end telemetry verification.
 * [Configure Ldms](configure_ldms.html) \-- Add LDMS metrics alongside OME data.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**OME collector returns "authentication failed"** Verify credentials:

Run on: K8s control plane node
 
 
 curl -sk https://10.5.1.50/api/SessionService/Sessions \
 -X POST -H "Content-Type: application/json" \
 -d '{"UserName":"omnia_readonly","Password":"YourPassword","SessionType":"API"}'
 

**OME collector returns "connection refused"** Check network connectivity:

Run on: K8s worker node
 
 
 curl -sk https://10.5.1.50/api/ApplicationService/Info
 

**SFM metrics not appearing** Verify SFM is accessible and the API version is supported:

Run on: K8s worker node
 
 
 curl -sk https://10.5.1.51/api/
 

**Certificate errors with OME/SFM** If using self-signed certificates, configure the collectors to skip TLS verification (development only) or import the CA certificate.

Back to top [ Previous Verify Telemetry ](verify_telemetry.html) [ Next Configure LDMS ](configure_ldms.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
