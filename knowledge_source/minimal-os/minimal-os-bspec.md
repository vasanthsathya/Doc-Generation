# Behavior Specification (BSpec) --- Minimal OS-Only Functional Group

**Document ID:** BSPEC-9294-2026-001 | **Capability:** 9294 | **Version:** 1.1 | **Date:** 2026-04-06
**SDD Phase:** 2a --- Behavior Specification (Customer Behavior) | **Status:** Draft --- For Review

> **AI Assistance Notice:** I am assisting with this specification. Human review and validation is required before approval.

---

**Table of Contents**

- [1 References](#1-references)
- [2 Glossary](#2-glossary)
- [3 Edit History](#3-edit-history)
- [4 Overview](#4-overview)
- [5 Description of Features Covered in Behavior Specification](#5-description-of-features-covered-in-behavior-specification)
- [6 General Behavioral Descriptions](#6-general-behavioral-descriptions)
  - [6.1 Minimal OS Functional Group Definition and Node Assignment](#61-minimal-os-functional-group-definition-and-node-assignment)
  - [6.2 Minimal OS Image Composition](#62-minimal-os-image-composition)
  - [6.3 Stateless Diskless Provisioning](#63-stateless-diskless-provisioning)
  - [6.4 Handoff State Contract for Downstream Consumers](#64-handoff-state-contract-for-downstream-consumers)
  - [6.5 Telemetry Readiness (Packages Without Services)](#65-telemetry-readiness-packages-without-services)
  - [6.6 Provisioning Error Handling and Validation](#66-provisioning-error-handling-and-validation)
- [7 Cross-Feature Integration](#7-cross-feature-integration)
- [8 End-to-End Scenario](#8-end-to-end-scenario)
- [9 Approvals](#9-approvals)

---

## 1 References

The following documents are included for reference.

| **LOB** | **Type** | **Document Name (Document Link)** | **Document Description** |
|---------|----------|-----------------------------------|--------------------------|
| Omnia | Requirements | Cap-9294 --- Minimal OS-Only Functional Group | PDM capability requirements defining a minimal OS functional group for nodes that host downstream platform software (e.g., RKE2) |
| Omnia | Functional Specification | FSPEC-9294-2026-001 --- Minimal OS-Only Functional Group (v1.1) | Defines internal system behavior (WHAT) for functional group definition, image composition, provisioning, and handoff state |
| Omnia | Methodology | Spec-Driven Development Approach | SDD 8-phase lifecycle methodology governing this specification |

---

## 2 Glossary

| **Acronym / Term** | **Definition** |
|---------------------|----------------|
| BSpec | Behavior Specification --- defines customer-facing behavior (what users see and do) |
| Functional Group | A role-based classification for cluster nodes that determines image composition, provisioning template, and software stack. Each node belongs to exactly one functional group. |
| Minimal OS | A functional group providing a bare operating system baseline with no schedulers, container runtimes, or orchestration software, intended for downstream platform consumers |
| OIM | Omnia Infrastructure Manager --- central management node that hosts provisioning services and repositories |
| PXE | Preboot Execution Environment --- network boot protocol used to provision stateless nodes |
| Stateless Node | A node whose operating system is loaded entirely into RAM from a network-served image; no local disk state persists across reboots |
| Handoff State | The guaranteed node condition after Omnia provisioning and before downstream consumers install their platform software |
| Downstream Consumer | Any team or system that installs platform software (e.g., RKE2, custom K8s) on Minimal OS nodes after Omnia provisioning |
| LDMS | Lightweight Distributed Metric Service --- collects HPC node-level performance metrics (CPU, memory, network, I/O) |
| iDRAC | Integrated Dell Remote Access Controller --- embedded server management controller. iDRAC telemetry is container-based and runs on the service cluster, not on compute nodes |
| Pulp | Local package repository system used by Omnia for air-gapped package distribution |
| DOCA-OFED | Driver package for NVIDIA/Mellanox InfiniBand and Ethernet adapters |
| RKE2 | Rancher Kubernetes Engine 2 --- an example downstream platform that may be installed on Minimal OS nodes |

---

## 3 Edit History

| **Revision** | **Date** | **Changes** | **Author** |
|--------------|----------|-------------|------------|
| 1.0 | 2026-03-31 | Initial BSpec generated from capability 9294 requirements and functional spec FSPEC-9294-2026-001 (v1.0). Six features covering group definition, image composition, provisioning, handoff contract, telemetry readiness, and error handling. | AI-assisted (human review required) |
| 1.1 | 2026-04-06 | (1) Renamed functional groups from `minimal_x86_64`/`minimal_aarch64` to `os_x86_64`/`os_aarch64` (renamed from existing `default_*` groups per engineering spec). (2) Added additional packages support via `additional_packages.json` in image composition (6.2), cross-feature integration (7), and end-to-end scenario (8). (3) Updated all workflows and acceptance criteria. | AI-assisted (human review required) |

---

## 4 Overview

This Behavior Specification defines how users and operators experience and interact with the Omnia Minimal OS-Only functional group capability (Capability 9294).

It describes observable behaviors, workflows, and outcomes from the perspective of:

- **Cluster Administrators** who define node roles in the PXE mapping file and provision Minimal OS nodes
- **Downstream Platform Teams** (e.g., RKE2 operators, custom K8s deployers) who install platform software on provisioned Minimal OS nodes
- **Observability Engineers** who need telemetry packages pre-installed for future sampler activation
- **Omnia Platform Operators** who build images, run discovery, and manage cluster lifecycle

The Minimal OS functional group addresses a key gap: customers need nodes provisioned with a truly clean operating system baseline --- no Slurm, no Kubernetes, no container runtimes, no DOCA-OFED --- so that downstream platform software can be installed without conflicts. At the same time, these nodes must carry telemetry packages (identical to worker nodes) so they can participate in cluster-wide observability once telemetry services are activated.

This document is derived from the approved Functional Specification (FSPEC-9294-2026-001 v1.0) and the PDM capability requirements (9294). It focuses strictly on customer-facing behavior. Internal system logic, implementation details, and configuration mechanics are intentionally excluded and deferred to the Engineering Specification (SDD Phase 3a).

---

## 5 Description of Features Covered in Behavior Specification

| **Section** | **Feature Name** | **Domain** | **Requirement Trace** |
|-------------|------------------|------------|----------------------|
| 6.1 | Minimal OS Functional Group Definition and Node Assignment | Configuration / Inventory | FS-GD-01, FS-GD-02, FS-GD-03 |
| 6.2 | Minimal OS Image Composition | Image Build / Packaging | FS-IC-01..03, FS-EX-01..05 |
| 6.3 | Stateless Diskless Provisioning | Provisioning / Boot | FS-PV-01..05 |
| 6.4 | Handoff State Contract for Downstream Consumers | Integration / Handoff | FS-HS-01..05 |
| 6.5 | Telemetry Readiness (Packages Without Services) | Observability | FS-IC-02, FS-HS-04 |
| 6.6 | Provisioning Error Handling and Validation | Reliability / Safety | FS-ER-01..03 |

---

## 6 General Behavioral Descriptions

### 6.1 Minimal OS Functional Group Definition and Node Assignment

#### 6.1.1 Marketing User Stories

| **Theme** | **MRD Excerpt / Feature Description** |
|-----------|---------------------------------------|
| Inventory | As a cluster administrator, I need a dedicated Minimal OS functional group so that I can assign nodes to a clean OS role distinct from Slurm workers, login nodes, and service cluster nodes. |
| Multi-Architecture | As a cluster administrator managing a mixed-architecture cluster, I need architecture-specific Minimal OS groups (x86_64 and AArch64) so that each node is provisioned with the correct image for its hardware. |

#### 6.1.2 Overview

Omnia renames the existing `default_x86_64` and `default_aarch64` functional groups to `os_x86_64` and `os_aarch64` as first-class entries in the functional group schema. Administrators assign nodes to these groups via the PXE mapping file, using the same workflow they already use for Slurm and service cluster nodes. The system validates that each node's hardware architecture matches the assigned group before provisioning proceeds.

#### 6.1.3 Detail

**Group Registration**

The OS functional groups (`os_x86_64`, `os_aarch64`) SHALL be available as valid values in the functional group schema. These are renamed from the existing `default_x86_64` and `default_aarch64` groups. They SHALL appear alongside existing groups (Slurm worker, Slurm controller, login, login compiler, service K8s control plane, service K8s node) without replacing or modifying any other existing group.

**Node Assignment**

Administrators SHALL assign nodes to an OS functional group by entering the group name in the `FUNCTIONAL_GROUP_NAME` column of the PXE mapping file. Each node SHALL belong to exactly one functional group at a time. The mapping file format and all other required columns (GROUP_NAME, SERVICE_TAG, HOSTNAME, ADMIN_MAC, ADMIN_IP, BMC_MAC, BMC_IP) SHALL remain unchanged.

**Architecture Validation**

The system SHALL validate that a node's hardware architecture matches the architecture suffix of the assigned functional group (`_x86_64` or `_aarch64`). If a mismatch is detected, provisioning SHALL fail at validation with a clear error identifying the mismatched node and the expected architecture. No partial provisioning SHALL occur for a mismatched node.

**Layer Classification**

The OS functional groups SHALL be classified within the provisioning system's layer model so that they participate in the same validation pipeline as all other functional groups. They SHALL NOT bypass layer-based validation.

#### 6.1.4 Workflow

```
  Administrator                    Omnia System                     Cluster Nodes
       |                                |                                |
       |-- Edit PXE mapping file ------>|                                |
       |   (FUNCTIONAL_GROUP_NAME       |                                |
       |    = os_x86_64)                |                                |
       |                                |                                |
       |-- Run discovery -------------->|                                |
       |                                |-- Validate architecture ------>|
       |                                |   (x86_64 node? yes -> pass)   |
       |                                |                                |
       |                                |-- Register node + assign ----->|
       |                                |   provisioning group           |
       |                                |                                |
       |<-- Discovery complete ---------|                                |
```

#### 6.1.5 Acceptance Criteria

| **AC-ID** | **Criteria** | **Validation Method** |
|-----------|--------------|-----------------------|
| AC-1.1 | `os_x86_64` and `os_aarch64` are accepted as valid functional group names in the PXE mapping file | Enter both names in the mapping file and verify discovery accepts them without schema validation errors |
| AC-1.2 | A node assigned to `os_x86_64` passes validation when the node hardware is x86_64 | Assign an x86_64 node to `os_x86_64` and verify discovery proceeds |
| AC-1.3 | A node assigned to `os_x86_64` fails validation when the node hardware is AArch64 | Assign an AArch64 node to `os_x86_64` and verify discovery fails with architecture mismatch error |
| AC-1.4 | OS functional groups participate in the same layer validation as all other functional groups | Verify that OS groups are present in the layer classification and do not bypass validation |
| AC-1.5 | Existing functional groups (Slurm, login, service K8s) remain unaffected | Provision nodes with existing groups alongside Minimal OS nodes and verify no behavioral changes |

#### 6.1.6 Performance

- Adding OS functional groups to the schema SHALL NOT measurably increase discovery validation time
- Architecture validation for OS functional group nodes SHALL complete in the same time as for any other functional group

#### 6.1.7 Assets/Resources at Risk

- Provisioning failure if architecture validation logic does not correctly handle the new group names
- Silent misconfiguration if OS functional groups bypass layer validation
- Inventory confusion if group names conflict with existing or future functional group conventions

---

### 6.2 Minimal OS Image Composition

#### 6.2.1 Marketing User Stories

| **Theme** | **MRD Excerpt / Feature Description** |
|-----------|---------------------------------------|
| Cleanliness | As a downstream platform team, I need Minimal OS nodes to contain only a base OS plus telemetry packages, with absolutely no Slurm, Kubernetes, container runtimes, or DOCA-OFED, so that my platform software installs without package conflicts. |
| Consistency | As a cluster administrator, I need the Minimal OS image to be built using the same base as all other Omnia functional groups so that networking, authentication, and system utilities behave identically across the cluster. |

#### 6.2.2 Overview

The OS image is composed using the same Omnia base image shared by all functional groups (kernel, init system, network manager, time synchronization, system logger, SSH, and essential utilities), with the addition of LDMS telemetry packages and optional administrator-defined additional packages. The image explicitly does not include any scheduler, container orchestration, GPU compute, InfiniBand driver, or MPI packages. Omnia's inclusion-based package model ensures that only explicitly mapped packages appear in the image.

#### 6.2.3 Detail

**Shared Base Image**

The OS image SHALL be built on the standard Omnia base image. This base includes the kernel, live image toolkit, init system, network manager, IP utilities, NFS client, system logger, time synchronization, sudo, provisioning agent, and essential system utilities. This is the same base used by every other Omnia functional group. No packages SHALL be removed from or added to the shared base specifically for the OS functional groups.

**Included Packages**

Beyond the shared base, the OS image SHALL include:
1. LDMS telemetry packages (ovis-ldms and its dependencies), identical to the telemetry package set installed on Slurm worker and login nodes
2. Administrator-defined additional packages (optional) --- specified via `additional_packages.json` configuration file. Examples include `podman`, diagnostic utilities, and monitoring agents. When the file is absent or empty, only base + LDMS packages are included.

**Excluded Software Categories**

The OS package mapping SHALL NOT include:
- Container orchestration packages (Kubernetes, container runtimes, container interfaces)
- Scheduler packages (Slurm, munge, CUDA, NVHPC, DOCA-OFED, apptainer)
- MPI or communication library packages (UCX, OpenMPI)

No exclusion list mechanism is needed. Omnia's inclusion-based model ensures that only packages explicitly mapped to the OS group are present in the image.

**Image Verification**

After image build completes, the administrator SHALL be able to verify that images for all OS functional groups present in the mapping file have been created and are available in object storage.

#### 6.2.4 Workflow

```
  Administrator                   Omnia Image Build              Object Storage
       |                                |                              |
       |-- Run image build ------------>|                              |
       |                                |-- Read mapping file          |
       |                                |   (find os_x86_64)          |
       |                                |                              |
       |                                |-- Collect packages:          |
       |                                |   base + LDMS                |
       |                                |   + additional_packages      |
       |                                |     (if present)             |
       |                                |                              |
       |                                |-- Build live image --------->|
       |                                |   (compressed, RAM-loadable) |
       |                                |                              |
       |<-- Build complete -------------|                              |
       |                                |                              |
       |-- Verify images in storage --->|                              |
       |<-- Image list returned --------|                              |
```

#### 6.2.5 Acceptance Criteria

| **AC-ID** | **Criteria** | **Validation Method** |
|-----------|--------------|-----------------------|
| AC-2.1 | The OS image contains the shared Omnia base packages | Boot an OS functional group node and verify presence of kernel, init system, network manager, SSH, time synchronization, NFS client, system logger, sudo |
| AC-2.2 | The OS image contains LDMS telemetry packages (ovis-ldms and dependencies) | Verify ovis-ldms package is installed on a booted OS functional group node |
| AC-2.3 | No Slurm packages are present on an OS functional group node | Verify absence of Slurm, munge on a booted OS functional group node |
| AC-2.4 | No Kubernetes or container runtime packages are present | Verify absence of Kubernetes, container runtime, container interface packages |
| AC-2.5 | No DOCA-OFED, CUDA, NVHPC, or apptainer packages are present | Verify absence of GPU compute and InfiniBand driver packages |
| AC-2.6 | No MPI or communication library packages are present | Verify absence of UCX, OpenMPI packages |
| AC-2.7 | Image is available in object storage after build | Run image verification command and confirm OS image is listed |
| AC-2.8 | Additional packages listed in `additional_packages.json` are present on the provisioned node | Add `podman` to `additional_packages.json`, build image, provision node, verify `rpm -q podman` shows installed |
| AC-2.9 | Image builds successfully when `additional_packages.json` is absent or empty | Remove or empty the file; run image build; verify success with base + LDMS only |
| AC-2.10 | Image build fails with clear error when `additional_packages.json` references unavailable packages | List a non-existent package; run image build; verify RPM dependency resolution error |

#### 6.2.6 Performance

- OS image build time SHALL be less than or equal to the build time for the Slurm or service K8s functional groups, since the OS image contains fewer packages
- Image size SHALL be smaller than Slurm or service K8s images due to the reduced package set

#### 6.2.7 Assets/Resources at Risk

- Package conflicts on downstream platform installation if unexpected packages are present in the image
- Broken downstream deployment if a required base package is missing
- Telemetry gap if LDMS packages are not included, preventing future sampler activation
- Image build failure if the package mapping references undefined or unavailable package definitions

---

### 6.3 Stateless Diskless Provisioning

#### 6.3.1 Marketing User Stories

| **Theme** | **MRD Excerpt / Feature Description** |
|-----------|---------------------------------------|
| Determinism | As a cluster administrator, I need Minimal OS nodes to boot into an identical, deterministic state every time, so that downstream platform installations always start from the same baseline. |
| Simplicity | As an operator, I need Minimal OS nodes to be stateless and diskless so that reprovisioning is as simple as rebooting the node, with no local state to clean up. |

#### 6.3.2 Overview

OS nodes are provisioned as stateless, diskless nodes via network boot. The operating system image is served over HTTP and loaded entirely into RAM. No local disk is used. Every boot produces an identical node state for the same functional group and image version. Reprovisioning requires only a reboot --- no manual cleanup, no disk wiping, no state migration.

#### 6.3.3 Detail

**Network Boot and RAM Loading**

OS nodes SHALL boot via PXE and load the operating system image entirely into RAM from an HTTP-served live image. The root filesystem SHALL be a read-only compressed image. No local disk SHALL be used for the operating system.

**Deterministic State**

Each provisioning cycle (boot) SHALL produce a deterministic, identical node state for the same functional group and image version. Two nodes assigned to the same OS functional group and image version SHALL be indistinguishable after provisioning (aside from network identity).

**Statelessness**

No persistent local state SHALL survive a reboot. The root filesystem in RAM is destroyed on power cycle. The only per-node differentiation is network identity (hostname, admin IP) assigned during provisioning.

**Network Identity Assignment**

The provisioning system SHALL assign each node's hostname and admin IP address per the PXE mapping file. After boot, the node SHALL be reachable via SSH on the assigned admin IP address.

**Concurrent Provisioning**

Multiple OS nodes SHALL be provisionable concurrently without ordering constraints. Provisioning of one node SHALL NOT block or delay provisioning of any other node.

#### 6.3.4 Workflow

```
  Cluster Nodes                    Boot Infrastructure              Administrator
       |                                |                                |
       |-- PXE boot request ----------->|                                |
       |                                |-- Serve kernel + initramfs --->|
       |<-- Load kernel into RAM -------|                                |
       |                                |                                |
       |-- Fetch live image (HTTP) ---->|                                |
       |<-- Image loaded into RAM ------|                                |
       |                                |                                |
       |-- Node initialization runs --->|                                |
       |   (SSH, time sync, hostname)   |                                |
       |                                |                                |
       |-- Node at handoff state ------>|                                |
       |                                |                  SSH into node at admin IP
```

#### 6.3.5 Acceptance Criteria

| **AC-ID** | **Criteria** | **Validation Method** |
|-----------|--------------|-----------------------|
| AC-3.1 | OS node boots successfully via PXE and loads OS into RAM | Power on a node assigned to `os_x86_64` and verify it reaches login prompt |
| AC-3.2 | Node is reachable via SSH on the assigned admin IP after boot | SSH to the admin IP from the OIM after provisioning |
| AC-3.3 | Node hostname matches the PXE mapping file entry | Check hostname on the provisioned node |
| AC-3.4 | Rebooting the node restores identical state (stateless) | Reboot a provisioned OS node; verify identical services, packages, and configuration after reboot |
| AC-3.5 | No local disk is used for the root filesystem | Verify root filesystem is RAM-based and no local disk mounts exist |
| AC-3.6 | Multiple OS nodes provision concurrently without interference | Provision 10+ OS nodes simultaneously; verify all reach handoff state |

#### 6.3.6 Performance

- Boot-to-handoff time SHALL be comparable to the existing default functional group provisioning time; exact targets in the Engineering Specification
- The system SHALL support concurrent provisioning of 100+ OS nodes without serialization
- No single-node provisioning SHALL block or delay other node provisioning

#### 6.3.7 Assets/Resources at Risk

- Extended provisioning time if image size is large or network bandwidth is insufficient
- Boot failure if network infrastructure (DHCP, TFTP, HTTP) is not operational
- RAM exhaustion if the image size exceeds available node memory
- Network identity collisions if PXE mapping file contains duplicate IP or MAC addresses

---

### 6.4 Handoff State Contract for Downstream Consumers

#### 6.4.1 Marketing User Stories

| **Theme** | **MRD Excerpt / Feature Description** |
|-----------|---------------------------------------|
| Contract | As a downstream platform team (e.g., RKE2 deployers), I need a formally defined handoff state so that I know exactly what is and is not present on the node before I begin installing my platform. |
| No Conflicts | As a downstream platform team, I need zero container runtimes, zero scheduler agents, and zero orchestration software on the node so that my platform installation does not encounter package or service conflicts. |

#### 6.4.2 Overview

The handoff state is a formal contract between Omnia provisioning and downstream consumers. After Omnia provisions an OS node, the node is in a guaranteed, documented state. Downstream consumers can rely on this contract to plan their installations without needing to audit every node individually.

#### 6.4.3 Detail

**Network Connectivity**

At handoff, the OS node SHALL have management network connectivity via DHCP and SHALL be reachable via SSH. Root login SHALL be enabled with authorized keys provisioned from the OIM.

**Running Services**

At handoff, the ONLY user-space services running SHALL be:
1. SSH daemon (for remote access)
2. Time synchronization daemon (for clock accuracy)
3. Network manager (for network connectivity)

No other services SHALL be running. Specifically: no scheduler agents, no container runtimes, no orchestration controllers, no telemetry sampler daemons.

**Absent Software**

At handoff, the following categories of software SHALL NOT be present on the node:
- Container runtimes (any container engine or container interface)
- Container orchestration components (Kubernetes, any K8s component)
- Scheduler agents (Slurm, munge)
- GPU compute packages (CUDA, NVHPC)
- InfiniBand drivers (DOCA-OFED)
- Container image formats (apptainer)
- MPI libraries (UCX, OpenMPI)

**Package Manager Functionality**

At handoff, the system package manager SHALL be functional with access to local Omnia repositories. Downstream consumers SHALL be able to install additional packages without configuring external repositories or Internet access.

**Telemetry Packages Present, Services Not Running**

At handoff, LDMS telemetry packages (ovis-ldms and dependencies) SHALL be installed. The LDMS sampler service SHALL NOT be running. This enables downstream consumers or observability teams to activate telemetry sampling at their discretion without requiring additional package installation.

#### 6.4.4 Workflow

```
  Omnia Provisioning              OS Node                       Downstream Consumer
       |                                |                              |
       |-- Provision complete --------->|                              |
       |   (handoff state reached)      |                              |
       |                                |                              |
       |                                |<---- SSH into node ----------|
       |                                |                              |
       |                                |<---- Verify handoff state ---|
       |                                |      (services, packages,    |
       |                                |       package manager)       |
       |                                |                              |
       |                                |<---- Install platform -------|
       |                                |      (e.g., RKE2, custom K8s)|
       |                                |                              |
       |                                |---- Platform running ------->|
```

#### 6.4.5 Acceptance Criteria

| **AC-ID** | **Criteria** | **Validation Method** |
|-----------|--------------|-----------------------|
| AC-4.1 | SSH access is available at handoff with root login via authorized keys | SSH to the node using OIM-provisioned keys |
| AC-4.2 | Only SSH daemon, time synchronization, and network manager are running | List running services and verify exactly three user-space services |
| AC-4.3 | No container runtimes are present | Check for container engine binaries and packages; verify none found |
| AC-4.4 | No Kubernetes components are present | Check for K8s binaries and packages; verify none found |
| AC-4.5 | No Slurm or munge packages are present | Check for Slurm/munge binaries and packages; verify none found |
| AC-4.6 | No DOCA-OFED, CUDA, NVHPC, or apptainer packages are present | Verify absence of GPU/IB/container packages |
| AC-4.7 | Package manager is functional with local repository access | Run a package query or search against local repositories; verify success |
| AC-4.8 | Downstream platform (e.g., RKE2) installs without package conflicts | Install RKE2 or equivalent platform on an OS node; verify clean installation |
| AC-4.9 | LDMS packages are installed but sampler service is not running | Verify ovis-ldms is installed; verify LDMS sampler is not in running services list |

#### 6.4.6 Performance

- Handoff state SHALL be reached within the same time window as existing default functional group provisioning
- Package manager operations (install, query) SHALL complete at comparable speeds to other provisioned nodes accessing the same local repositories

#### 6.4.7 Assets/Resources at Risk

- Downstream deployment failure if unexpected packages or services are present at handoff
- Customer trust erosion if the handoff state is not reproducible or documented inaccurately
- Security exposure if unexpected listening ports are open at handoff
- Operational overhead for downstream teams if they must audit each node rather than trusting the contract

---

### 6.5 Telemetry Readiness (Packages Without Services)

#### 6.5.1 Marketing User Stories

| **Theme** | **MRD Excerpt / Feature Description** |
|-----------|---------------------------------------|
| Observability | As an observability engineer, I need LDMS telemetry packages pre-installed on Minimal OS nodes so that I can activate metric collection without a separate package installation step. |
| Parity | As a cluster administrator, I need the same LDMS package set on Minimal OS nodes as on Slurm worker nodes so that telemetry behavior is consistent across all compute-tier nodes. |

#### 6.5.2 Overview

OS nodes ship with the same LDMS telemetry package set as Slurm worker and login nodes. However, unlike those nodes, the LDMS sampler service is NOT started at boot. This design ensures that downstream consumers receive a clean node with no unexpected running services, while observability teams can activate telemetry at their discretion by simply starting the sampler --- no package installation required.

iDRAC telemetry is out of scope for OS nodes. iDRAC telemetry is container-based and runs on the service Kubernetes cluster, not on individual compute or OS nodes.

#### 6.5.3 Detail

**LDMS Package Parity**

The LDMS package set installed on OS nodes SHALL be identical to the LDMS package set installed on Slurm worker nodes (ovis-ldms and its dependencies). The packages SHALL be installed during image build. No separate installation step SHALL be required post-provisioning.

**No Services at Boot**

The LDMS sampler service SHALL NOT be started, enabled, or configured to auto-start on OS nodes. The provisioning template for OS functional groups SHALL NOT include telemetry service activation commands. This contrasts with Slurm worker nodes, where the provisioning template explicitly starts the LDMS sampler.

**Manual Activation Path**

After handoff, an observability engineer or downstream consumer MAY start the LDMS sampler service manually or via their own automation. The pre-installed packages SHALL be sufficient for the sampler to operate without additional package installation. Configuration of the sampler (aggregator endpoint, sampling interval, etc.) is the responsibility of whoever activates it.

**iDRAC Telemetry Scope**

iDRAC telemetry SHALL NOT be installed on OS nodes. iDRAC telemetry collection is a Kubernetes-based service running on the service cluster. No iDRAC telemetry components, containers, or agents SHALL be present in the OS image or provisioning template.

#### 6.5.4 Workflow

```
  Image Build                     OS Node                       Observability Engineer
       |                                |                              |
       |-- Include LDMS packages ------>|                              |
       |   (in image, not in services)  |                              |
       |                                |                              |
       |                                |-- Boot: LDMS NOT started --->|
       |                                |                              |
       |                                |                (optional, post-handoff)
       |                                |<---- Start LDMS sampler -----|
       |                                |      (manual or automation)  |
       |                                |                              |
       |                                |---- Metrics flowing -------->|
```

#### 6.5.5 Acceptance Criteria

| **AC-ID** | **Criteria** | **Validation Method** |
|-----------|--------------|-----------------------|
| AC-5.1 | LDMS packages (ovis-ldms) are installed on the OS node | Verify ovis-ldms package is present after boot |
| AC-5.2 | LDMS package set is identical to the set on Slurm worker nodes | Compare installed LDMS packages on an OS node vs a Slurm worker node |
| AC-5.3 | LDMS sampler service is NOT running at handoff | Check service status; verify sampler is inactive |
| AC-5.4 | LDMS sampler can be started manually without additional package installation | Start the sampler service on an OS node; verify it starts successfully |
| AC-5.5 | No iDRAC telemetry components are present on the node | Verify absence of iDRAC collector, iDRAC telemetry receiver, or related containers/agents |

#### 6.5.6 Performance

- Telemetry package inclusion SHALL NOT measurably increase image build time (LDMS packages are small relative to the base image)
- LDMS sampler, when manually activated, SHALL exhibit the same performance characteristics as on a Slurm worker node

#### 6.5.7 Assets/Resources at Risk

- Telemetry blind spot if LDMS packages are missing and cannot be installed post-handoff (air-gapped environment)
- Incorrect assumption by downstream consumers that iDRAC telemetry runs on their nodes (it does not --- it is service-cluster-based)
- Unexpected service running if LDMS sampler is mistakenly auto-started at boot, violating the handoff contract

---

### 6.6 Provisioning Error Handling and Validation

#### 6.6.1 Marketing User Stories

| **Theme** | **MRD Excerpt / Feature Description** |
|-----------|---------------------------------------|
| Safety | As a cluster administrator, I need provisioning to fail cleanly on validation errors rather than producing partially configured nodes that are difficult to diagnose and recover. |
| Visibility | As an operator, I need clear error messages when provisioning fails so that I can identify and correct the issue without guessing. |

#### 6.6.2 Overview

Provisioning validation for OS nodes follows the same pipeline as all other functional groups. Architecture mismatches are caught before discovery proceeds. Missing images are detected before nodes attempt to boot. Network boot failures are logged with node identity. In all error cases, the system fails cleanly --- no partially provisioned nodes are left behind.

#### 6.6.3 Detail

**Architecture Mismatch**

When a node's hardware architecture does not match the functional group's architecture suffix (e.g., an AArch64 node assigned to `os_x86_64`), the provisioning system SHALL reject the node at the validation stage. Discovery SHALL NOT proceed for the mismatched node. Other nodes in the same discovery run SHALL NOT be affected.

**Missing Image**

When the required image for an OS functional group is not found in object storage, pre-discovery validation SHALL fail. Discovery SHALL NOT proceed. The error message SHALL identify the missing image and the functional group.

**Network Boot Failure**

When a node fails to retrieve its kernel or initramfs during PXE boot, the failure SHALL be logged with the node's identity (hostname, MAC, IP from the mapping file). The node SHALL remain in an unprovisioned state. No partial configuration SHALL be applied.

**No Post-Provision Validation**

There is no post-provision mechanism to verify what packages or services are running on a node after boot. Exclusion of unwanted packages is enforced at image build time through the inclusion-based package mapping model. This is a known architectural characteristic shared with all Omnia functional groups.

#### 6.6.4 Workflow

```
  Administrator                   Omnia Validation                Cluster Node
       |                                |                              |
       |-- Run discovery -------------->|                              |
       |                                |-- Check architecture match   |
       |                                |   [FAIL: mismatch]           |
       |<-- Error: arch mismatch -------|                              |
       |   "Node X is aarch64 but       |                              |
       |    assigned to os_x86_64"      |                              |
       |                                |                              |
       |-- Fix mapping, re-run -------->|                              |
       |                                |-- Check architecture [PASS]  |
       |                                |-- Check image exists  [PASS] |
       |                                |-- Proceed with discovery --->|
```

#### 6.6.5 Acceptance Criteria

| **AC-ID** | **Criteria** | **Validation Method** |
|-----------|--------------|-----------------------|
| AC-6.1 | Architecture mismatch is detected before discovery proceeds | Assign a mismatched node; verify discovery fails with clear error message |
| AC-6.2 | Architecture mismatch does not affect other nodes in the same discovery run | Include both valid and mismatched nodes; verify valid nodes proceed |
| AC-6.3 | Missing image is detected before discovery proceeds | Remove the OS image from storage; run discovery and verify pre-discovery validation failure |
| AC-6.4 | Network boot failure is logged with node identity | Simulate boot failure; verify log entry includes hostname, MAC, and IP |
| AC-6.5 | No partially provisioned nodes exist after any failure | After each failure scenario, verify the node is in an unprovisioned state |

#### 6.6.6 Performance

- Validation SHALL complete in the same time as validation for any other functional group
- Validation failures SHALL be reported within seconds, not requiring the administrator to wait for a timeout

#### 6.6.7 Assets/Resources at Risk

- Partially provisioned nodes if validation does not fail atomically
- Wasted operator time if error messages do not clearly identify the root cause
- Cascading failures if one node's validation error blocks discovery for all other nodes
- Undetected configuration drift since no post-provision validation exists (accepted architectural limitation)

---

## 7 Cross-Feature Integration

The six features described above are tightly integrated in the following ways:

**Group Definition (6.1) drives Image Composition (6.2):** The functional group name determines which package mapping is used during image build. A node assigned to `os_x86_64` receives the OS package set (base + LDMS + optional additional packages), not the Slurm or service K8s package set.

**Image Composition (6.2) determines Handoff State (6.4):** The packages present in the image directly define what is and is not present at handoff. Since the image uses inclusion-based composition, the handoff guarantee of "no Slurm, no K8s, no container runtimes" is a direct consequence of those packages not being mapped. Administrator-defined additional packages via `additional_packages.json` extend the image without changing the exclusion guarantees.

**Telemetry Readiness (6.5) is a controlled subset of Image Composition (6.2):** LDMS packages are explicitly included in the image, but the provisioning template (which controls boot-time service activation) deliberately does not start the sampler. This separation of "packages in image" vs "services at boot" is the mechanism that delivers the telemetry readiness behavior.

**Provisioning (6.3) relies on Validation (6.6):** Before any node boots, validation ensures architecture match and image availability. The stateless provisioning model ensures that if validation passes, the resulting node state is deterministic.

**Handoff State (6.4) is the integration point with Downstream Consumers:** All other features exist to produce a reliable, documented handoff state. Downstream consumers interact with the handoff state, not with the provisioning pipeline itself.

---

## 8 End-to-End Scenario

**Scenario: Provisioning 50 OS x86_64 Nodes for an RKE2 Deployment**

1. The cluster administrator creates entries in the PXE mapping file for 50 nodes, each with `FUNCTIONAL_GROUP_NAME = os_x86_64`, along with hostnames, admin IPs, admin MACs, and BMC information.

2. The administrator runs the local repository playbook. The system downloads base OS packages and LDMS packages to the local Pulp repository.

3. (Optional) The administrator creates `additional_packages.json` at `input/config/x86_64/rhel/10.0/additional_packages.json` with site-specific packages (e.g., `podman`, diagnostic tools). If skipped, the image proceeds with base + LDMS only.

4. The administrator runs the image build playbook. The system builds an OS image containing the base packages, LDMS telemetry packages, and any additional packages specified. The image is uploaded to object storage.

5. The administrator runs the discovery playbook. The system validates that all 50 nodes are x86_64 hardware (matching the `os_x86_64` suffix). It verifies the OS image exists in storage. It registers all 50 nodes with the boot management system and assigns the OS provisioning group.

6. All 50 nodes PXE boot concurrently. Each node loads the live image into RAM, runs the common provisioning template (SSH, time sync), and runs the OS group template (root user only, no services started). All 50 nodes reach handoff state.

7. The administrator verifies: SSH access works, only SSH/time-sync/network-manager are running, no Slurm/K8s/container-runtime packages are present, LDMS packages are installed but sampler is not running, any additional packages are installed, package manager can query local repos.

8. The downstream RKE2 team SSHes into all 50 nodes and runs their platform installer. RKE2 installs cleanly without package conflicts. The observability team later activates the LDMS sampler on all 50 nodes.

---

## 9 Approvals

| **Role** | **Name** | **Date** | **Signature** |
|----------|----------|----------|---------------|
| Product Management | | | |
| Engineering Lead | | | |
| QA Lead | | | |
| Architecture | | | |
