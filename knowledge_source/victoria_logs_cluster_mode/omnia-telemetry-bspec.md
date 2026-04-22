# Omnia Telemetry — Behaviour Specification (BSpec)

**Document ID:** BSPEC-TELEM-2026-001
**Version:** 2.0
**Date:** 2026-03-30
**Status:** Draft — For Review
**Author:** Venkateswara Vatam

**Revision History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-03-23 | Initial draft | Venkateswara Vatam |
| 1.0 | 2026-03-23 | Complete rewrite covering full telemetry and monitoring scope | Venkateswara Vatam |
| 2.0 | 2026-03-30 | SDD-aligned rewrite — separated customer-facing behavior from internal system behavior (moved to Functional Spec FSPEC-TELEM-2026-001) | Venkateswara Vatam |

**SDD Phase:** Phase 2a — Behaviour Specification (parallel with Functional Spec)

**Companion Document:** Functional Specification FSPEC-TELEM-2026-001 (internal system behavior)

> **SDD Scope Boundary:** This document defines **customer interaction** — what operators see, configure, and observe. Internal system behavior (component topology, data routing, resource allocation, protocols) is documented in the Functional Specification.

---

## 1. References

| LOB | Type | Document Name | Description |
|-----|------|---------------|-------------|
| Global Large Enterprise | Confluence | Product Requirements Document (PRD) Omnia 2.x | Omnia PRD covering telemetry requirements |
| Dell Omnia | External Docs | Omnia v2.1.0.0-rc2 Documentation | Official release documentation |
| VictoriaMetrics | External Docs | VictoriaMetrics Cluster Mode | Upstream cluster deployment reference |
| VictoriaLogs | External Docs | VictoriaLogs Documentation | Upstream log management reference |
| NVIDIA | External Docs | NVIDIA DCGM Documentation | Data Center GPU Manager reference |

---

## 2. Glossary

| Term | Definition |
|------|-----------|
| **HPC** | High Performance Computing |
| **OIM** | Omnia Infrastructure Manager — central management host |
| **iDRAC** | Integrated Dell Remote Access Controller — out-of-band hardware management on Dell PowerEdge servers |
| **LDMS** | Lightweight Distributed Metric Service — in-band OS-level metric collection for HPC compute nodes |
| **VictoriaMetrics** | High-performance time-series database for metric storage and querying |
| **VictoriaLogs** | Centralised log management component of the VictoriaMetrics ecosystem |
| **vmagent** | VictoriaMetrics agent — metrics scraper and forwarder |
| **VLAgent** | VictoriaLogs agent — syslog receiver that forwards logs to VictoriaLogs |
| **Kafka** | Apache Kafka — distributed streaming platform used as a telemetry data bus |
| **Vector** | High-performance data pipeline tool for transforming and routing logs and metrics |
| **SFM** | Smart Fabric Manager — Dell management console for SONiC-based Ethernet switches |
| **OME** | OpenManage Enterprise — Dell server management and monitoring console |
| **UFM** | NVIDIA Unified Fabric Manager — management and monitoring platform for InfiniBand fabrics |
| **NetQ** | NVIDIA NetQ — Ethernet fabric monitoring and telemetry platform |
| **Skyway** | NVIDIA Skyway — InfiniBand-to-Ethernet gateway |
| **DCGM** | NVIDIA Data Center GPU Manager — daemon and exporter for GPU telemetry |
| **VAST** | VAST Data Platform — flash-based parallel storage cluster |
| **PowerScale** | Dell PowerScale — scale-out NAS storage platform (OneFS) |
| **PowerVault** | Dell PowerVault ME5 — SAN/DAS block storage array |
| **mTLS** | Mutual Transport Layer Security — both client and server authenticate via certificates |

---

## 3. Overview

Omnia (Latin: *all or everything*) is a deployment tool that configures Dell PowerEdge servers into clusters capable of handling HPC, AI, and data analytics workloads. The telemetry and monitoring subsystem provides automated deployment and configuration of a comprehensive observability stack.

The telemetry subsystem enables operators to:

- **Collect** hardware, OS, network, storage, and GPU metrics from all cluster components
- **Store** metrics in a highly-available time-series database (VictoriaMetrics)
- **Store** logs and events in a centralised log management system (VictoriaLogs)
- **Query** metrics and logs from a unified observability interface
- **Scale** to enterprise HPC environments (up to 2,000 nodes)
- **Operate** in air-gapped / offline environments
- **Secure** all telemetry traffic with TLS/mTLS encryption

### 3.1 Telemetry Data Sources

| Data Source | What the Operator Gets | Metrics | Logs/Events |
|-------------|----------------------|---------|-------------|
| **iDRAC** (Dell PowerEdge servers) | Hardware health: power, thermal, CPU, memory, storage, NIC, GPU, SFP | ✅ | ✅ |
| **LDMS** (Compute nodes) | OS-level performance: memory, process, network, load, Slurm workload | ✅ | — |
| **SFM** (SONiC switches) | Network fabric: interface counters, transceiver health, queue statistics | ✅ | — |
| **OME** (Server management) | Server management telemetry streamed to Kafka | ✅ | — |
| **NVIDIA DCGM** (GPUs) | GPU utilisation, temperature, power, memory, errors, NVLink bandwidth | ✅ | — |
| **NVIDIA UFM** (InfiniBand) | Per-port traffic, link health, congestion indicators, topology changes | ✅ | ✅ |
| **NVIDIA NetQ** (Ethernet) | Interface health, DOM optics, resource utilisation, fans, PSUs, temperature | ✅ | ✅ |
| **NVIDIA Skyway** (IB-to-Eth) | Port statistics, system health, link events across gateway fabric | ✅ | ✅ |
| **PowerVault ME5** (Block storage) | IOPS, throughput, latency, capacity, component health | ✅ | ✅ |
| **PowerScale** (NAS storage) | IOPS, throughput, latency, capacity, node/cluster health | ✅ | ✅ |
| **VAST** (Parallel storage) | Performance, capacity, alarms, audit metrics, syslog events | ✅ | ✅ |

---

## 4. Feature Descriptions

### 4.1 Features Covered

| Section | Feature | Domain |
|---------|---------|--------|
| §5.1 | VictoriaMetrics — Metrics Database | Metrics Infrastructure |
| §5.2 | vmagent — Metrics Collection | Metrics Infrastructure |
| §5.3 | Apache Kafka — Telemetry Data Bus | Data Transport |
| §5.4 | iDRAC Hardware Telemetry | Hardware Monitoring |
| §5.5 | LDMS In-Band Metric Collection | Compute Monitoring |
| §5.6 | SFM Telemetry Integration | Network Monitoring |
| §5.7 | OME Telemetry Integration | Server Management |
| §5.8 | VictoriaLogs — Log Database | Log Infrastructure |
| §5.9 | Kafka → VictoriaMetrics Ingestion via Vector | Data Pipeline |
| §5.10 | NVIDIA DCGM GPU Metrics | Compute Monitoring |
| §5.11 | NVIDIA UFM InfiniBand Telemetry | Network Monitoring |
| §5.12 | NVIDIA NetQ Ethernet Telemetry | Network Monitoring |
| §5.13 | NVIDIA Skyway IB-to-Ethernet Telemetry | Network Monitoring |
| §5.14 | PowerVault ME5 Storage Telemetry | Storage Monitoring |
| §5.15 | PowerScale Storage Telemetry | Storage Monitoring |
| §5.16 | VAST Storage Telemetry | Storage Monitoring |
| §5.17 | One-Shot Log Extraction for Debugging | Operational Tooling |

---

## 5. Behavioural Descriptions

### 5.1 VictoriaMetrics — Metrics Database

#### 5.1.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia provides a highly-available time-series database for telemetry metrics, deployed on the Service Kubernetes cluster. The database supports both cluster and single-node deployment modes, with cluster mode recommended for production environments. |

#### 5.1.2 Operator Interaction

The operator configures telemetry via `telemetry_config.yml`. After running the telemetry deployment playbook:

- **Cluster mode** (default, recommended for production): The operator receives two externally-accessible endpoints — one for metric ingestion and one for metric querying (including a built-in web UI).
- **Single-node mode** (for dev/test environments with <10 nodes): A single endpoint serves both ingestion and querying.

All endpoints are TLS-secured. External clients (SFM, OME) can connect using the provided CA certificate. Metrics persist across restarts and are automatically purged after the configured retention period (default: 7 days).

The operator can selectively remove VictoriaMetrics without affecting other telemetry services (Kafka, VictoriaLogs).

#### 5.1.3 Acceptance Criteria

- All database components reach healthy state after telemetry deployment
- Ingestion and query endpoints obtain externally-accessible IPs reachable from outside the cluster
- TLS connectivity is validated automatically
- Metrics persist across component restarts
- Data older than the configured retention period is automatically purged
- Re-running the deployment playbook produces no unintended changes (idempotent)

#### 5.1.4 Feature Constraints

- Cluster mode requires at least 3 Service Kubernetes worker nodes
- `pod_external_ip_range` must be configured in `omnia_config.yml` and reachable from external telemetry sources (SFM, OME)
- Storage sizing must account for metric volume and retention period

#### 5.1.5 Performance

- Cluster mode provides approximately 4× ingestion throughput and 2× query speed compared to single-node mode
- Total cluster memory footprint: approximately 10 Gi

#### 5.1.6 Assets / Resources at Risk

Loss of a storage volume results in partial metric data loss. Mitigation: replicas spread across different worker nodes, regular backup of critical metrics.

---

### 5.2 vmagent — Metrics Collection

#### 5.2.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia deploys a Prometheus-compatible metrics scraper that automatically discovers telemetry endpoints within the Kubernetes cluster and forwards collected metrics to VictoriaMetrics. |

#### 5.2.2 Operator Interaction

The metrics collection agent is deployed automatically as part of telemetry setup. The operator does not interact with vmagent directly — it automatically discovers and scrapes all telemetry endpoints.

As new telemetry sources are enabled (UFM, NetQ, PowerScale, VAST), the agent automatically includes them in its collection cycle.

#### 5.2.3 Acceptance Criteria

- Agent discovers new telemetry endpoints within 30 seconds of them becoming available
- Scraped metrics are queryable in VictoriaMetrics within 20 seconds (2 scrape intervals)
- All scraped metrics carry identifying labels for source tracking

#### 5.2.4 Feature Constraints

- Currently collects within the telemetry namespace only; external endpoint scraping (UFM, NetQ, PowerScale, VAST) requires additional configuration

#### 5.2.5 Performance

Lightweight, minimal overhead. Default scrape interval: 10 seconds.

#### 5.2.6 Assets / Resources at Risk

N/A

---

### 5.3 Apache Kafka — Telemetry Data Bus

#### 5.3.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia deploys a reliable, TLS-secured message streaming bus for telemetry data, enabling multiple independent consumers to access telemetry streams without impacting each other. |

#### 5.3.2 Operator Interaction

Kafka is deployed automatically as part of telemetry setup. The operator interacts with Kafka in two scenarios:

1. **OME integration**: The operator runs a connection details playbook to obtain the external Kafka endpoint and mTLS certificates, then configures OME to publish telemetry to Kafka.
2. **Custom consumers**: External systems can consume telemetry data via the HTTP REST bridge or direct Kafka connections using mTLS.

All Kafka traffic is TLS-encrypted. No plaintext connections are permitted.

#### 5.3.3 Acceptance Criteria

- All Kafka components reach healthy state after deployment
- Telemetry topics are auto-created based on enabled telemetry features
- TLS/mTLS connectivity is validated automatically
- External endpoint accepts mTLS connections from authorised clients
- HTTP REST bridge provides functional access to topics

#### 5.3.4 Feature Constraints

- Strimzi operator must be deployed before Kafka components
- Default data retention: 7 days

#### 5.3.5 Performance

3-broker cluster provides adequate throughput for clusters up to 2,000+ nodes. Default retention: 7 days.

#### 5.3.6 Assets / Resources at Risk

Total storage: 48 Gi (default). Must be sized to accommodate retention period and message volume.

---

### 5.4 iDRAC Hardware Telemetry

#### 5.4.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia provides and configures iDRAC collector to push iDRAC metrics to VictoriaMetrics and/or Kafka. Telemetry data includes power, thermal, CPU, memory, storage SMART, NIC statistics, GPU metrics, and SFP transceiver metrics. |

#### 5.4.2 Operator Interaction

The operator provides a list of BMC (iDRAC) IP addresses in the inventory file. After deployment:

- The operator chooses the collection destination: **VictoriaMetrics only**, **Kafka only**, or **both** (recommended for dual-write).
- All 37 supported telemetry reports are automatically enabled on target servers (covering CPU, memory, storage, NIC, power, thermal, GPU, and OME metrics). Supports iDRAC 9 and iDRAC 10.
- A telemetry status report is generated listing all configured iDRAC endpoints and their status.

#### 5.4.3 Acceptance Criteria

- All iDRAC telemetry components reach healthy state
- All 37 iDRAC telemetry reports are enabled on target servers
- When dual-write is enabled, metrics are queryable in VictoriaMetrics AND consumable from the Kafka topic
- Credential data persists across restarts
- Telemetry report is generated listing all configured iDRAC endpoints and their status

#### 5.4.4 Feature Constraints

- Redfish must be enabled on all target iDRAC interfaces
- iDRAC firmware must be updated to the latest version
- Datacenter license is required on the target servers
- All BMC IPs must be reachable from the Service Kubernetes cluster

#### 5.4.5 Performance

Service node worker load should not exceed 40% when iDRAC collector is configured at maximum collection frequency.

#### 5.4.6 Assets / Resources at Risk

Loss of credential storage requires re-initialisation of iDRAC telemetry configuration.

---

### 5.5 LDMS In-Band Metric Collection

#### 5.5.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Build LDMSd producers for RHEL 10 and deploy on Slurm cluster nodes (login, login/compiler, controller & workers). Build and configure LDMS aggregator framework and deploy on Service Node K8s workers. |

#### 5.5.2 Operator Interaction

The operator configures LDMS via `telemetry_config.yml`, selecting which sampler plugins to enable. LDMS is automatically deployed to compute nodes during provisioning.

Available sampler plugins: `meminfo` (memory), `procstat2` (processes), `vmstat` (virtual memory), `loadavg` (system load), `procnetdev2` (network interfaces), `slurm_sampler` (HPC workload monitoring).

When compute nodes are added or removed from the cluster, the aggregator automatically picks up the new topology.

#### 5.5.3 Acceptance Criteria

- On Slurm controller, worker, and login nodes, LDMS producer is installed and captures local host metrics
- Aggregator framework is deployed on Service K8s workers
- LDMS data is pushed to the Kafka message bus
- Aggregator automatically adapts when cluster node topology changes

#### 5.5.4 Feature Constraints

- This feature relies on NERSC codebase availability for LDMS framework components
- Omnia builds and configures the LDMS framework but does not address functional defects in LDMS itself

#### 5.5.5 Performance

Load on each K8s worker node should not exceed 40% when all LDMS producers are publishing at maximum frequency.

#### 5.5.6 Assets / Resources at Risk

N/A

---

### 5.6 SFM Telemetry Integration

#### 5.6.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia enables Smart Fabric Manager (SFM) to securely stream SONiC switch telemetry metrics to VictoriaMetrics, providing visibility into network fabric health, interface counters, transceiver health, and queue statistics. |

#### 5.6.2 Operator Interaction

The operator runs the connection details playbook (`external_victoria_connect_details.yml`) to obtain VictoriaMetrics endpoint IPs and the TLS CA certificate. The operator then configures the SFM UI to enable Prometheus remote write with the extracted URL and uploads the CA certificate.

A DNS mapping entry is required inside SFM for TLS certificate validation — this entry is ephemeral and must be re-applied if the SFM monitoring component restarts.

Key metrics available to the operator: transceiver health (DOM temperature), per-queue traffic and congestion, throughput, and per-interface counters (in/out octets and errors).

#### 5.6.3 Acceptance Criteria

- Connection details playbook produces valid endpoints and CA certificate
- SFM switch metrics (interface counters, transceiver DOM, queue statistics) are queryable in VictoriaMetrics after configuration
- TLS handshake succeeds between SFM and VictoriaMetrics

#### 5.6.4 Feature Constraints

- `pod_external_ip_range` must be configured and reachable from the SFM network
- SSH must be enabled on the SFM virtual machine
- DNS mapping must be re-applied if the SFM monitoring component restarts

#### 5.6.5 Performance

Metrics forwarded every 15–30 seconds (configurable). End-to-end latency approximately 15–35 seconds.

#### 5.6.6 Assets / Resources at Risk

N/A

---

### 5.7 OME Telemetry Integration

#### 5.7.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia enables OpenManage Enterprise to securely stream server management telemetry to the Omnia Kafka bus using mutual TLS, providing integration with the broader telemetry pipeline. |

#### 5.7.2 Operator Interaction

The operator runs the connection details playbook (`external_kafka_connect_details.yml`) to obtain the Kafka external endpoint and mTLS certificates. The operator generates a `.pfx` client certificate and configures the OME UI to enable Kafka connectivity with SSL authentication, uploading the certificates.

The OME Kafka integration wizard allows the operator to select specific metrics to stream and device groups to collect from. A green checkmark confirms successful connectivity.

#### 5.7.3 Acceptance Criteria

- Connection details playbook produces valid Kafka endpoint, CA certificate, and client certificates
- OME connectivity status shows "Connected since" with green checkmark in the OME UI
- OME telemetry messages are consumable from the Kafka topic

#### 5.7.4 Feature Constraints

- `pod_external_ip_range` must be configured and reachable from the OME appliance network
- If OME is on a different system than the OIM host, certificates must be manually copied

#### 5.7.5 Performance

Streaming frequency and metric selection are configurable within the OME UI.

#### 5.7.6 Assets / Resources at Risk

N/A

---

### 5.8 VictoriaLogs — Log Database

#### 5.8.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia deploys a centralised log management system alongside VictoriaMetrics, enabling operators to ingest, store, and query infrastructure logs (syslog from network devices, iDRAC events, system audit trails) from a single observability interface. |

#### 5.8.2 Operator Interaction

VictoriaLogs is deployed alongside VictoriaMetrics using the same deployment modes (cluster or single-node). The operator does not need to configure separate retention or storage settings — existing VictoriaMetrics settings govern both metrics and logs.

Two log ingestion paths are available simultaneously:

- **Real-time syslog**: Network and storage devices (UFM, SFM, Skyway, PowerScale, VAST) send syslog messages that are ingested in real time.
- **Kafka-buffered events**: iDRAC events and control plane logs flow through Kafka for buffered, reliable delivery.

All external access requires TLS/mTLS. VictoriaLogs can be removed independently without affecting VictoriaMetrics or Kafka.

#### 5.8.3 Acceptance Criteria

- Log database components deploy and reach healthy state within 5 minutes
- A test log submitted to the ingestion endpoint is queryable within 10 seconds
- Syslog messages are retrievable with preserved severity, timestamp, and source
- TLS is enforced on all external endpoints; plaintext connections are rejected
- Logs persist across component restarts
- Retention policy automatically deletes logs older than the configured period
- Both ingestion paths (syslog and Kafka-sourced) operate simultaneously
- Air-gapped deployment succeeds using offline container image repository
- No new configuration knobs for storage/retention are added (per Cap 23732)

#### 5.8.4 Feature Constraints

- Log agent deployment on compute nodes is out of scope
- Grafana dashboard provisioning for logs is out of scope
- Log-based alerting rules are out of scope
- Multi-tenant log isolation is out of scope

#### 5.8.5 Performance

Estimated storage: ~70 GB for 7-day retention at 500 nodes; ~350 GB at 2,000 nodes.

#### 5.8.6 Assets / Resources at Risk

VictoriaLogs cluster mode is relatively new in the upstream project. Mitigation: pin to a tested release and perform soak testing at target scale before production deployment.

---

### 5.9 Kafka → VictoriaMetrics Ingestion via Vector

#### 5.9.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Telemetry data from LDMS, iDRAC, and OME published to Kafka topics is automatically ingested into VictoriaMetrics for long-term time-series storage and querying, using Vector as the transformation and routing layer. |

#### 5.9.2 Operator Interaction

Vector operates transparently — the operator does not interact with it directly. It automatically:

- Consumes telemetry data from Kafka topics
- Separates metrics from logs/events
- Routes metrics to VictoriaMetrics and logs/events to VictoriaLogs
- Dynamically discovers new Kafka topics and begins consuming within 60 seconds of topic creation

New telemetry subsystems that publish to Kafka are automatically picked up without operator intervention.

#### 5.9.3 Acceptance Criteria

- Data from LDMS, OME, and iDRAC Kafka topics is stored in VictoriaMetrics
- New topics are discovered and consumed within 60 seconds of creation
- Ingestion success rate ≥99.9% over 24 hours
- End-to-end latency (Kafka to queryable in VictoriaMetrics) ≤30 seconds at p99
- Pipeline uptime ≥99.5%

#### 5.9.4 Feature Constraints

- Topic naming convention must be enforced by producers
- Schema changes in source data may require pipeline transform updates

#### 5.9.5 Performance

New subsystem onboardable in ≤4 hours. Pipeline designed for continuous operation with minimal operator intervention.

#### 5.9.6 Assets / Resources at Risk

LDMS schema changes may break pipeline transforms (HIGH risk). Mitigation: version-pinned schema definitions and automated transform testing.

---

### 5.10 NVIDIA DCGM GPU Metrics

#### 5.10.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia deploys NVIDIA DCGM and DCGM Exporter on all NVIDIA-accelerated compute nodes, integrating GPU telemetry into the existing LDMS data pipeline for real-time monitoring of GPU utilisation, temperature, power, memory, and health. |

#### 5.10.2 Operator Interaction

The operator enables or disables DCGM via an inventory-level toggle (`omnia_dcgm_enabled`). When enabled:

- DCGM is automatically installed on every compute node with NVIDIA GPUs
- Non-GPU nodes are detected and skipped — no DCGM packages are installed
- GPU metrics are integrated into the LDMS data pipeline alongside standard OS metrics
- Per-functional-group configuration supports different GPU monitoring profiles for heterogeneous node types

Key GPU metrics available to the operator: utilisation percentage, framebuffer memory (used/free), temperature, power consumption, hardware error codes (XID), NVLink bandwidth.

Supported GPU architectures: Blackwell (B100/B200/GB200), Hopper (H100/H200), Ampere (A100) on x86_64 and aarch64. Packages are served from the Omnia local repository for air-gapped environments.

#### 5.10.3 Acceptance Criteria

- DCGM Exporter exposes metrics on 100% of GPU nodes within 5 minutes of deployment
- LDMS collects all required GPU metrics (GPU_UTIL, FB_USED, FB_FREE, GPU_TEMP, POWER_USAGE, XID_ERRORS, NVLINK_BANDWIDTH_TOTAL)
- Toggle to disable and re-enable DCGM works without requiring a node reboot
- Non-GPU nodes show no DCGM packages installed after deployment

#### 5.10.4 Feature Constraints

- Blackwell GPU support in DCGM depends on NVIDIA release timeline
- aarch64 DCGM package availability must be verified early in development

#### 5.10.5 Performance

DCGM overhead: ~2% GPU utilisation, ~200 MB host RAM (daemon + exporter combined).

#### 5.10.6 Assets / Resources at Risk

Blackwell GPU and aarch64 DCGM packages may not be available at development start (HIGH risk). Mitigation: engage NVIDIA early; fallback to `nvidia-smi` scraping if DCGM packages are unavailable.

---

### 5.11 NVIDIA UFM InfiniBand Telemetry

#### 5.11.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia collects InfiniBand fabric metrics and events from NVIDIA UFM appliances, providing visibility into per-port traffic, link health, congestion indicators, and topology changes across the IB fabric. |

#### 5.11.2 Operator Interaction

The operator enables UFM telemetry collection and provides UFM appliance connection details. The system supports UFM Enterprise 6.15.x in HA configuration (active/standby pair).

Metrics collected include: per-port Tx/Rx bytes and packets, error counters, link down/recovery events, and congestion indicators. Labels preserve device/port identity, GUIDs, and node/port names.

Logs/events from UFM are collected via syslog and stored in VictoriaLogs.

Dual-destination forwarding to an external observability endpoint is planned (depends on API finalisation).

#### 5.11.3 Acceptance Criteria

- 100% of metrics exposed by the UFM Prometheus exporter appear in VictoriaMetrics within one scrape interval
- ≥95% of critical, error, and warning syslog events are ingested into VictoriaLogs within 60 seconds
- Metric batch failure rate <0.1% over 24 hours
- UFM HA failover: metrics resume from the surviving appliance within 2 scrape intervals

#### 5.11.4 Feature Constraints

- UFM exporter schema may change across UFM versions; version pinning required
- External destination API not finalised (TBD)

#### 5.11.5 Performance

End-to-end metric latency: <60 seconds. Syslog event latency: <60 seconds. Log and metric drop rate: <0.1% over 24 hours.

#### 5.11.6 Assets / Resources at Risk

Cardinality explosion (>800K series) may impact metrics database performance. Mitigation: filtering rules to drop high-churn metrics.

---

### 5.12 NVIDIA NetQ Ethernet Telemetry

#### 5.12.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia collects Ethernet fabric telemetry from NVIDIA NetQ appliances, providing visibility into interface health, DOM optics, resource utilisation, fans, PSUs, temperature, and node health. |

#### 5.12.2 Operator Interaction

The operator enables NetQ telemetry and provides appliance connection details. Up to 4 NetQ appliances are supported. Metric domains include: interface/link statistics, DOM optics (transceiver health), system resource utilisation, environmental sensors (fans, PSUs, temperatures), node health, and per-process/per-device network counters.

Rsyslog events are collected and stored in VictoriaLogs. A 4-hour buffer provides resilience during destination outages.

#### 5.12.3 Acceptance Criteria

- ≥90% of metric families queryable within 2 scrape intervals of deployment start
- ≥95% of log events ingested into VictoriaLogs within 60 seconds
- Scrape failure rate <0.1% over 24 hours
- Deployment via a single Ansible playbook in <10 minutes for 4 appliances

#### 5.12.4 Feature Constraints

- NetQ PromQL schema may vary across versions
- Kafka integration is optional (Phase 2)

#### 5.12.5 Performance

Metrics available within scrape interval + 5 seconds. Log event latency: <60 seconds.

#### 5.12.6 Assets / Resources at Risk

Cardinality may exceed agent budget at scale. Mitigation: metric filtering and relabeling.

---

### 5.13 NVIDIA Skyway IB-to-Ethernet Telemetry

#### 5.13.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia collects telemetry from NVIDIA Skyway InfiniBand-to-Ethernet gateways via SNMP and syslog, providing visibility into port statistics, system health, and link events across the gateway fabric. |

#### 5.13.2 Operator Interaction

The operator enables Skyway telemetry and provides gateway connection details and SNMPv3 credentials. Up to 32 gateways (128 ports each, 4,096 total ports) are supported. Poll interval is configurable (15–30 seconds).

Metric domains: port bytes/packets, errors, discards, CRC, link state, speed, system temperature, fan/PSU status, alarms, CPU/memory utilisation.

An optional SNMP trap feature (toggle-controlled) provides event-driven notifications. Unsupported OIDs on specific firmware versions are reported in status output without failing the collection pipeline. Port subsets can be configured to manage metric volume at scale.

#### 5.13.3 Acceptance Criteria

- ≥90% of OIDs from the prioritised list are collected and queryable
- ≥95% of critical, error, and warning syslog events ingested within 60 seconds
- Metric batch failure rate <0.1% over 24 hours
- SNMPv3 authPriv enforced with zero credential exposure in logs
- Status output lists active telemetry source, enabled domains, and any failed OIDs

#### 5.13.4 Feature Constraints

- Skyway MIB OIDs may differ across firmware versions; an OID inventory per firmware version is required

#### 5.13.5 Performance

Metric end-to-end latency: poll interval + 10 seconds. Syslog event latency: <60 seconds.

#### 5.13.6 Assets / Resources at Risk

SNMP poll latency may exceed the poll interval at scale (32 gateways, 4,096 ports). Mitigation: parallel polling and configurable port subset filtering.

---

### 5.14 PowerVault ME5 Storage Telemetry

#### 5.14.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia collects PowerVault ME5 performance, capacity, and health metrics along with event logs, enabling proactive identification of storage bottlenecks and hardware issues. |

#### 5.14.2 Operator Interaction

The operator enables PowerVault telemetry and provides array connection details. Metrics are collected via Redfish API (preferred) with CLI fallback. Up to 16 arrays are supported.

Metrics available: read/write IOPS, throughput, latency (average and max), queue depth, cache utilisation, destage statistics, capacity (free/used per pool and volume), and component health (controllers, disks, PSUs, fans, temperatures).

Event logs cover Critical, Error, Warning, Informational, and Resolved severity levels.

Independent feature toggles allow the operator to enable/disable metrics and event log collection separately. Dual remote write delivers to both internal VictoriaMetrics and external Omni DB endpoints.

#### 5.14.3 Acceptance Criteria

- ≥90% metric coverage achieved within 14 days of development
- ≥95% of events ingested within 60 seconds
- Failed metric batch rate <0.1% per destination over 24 hours
- During a 4-hour destination outage, the surviving destination continues uninterrupted; buffered data delivered on recovery without loss
- Zero plaintext credentials in logs or configuration

#### 5.14.4 Feature Constraints

- Redfish metric coverage may be below 90%, requiring CLI fallback
- ME5 may throttle concurrent management sessions
- Lab hardware must be secured for testing

#### 5.14.5 Performance

Sampling interval: 30–60 seconds (configurable). Event latency: <60 seconds.

#### 5.14.6 Assets / Resources at Risk

No ME5 lab hardware available for testing (HIGH risk). Mitigation: secure lab allocation early in Q2.

---

### 5.15 PowerScale Storage Telemetry

#### 5.15.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia collects PowerScale IOPS, throughput, latency, capacity, and node/cluster health metrics via the gostats Prometheus exporter, alongside syslog events, providing unified storage observability. |

#### 5.15.2 Operator Interaction

The operator enables PowerScale telemetry. A single PowerScale cluster per Omnia deployment is assumed, running OneFS 9.5+ (latest two major versions supported).

When the gostats exporter runs on the service cluster, Omnia orchestrates its deployment. When gostats runs on the PowerScale side, the operator provides the endpoint URL and Omnia only scrapes.

Independent feature flags allow the operator to enable/disable PowerScale metrics and logs separately. Operational health metrics are exposed for scrape success rate and log ingest error monitoring.

#### 5.15.3 Acceptance Criteria

- vmagent scrape failure rate <2% over 24 hours
- Key metrics (IOPS, throughput, latency, capacity, node/cluster health) appear in VictoriaMetrics within one scrape interval
- Logs and events arrive in VictoriaLogs with <1-minute end-to-end latency
- No mTLS handshake failures on PowerScale metric endpoints; TLS enforced for off-cluster traffic
- Feature flags for metrics and logs operate independently

#### 5.15.4 Feature Constraints

- gostats version compatibility must be verified at development start
- TLS certificate misconfiguration is a common integration issue

#### 5.15.5 Performance

Metric latency: within one scrape interval. Log latency: <1 minute under nominal load.

#### 5.15.6 Assets / Resources at Risk

gostats version incompatibility (HIGH risk). Mitigation: pin to a tested gostats release.

---

### 5.16 VAST Storage Telemetry

#### 5.16.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia collects VAST storage cluster performance, capacity, alarm, and audit metrics alongside syslog events, providing unified storage observability for flash-based parallel storage systems at scale. |

#### 5.16.2 Operator Interaction

The operator enables VAST telemetry and provides cluster connection details. Up to 4 VAST clusters are supported (VAST Data Platform 5.2.2+ required; 5.1.x best-effort).

By default, individual metric domain endpoints are scraped rather than the combined endpoint, to manage metric volume. Operators can configure endpoint inclusion/exclusion to tailor the collection scope. For smaller clusters, the combined endpoint can be enabled for simplicity.

Syslog events (system activities, alarms, protocol audit logs) are collected and stored in VictoriaLogs.

Dual-destination forwarding delivers to both internal VictoriaMetrics and external observability endpoints.

#### 5.16.3 Acceptance Criteria

- ≥90% of prioritised metric families appear in VictoriaMetrics within 2× scrape interval
- ≥95% of WARNING and above syslog events ingested within 60 seconds
- Metric batch failure rate <0.1% over 24 hours
- During a 30-minute external destination outage, internal VictoriaMetrics ingestion continues uninterrupted; buffered data delivered within 10 minutes of recovery
- Self-metrics available within 60 seconds of collector start

#### 5.16.4 Feature Constraints

- VAST Data Platform version 5.2.2+ required (5.1.x best-effort)
- VAST API may change between versions; version pinning and regression testing required

#### 5.16.5 Performance

Scrape interval: 30–60 seconds (configurable). Syslog event latency: <60 seconds.

#### 5.16.6 Assets / Resources at Risk

- VAST exporter latency may exceed scrape interval at scale (HIGH risk). Mitigation: increase scrape timeout, use parallel scrape jobs.
- Cardinality from user-related endpoint (HIGH risk). Mitigation: exclude by default, apply filtering rules.

---

### 5.17 One-Shot Combined Log Extraction for Debugging

#### 5.17.1 Marketing User Stories

| Theme | MRD Excerpt / Feature Description |
|-------|-----------------------------------|
| AI/HPC | Omnia provides a single admin command that packages all relevant management logs into a timestamped archive for rapid troubleshooting and support engagement. |

#### 5.17.2 Operator Interaction

The operator runs a single CLI command to generate a log bundle. The command:

- Creates a compressed archive with filename pattern: `omnia-logs-<hostname>-<timestamp>.tar.gz`
- Prints the absolute path to the bundle and a SHA256 checksum
- Includes all documented Omnia/OIM log paths by default (configurable via pointers, not hardcoded)
- Allows the operator to add custom log file locations
- Supports utility flags for filesize limits and exclusion patterns (ignore temp/stale logs)
- Reports excluded items and warns about missing logs without failing

The archive includes a `metadata.json` capturing: timestamp (UTC+local), triggering user, OIM hostname/OS info, and checksum.

#### 5.17.3 Acceptance Criteria

- Running the command generates a `.tar.gz` file and prints its absolute path and SHA256 (Pass/Fail)
- `metadata.json` includes timestamp (UTC+local), triggering user, versions, and flags (Pass/Fail)
- Bundle contains logs from documented Omnia/OIM paths and system logs (Pass/Fail)
- Operator can pass exclusion patterns and max file size; excluded items are reported (Pass/Fail)

#### 5.17.4 Feature Constraints

- Requires network and container/pod connectivity to the OIM
- Software should be mostly self-contained; requires standard Linux utilities for metadata and checksum

#### 5.17.5 Performance

Target: Time to provide a complete bundle to engineering/support reduced by >50% vs manual collection.

#### 5.17.6 Assets / Resources at Risk

N/A

---

## 6. License Information

| # | Component | License |
|---|-----------|---------|
| 1 | VictoriaMetrics | Apache 2.0 |
| 2 | VictoriaLogs | Apache 2.0 |
| 3 | Apache Kafka (Strimzi) | Apache 2.0 |
| 4 | Vector | Mozilla Public License 2.0 |
| 5 | NVIDIA DCGM | NVIDIA proprietary (free for use on NVIDIA hardware) |
| 6 | LDMS (OVIS) | GPLv2 / open-source |

---

*Document Version: 2.0 | Last Updated: 2026-03-30*
*SDD Phase: 2a — Behaviour Specification*
*Companion: Functional Specification FSPEC-TELEM-2026-001 (internal system behavior)*
