# VLAgent & Ansible Task Orchestration Component Spec (LLD)

| | |
|---|---|
| **Parent Document** | VictoriaLog_Cluster_engineering_spec.md (HLD v0.7) |
| **Spec Version** | 1.0 |
| **Author(s)** | Derived from HLD by Engineering |
| **Date** | 2025-04-13 |
| **Status** | Draft |

---

## Purpose

This Low-Level Design (LLD) document provides the coding-level blueprint for **VLAgent log collection and forwarding** and **Ansible task orchestration** (deploy, teardown, upgrade). It covers:

1. **VLAgent** — log collection pipeline, scrape targets, `remoteWrite` configuration, and forwarding behavior
2. **Ansible Task Flows** — deploy, teardown, and upgrade task design with pre/post conditions
3. **Idempotency Strategy** — ensuring repeat runs produce no unintended changes

All design decisions reference the parent HLD (Sections 3.2, 3.3, 4.1.3.1, 4.1.3.2, 4.1.3.7, 4.1.3.8, 4.1.3.10) and existing codebase patterns (`victoria-operator-vmcluster.yaml.j2`, `victoria-operator-vmagent.yaml.j2`, `vars/main.yml`, `telemetry_config.yml`, `deploy_victoria_cluster.yml`).

**Out of scope for this document**: VLCluster component design (vlstorage sizing, vlinsert sharding, vlselect routing) — covered in `VL_cluster_component_spec.md`. Source-specific pipeline wiring (PowerScale syslog, VAST, PowerVault) — covered in downstream capability epics. Molecule test implementation — covered in HLD Section 4.1.7.2.

---

## Table of Contents

- 1 [Design Decision Summary](#1-design-decision-summary)
- 2 [VLAgent — Log Collection Pipeline](#2-vlagent--log-collection-pipeline)
  - 2.1 [Component Overview](#21-component-overview)
  - 2.2 [Scrape Targets and Syslog Receivers](#22-scrape-targets-and-syslog-receivers)
  - 2.3 [Pipeline Configuration](#23-pipeline-configuration)
  - 2.4 [remoteWrite Configuration (Forwarding to vlinsert)](#24-remotewrite-configuration-forwarding-to-vlinsert)
  - 2.5 [Forwarding Behavior](#25-forwarding-behavior)
  - 2.6 [Buffer and Retry Semantics](#26-buffer-and-retry-semantics)
  - 2.7 [Resource Allocation](#27-resource-allocation)
  - 2.8 [PVC Configuration (Buffer Storage)](#28-pvc-configuration-buffer-storage)
  - 2.9 [Service Exposure](#29-service-exposure)
  - 2.10 [Health Probes](#210-health-probes)
  - 2.11 [TLS Configuration](#211-tls-configuration)
  - 2.12 [VLAgent CR Template](#212-vlagent-cr-template)
  - 2.13 [VLAgent ConfigMap Template](#213-vlagent-configmap-template)
  - 2.14 [Ansible Variable Definition](#214-ansible-variable-definition)
  - 2.15 [User Configuration — telemetry_config.yml](#215-user-configuration--telemetry_configyml)
- 3 [Ansible Task Flow — Deploy](#3-ansible-task-flow--deploy)
  - 3.1 [Deploy Task: deploy_victorialogs_cluster.yml](#31-deploy-task-deploy_victorialogs_clusteryml)
  - 3.2 [Pre-conditions](#32-pre-conditions)
  - 3.3 [Task Sequence](#33-task-sequence)
  - 3.4 [Post-conditions](#34-post-conditions)
  - 3.5 [Manifest Generation Detail](#35-manifest-generation-detail)
  - 3.6 [Kustomization Integration](#36-kustomization-integration)
  - 3.7 [Endpoint Discovery Output](#37-endpoint-discovery-output)
  - 3.8 [Conditional Deployment Logic](#38-conditional-deployment-logic)
- 4 [Ansible Task Flow — Teardown](#4-ansible-task-flow--teardown)
  - 4.1 [Teardown Task: teardown_victorialogs_cluster.yml](#41-teardown-task-teardown_victorialogs_clusteryml)
  - 4.2 [Pre-conditions](#42-pre-conditions)
  - 4.3 [Task Sequence](#43-task-sequence)
  - 4.4 [Post-conditions](#44-post-conditions)
  - 4.5 [Cleanup Script Extension (cleanup_telemetry.sh)](#45-cleanup-script-extension-cleanup_telemetrysh)
  - 4.6 [Disable Log Source Pipelines (disable_log.yml)](#46-disable-log-source-pipelines-disable_logyml)
  - 4.7 [PVC Data Retention Policy](#47-pvc-data-retention-policy)
- 5 [Ansible Task Flow — Upgrade](#5-ansible-task-flow--upgrade)
  - 5.1 [Upgrade Task: apply_telemetry_on_upgrade.yml (VictoriaLogs block)](#51-upgrade-task-apply_telemetry_on_upgradeyml-victorialogs-block)
  - 5.2 [Pre-conditions](#52-pre-conditions)
  - 5.3 [Task Sequence](#53-task-sequence)
  - 5.4 [Post-conditions](#54-post-conditions)
  - 5.5 [Configuration Transformation (transform_telemetry_config.yml)](#55-configuration-transformation-transform_telemetry_configyml)
  - 5.6 [Upgrade Scenario Matrix](#56-upgrade-scenario-matrix)
- 6 [Idempotency Strategy](#6-idempotency-strategy)
  - 6.1 [Idempotency Principles](#61-idempotency-principles)
  - 6.2 [Idempotency by Task Category](#62-idempotency-by-task-category)
  - 6.3 [Operator Reconciliation Loop](#63-operator-reconciliation-loop)
  - 6.4 [Edge Cases and Guarantees](#64-edge-cases-and-guarantees)
- 7 [Error Handling](#7-error-handling)
  - 7.1 [Ansible Task Error Handling](#71-ansible-task-error-handling)
  - 7.2 [VLAgent Runtime Error Handling](#72-vlagent-runtime-error-handling)
  - 7.3 [Deployment Failure Recovery](#73-deployment-failure-recovery)
- 8 [Acceptance Criteria Traceability](#8-acceptance-criteria-traceability)

---

## 1 Design Decision Summary

| ID | Component | Decision | Default | Rationale |
|----|-----------|----------|---------|-----------|
| DD-A1 | VLAgent | Deployed as a single-replica Deployment via `VLAgent` CR managed by the VictoriaMetrics operator | 1 replica | Platform-managed log forwarding agent; single replica sufficient for syslog receiver; HA provided by PVC buffer persistence and pod restart |
| DD-A2 | VLAgent | Syslog receiver on port 514 (plaintext) and port 6514 (TLS) exposed via LoadBalancer | 514 TCP+UDP, 6514 TLS TCP | Standard syslog ports (RFC 3164/5424 for plaintext, RFC 5425 for TLS); LoadBalancer provides stable external IP for device configuration |
| DD-A3 | VLAgent | `remoteWrite` forwards logs to vlinsert via HTTPS JSON Lines on port 9481 | `https://vlinsert-victoria-logs-cluster.telemetry.svc.cluster.local:9481/insert/jsonline` | In-cluster TLS communication to vlinsert; JSON Lines is the primary VictoriaLogs ingestion format; CA cert validation from shared `victoria-tls-certs` secret |
| DD-A4 | VLAgent | 5 Gi PVC buffer at `/vlagent-data` for client-side buffering and retry | 5 Gi | Prevents log loss during vlinsert unavailability (pod restart, rolling update); VLAgent persists unsent logs to disk and retries on recovery |
| DD-A5 | VLAgent | Source-neutral base configuration — no source-specific relabel rules, external labels, or pipeline wiring | N/A | Platform provides the log forwarding infrastructure; downstream capabilities extend VLAgent configuration for source-specific pipelines (separate epics) |
| DD-T1 | Deploy | Operator-managed deployment via `kubectl apply -k` with generated CRs | N/A | Declarative, idempotent deployment; operator reconciles desired state; matches VictoriaMetrics deployment pattern |
| DD-T2 | Teardown | CR deletion triggers operator cleanup of underlying workloads; PVCs require manual cleanup | N/A | Operator manages workload lifecycle; PVC retention prevents accidental data loss |
| DD-T3 | Upgrade | Re-apply CRs with updated spec; operator performs rolling update; preserve replica count and PVC data | N/A | Non-disruptive upgrade; data preservation; matches iDRAC telemetry upgrade pattern |
| DD-T4 | Idempotency | All Ansible tasks use `kubectl apply` (not `create`), Jinja2 template rendering is deterministic, operator reconciliation is convergent | N/A | Repeated playbook runs produce identical cluster state; safe for automated re-runs and CI/CD pipelines |

---

## 2 VLAgent — Log Collection Pipeline

### 2.1 Component Overview

**Decision (DD-A1)**: VLAgent is deployed as a platform-managed log forwarding agent via the `VLAgent` CR.

| Property | Value |
|----------|-------|
| Kind | Deployment (operator-managed via `VLAgent` CR) |
| Name | `vlagent` |
| Replicas | 1 |
| Image | `victoriametrics/vlagent:<version>` (from `service_k8s.json`) |
| Operator CR | `VLAgent` (API: `operator.victoriametrics.com/v1beta1`) |
| Namespace | `telemetry` |
| Configuration | ConfigMap `vlagent-config` (manual manifest) + operator CR spec |
| Purpose | Platform-managed syslog receiver and HTTP log forwarder to vlinsert |

**Architectural role**: VLAgent sits between external log sources and vlinsert, providing:
1. **Syslog reception** — standard syslog listener for RFC 3164/5424 messages
2. **Protocol translation** — converts syslog to JSON Lines format
3. **HTTP forwarding** — delivers logs to vlinsert over HTTPS
4. **Client-side buffering** — PVC-backed buffer for retry during vlinsert unavailability

```
External Log Sources              VLAgent                          vlinsert
(syslog devices,                  (platform agent)                 (ingestion GW)
 future capabilities)
     |                               |                                |
     |-- syslog TCP/UDP :514 ------->|                                |
     |-- syslog TLS TCP :6514 ------>|                                |
     |                               |-- JSON Lines HTTP POST ------->|
     |                               |   (HTTPS :9481)                |
     |                               |   remoteWrite config           |
     |                               |                                |
     |                               |   [PVC buffer: /vlagent-data]  |
     |                               |   (retry on failure)           |
```

### 2.2 Scrape Targets and Syslog Receivers

**Decision (DD-A2)**: VLAgent exposes syslog receivers as platform-level scrape targets.

| Receiver | Port | Protocol | Format | Service Type | Description |
|----------|------|----------|--------|-------------|-------------|
| Syslog plaintext | 514 | TCP + UDP | RFC 3164/5424 | LoadBalancer (MetalLB) | Standard syslog listener; any device or application can send syslog messages to this port |
| Syslog TLS | 6514 | TLS TCP | RFC 5425 | LoadBalancer (MetalLB) | TLS-secured syslog listener; uses `victoria-tls-certs` for server certificate |
| Health | 8429 | HTTP | N/A | ClusterIP | Health check endpoint (`/health`); internal only |

**Scrape target design**:

VLAgent is **not** a pull-based scraper (unlike vmagent for metrics). VLAgent is a **push-based receiver** — external sources push syslog messages to VLAgent's listener ports. The term "scrape target" in the VLAgent context refers to the configured **receiver endpoints** that VLAgent listens on.

| Property | Value | Rationale |
|----------|-------|-----------|
| Listen address (syslog) | `0.0.0.0:514` | Bind to all interfaces; LoadBalancer routes external traffic to this port |
| Listen address (syslog TLS) | `0.0.0.0:6514` | Bind to all interfaces; TLS termination at VLAgent using shared certificates |
| Listen address (health) | `0.0.0.0:8429` | Standard VLAgent/vmagent health port |
| UDP support | Yes (port 514) | Many legacy syslog implementations use UDP; VLAgent supports both TCP and UDP on the same port |
| Max message size | VLAgent default (8 KB per RFC 5424) | Standard syslog message size limit; oversized messages are truncated |

**Source-neutral design (DD-A5)**:

The platform VLAgent base configuration defines **only** the receiver endpoints and forwarding destination. It does **not** define:
- Which devices or services send syslog to VLAgent
- Relabel rules for specific sources (e.g., `source: powerscale`)
- External labels for source identification
- Dual-write destinations (e.g., forwarding to both vlinsert and a secondary destination)
- Parsing or enrichment rules

These are the responsibility of downstream capabilities that extend VLAgent configuration.

### 2.3 Pipeline Configuration

**VLAgent log processing pipeline (platform base)**:

```
Stage 1: RECEIVE                Stage 2: PARSE                Stage 3: FORWARD
=================               ===============               =================
syslog TCP :514  ──┐            VLAgent internal               remoteWrite to
syslog UDP :514  ──┤──> parse   syslog-to-JSON    ──> buffer   vlinsert :9481
syslog TLS :6514 ──┘            conversion               ↓    (JSON Lines POST)
                                                    PVC buffer
                                                    /vlagent-data
                                                    (retry queue)
```

**Stage 1 — Receive**:
- VLAgent listens on configured ports for incoming syslog messages
- TCP connections are accepted concurrently (VLAgent uses goroutine-per-connection model)
- UDP datagrams are read from a single socket (standard UDP syslog behavior)
- TLS connections use the server certificate from `victoria-tls-certs`

**Stage 2 — Parse**:
- VLAgent parses incoming syslog messages according to RFC 3164 (BSD) or RFC 5424 (structured)
- Parsed fields are mapped to VictoriaLogs fields:

| Syslog Field | VictoriaLogs Field | Description |
|-------------|-------------------|-------------|
| MSG | `_msg` | Log message body |
| TIMESTAMP | `_time` | Event timestamp (RFC 3339 format) |
| HOSTNAME | `hostname` | Source hostname |
| APP-NAME | `app_name` | Application name |
| FACILITY | `facility` | Syslog facility code |
| SEVERITY | `severity` | Syslog severity level |
| PROCID | `proc_id` | Process ID |
| MSGID | `msg_id` | Message ID |
| STRUCTURED-DATA | (expanded as JSON fields) | RFC 5424 structured data elements |

- Output format: JSON Lines (NDJSON) — one JSON object per log entry per line

**Stage 3 — Forward**:
- Parsed JSON Lines are batched and sent to vlinsert via HTTP POST
- See Section 2.4 for `remoteWrite` configuration details
- See Section 2.6 for buffer and retry semantics

### 2.4 remoteWrite Configuration (Forwarding to vlinsert)

**Decision (DD-A3)**: VLAgent forwards logs to vlinsert via `remoteWrite` using JSON Lines over HTTPS.

```yaml
remoteWrite:
  url: "https://vlinsert-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local:9481/insert/jsonline"
  tls_config:
    ca_file: "/etc/victoria/certs/ca.crt"
    insecure_skip_verify: false
```

| Property | Value | Rationale |
|----------|-------|-----------|
| URL | `https://vlinsert-...svc.cluster.local:9481/insert/jsonline` | In-cluster FQDN of vlinsert service; JSON Lines endpoint is the primary VictoriaLogs ingestion format |
| Protocol | HTTPS (TLS) | Matches vlinsert TLS enforcement; CA cert validation ensures connection to legitimate vlinsert |
| CA file | `/etc/victoria/certs/ca.crt` | CA certificate from shared `victoria-tls-certs` secret; validates vlinsert's server certificate |
| `insecure_skip_verify` | `false` | Production setting; CA validation required for security |
| Ingestion path | `/insert/jsonline` | Primary VictoriaLogs ingestion endpoint; accepts NDJSON format |
| Query parameters | `_stream_fields=hostname,app_name` | Stream identification for vlinsert consistent-hash sharding; hostname and app_name provide natural log stream grouping |
| Batch size | VLAgent default (1 MB or 10,000 entries, whichever comes first) | Balances ingestion throughput with memory usage |
| Flush interval | VLAgent default (1 second) | Ensures logs are forwarded with low latency in normal operation |

**Full remoteWrite URL with stream fields**:
```
https://vlinsert-victoria-logs-cluster.telemetry.svc.cluster.local:9481/insert/jsonline?_stream_fields=hostname,app_name
```

### 2.5 Forwarding Behavior

| Behavior | Description |
|----------|-------------|
| Normal operation | VLAgent batches parsed log entries and sends HTTP POST to vlinsert every flush interval (1s default) or when batch size threshold is reached |
| vlinsert returns 200 | Batch acknowledged; VLAgent discards the batch from buffer and proceeds with next batch |
| vlinsert returns 4xx | Client error (malformed request); VLAgent logs the error; batch is discarded (no retry — indicates a format issue, not a transient failure) |
| vlinsert returns 5xx | Server error (vlinsert overloaded or vlstorage unavailable); VLAgent retries with exponential backoff; batch is persisted to PVC buffer |
| vlinsert unreachable | Connection refused (vlinsert pod restarting, rolling update); VLAgent persists batch to PVC buffer; retries with exponential backoff until vlinsert recovers |
| PVC buffer full | VLAgent drops oldest buffered entries to make room for new entries (FIFO eviction); logs a warning; new incoming syslog messages continue to be accepted |
| VLAgent pod restart | On restart, VLAgent reads unsent batches from PVC buffer (`/vlagent-data`) and retries forwarding before accepting new messages |

### 2.6 Buffer and Retry Semantics

**Decision (DD-A4)**: VLAgent uses a 5 Gi PVC buffer for client-side persistence.

| Property | Value | Rationale |
|----------|-------|-----------|
| Buffer path | `/vlagent-data` | PVC mount point for persistent buffer storage |
| Buffer size | 5 Gi (configurable) | Provides sufficient buffer for ~24-48 hours of log accumulation during vlinsert outage (at typical syslog rates of ~50-100 MB/hour) |
| Buffer type | Disk-backed WAL (write-ahead log) | VLAgent writes incoming data to disk before forwarding; survives pod restarts |
| Retry strategy | Exponential backoff | Initial: 1s, max: 60s, multiplier: 2x; prevents thundering herd on vlinsert recovery |
| Retry limit | Unlimited (retries until success or PVC eviction) | Ensures maximum delivery; eviction only when PVC is full |
| Ordering guarantee | Per-stream ordering preserved | Logs from the same syslog source maintain chronological order; cross-stream ordering is best-effort |

### 2.7 Resource Allocation

| Resource | Request | Limit | Rationale |
|----------|---------|-------|-----------|
| CPU | 50m | 250m | VLAgent is I/O-bound (syslog receive + HTTP forward); low CPU usage; matches HLD Section 4.1.5 resource table |
| Memory | 128 Mi | 512 Mi | In-memory batch buffers are bounded by batch size (1 MB default); disk-backed WAL handles overflow; low resident memory |

### 2.8 PVC Configuration (Buffer Storage)

| Property | Value | Rationale |
|----------|-------|-----------|
| Name | `vlagent-data` | Consistent naming with VLAgent data path |
| Size | `5 Gi` (configurable) | Default sufficient for moderate syslog volume; configurable for high-volume environments |
| Access mode | `ReadWriteOnce` | Single VLAgent pod has exclusive access |
| Storage class | Cluster default | Follows VLCluster pattern |
| Mount path | `/vlagent-data` | VLAgent buffer directory |
| Reclaim policy | Retain (PVC persists after Deployment deletion) | Prevents loss of buffered logs; manual cleanup required during teardown |
| Cleanup | `kubectl delete pvc -l app=vlagent -n telemetry` | Manual cleanup command; not auto-deleted during teardown |

### 2.9 Service Exposure

| Port | Service Type | Protocol | External | Rationale |
|------|-------------|----------|----------|-----------|
| 514 | LoadBalancer (MetalLB) | TCP + UDP | Yes | Stable external IP for syslog device configuration; standard syslog port |
| 6514 | LoadBalancer (MetalLB) | TLS TCP | Yes | TLS-secured syslog for environments requiring encrypted log transport |
| 8429 | ClusterIP | HTTP | No | Internal health check only; no external exposure needed |

**MetalLB detection** (for environments without MetalLB):
```yaml
{% if metalLB_deployed | default(false) %}
    serviceSpec:
      spec:
        type: LoadBalancer
{% else %}
    serviceSpec:
      spec:
        type: NodePort
{% endif %}
```

### 2.10 Health Probes

| Probe | Type | Port | Path | Delay | Period | Timeout |
|-------|------|------|------|-------|--------|---------|
| Liveness | HTTP GET | 8429 | `/health` | 30s | 30s | 5s |
| Readiness | HTTP GET | 8429 | `/health` | 5s | 10s | 5s |

**Rationale**: Port 8429 is the standard vlagent/vmagent health port. Liveness delay of 30s allows time for PVC buffer replay on restart. Readiness delay of 5s enables fast syslog traffic routing after pod start.

### 2.11 TLS Configuration

| Interface | TLS Mode | Certificate Source | Purpose |
|-----------|----------|-------------------|---------|
| Syslog TLS receiver (:6514) | Server TLS | `victoria-tls-certs` secret (`server.crt`, `server.key`) | TLS termination for incoming syslog-over-TLS connections (RFC 5425) |
| remoteWrite to vlinsert | Client TLS (CA validation) | `victoria-tls-certs` secret (`ca.crt`) | Validates vlinsert's server certificate when forwarding logs |
| Syslog plaintext receiver (:514) | None | N/A | Plaintext syslog for trusted internal networks; no TLS |
| Health endpoint (:8429) | None | N/A | Internal health check; no TLS needed for ClusterIP service |

**Volume mounts**:
```yaml
volumes:
  - name: victoria-tls-certs
    secret:
      secretName: victoria-tls-certs
      items:
        - key: tls.crt
          path: server.crt
        - key: tls.key
          path: server.key
        - key: ca.crt
          path: ca.crt
volumeMounts:
  - name: victoria-tls-certs
    mountPath: /etc/victoria/certs
    readOnly: true
```

### 2.12 VLAgent CR Template

**File**: `provision/roles/telemetry/templates/telemetry/victoria/victorialogs-operator-vlagent.yaml.j2`

```yaml
#  Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# VLAgent - VictoriaLogs log collection agent via operator
# Managed by victoria-metrics-operator (>= v0.59.0)

apiVersion: operator.victoriametrics.com/v1beta1
kind: VLAgent
metadata:
  name: vlagent
  namespace: {{ telemetry_namespace }}
spec:
  image:
    repository: {{ victoria_logs_cluster.vlagent.image.split(':')[0] }}
    tag: {{ victoria_logs_cluster.vlagent.image.split(':')[1] }}
    pullPolicy: IfNotPresent

  replicaCount: {{ victoria_logs_cluster.vlagent.replicas }}

  configSecret: vlagent-config

  resources:
    requests:
      memory: {{ victoria_logs_cluster.vlagent.resources.requests.memory }}
      cpu: {{ victoria_logs_cluster.vlagent.resources.requests.cpu }}
    limits:
      memory: {{ victoria_logs_cluster.vlagent.resources.limits.memory }}
      cpu: {{ victoria_logs_cluster.vlagent.resources.limits.cpu }}

  # PVC buffer for client-side log persistence
  storage:
    volumeClaimTemplate:
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: {{ victoria_logs_cluster.vlagent.pvc_size | default('5Gi') }}

{% if victoria_logs_cluster.tls_enabled %}
  volumes:
    - name: victoria-tls-certs
      secret:
        secretName: victoria-tls-certs
        items:
          - key: tls.crt
            path: server.crt
          - key: tls.key
            path: server.key
          - key: ca.crt
            path: ca.crt
  volumeMounts:
    - name: victoria-tls-certs
      mountPath: /etc/victoria/certs
      readOnly: true
{% endif %}

{% if metalLB_deployed | default(false) %}
  serviceSpec:
    spec:
      type: LoadBalancer
{% else %}
  serviceSpec:
    spec:
      type: NodePort
{% endif %}

  ports:
    - name: syslog
      port: 514
      targetPort: 514
      protocol: TCP
    - name: syslog-udp
      port: 514
      targetPort: 514
      protocol: UDP
    - name: syslog-tls
      port: 6514
      targetPort: 6514
      protocol: TCP
    - name: health
      port: 8429
      targetPort: 8429
      protocol: TCP
```

### 2.13 VLAgent ConfigMap Template

**File**: `provision/roles/telemetry/templates/telemetry/victoria/vlagent-config.yaml.j2`

```yaml
#  Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

apiVersion: v1
kind: ConfigMap
metadata:
  name: vlagent-config
  namespace: {{ telemetry_namespace }}
data:
  vlagent.yml: |
    # VLAgent platform base configuration
    # Source-neutral: no source-specific relabel rules or external labels
    # Downstream capabilities extend this configuration for specific log sources

    # Syslog receivers (platform-provided scrape targets)
    syslog:
      # Plaintext syslog receiver (RFC 3164/5424)
      listenAddr: "0.0.0.0:514"
      # TLS syslog receiver (RFC 5425)
      tlsListenAddr: "0.0.0.0:6514"
{% if victoria_logs_cluster.tls_enabled %}
      tlsCertFile: "/etc/victoria/certs/server.crt"
      tlsKeyFile: "/etc/victoria/certs/server.key"
{% endif %}

    # Forward parsed logs to vlinsert (JSON Lines over HTTPS)
    remoteWrite:
      url: "https://vlinsert-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local:9481/insert/jsonline?_stream_fields=hostname,app_name"
{% if victoria_logs_cluster.tls_enabled %}
      tls_config:
        ca_file: "/etc/victoria/certs/ca.crt"
        insecure_skip_verify: false
{% endif %}

    # Buffer configuration
    persistentQueue:
      dir: "/vlagent-data"
      maxPendingBytes: "5GiB"
```

**Note**: This is the platform base ConfigMap. Downstream capabilities overlay source-specific configuration (relabel rules, external labels, additional receivers) by extending or replacing this ConfigMap.

### 2.14 Ansible Variable Definition

Added to `provision/roles/telemetry/vars/main.yml` (within the `victoria_logs_cluster` block, parallel to vlstorage, vlinsert, vlselect):

```yaml
victoria_logs_cluster:
  tls_enabled: true

  # ... vlstorage, vlinsert, vlselect definitions (see VL_cluster_component_spec.md) ...

  # VLAgent: Platform-managed log forwarding agent
  vlagent:
    replicas: 1
    image: "{{ telemetry_images['victoriametrics/vlagent'] | default('victoriametrics/vlagent:v1.49.0') }}"
    pvc_size: "5Gi"
    resources:
      requests:
        memory: "128Mi"
        cpu: "50m"
      limits:
        memory: "512Mi"
        cpu: "250m"
```

#### Image Versions Reference

| Component | Image Key in `service_k8s.json` | Default Version | Purpose | License |
|-----------|--------------------------------|-----------------|---------|---------|
| VLAgent | `victoriametrics/vlagent` | v1.49.0 | Log collector/forwarder | Apache 2.0 |
| VictoriaLogs Cluster | `victoriametrics/victoria-logs` | v1.49.0 | vlstorage, vlinsert, vlselect | Apache 2.0 |
| Operator | `victoriametrics/operator` | v0.68.3 | Manages VLAgent and VLCluster CRs | Apache 2.0 |
| Operator Helm Chart | N/A | 0.59.3 | Operator deployment via Helm | Apache 2.0 |

**Note**: VLAgent CRD support requires operator >= v0.59.0. All images are sourced from `service_k8s.json` and pre-staged in local Pulp repository for air-gapped deployment.

### 2.15 User Configuration — telemetry_config.yml

No user-configurable VLAgent parameters are exposed in `telemetry_config.yml` for the platform base. VLAgent configuration is managed entirely through `vars/main.yml` defaults.

**Rationale**: VLAgent is platform infrastructure with fixed resource allocation. Source-specific configuration (syslog ports, receiver addresses) is managed by downstream capability epics that extend `telemetry_config.yml` with source-level parameters.

**Future extension point**: Downstream capabilities may add the following to `telemetry_config.yml`:
```yaml
# (Added by downstream capability epics, NOT by this platform epic)
# victoria_logs_configurations:
#   syslog_receiver_port: 514          # Plaintext syslog port
#   syslog_tls_receiver_port: 6514     # TLS syslog port
```

---

## 3 Ansible Task Flow — Deploy

### 3.1 Deploy Task: deploy_victorialogs_cluster.yml

**New task file**: `provision/roles/telemetry/tasks/deploy_victorialogs_cluster.yml`

This task generates and applies VictoriaLogs operator CRs. It is called from the main telemetry deployment flow when `'victoria' in telemetry_collection_type`.

### 3.2 Pre-conditions

| # | Pre-condition | Checked By | Failure Behavior |
|---|---------------|-----------|------------------|
| P1 | `'victoria' in telemetry_collection_type` | `generate_telemetry_deployments.yml` (conditional include) | Task file is not included; no VictoriaLogs manifests generated |
| P2 | Service Kubernetes cluster is accessible via `kubectl` | Existing playbook infrastructure | Playbook fails with connection error |
| P3 | `telemetry` namespace exists | Created by `telemetry_namespace_creation.yaml` (applied before CRs) | Created as part of deployment flow |
| P4 | `victoria-tls-certs` secret exists in `telemetry` namespace | VictoriaMetrics deployment or `gen_victoria_certs.sh` | Generated before VictoriaLogs deployment; VictoriaMetrics must deploy first (or concurrently) |
| P5 | VictoriaMetrics operator is installed (Helm chart) | `telemetry.sh.j2` installs operator Helm chart before CR application | Operator Helm install step precedes `kubectl apply -k` |
| P6 | Image versions exist in `service_k8s.json` | L2 Python validation (`common_validation.py`) | Validation fails with descriptive error before deployment |
| P7 | `victoria_logs_configurations.retention_period` is valid | L2 Python validation (`common_validation.py`) | Validation fails with descriptive error before deployment |
| P8 | `victoria_logs_configurations.storage_size` is valid PVC format | L2 Python validation (`common_validation.py`) | Validation fails with descriptive error before deployment |

#### 3.2.1 L2 Python Validation Details (common_validation.py)

When `'victoria' in telemetry_collection_type`, the following VictoriaLogs validations are performed:

| Validation | Input | Rule | Failure Behavior |
|-----------|-------|------|-----------------|
| Retention period format | `victoria_logs_configurations.retention_period` | Must be valid duration (e.g., `7d`, `30d`, `90d`) | Fail with descriptive error |
| Storage size format | `victoria_logs_configurations.storage_size` | Must be valid Kubernetes PVC size (e.g., `8Gi`, `50Gi`) | Fail with descriptive error |
| VLAgent image key exists | `victoriametrics/vlagent` in `service_k8s.json` | Image key must exist and resolve to a valid image | Fail with descriptive error |
| VictoriaLogs image key exists | `victoriametrics/victoria-logs` in `service_k8s.json` | Image key must exist and resolve to a valid image | Fail with descriptive error |
| Images staged in Pulp | All VictoriaLogs images | Images must be pre-staged in local Pulp repository | Fail with descriptive error |

**Validation is skipped when** `'victoria'` is NOT in `telemetry_collection_type`.

### 3.3 Task Sequence

```yaml
# deploy_victorialogs_cluster.yml — Pseudocode

# Step 1: Load configuration
- name: Load telemetry_config.yml
  include_vars:
    file: "{{ telemetry_config_file }}"
  # Loads victoria_logs_configurations (retention_period, storage_size)

# Step 2: Load image versions from service_k8s.json
- name: Set VictoriaLogs image facts
  set_fact:
    victoria_logs_image: "{{ telemetry_images['victoriametrics/victoria-logs'] }}"
    vlagent_image: "{{ telemetry_images['victoriametrics/vlagent'] }}"

# Step 3: Set cluster topology facts
- name: Set VictoriaLogs cluster facts
  set_fact:
    vlstorage_replicas: "{{ victoria_logs_cluster.vlstorage.replicas }}"
    vlinsert_replicas: "{{ victoria_logs_cluster.vlinsert.replicas }}"
    vlselect_replicas: "{{ victoria_logs_cluster.vlselect.replicas }}"
    vlagent_replicas: "{{ victoria_logs_cluster.vlagent.replicas }}"

# Step 4: Display cluster topology summary
- name: Display VictoriaLogs cluster topology
  debug:
    msg: |
      VictoriaLogs Cluster Topology:
        vlstorage: {{ vlstorage_replicas }} replicas (StatefulSet)
        vlinsert:  {{ vlinsert_replicas }} replicas (Deployment)
        vlselect:  {{ vlselect_replicas }} replicas (Deployment)
        VLAgent:   {{ vlagent_replicas }} replica (Deployment)
        Retention: {{ victoria_logs_configurations.retention_period }}
        Storage:   {{ victoria_logs_configurations.storage_size }} per vlstorage replica

# Step 5: Generate VLCluster CR from template
- name: Generate VLCluster operator CR
  template:
    src: telemetry/victoria/victorialogs-operator-vlcluster.yaml.j2
    dest: "{{ telemetry_deploy_dir }}/victorialogs-operator-vlcluster.yaml"
    mode: '0644'
  no_log: false

# Step 6: Generate VLAgent CR from template
- name: Generate VLAgent operator CR
  template:
    src: telemetry/victoria/victorialogs-operator-vlagent.yaml.j2
    dest: "{{ telemetry_deploy_dir }}/victorialogs-operator-vlagent.yaml"
    mode: '0644'
  no_log: false

# Step 7: Generate VLAgent ConfigMap from template
- name: Generate VLAgent ConfigMap
  template:
    src: telemetry/victoria/vlagent-config.yaml.j2
    dest: "{{ telemetry_deploy_dir }}/vlagent-config.yaml"
    mode: '0644'
  no_log: false

# Step 8: Apply via kustomization (batched with VictoriaMetrics CRs)
# This step is handled by telemetry.sh.j2:
#   kubectl apply -k {{ telemetry_deploy_dir }}/
# The kustomization.yaml includes both VMCluster and VLCluster CRs
```

**Task ordering within telemetry deployment**:
```
telemetry.sh.j2 execution order:
  1. kubectl apply -f telemetry_namespace_creation.yaml
  2. helm install victoria-metrics-operator <tarball>        # Operator for both VM and VL
  3. [Ansible generates all CR templates — VMCluster, VLCluster, VMAgent, VLAgent]
  4. kubectl apply -k deployments/                           # Single kustomize apply
     # Operator reconciles:
     #   VMCluster CR → vmstorage, vminsert, vmselect
     #   VLCluster CR → vlstorage, vlinsert, vlselect
     #   VMAgent CR   → vmagent
     #   VLAgent CR   → vlagent
```

### 3.4 Post-conditions

| # | Post-condition | Verification | Timeout |
|---|---------------|-------------|---------|
| Q1 | vlstorage StatefulSet is 3/3 READY | `kubectl get statefulset -l app=vlstorage -n telemetry` | 120s |
| Q2 | vlinsert Deployment is 2/2 READY | `kubectl get deploy -l app=vlinsert -n telemetry` | 120s |
| Q3 | vlselect Deployment is 2/2 READY | `kubectl get deploy -l app=vlselect -n telemetry` | 120s |
| Q4 | VLAgent Deployment is 1/1 READY | `kubectl get deploy -l app=vlagent -n telemetry` | 120s |
| Q5 | vlinsert LoadBalancer has external IP | `kubectl get svc vlinsert-victoria-logs-cluster -n telemetry` | MetalLB allocation |
| Q6 | vlselect LoadBalancer has external IP | `kubectl get svc vlselect-victoria-logs-cluster -n telemetry` | MetalLB allocation |
| Q7 | VLAgent LoadBalancer has external IP | `kubectl get svc vlagent -n telemetry` | MetalLB allocation |
| Q8 | Endpoint discovery output emitted | Ansible debug message with endpoints | Immediate |

### 3.5 Manifest Generation Detail

| Manifest | Template Source | Generated File | CR Kind | Purpose |
|----------|----------------|---------------|---------|---------|
| VLCluster CR | `victorialogs-operator-vlcluster.yaml.j2` | `victorialogs-operator-vlcluster.yaml` | `VLCluster` | Declares vlstorage, vlinsert, vlselect configuration |
| VLAgent CR | `victorialogs-operator-vlagent.yaml.j2` | `victorialogs-operator-vlagent.yaml` | `VLAgent` | Declares VLAgent deployment configuration |
| VLAgent ConfigMap | `vlagent-config.yaml.j2` | `vlagent-config.yaml` | `ConfigMap` | Syslog receiver and remoteWrite configuration |
| Kustomization | `kustomization.yaml.j2` | `kustomization.yaml` | `Kustomization` | Aggregates all CRs for `kubectl apply -k` |

### 3.6 Kustomization Integration

Extend `provision/roles/telemetry/templates/telemetry/kustomization.yaml.j2` (within the existing `{% if 'victoria' in types %}` block):

```yaml
{% if 'victoria' in types %}
  # Existing VictoriaMetrics resources
  - victoria-operator-vmcluster.yaml
  - victoria-operator-vmagent.yaml

  # VictoriaLogs Cluster Mode
  - victorialogs-operator-vlcluster.yaml
  - victorialogs-operator-vlagent.yaml
  - vlagent-config.yaml
{% endif %}
```

### 3.7 Endpoint Discovery Output

After deployment, emit endpoint information matching VictoriaMetrics output pattern:

```yaml
- name: Display VictoriaLogs endpoint discovery
  debug:
    msg: |
      ============================================================
      VictoriaLogs Cluster Endpoints:
      ============================================================
      vlinsert (log ingestion):
        In-cluster:  https://vlinsert-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local:9481
        External:    https://{{ vlinsert_external_ip }}:9481
        Endpoints:
          - /insert/jsonline    (JSON Lines ingestion)
          - /insert/syslog      (syslog RFC 5424 ingestion)
          - /insert/elasticsearch/_bulk  (ES bulk API)

      vlselect (log query):
        In-cluster:  https://vlselect-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local:9491
        External:    https://{{ vlselect_external_ip }}:9491
        Endpoints:
          - /select/logsql/query       (LogsQL query)
          - /select/logsql/hits        (hit counts)
          - /select/logsql/stats_query (statistics)
          - /select/logsql/tail        (live tail)

      VLAgent (syslog receiver):
        Syslog:      {{ vlagent_external_ip }}:514  (plaintext TCP+UDP)
        Syslog TLS:  {{ vlagent_external_ip }}:6514 (TLS TCP, RFC 5425)
      ============================================================
```

### 3.8 Conditional Deployment Logic

**In `generate_telemetry_deployments.yml`** (extend existing victoria block):

```yaml
# Existing VictoriaMetrics conditional block
- name: Generate VictoriaMetrics manifests
  include_tasks: deploy_victoria_cluster.yml
  when: "'victoria' in telemetry_collection_types"

# NEW: VictoriaLogs conditional block (same gate)
- name: Generate VictoriaLogs manifests
  include_tasks: deploy_victorialogs_cluster.yml
  when: "'victoria' in telemetry_collection_types"
```

**When `'victoria'` is NOT in `telemetry_collection_type`**:
- `deploy_victorialogs_cluster.yml` is not included
- No VictoriaLogs manifests are generated
- No VLCluster or VLAgent CRs are applied
- Existing VictoriaLogs resources (if previously deployed) remain until explicit cleanup

#### 3.8.1 Deployment Gate Design

VictoriaLogs deployment uses the **same deployment gate as VictoriaMetrics**: the presence of `'victoria'` in `telemetry_collection_type`. VictoriaMetrics and VictoriaLogs are always co-deployed — there is no scenario where one is deployed without the other.

#### 3.8.2 Validation and Messaging When Disabled

When `'victoria'` is NOT in `telemetry_collection_type`:

| Component | Behavior |
|-----------|----------|
| L2 Python Validation | Skips VictoriaLogs-specific validation (retention period, storage size, image versions) |
| Ansible Deployment | Displays informational message; skips all VictoriaLogs manifest generation |
| Endpoint Discovery | VictoriaLogs endpoints are not emitted in the discovery output |

---

## 4 Ansible Task Flow — Teardown

### 4.1 Teardown Task: teardown_victorialogs_cluster.yml

**New task file**: `provision/roles/telemetry/tasks/teardown_victorialogs_cluster.yml`

### 4.2 Pre-conditions

| # | Pre-condition | Checked By | Failure Behavior |
|---|---------------|-----------|------------------|
| P1 | Service Kubernetes cluster is accessible | Existing playbook infrastructure | Task fails with connection error |
| P2 | `telemetry` namespace exists | `kubectl get namespace` | Skip teardown if namespace doesn't exist (nothing to tear down) |

### 4.3 Task Sequence

```yaml
# teardown_victorialogs_cluster.yml — Pseudocode

# Step 1: Check if VLCluster CR exists
- name: Check for VLCluster CR
  command: kubectl get vlcluster victoria-logs-cluster -n {{ telemetry_namespace }} --ignore-not-found
  register: vlcluster_exists
  changed_when: false

# Step 2: Delete VLCluster CR (operator removes vlstorage, vlinsert, vlselect workloads)
- name: Delete VLCluster CR
  command: kubectl delete vlcluster victoria-logs-cluster -n {{ telemetry_namespace }} --timeout=120s
  when: vlcluster_exists.stdout | length > 0
  ignore_errors: true

# Step 3: Check if VLAgent CR exists
- name: Check for VLAgent CR
  command: kubectl get vlagent vlagent -n {{ telemetry_namespace }} --ignore-not-found
  register: vlagent_exists
  changed_when: false

# Step 4: Delete VLAgent CR (operator removes VLAgent Deployment)
- name: Delete VLAgent CR
  command: kubectl delete vlagent vlagent -n {{ telemetry_namespace }} --timeout=120s
  when: vlagent_exists.stdout | length > 0
  ignore_errors: true

# Step 5: Delete VLAgent ConfigMap
- name: Delete VLAgent ConfigMap
  command: kubectl delete configmap vlagent-config -n {{ telemetry_namespace }} --ignore-not-found
  changed_when: false

# Step 6: Wait for workload removal
- name: Wait for VictoriaLogs pods to terminate
  command: kubectl wait --for=delete pod -l app.kubernetes.io/instance=victoria-logs-cluster -n {{ telemetry_namespace }} --timeout=120s
  ignore_errors: true

# Step 7: Display PVC cleanup guidance
- name: Display PVC cleanup notice
  debug:
    msg: |
      VictoriaLogs workloads have been removed.
      PVCs are NOT automatically deleted. To remove log data:
        kubectl delete pvc -l app=vlstorage -n {{ telemetry_namespace }}
        kubectl delete pvc -l app=vlagent -n {{ telemetry_namespace }}
      WARNING: Deleting PVCs permanently removes all stored log data.
```

### 4.4 Post-conditions

| # | Post-condition | Verification |
|---|---------------|-------------|
| Q1 | VLCluster CR deleted | `kubectl get vlcluster -n telemetry` returns empty |
| Q2 | VLAgent CR deleted | `kubectl get vlagent -n telemetry` returns empty |
| Q3 | VLAgent ConfigMap deleted | `kubectl get configmap vlagent-config -n telemetry` returns not found |
| Q4 | All VictoriaLogs pods terminated | `kubectl get pods -l app.kubernetes.io/instance=victoria-logs-cluster -n telemetry` returns empty |
| Q5 | VictoriaMetrics pods unaffected | `kubectl get pods -l app.kubernetes.io/instance=victoria-metrics-cluster -n telemetry` shows all READY |
| Q6 | Kafka pods unaffected | `kubectl get pods -n telemetry -l strimzi.io/kind=Kafka` shows all READY |
| Q7 | `victoria-tls-certs` secret preserved | Secret still exists (shared with VictoriaMetrics) |
| Q8 | vlstorage PVCs preserved | PVCs exist but are unbound (require manual cleanup) |
| Q9 | VLAgent PVC preserved | PVC exists but is unbound (requires manual cleanup) |

### 4.5 Cleanup Script Extension (cleanup_telemetry.sh)

Extend `provision/roles/telemetry/templates/telemetry/cleanup_telemetry.sh.j2` with `victorialogs` argument:

**Updated usage**:
```bash
# Usage: ./cleanup_telemetry.sh [kafka] [ldms] [idrac] [victoria] [victorialogs] [all]
```

**Argument parsing extension**:
```bash
CLEAN_VICTORIALOGS=false

for arg in "$@"; do
    case "$arg" in
        victorialogs) CLEAN_VICTORIALOGS=true ;;
        all)
            CLEAN_KAFKA=true
            CLEAN_LDMS=true
            CLEAN_IDRAC=true
            CLEAN_VICTORIA=true
            CLEAN_VICTORIALOGS=true
            ;;
    esac
done
```

**VictoriaLogs cleanup steps** (added after existing Victoria cleanup):
```bash
if [ "$CLEAN_VICTORIALOGS" = true ]; then
    echo "=== Cleaning up VictoriaLogs ==="

    # Delete VLCluster CR (operator removes underlying workloads)
    echo "Deleting VLCluster CR..."
    kubectl delete vlcluster victoria-logs-cluster -n {{ telemetry_namespace }} --timeout=120s 2>/dev/null || true

    # Delete VLAgent CR
    echo "Deleting VLAgent CR..."
    kubectl delete vlagent vlagent -n {{ telemetry_namespace }} --timeout=120s 2>/dev/null || true

    # Delete VLAgent ConfigMap
    echo "Deleting VLAgent ConfigMap..."
    kubectl delete configmap vlagent-config -n {{ telemetry_namespace }} 2>/dev/null || true

    # Wait for pods to terminate
    echo "Waiting for VictoriaLogs pods to terminate..."
    kubectl wait --for=delete pod -l app.kubernetes.io/instance=victoria-logs-cluster -n {{ telemetry_namespace }} --timeout=120s 2>/dev/null || true

    echo "VictoriaLogs cleanup complete."
    echo "NOTE: PVCs are NOT deleted. To remove log data:"
    echo "  kubectl delete pvc -l app=vlstorage -n {{ telemetry_namespace }}"
    echo "  kubectl delete pvc -l app=vlagent -n {{ telemetry_namespace }}"
fi
```

**PVC cleanup** (added to existing PVC cleanup step):
```bash
if [ "$CLEAN_VICTORIALOGS" = true ]; then
    echo "Deleting VictoriaLogs PVCs..."
    kubectl delete pvc -l app=vlstorage -n {{ telemetry_namespace }} 2>/dev/null || true
    kubectl delete pvc -l app=vlagent -n {{ telemetry_namespace }} 2>/dev/null || true
fi
```

**Force delete** (added to existing force delete step):
```bash
if [ "$CLEAN_VICTORIALOGS" = true ]; then
    echo "Force deleting stuck VictoriaLogs pods..."
    kubectl delete pod -l app.kubernetes.io/instance=victoria-logs-cluster -n {{ telemetry_namespace }} --force --grace-period=0 2>/dev/null || true
fi
```

**Remaining resource check** (added to existing check step):
```bash
if [ "$CLEAN_VICTORIALOGS" = true ]; then
    echo "Checking remaining VictoriaLogs resources..."
    kubectl get all -l app.kubernetes.io/instance=victoria-logs-cluster -n {{ telemetry_namespace }} 2>/dev/null
    kubectl get pvc -l app=vlstorage -n {{ telemetry_namespace }} 2>/dev/null
    kubectl get pvc -l app=vlagent -n {{ telemetry_namespace }} 2>/dev/null
fi
```

#### 4.5.1 Cleanup Ordering and Dependencies

VictoriaLogs cleanup is **independent** of all other telemetry components:

| Cleanup Scenario | VictoriaMetrics | Kafka | iDRAC | VictoriaLogs | Effect |
|-----------------|-----------------|-------|-------|--------------|--------|
| `./cleanup_telemetry.sh victorialogs` | Untouched | Untouched | Untouched | Removed | Only VictoriaLogs cluster and VLAgent removed |
| `./cleanup_telemetry.sh victoriametrics` | Removed | Untouched | Untouched | Untouched | Only VictoriaMetrics removed; VictoriaLogs continues operating |
| `./cleanup_telemetry.sh victoriametrics victorialogs` | Removed | Untouched | Untouched | Removed | Both metrics and logs stacks removed |
| `./cleanup_telemetry.sh all` | Removed | Removed | Removed | Removed | Full telemetry cleanup |

**Shared resource handling**:
- `victoria-tls-certs` secret: **NOT deleted** during `victorialogs` cleanup. This secret is shared with VictoriaMetrics and is only deleted during `victoriametrics` cleanup.
- `telemetry` namespace: **NOT deleted** during `victorialogs` cleanup. Namespace is shared and only deleted when all telemetry components are cleaned up.

**Cleanup step ordering** (within `victorialogs` cleanup):
1. Delete VLCluster CR (operator removes vlstorage, vlinsert, vlselect workloads)
2. Delete VLAgent CR (operator removes VLAgent Deployment)
3. Delete VLAgent ConfigMap
4. Wait for pods to terminate
5. (Optional) Delete PVCs if explicitly requested via cleanup script

### 4.6 Disable Log Source Pipelines (disable_log.yml)

**New playbook**: `disable_log.yml`

A dedicated playbook for selective disabling of log source pipelines without tearing down the VictoriaLogs cluster.

**Usage**:
```bash
ansible-playbook disable_log.yml --tags powerscale    # Disable PowerScale syslog pipeline
ansible-playbook disable_log.yml --tags vast           # Disable VAST log pipeline
ansible-playbook disable_log.yml --tags powervault     # Disable PowerVault log pipeline
ansible-playbook disable_log.yml --tags all            # Disable all log source pipelines
ansible-playbook disable_log.yml                       # Same as --tags all
```

**Design principle**: `disable_log.yml` removes only source-specific log pipelines (VLAgent configurations, relabel rules, syslog receivers wired by downstream capabilities). The VictoriaLogs cluster (vlstorage, vlinsert, vlselect) and VLAgent base platform instance continue running.

| Tag | Components Removed | VictoriaLogs Cluster | VLAgent Platform Base |
|-----|-------------------|---------------------|----------------------|
| *(no tags)* | All source-specific pipelines | Keeps running | Keeps running |
| `powerscale` | PowerScale VLAgent syslog pipeline, source ConfigMap, source service | Keeps running | Keeps running |
| `vast` | VAST log forwarding pipeline | Keeps running | Keeps running |
| `powervault` | PowerVault log forwarding pipeline | Keeps running | Keeps running |
| `all` | All of the above | Keeps running | Keeps running |

**Task sequence** (per source tag):
```yaml
# disable_log.yml — PowerScale tag example

- name: Disable PowerScale syslog pipeline
  tags: [powerscale]
  block:
    - name: Delete PowerScale VLAgent source ConfigMap overlay
      command: kubectl delete configmap vlagent-powerscale-config -n {{ telemetry_namespace }} --ignore-not-found
      changed_when: false

    - name: Delete PowerScale VLAgent source service
      command: kubectl delete svc vlagent-powerscale -n {{ telemetry_namespace }} --ignore-not-found
      changed_when: false

    - name: Display PowerScale pipeline disabled
      debug:
        msg: "PowerScale syslog pipeline disabled. VictoriaLogs cluster continues running."
```

**PVC handling**: PVCs are preserved. Historical logs remain queryable via vlselect after disabling a log source pipeline.

#### 4.6.1 Design Principle: Pipelines vs Cluster

`disable_log.yml` is designed to disable **log source pipelines** (source-specific VLAgent configurations) WITHOUT tearing down the VictoriaLogs cluster itself.

| Action | VictoriaLogs Cluster | VLAgent Base Instance | Previously Ingested Logs | PVCs |
|--------|---------------------|----------------------|--------------------------|------|
| `disable_log.yml` | Keeps running | Keeps running | Remain queryable via vlselect | Preserved |
| `cleanup_telemetry.sh victorialogs` | Removed entirely | Removed entirely | Inaccessible (PVCs require manual cleanup) | Require explicit deletion |

This design allows selective disabling of log sources without disrupting the logging platform.

### 4.7 PVC Data Retention Policy

| Resource | Auto-deleted on teardown | Auto-deleted on disable_log | Manual Cleanup Command |
|----------|-------------------------|-----------------------------|----------------------|
| vlstorage StatefulSet | Yes (via CR deletion) | No (cluster keeps running) | N/A |
| vlinsert Deployment | Yes (via CR deletion) | No (cluster keeps running) | N/A |
| vlselect Deployment | Yes (via CR deletion) | No (cluster keeps running) | N/A |
| VLAgent Deployment | Yes (via CR deletion) | No (platform agent keeps running) | N/A |
| vlstorage PVCs (log data) | **No** — requires explicit cleanup | No | `kubectl delete pvc -l app=vlstorage -n telemetry` |
| VLAgent PVC (buffer) | **No** — requires explicit cleanup | No | `kubectl delete pvc -l app=vlagent -n telemetry` |
| VLAgent ConfigMap | Yes (teardown) | Only source-specific overlays | N/A |

**Rationale**: PVCs contain log data that may be needed for audit or compliance. Automatic deletion during teardown could cause unintended data loss. PVCs are deleted only via the cleanup script when explicitly invoked with the `victorialogs` argument.

---

## 5 Ansible Task Flow — Upgrade

### 5.1 Upgrade Task: apply_telemetry_on_upgrade.yml (VictoriaLogs block)

Extends the existing `apply_telemetry_on_upgrade.yml` with a VictoriaLogs upgrade block (appended after iDRAC and LDMS upgrade blocks).

### 5.2 Pre-conditions

| # | Pre-condition | Checked By | Failure Behavior |
|---|---------------|-----------|------------------|
| P1 | `upgrade_enabled: true` | `oim_metadata.upgrade_backup_dir` is defined and non-empty | Upgrade block is skipped |
| P2 | `'victoria' in telemetry_collection_type` | Conditional check in `apply_telemetry_on_upgrade.yml` | VictoriaLogs upgrade block is skipped |
| P3 | Backup `telemetry_config.yml` exists | `transform_telemetry_config.yml` reads backup | Fails with descriptive error |
| P4 | VictoriaMetrics operator is installed | Helm chart installed during standard deployment flow | Operator manages rolling update |

### 5.3 Task Sequence

```yaml
# apply_telemetry_on_upgrade.yml — VictoriaLogs upgrade block (pseudocode)

# Appended after existing iDRAC and LDMS upgrade blocks

- name: Upgrade VictoriaLogs cluster
  when:
    - upgrade_enabled | bool
    - "'victoria' in telemetry_collection_types"
  block:

    # Step 1: Check if VLCluster CR exists (determines upgrade vs fresh deploy)
    - name: Check for existing VLCluster CR
      command: kubectl get vlcluster victoria-logs-cluster -n {{ telemetry_namespace }} --ignore-not-found
      register: vlcluster_upgrade_exists
      changed_when: false

    # Step 2: If VLCluster exists — preserve vlstorage replica count
    - name: Get current vlstorage replica count
      command: >
        kubectl get statefulset -l app=vlstorage -n {{ telemetry_namespace }}
        -o jsonpath='{.items[0].spec.replicas}'
      register: current_vlstorage_replicas
      when: vlcluster_upgrade_exists.stdout | length > 0
      changed_when: false

    - name: Set vlstorage replica count fact (preserve on upgrade)
      set_fact:
        vlstorage_upgrade_replicas: "{{ current_vlstorage_replicas.stdout | default(victoria_logs_cluster.vlstorage.replicas) }}"

    # Step 3: Re-generate CRs with updated images and preserved state
    - name: Generate updated VLCluster CR
      template:
        src: telemetry/victoria/victorialogs-operator-vlcluster.yaml.j2
        dest: "{{ telemetry_deploy_dir }}/victorialogs-operator-vlcluster.yaml"
        mode: '0644'

    - name: Generate updated VLAgent CR
      template:
        src: telemetry/victoria/victorialogs-operator-vlagent.yaml.j2
        dest: "{{ telemetry_deploy_dir }}/victorialogs-operator-vlagent.yaml"
        mode: '0644'

    - name: Generate updated VLAgent ConfigMap
      template:
        src: telemetry/victoria/vlagent-config.yaml.j2
        dest: "{{ telemetry_deploy_dir }}/vlagent-config.yaml"
        mode: '0644'

    # Step 4: Apply updated CRs
    - name: Apply updated VictoriaLogs CRs
      command: kubectl apply -k {{ telemetry_deploy_dir }}/
      register: vlcluster_apply_result
      changed_when: "'configured' in vlcluster_apply_result.stdout or 'created' in vlcluster_apply_result.stdout"

    # Step 5: Wait for rolling update to complete
    - name: Wait for vlstorage rollout
      command: kubectl rollout status statefulset -l app=vlstorage -n {{ telemetry_namespace }} --timeout=120s

    - name: Wait for vlinsert rollout
      command: kubectl rollout status deployment -l app=vlinsert -n {{ telemetry_namespace }} --timeout=120s

    - name: Wait for vlselect rollout
      command: kubectl rollout status deployment -l app=vlselect -n {{ telemetry_namespace }} --timeout=120s

    - name: Wait for VLAgent rollout
      command: kubectl rollout status deployment -l app=vlagent -n {{ telemetry_namespace }} --timeout=120s

    # Step 6: Verify health post-upgrade
    - name: Verify vlinsert health post-upgrade
      uri:
        url: "https://{{ vlinsert_service_ip }}:9481/health"
        validate_certs: false
        status_code: 200
      retries: 5
      delay: 10

    - name: Display VictoriaLogs upgrade complete
      debug:
        msg: "VictoriaLogs cluster upgrade complete. All components are healthy."
```

### 5.4 Post-conditions

| # | Post-condition | Verification | Timeout |
|---|---------------|-------------|---------|
| Q1 | vlstorage StatefulSet running with preserved replica count | `kubectl get statefulset -l app=vlstorage` | 120s |
| Q2 | vlstorage pods running with updated image | `kubectl get pods -l app=vlstorage -o jsonpath='{.items[*].spec.containers[0].image}'` | N/A |
| Q3 | vlinsert Deployment running with updated image | `kubectl get deploy -l app=vlinsert -o jsonpath='{.items[0].spec.template.spec.containers[0].image}'` | 120s |
| Q4 | vlselect Deployment running with updated image | Same as vlinsert | 120s |
| Q5 | VLAgent Deployment running with updated image | Same pattern | 120s |
| Q6 | PVC data preserved (no data loss) | Query previously ingested logs via vlselect | N/A |
| Q7 | Endpoints functional (health returns 200) | `curl -k https://<ip>:9481/health` and `:9491/health` | 50s (5 retries x 10s) |

### 5.5 Configuration Transformation (transform_telemetry_config.yml)

Extend `transform_telemetry_config.yml` to preserve VictoriaLogs configuration across Omnia version upgrades:

```yaml
# transform_telemetry_config.yml — VictoriaLogs extension

# Extract VictoriaLogs configuration from backup telemetry_config.yml
- name: Extract VictoriaLogs retention period from backup
  set_fact:
    backup_victoria_logs_retention: "{{ backup_telemetry_config.victoria_logs_configurations.retention_period | default('30d') }}"

- name: Extract VictoriaLogs storage size from backup
  set_fact:
    backup_victoria_logs_storage: "{{ backup_telemetry_config.victoria_logs_configurations.storage_size | default('8Gi') }}"

# These facts are then injected into the telemetry_config.j2 template
# to render the new telemetry_config.yml with preserved values
```

**Template extension** (`telemetry_config.j2`):
```yaml
# ... existing victoria_metrics_configurations block ...

victoria_logs_configurations:
  retention_period: "{{ backup_victoria_logs_retention | default('30d') }}"
  storage_size: "{{ backup_victoria_logs_storage | default('8Gi') }}"
```

#### 5.5.1 Backup Configuration Reading

During an Omnia upgrade, the `transform_telemetry_config.yml` task reads the backup `telemetry_config.yml` from `oim_metadata.upgrade_backup_dir`:

```yaml
- name: Read backup telemetry_config.yml
  include_vars:
    file: "{{ oim_metadata.upgrade_backup_dir }}/telemetry_config.yml"
    name: backup_telemetry_config
```

**Backup location**: `{{ oim_metadata.upgrade_backup_dir }}/telemetry_config.yml`

The backup config contains the previous version's `victoria_logs_configurations` section (if VictoriaLogs was deployed in the previous version). Default values (`30d`, `8Gi`) ensure graceful handling when upgrading from a version that did not include VictoriaLogs.

### 5.6 Upgrade Scenario Matrix

| # | Scenario | `idrac_telemetry_support` | `collection_type` includes `victoria` | VictoriaLogs Action |
|---|----------|--------------------------|---------------------------------------|---------------------|
| U1 | Full telemetry (typical) | `true` | Yes | Deploy/upgrade VictoriaLogs cluster; TLS certs shared; rolling update if image changed |
| U2 | Kafka-only collection | `true` | No | VictoriaLogs NOT deployed; upgrade block skipped |
| U3 | Telemetry previously disabled | `false` → `true` | Yes | Fresh deploy of VictoriaLogs (namespace may not exist; create it) |
| U4 | Collection type added victoria | `true` | Yes (was `kafka`, now `victoria,kafka`) | Fresh deploy; no prior VictoriaLogs data |
| U5 | Collection type removed victoria | `true` | No (was `victoria,kafka`, now `kafka`) | VictoriaLogs deployment skipped; existing resources remain until cleanup |
| U6 | Existing VictoriaLogs | `true` | Yes | Upgrade via CR re-apply; operator performs rolling update; replica count and PVCs preserved |

**Scenario U1 — Full Telemetry Upgrade (typical)**:
```
Upgrade playbook
    ├── Standard telemetry deployment (re-generate + apply manifests)
    │   ├── VictoriaMetrics CRs regenerated with updated images
    │   ├── VictoriaLogs CRs regenerated with updated images
    │   └── kubectl apply -k (operator reconciles both VM and VL)
    └── apply_telemetry_on_upgrade.yml
        ├── iDRAC telemetry upgrade (existing)
        ├── LDMS upgrade (existing)
        └── VictoriaLogs upgrade block
            ├── Preserve vlstorage replica count
            ├── Re-apply CRs
            ├── Wait for rolling update
            └── Verify health
```

**Scenario U3 — Fresh Deploy During Upgrade**:
```
Upgrade playbook (telemetry was previously disabled)
    ├── Create telemetry namespace (if not exists)
    ├── Generate TLS certificates (gen_victoria_certs.sh)
    ├── Install operator Helm chart
    ├── Generate VictoriaMetrics + VictoriaLogs CRs
    ├── kubectl apply -k (fresh deploy)
    └── apply_telemetry_on_upgrade.yml
        └── VictoriaLogs upgrade block
            ├── VLCluster CR not found → skip replica preservation
            └── Fresh deploy behavior (operator creates new workloads)
```

---

## 6 Idempotency Strategy

### 6.1 Idempotency Principles

**Decision (DD-T4)**: All deployment, teardown, and upgrade operations are idempotent — repeated execution produces the same result as a single execution.

| Principle | Implementation | Verification |
|-----------|---------------|-------------|
| Declarative desired state | Operator CRs define desired state; operator reconciles to match | Re-running `kubectl apply -k` with unchanged CRs produces zero changes |
| `kubectl apply` (not `create`) | All CR application uses `kubectl apply` which updates existing resources or creates if missing | `create` would fail on second run; `apply` succeeds idempotently |
| Deterministic template rendering | Jinja2 templates produce identical output given identical inputs | Same `telemetry_config.yml` + `vars/main.yml` → same manifest output |
| Operator convergent reconciliation | Operator watches CR spec; if actual state matches desired state, no action taken | Operator reconciliation loop is a no-op when spec unchanged |
| `ignore_errors` on deletion | Teardown tasks use `--ignore-not-found` or `ignore_errors: true` | Deleting non-existent resources is a no-op, not an error |
| `changed_when` on read-only tasks | `kubectl get` tasks use `changed_when: false` | Ansible does not report spurious changes for read-only operations |

### 6.2 Idempotency by Task Category

| Category | Task | Idempotent Mechanism | Evidence |
|----------|------|---------------------|----------|
| **Deploy** | Generate VLCluster CR template | Jinja2 deterministic rendering; `template` module reports `changed` only if file content differs | Second run: `ok` (not `changed`) if inputs unchanged |
| **Deploy** | Generate VLAgent CR template | Same as above | Same as above |
| **Deploy** | `kubectl apply -k` | `apply` performs 3-way merge; unchanged resources report `unchanged` | `kubectl apply` output: `victorialogs-operator-vlcluster.yaml unchanged` |
| **Deploy** | Operator reconciliation | Operator compares CR spec to actual workload spec; no action if matching | Operator logs: `no changes detected for VLCluster victoria-logs-cluster` |
| **Teardown** | Delete VLCluster CR | `--ignore-not-found` flag; second deletion is a no-op | Second run: no error, resource already absent |
| **Teardown** | Delete VLAgent CR | Same as above | Same as above |
| **Teardown** | Delete ConfigMap | `--ignore-not-found` flag | Same as above |
| **Upgrade** | Re-apply CRs with updated spec | `kubectl apply` updates only changed fields; operator performs rolling update only if spec changed | Image version changed → rolling update; nothing changed → no-op |
| **Upgrade** | Preserve replica count | `set_fact` reads current state; template uses preserved value; re-apply is no-op if replica count unchanged | Replica count preserved across upgrade cycles |

### 6.3 Operator Reconciliation Loop

The VictoriaMetrics operator runs a continuous reconciliation loop:

```
Operator Reconciliation (every 30s or on CR change)
    │
    ├── Read VLCluster CR desired state
    │   ├── vlstorage: 3 replicas, image v1.49.0, 8Gi PVC, 30d retention
    │   ├── vlinsert: 2 replicas, image v1.49.0, LoadBalancer
    │   └── vlselect: 2 replicas, image v1.49.0, LoadBalancer
    │
    ├── Read actual cluster state
    │   ├── vlstorage StatefulSet: 3 replicas, image v1.49.0, 8Gi PVC
    │   ├── vlinsert Deployment: 2 replicas, image v1.49.0
    │   └── vlselect Deployment: 2 replicas, image v1.49.0
    │
    ├── Compare desired vs actual
    │   ├── Match → NO ACTION (idempotent)
    │   └── Mismatch → RECONCILE (rolling update, scale, etc.)
    │
    └── Update CR status
```

**Key guarantee**: The operator ensures eventual consistency between the CR spec and the actual cluster state. Even if a pod is manually deleted, the operator (via the underlying StatefulSet/Deployment controller) recreates it to match the desired state.

### 6.4 Edge Cases and Guarantees

| Edge Case | Behavior | Idempotent |
|-----------|----------|------------|
| Playbook run during operator reconciliation | `kubectl apply` succeeds; operator finishes current reconciliation then processes any new changes | Yes |
| Playbook run during rolling update | `kubectl apply` succeeds (no-op if spec unchanged); operator continues rolling update | Yes |
| Playbook run after partial failure (some pods not ready) | `kubectl apply` re-applies CRs (no-op); operator continues reconciliation to reach desired state | Yes |
| Node failure during deploy | Operator reschedules pods on available nodes; `preferred` anti-affinity allows co-location | Yes |
| Network partition during `kubectl apply` | `kubectl apply` fails; next playbook run succeeds (CRs are applied fresh) | Yes (on retry) |
| Concurrent playbook runs | `kubectl apply` is serialized by API server; last-write-wins semantics; deterministic templates ensure same output | Yes (eventual) |
| vlstorage PVC already exists from previous deploy | StatefulSet reuses existing PVCs by name; no duplicate PVC creation | Yes |
| VLAgent ConfigMap already exists | `kubectl apply` updates existing ConfigMap; operator detects change and restarts VLAgent if config content changed | Yes |

---

## 7 Error Handling

### 7.1 Ansible Task Error Handling

| Error Category | Handling Strategy | Ansible Mechanism |
|---------------|-------------------|-------------------|
| **Validation failure** (invalid retention, storage size) | Fail fast with descriptive error before deployment | `assert` module or Python `raise ValueError()` in L2 validation |
| **kubectl connection failure** | Fail task with connection error; do not proceed with deployment | Default Ansible `failed_when` behavior |
| **CR application failure** | Fail task; display kubectl error output; allow operator to retry reconciliation on next run | `register` + `failed_when` with error message display |
| **Timeout waiting for rollout** | Fail task with timeout error; pods may still be starting | `command` module with `--timeout` flag; `failed_when` on non-zero exit |
| **Helm chart install failure** | Fail task; operator not available; CR application will fail | Default Ansible behavior; descriptive error message |
| **Template rendering failure** | Fail task with Jinja2 error (undefined variable, syntax error) | Default Ansible `template` module behavior |
| **Teardown of non-existent resources** | No error; operation is a no-op | `--ignore-not-found` flag on `kubectl delete`; `ignore_errors: true` on tasks |

**Credential isolation**:
```yaml
# All tasks handling TLS secrets use no_log
- name: Apply TLS secret
  command: kubectl apply -f victoria-tls-certs.yaml
  no_log: true
```

### 7.2 VLAgent Runtime Error Handling

| Error | VLAgent Behavior | Recovery |
|-------|-----------------|----------|
| vlinsert unreachable | Buffer to PVC; retry with exponential backoff (1s → 60s) | Automatic recovery when vlinsert becomes available; buffered logs forwarded |
| vlinsert returns 5xx | Buffer to PVC; retry with exponential backoff | Same as above |
| vlinsert returns 4xx | Log error; discard malformed batch (no retry) | Manual investigation; likely ConfigMap error |
| Syslog source disconnects | Accept new connections; no impact on other sources | Syslog sources reconnect independently |
| PVC buffer full | FIFO eviction of oldest entries; log warning | Increase PVC size or resolve vlinsert outage |
| TLS certificate expired | VLAgent cannot connect to vlinsert; buffers to PVC | Regenerate certificates via `gen_victoria_certs.sh`; rolling restart |
| OOM kill (memory limit) | Kubernetes restarts pod; PVC buffer preserves unsent logs | Pod restarts; replays PVC buffer; consider increasing memory limit |
| VLAgent pod crash | Kubernetes restarts pod (Deployment restartPolicy: Always) | Automatic restart; PVC buffer preserves state |

### 7.3 Deployment Failure Recovery

| Failure Point | Recovery Action | Idempotent |
|--------------|-----------------|------------|
| Operator Helm install failed | Re-run playbook; Helm `upgrade --install` is idempotent | Yes |
| VLCluster CR application failed | Re-run playbook; `kubectl apply` retries | Yes |
| vlstorage pods not starting (PVC issue) | Check StorageClass; verify PV availability; re-run playbook | Yes |
| vlinsert pods not starting (image pull) | Verify image in Pulp repository; check `service_k8s.json`; re-run playbook | Yes |
| LoadBalancer IP not assigned | Check MetalLB configuration; verify address pool; re-run playbook | Yes |
| TLS handshake failure | Regenerate certs with VictoriaLogs SANs; re-run playbook | Yes |
| Partial deployment (some CRs applied, some not) | Re-run playbook; `kubectl apply -k` applies all CRs; operator reconciles | Yes |

---

## 8 Acceptance Criteria Traceability

### AC-1: VLAgent spec defines scrape targets, pipeline configuration, and forwarding behavior

| Requirement | Section | Evidence |
|-------------|---------|----------|
| Scrape targets (syslog receivers) | 2.2 | Port 514 (plaintext TCP+UDP), port 6514 (TLS TCP); LoadBalancer exposure; source-neutral design (DD-A2) |
| Pipeline configuration | 2.3 | Three-stage pipeline: Receive (syslog) → Parse (syslog-to-JSON) → Forward (HTTP POST to vlinsert); field mapping table |
| Forwarding behavior (remoteWrite) | 2.4, 2.5 | HTTPS JSON Lines to vlinsert:9481 (DD-A3); CA cert validation; batch size and flush interval; forwarding behavior table (200/4xx/5xx handling) |
| Buffer and retry | 2.6 | 5 Gi PVC buffer (DD-A4); exponential backoff retry; per-stream ordering guarantee |
| VLAgent CR template | 2.12 | Full Jinja2 template with operator CR spec |
| VLAgent ConfigMap template | 2.13 | Syslog receiver + remoteWrite + persistentQueue configuration |
| Resource allocation | 2.7 | CPU 50m-250m, Memory 128Mi-512Mi |
| Service exposure | 2.9 | LoadBalancer for syslog; ClusterIP for health; MetalLB detection |

### AC-2: Task design documents deploy, teardown, and upgrade flows with pre/post conditions

| Requirement | Section | Evidence |
|-------------|---------|----------|
| Deploy flow | 3.1–3.8 | `deploy_victorialogs_cluster.yml` with 8 pre-conditions, 8-step task sequence, 8 post-conditions |
| Deploy manifest generation | 3.5 | 4 manifests: VLCluster CR, VLAgent CR, VLAgent ConfigMap, Kustomization |
| Deploy conditional logic | 3.8 | `'victoria' in telemetry_collection_type` gate; shared with VictoriaMetrics |
| Teardown flow | 4.1–4.5 | `teardown_victorialogs_cluster.yml` with 2 pre-conditions, 7-step task sequence, 9 post-conditions |
| Teardown cleanup script | 4.5 | `cleanup_telemetry.sh` extension with `victorialogs` argument; argument parsing, cleanup steps, PVC handling, force delete, resource check |
| Teardown disable_log | 4.6 | `disable_log.yml` tag-based selective pipeline disabling; VLCluster keeps running |
| PVC retention policy | 4.7 | Table showing auto-delete vs manual cleanup for each resource type |
| Upgrade flow | 5.1–5.5 | `apply_telemetry_on_upgrade.yml` VictoriaLogs block; 4 pre-conditions, 6-step task sequence, 7 post-conditions |
| Upgrade scenario matrix | 5.6 | 6 scenarios (U1–U6) covering full telemetry, kafka-only, fresh deploy, collection type changes |
| Upgrade config transformation | 5.5 | `transform_telemetry_config.yml` extension; retention and storage size preserved across upgrades |

### AC-3: Idempotency strategy ensures repeat runs produce no unintended changes

| Requirement | Section | Evidence |
|-------------|---------|----------|
| Idempotency principles | 6.1 | 6 principles: declarative state, kubectl apply, deterministic templates, operator convergence, ignore_errors on delete, changed_when on reads |
| Idempotency by task category | 6.2 | Table mapping each task to its idempotent mechanism with evidence |
| Operator reconciliation loop | 6.3 | Detailed reconciliation flow: read CR → read actual → compare → action/no-op |
| Edge cases and guarantees | 6.4 | 8 edge cases: concurrent runs, partial failure, node failure, network partition, PVC reuse, ConfigMap update |
| Error handling (Ansible) | 7.1 | Error categories with handling strategies; credential isolation with `no_log` |
| Error handling (VLAgent runtime) | 7.2 | 8 runtime error scenarios with VLAgent behavior and recovery actions |
| Deployment failure recovery | 7.3 | 7 failure points with recovery actions; all marked as idempotent |

---

## 9 Deployment Overview and Integration

### 9.1 telemetry.sh.j2 Execution Order

VLAgent deployment is orchestrated through the telemetry deployment flow, which follows this strict sequence:

```
1. kubectl apply -f telemetry_namespace_creation.yaml
   └─ Creates/ensures telemetry namespace exists

2. helm install victoria-metrics-operator <tarball>
   └─ Installs operator (manages both VictoriaMetrics and VictoriaLogs CRs)

3. [Ansible generates all CR templates]
   ├─ VMCluster CR (VictoriaMetrics cluster)
   ├─ VLCluster CR (VictoriaLogs cluster)
   ├─ VMAgent CR (metrics collector)
   └─ VLAgent CR (log collector) + ConfigMap

4. kubectl apply -k deployments/
   └─ Single kustomize apply of all CRs
   └─ Operator reconciles and creates workloads
```

**Critical ordering constraints**:
- Namespace MUST exist before operator install
- Operator MUST be installed before CRs are applied
- All CRs are applied together in a single `kubectl apply -k` command
- Operator reconciliation is asynchronous — pods may not be ready immediately

### 9.2 Deployment Gate vs Cleanup Independence

**Critical design principle**: VictoriaMetrics and VictoriaLogs share the same **deployment gate** but have **independent cleanup**.

#### Deployment Gate (Co-deployment)

VictoriaMetrics and VictoriaLogs are always deployed together:
- Both are gated by `'victoria' in telemetry_collection_type`
- If `'victoria'` is in the collection type, both are deployed
- If `'victoria'` is NOT in the collection type, neither is deployed
- There is no scenario where VictoriaLogs is deployed without VictoriaMetrics

#### Cleanup Independence

Cleanup is **independent** — you can remove one without affecting the other:

| Cleanup Command | VictoriaMetrics | VictoriaLogs | Other Components |
|-----------------|-----------------|--------------|------------------|
| `./cleanup_telemetry.sh victorialogs` | Untouched | Removed | Untouched |
| `./cleanup_telemetry.sh victoriametrics` | Removed | Untouched | Untouched |
| `./cleanup_telemetry.sh victoriametrics victorialogs` | Removed | Removed | Untouched |
| `./cleanup_telemetry.sh all` | Removed | Removed | Removed |

**Shared resources**:
- `victoria-tls-certs` secret: **NOT deleted** during `victorialogs` cleanup. This secret is shared with VictoriaMetrics and is only deleted during `victoriametrics` cleanup.
- `telemetry` namespace: **NOT deleted** during `victorialogs` cleanup. Namespace is shared among all telemetry components.

---

## 10 Operator Requirements

### 10.1 Operator Version and CRD Support

VLAgent is deployed and managed by the VictoriaMetrics operator, which watches for `VLAgent` Custom Resources and reconciles the underlying Kubernetes Deployment automatically.

| Property | Value |
|----------|-------|
| Operator Version | v0.68.3 or later |
| Operator Helm Chart | `victoria-metrics-operator-0.59.3.tgz` |
| CRD Kind | `VLAgent` |
| API Version | `operator.victoriametrics.com/v1beta1` |
| CRD Support | Requires operator >= v0.59.0 for VLCluster and VLAgent CRD support |

### 10.2 Image Sourcing from service_k8s.json

All VLAgent images are sourced from `service_k8s.json` and pre-staged in the local Pulp repository for air-gapped deployment:

| Image Key in `service_k8s.json` | Default Version | Purpose |
|---------------------------------|-----------------|---------|
| `victoriametrics/vlagent` | v1.49.0 | Log collector/forwarder |
| `victoriametrics/operator` | v0.68.3 | Manages VLAgent CR |

**Image staging flow**:
1. L2 validation extracts image references from `service_k8s.json`
2. `local_repo.yml` downloads images and stages them in the local Pulp repository
3. Kubernetes manifests reference images via the Pulp-mirrored registry
4. Deployment proceeds entirely offline — no Internet connectivity required

**Ansible variable usage**:
```yaml
image: "{{ telemetry_images['victoriametrics/vlagent'] | default('victoriametrics/vlagent:v1.49.0') }}"
```

---

## 11 Open Source License Information

All VLAgent and related components are open source software licensed under the Apache License 2.0:

| Component | License | Source Repository | Docker Image | Version |
|-----------|---------|-------------------|--------------|---------|
| VLAgent (vlagent) | Apache License 2.0 | https://github.com/VictoriaMetrics/VictoriaMetrics | `docker.io/victoriametrics/vlagent` | v1.49.0 |
| VictoriaMetrics Operator | Apache License 2.0 | https://github.com/VictoriaMetrics/operator | `docker.io/victoriametrics/operator` | v0.68.3 |
| Operator Helm Chart | Apache License 2.0 | https://github.com/VictoriaMetrics/helm-charts | `victoria-metrics-operator-0.59.3.tgz` | 0.59.3 |

For detailed license terms, refer to:
- VictoriaMetrics: https://github.com/VictoriaMetrics/VictoriaMetrics/blob/master/LICENSE
- Operator: https://github.com/VictoriaMetrics/operator/blob/master/LICENSE
