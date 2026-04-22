# VictoriaLogs Cluster Mode — Content Plan

**Product:** Omnia  
**Version:** 2.1.0.0-rc2  
**Feature:** VictoriaLogs Cluster Mode  
**Created:** 2026-04-22  
**Updated:** 2026-04-22 (Updated to reflect existing telemetry structure)  
**Owner:** Documentation Team  
**Status:** Draft  

**Source File Locations:**
- Behaviour Spec: `knowledge_source/victoria_logs_cluster_mode/omnia-telemetry-bspec.md`
- Engineering Specification: `knowledge_source/victoria_logs_cluster_mode/VictoriaLogs_cluster_Engineering_spec(HLD).md`
- Component Specification: `knowledge_source/victoria_logs_cluster_mode/VL_Agent_Component_Spec.md`
- Component Specification: `knowledge_source/victoria_logs_cluster_mode/VL_Cluster_component_spec.md`

**Existing Documentation Analysis:**
- Existing telemetry documentation found at `docs/source/OmniaInstallGuide/RHEL_new/Telemetry/`
- Current telemetry documentation covers VictoriaMetrics (metrics) but NOT VictoriaLogs (logs)
- Telemetry index.rst mentions VictoriaMetrics, Kafka, LDMS, iDRAC — VictoriaLogs is not documented
- Decision: Update existing telemetry structure to include VictoriaLogs, create new VictoriaLogs-specific topics within the telemetry directory

**Source Asset Priority:**
1. Behaviour Spec — Customer interaction details and victoria logs section for doc generation
2. Engineering Specification — Technical architecture and implementation approach
3. Component Specification — Details of each component in engineering specs

---

## Topic 1: Update Telemetry Index to Include VictoriaLogs

| Field | Details |
|-------|---------|
| **Topic Type** | Index Update |
| **Status** | Update Existing Topic |
| **Target Audience** | Infrastructure/HPC Administrator, Platform Engineer |
| **Source Traceability** | Behaviour Spec §5.8, Engineering Spec §2, §3.1 |
| **RST File** | `docs/source/OmniaInstallGuide/RHEL_new/Telemetry/index.rst` |
| **Content Type** | Telemetry/ |

**Customer Workflow Context:**
The existing telemetry index.rst currently documents VictoriaMetrics (metrics), Kafka, LDMS, and iDRAC telemetry but does not mention VictoriaLogs (logs). This update adds VictoriaLogs to the telemetry architecture overview, component list, and data flow diagram to provide a complete picture of the observability stack including both metrics and logs.

**Content Requirements:**
- Add VictoriaLogs to the telemetry components section
- Add VictoriaLogs to the data flow diagram section
- Add VictoriaLogs to the toctree
- Add a brief description of VictoriaLogs capabilities
- Expected outcomes: Telemetry index includes VictoriaLogs alongside VictoriaMetrics, providing complete observability stack documentation
- Warnings/Notes:
  - .. note:: VictoriaLogs is deployed as a mandatory platform service when victoria is present in telemetry_collection_type
  - .. important:: Single-node VictoriaLogs is not supported; cluster mode only for production environments

**Configuration Artifacts:**
- `telemetry_config.yml` — victoria_logs_configurations section (retention_period, storage_size)
- `telemetry_collection_type` — must include "victoria" to deploy VictoriaLogs

**Cross-References:**
- Add reference to new VictoriaLogs topics in toctree
- `external_victoria.rst` (existing VictoriaMetrics documentation)

**Build Agent Instructions:**
- Load existing telemetry index.rst
- Add VictoriaLogs to the "Telemetry Components" section
- Add VictoriaLogs to the data flow diagram section
- Add VictoriaLogs to the toctree
- Preserve existing structure and content
- No SME validation required
- Confidence: High (0.9)
- AI_REVIEW markers: None

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [x] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] None identified

---

## Topic 2: Deploy VictoriaLogs Cluster Mode

| Field | Details |
|-------|---------|
| **Topic Type** | How-To |
| **Status** | New Topic |
| **Target Audience** | Infrastructure/HPC Administrator |
| **Source Traceability** | Behaviour Spec §5.8.2, §5.8.3, Engineering Spec §3.2, §4.1.3.1 |
| **RST File** | `docs/source/OmniaInstallGuide/RHEL_new/Telemetry/deploy_victorialogs.rst` |
| **Content Type** | Telemetry/ |

**Customer Workflow Context:**
As an HPC administrator, I need to deploy VictoriaLogs in cluster mode to enable centralized log management for my Omnia cluster. This procedure guides me through configuring telemetry settings and deploying VictoriaLogs alongside VictoriaMetrics.

**Content Requirements:**
- Prerequisites:
  - Omnia Infrastructure Manager (OIM) deployed
  - Service Kubernetes cluster deployed with at least 2 worker nodes
  - VictoriaMetrics deployment (VictoriaLogs co-deploys with VictoriaMetrics)
  - `pod_external_ip_range` configured in omnia_config.yml
  - Storage provisioner available for PVC provisioning
- Key steps:
  1. Configure victoria_logs_configurations in telemetry_config.yml
     - Set retention_period (default: 168 hours / 7 days)
     - Set storage_size (default: 8Gi per replica, 3 replicas = 24Gi total)
  2. Set telemetry_collection_type to include "victoria"
  3. Run discovery playbook for telemetry deployment
  4. Verify VictoriaLogs cluster components are healthy (vlstorage, vlinsert, vlselect, VLAgent)
  5. Record endpoint information for log source configuration
- Expected outcomes:
  - VictoriaLogs cluster deployed with 3 vlstorage replicas, 2 vlinsert replicas, 2 vlselect replicas
  - VLAgent deployed with syslog receivers on ports 514 (plaintext) and 6514 (TLS)
  - Ingestion and query endpoints accessible via external IPs
  - TLS connectivity validated
- Warnings/Notes:
  - .. important:: Cluster mode requires at least 2 Service Kubernetes worker nodes for pod anti-affinity
  - .. note:: VictoriaLogs shares the same deployment gate as VictoriaMetrics — both deploy when "victoria" is in telemetry_collection_type
  - .. warning:: Storage sizing must account for log volume and retention period (use sizing formula: 140 MB/day × retention_days × node_count)

**Configuration Artifacts:**
- `telemetry_config.yml`:
  ```yaml
  victoria_logs_configurations:
    retention_period: 168  # hours (7 days)
    storage_size: 8Gi      # per replica
  telemetry_collection_type:
    - victoria
  ```
- `omnia_config.yml`:
  ```yaml
  pod_external_ip_range: <IP range reachable from external telemetry sources>
  ```

**Cross-References:**
- `index.rst` (Topic 1 - updated telemetry index)
- `configure_victorialogs_sources.rst` (Topic 3)
- `external_victoria.rst` (existing VictoriaMetrics documentation)

**Build Agent Instructions:**
- Create new RST file
- Section headings:
  - Prerequisites
  - Configure VictoriaLogs Settings
  - Deploy VictoriaLogs Cluster
  - Verify Deployment
  - Record Endpoint Information
- Admonitions:
  - important: Cluster mode node requirement
  - note: Co-deployment with VictoriaMetrics
  - warning: Storage sizing guidance
- No SME validation required
- Confidence: High (0.9)
- AI_REVIEW markers: None

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [x] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] None identified

---

## Topic 3: Configure Log Sources for VictoriaLogs

| Field | Details |
|-------|---------|
| **Topic Type** | How-To |
| **Status** | New Topic |
| **Target Audience** | Infrastructure/HPC Administrator |
| **Source Traceability** | Behaviour Spec §5.8.2, Engineering Spec §3.3 |
| **RST File** | `docs/source/OmniaInstallGuide/RHEL_new/Telemetry/configure_victorialogs_sources.rst` |
| **Content Type** | Telemetry/ |

**Customer Workflow Context:**
As an HPC administrator, I need to configure external log sources (network devices, storage systems, fabric managers) to send logs to VictoriaLogs for centralized log collection and analysis.

**Content Requirements:**
- Prerequisites:
  - VictoriaLogs cluster deployed (see Topic 2)
  - VLAgent endpoint information recorded
  - TLS CA certificate for VictoriaLogs
  - Network connectivity from log sources to Service Kubernetes cluster
- Key steps:
  1. Obtain VictoriaLogs ingestion endpoint and TLS CA certificate
  2. Configure syslog sources to send logs to VLAgent
     - Plaintext syslog: port 514 (TCP/UDP)
     - TLS syslog: port 6514 (TCP) with CA certificate
  3. Configure log sources that support HTTP forwarding
     - Use JSON Lines format
     - POST to vlinsert endpoint (:9481)
  4. Verify logs are queryable in VictoriaLogs
- Expected outcomes:
  - External devices sending syslog messages to VLAgent
  - Logs appearing in VictoriaLogs query interface
  - TLS handshake successful for encrypted connections
- Warnings/Notes:
  - .. note:: VLAgent provides platform-managed syslog receivers — no additional configuration needed on Omnia side
  - .. important:: Ensure `pod_external_ip_range` is reachable from external log sources
  - .. note:: DNS mapping may be required in some devices for TLS certificate validation

**Configuration Artifacts:**
- VLAgent endpoints (from deployment output):
  - Syslog plaintext: `<LoadBalancer IP>:514`
  - Syslog TLS: `<LoadBalancer IP>:6514`
  - HTTP forwarder: `https://vlinsert-victoria-logs-cluster.telemetry.svc.cluster.local:9481/insert/jsonline`
- TLS CA certificate: `victoria-tls-certs` secret

**Cross-References:**
- `deploy_victorialogs.rst` (Topic 2)
- `query_victorialogs.rst` (Topic 4)
- `index.rst` (Topic 1)

**Build Agent Instructions:**
- Create new RST file
- Section headings:
  - Prerequisites
  - Obtain Endpoint Information
  - Configure Syslog Sources
  - Configure HTTP Forwarding Sources
  - Verify Log Ingestion
- Admonitions:
  - note: VLAgent platform-managed receivers
  - important: Network reachability requirement
  - note: DNS mapping for TLS
- SME validation required: Yes — specific device configuration examples may vary
- Confidence: Medium (0.7)
- AI_REVIEW markers: 
  - .. AI_REVIEW: Device-specific syslog configuration examples may need SME verification for accuracy

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if device-specific syslog configuration examples needed from SME

---

## Topic 4: Query Logs with VictoriaLogs

| Field | Details |
|-------|---------|
| **Topic Type** | How-To |
| **Status** | New Topic |
| **Target Audience** | Infrastructure/HPC Administrator, Platform Engineer |
| **Source Traceability** | Behaviour Spec §5.8.2, Engineering Spec §3.3 |
| **RST File** | `docs/source/OmniaInstallGuide/RHEL_new/Telemetry/query_victorialogs.rst` |
| **Content Type** | Telemetry/ |

**Customer Workflow Context:**
As an HPC administrator or platform engineer, I need to query logs stored in VictoriaLogs to troubleshoot issues, analyze system behavior, and investigate events across the cluster.

**Content Requirements:**
- Prerequisites:
  - VictoriaLogs cluster deployed
  - Logs ingested from one or more sources
  - vlselect endpoint information
- Key steps:
  1. Access VictoriaLogs query interface
     - Built-in web UI (if configured)
     - HTTP API via vlselect endpoint
  2. Use LogsQL query language to search and filter logs
     - Basic query syntax examples
     - Filter by time range, severity, source
  3. Common query patterns:
     - Search for specific error messages
     - Filter by log level (error, warning, info)
     - Query logs from specific hosts or devices
     - Aggregate and analyze log data
  4. Export query results if needed
- Expected outcomes:
  - User can construct and execute LogsQL queries
  - Query results display relevant log entries
  - User can troubleshoot issues using log data
- Warnings/Notes:
  - .. note:: LogsQL is VictoriaLogs query language — syntax differs from other log query languages
  - .. note:: Query latency depends on time range and data volume
  - .. important:: TLS required for all external query access

**Configuration Artifacts:**
- vlselect endpoint: `https://vlselect-victoria-logs-cluster.telemetry.svc.cluster.local:9491`
- LogsQL query examples

**Cross-References:**
- `index.rst` (Topic 1)
- `configure_victorialogs_sources.rst` (Topic 3)
- `external_victoria.rst` (existing VictoriaMetrics query documentation)

**Build Agent Instructions:**
- Create new RST file
- Section headings:
  - Prerequisites
  - Access Query Interface
  - LogsQL Query Basics
  - Common Query Patterns
  - Export Results
- Admonitions:
  - note: LogsQL syntax
  - note: Query latency considerations
  - important: TLS requirement
- SME validation required: Yes — LogsQL syntax examples need verification
- Confidence: Medium (0.7)
- AI_REVIEW markers:
  - .. AI_REVIEW: LogsQL query syntax examples require SME verification against VictoriaLogs documentation

**Gap Analysis:**
- [x] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [ ] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if LogsQL reference documentation needs to be created as separate topic
- [ ] Flag if SME input needed for query examples

---

## Topic 5: VictoriaLogs Configuration Reference

| Field | Details |
|-------|---------|
| **Topic Type** | Reference |
| **Status** | New Topic |
| **Target Audience** | Infrastructure/HPC Administrator, Platform Engineer |
| **Source Traceability** | Behaviour Spec §5.8.2, Engineering Spec §4.1.3.1, VL_Cluster_Component_Spec §2.1, §2.2 |
| **RST File** | `docs/source/OmniaInstallGuide/RHEL_new/Telemetry/victorialogs_config.rst` |
| **Content Type** | Telemetry/ |

**Customer Workflow Context:**
As an administrator or platform engineer, I need a reference for all VictoriaLogs configuration parameters in telemetry_config.yml to correctly size and configure the log management system for my environment.

**Content Requirements:**
- Prerequisites: None (reference topic)
- Configuration parameters:
  - victoria_logs_configurations.retention_period
    - Type: Integer (hours)
    - Default: 168 (7 days)
    - Range: 24-8760 (1 day to 1 year)
    - Description: How long logs are retained before automatic deletion
  - victoria_logs_configurations.storage_size
    - Type: Kubernetes PVC size format
    - Default: 8Gi (per replica)
    - Description: Storage allocated per vlstorage replica
    - Sizing formula: (140 MB/day × retention_days × node_count) / 3 replicas
- Deployment mode:
  - Cluster mode only (no single-node mode supported)
  - Replicas: 3 vlstorage, 2 vlinsert, 2 vlselect
- Expected outcomes: Reader can configure VictoriaLogs appropriately for their environment
- Warnings/Notes:
  - .. warning:: Storage under-provisioning can lead to data loss before retention period
  - .. note:: Retention is global — applies to all log streams uniformly
  - .. note:: Deletion is asynchronous during background merge operations

**Configuration Artifacts:**
- `telemetry_config.yml` — victoria_logs_configurations section
- Storage sizing table for different cluster scales

**Cross-References:**
- `deploy_victorialogs.rst` (Topic 2)
- `index.rst` (Topic 1)

**Build Agent Instructions:**
- Create new RST file
- Section headings:
  - victoria_logs_configurations Parameters
  - Retention Period
  - Storage Size
  - Storage Sizing Guidelines
  - Deployment Mode
- Admonitions:
  - warning: Storage under-provisioning
  - note: Global retention
  - note: Asynchronous deletion
- No SME validation required
- Confidence: High (0.9)
- AI_REVIEW markers: None

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [x] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] None identified

---

## Topic 6: Troubleshooting VictoriaLogs

| Field | Details |
|-------|---------|
| **Topic Type** | Troubleshooting |
| **Status** | New Topic |
| **Target Audience** | Infrastructure/HPC Administrator |
| **Source Traceability** | Behaviour Spec §5.8.3, Engineering Spec §4.1.10 |
| **RST File** | `docs/source/OmniaInstallGuide/RHEL_new/Telemetry/troubleshoot_victorialogs.rst` |
| **Content Type** | Telemetry/ |

**Customer Workflow Context:**
As an HPC administrator, I need to troubleshoot common issues with VictoriaLogs deployment, log ingestion, and querying to maintain observability of my cluster.

**Content Requirements:**
- Prerequisites: VictoriaLogs deployed
- Common issues and solutions:
  1. VictoriaLogs components not reaching healthy state
     - Check pod status and logs
     - Verify TLS certificate configuration
     - Check resource limits
  2. Logs not appearing in VictoriaLogs
     - Verify log source configuration
     - Check network connectivity to VLAgent
     - Verify TLS handshake for encrypted sources
  3. Query endpoint not accessible
     - Verify LoadBalancer service type
     - Check MetalLB configuration
     - Verify TLS certificate SANs
  4. Storage space exhaustion
     - Check PVC utilization
     - Adjust retention period or storage size
  5. High query latency
     - Check time range in query
     - Verify vlselect pod health
- Expected outcomes: Administrator can diagnose and resolve common VictoriaLogs issues
- Warnings/Notes:
  - .. note:: VictoriaLogs cluster mode is relatively new in upstream — pin to tested release
  - .. important:: vlstorage PVCs persist after StatefulSet deletion — manual cleanup required during teardown

**Configuration Artifacts:**
- kubectl commands for checking pod status
- kubectl commands for checking PVC utilization
- Log locations for VictoriaLogs components

**Cross-References:**
- `deploy_victorialogs.rst` (Topic 2)
- `configure_victorialogs_sources.rst` (Topic 3)
- `query_victorialogs.rst` (Topic 4)
- `Telemetry.rst` (existing known issues)

**Build Agent Instructions:**
- Create new RST file
- Section headings:
  - Component Health Issues
  - Log Ingestion Issues
  - Query Access Issues
  - Storage Issues
  - Performance Issues
- Admonitions:
  - note: Upstream cluster mode maturity
  - important: PVC cleanup during teardown
- SME validation required: Yes — troubleshooting scenarios may need real-world validation
- Confidence: Medium (0.7)
- AI_REVIEW markers:
  - .. AI_REVIEW: Troubleshooting steps require SME validation against real deployment scenarios

**Gap Analysis:**
- [x] User workflows and use cases identified
- [ ] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [x] Performance characteristics covered
- [x] Integration examples provided
- [x] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if real-world troubleshooting examples needed from SME

---

## Summary

This content plan defines 6 documentation topics for VictoriaLogs Cluster Mode:

1. **Update Telemetry Index** — Add VictoriaLogs to existing telemetry documentation
2. **Deployment Guide** — How to deploy VictoriaLogs in cluster mode
3. **Log Source Configuration** — How to configure external devices to send logs
4. **Query Guide** — How to search and analyze logs using LogsQL
5. **Configuration Reference** — Reference for all configuration parameters
6. **Troubleshooting** — Common issues and resolutions

**Total Topics:** 6  
**New Topics:** 5  
**Update Existing Topics:** 1  

**Priority Order for Implementation:**
1. Topic 1 (Update Telemetry Index) — Foundation for all other topics, updates existing structure
2. Topic 2 (Deployment) — Core capability required before use
3. Topic 5 (Configuration Reference) — Supports deployment topic
4. Topic 3 (Log Source Configuration) — Core use case
5. Topic 4 (Query Guide) — Core use case
6. Topic 6 (Troubleshooting) — Support topic

**SME Validation Required:**
- Topic 3 (Log Source Configuration) — Device-specific examples
- Topic 4 (Query Guide) — LogsQL syntax verification
- Topic 6 (Troubleshooting) — Real-world scenario validation

**Confidence Assessment:** High (0.85) — Source documents provide comprehensive coverage of customer-facing behavior and technical implementation details.

**Additional Source Requirements:**
- SME input needed for device-specific syslog configuration examples
- SME input needed for LogsQL query syntax verification
- SME input needed for troubleshooting scenario validation
