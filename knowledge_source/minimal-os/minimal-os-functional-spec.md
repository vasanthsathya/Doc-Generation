# Functional Specification --- Minimal OS-Only Functional Group

**Document ID:** FSPEC-9294-2026-001 | **Capability:** 9294 | **Version:** 1.1 | **Date:** 2026-04-06
**SDD Phase:** 2b --- Functional Specification (WHAT) | **Status:** Draft --- For Review

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-31 | Initial spec from capability 9294 requirements | AI-assisted |
| 1.1 | 2026-04-06 | (1) Renamed functional groups from `minimal_x86_64`/`minimal_aarch64` to `os_x86_64`/`os_aarch64` (renamed from existing `default_*` groups per engineering spec). (2) Added additional packages support via `additional_packages.json` (FS-IC-03, FS-CR-05, FS-AC-10, FS-AC-11). (3) Updated data flow diagram. | AI-assisted |

> **AI Assistance Notice:** Human review and validation required before approval.

---

## 1. Purpose

Defines **WHAT** the Omnia provisioning system does to support OS functional groups (`os_x86_64`, `os_aarch64`). These nodes provide a clean, minimal operating system baseline; they must be provisioned clean enough for downstream consumers to install platform software (e.g., RKE2) without conflicts, while still collecting telemetry on themselves. Administrators may optionally include additional packages (e.g., `podman`, diagnostic tools) via configuration.


## 2. Scope

**In Scope:** OS functional group definition (architecture-specific, renamed from existing `default_*` groups) | OS image composition using the existing Omnia base image plus LDMS telemetry package definitions plus optional administrator-defined additional packages | clean image through inclusion-only software mapping (no container orchestration, no container runtimes, no scheduler, no Omnia services) | stateless diskless provisioning | handoff state contract for downstream consumers

**Out of Scope:** Post-handoff platform installation (downstream consumer responsibility) | HA/failover for Minimal OS nodes (explicitly not required per capability) | telemetry pipeline configuration (separate capability) | iDRAC telemetry collection (container-based, runs on service cluster, not on compute nodes)

---

## 3. Functional Group Definition

| ID | Behavior |
|----|----------|
| FS-GD-01 | The system SHALL rename the existing `default_x86_64` and `default_aarch64` functional groups to `os_x86_64` and `os_aarch64` respectively. These OS functional groups SHALL be distinct inventory entities in the functional groups schema, alongside workers, login/compile, service, and OIM. |
| FS-GD-02 | Nodes SHALL be assigned to an OS functional group via the PXE mapping file (`FUNCTIONAL_GROUP_NAME` column); a node belongs to exactly one functional group at a time. |
| FS-GD-03 | The system SHALL validate that a node's hardware architecture matches the target functional group's architecture suffix (`_x86_64` or `_aarch64`) before provisioning. Architecture mismatch SHALL be reported as a validation error. |

---

## 4. Image Composition

### 4.1 Baseline

| ID | Behavior |
|----|----------|
| FS-IC-01 | The OS image SHALL be built on the standard Omnia base image: kernel, live image toolkit (network-capable), init system, network manager, IP utilities, NFS client, system logger, time synchronization, sudo, provisioning agent, and essential utilities. This is the same base shared by all Omnia functional groups. |
| FS-IC-02 | The image SHALL include LDMS telemetry packages (ovis-ldms and its dependencies) identical to the set installed on worker/compute nodes --- installed as **packages only**; no telemetry services enabled or started. |
| FS-IC-03 | The image SHALL support administrator-defined additional packages via an optional `additional_packages.json` configuration file. When present and non-empty, packages listed in this file SHALL be included in the image alongside base and LDMS packages. When the file is absent or empty, the image SHALL build successfully with base + LDMS only (graceful fallback). |


### 4.2 Exclusion Model

Omnia uses an **inclusion-based model**: only packages explicitly mapped to a functional group are included in its image. There are no explicit exclusion lists.

| ID | Behavior |
|----|----------|
| FS-EX-01 | The OS package mapping SHALL NOT include container orchestration packages (excludes container runtimes, Kubernetes, container interfaces). |
| FS-EX-02 | The OS package mapping SHALL NOT include scheduler packages (excludes Slurm, munge, CUDA, NVHPC, DOCA-OFED, apptainer). |
| FS-EX-03 | The OS package mapping SHALL NOT include MPI or communication library packages. |
| FS-EX-04 | The provisioning template for OS functional groups SHALL NOT start any services beyond OS minimum (SSH, time synchronization) and SHALL NOT run DOCA-OFED installation, scheduler configuration, or telemetry sampler setup. |
| FS-EX-05 | At boot, no user-space services SHALL be running beyond OS minimum (SSH daemon, time synchronization, network manager). |

---

## 5. Provisioning Behavior

| ID | Behavior |
|----|----------|
| FS-PV-01 | OS functional group nodes SHALL be provisioned as stateless, diskless nodes via HTTP-served live image, loaded entirely into RAM. |
| FS-PV-02 | Each provisioning cycle SHALL produce a deterministic, identical node state for the same functional group and image version. |
| FS-PV-03 | No persistent local state SHALL survive a reboot --- the root filesystem is read-only compressed image loaded into RAM. |
| FS-PV-04 | The provisioning system SHALL assign network identity (hostname, admin IP) per the PXE mapping file and node initialization configuration. |
| FS-PV-05 | Concurrent provisioning of multiple OS functional group nodes SHALL be supported without ordering constraints. |

---

## 6. Handoff State Contract

The handoff state is the node condition after Omnia provisioning and before downstream consumers install platform software. This is a formal contract --- downstream consumers rely on these guarantees.

| ID | Behavior |
|----|----------|
| FS-HS-01 | At handoff: running minimal OS with management network connectivity (via DHCP) and SSH access (root login enabled via provisioning system). |
| FS-HS-02 | At handoff: only SSH daemon, time synchronization daemon, and network manager running as user-space services. |
| FS-HS-03 | At handoff: no container runtimes, orchestration components, scheduler agents, or DOCA-OFED drivers present. |
| FS-HS-04 | At handoff: LDMS packages installed (ovis-ldms present), no LDMS sampler service running. |
| FS-HS-05 | At handoff: package manager functional with access to local repositories; downstream consumers can install platform software without conflicts. |

---

## 7. Error Handling

| ID | Condition | Behavior |
|----|-----------|----------|
| FS-ER-01 | Architecture mismatch (node vs. functional group suffix) | Provisioning fails at validation; node not partially provisioned. |
| FS-ER-02 | Network boot failure (kernel/initramfs retrieval) | Logged with node identity; node remains unprovisioned. |
| FS-ER-03 | Image not found in object storage | Pre-discovery validation fails; discovery does not proceed. |

> **Note:** FS-ER-04 ("excluded component detected post-provision") was removed --- no such mechanism exists in Omnia. Exclusion is enforced at image build time through the inclusion-only package mapping.

---

## 8. Data Flow

```
PXE Mapping File            Image Build                  Discovery + Boot
(functional group    --->   Package mapping      --->    Boot management system:
 = os_x86_64,              lookup (LDMS                  - Register node
 hostname, admin IP,        telemetry packages           - Set boot parameters
 admin MAC)                 + additional_packages        - Assign provisioning group
        |                   on base)                           |
  Architecture                                           Node PXE boots,
  validation                                             live image into RAM
                                                               |
                                                               v
                                                         Node initialization:
                                                         - Common config (SSH, time sync)
                                                         - Group-specific config
                                                           (root user only, no services)
                                                               |
                                                               v
                                                         Handoff State
                                                         (Ready for downstream)
```

---

## 9. Performance Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| FS-PR-01 | Provisioning duration (boot to handoff) | Comparable to existing default functional group; exact target in Engineering Spec |
| FS-PR-02 | Concurrent provisioning | No serialization; async image builds, independent PXE boot |
| FS-PR-03 | Scale | Validated at 100+ nodes per OS functional group |

---

## 10. Security Requirements

| ID | Requirement |
|----|-------------|
| FS-SR-01 | Provisioning traffic on management network only; no data on compute fabric. |
| FS-SR-02 | SSH root access controlled via provisioning system (authorized keys from OIM). |
| FS-SR-03 | Image SHALL NOT contain embedded credentials, secrets, or API tokens. |
| FS-SR-04 | No unnecessary listening ports beyond SSH at handoff. |

---

## 11. Configuration Requirements

| ID | Parameter |
|----|-----------|
| FS-CR-01 | Functional group name and target architecture (renamed from `default_*` to `os_*` in schema) |
| FS-CR-02 | Node-to-functional-group assignment in PXE mapping file |
| FS-CR-03 | Package mapping entry for OS functional groups (which package definitions to include) |
| FS-CR-04 | Provisioning template for OS functional groups |
| FS-CR-05 | Optional `additional_packages.json` file per architecture for administrator-defined additional packages |

> HOW configuration is structured is deferred to Engineering Specification.

---

## 12. Assumptions

| ID | Assumption |
|----|------------|
| FS-AS-01 | Boot infrastructure (DHCP, TFTP, HTTP, object storage) is pre-deployed and operational. |
| FS-AS-02 | Target OS is RHEL 10.x. |
| FS-AS-03 | LDMS package set is the shared telemetry reference across compute functional groups. iDRAC telemetry is container-based and out of scope for node images. |
| FS-AS-04 | Downstream consumers have documented their platform installation prerequisites and can confirm handoff compatibility. |
| FS-AS-05 | Local package repositories are accessible from provisioned nodes for post-handoff software installation. |

---

## 13. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| FS-AC-01 | A node assigned to `os_x86_64` provisions as a stateless, diskless x86_64 node with OS image loaded into RAM. |
| FS-AC-02 | A node assigned to `os_aarch64` provisions as a stateless, diskless AArch64 node with OS image loaded into RAM. |
| FS-AC-03 | After provisioning: no container runtimes, Kubernetes components, Slurm agents, DOCA-OFED, or CUDA present. |
| FS-AC-04 | After provisioning: only SSH daemon, time synchronization daemon, and network manager running as services. |
| FS-AC-05 | After provisioning: LDMS packages installed (ovis-ldms present), no LDMS sampler service running. |
| FS-AC-06 | After provisioning: package manager functional with local repository access; downstream consumers can install platform software without conflicts. |
| FS-AC-07 | Architecture mismatch detected and rejected at validation before discovery proceeds. |
| FS-AC-08 | Reprovisioning (reboot) restores identical handoff state --- stateless by design. |
| FS-AC-09 | Multiple nodes provisioned concurrently without interference (async image builds, independent PXE boot). |
| FS-AC-10 | When `additional_packages.json` is present with valid entries, listed packages are included in the image and available on provisioned nodes. |
| FS-AC-11 | When `additional_packages.json` is absent or empty, image builds successfully with base + LDMS only. |

---

## 14. Traceability

### 14.1 Upstream Requirements

| Requirement Source | Functional Behavior IDs |
|-------------------|------------------------|
| Cap-9294: Create Minimal OS inventory group | FS-GD-01..03 |
| Cap-9294: Minimal set of images and packages | FS-IC-01..03, FS-EX-01..05 |
| Cap-9294: Telemetry collection tools (identical to worker) | FS-IC-02, FS-HS-04 |
| Cap-9294: Network connectivity and drivers | FS-IC-01 (base image includes network manager, IP utilities), FS-HS-01 |
| Cap-9294: No conflicts with RKE2 | FS-EX-01..03, FS-HS-03, FS-HS-05 |
| Cap-9294: Truly minimal, no services running | FS-EX-04..05, FS-HS-02, FS-AC-04 |

### 14.2 Downstream Documents

| Downstream Document | Dependency |
|--------------------|------------|
| BSpec (Phase 2a) | Customer-facing behavior for Minimal OS groups |
| Engineering Spec (Phase 3a) | Implementation design: schema changes, package mapping, provisioning templates, validation pipeline |
| Test Spec (Phase 3b) | Test strategy based on acceptance criteria |

---

**SDD Phase 2b** | **Status:** Draft --- Requires engineering team approval before Phase 3
