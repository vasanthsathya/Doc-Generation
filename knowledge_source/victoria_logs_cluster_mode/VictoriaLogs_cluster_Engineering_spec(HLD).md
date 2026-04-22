# High Level Design (HLD) Document

| | |
|---|---|
| **Template Version** | 2.46 |
| **Current Version** | 0.7 |
| **Approved By** | |
| **Approval Date** | |

---

## VictoriaLogs Cluster Mode — Platform Logging Service

---

*This document contains information of a proprietary nature. ALL INFORMATION CONTAINED HEREIN SHALL BE KEPT IN CONFIDENCE. None of this information shall be divulged to persons other than Dell employees authorized by the nature of their duties to receive such information, or individuals or organizations authorized by Dell research and development in accordance with existing policy regarding the release of company information.*

---

## Revision History

| Version | Date | Description | Author(s) |
|---------|------|-------------|-----------|
| 0.1 | 04/01/2025 | Initial draft | Priti Parate |
| 0.5 | 04/10/2025 | Added sequence diagrams and data flow details | Priti Parate |
| 0.7 | 04/23/2025 | Updated feedback comments; aligned with business requirements — platform-decoupled design, cluster-mode-only, removed single-node references and source-specific pipeline wiring | Priti Parate |

---

## Table of Contents

- 1 [Glossary](#1-glossary)
- 2 [Introduction](#2-introduction)
  - 2.1 [Scope](#21-scope)
  - 2.2 [References](#22-references)
- 3 [Solution Architecture](#3-solution-architecture)
  - 3.1 [Architecture Constraints and Assumptions](#31-architecture-constraints-and-assumptions)
    - 3.1.1 [Constraints](#311-constraints)
    - 3.1.2 [Assumptions](#312-assumptions)
  - 3.2 [Architecture Control Flow](#32-architecture-control-flow)
  - 3.3 [Architecture Data Flow Diagram](#33-architecture-data-flow-diagram)
  - 3.4 [Actor / Action Matrix](#34-actor--action-matrix)
  - 3.5 [Architecture Threat Model](#35-architecture-threat-model)
    - 3.5.1 [Threat Model](#351-threat-model)
- 4 [High Level Design of Architectural Components](#4-high-level-design-of-architectural-components)
  - 4.1 [Design for VictoriaLogs Cluster Mode Platform Service](#41-design-for-victorialogs-cluster-mode-platform-service)
    - 4.1.1 [Component Description / Purpose](#411-component-description--purpose)
    - 4.1.2 [Component Design Constraints and Assumptions](#412-component-design-constraints-and-assumptions)
    - 4.1.3 [Component Design](#413-component-design)
    - 4.1.4 [Security Considerations and Test Plan](#414-security-considerations-and-test-plan)
    - 4.1.5 [Resource Utilization and Scalability](#415-resource-utilization-and-scalability)
    - 4.1.6 [Open Source](#416-open-source)
    - 4.1.7 [Component Test](#417-component-test)
    - 4.1.8 [Module API Sharing within Dell ISG Organizations](#418-module-api-sharing-within-dell-isg-organizations)
    - 4.1.9 [New API Conformance within Dell ISG Organizations](#419-new-api-conformance-within-dell-isg-organizations)
    - 4.1.10 [Unresolved Issues](#4110-unresolved-issues)

---

## 1 Glossary

| Term | Meaning |
|------|---------|
| VictoriaLogs | High-performance log storage and querying engine from VictoriaMetrics, deployed as a mandatory Omnia platform service |
| vlstorage | VictoriaLogs cluster component — persistent log storage node that stores raw log data and returns query results |
| vlinsert | VictoriaLogs cluster component — log ingestion gateway that accepts incoming logs and shards across vlstorage nodes |
| vlselect | VictoriaLogs cluster component — log query gateway that fans out queries to vlstorage nodes and merges results |
| VLAgent | VictoriaMetrics log collector (vlagent) — platform-managed log forwarding agent, part of the Omnia logging platform |
| LogsQL | VictoriaLogs query language for searching, filtering, and aggregating log data |
| JSON Lines | Newline-delimited JSON format for structured log ingestion (also known as JSONL or NDJSON) |
| RFC 5424 | The Syslog Protocol — standard format for system log messages |
| ES Bulk API | Elasticsearch-compatible bulk ingestion API supported by VictoriaLogs for log import |
| mTLS | Mutual TLS — both client and server present certificates for authentication |
| TLS | Transport Layer Security — encryption protocol for in-cluster and external communication |
| PVC | Persistent Volume Claim — Kubernetes persistent storage abstraction |
| StatefulSet | Kubernetes workload resource for stateful applications with stable network identities and persistent storage |
| Kustomize | Kubernetes configuration customization tool for declarative manifest management |
| MetalLB | Bare-metal Kubernetes load balancer implementation |
| RBAC | Role-Based Access Control |
| OIM | Omnia Infrastructure Manager — control plane for Omnia deployment |
| Pulp | Repository mirroring tool for air-gapped (offline) environments |
| Idempotent | Property where repeated execution produces the same result as a single execution |

---

## 2 Introduction

This document describes the high level design for deploying **VictoriaLogs (cluster mode) and VLAgent as a mandatory Omnia platform service**. This establishes a centrally managed, secure, scalable, and durable logging foundation within the Omnia Telemetry subsystem that current and future telemetry capabilities can rely on without reimplementing infrastructure.

### Business Value Statement

As a platform owner and site administrator, I want a centrally managed, cluster-mode logging platform with a standard ingestion frontend so that current and future telemetry capabilities can rely on a secure, scalable, and durable logging foundation without reimplementing infrastructure.

### Problem Statement

Omnia currently provides a mature metrics observability stack (VictoriaMetrics) but lacks an equivalent platform-managed logging backend. Without a standardized log storage and ingestion foundation, telemetry capabilities must either defer logging support or deploy bespoke infrastructure, increasing operational complexity and long-term maintenance risk.

This epic establishes VictoriaLogs (cluster mode only) and VLAgent as a mandatory Omnia platform service, **decoupled from any specific log sources or ingestion pipelines**, enabling consistent reuse by future capabilities.

### Design Principles

1. **Co-deployed with VictoriaMetrics**: VictoriaLogs and VLAgent are deployed whenever `"victoria"` is present in `telemetry_collection_type`. No separate feature flag is required — VictoriaMetrics and VictoriaLogs share the same deployment gate.
2. **Source-decoupled**: The platform provides ingestion endpoints and query endpoints. How and what gets routed to those endpoints is the responsibility of downstream capabilities (separate epics).
3. **Role-separated**: Storage (vlstorage), ingestion (vlinsert), and query (vlselect) are independent components, architecturally aligned with VictoriaMetrics (vmstorage, vminsert, vmselect).
4. **Cluster mode only**: Single-node VictoriaLogs is not supported. The platform always deploys in cluster mode for production-grade durability and scalability.

### 2.1 Scope

**In Scope:**

1. Deployment of VictoriaLogs in cluster mode only
2. Deployment and lifecycle management of VLAgent as part of the platform
3. Role-separated architecture (storage, ingestion, query) aligned with VictoriaMetrics
4. Persistent log storage with configurable retention
5. TLS-secured in-cluster traffic and mTLS (where supported) for external access
6. External exposure of ingestion and query endpoints
7. Integration with Omnia deploy / redeploy / teardown workflows
8. Idempotent deployment behavior
9. Endpoint discovery aligned with existing VictoriaMetrics output
10. Support for air-gapped (offline) installations
11. Coexistence with VictoriaMetrics and Kafka in the telemetry namespace

**Out of Scope:**

1. Single-node VictoriaLogs deployment
2. Definition or enablement of log sources
3. Kafka, syslog, or source-specific pipeline wiring
4. Log parsing, enrichment, or routing rules
5. Log-based alerting
6. Dashboard or visualization provisioning
7. Multi-tenant isolation
8. Cross-cluster or cross-site replication
9. Enterprise-only VictoriaLogs features

### 2.2 References

The following documents are included for reference.

| LOB | Type | Document Name | Document Description |
|-----|------|---------------|----------------------|
| Dell Omnia | Internal | VictoriaLogs Cluster Mode Functional Specification (Section 5.8) | Companion functional spec defining requirements and acceptance criteria |
| Dell Omnia | Internal | PowerScale Telemetry Engineering Specification | Reference eng spec for architectural alignment with VictoriaMetrics |
| Dell Omnia | Confluence | Omnia Telemetry Behaviour Specification (CY26 Q2) | Companion BSpec defining customer-facing behavior |
| Dell Omnia | Confluence | Product Requirements Document (PRD) Omnia 2.x | PDM requirements covering telemetry |
| Dell Omnia | External Docs | Omnia v2.1.0.0 Documentation | Current release documentation |
| VictoriaMetrics | External Docs | VictoriaLogs Cluster Mode Documentation | Upstream cluster deployment reference for VictoriaLogs |
| VictoriaMetrics | External Docs | VictoriaLogs Data Ingestion API | VictoriaLogs insert API reference (JSON Lines, syslog, ES bulk) |
| VictoriaMetrics | External Docs | VictoriaLogs LogsQL Reference | VictoriaLogs query language reference |
| VictoriaMetrics | External Docs | VLAgent Documentation | Log collector and forwarder reference |

---

## 3 Solution Architecture

### 3.1 Architecture Constraints and Assumptions

#### 3.1.1 Constraints

- Omnia is always deployed in an **air-gapped (offline) environment**. All container images for VictoriaLogs cluster deployment must be pre-staged in the local Pulp repository via `local_repo.yml` before deployment. No Internet connectivity is available at deployment time.
- OIM should have a minimum of 2 NICs in active state. One for public connectivity and the other for connection to the cluster.
- VictoriaLogs is deployed in **cluster mode only**. Single-node deployment is not supported.
- VictoriaLogs cluster mode requires a minimum of 2 worker nodes in the Service Kubernetes cluster to satisfy pod anti-affinity constraints for vlstorage replicas (3 replicas distributed across available nodes).
- TLS certificates are shared with VictoriaMetrics — VictoriaMetrics must be deployed first (or concurrently) to generate the `victoria-tls-certs` secret.
- vlinsert and vlselect require LoadBalancer service type (MetalLB) for external access.
- vlstorage PVCs are not automatically deleted on StatefulSet removal; manual cleanup is required during teardown.
- VictoriaLogs and VLAgent are **platform infrastructure** — they do not define, enable, or configure any specific log sources or ingestion pipelines.

#### 3.1.2 Assumptions

- The Service Kubernetes cluster is already deployed and accessible via `kubectl`.
- The `telemetry` namespace already exists (created during VictoriaMetrics or iDRAC telemetry deployment).
- The `victoria-tls-certs` Kubernetes secret already exists with TLS certificates that include VictoriaLogs SANs (vlinsert, vlselect, vlstorage).
- MetalLB is optionally deployed for LoadBalancer service type support.
- Storage provisioner is available in the cluster for dynamic PVC provisioning.
- Downstream capabilities (future epics) are responsible for wiring specific log sources to the VictoriaLogs ingestion endpoints.

### 3.2 Architecture Control Flow

VictoriaLogs cluster is deployed alongside VictoriaMetrics during the discovery playbook, gated by the same `telemetry_collection_type` flag. When `"victoria"` is present in the collection type, both VictoriaMetrics and VictoriaLogs are deployed. No separate flag is needed.

Both VictoriaMetrics and VictoriaLogs are managed by the **VictoriaMetrics operator** (installed via Helm chart). The operator watches for `VMCluster`, `VLCluster`, `VMAgent`, and `VLAgent` Custom Resources (CRs) and reconciles the underlying Kubernetes workloads automatically.

**Deployment control flow:**
```
Discovery playbook execution (telemetry block)
    |
    ↓
Parse telemetry_collection_type (e.g., "victoria,kafka")
    ├── 'victoria' in types → Deploy VictoriaMetrics + VictoriaLogs (via operator CRs)
    └── 'kafka' in types    → Deploy Kafka
    |
    ↓
L2 Python validation (common_validation.py)
    ├── Validate victoria_logs_configurations.retention_period as valid duration
    ├── Validate victoria_logs_configurations.storage_size as valid PVC format
    ├── Verify image versions in service_k8s.json
    └── Validate TLS configuration
    |
    ↓
Ansible validation (validate_telemetry_config.yml)
    ├── Set VictoriaLogs cluster facts
    └── Display cluster topology summary
    |
    ↓
telemetry.sh.j2 — Deployment execution
    1. kubectl apply -f telemetry_namespace_creation.yaml
    2. helm install strimzi-cluster-operator <tarball>         # if kafka in types
    3. helm install victoria-metrics-operator <tarball>         # if victoria in types
       # Operator watches for VMCluster, VLCluster, VMAgent, VLAgent CRs
    4. kubectl apply -k deployments/
       # Applies operator CRs — operator reconciles underlying workloads:
       #   VMCluster CR → vmstorage StatefulSet, vminsert Deployment, vmselect Deployment
       #   VLCluster CR → vlstorage StatefulSet, vlinsert Deployment, vlselect Deployment
       #   VMAgent CR  → vmagent Deployment
       #   VLAgent CR  → VLAgent Deployment
    |
    ↓
Operator reconciles CRs → creates/updates workloads automatically
    |
    ↓
Emit endpoint discovery output (aligned with VictoriaMetrics)
    ├── vlinsert_endpoint: https://vlinsert.telemetry.svc.cluster.local:9481
    ├── vlselect_endpoint: https://vlselect.telemetry.svc.cluster.local:9491
    └── vlagent_endpoint:  <LoadBalancer IP>:514
```

**Redeploy behavior**: Re-running the discovery playbook re-applies CRs via `kubectl apply -k`. The operator detects CR spec changes and performs rolling updates automatically. Unchanged CRs produce no workload changes. This is idempotent.

**Teardown behavior**: Teardown deletes the `VLCluster` and `VLAgent` CRs. The operator removes the underlying workloads (Deployments, StatefulSets, Services). vlstorage PVCs require separate manual cleanup. VictoriaMetrics and Kafka are unaffected.

**Deployment gate vs cleanup independence**: VictoriaMetrics and VictoriaLogs share the same deployment gate (`'victoria' in telemetry_collection_type`). They are always deployed together. However, cleanup is independent — `./cleanup_telemetry.sh victorialogs` removes only VictoriaLogs while leaving VictoriaMetrics untouched. This allows selective removal of the logs stack without disrupting metrics collection. To remove both, use `./cleanup_telemetry.sh victoriametrics victorialogs`.

### 3.3 Architecture Data Flow Diagram

The platform provides ingestion and query endpoints. Downstream capabilities wire their log sources to these endpoints.

```
+======================== TELEMETRY NAMESPACE (Kubernetes) ========================+
|                                                                                   |
|  PLATFORM-PROVIDED INFRASTRUCTURE (this epic)                                     |
|  ============================================                                     |
|                                                                                   |
|                   +-----------+                                                   |
|                   | VLAgent   |   Platform-managed log forwarding agent            |
|   [Any future     | (platform |   Provides standard syslog receiver (:514 plaintext)|
|    syslog source  |  instance)|   and TLS syslog receiver (:6514 RFC 5425)         |
|    wired by       +-----------+   and HTTP forwarder to vlinsert                  |
|    downstream         |                                                           |
|    capability]        | JSON Lines HTTP POST (TLS :9481)                          |
|                       |                                                           |
|                       ↓                                                           |
|  [Any future     +----------+      consistent hash      +------------+            |
|   ingestion      | vlinsert |      sharding             | vlstorage  |            |
|   client can     | (2 repl) |  -----------------------> | (2 repl)   |            |
|   POST to        | LB:9481  |                           | StatefulSet|            |
|   vlinsert       +----------+                           | 8Gi PVC ea |            |
|   directly]           ↑                                 +------+-----+            |
|                       |                                        |                  |
|        Ingestion Endpoints:                                    |                  |
|        - /insert/jsonline                                      |                  |
|        - /insert/syslog                                        |                  |
|        - /insert/elasticsearch/_bulk                           |                  |
|                                                                |                  |
|                                                                ↓                  |
|  [Any future     +----------+      fan-out query        +------------+            |
|   query client]  | vlselect |  -----------------------> | vlstorage  |            |
|                  | (2 repl) |  <----------------------- | (all pods) |            |
|                  | LB:9491  |      merge results         +------------+            |
|                  +----------+                                                     |
|                       ↑                                                           |
|        Query Endpoints:                                                           |
|        - /select/logsql/query                                                     |
|        - /select/logsql/hits                                                      |
|        - /select/logsql/stats_query                                               |
|        - /select/logsql/tail                                                      |
|                                                                                   |
+===================================================================================+

Note: Log sources, Kafka consumers, syslog device wiring, parsing rules, and
routing pipelines are OUT OF SCOPE for this platform service. They are the
responsibility of downstream capabilities (separate epics).
```

### 3.4 Actor / Action Matrix

| Actions | Administrator | Non-Administrator | Viewer |
|---------|--------------|-------------------|--------|
| Configure `telemetry_config.yml` (retention, storage size) | Allowed | Not Allowed | Not Allowed |
| Run discovery playbook to deploy/redeploy VictoriaLogs cluster | Allowed | Not Allowed | Not Allowed |
| Run teardown to remove VictoriaLogs cluster | Allowed | Not Allowed | Not Allowed |
| Query logs via vlselect LogsQL endpoint | Allowed | Allowed | Allowed |
| Ingest logs via vlinsert endpoint | Allowed | Allowed (programmatic) | Not Allowed |
| View VictoriaLogs cluster health status | Allowed | Allowed | Allowed |
| Manage TLS certificates | Allowed | Not Allowed | Not Allowed |

### 3.5 Architecture Threat Model

#### 3.5.1 Threat Model

| Threat | Mitigation |
|--------|------------|
| Unauthorized log ingestion via vlinsert | TLS enforced on vlinsert :9481; mTLS for external access; LoadBalancer restricts network-level access |
| Unauthorized log query via vlselect | TLS enforced on vlselect :9491; mTLS for external access; RBAC controls on Kubernetes namespace |
| Man-in-the-middle on vlstorage communication | TLS enforced on all vlinsert ↔ vlstorage (:9401) and vlselect ↔ vlstorage (:9402) traffic |
| TLS certificate exposure | Certificates stored in Kubernetes `victoria-tls-certs` secret with namespace-level RBAC; 10-year self-signed CA |
| Denial of service on vlinsert | 2-replica Deployment behind LoadBalancer; resource limits prevent container resource exhaustion |
| Persistent storage data at rest | Relies on underlying storage provisioner encryption; VictoriaLogs does not provide application-level encryption at rest |
| Credential isolation during deployment | `no_log: true` on all Ansible tasks handling TLS secrets; secrets are Kubernetes-managed |

**Identified Risks (from Business Requirements):**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Storage under-provisioned | Medium | High | Conservative defaults (8 Gi per vlstorage replica, 3 replicas = 24 Gi total); storage size configurable in `telemetry_config.yml`; monitoring recommended |
| Storage replica downtime | Medium | Medium | Document maintenance procedures; StatefulSet auto-restarts failed pods; PVC preserves data; 3 replicas provide redundancy |
| Certificate SAN mismatch | High | Medium | Operational guidance; `gen_victoria_certs.sh` extended with VictoriaLogs SANs; validation during deployment |
| Namespace resource contention | Medium | Medium | Enforce resource limits on all pods (CPU and memory limits defined); pod anti-affinity distributes across nodes |

Refer Threat Modeling Report for comprehensive threat analysis.

---

## 4 High Level Design of Architectural Components

### 4.1 Design for VictoriaLogs Cluster Mode Platform Service

This section provides the design for deploying VictoriaLogs in cluster mode and VLAgent as a mandatory Omnia platform service. The design is **source-decoupled** — it provides ingestion and query endpoints that downstream capabilities can consume, without defining or wiring specific log sources.

#### 4.1.1 Component Description / Purpose

VictoriaLogs cluster mode and VLAgent are deployed as mandatory Omnia platform infrastructure, providing a centrally managed logging foundation for current and future telemetry capabilities.

**Platform components:**

| Component | Role | Analogy to VictoriaMetrics |
|-----------|------|---------------------------|
| vlstorage | Persistent log storage | vmstorage |
| vlinsert | Log ingestion gateway | vminsert |
| vlselect | Log query gateway | vmselect |
| VLAgent | Platform-managed log forwarding agent | vmagent |

**Key platform capabilities:**
- **Role-separated architecture**: Storage, ingestion, and query are independent components aligned with VictoriaMetrics
- **Standard ingestion frontend**: vlinsert exposes JSON Lines, syslog RFC 5424, and Elasticsearch bulk API endpoints that any downstream capability can use
- **Persistent, durable storage**: StatefulSet-based vlstorage with PVC-backed data and configurable retention
- **TLS security**: Shared certificate infrastructure with VictoriaMetrics; TLS enforced in-cluster, mTLS for external access
- **Independent lifecycle**: Deployed/removed independently of VictoriaMetrics and Kafka; coexists in `telemetry` namespace
- **Idempotent deployment**: Repeated deploy/redeploy produces the same result
- **Air-gapped deployment**: All images pre-staged in local Pulp repository via `service_k8s.json`

**What this platform does NOT do** (out of scope for this epic):
- Define or enable specific log sources (PowerScale syslog, iDRAC events, etc.)
- Wire Kafka topics, syslog receivers, or source-specific pipelines
- Parse, enrich, or route logs
- Provide alerting or dashboards

#### 4.1.2 Component Design Constraints and Assumptions

##### 4.1.2.1 Constraints

- VictoriaLogs is deployed in **cluster mode only**. Single-node deployment is not supported and is out of scope.
- VictoriaLogs cluster mode requires at least 2 worker nodes for pod anti-affinity distribution of vlstorage replicas (3 replicas).
- vlstorage uses `ReadWriteOnce` PVCs — each vlstorage pod must be scheduled on a node with available persistent storage.
- TLS certificates must include VictoriaLogs SANs (vlinsert, vlselect, vlstorage). The shared `gen_victoria_certs.sh.j2` must be extended before cluster deployment.
- vlinsert and vlselect require LoadBalancer service type (MetalLB) for external access.
- vlstorage PVCs persist after StatefulSet deletion and require manual cleanup during teardown.
- VLAgent is deployed as a platform component. Source-specific VLAgent configuration (syslog source wiring, relabel rules, etc.) is the responsibility of downstream capabilities.

##### 4.1.2.2 Assumptions

- The existing Ansible telemetry role infrastructure (`discovery/roles/telemetry/`) is extended with new task files and templates for VictoriaLogs cluster components.
- Image versions are managed through the existing `service_k8s.json` image registry mechanism. All images are pre-staged in the local Pulp repository for air-gapped deployment.
- Downstream capabilities will use the vlinsert endpoint for log ingestion and vlselect endpoint for log queries.

#### 4.1.3 Component Design

##### 4.1.3.1 Control Flow of Component

**Deployment configuration:**

VictoriaLogs cluster is deployed as a mandatory platform service. The user configures platform-level parameters under `victoria_logs_configurations:` in `telemetry_config.yml` (parallel to the existing `victoria_metrics_configurations:` for VictoriaMetrics):

> *Implementation details: See Component Spec (LLD)*


There is no `victorialogs_deployment_mode` toggle — cluster mode is the only mode.

**Configuration processing flow:**

1. **L2 Python Validation** (`common_validation.py`):
   - `victoria_logs_configurations.retention_period` must be a valid duration format (e.g., `7d`, `30d`, `90d`)
   - `victoria_logs_configurations.storage_size` must be a valid Kubernetes PVC size format (e.g., `8Gi`, `50Gi`)
   - Image versions for `victoriametrics/victoria-logs` and `victoriametrics/vlagent` must exist in `service_k8s.json`
   - Images must be present in local Pulp repository

2. **Ansible Validation** (`validate_telemetry_config.yml`):
   - Sets VictoriaLogs cluster facts
   - Displays cluster topology summary
   - Validates TLS certificate secret existence

3. **Deployment** (`deploy_victorialogs_cluster.yml` — idempotent):
   - Loads `telemetry_config.yml` and image versions from `service_k8s.json`
   - Generates `VLCluster` CR template (operator manages vlstorage, vlinsert, vlselect)
   - Generates `VLAgent` CR template (operator manages VLAgent)
   - Generates VLAgent ConfigMap (syslog receiver configuration)
   - Generates `kustomization.yaml` referencing operator CRs
   - Applies via `kubectl apply -k` — operator reconciles underlying workloads

4. **Endpoint Discovery Output** (aligned with VictoriaMetrics output pattern):
   - Displays vlinsert, vlselect, and VLAgent endpoints
   - Format matches existing VictoriaMetrics endpoint output for consistency

**Deployment pseudocode:**

> *Implementation details: See Component Spec (LLD)*


**Omnia workflow integration:**

| Workflow | Action | Idempotent |
|----------|--------|------------|
| `discovery_provision.yml` (deploy) | Apply `VLCluster` + `VLAgent` CRs; operator creates workloads; emit endpoint discovery | Yes |
| `discovery_provision.yml` (redeploy) | Re-apply CRs via `kubectl apply -k`; operator performs rolling update on changed specs | Yes |
| Teardown | Delete `VLCluster` + `VLAgent` CRs; operator removes workloads; manual PVC cleanup for vlstorage | Yes |

##### 4.1.3.2 Component Design Details

**Component 1 — vlstorage (StatefulSet, 3 replicas) — Operator-managed via `VLCluster` CR**

Persistent log storage nodes that store raw log data on local PVCs and respond to queries from vlselect. Created and managed by the VictoriaMetrics operator from the `VLCluster` CR spec.

| Property | Value |
|----------|-------|
| Kind | StatefulSet |
| Name | `vlstorage` |
| Replicas | 3 |
| Image | `victoriametrics/victoria-logs:v1.49.0` (from `service_k8s.json`; operator manages via `clusterVersion`) |
| Service | Headless (`vlstorage`, ClusterIP: None) |
| Port: HTTP | 9491 (health checks, admin API) |
| Port: vlinsert | 9401 (data ingestion from vlinsert) |
| Port: vlselect | 9402 (query from vlselect) |
| PVC | Configurable per replica (default 8 Gi), `ReadWriteOnce` at `/vlstorage-data` |
| Retention | Configurable (default `30d`) |
| CPU | Request: 250m, Limit: 1000m |
| Memory | Request: 1 Gi, Limit: 2 Gi |
| Anti-affinity | `preferredDuringSchedulingIgnoredDuringExecution` on `kubernetes.io/hostname` |
| Termination grace | 30s |
| TLS | `-tls -tlsCertFile=/etc/victoria/certs/server.crt -tlsKeyFile=/etc/victoria/certs/server.key` |
| Liveness probe | HTTP GET `/health` :9491 (delay 30s, period 30s, timeout 5s) |
| Readiness probe | HTTP GET `/health` :9491 (delay 5s, period 15s) |
| Init container | `cleanup-vlstorage-locks` — removes stale `flock.lock` files from ungraceful shutdowns |

Container args:
> *Implementation details: See Component Spec (LLD)*


Volume mounts:
- `vlstorage-data` at `/vlstorage-data` (from PVC volumeClaimTemplate)
- `victoria-tls-certs` at `/etc/victoria/certs` (read-only, from Secret)

---

**Component 2 — vlinsert (Deployment, 2 replicas) — Operator-managed via `VLCluster` CR**

Log ingestion gateway that accepts logs and shards across vlstorage nodes. This is the **standard ingestion frontend** for the platform. Created and managed by the operator from the `VLCluster` CR spec.

| Property | Value |
|----------|-------|
| Kind | Deployment |
| Name | `vlinsert` |
| Replicas | 2 |
| Image | `victoriametrics/victoria-logs:v1.49.0` (from `service_k8s.json`; operator manages via `clusterVersion`) |
| Service | LoadBalancer (`vlinsert`, port 9481) |
| Port: HTTP | 9481 (ingestion endpoint) |
| CPU | Request: 250m, Limit: 1000m |
| Memory | Request: 512 Mi, Limit: 1 Gi |
| Anti-affinity | `preferredDuringSchedulingIgnoredDuringExecution` on `kubernetes.io/hostname` |
| TLS | `-tls -tlsCertFile=/etc/victoria/certs/server.crt -tlsKeyFile=/etc/victoria/certs/server.key` |
| Liveness probe | HTTP GET `/health` :9481 (delay 30s, period 30s) |
| Readiness probe | HTTP GET `/health` :9481 (delay 5s, period 10s) |

**Standard ingestion endpoints (available to all downstream capabilities):**

| Endpoint | Format | Description |
|----------|--------|-------------|
| `/insert/jsonline` | JSON Lines (NDJSON) | Primary ingestion format; supports `_stream_fields`, `_msg_field`, `_time_field` query parameters |
| `/insert/syslog` | syslog RFC 5424 | Native syslog ingestion |
| `/insert/elasticsearch/_bulk` | Elasticsearch bulk API | ES-compatible bulk import |

Container args:
> *Implementation details: See Component Spec (LLD)*


---

**Component 3 — vlselect (Deployment, 2 replicas) — Operator-managed via `VLCluster` CR**

Log query gateway that fans out queries to all vlstorage nodes and merges results. Created and managed by the operator from the `VLCluster` CR spec.

| Property | Value |
|----------|-------|
| Kind | Deployment |
| Name | `vlselect` |
| Replicas | 2 |
| Image | `victoriametrics/victoria-logs:v1.49.0` (from `service_k8s.json`; operator manages via `clusterVersion`) |
| Service | LoadBalancer (`vlselect`, port 9491) |
| Port: HTTP | 9491 (query endpoint) |
| CPU | Request: 250m, Limit: 1000m |
| Memory | Request: 512 Mi, Limit: 1 Gi |
| Anti-affinity | `preferredDuringSchedulingIgnoredDuringExecution` on `kubernetes.io/hostname` |
| TLS | `-tls -tlsCertFile=/etc/victoria/certs/server.crt -tlsKeyFile=/etc/victoria/certs/server.key` |
| Liveness probe | HTTP GET `/health` :9491 (delay 30s, period 30s) |
| Readiness probe | HTTP GET `/health` :9491 (delay 5s, period 10s) |

**Standard query endpoints (available to all downstream capabilities):**

| Endpoint | Description |
|----------|-------------|
| `/select/logsql/query` | LogsQL query execution |
| `/select/logsql/hits` | Log hit count |
| `/select/logsql/stats_query` | Statistical aggregation |
| `/select/logsql/stream_ids` | Stream enumeration |
| `/select/logsql/streams` | Stream metadata |
| `/select/logsql/tail` | Live tail streaming |

Container args:
> *Implementation details: See Component Spec (LLD)*


---

**Component 4 — VLAgent (Deployment, 1 replica) — Operator-managed via `VLAgent` CR**

Platform-managed log forwarding agent deployed as part of the Omnia logging platform. Created and managed by the operator from the `VLAgent` CR. VLAgent provides a standard syslog receiver and HTTP forwarding frontend. Source-specific configuration (which devices send syslog, relabel rules, parsing) is the responsibility of downstream capabilities.

| Property | Value |
|----------|-------|
| Kind | Deployment |
| Name | `vlagent` |
| Replicas | 1 |
| Image | `victoriametrics/vlagent:<version>` (from `service_k8s.json`) |
| Service | LoadBalancer (`vlagent`, via MetalLB) |
| Port: syslog | 514 TCP+UDP (plaintext, default, configurable) |
| Port: syslog TLS | 6514 TCP (TLS-secured, RFC 5425, configurable) |
| Port: HTTP | 8429 (health checks) |
| PVC | 5 Gi at `/vlagent-data` (configurable) |
| CPU | Request: 50m, Limit: 250m |
| Memory | Request: 128 Mi, Limit: 512 Mi |
| Liveness probe | HTTP GET `/health` :8429 (delay 30s, period 30s) |
| Readiness probe | HTTP GET `/health` :8429 (delay 5s, period 10s) |

VLAgent base ConfigMap (platform configuration — source-neutral):
> *Implementation details: See Component Spec (LLD)*


**Note**: Source-specific relabel configs, external labels (e.g., `source: powerscale`), dual-write destinations, and parsing rules are NOT configured in this platform base. Downstream capabilities extend or overlay VLAgent configuration as needed.

MetalLB detection for service type selection:
> *Implementation details: See Component Spec (LLD)*


---

**TLS Certificate Extension:**

The shared certificate generation script (`gen_victoria_certs.sh.j2`) is extended with VictoriaLogs SANs:

> *Implementation details: See Component Spec (LLD)*


---

**Ansible variable definitions (extension to `vars/main.yml`):**

> *Implementation details: See Component Spec (LLD)*


---

**Air-gapped (offline) installation:**

Omnia is always deployed in an air-gapped environment. All container images are managed through the `service_k8s.json` image registry mechanism and pre-staged in the local Pulp repository:

| Image | Key in `service_k8s.json` | Notes |
|-------|--------------------------|-------|
| `victoriametrics/victoria-logs` | `victoriametrics/victoria-logs` | Single image for all VictoriaLogs cluster components. Operator determines component role internally via `clusterVersion`. Admin manages version only. |
| `victoriametrics/vlagent` | `victoriametrics/vlagent` | Log collector/forwarder. Version aligned with victoria-logs. |

**Image staging flow:**
1. L2 validation extracts image references from `service_k8s.json`
2. `local_repo.yml` downloads images and stages them in the local Pulp repository
3. Kubernetes manifests reference images via the Pulp-mirrored registry
4. Deployment proceeds entirely offline — no Internet connectivity required

---

**Endpoint discovery output (aligned with VictoriaMetrics):**

After deployment, the following endpoint information is emitted (matching VictoriaMetrics output pattern):

> *Implementation details: See Component Spec (LLD)*


This allows downstream capabilities to discover and use VictoriaLogs endpoints programmatically, identical to how they discover VictoriaMetrics endpoints (vminsert, vmselect).

---

**Generated manifest inventory (operator CRs):**

| Manifest | Type | Scope | Template Source |
|----------|------|-------|-----------------|
| `victorialogs-operator-vlcluster.yaml` | `VLCluster` CR | Platform | `victorialogs-operator-vlcluster.yaml.j2` |
| `victorialogs-operator-vlagent.yaml` | `VLAgent` CR | Platform | `victorialogs-operator-vlagent.yaml.j2` |
| `vlagent-config.yaml` | ConfigMap | Platform | `vlagent-config.yaml.j2` |
| `kustomization.yaml` | Kustomization | Platform | `kustomization.yaml.j2` |

**Note**: The operator creates the underlying Kubernetes resources (StatefulSets, Deployments, Services, PVCs) from the CRs. Manual StatefulSet/Deployment manifests are not generated.

##### 4.1.3.3 Data Flow Diagram for Component

**Platform-level data flow (source-decoupled):**

```
SEQUENCE: Log Ingestion (Platform View)

Any Ingestion Client        vlinsert               vlstorage
(VLAgent, future             (ingestion GW)         (storage)
 capability, direct POST)
     |                           |                      |
     |-- JSON Lines / syslog --> |                      |
     |   / ES bulk API           |                      |
     |   (HTTPS :9481)          |                      |
     |                           |-- shard data ------->|
     |                           |   (TLS :9401)        |
     |                           |   consistent hash    |
     |                           |                      |
     |                           |   vlstorage-0 ←      |
     |                           |   vlstorage-1 ←      |
     |                           |                      |
```

**Query path:**

```
SEQUENCE: Log Query (Platform View)

Any Query Client        vlselect               vlstorage-0          vlstorage-1
(future capability,     (query GW)             (storage)            (storage)
 admin, API client)
     |                     |                       |                     |
     |-- LogsQL query ---->|                       |                     |
     |   (HTTPS :9491)     |                       |                     |
     |                     |-- fan-out query ----->|                     |
     |                     |   (TLS :9402)         |                     |
     |                     |                       |                     |
     |                     |-- fan-out query ------------------------------>|
     |                     |   (TLS :9402)                                 |
     |                     |                       |                     |
     |                     |<-- partial results ---|                     |
     |                     |<-- partial results ----------------------------|
     |                     |                       |                     |
     |                     |-- merge + sort        |                     |
     |                     |                       |                     |
     |<-- results ---------|                       |                     |
     |                     |                       |                     |
```

##### 4.1.3.4 Actor / Action Matrix

Refer section 3.4

##### 4.1.3.5 Component Threat Modeling

Refer section 3.5

##### 4.1.3.6 Interfaces

**Provided Interfaces (platform endpoints for downstream capabilities):**

| Interface | Type | Purpose |
|-----------|------|---------|
| `vlinsert :9481` | HTTPS (LoadBalancer) | Standard log ingestion endpoint — JSON Lines, syslog RFC 5424, ES bulk API |
| `vlselect :9491` | HTTPS (LoadBalancer) | Standard log query endpoint — LogsQL query, hits, stats, streams, tail |
| `VLAgent :514` | syslog TCP+UDP (LoadBalancer) | Platform syslog receiver (plaintext) |
| `VLAgent :6514` | syslog TLS TCP (LoadBalancer) | Platform syslog receiver (TLS-secured, RFC 5425) |
| `VLAgent :8429` | HTTP (ClusterIP) | Health check endpoint |

**Internal Interfaces (within telemetry namespace):**

| Source | Destination | Protocol | Port | Authentication | Purpose |
|--------|-------------|----------|------|----------------|---------|
| vlinsert | vlstorage | HTTPS | 9401 | TLS (cert from victoria-tls-certs) | Log data sharding |
| vlselect | vlstorage | HTTPS | 9402 | TLS (cert from victoria-tls-certs) | Query fan-out |
| VLAgent | vlinsert | HTTPS | 9481 | TLS (CA cert validation) | Log delivery |

**External Interfaces (outside cluster):**

| Source | Destination | Protocol | Port | Authentication | Purpose |
|--------|-------------|----------|------|----------------|---------|
| Any downstream log client | vlinsert | HTTPS | 9481 | mTLS (CA cert) | Log ingestion |
| Any downstream query client | vlselect | HTTPS | 9491 | mTLS (CA cert) | Log queries |

**Secret Interfaces:**

| Secret Name | Namespace | Contents | Used By |
|-------------|-----------|----------|---------|
| `victoria-tls-certs` | telemetry | tls.crt, tls.key, ca.crt | vlstorage, vlinsert, vlselect, VLAgent |

**Consumed Interfaces:**

| Interface | Provider | Purpose |
|-----------|----------|---------|
| `victoria-tls-certs` Secret | VictoriaMetrics deployment | Shared TLS certificates |
| `telemetry` Namespace | VictoriaMetrics / iDRAC deployment | Shared namespace |

**Ansible Playbook Interfaces:**

| Playbook / Task | Purpose |
|-----------------|---------|
| `deploy_victorialogs_cluster.yml` | Generate and apply `VLCluster` + `VLAgent` operator CRs (idempotent); skipped when `'victoria'` is not in `telemetry_collection_type` |
| `teardown_victorialogs_cluster.yml` | Delete `VLCluster` + `VLAgent` CRs; operator removes workloads; prompt for PVC cleanup |
| `validate_telemetry_config.yml` | Validate VictoriaLogs configuration inputs; skips VictoriaLogs validation when disabled |
| `cleanup_telemetry.sh` | Cleanup script with `victorialogs` argument for selective component removal |

##### 4.1.3.7 Disabling VictoriaLogs Cluster

This section describes the design for disabling (tearing down) the VictoriaLogs cluster platform service and the log source pipelines. Two levels of disabling are supported:

1. **Disable log source pipelines** — via `disable_log.yml` playbook with tags (VictoriaLogs cluster keeps running)
2. **Disable VictoriaLogs cluster entirely** — via `telemetry_collection_type` or cleanup script (removes all VictoriaLogs components)

**4.1.3.7.1 Disable Log Source Pipelines (`disable_log.yml`)**

A dedicated `disable_log.yml` playbook provides tag-based selective disabling of log source pipelines. This disables the **log forwarding** from specific storage platforms to VictoriaLogs, without tearing down the VictoriaLogs cluster itself.

**Usage:**

```bash
# Disable PowerScale syslog forwarding to VictoriaLogs
ansible-playbook disable_log.yml --tags powerscale

# Disable VAST log forwarding to VictoriaLogs
ansible-playbook disable_log.yml --tags vast

# Disable PowerVault log forwarding to VictoriaLogs
ansible-playbook disable_log.yml --tags powervault

# Disable all log source pipelines (VictoriaLogs cluster keeps running)
ansible-playbook disable_log.yml --tags all
ansible-playbook disable_log.yml   # same as --tags all
```

**Supported tags:**

| Tag | Components Removed | VictoriaLogs Cluster |
|-----|-------------------|---------------------|
| *(no tags)* | All log source pipelines (same as `all`) | Keeps running |
| `powerscale` | PowerScale VLAgent syslog pipeline, configmap, service | Keeps running |
| `vast` | VAST log forwarding pipeline | Keeps running |
| `powervault` | PowerVault log forwarding pipeline | Keeps running |
| `all` | All of the above | Keeps running |

**Key design principle:** `disable_log.yml` removes only the source-specific log pipelines (VLAgent configurations, relabel rules, syslog receivers). The VictoriaLogs cluster (vlstorage, vlinsert, vlselect) continues running and serving queries on previously ingested logs.

**PVC handling:** PVCs are preserved. Historical logs remain queryable via vlselect after disabling a log source pipeline.

> *Implementation details: See Component Spec (LLD)*

**4.1.3.7.2 Disable VictoriaLogs Cluster (Deployment Gate)**

VictoriaLogs cluster shares the same deployment gate as VictoriaMetrics: the `telemetry_collection_type` field in `telemetry_config.yml`.

**To disable VictoriaLogs cluster entirely**: Remove `"victoria"` from `telemetry_collection_type`. This also disables VictoriaMetrics — the two are always co-deployed.

**To disable only log source pipelines** (keep VictoriaLogs cluster running): Use `disable_log.yml --tags <source>` instead.

**4.1.3.7.3 Conditional Deployment Logic**

VictoriaLogs deployment is gated by the same `'victoria' in types` condition used by VictoriaMetrics, matching the existing pattern in `generate_telemetry_deployments.yml` and `kustomization.yaml.j2`.

**In `generate_telemetry_deployments.yml`** (extend existing victoria block):

> *Implementation details: See Component Spec (LLD)*


**In `kustomization.yaml.j2`** (extend existing victoria block):

> *Implementation details: See Component Spec (LLD)*


**When `'victoria'` is NOT in `telemetry_collection_type`**:
- No VictoriaMetrics manifests are generated (existing behavior)
- No VictoriaLogs manifests are generated (new behavior — same gate)
- No `kubectl apply` for either VictoriaMetrics or VictoriaLogs
- Existing resources (if previously deployed) remain running until explicitly cleaned up via the cleanup script
- Kafka and iDRAC telemetry are unaffected (controlled by their own flags)

**4.1.3.7.3 Cleanup Script Extension**

The existing `cleanup_telemetry.sh.j2` is extended with a `victorialogs` cleanup option, following the exact same pattern as `kafka`, `ldms`, `idrac`, and `victoria`.

**Updated usage line:**
```bash
# Usage: ./cleanup_telemetry.sh [kafka] [ldms] [idrac] [victoria] [victorialogs] [all]
```

**Updated argument parsing:**
> *Implementation details: See Component Spec (LLD)*


**Updated components display:**
```bash
echo "  VictoriaLogs:    $([ "$CLEAN_VICTORIALOGS" = true ] && echo "YES" || echo "NO")"
```

**New cleanup steps for VictoriaLogs (added after existing Victoria cleanup):**

> *Implementation details: See Component Spec (LLD)*


**PVC cleanup (added to the existing PVC cleanup step):**

> *Implementation details: See Component Spec (LLD)*


**Force delete (added to the existing force delete step):**

> *Implementation details: See Component Spec (LLD)*


**Remaining resource check (added to the existing check step):**

> *Implementation details: See Component Spec (LLD)*


**4.1.3.7.4 Cleanup Ordering and Dependencies**

VictoriaLogs cleanup is **independent** of all other telemetry components:

| Cleanup Scenario | VictoriaMetrics | Kafka | iDRAC | VictoriaLogs | Effect |
|-----------------|-----------------|-------|-------|--------------|--------|
| `./cleanup_telemetry.sh victorialogs` | Untouched | Untouched | Untouched | Removed | Only VictoriaLogs cluster and VLAgent removed |
| `./cleanup_telemetry.sh victoriametrics` | Removed | Untouched | Untouched | Untouched | Only VictoriaMetrics removed; VictoriaLogs continues operating |
| `./cleanup_telemetry.sh victoriametrics victorialogs` | Removed | Untouched | Untouched | Removed | Both metrics and logs stacks removed |
| `./cleanup_telemetry.sh all` | Removed | Removed | Removed | Removed | Full telemetry cleanup |

**Shared resource handling:**
- `victoria-tls-certs` secret: **NOT deleted** during `victorialogs` cleanup. This secret is shared with VictoriaMetrics and is only deleted during `victoriametrics` cleanup (existing behavior). If VictoriaLogs is re-enabled later, the secret is still available.
- `telemetry` namespace: **NOT deleted** during `victorialogs` cleanup. Namespace is shared and only deleted via explicit `kubectl delete namespace telemetry`.

**4.1.3.7.5 PVC Data Retention Policy**

Following the existing VictoriaMetrics pattern, vlstorage PVCs are **NOT automatically deleted** when VictoriaLogs is disabled or cleaned up:

| Resource | Auto-deleted on disable | Manual cleanup command |
|----------|------------------------|----------------------|
| vlstorage StatefulSet | Yes (via cleanup script) | N/A |
| vlinsert Deployment | Yes (via cleanup script) | N/A |
| vlselect Deployment | Yes (via cleanup script) | N/A |
| VLAgent Deployment | Yes (via cleanup script) | N/A |
| vlstorage PVCs (data) | **No** — requires explicit cleanup | `kubectl delete pvc -l app=vlstorage -n telemetry` |
| VLAgent PVC (buffer) | **No** — requires explicit cleanup | `kubectl delete pvc -l app=vlagent -n telemetry` |

**Rationale**: PVCs contain log data that may be needed for audit or compliance. Automatic deletion could cause unintended data loss. The cleanup script deletes PVCs only when explicitly invoked with the `victorialogs` argument.

**4.1.3.7.6 Disable → Re-enable Behavior**

When VictoriaLogs is disabled (by removing `"victoria"` from `telemetry_collection_type`) and later re-enabled (by adding `"victoria"` back):

| Scenario | Behavior |
|----------|----------|
| PVCs still exist (not manually cleaned) | vlstorage pods remount existing PVCs; previously stored logs are accessible |
| PVCs manually deleted | vlstorage pods create new PVCs; fresh start with no historical data |
| TLS certs still valid | VictoriaLogs components reuse existing `victoria-tls-certs` secret |
| TLS certs regenerated | VictoriaLogs components use new certificates; no reconfiguration needed |

**Re-enable is idempotent**: Running the discovery playbook with `"victoria"` in `telemetry_collection_type` generates and applies all manifests via `kubectl apply -k`, creating any missing resources.

**4.1.3.7.7 Validation When Disabled**

When `"victoria"` is NOT in `telemetry_collection_type`:

- **L2 Python Validation**: Skips VictoriaLogs-specific validation (retention period, storage size, image versions) — same as existing VictoriaMetrics skip behavior
- **Ansible Validation**: Displays informational message that VictoriaMetrics and VictoriaLogs are not being deployed
- **Deployment**: Skips all VictoriaMetrics and VictoriaLogs manifest generation and `kubectl apply`
- **Endpoint Discovery**: VictoriaMetrics and VictoriaLogs endpoints are not emitted in the discovery output

**Warning handling:**

> *Implementation details: See Component Spec (LLD)*


**4.1.3.7.8 Impact on Downstream Capabilities**

When VictoriaLogs is disabled, all downstream capabilities that depend on the VictoriaLogs ingestion or query endpoints will be affected:

| Impact | Description |
|--------|-------------|
| vlinsert endpoint unavailable | Downstream log ingestion clients will receive connection refused errors |
| vlselect endpoint unavailable | Downstream log query clients will receive connection refused errors |
| VLAgent syslog receiver unavailable | External syslog sources will fail to deliver logs (connection refused on :514 and :6514) |
| No log data loss for sources | Log sources (Kafka topics, syslog devices) continue to operate; logs are simply not collected |
| Re-enabling restores service | When re-enabled, endpoints become available again; Kafka consumers can replay from last offset |

**No cascading failures**: Disabling VictoriaLogs does not affect VictoriaMetrics (metrics), Kafka (event streaming), iDRAC telemetry, LDMS, or any other telemetry component.

##### 4.1.3.8 Upgrade Scenarios

This section describes VictoriaLogs cluster behavior during Omnia version upgrades. The design aligns with the existing upgrade pattern used by iDRAC telemetry and LDMS (`apply_telemetry_on_upgrade.yml`).

**4.1.3.8.1 Upgrade Detection**

Omnia detects an upgrade scenario via the `upgrade_enabled` flag, which is set when `oim_metadata.upgrade_backup_dir` is defined and non-empty. When `upgrade_enabled: true`, the discovery playbook invokes `apply_telemetry_on_upgrade.yml` after standard telemetry deployment.

The existing upgrade flow is:
```
discovery playbook
    ├── Standard telemetry deployment (generate + apply manifests)
    └── if upgrade_enabled:
            apply_telemetry_on_upgrade.yml
                ├── iDRAC telemetry upgrade (preserve replica count, reapply StatefulSet)
                ├── LDMS upgrade (restart store daemon)
                └── VictoriaLogs cluster upgrade  ← NEW
```

**4.1.3.8.2 Upgrade Configuration Transformation**

During an Omnia upgrade, `transform_telemetry_config.yml` reads the backup `telemetry_config.yml` and transforms it into the new version format. VictoriaLogs configuration fields are extracted from the `victoria_logs_configurations` section, carried forward alongside existing `victoria_metrics_configurations`:

> *Implementation details: See Component Spec (LLD)*


**4.1.3.8.3 Scenario Matrix**

The upgrade behavior depends on two factors:
- `idrac_telemetry_support` — whether iDRAC telemetry is enabled (gates the telemetry block)
- `telemetry_collection_type` — whether `"victoria"` is included (controls VictoriaMetrics AND VictoriaLogs deployment)

| # | Scenario | `idrac_telemetry_support` | `collection_type` includes `victoria` | VictoriaMetrics State | VictoriaLogs Action |
|---|----------|--------------------------|---------------------------------------|----------------------|---------------------|
| U1 | Full telemetry (typical) | `true` | Yes (`victoria,kafka`) | Running (cluster mode) | Deploy/upgrade VictoriaLogs cluster; TLS certs shared; both stacks coexist |
| U2 | Kafka-only collection | `true` | No (`kafka` only) | Not deployed | VictoriaLogs NOT deployed — `'victoria'` not in collection type |
| U3 | Telemetry previously disabled | `false` (was false), now `true` | Yes | Not deployed → deployed | Fresh deploy of both VictoriaMetrics and VictoriaLogs; create TLS certs |
| U4 | Collection type changed to include victoria | `true` | Yes (was `kafka`, now `victoria,kafka`) | Not deployed → deployed | Fresh deploy of both VictoriaMetrics and VictoriaLogs; no prior data |
| U5 | Collection type changed to remove victoria | `true` | No (was `victoria,kafka`, now `kafka`) | Running → skipped | VictoriaLogs deployment skipped; existing resources remain until cleanup |
| U6 | Full stack with existing VictoriaLogs | `true` | Yes (`victoria,kafka`) | Running | Upgrade VictoriaLogs — reapply manifests with preserved state; rolling update |

**4.1.3.8.4 Scenario U1 — Full Telemetry (`telemetry_support: true`, collection type includes `victoria`)**

This is the typical production scenario. VictoriaMetrics is deployed (cluster or single-node) and VictoriaLogs is deployed alongside it.

**Upgrade behavior:**
> *Implementation details: See Component Spec (LLD)*


**Key behaviors:**
- vlstorage replica count is preserved across the upgrade (same pattern as iDRAC StatefulSet)
- Manifests are re-applied via `kubectl apply -k` (idempotent)
- Rolling update — Kubernetes performs rolling update if image versions changed
- PVC data is preserved — vlstorage PVCs are not deleted during upgrade
- 120-second readiness timeout per component

**TLS certificate handling:**
- `victoria-tls-certs` secret is shared with VictoriaMetrics — already present and valid
- VictoriaLogs SANs verified; if missing, TLS certs are regenerated with extended SANs
- Rolling restart triggered only if certificate content changed

**4.1.3.8.5 Scenario U2 — Collection Type Does NOT Include `victoria`**

When `telemetry_collection_type` is `"kafka"` only, **neither VictoriaMetrics nor VictoriaLogs is deployed**. The two are always co-deployed — there is no scenario where VictoriaLogs is deployed without VictoriaMetrics.

**Behavior:**
- VictoriaMetrics cluster (vminsert, vmselect, vmstorage) is NOT deployed
- VictoriaLogs cluster (vlinsert, vlselect, vlstorage, VLAgent) is NOT deployed
- `victoria-tls-certs` secret is NOT generated
- Only Kafka and iDRAC telemetry components are deployed (if their flags are enabled)
- If VictoriaMetrics/VictoriaLogs were previously deployed (collection type changed from `victoria,kafka` to `kafka`), existing resources remain running until cleaned up via `./cleanup_telemetry.sh victoriametrics victorialogs`

**4.1.3.8.6 Scenario U3 — `telemetry_support` Was Previously `false`**

When upgrading from a deployment where all telemetry was disabled (`idrac_telemetry_support: false`) and now set to `true` with `"victoria"` in the collection type.

**Key behaviors:**
- `telemetry` namespace may NOT exist (it is created when any telemetry feature is enabled)
- No existing VictoriaMetrics, Kafka, or VictoriaLogs resources
- Fresh deployment of both VictoriaMetrics and VictoriaLogs cluster

**Upgrade behavior:**
> *Implementation details: See Component Spec (LLD)*


**Validation handling:**
- `telemetry_config.yml` is validated — both VictoriaMetrics and VictoriaLogs fields must be valid
- If `idrac_telemetry_support: false`, all VictoriaMetrics and VictoriaLogs validation is skipped

**4.1.3.8.7 Upgrade Transformation Template Extension**

The existing `transform_telemetry_config.yml` must be extended to preserve VictoriaLogs configuration across upgrades:

> *Implementation details: See Component Spec (LLD)*


The `telemetry_config.j2` template must include these new fields in the rendered output.

**4.1.3.8.8 Upgrade Validation Summary**

| Validation | When Checked | Action on Failure |
|------------|-------------|-------------------|
| `'victoria' in telemetry_collection_type` | L2 Python validation / Ansible | Determines whether VictoriaMetrics + VictoriaLogs are deployed |
| `victoria_logs_configurations.retention_period` is valid duration | L2 Python validation (when `'victoria'` in types) | Fail with validation error |
| `victoria_logs_configurations.storage_size` is valid PVC format | L2 Python validation (when `'victoria'` in types) | Fail with validation error |
| Image versions in `service_k8s.json` | L2 Python validation (when `'victoria'` in types) | Fail with validation error |
| `victoria-tls-certs` secret exists | Ansible deployment (when `'victoria'` in types) | Generate new certificates |
| `telemetry` namespace exists | Ansible deployment (when `'victoria'` in types) | Create namespace |
| vlstorage StatefulSet exists (upgrade) | `apply_telemetry_on_upgrade.yml` | Fresh deploy (not upgrade) |
| Backup `telemetry_config.yml` exists | `transform_telemetry_config.yml` | Fail with error |

---

##### 4.1.3.9 Port Allocation and Conflict Verification

This section documents all ports used by VictoriaLogs cluster components and verifies there are no conflicts with existing components in the telemetry namespace.

**4.1.3.9.1 VictoriaLogs Cluster Port Assignments**

| Port | Component | Protocol | Service Type | Purpose |
|------|-----------|----------|-------------|---------|
| 9481 | vlinsert | HTTPS | LoadBalancer | Log ingestion endpoint (JSON Lines, syslog RFC 5424, ES bulk API) |
| 9491 | vlselect | HTTPS | LoadBalancer | Log query endpoint (LogsQL) |
| 9401 | vlstorage | HTTPS | Headless (internal) | Data ingestion from vlinsert (sharding) |
| 9402 | vlstorage | HTTPS | Headless (internal) | Query fan-out from vlselect |
| 514 | VLAgent | TCP+UDP | LoadBalancer | Syslog receiver — plaintext (RFC 3164/5424) |
| 6514 | VLAgent | TLS TCP | LoadBalancer | Syslog receiver — TLS-secured (RFC 5425) |
| 8429 | VLAgent | HTTP | ClusterIP | Health check endpoint |

**4.1.3.9.2 Existing Telemetry Namespace Port Inventory**

All ports currently used by components in the `telemetry` namespace:

| Port | Component | Type | Status |
|------|-----------|------|--------|
| 8480 | vminsert (VictoriaMetrics cluster) | LoadBalancer | Active |
| 8481 | vmselect (VictoriaMetrics cluster) | LoadBalancer | Active |
| 8482 | vmstorage (VictoriaMetrics cluster) | Headless | Active |
| 8400 | vmstorage (VictoriaMetrics cluster) | Headless (vminsert comm) | Active |
| 8401 | vmstorage (VictoriaMetrics cluster) | Headless (vmselect comm) | Active |
| 8443 | victoria-loadbalancer (VictoriaMetrics single-node) | LoadBalancer | Active |
| 8429 | vmagent / VLAgent | ClusterIP (health) | Active |
| 9428 | victorialogs (single-node) — **LEGACY, replaced by cluster mode** | ClusterIP | Deprecated — replaced by vlinsert :9481 and vlselect :9491 |
| 514 | vlagent-powerscale (VLAgent) | LoadBalancer | Active |
| 2112 | victoria-pump (iDRAC telemetry) | ClusterIP | Active |
| 9092 | Kafka brokers (Strimzi) | ClusterIP | Active |
| 6001 | LDMS aggregator / store | ClusterIP | Active |
| 10001 | LDMS sampler | ClusterIP | Active |
| 4317 | OTEL Collector (gRPC) | ClusterIP | Active |
| 4318 | OTEL Collector (HTTP) | ClusterIP | Active |
| 8889 | OTEL Collector (Prometheus) | ClusterIP | Active |

**4.1.3.9.3 Conflict Verification Results**

| VictoriaLogs Port | Conflicts With | Status | Notes |
|-------------------|---------------|--------|-------|
| **9481** (vlinsert) | None | **NO CONFLICT** | Not used by any existing component |
| **9491** (vlselect) | None | **NO CONFLICT** | Not used by any existing component |
| **9401** (vlstorage ingestion) | None | **NO CONFLICT** | Not used by any existing component |
| **9402** (vlstorage query) | None | **NO CONFLICT** | Not used by any existing component |
| **514** (VLAgent syslog) | vlagent-powerscale (existing) | **SHARED — EXPECTED** | Same component (VLAgent platform replaces per-source VLAgent); standard syslog port |
| **8429** (VLAgent health) | vmagent-powerscale, VLAgent (existing) | **SHARED — EXPECTED** | Same health port used by existing VLAgent and vmagent; no conflict because each runs in separate pods with separate ClusterIP services |

**4.1.3.9.4 Port 9428 — Legacy Single-Node (Deprecated)**

The legacy single-node VictoriaLogs deployment used port 9428. Since only cluster mode is supported, this port is deprecated. In cluster mode, this port is replaced by:
- **9481** (vlinsert) for ingestion — replaces `victorialogs:9428` as the ingestion endpoint
- **9491** (vlselect) for queries — new query-specific endpoint

**Migration impact:**
- VLAgent config must update `url:` from `http://victorialogs.telemetry.svc.cluster.local:9428/insert/jsonline` to `https://vlinsert.telemetry.svc.cluster.local:9481/insert/jsonline`
- Any downstream clients pointing to port 9428 must be updated to 9481 (ingestion) or 9491 (query)
- The single-node VictoriaLogs Deployment and Service (port 9428) are replaced by cluster components during deployment; no port conflict during transition

**4.1.3.9.5 Port Allocation Design Rationale**

| Decision | Rationale |
|----------|-----------|
| 9481 for vlinsert (not 8480) | Avoids conflict with vminsert (8480); 9xxx range reserved for VictoriaLogs |
| 9491 for vlselect (not 8481) | Avoids conflict with vmselect (8481); 9xxx range reserved for VictoriaLogs |
| 9401/9402 for vlstorage internal (not 8400/8401) | Avoids conflict with vmstorage (8400/8401); parallel port scheme: VM uses 8400-8482, VL uses 9401-9491 |
| 514 for syslog plaintext (unchanged) | Standard syslog port (RFC 3164/5424); configurable via `syslog_receiver_port` in `telemetry_config.yml` |
| 6514 for syslog TLS (new) | Standard syslog-over-TLS port (RFC 5425); reuses `victoria-tls-certs` shared certificate; configurable via `syslog_tls_receiver_port` in `telemetry_config.yml` |
| 8429 for health (unchanged) | Existing VLAgent/vmagent health port; no change needed |

**Port range summary:**
- **VictoriaMetrics cluster**: 8400–8482
- **VictoriaLogs cluster**: 9401–9491
- **No overlap**: Both port ranges are fully independent

---

##### 4.1.3.10 VictoriaMetrics Operator — Unified Deployment for VictoriaMetrics and VictoriaLogs

This section documents the operator-based deployment model for both VictoriaMetrics and VictoriaLogs. The same VictoriaMetrics operator manages both systems via Custom Resources (CRs). All container images are sourced from `docker.io/victoriametrics/operator` in `service_k8s.json`.

**4.1.3.10.1 Operator Overview**

The VictoriaMetrics operator (v0.68.3+) supports CRDs for both VictoriaMetrics (metrics) and VictoriaLogs (logs). A single operator instance manages the complete observability stack:

| CRD Kind | API Version | Purpose | Manages |
|----------|-------------|---------|---------|
| `VMCluster` | `operator.victoriametrics.com/v1beta1` | VictoriaMetrics cluster mode | vmstorage StatefulSet, vminsert Deployment, vmselect Deployment |
| `VMSingle` | `operator.victoriametrics.com/v1beta1` | VictoriaMetrics single-node mode | Single Victoria StatefulSet |
| `VMAgent` | `operator.victoriametrics.com/v1beta1` | Metrics scraper/forwarder | vmagent Deployment with remote_write |
| `VMPodScrape` | `operator.victoriametrics.com/v1beta1` | Pod-based metrics discovery | Replaces ConfigMap-based scrape config |
| **`VLCluster`** | `operator.victoriametrics.com/v1beta1` | **VictoriaLogs cluster mode** | **vlstorage StatefulSet, vlinsert Deployment, vlselect Deployment** |
| **`VLAgent`** | `operator.victoriametrics.com/v1beta1` | **Log collector/forwarder** | **VLAgent Deployment** |

**Key advantage**: One operator Helm chart install manages both VictoriaMetrics and VictoriaLogs — no separate operator or Helm chart needed for logs.

**4.1.3.10.2 Operator Installation**

The operator is installed via Helm chart as part of the telemetry deployment:

> *Implementation details: See Component Spec (LLD)*


**Image in `service_k8s.json`:**
```json
{
  "victoriametrics/operator": "docker.io/victoriametrics/operator:v0.68.3"
}
```

**4.1.3.10.3 VictoriaLogs Operator CRDs**

**VLCluster CR — VictoriaLogs Cluster Mode:**

The `VLCluster` CR declaratively defines the VictoriaLogs cluster. The operator creates and manages vlstorage StatefulSet, vlinsert Deployment, and vlselect Deployment.

> *Implementation details: See Component Spec (LLD)*


**VLAgent CR — Log Collector/Forwarder:**

> *Implementation details: See Component Spec (LLD)*


**4.1.3.10.4 Kustomization — Unified CRs**

> *Implementation details: See Component Spec (LLD)*


**4.1.3.10.5 Images in `service_k8s.json`**

All images use the `docker.io/victoriametrics/` registry. The operator image manages all components.

| Image | Key in `service_k8s.json` | Purpose |
|-------|--------------------------|---------|
| `docker.io/victoriametrics/operator` | `victoriametrics/operator` | Operator itself (Helm chart) |
| `docker.io/victoriametrics/vmstorage` | `victoriametrics/vmstorage` | VictoriaMetrics storage |
| `docker.io/victoriametrics/vminsert` | `victoriametrics/vminsert` | VictoriaMetrics ingestion |
| `docker.io/victoriametrics/vmselect` | `victoriametrics/vmselect` | VictoriaMetrics query |
| `docker.io/victoriametrics/vmagent` | `victoriametrics/vmagent` | Metrics scraper/forwarder |
| `docker.io/victoriametrics/victoria-logs` | `victoriametrics/victoria-logs` | VictoriaLogs (vlstorage, vlinsert, vlselect — tag selects component) |
| `docker.io/victoriametrics/vlagent` | `victoriametrics/vlagent` | VLAgent — log collector/forwarder |

All images are pre-staged in the local Pulp repository for air-gapped deployment.

**4.1.3.10.6 TLS Certificate Handling**

TLS certificates are managed by Omnia via `gen_victoria_certs.sh` and stored in the `victoria-tls-certs` Kubernetes secret. The operator mounts this user-provided secret into vlstorage, vlinsert, and vlselect pods. SAN management remains Omnia's responsibility. The `gen_victoria_certs.sh` script must include VictoriaLogs SANs (vlinsert, vlselect, vlstorage, vlstorage-0, vlstorage-1).

**4.1.3.10.7 Operator-Managed vs Manual Resources**

| Resource | Managed By | Notes |
|----------|-----------|-------|
| vmstorage StatefulSet | Operator (via `VMCluster` CR) | Operator creates, scales, updates |
| vminsert Deployment | Operator (via `VMCluster` CR) | Operator creates, scales, updates |
| vmselect Deployment | Operator (via `VMCluster` CR) | Operator creates, scales, updates |
| vmagent Deployment | Operator (via `VMAgent` CR) | Operator creates, configures remote_write |
| vlstorage StatefulSet | Operator (via `VLCluster` CR) | Operator creates, scales, updates |
| vlinsert Deployment | Operator (via `VLCluster` CR) | Operator creates, scales, updates |
| vlselect Deployment | Operator (via `VLCluster` CR) | Operator creates, scales, updates |
| VLAgent Deployment | Operator (via `VLAgent` CR) | Operator creates, manages lifecycle |
| vmagent RBAC | Manual manifest | ServiceAccount, Role, RoleBinding retained as manual |
| VLAgent ConfigMap | Manual manifest | Syslog receiver configuration |
| VLAgent PVC | Manual manifest | Buffer storage |
| TLS Certificates | Manual (`gen_victoria_certs.sh` → `victoria-tls-certs` secret; operator mounts it) | Omnia generates certs; operator mounts the user-provided secret |

**4.1.3.10.8 Upgrade Behavior with Operator**

When upgrading VictoriaLogs via operator CRs:
- Update `VLCluster` CR spec (e.g., new image tag, changed replica count, storage size)
- Operator detects CR change and performs **rolling update** automatically
- vlstorage StatefulSet pods are updated one by one (ordered)
- vlinsert/vlselect Deployments are updated via standard Kubernetes rolling update
- PVCs are preserved — operator does not delete PVCs during upgrades
- No need for manual `kubectl apply -k` replica count preservation — operator manages state
- Version is controlled via `clusterVersion` field in the VLCluster CR (single image for all components)

> *Implementation details: See Component Spec (LLD)*

---

#### 4.1.4 Security Considerations and Test Plan

##### 4.1.4.1 Security Design Objectives

###### 4.1.4.1.1 Applicable Security Design Controls

| Control | Implementation |
|---------|---------------|
| TLS encryption in transit | All vlinsert ↔ vlstorage and vlselect ↔ vlstorage communication uses TLS via shared `victoria-tls-certs` secret |
| mTLS for external access | External clients accessing vlinsert :9481 or vlselect :9491 must present valid certificates (where supported) |
| Credential isolation | `no_log: true` on all Ansible tasks handling TLS secrets; secrets are Kubernetes-managed with namespace RBAC |
| Certificate rotation | 10-year self-signed CA; regeneration via `gen_victoria_certs.sh` with rolling restart |

###### 4.1.4.1.2 Manual Security Unit Testing Plan

| Test | Steps | Expected Result |
|------|-------|-----------------|
| Verify TLS on vlinsert | `curl -v https://<vlinsert_ip>:9481/health` | TLS handshake successful; returns 200 OK |
| Verify mTLS enforcement | `curl -v https://<vlinsert_ip>:9481/health` (without client cert) | Connection rejected or 403 when mTLS enforced |
| Verify TLS on vlselect | `curl -v https://<vlselect_ip>:9491/health` | TLS handshake successful; returns 200 OK |
| Verify VLAgent → vlinsert TLS | Inspect VLAgent logs for TLS handshake success | No TLS errors in VLAgent logs |
| Verify credential isolation | Check Ansible logs for credential exposure | No credentials visible in Ansible output (`no_log: true`) |

###### 4.1.4.1.3 Automation Security Unit Testing Plan

N/A — Security testing is performed as part of integration testing.

##### 4.1.4.2 Protect Sensitive Information

###### 4.1.4.2.1 Applicable Sensitive Information Controls

| Sensitive Data | Storage | Protection |
|----------------|---------|------------|
| TLS certificates (tls.crt, tls.key, ca.crt) | Kubernetes Secret `victoria-tls-certs` | Namespace-level RBAC; `no_log: true` in Ansible |

###### 4.1.4.2.2 Manual Security Unit Testing Plan

N/A

###### 4.1.4.2.3 Automation Security Unit Testing Plan

N/A

##### 4.1.4.3 Secure Web Interfaces

###### 4.1.4.3.1 Applicable Secure Web Interfaces Controls

| Interface | Control |
|-----------|---------|
| vlinsert :9481 | HTTPS with TLS; mTLS for external access |
| vlselect :9491 | HTTPS with TLS; mTLS for external access |
| VLAgent :514 | Plaintext syslog TCP+UDP; for trusted internal networks only |
| VLAgent :6514 | Syslog over TLS (RFC 5425); TLS cert from shared `victoria-tls-certs` secret |
| VLAgent :8429 | HTTP (internal only, ClusterIP); no external exposure |

###### 4.1.4.3.2 Manual Security Unit Testing Plan

N/A

###### 4.1.4.3.3 Automation Security Unit Testing Plan

N/A

##### 4.1.4.4 Prevent Injection

###### 4.1.4.4.1 Applicable Security Design Controls

| Control | Implementation |
|---------|---------------|
| LogsQL injection prevention | VictoriaLogs vlselect sanitizes LogsQL query parameters; no raw SQL/shell execution |
| Ansible template injection | Jinja2 templates use `{{ variable }}` syntax with validated inputs from `telemetry_config.yml` |

###### 4.1.4.4.2 Manual Security Unit Testing Plan

N/A

###### 4.1.4.4.3 Automation Security Unit Testing Plan

N/A

#### 4.1.5 Resource Utilization and Scalability

**Platform resource footprint (8 pods — core cluster + VLAgent):**

| Component | Kind | Replicas | CPU Request | CPU Limit | Memory Request | Memory Limit | PVC per replica |
|-----------|------|----------|------------|-----------|----------------|--------------|-----------------|
| vlstorage | StatefulSet | 3 | 250m | 1000m | 1 Gi | 2 Gi | 8 Gi (configurable) |
| vlinsert | Deployment | 2 | 250m | 1000m | 512 Mi | 1 Gi | — |
| vlselect | Deployment | 2 | 250m | 1000m | 512 Mi | 1 Gi | — |
| VLAgent | Deployment | 1 | 50m | 250m | 128 Mi | 512 Mi | 5 Gi (configurable) |
| **Total** | | **8** | **1800m** | **7250m** | **~5.1 Gi** | **~10.5 Gi** | **29 Gi** |

**Estimated total at scale:**

| Scale | RAM (Estimated) | CPU (Estimated) | Storage (7-day retention) | Storage (30-day retention) |
|-------|-----------------|-----------------|---------------------------|---------------------------|
| 500-node cluster | ~8 Gi | ~4 CPU | ~70 GB | ~300 GB |
| 2,000-node cluster | ~8 Gi | ~4 CPU | ~350 GB | ~1.5 TB |

**Storage scaling formula:**
```
storage_per_node ≈ 140 MB/day × retention_days × node_count
```

**Scalability guidance:**
- vlinsert and vlselect replicas can be increased independently for higher ingestion or query throughput
- vlstorage replicas can be increased for additional storage capacity and query parallelism (requires TLS SAN extension for new pod DNS names)
- VLAgent resource allocation is configurable for environments with high syslog volume

#### 4.1.6 Open Source

| Component | License | Source | Docker Image | Version |
|-----------|---------|--------|--------------|---------|
| VictoriaLogs (vlstorage, vlinsert, vlselect) | Apache License 2.0 | https://github.com/VictoriaMetrics/VictoriaMetrics | `docker.io/victoriametrics/victoria-logs` | v1.49.0 |
| VLAgent (vlagent) | Apache License 2.0 | https://github.com/VictoriaMetrics/VictoriaMetrics | `docker.io/victoriametrics/vlagent` | v1.49.0 |
| VictoriaMetrics Operator | Apache License 2.0 | https://github.com/VictoriaMetrics/operator | `docker.io/victoriametrics/operator` | v0.68.3 |
| VictoriaMetrics Operator (config-reloader) | Apache License 2.0 | https://github.com/VictoriaMetrics/operator | `docker.io/victoriametrics/operator` | config-reloader-v0.68.3 |
| VictoriaMetrics Operator Helm Chart | Apache License 2.0 | https://github.com/VictoriaMetrics/helm-charts | `victoria-metrics-operator-0.59.3.tgz` | 0.59.3 |

**Note:** VLCluster CRD support requires operator >= v0.59.0. The operator Helm chart v0.59.3 includes VLCluster and VLAgent CRDs for deploying VictoriaLogs in cluster mode.

#### 4.1.7 Component Test

##### 4.1.7.1 Manual Unit Testing Plan

| Test ID | Test Description | Steps | Expected Result |
|---------|-----------------|-------|-----------------|
| VL-001 | vlstorage StatefulSet readiness | Deploy cluster; `kubectl get statefulset vlstorage -n telemetry` | 3/3 READY |
| VL-002 | vlinsert Deployment readiness | Deploy cluster; `kubectl get deploy vlinsert -n telemetry` | 2/2 READY |
| VL-003 | vlselect Deployment readiness | Deploy cluster; `kubectl get deploy vlselect -n telemetry` | 2/2 READY |
| VL-004 | VLAgent Deployment readiness | Deploy cluster; `kubectl get deploy vlagent -n telemetry` | 1/1 READY |
| VL-005 | vlinsert LoadBalancer IP allocation | `kubectl get svc vlinsert -n telemetry` | EXTERNAL-IP assigned |
| VL-006 | vlselect LoadBalancer IP allocation | `kubectl get svc vlselect -n telemetry` | EXTERNAL-IP assigned |
| VL-007 | TLS health check on vlinsert | `curl -k https://<vlinsert_ip>:9481/health` | 200 OK |
| VL-008 | TLS health check on vlselect | `curl -k https://<vlselect_ip>:9491/health` | 200 OK |
| VL-009 | Log ingestion via JSON Lines | `curl -k -X POST "https://<vlinsert_ip>:9481/insert/jsonline" -d '{"_msg":"test","_time":"2026-01-01T00:00:00Z","source":"test"}'` | 200 OK |
| VL-010 | Log query via LogsQL | `curl -k "https://<vlselect_ip>:9491/select/logsql/query?query=source:test"` | Returns ingested log |
| VL-011 | Endpoint discovery output | Check discovery playbook output | vlinsert, vlselect, VLAgent endpoints displayed (matching VictoriaMetrics output format) |
| VL-012 | Idempotent redeploy | Run discovery playbook twice; compare cluster state | No change on second run; all pods remain READY |
| VL-013 | vlstorage pod restart resilience | Delete vlstorage-0 pod; wait for restart; query data | Data preserved; pod recovers; query returns previous data |
| VL-014 | vlinsert failover | Delete one vlinsert pod; send log via curl | LoadBalancer routes to surviving replica; log ingested |
| VL-015 | vlselect failover | Delete one vlselect pod; run LogsQL query | LoadBalancer routes to surviving replica; query succeeds |
| VL-016 | Cleanup independence | Delete VictoriaLogs cluster; verify VictoriaMetrics and Kafka unaffected | VictoriaMetrics and Kafka pods remain READY |
| VL-017 | PVC persistence after StatefulSet deletion | Delete vlstorage StatefulSet; `kubectl get pvc -l app=vlstorage -n telemetry` | PVCs still exist (require manual cleanup) |
| VL-018 | Retention enforcement | Set retention to 1d; ingest logs; wait >1d; query | Old logs purged by vlstorage |
| VL-019 | Air-gapped deployment | Deploy with Pulp-staged images (standard air-gapped environment) | All pods start with images from local Pulp repository |
| VL-020 | Teardown workflow | Run teardown; verify all VictoriaLogs resources removed | All VictoriaLogs pods, services deleted; PVCs flagged for manual cleanup |
| VL-021 | Coexistence with VictoriaMetrics | Deploy VictoriaLogs alongside VictoriaMetrics; verify both healthy | Both clusters operate independently in telemetry namespace |
| VL-022 | Disable via collection type | Set `telemetry_collection_type: "kafka"` (remove `victoria`); re-run discovery playbook | No VictoriaMetrics or VictoriaLogs manifests generated; existing pods remain until cleanup |
| VL-023 | Cleanup script — VictoriaLogs only | Run `./cleanup_telemetry.sh victorialogs` | All VictoriaLogs pods/services deleted; VictoriaMetrics and Kafka unaffected |
| VL-024 | Cleanup script — all | Run `./cleanup_telemetry.sh all` | VictoriaLogs included in full cleanup alongside all other components |
| VL-025 | PVC retention after cleanup | Run cleanup; `kubectl get pvc -l app=vlstorage -n telemetry` | vlstorage PVCs still exist (require manual deletion) |
| VL-026 | PVC manual cleanup | Run `kubectl delete pvc -l app=vlstorage -n telemetry` | PVCs deleted; storage freed |
| VL-027 | Disable then re-enable (PVCs exist) | Remove `victoria` from collection type, cleanup pods; re-add `victoria`; query historical logs | vlstorage remounts existing PVCs; previously stored logs are accessible |
| VL-028 | Disable then re-enable (PVCs deleted) | Remove `victoria`, cleanup all including PVCs; re-add `victoria` | Fresh start; new PVCs created; no historical data |
| VL-029 | Shared TLS secret preserved after disable | Run `./cleanup_telemetry.sh victorialogs`; check `kubectl get secret victoria-tls-certs -n telemetry` | Secret still exists (shared with VictoriaMetrics) |
| VL-030 | Downstream impact when disabled | Remove `victoria` from collection type; attempt curl to vlinsert/vlselect endpoints | Connection refused; no cascading failure to other components |
| VL-031 | Upgrade U1 — full telemetry | Upgrade with `idrac_telemetry_support: true`, collection type `victoria,kafka` | VictoriaLogs cluster upgraded alongside VictoriaMetrics; replica count preserved; TLS certs shared |
| VL-032 | Upgrade U2 — kafka-only collection | Upgrade with collection type `kafka` only | Neither VictoriaMetrics nor VictoriaLogs deployed |
| VL-033 | Upgrade U3 — telemetry was disabled | Upgrade from `idrac_telemetry_support: false` to `true` with collection type `victoria,kafka` | Namespace created; TLS certs generated; fresh VictoriaMetrics + VictoriaLogs cluster deployed |
| VL-034 | Upgrade U6 — rolling update | Upgrade with new VictoriaLogs image version in `service_k8s.json` | Rolling update; pods updated one by one; no downtime; PVC data preserved |
| VL-035 | Upgrade config transformation | Run upgrade; verify VictoriaLogs retention/storage values preserved from backup config | Values from backup `telemetry_config.yml` carried to new format |
| VL-036 | Port 9481 no conflict | `kubectl get svc -n telemetry -o wide`; check no other service uses 9481 | Port 9481 exclusively used by vlinsert |
| VL-037 | Port 9491 no conflict | `kubectl get svc -n telemetry -o wide`; check no other service uses 9491 | Port 9491 exclusively used by vlselect |
| VL-038 | Port separation from VictoriaMetrics | Deploy both VictoriaMetrics cluster and VictoriaLogs cluster; verify all ports are distinct | VM ports (8400-8482) and VL ports (9401-9491) do not overlap |

##### 4.1.7.2 Automation Unit Testing Plan — Molecule

VictoriaLogs cluster mode introduces Molecule-based automated testing for the telemetry Ansible role. This is the first Molecule test framework in the Omnia repository and establishes the pattern for future role testing.

**4.1.7.2.1 Molecule Framework Overview**

| Property | Value |
|----------|-------|
| Framework | Molecule (Ansible role testing) |
| Driver | `delegated` (uses existing service Kubernetes cluster) |
| Provisioner | Ansible |
| Verifier | Ansible (verify.yml playbooks) |
| CI/CD | GitHub Actions (`.github/workflows/molecule-test.yml`) |
| Scope | VictoriaLogs cluster deployment, upgrade, disable, cleanup |

**4.1.7.2.2 Molecule Directory Structure**

Following the [omnia-artifactory automation](https://github.com/dell/omnia-artifactory/tree/automation/molecule) naming convention:

```
molecule/
├── victorialogs/                        # Primary VictoriaLogs test scenario
│   ├── molecule.yml                     # Scenario config: delegated driver, telemetry namespace
│   ├── create.yml                       # Pre-test: ensure K8s cluster, namespace, TLS certs exist
│   ├── converge.yml                     # Execute: deploy VictoriaLogs cluster (include telemetry role)
│   ├── tasks/
│   │   ├── test_deploy_victorialogs_cluster_success.yml
│   │   ├── test_deploy_victorialogs_idempotent.yml
│   │   ├── test_disable_victorialogs_no_manifests.yml
│   │   ├── test_cleanup_victorialogs_pods_deleted.yml
│   │   ├── test_cleanup_victorialogs_pvcs_retained.yml
│   │   ├── test_upgrade_victorialogs_rolling_update.yml
│   │   └── test_port_victorialogs_no_conflict.yml
│   ├── tests/
│   │   ├── test_victorialogs_pods_ready.py
│   │   ├── test_victorialogs_endpoints_reachable.py
│   │   ├── test_victorialogs_ingest_query.py
│   │   └── test_victorialogs_port_allocation.py
│   └── vars/
│       └── main.yml                     # Test-specific variables
```

**4.1.7.2.3 Molecule Configuration**

> *Implementation details: See Component Spec (LLD)*


**4.1.7.2.4 Key Test Cases (molecule/victorialogs/tasks/)**

Following the naming convention `test_<action>_<component>_<expected_result>.yml`:

| Task File | Description |
|-----------|-------------|
| `test_deploy_victorialogs_cluster_success.yml` | Fresh deploy — verify all pods ready |
| `test_deploy_victorialogs_idempotent.yml` | Run converge twice — zero changes on second run |
| `test_disable_victorialogs_no_manifests.yml` | Change collection type to kafka-only — no VictoriaLogs manifests |
| `test_cleanup_victorialogs_pods_deleted.yml` | Run cleanup — pods/services deleted |
| `test_cleanup_victorialogs_pvcs_retained.yml` | Run cleanup — PVCs preserved for re-enable |
| `test_upgrade_victorialogs_rolling_update.yml` | Upgrade with new images — rolling update, data preserved |
| `test_port_victorialogs_no_conflict.yml` | Verify port allocations — no overlap with VictoriaMetrics |

> *Implementation details: See Component Spec (LLD)*


**4.1.7.2.5 Test Matrix**

| Test Case | ID | Description | Key Assertions |
|-----------|----|-------------|----------------|
| `test_deploy_victorialogs_cluster_success` | MOL-001 | Fresh deploy of VictoriaLogs cluster | vlstorage 3/3, vlinsert 2/2, vlselect 2/2, VLAgent 1/1, health endpoints 200, log ingest+query works |
| `test_deploy_victorialogs_idempotent` | MOL-002 | Run converge twice | Second run reports zero changes |
| `test_disable_victorialogs_no_manifests` | MOL-003 | Change collection type to kafka-only | No VictoriaLogs manifests generated; no VictoriaLogs pods |
| `test_cleanup_victorialogs_pods_deleted` | MOL-004 | Run cleanup | Pods/services deleted; VictoriaMetrics unaffected; TLS secret preserved |
| `test_cleanup_victorialogs_pvcs_retained` | MOL-005 | Verify PVCs after cleanup | vlstorage PVCs still exist; VLAgent PVC preserved |
| `test_upgrade_victorialogs_rolling_update` | MOL-006 | Upgrade with new image versions | Rolling update; replica count preserved; PVC data preserved; endpoints functional |
| `test_port_victorialogs_no_conflict` | MOL-007 | Verify port allocations | Ports 9481/9491/9401/9402 exclusively used by VictoriaLogs; no overlap with VM ports 8400-8482 |

**4.1.7.2.6 CI/CD Integration**

> *Implementation details: See Component Spec (LLD)*


**4.1.7.2.7 Molecule Test Naming Convention**

Following the [omnia-artifactory automation](https://github.com/dell/omnia-artifactory/tree/automation/molecule) naming convention:

| Convention | Pattern | Example |
|------------|---------|---------|
| Scenario directory | `molecule/<feature>/` | `molecule/victorialogs/` |
| Task file name | `test_<action>_<component>_<expected_result>.yml` | `test_deploy_victorialogs_cluster_success.yml` |
| Test file name | `test_<component>_<what>.py` | `test_victorialogs_pods_ready.py` |
| Verify task name | `Verify <component> <condition>` | `Verify vlstorage StatefulSet is ready` |
| Assert message | `<component> should <expected>` | `vlstorage PVCs should be retained after cleanup` |

#### 4.1.8 Module API Sharing within Dell ISG Organizations

N/A

#### 4.1.9 New API Conformance within Dell ISG Organizations

N/A

#### 4.1.10 Unresolved Issues

| Issue | Description | Status |
|-------|-------------|--------|
| VLAgent configuration overlay mechanism | Downstream capabilities need a standardized mechanism to extend VLAgent base configuration with source-specific settings (relabel rules, external labels, dual-write destinations). Design for overlay/merge approach is pending. | Under review |
| Grafana/VMUI integration for log visualization | Dashboard provisioning is out of scope for this epic. Integration point definition for future visualization capability is pending. | Out of scope |
| Retention policy per-stream | VictoriaLogs currently supports a single global retention period. Per-stream retention requires upstream feature support. | Upstream dependency |
