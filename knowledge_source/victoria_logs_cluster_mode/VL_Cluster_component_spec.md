# VLCluster Component Spec (LLD)

| | |
|---|---|
| **Parent Document** | VictoriaLog_Cluster_engineering_spec.md (HLD v0.7) |
| **Spec Version** | 1.0 |
| **Author(s)** | Derived from HLD by Engineering |
| **Date** | 2025-04-13 |
| **Status** | Draft |

---

## Purpose

This Low-Level Design (LLD) document provides the coding-level blueprint for the three core VLCluster components — **vlstorage**, **vlinsert**, and **vlselect** — managed by the VictoriaMetrics operator via the `VLCluster` Custom Resource. It covers:

1. **vlstorage** — storage sizing and retention
2. **vlinsert** — replication factor and ingestion pipeline
3. **vlselect** — query routing and load balancing

All design decisions reference the parent HLD (Sections 3.2, 4.1.3.2, 4.1.5) and existing VMCluster implementation patterns in the codebase (`victoria-operator-vmcluster.yaml.j2`, `vars/main.yml`, `telemetry_config.yml`).

**Out of scope for this document**: VLAgent configuration, TLS certificate generation, Ansible playbook orchestration, teardown/cleanup, upgrade workflows, and Molecule test implementation. These are covered in separate LLD sections or in the parent HLD.

---

## Table of Contents

- 1 [Design Decision Summary](#1-design-decision-summary)
- 2 [vlstorage — Storage Sizing and Retention](#2-vlstorage--storage-sizing-and-retention)
  - 2.1 [Retention Design](#21-retention-design)
  - 2.2 [Storage Sizing Formula](#22-storage-sizing-formula)
  - 2.3 [PVC Configuration](#23-pvc-configuration)
  - 2.4 [Resource Allocation](#24-resource-allocation)
  - 2.5 [Data Path and Volume Mounts](#25-data-path-and-volume-mounts)
  - 2.6 [Anti-Affinity and Scheduling](#26-anti-affinity-and-scheduling)
  - 2.7 [Init Container — Lock Cleanup](#27-init-container--lock-cleanup)
  - 2.8 [Health Probes](#28-health-probes)
  - 2.9 [Container Args](#29-container-args)
  - 2.10 [Ansible Variable Definition](#210-ansible-variable-definition)
  - 2.11 [VLCluster CR Template — vlstorage Section](#211-vlcluster-cr-template--vlstorage-section)
  - 2.12 [User Configuration — telemetry_config.yml](#212-user-configuration--telemetry_configyml)
  - 2.13 [Input Validation — L2 Python](#213-input-validation--l2-python)
- 3 [vlinsert — Replication Factor and Ingestion Pipeline](#3-vlinsert--replication-factor-and-ingestion-pipeline)
  - 3.1 [Replication Factor](#31-replication-factor)
  - 3.2 [Ingestion Pipeline Architecture](#32-ingestion-pipeline-architecture)
  - 3.3 [Ingestion Endpoints](#33-ingestion-endpoints)
  - 3.4 [Sharding Strategy](#34-sharding-strategy)
  - 3.5 [Capacity Limits](#35-capacity-limits)
  - 3.6 [Resource Allocation](#36-resource-allocation)
  - 3.7 [Service Exposure](#37-service-exposure)
  - 3.8 [Health Probes](#38-health-probes)
  - 3.9 [Container Args](#39-container-args)
  - 3.10 [Ansible Variable Definition](#310-ansible-variable-definition)
  - 3.11 [VLCluster CR Template — vlinsert Section](#311-vlcluster-cr-template--vlinsert-section)
- 4 [vlselect — Query Routing and Load Balancing](#4-vlselect--query-routing-and-load-balancing)
  - 4.1 [Load Balancing Strategy](#41-load-balancing-strategy)
  - 4.2 [Query Routing Behavior](#42-query-routing-behavior)
  - 4.3 [Query Endpoints](#43-query-endpoints)
  - 4.4 [Resource Allocation](#44-resource-allocation)
  - 4.5 [Service Exposure](#45-service-exposure)
  - 4.6 [Health Probes](#46-health-probes)
  - 4.7 [Container Args](#47-container-args)
  - 4.8 [Ansible Variable Definition](#48-ansible-variable-definition)
  - 4.9 [VLCluster CR Template — vlselect Section](#49-vlcluster-cr-template--vlselect-section)
- 5 [Unified VLCluster CR Template](#5-unified-vlcluster-cr-template)
- 6 [Kustomization Integration](#6-kustomization-integration)
- 7 [TLS SAN Extension](#7-tls-san-extension)
- 8 [Port Allocation Summary](#8-port-allocation-summary)
- 9 [Acceptance Criteria Traceability](#9-acceptance-criteria-traceability)

---

## 1 Design Decision Summary

| ID | Component | Decision | Default | Rationale |
|----|-----------|----------|---------|-----------|
| DD-S1 | vlstorage | Retention period uses integer-hours format, consistent with VictoriaMetrics | `168` (7 days) | Aligns with VictoriaMetrics `victoria_configurations.retention_period` pattern; template appends `h` to convert to VictoriaLogs `-retentionPeriod` flag; single consistent format across metrics and logs |
| DD-S2 | vlstorage | Storage sized per-replica via PVC `volumeClaimTemplate` | `8Gi` per replica (24 Gi total for 3 replicas) | Matches VMCluster pattern; conservative default for moderate log volume; configurable upward |
| DD-S3 | vlstorage | 3 StatefulSet replicas with `preferredDuringScheduling` pod anti-affinity | 3 replicas | Provides redundancy across 2+ worker nodes; `preferred` (not `required`) allows scheduling on fewer nodes in constrained environments |
| DD-S4 | vlstorage | Storage sizing formula: `140 MB/day x retention_days x node_count` | N/A | Empirical estimate from VictoriaLogs compression ratio (~10:1 on structured JSON logs); provides planning guidance |
| DD-I1 | vlinsert | Replication factor = 2 (Deployment replicas) | 2 replicas | Provides ingestion HA — one pod can fail while ingestion continues; matches VMCluster vminsert pattern |
| DD-I2 | vlinsert | Consistent-hash sharding across vlstorage pods | Automatic (VictoriaLogs internal) | Even data distribution; no manual shard assignment; VictoriaLogs uses stream-based hashing by `_stream_fields` |
| DD-I3 | vlinsert | Capacity bounded by CPU/memory limits and vlstorage write throughput | CPU limit 1000m, Memory limit 1 Gi per pod | Prevents resource exhaustion on shared worker nodes; ingestion backpressure propagates to clients on saturation |
| DD-Q1 | vlselect | Load balancing via Kubernetes LoadBalancer service (MetalLB) | Round-robin across 2 vlselect pods | Standard L4 load balancing; client connections distributed across pods; no application-level routing needed |
| DD-Q2 | vlselect | Fan-out query routing: each vlselect pod queries ALL vlstorage pods and merges results | Automatic (VictoriaLogs internal) | Ensures complete result set regardless of data sharding; VictoriaLogs handles parallel scatter-gather and merge internally |
| DD-Q3 | vlselect | Replication factor = 2 (Deployment replicas) | 2 replicas | Provides query HA — one pod can fail while queries continue; matches VMCluster vmselect pattern |

---

## 2 vlstorage — Storage Sizing and Retention

### 2.1 Retention Design

**Decision (DD-S1)**: vlstorage uses integer-hours retention format, consistent with VictoriaMetrics.

| Property | Value |
|----------|-------|
| Configuration key | `victoria_logs_configurations.retention_period` |
| Format | Integer (hours). Examples: `168` (7 days), `720` (30 days), `2160` (90 days) |
| Default | `168` (7 days) |
| VictoriaLogs CLI flag | `-retentionPeriod` (template appends `h` suffix: `168` → `168h`) |
| Enforcement | vlstorage automatically deletes log data older than `retention_period` via background compaction |

**Rationale**: VictoriaMetrics (metrics) uses integer hours for retention (`168` = 7 days) and the VMCluster CR template appends `h` (e.g., `"168h"`). VictoriaLogs follows the same pattern for consistency: the administrator sets a single integer-hours value, and the Jinja2 template appends `h` before passing it to the `-retentionPeriod` flag. This ensures a uniform configuration experience across `victoria_configurations.retention_period` (metrics) and `victoria_logs_configurations.retention_period` (logs).

**Retention behavior**:
- vlstorage stores logs in time-partitioned blocks on the PVC filesystem
- Blocks older than `retention_period` are deleted during background merge operations
- Retention is **global** — applies to all log streams uniformly (per-stream retention is not supported upstream; see HLD Section 4.1.10)
- Deletion is asynchronous — disk space is reclaimed during the next merge cycle, not immediately at the retention boundary
- PVC data survives pod restarts — StatefulSet preserves PVC binding

**Validation rules** (see Section 2.13):
- Must be a positive integer
- Minimum: `24` (1 day)
- Maximum: `8760` (365 days / 1 year) — soft upper bound; validated as a warning, not a hard error

### 2.2 Storage Sizing Formula

**Decision (DD-S4)**: Provide a sizing formula for capacity planning.

```
Total storage required = ingestion_rate_per_node x retention_days x node_count
                       = 140 MB/day x retention_days x node_count
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ingestion_rate_per_node` | 140 MB/day | Estimated compressed storage per managed node per day |
| `retention_days` | 7 | From `victoria_logs_configurations.retention_period` (default `168` hours = 7 days) |
| `node_count` | Cluster-dependent | Number of managed nodes generating logs |

**Per-replica storage**:
```
storage_per_replica = Total storage required / vlstorage_replica_count
                    = (140 MB/day x retention_days x node_count) / 3
```

**Decision (DD-S2)**: Default PVC size of `8 Gi` per vlstorage replica.

| Scale | Nodes | Retention | Total Storage | Per-Replica (3) | Default Sufficient |
|-------|-------|-----------|--------------|-----------------|-------------------|
| Small | 50 | 7d | ~49 GB | ~16.3 GB | No (increase to 20Gi) |
| Small | 50 | 30d | ~210 GB | ~70 GB | No (increase to 75Gi) |
| Medium | 500 | 7d | ~70 GB | ~23.3 GB | No (increase to 25Gi) |
| Medium | 500 | 30d | ~300 GB | ~100 GB | No (increase to 105Gi) |
| Large | 2000 | 7d | ~350 GB | ~117 GB | No (increase to 120Gi) |
| Large | 2000 | 30d | ~1.5 TB | ~500 GB | No (increase to 512Gi) |

**Rationale for 8 Gi default**: The `8 Gi` default matches the VMCluster `persistence_size` default, enabling a functional cluster deployment without configuration changes in small development or evaluation environments (~4 nodes, 7-day retention). Production environments **must** adjust `storage_size` based on the sizing formula above.

**Sizing guidance comment** (rendered in `telemetry_config.yml`):
```yaml
# Storage per replica. Total cluster storage = storage_size x 3 vlstorage replicas.
# Sizing formula: 140 MB/day x retention_days x node_count / 3 replicas
# Example: 500 nodes, 7d retention → 70 GB total → 23 Gi per replica
```

### 2.3 PVC Configuration

| Property | Value | Rationale |
|----------|-------|-----------|
| Access mode | `ReadWriteOnce` | Each vlstorage pod has exclusive access to its PVC; required for StatefulSet with stable storage identity |
| Storage class | Cluster default (not specified) | Follows VMCluster pattern; uses whatever default StorageClass the cluster provisioner provides |
| Volume claim template name | `vlstorage-data` | Matches `storageDataPath` mount; operator names PVCs as `vlstorage-data-vlstorage-victoria-logs-cluster-{0,1,2}` |
| Reclaim policy | Retain (PVCs persist after StatefulSet deletion) | Prevents accidental data loss; manual cleanup required during teardown (see HLD Section 4.1.3.7.5) |

### 2.4 Resource Allocation

| Resource | Request | Limit | Rationale |
|----------|---------|-------|-----------|
| CPU | 250m | 1000m | Lower than VMCluster vmstorage (500m/2000m) because log storage is write-heavy sequential I/O, less CPU-intensive than metrics aggregation |
| Memory | 1 Gi | 2 Gi | Lower than VMCluster vmstorage (2Gi/4Gi) because VictoriaLogs uses memory-mapped files for indexing with lower resident memory requirements than VictoriaMetrics' in-memory merge trees |

### 2.5 Data Path and Volume Mounts

| Mount | Path | Source | Purpose |
|-------|------|--------|---------|
| `vlstorage-data` | `/vlstorage-data` | PVC `volumeClaimTemplate` | Persistent log data storage |
| `victoria-tls-certs` | `/etc/victoria/certs` (read-only) | Secret `victoria-tls-certs` | TLS certificate and key for encrypted inter-component communication |

### 2.6 Anti-Affinity and Scheduling

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app.kubernetes.io/name
                operator: In
                values:
                  - vlstorage
          topologyKey: "kubernetes.io/hostname"
```

**Decision (DD-S3)**: Use `preferred` (not `required`) anti-affinity.

**Rationale**: The HLD requires a minimum of 2 worker nodes (Section 3.1.1). With 3 vlstorage replicas and 2 nodes, `required` anti-affinity would fail to schedule the third pod. `preferred` with weight 100 distributes pods across nodes when possible but allows co-location when node count < replica count.

**Tolerations** (aligned with VMCluster pattern):
```yaml
tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 5
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 5
```

**Rationale**: 5-second toleration allows Kubernetes to quickly reschedule vlstorage pods when a node becomes unreachable, minimizing storage unavailability.

### 2.7 Init Container — Lock Cleanup

```yaml
initContainers:
  - name: cleanup-vlstorage-locks
    image: {{ victoria_logs_cluster.vlstorage.image }}
    command: ["sh", "-c"]
    args:
      - |
        echo "Cleaning up stale flock.lock files..."
        find /vlstorage-data -name "flock.lock" -delete 2>/dev/null || true
        echo "Lock cleanup complete."
    volumeMounts:
      - name: vlstorage-data
        mountPath: /vlstorage-data
```

**Rationale**: VictoriaLogs uses `flock.lock` files to prevent concurrent access to data directories. After ungraceful pod termination (e.g., node failure), stale lock files prevent the replacement pod from starting. The init container removes these locks before the main container starts.

### 2.8 Health Probes

| Probe | Type | Port | Path | Delay | Period | Timeout |
|-------|------|------|------|-------|--------|---------|
| Liveness | HTTP GET | 9491 | `/health` | 30s | 30s | 5s |
| Readiness | HTTP GET | 9491 | `/health` | 5s | 15s | 5s |

**Rationale**: Port 9491 is the vlstorage HTTP admin port. The `/health` endpoint returns 200 when the storage engine is operational. Liveness delay of 30s allows time for data directory initialization on first start. Readiness delay of 5s enables fast traffic routing after restart.

### 2.9 Container Args

```
-storageDataPath=/vlstorage-data
-retentionPeriod={{ hostvars['localhost']['victoria_logs_configurations']['retention_period'] }}h
-httpListenAddr=:9491
-vlinsertAddr=:9401
-vlselectAddr=:9402
-tls
-tlsCertFile=/etc/victoria/certs/server.crt
-tlsKeyFile=/etc/victoria/certs/server.key
```

| Flag | Value | Purpose |
|------|-------|---------|
| `-storageDataPath` | `/vlstorage-data` | PVC mount path for persistent log data |
| `-retentionPeriod` | From config with `h` suffix (default `168h` = 7 days) | Automatic purge of data older than this duration |
| `-httpListenAddr` | `:9491` | HTTP admin and health-check port |
| `-vlinsertAddr` | `:9401` | Port accepting data from vlinsert (ingestion) |
| `-vlselectAddr` | `:9402` | Port accepting queries from vlselect (query fan-out) |
| `-tls` | (flag) | Enable TLS on all listener ports |
| `-tlsCertFile` | `/etc/victoria/certs/server.crt` | Server certificate from shared `victoria-tls-certs` secret |
| `-tlsKeyFile` | `/etc/victoria/certs/server.key` | Server private key from shared `victoria-tls-certs` secret |

### 2.10 Ansible Variable Definition

Added to `provision/roles/telemetry/vars/main.yml` (parallel to `victoria_cluster` block):

```yaml
victoria_logs_cluster:
  tls_enabled: true

  # vlstorage: Persistent log storage nodes
  vlstorage:
    replicas: 3
    image: "{{ telemetry_images['victoriametrics/victoria-logs'] | default('victoriametrics/victoria-logs:v1.49.0') }}"
    resources:
      requests:
        memory: "1Gi"
        cpu: "250m"
      limits:
        memory: "2Gi"
        cpu: "1000m"
```

**Consolidated `victoria_logs_cluster` variable block** (vlinsert and vlselect definitions are in Sections 3.10 and 4.8 respectively; shown here for reference):

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `victoria_logs_cluster.tls_enabled` | Boolean | `true` | Enable TLS on all inter-component communication |
| `victoria_logs_cluster.vlstorage.replicas` | Integer | `3` | Number of vlstorage StatefulSet replicas |
| `victoria_logs_cluster.vlstorage.image` | String | `victoriametrics/victoria-logs:v1.49.0` | vlstorage container image (sourced from `service_k8s.json`) |
| `victoria_logs_cluster.vlstorage.resources` | Object | 1Gi/250m req, 2Gi/1000m lim | vlstorage resource requests and limits |
| `victoria_logs_cluster.vlinsert.replicas` | Integer | `2` | Number of vlinsert Deployment replicas |
| `victoria_logs_cluster.vlinsert.image` | String | `victoriametrics/victoria-logs:v1.49.0` | vlinsert container image (same image as vlstorage) |
| `victoria_logs_cluster.vlinsert.external_access` | Boolean | `true` | Expose vlinsert via LoadBalancer service |
| `victoria_logs_cluster.vlinsert.resources` | Object | 512Mi/250m req, 1Gi/1000m lim | vlinsert resource requests and limits |
| `victoria_logs_cluster.vlselect.replicas` | Integer | `2` | Number of vlselect Deployment replicas |
| `victoria_logs_cluster.vlselect.image` | String | `victoriametrics/victoria-logs:v1.49.0` | vlselect container image (same image as vlstorage) |
| `victoria_logs_cluster.vlselect.resources` | Object | 512Mi/250m req, 1Gi/1000m lim | vlselect resource requests and limits |

### Image Versions Reference

| Component | Image Key in `service_k8s.json` | Default Version | Purpose | License |
|-----------|--------------------------------|-----------------|---------|---------|
| VictoriaLogs (vlstorage, vlinsert, vlselect) | `victoriametrics/victoria-logs` | v1.49.0 | Core cluster components | Apache 2.0 |
| VLAgent | `victoriametrics/vlagent` | v1.49.0 | Log collector/forwarder | Apache 2.0 |
| Operator | `victoriametrics/operator` | v0.68.3 | Manages VLCluster and VLAgent CRs | Apache 2.0 |
| Operator Helm Chart | N/A | 0.59.3 | Operator deployment via Helm | Apache 2.0 |

**Note**: VLCluster CRD support requires operator >= v0.59.0. All images are sourced from `service_k8s.json` and pre-staged in local Pulp repository for air-gapped deployment.

### 2.11 VLCluster CR Template — vlstorage Section

```yaml
  vlstorage:
    replicaCount: {{ victoria_logs_cluster.vlstorage.replicas }}
    image:
      repository: {{ victoria_logs_cluster.vlstorage.image.split(':')[0] }}
      tag: {{ victoria_logs_cluster.vlstorage.image.split(':')[1] }}
      pullPolicy: IfNotPresent

    storageDataPath: /vlstorage-data
    storage:
      volumeClaimTemplate:
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: {{ hostvars['localhost']['victoria_logs_configurations']['storage_size'] }}

    resources:
      requests:
        memory: {{ victoria_logs_cluster.vlstorage.resources.requests.memory }}
        cpu: {{ victoria_logs_cluster.vlstorage.resources.requests.cpu }}
      limits:
        memory: {{ victoria_logs_cluster.vlstorage.resources.limits.memory }}
        cpu: {{ victoria_logs_cluster.vlstorage.resources.limits.cpu }}

    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: app.kubernetes.io/name
                    operator: In
                    values:
                      - vlstorage
              topologyKey: "kubernetes.io/hostname"

    tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 5
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 5

    extraArgs:
      retentionPeriod: "{{ hostvars['localhost']['victoria_logs_configurations']['retention_period'] }}h"
{% if victoria_logs_cluster.tls_enabled %}
      tls: "true"
      tlsCertFile: "/etc/victoria/certs/server.crt"
      tlsKeyFile: "/etc/victoria/certs/server.key"
{% endif %}
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
    volumeMounts:
      - name: victoria-tls-certs
        mountPath: /etc/victoria/certs
        readOnly: true
{% endif %}
```

### 2.12 User Configuration — telemetry_config.yml

Added under the existing `victoria_configurations:` block:

```yaml
# ============================================================================
# VICTORIALOGS CONFIGURATION
# ============================================================================
# VictoriaLogs provides centralized log storage and querying (cluster mode only).
# Deployed alongside VictoriaMetrics when 'victoria' is in idrac_telemetry_collection_type.
#
# DEPLOYMENT:
#   - Always cluster mode (vlstorage, vlinsert, vlselect, VLAgent)
#   - Co-deployed with VictoriaMetrics — same deployment gate
#   - Shares TLS infrastructure with VictoriaMetrics
#
# STORAGE REQUIREMENTS:
# ┌─────────────────┬──────────────────┬─────────────────┬──────────────────┐
# │ Component       │ Per-Pod Storage  │ Number of Pods  │ Total Storage    │
# ├─────────────────┼──────────────────┼─────────────────┼──────────────────┤
# │ vlstorage       │ storage_size     │ 3 pods          │ 3× storage       │
# ├─────────────────┼──────────────────┼─────────────────┼──────────────────┤
# │ VLAgent buffer  │ 5Gi (fixed)      │ 1 pod           │ 5Gi              │
# └─────────────────┴──────────────────┴─────────────────┴──────────────────┘
# Example: 8Gi × 3 vlstorage = 24Gi + 5Gi VLAgent = 29Gi total
victoria_logs_configurations:
  # Storage size per vlstorage replica PVC
  # IMPORTANT: Total VictoriaLogs storage = storage_size × 3 vlstorage pods
  # Accepted values: in the form of "X[Ki|Mi|Gi|Ti|Pi|Ei]"
  # Default: 8Gi (results in 24Gi total storage)
  storage_size: "8Gi"

  # Log retention period (duration in hours)
  # Logs older than this period are automatically purged by vlstorage.
  # Template appends 'h' suffix: 168 → "-retentionPeriod=168h" (7 days)
  # Default: 168 (7 days)
  retention_period: 168
```

### 2.13 Input Validation — L2 Python

Extend `common_validation.py` with the following validation rules (gated by `'victoria' in telemetry_collection_type`):

**retention_period validation**:
```python
MIN_RETENTION_HOURS = 24       # 1 day minimum
MAX_RETENTION_HOURS = 8760     # 365 days maximum (soft limit)

def validate_victoria_logs_retention(retention_period) -> None:
    """Validate victoria_logs_configurations.retention_period as integer hours."""
    if not isinstance(retention_period, int) or retention_period <= 0:
        raise ValueError(
            f"victoria_logs_configurations.retention_period '{retention_period}' "
            f"is invalid. Expected a positive integer (hours). "
            f"Examples: 168 (7 days), 720 (30 days), 2160 (90 days)"
        )

    if retention_period < MIN_RETENTION_HOURS:
        raise ValueError(
            f"victoria_logs_configurations.retention_period '{retention_period}' "
            f"is below the minimum of {MIN_RETENTION_HOURS} hours (1 day)."
        )

    if retention_period > MAX_RETENTION_HOURS:
        # Warning, not error — allow but flag
        logger.warning(
            f"victoria_logs_configurations.retention_period '{retention_period}' hours "
            f"exceeds {MAX_RETENTION_HOURS} hours (365 days). "
            f"Ensure sufficient storage is provisioned."
        )
```

**storage_size validation**:
```python
VALID_PVC_SIZE_PATTERN = re.compile(r'^[1-9][0-9]*(Ki|Mi|Gi|Ti|Pi|Ei)$')

def validate_victoria_logs_storage_size(storage_size: str) -> None:
    """Validate victoria_logs_configurations.storage_size as valid PVC format."""
    if not VALID_PVC_SIZE_PATTERN.match(storage_size):
        raise ValueError(
            f"victoria_logs_configurations.storage_size '{storage_size}' "
            f"is invalid. Expected Kubernetes PVC size format. "
            f"Examples: '8Gi', '50Gi', '100Gi'"
        )
```

---

## 3 vlinsert — Replication Factor and Ingestion Pipeline

### 3.1 Replication Factor

**Decision (DD-I1)**: vlinsert runs as a Kubernetes Deployment with 2 replicas.

| Property | Value | Rationale |
|----------|-------|-----------|
| Kind | Deployment | Stateless ingestion gateway; no persistent storage needed; Deployment enables rolling updates without StatefulSet overhead |
| Replicas | 2 | Provides HA — if one pod fails, the LoadBalancer routes all traffic to the surviving pod; matches VMCluster vminsert (2 replicas) |
| Scaling | Horizontal — increase `replicas` in `vars/main.yml` | Each additional replica adds ingestion throughput; vlstorage pods are automatically discovered via the operator |

**Replication factor context**: The term "replication factor" in the VLCluster context refers to the **number of vlinsert Deployment replicas**, not data replication. VictoriaLogs cluster mode does **not** replicate log data across vlstorage nodes — each log entry is stored on exactly one vlstorage pod (determined by consistent hashing). Data durability comes from PVC persistence, not replication. This aligns with the VictoriaMetrics cluster design where vminsert similarly does not replicate data across vmstorage.

### 3.2 Ingestion Pipeline Architecture

```
                                        vlstorage-0
                                       ┌────────────┐
Ingestion       vlinsert-0             │  PVC 8Gi   │
Clients    ┌─────────────┐  consistent │  :9401     │
  ────────>│  :9481 HTTPS │ hash shard  ├────────────┤
           │  (pod 0)     │────────────>│  logs for  │
  ────────>│              │             │  streams   │
           └─────────────┘             │  A, C, E   │
                                       └────────────┘
LoadBalancer                           vlstorage-1
(MetalLB)                             ┌────────────┐
  ────────>┌─────────────┐            │  PVC 8Gi   │
           │  :9481 HTTPS │ consistent │  :9401     │
  ────────>│  (pod 1)     │ hash shard ├────────────┤
           │              │───────────>│  logs for  │
           └─────────────┘            │  streams   │
                                      │  B, D, F   │
                                      └────────────┘
```

**Pipeline stages**:

1. **Client connection**: Ingestion client (VLAgent, curl, application) establishes HTTPS connection to vlinsert LoadBalancer IP on port 9481
2. **L4 load balancing**: MetalLB distributes TCP connections across vlinsert pods using round-robin (default MetalLB behavior for L4)
3. **Request parsing**: vlinsert parses the incoming request body based on the endpoint path:
   - `/insert/jsonline` — parse JSON Lines format
   - `/insert/syslog` — parse syslog RFC 5424 format
   - `/insert/elasticsearch/_bulk` — parse Elasticsearch bulk API format
4. **Stream identification**: vlinsert extracts `_stream_fields` from each log entry to determine the log stream identity (e.g., `host`, `app`, `source`)
5. **Consistent-hash sharding**: vlinsert computes a hash of the stream identity and routes the entry to the target vlstorage pod via TLS on port 9401
6. **Acknowledgment**: vlinsert returns HTTP 200 to the client after vlstorage confirms the write

### 3.3 Ingestion Endpoints

| Endpoint | Format | Content-Type | Description |
|----------|--------|-------------|-------------|
| `/insert/jsonline` | JSON Lines (NDJSON) | `application/x-ndjson` or `application/json` | Primary ingestion format; each line is a JSON object with `_msg`, `_time`, and optional fields; supports `_stream_fields`, `_msg_field`, `_time_field` query parameters |
| `/insert/syslog` | syslog RFC 5424 | `application/octet-stream` | Native syslog ingestion; VictoriaLogs parses RFC 5424 structured data |
| `/insert/elasticsearch/_bulk` | Elasticsearch bulk API | `application/x-ndjson` | ES-compatible bulk import for clients that natively support Elasticsearch |

**Endpoint URL pattern** (from outside the cluster):
```
https://<vlinsert_loadbalancer_ip>:9481/insert/jsonline
https://<vlinsert_loadbalancer_ip>:9481/insert/syslog
https://<vlinsert_loadbalancer_ip>:9481/insert/elasticsearch/_bulk
```

**Endpoint URL pattern** (from within the cluster):
```
https://vlinsert-victoria-logs-cluster.telemetry.svc.cluster.local:9481/insert/jsonline
```

### 3.4 Sharding Strategy

**Decision (DD-I2)**: Consistent-hash sharding across vlstorage pods.

| Property | Value |
|----------|-------|
| Algorithm | Consistent hashing on log stream identity |
| Hash key | Stream identity derived from `_stream_fields` (e.g., `{host="node1", app="syslog"}`) |
| Target | vlstorage pods discovered via headless service DNS (`vlstorage-victoria-logs-cluster-{0,1,2}`) |
| Rebalancing | Automatic when vlstorage replicas change — new streams may hash to new pods; existing data is NOT redistributed |

**Sharding behavior**:
- All log entries belonging to the same stream land on the same vlstorage pod — this enables efficient time-series-like storage and querying within a stream
- vlinsert maintains a consistent-hash ring of vlstorage endpoints, updated via the operator's headless service
- If a vlstorage pod is temporarily unreachable, vlinsert will return an error to the ingestion client (no automatic retry or buffering in vlinsert itself — VLAgent provides client-side retry and buffering)

### 3.5 Capacity Limits

| Limit | Value | Source | Behavior on Breach |
|-------|-------|--------|--------------------|
| CPU per pod | 1000m (limit) | Kubernetes resource limit | Throttled by cgroup; ingestion slows |
| Memory per pod | 1 Gi (limit) | Kubernetes resource limit | OOM-killed; Deployment restarts pod |
| Concurrent connections | Unlimited (bounded by OS limits) | VictoriaLogs default | Kernel `net.core.somaxconn` applies |
| Max request body size | VictoriaLogs default (unlimited) | Not explicitly configured | Large payloads consume memory; bounded by memory limit |
| Network throughput | Node NIC capacity | Physical infrastructure | vlinsert is CPU/memory bound before NIC saturation in typical log volumes |

**Capacity planning**:
- Each vlinsert pod can handle approximately 50-100 MB/s of compressed log ingestion at the default resource limits
- For clusters generating > 100 MB/s sustained log traffic, increase vlinsert replicas or CPU/memory limits
- vlinsert is stateless — horizontal scaling is linear and does not require coordination

**Backpressure behavior**:
1. vlstorage disk full → vlstorage returns error to vlinsert → vlinsert returns 500 to client
2. vlinsert CPU saturated → ingestion latency increases → client-side timeouts
3. vlinsert memory saturated → OOM kill → Deployment restarts pod within seconds → LoadBalancer routes to surviving replica

### 3.6 Resource Allocation

| Resource | Request | Limit | Rationale |
|----------|---------|-------|-----------|
| CPU | 250m | 1000m | Matches VMCluster vminsert; ingestion involves parsing + network I/O, moderate CPU |
| Memory | 512 Mi | 1 Gi | Matches VMCluster vminsert; buffers in-flight log entries during sharding |

### 3.7 Service Exposure

```yaml
serviceSpec:
  useAsDefault: true
  spec:
    type: LoadBalancer
```

| Property | Value | Rationale |
|----------|-------|-----------|
| Service type | `LoadBalancer` | External access for VLAgent and downstream ingestion clients via MetalLB |
| Port | 9481 | VictoriaLogs cluster vlinsert default; avoids conflict with VMCluster vminsert (8480) |
| Protocol | HTTPS (TLS) | All ingestion traffic encrypted; enforced via `-tls` flag |
| Service name (operator-managed) | `vlinsert-victoria-logs-cluster` | Operator derives from CR name: `vlinsert-<VLCluster.metadata.name>` |

**MetalLB detection** (for environments without MetalLB):
```yaml
{% if metalLB_deployed | default(false) %}
    serviceSpec:
      useAsDefault: true
      spec:
        type: LoadBalancer
{% else %}
    serviceSpec:
      useAsDefault: true
      spec:
        type: NodePort
{% endif %}
```

### 3.8 Health Probes

| Probe | Type | Port | Path | Delay | Period | Timeout |
|-------|------|------|------|-------|--------|---------|
| Liveness | HTTP GET | 9481 | `/health` | 30s | 30s | 5s |
| Readiness | HTTP GET | 9481 | `/health` | 5s | 10s | 5s |

### 3.9 Container Args

```
-httpListenAddr=:9481
-storageNode=vlstorage-victoria-logs-cluster-0.vlstorage-victoria-logs-cluster.telemetry.svc.cluster.local:9401
-storageNode=vlstorage-victoria-logs-cluster-1.vlstorage-victoria-logs-cluster.telemetry.svc.cluster.local:9401
-storageNode=vlstorage-victoria-logs-cluster-2.vlstorage-victoria-logs-cluster.telemetry.svc.cluster.local:9401
-tls
-tlsCertFile=/etc/victoria/certs/server.crt
-tlsKeyFile=/etc/victoria/certs/server.key
```

| Flag | Value | Purpose |
|------|-------|---------|
| `-httpListenAddr` | `:9481` | HTTPS ingestion port |
| `-storageNode` | (one per vlstorage pod, FQDN:9401) | vlstorage endpoints for data sharding; operator auto-configures based on `vlstorage.replicaCount` |
| `-tls` | (flag) | Enable TLS on listener |
| `-tlsCertFile` | `/etc/victoria/certs/server.crt` | Server certificate |
| `-tlsKeyFile` | `/etc/victoria/certs/server.key` | Server private key |

**Note**: The operator automatically constructs the `-storageNode` flags from the `VLCluster` CR. The vlinsert template does **not** hardcode storage node addresses — the operator resolves them from the headless service.

### 3.10 Ansible Variable Definition

Added to `provision/roles/telemetry/vars/main.yml`:

```yaml
  # vlinsert: Log ingestion gateway
  vlinsert:
    replicas: 2
    image: "{{ telemetry_images['victoriametrics/victoria-logs'] | default('victoriametrics/victoria-logs:v1.49.0') }}"
    external_access: true
    resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "1000m"
```

### 3.11 VLCluster CR Template — vlinsert Section

```yaml
  vlinsert:
    replicaCount: {{ victoria_logs_cluster.vlinsert.replicas }}
    image:
      repository: {{ victoria_logs_cluster.vlinsert.image.split(':')[0] }}
      tag: {{ victoria_logs_cluster.vlinsert.image.split(':')[1] }}
      pullPolicy: IfNotPresent

    resources:
      requests:
        memory: {{ victoria_logs_cluster.vlinsert.resources.requests.memory }}
        cpu: {{ victoria_logs_cluster.vlinsert.resources.requests.cpu }}
      limits:
        memory: {{ victoria_logs_cluster.vlinsert.resources.limits.memory }}
        cpu: {{ victoria_logs_cluster.vlinsert.resources.limits.cpu }}

    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: app.kubernetes.io/name
                    operator: In
                    values:
                      - vlinsert
              topologyKey: "kubernetes.io/hostname"
{% if victoria_logs_cluster.tls_enabled %}

    extraArgs:
      tls: "true"
      tlsCertFile: "/etc/victoria/certs/server.crt"
      tlsKeyFile: "/etc/victoria/certs/server.key"

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
{% if victoria_logs_cluster.vlinsert.external_access %}

    serviceSpec:
      useAsDefault: true
      spec:
        type: LoadBalancer
{% endif %}
```

---

## 4 vlselect — Query Routing and Load Balancing

### 4.1 Load Balancing Strategy

**Decision (DD-Q1)**: L4 load balancing via Kubernetes LoadBalancer service (MetalLB).

```
                 MetalLB
                LoadBalancer
                <External IP>:9491
                    │
            ┌───────┴───────┐
            │ Round-Robin L4 │
            └───────┬───────┘
         ┌──────────┴──────────┐
         ▼                     ▼
   vlselect-0              vlselect-1
   (pod 0, :9491)         (pod 1, :9491)
```

| Property | Value | Rationale |
|----------|-------|-----------|
| Load balancer type | MetalLB (bare-metal L4 LoadBalancer) | Omnia runs on bare-metal Kubernetes — MetalLB provides external IP allocation without cloud provider; consistent with VMCluster vmselect exposure |
| Algorithm | Round-robin (MetalLB default for L4) | Stateless query processing — no session affinity needed; each query is independent; even distribution across pods provides optimal latency |
| Session affinity | None | LogsQL queries are stateless; no benefit from sticky sessions; absence of affinity maximizes pod utilization |
| Failover behavior | Automatic — MetalLB removes unhealthy pods from rotation based on readiness probe | Pod fails readiness → MetalLB stops routing → surviving pod handles all queries → failed pod recovers → MetalLB resumes routing |
| External IP | Assigned by MetalLB from configured address pool | IP is stable across pod restarts; downstream clients cache this IP |

**Alternative considered**: NodePort. Rejected because it exposes a high-numbered port requiring client-side port management and does not provide a stable external IP. LoadBalancer is the standard VMCluster pattern.

### 4.2 Query Routing Behavior

**Decision (DD-Q2)**: Fan-out scatter-gather query routing.

```
Query Client                vlselect pod            vlstorage-0        vlstorage-1        vlstorage-2
    │                          │                       │                   │                   │
    │── LogsQL query ─────────>│                       │                   │                   │
    │   (HTTPS :9491)          │                       │                   │                   │
    │                          │── fan-out query ─────>│                   │                   │
    │                          │   (TLS :9402)         │                   │                   │
    │                          │── fan-out query ──────────────────────────>│                   │
    │                          │   (TLS :9402)                             │                   │
    │                          │── fan-out query ─────────────────────────────────────────────>│
    │                          │   (TLS :9402)                                                 │
    │                          │                       │                   │                   │
    │                          │<─ partial results ────│                   │                   │
    │                          │<─ partial results ───────────────────────│                   │
    │                          │<─ partial results ──────────────────────────────────────────│
    │                          │                       │                   │                   │
    │                          │── merge + sort +      │                   │                   │
    │                          │   dedup results       │                   │                   │
    │                          │                       │                   │                   │
    │<─ merged results ────────│                       │                   │                   │
```

**Routing rules**:

| Rule | Behavior |
|------|----------|
| Fan-out target | Every vlselect pod queries **ALL** vlstorage pods on every query |
| Partial result merging | vlselect collects partial results from each vlstorage pod, merges them by timestamp, and deduplicates |
| Ordering | Results are returned in reverse chronological order (newest first) by default; configurable via LogsQL `sort` pipe |
| Timeout | vlselect waits for all vlstorage pods to respond; if a vlstorage pod is unreachable, the query returns partial results after the connection timeout |
| Parallelism | Fan-out queries to vlstorage pods are executed in parallel (concurrent goroutines within vlselect) |

**Rationale for fan-out to ALL vlstorage**: Because vlinsert shards data by stream identity (consistent hash), a given LogsQL query may match logs on any vlstorage pod. The only way to guarantee a complete result set is to query all pods. This is the same scatter-gather pattern used by VMCluster vmselect.

### 4.3 Query Endpoints

| Endpoint | Description | Use Case |
|----------|-------------|----------|
| `/select/logsql/query` | Execute a LogsQL query and return matching log entries | Primary query interface; supports filters, pipes, aggregations |
| `/select/logsql/hits` | Return log hit counts grouped by time interval | Time-series visualization of log volume (histogram) |
| `/select/logsql/stats_query` | Execute statistical aggregation queries | Top-N analysis, field cardinality, count by field value |
| `/select/logsql/stream_ids` | Enumerate log stream IDs matching a filter | Discovery of available log streams |
| `/select/logsql/streams` | Return stream metadata | Stream introspection |
| `/select/logsql/tail` | Live tail streaming (long-poll or WebSocket) | Real-time log monitoring |

**Endpoint URL pattern** (from outside the cluster):
```
https://<vlselect_loadbalancer_ip>:9491/select/logsql/query?query=<LogsQL>
```

**Endpoint URL pattern** (from within the cluster):
```
https://vlselect-victoria-logs-cluster.telemetry.svc.cluster.local:9491/select/logsql/query?query=<LogsQL>
```

### 4.4 Resource Allocation

| Resource | Request | Limit | Rationale |
|----------|---------|-------|-----------|
| CPU | 250m | 1000m | Matches VMCluster vmselect; query processing involves fan-out I/O and result merging |
| Memory | 512 Mi | 1 Gi | Matches VMCluster vmselect; buffers partial results from vlstorage pods during merge; memory scales with query result size |

### 4.5 Service Exposure

```yaml
serviceSpec:
  useAsDefault: true
  spec:
    type: LoadBalancer
```

| Property | Value | Rationale |
|----------|-------|-----------|
| Service type | `LoadBalancer` | External access for query clients via MetalLB |
| Port | 9491 | VictoriaLogs cluster vlselect default; avoids conflict with VMCluster vmselect (8481) |
| Protocol | HTTPS (TLS) | All query traffic encrypted; enforced via `-tls` flag |
| Service name (operator-managed) | `vlselect-victoria-logs-cluster` | Operator derives from CR name: `vlselect-<VLCluster.metadata.name>` |

### 4.6 Health Probes

| Probe | Type | Port | Path | Delay | Period | Timeout |
|-------|------|------|------|-------|--------|---------|
| Liveness | HTTP GET | 9491 | `/health` | 30s | 30s | 5s |
| Readiness | HTTP GET | 9491 | `/health` | 5s | 10s | 5s |

### 4.7 Container Args

```
-httpListenAddr=:9491
-storageNode=vlstorage-victoria-logs-cluster-0.vlstorage-victoria-logs-cluster.telemetry.svc.cluster.local:9402
-storageNode=vlstorage-victoria-logs-cluster-1.vlstorage-victoria-logs-cluster.telemetry.svc.cluster.local:9402
-storageNode=vlstorage-victoria-logs-cluster-2.vlstorage-victoria-logs-cluster.telemetry.svc.cluster.local:9402
-tls
-tlsCertFile=/etc/victoria/certs/server.crt
-tlsKeyFile=/etc/victoria/certs/server.key
```

| Flag | Value | Purpose |
|------|-------|---------|
| `-httpListenAddr` | `:9491` | HTTPS query port |
| `-storageNode` | (one per vlstorage pod, FQDN:9402) | vlstorage endpoints for fan-out queries; operator auto-configures |
| `-tls` | (flag) | Enable TLS on listener |
| `-tlsCertFile` | `/etc/victoria/certs/server.crt` | Server certificate |
| `-tlsKeyFile` | `/etc/victoria/certs/server.key` | Server private key |

**Note**: Same as vlinsert — the operator automatically constructs the `-storageNode` flags. The vlselect template does **not** hardcode storage node addresses.

### 4.8 Ansible Variable Definition

Added to `provision/roles/telemetry/vars/main.yml`:

```yaml
  # vlselect: Log query gateway
  vlselect:
    replicas: 2
    image: "{{ telemetry_images['victoriametrics/victoria-logs'] | default('victoriametrics/victoria-logs:v1.49.0') }}"
    resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "1000m"
```

### 4.9 VLCluster CR Template — vlselect Section

```yaml
  vlselect:
    replicaCount: {{ victoria_logs_cluster.vlselect.replicas }}
    image:
      repository: {{ victoria_logs_cluster.vlselect.image.split(':')[0] }}
      tag: {{ victoria_logs_cluster.vlselect.image.split(':')[1] }}
      pullPolicy: IfNotPresent

{% if metalLB_deployed | default(false) %}
    serviceSpec:
      useAsDefault: true
      spec:
        type: LoadBalancer
{% else %}
    serviceSpec:
      useAsDefault: true
      spec:
        type: NodePort
{% endif %}

    resources:
      requests:
        memory: {{ victoria_logs_cluster.vlselect.resources.requests.memory }}
        cpu: {{ victoria_logs_cluster.vlselect.resources.requests.cpu }}
      limits:
        memory: {{ victoria_logs_cluster.vlselect.resources.limits.memory }}
        cpu: {{ victoria_logs_cluster.vlselect.resources.limits.cpu }}

    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: app.kubernetes.io/name
                    operator: In
                    values:
                      - vlselect
              topologyKey: "kubernetes.io/hostname"
{% if victoria_logs_cluster.tls_enabled %}

    extraArgs:
      tls: "true"
      tlsCertFile: "/etc/victoria/certs/server.crt"
      tlsKeyFile: "/etc/victoria/certs/server.key"

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
```

---

## 5 Unified VLCluster CR Template

**File**: `provision/roles/telemetry/templates/telemetry/victoria/victorialogs-operator-vlcluster.yaml.j2`

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

# VLCluster - VictoriaLogs cluster deployment via operator
# Managed by victoria-metrics-operator (>= v0.59.0)

apiVersion: operator.victoriametrics.com/v1beta1
kind: VLCluster
metadata:
  name: victoria-logs-cluster
  namespace: {{ telemetry_namespace }}
spec:
  # Single image version for all cluster components
  # Operator determines component role (vlstorage, vlinsert, vlselect) internally
  clusterVersion: {{ victoria_logs_cluster.vlstorage.image.split(':')[1] }}

  # ========================
  # vlstorage — Persistent log storage (StatefulSet, 3 replicas)
  # ========================
  vlstorage:
    replicaCount: {{ victoria_logs_cluster.vlstorage.replicas }}
    image:
      repository: {{ victoria_logs_cluster.vlstorage.image.split(':')[0] }}
      tag: {{ victoria_logs_cluster.vlstorage.image.split(':')[1] }}
      pullPolicy: IfNotPresent

    storageDataPath: /vlstorage-data
    storage:
      volumeClaimTemplate:
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: {{ hostvars['localhost']['victoria_logs_configurations']['storage_size'] }}

    resources:
      requests:
        memory: {{ victoria_logs_cluster.vlstorage.resources.requests.memory }}
        cpu: {{ victoria_logs_cluster.vlstorage.resources.requests.cpu }}
      limits:
        memory: {{ victoria_logs_cluster.vlstorage.resources.limits.memory }}
        cpu: {{ victoria_logs_cluster.vlstorage.resources.limits.cpu }}

    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: app.kubernetes.io/name
                    operator: In
                    values:
                      - vlstorage
              topologyKey: "kubernetes.io/hostname"

    tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 5
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 5

    extraArgs:
      retentionPeriod: "{{ hostvars['localhost']['victoria_logs_configurations']['retention_period'] }}h"
{% if victoria_logs_cluster.tls_enabled %}
      tls: "true"
      tlsCertFile: "/etc/victoria/certs/server.crt"
      tlsKeyFile: "/etc/victoria/certs/server.key"
{% endif %}
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
    volumeMounts:
      - name: victoria-tls-certs
        mountPath: /etc/victoria/certs
        readOnly: true
{% endif %}

  # ========================
  # vlinsert — Log ingestion gateway (Deployment, 2 replicas)
  # ========================
  vlinsert:
    replicaCount: {{ victoria_logs_cluster.vlinsert.replicas }}
    image:
      repository: {{ victoria_logs_cluster.vlinsert.image.split(':')[0] }}
      tag: {{ victoria_logs_cluster.vlinsert.image.split(':')[1] }}
      pullPolicy: IfNotPresent

    resources:
      requests:
        memory: {{ victoria_logs_cluster.vlinsert.resources.requests.memory }}
        cpu: {{ victoria_logs_cluster.vlinsert.resources.requests.cpu }}
      limits:
        memory: {{ victoria_logs_cluster.vlinsert.resources.limits.memory }}
        cpu: {{ victoria_logs_cluster.vlinsert.resources.limits.cpu }}

    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: app.kubernetes.io/name
                    operator: In
                    values:
                      - vlinsert
              topologyKey: "kubernetes.io/hostname"
{% if victoria_logs_cluster.tls_enabled %}

    extraArgs:
      tls: "true"
      tlsCertFile: "/etc/victoria/certs/server.crt"
      tlsKeyFile: "/etc/victoria/certs/server.key"

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
{% if victoria_logs_cluster.vlinsert.external_access %}

    serviceSpec:
      useAsDefault: true
      spec:
        type: LoadBalancer
{% endif %}

  # ========================
  # vlselect — Log query gateway (Deployment, 2 replicas)
  # ========================
  vlselect:
    replicaCount: {{ victoria_logs_cluster.vlselect.replicas }}
    image:
      repository: {{ victoria_logs_cluster.vlselect.image.split(':')[0] }}
      tag: {{ victoria_logs_cluster.vlselect.image.split(':')[1] }}
      pullPolicy: IfNotPresent

    serviceSpec:
      useAsDefault: true
      spec:
        type: LoadBalancer

    resources:
      requests:
        memory: {{ victoria_logs_cluster.vlselect.resources.requests.memory }}
        cpu: {{ victoria_logs_cluster.vlselect.resources.requests.cpu }}
      limits:
        memory: {{ victoria_logs_cluster.vlselect.resources.limits.memory }}
        cpu: {{ victoria_logs_cluster.vlselect.resources.limits.cpu }}

    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: app.kubernetes.io/name
                    operator: In
                    values:
                      - vlselect
              topologyKey: "kubernetes.io/hostname"
{% if victoria_logs_cluster.tls_enabled %}

    extraArgs:
      tls: "true"
      tlsCertFile: "/etc/victoria/certs/server.crt"
      tlsKeyFile: "/etc/victoria/certs/server.key"

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
```

---

## 6 Kustomization Integration

Extend `provision/roles/telemetry/templates/telemetry/kustomization.yaml.j2` (within the existing `{% if 'victoria' in types %}` block):

```yaml
{% if 'victoria' in types %}
  # ... existing VictoriaMetrics resources ...

  # VictoriaLogs Cluster Mode: VLCluster CR (operator manages vlstorage StatefulSet, vlinsert/vlselect Deployments)
  - victorialogs-operator-vlcluster.yaml
{% endif %}
```

**Rationale**: VictoriaLogs is always deployed in cluster mode (no single-node toggle). The VLCluster CR is included whenever `'victoria'` is in `telemetry_collection_type`, matching the existing VMCluster inclusion gate. No additional mode check is needed.

---

## 7 TLS SAN Extension

Extend `gen_victoria_certs.sh.j2` `[alt_names]` section with VictoriaLogs DNS SANs (appended after existing VMCluster SANs):

```bash
# VictoriaLogs cluster deployment names (operator-managed)
DNS.24 = vlinsert-victoria-logs-cluster
DNS.25 = vlinsert-victoria-logs-cluster.{{ telemetry_namespace }}
DNS.26 = vlinsert-victoria-logs-cluster.{{ telemetry_namespace }}.svc
DNS.27 = vlinsert-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local
DNS.28 = vlselect-victoria-logs-cluster
DNS.29 = vlselect-victoria-logs-cluster.{{ telemetry_namespace }}
DNS.30 = vlselect-victoria-logs-cluster.{{ telemetry_namespace }}.svc
DNS.31 = vlselect-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local
DNS.32 = vlstorage-victoria-logs-cluster
DNS.33 = vlstorage-victoria-logs-cluster.{{ telemetry_namespace }}
DNS.34 = vlstorage-victoria-logs-cluster.{{ telemetry_namespace }}.svc
DNS.35 = vlstorage-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local
# vlstorage StatefulSet pod FQDNs (operator-managed, 3 replicas)
DNS.36 = vlstorage-victoria-logs-cluster-0.vlstorage-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local
DNS.37 = vlstorage-victoria-logs-cluster-1.vlstorage-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local
DNS.38 = vlstorage-victoria-logs-cluster-2.vlstorage-victoria-logs-cluster.{{ telemetry_namespace }}.svc.cluster.local
```

**Rationale**: The operator creates services named `vlinsert-<CR-name>`, `vlselect-<CR-name>`, and `vlstorage-<CR-name>`. TLS certificates must include these DNS names as SANs for in-cluster HTTPS to succeed. StatefulSet pod FQDNs are required for vlinsert → vlstorage and vlselect → vlstorage direct pod-to-pod TLS communication.

#### Impact of Missing SANs

If the `gen_victoria_certs.sh.j2` script is **not extended** with VictoriaLogs SANs:
- vlinsert → vlstorage TLS handshake will fail (certificate name mismatch)
- vlselect → vlstorage TLS handshake will fail (certificate name mismatch)
- Deployment will fail with TLS certificate validation errors
- Pods will enter CrashLoopBackOff state

#### SAN Verification

After certificate generation, verify SANs are present:
```bash
openssl x509 -in /path/to/server.crt -text -noout | grep -A 20 "Subject Alternative Name"
```

Expected output should include all VictoriaLogs DNS names listed above. If vlstorage replica count is increased beyond 3, additional pod FQDNs must be added (vlstorage-victoria-logs-cluster-3, etc.).

---

## 8 Port Allocation Summary

| Port | Component | Protocol | Service Type | Direction | Conflict Check |
|------|-----------|----------|-------------|-----------|----------------|
| 9481 | vlinsert | HTTPS | LoadBalancer | Ingestion clients → vlinsert | No conflict (VMCluster uses 8480) |
| 9491 | vlselect | HTTPS | LoadBalancer | Query clients → vlselect | No conflict (VMCluster uses 8481) |
| 9491 | vlstorage | HTTP | Headless (internal) | Health checks and admin API | Internal only; no external exposure |
| 9401 | vlstorage | HTTPS | Headless (internal) | vlinsert → vlstorage (data sharding) | No conflict (VMCluster uses 8400) |
| 9402 | vlstorage | HTTPS | Headless (internal) | vlselect → vlstorage (query fan-out) | No conflict (VMCluster uses 8401) |

**Port range separation**: VMCluster uses ports 8400-8482; VLCluster uses ports 9401-9491. The ranges are fully independent with no overlap.

---

## 9 Acceptance Criteria Traceability

### AC-1: VLCluster storage design decision documents retention sizing formula, default values, and rationale

| Requirement | Section | Evidence |
|-------------|---------|----------|
| Retention sizing formula | 2.2 | `140 MB/day x retention_days x node_count` with scale table |
| Default retention value | 2.1 | `168` hours (7 days) (DD-S1) |
| Default storage size | 2.2 | `8 Gi` per replica, 24 Gi total (DD-S2) |
| Rationale for retention format | 2.1 | Integer-hours format consistent with VictoriaMetrics `victoria_configurations.retention_period` |
| Rationale for storage default | 2.2 | Matches VMCluster pattern; functional for small environments; production must tune |
| Rationale for replica count | 2.6 | 3 replicas with `preferred` anti-affinity across 2+ nodes (DD-S3) |
| PVC configuration details | 2.3 | `ReadWriteOnce`, cluster default StorageClass, `Retain` reclaim |
| Input validation | 2.13 | Regex, min/max bounds, Python validation code |

### AC-2: VLCluster ingestion design decision specifies replication factor, pipeline configuration, and capacity limits

| Requirement | Section | Evidence |
|-------------|---------|----------|
| Replication factor | 3.1 | 2 Deployment replicas (DD-I1); clarification that this is pod-level HA, not data replication |
| Pipeline configuration | 3.2 | Full pipeline architecture: client → L4 LB → vlinsert parse → consistent-hash shard → vlstorage write → ack |
| Ingestion endpoints | 3.3 | `/insert/jsonline`, `/insert/syslog`, `/insert/elasticsearch/_bulk` with URL patterns |
| Sharding strategy | 3.4 | Consistent-hash on `_stream_fields` (DD-I2) |
| Capacity limits | 3.5 | CPU 1000m, Memory 1 Gi per pod; backpressure behavior; scaling guidance (DD-I3) |
| Container args | 3.9 | `-httpListenAddr`, `-storageNode`, TLS flags |
| Service exposure | 3.7 | LoadBalancer on port 9481 with MetalLB detection fallback |

### AC-3: VLCluster query design decision defines load balancing strategy and routing behavior

| Requirement | Section | Evidence |
|-------------|---------|----------|
| Load balancing strategy | 4.1 | L4 round-robin via MetalLB LoadBalancer (DD-Q1); no session affinity; architecture diagram |
| Routing behavior | 4.2 | Fan-out scatter-gather to ALL vlstorage pods (DD-Q2); parallel execution; merge + sort + dedup; sequence diagram |
| Query endpoints | 4.3 | `/select/logsql/query`, `/hits`, `/stats_query`, `/stream_ids`, `/streams`, `/tail` with URL patterns |
| Failover behavior | 4.1 | Automatic via readiness probe; MetalLB removes unhealthy pods from rotation |
| Replication factor | 4.1 | 2 Deployment replicas (DD-Q3) |
| Container args | 4.7 | `-httpListenAddr`, `-storageNode` (port 9402), TLS flags |
| Service exposure | 4.5 | LoadBalancer on port 9491 |

---

## 10 Operator Architecture and Deployment

### 10.1 Operator Overview

The VictoriaMetrics operator (v0.68.3+) supports CRDs for both VictoriaMetrics (metrics) and VictoriaLogs (logs). A single operator instance manages the complete observability stack:

| CRD Kind | API Version | Purpose | Manages |
|----------|-------------|---------|---------|
| `VMCluster` | `operator.victoriametrics.com/v1beta1` | VictoriaMetrics cluster mode | vmstorage StatefulSet, vminsert Deployment, vmselect Deployment |
| `VLCluster` | `operator.victoriametrics.com/v1beta1` | VictoriaLogs cluster mode | vlstorage StatefulSet, vlinsert Deployment, vlselect Deployment |
| `VLAgent` | `operator.victoriametrics.com/v1beta1` | Log collector/forwarder | VLAgent Deployment |

**Key advantage**: One operator Helm chart install manages both VictoriaMetrics and VictoriaLogs — no separate operator or Helm chart needed for logs.

### 10.2 Operator Installation

The operator is installed via Helm chart as part of the telemetry deployment:

| Property | Value |
|----------|-------|
| Chart | `victoria-metrics-operator-0.59.3.tgz` |
| Version | 0.59.3 |
| Minimum operator version | v0.59.0 (required for VLCluster CRD support) |
| Operator image | `docker.io/victoriametrics/operator:v0.68.3` |
| License | Apache 2.0 |

The operator Helm chart is sourced from `service_k8s.json` and pre-staged in the local Pulp repository. Installation is performed by `telemetry.sh.j2` before CR application:

```bash
helm install victoria-metrics-operator \
  victoria-metrics-operator-0.59.3.tgz \
  --namespace telemetry
```

### 10.3 Operator-Managed vs Manual Resources

| Resource | Managed By | Notes |
|----------|-----------|-------|
| vlstorage StatefulSet | Operator (via `VLCluster` CR) | Operator creates, scales, updates |
| vlinsert Deployment | Operator (via `VLCluster` CR) | Operator creates, scales, updates |
| vlselect Deployment | Operator (via `VLCluster` CR) | Operator creates, scales, updates |
| VLAgent Deployment | Operator (via `VLAgent` CR) | Operator creates, manages lifecycle |
| VLAgent ConfigMap | Manual manifest | Syslog receiver configuration |
| VLAgent PVC | Manual manifest | Buffer storage |
| TLS Certificates | Manual (`gen_victoria_certs.sh` → `victoria-tls-certs` secret) | Omnia generates certs; operator mounts the user-provided secret |

### 10.4 clusterVersion Field

The `clusterVersion` field in the VLCluster CR specifies a single image version for all VictoriaLogs cluster components (vlstorage, vlinsert, vlselect):

```yaml
spec:
  clusterVersion: {{ victoria_logs_cluster.vlstorage.image.split(':')[1] }}
```

**Design rationale**: VictoriaLogs components are tightly coupled and must use the same version. vlinsert and vlselect communicate with vlstorage using version-specific protocols — mixing versions can cause protocol incompatibility. The `clusterVersion` field prevents version mismatches by design, as the operator automatically applies this version to all three component image tags.

**Templating**: The Jinja2 template extracts the version tag from the image string (e.g., `victoriametrics/victoria-logs:v1.49.0` → `v1.49.0`) using `.split(':')[1]`.

### 10.5 Upgrade Behavior with Operator

When upgrading VictoriaLogs via operator CRs:
- Update `VLCluster` CR spec (e.g., new image tag, changed replica count, storage size)
- Operator detects CR change and performs **rolling update** automatically
- vlstorage StatefulSet pods are updated one by one (ordered)
- vlinsert/vlselect Deployments are updated via standard Kubernetes rolling update
- PVCs are preserved — operator does not delete PVCs during upgrades
- Version is controlled via `clusterVersion` field (single image for all components)

---

## 11 Container Arguments — Templating Mechanism

### 11.1 How Arguments Are Passed to Containers

The VLCluster CR uses the `extraArgs` field to pass command-line arguments to each component. The operator constructs the final container command by combining:
1. VictoriaLogs binary defaults
2. Arguments from the CR spec's `extraArgs` field

### 11.2 Templating Pattern

Arguments that depend on user configuration (e.g., retention period) are templated in the Jinja2 template before being rendered into the CR:

```yaml
extraArgs:
  retentionPeriod: "{{ hostvars['localhost']['victoria_logs_configurations']['retention_period'] }}h"
  tls: "true"
  tlsCertFile: "/etc/victoria/certs/server.crt"
  tlsKeyFile: "/etc/victoria/certs/server.key"
```

**Templating rules**:
- Retention period is an integer (hours) from `telemetry_config.yml`, e.g., `168`
- The template appends `h` suffix to convert to VictoriaLogs format: `168` → `168h`
- TLS flags are conditionally included based on `victoria_logs_cluster.tls_enabled`
- Storage node addresses are automatically constructed by the operator from the headless service

### 11.3 Example: Rendered Container Command

Given user configuration `retention_period: 168` (7 days), the operator constructs:

```
/victoria-logs-vlstorage \
  -storageDataPath=/vlstorage-data \
  -retentionPeriod=168h \
  -httpListenAddr=:9491 \
  -vlinsertAddr=:9401 \
  -vlselectAddr=:9402 \
  -tls \
  -tlsCertFile=/etc/victoria/certs/server.crt \
  -tlsKeyFile=/etc/victoria/certs/server.key
```

---

## 12 Image Sourcing from service_k8s.json

All container images for VictoriaLogs cluster deployment are sourced from `service_k8s.json` and pre-staged in the local Pulp repository for air-gapped deployment:

| Image Key in `service_k8s.json` | Purpose | Notes |
|---------------------------------|---------|-------|
| `victoriametrics/victoria-logs` | Single image for all VictoriaLogs cluster components (vlstorage, vlinsert, vlselect). Operator determines component role internally via `clusterVersion`. | Admin manages version only. |
| `victoriametrics/vlagent` | Log collector/forwarder. Version aligned with victoria-logs. | Deployed as separate `VLAgent` CR. |
| `victoriametrics/operator` | VictoriaMetrics operator (manages both VictoriaMetrics and VictoriaLogs CRs). | Installed via Helm chart. |

**Image staging flow**:
1. L2 validation extracts image references from `service_k8s.json`
2. `local_repo.yml` downloads images and stages them in the local Pulp repository
3. Kubernetes manifests reference images via the Pulp-mirrored registry
4. Deployment proceeds entirely offline — no Internet connectivity required

**Ansible variable usage**:
```yaml
image: "{{ telemetry_images['victoriametrics/victoria-logs'] | default('victoriametrics/victoria-logs:v1.49.0') }}"
```

The `telemetry_images` dictionary is populated from `service_k8s.json`. The `default()` filter provides a fallback version if the key is not found.

---

## 13 Open Source License Information

All VictoriaLogs cluster components are open source software licensed under the Apache License 2.0:

| Component | License | Source Repository | Docker Image | Version |
|-----------|---------|-------------------|--------------|---------|
| VictoriaLogs (vlstorage, vlinsert, vlselect) | Apache License 2.0 | https://github.com/VictoriaMetrics/VictoriaMetrics | `docker.io/victoriametrics/victoria-logs` | v1.49.0 |
| VLAgent (vlagent) | Apache License 2.0 | https://github.com/VictoriaMetrics/VictoriaMetrics | `docker.io/victoriametrics/vlagent` | v1.49.0 |
| VictoriaMetrics Operator | Apache License 2.0 | https://github.com/VictoriaMetrics/operator | `docker.io/victoriametrics/operator` | v0.68.3 |
| Operator Helm Chart | Apache License 2.0 | https://github.com/VictoriaMetrics/helm-charts | `victoria-metrics-operator-0.59.3.tgz` | 0.59.3 |

For detailed license terms, refer to:
- VictoriaMetrics: https://github.com/VictoriaMetrics/VictoriaMetrics/blob/master/LICENSE
- Operator: https://github.com/VictoriaMetrics/operator/blob/master/LICENSE
