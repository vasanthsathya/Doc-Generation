# Component Specification --- Minimal OS-Only Functional Group

| | |
|---|---|
| **Document ID** | CSPEC-9294-2026-001 |
| **Capability** | 9294 |
| **Version** | 1.2 |
| **Date** | 04/09/2026 |
| **Author** | Abhishek S A |
| **Team** | Dell Omnia |
| **Document Type** | Component Specification |
| **SDD Phase** | 5a --- Component Specification |
| **Status** | Draft --- For Review |

---

**Dell Confidential - Internal Use Only**

Copyright 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

---

## Revision History

| Version | Date | Description | Author(s) |
|---------|------|-------------|-----------|
| 1.0 | 04/03/2026 | Initial component spec. Decomposes ESPEC-9294-2026-001 v0.2 into 8 change descriptors with before/after code, function-level flows, interface contracts, and data models. | AI-assisted (human review required) |
| 1.1 | 04/07/2026 | **Aligned with ESPEC v0.3:** (1) Renamed functional groups from `minimal_x86_64`/`minimal_aarch64` to `os_x86_64`/`os_aarch64` across all CDs. (2) Updated DESCRIPTION_MAP key from `"minimal"` to `"os"`. (3) CD-03 software_map now includes `default_packages.json` explicitly; `admin_debug_packages.json` excluded from os_* groups. (4) Added CD-09 (Additional Packages JSON file) and CD-10 (Software Map update for additional_packages.json). (5) Updated dependency matrix, traceability, and component interaction diagram. | AI-assisted (human review required) |
| 1.2 | 04/09/2026 | **Aligned with ESPEC v0.4:** (1) CD-10 rewritten --- `additional_packages.json` is now an **independent optional flow** loaded separately by the package collector, NOT listed in `software_map`. (2) Updated CD-09 interface contract to reflect independent loading. (3) Updated DESCRIPTION_MAP value from `"Minimal OS Node"` to `"OS Node"` per ESPEC. (4) Updated component interaction diagram, dependency matrix, and traceability references. | AI-assisted (human review required) |

---

## Table of Contents

- [1 References](#1-references)
- [2 Scope](#2-scope)
- [3 Component Inventory](#3-component-inventory)
- [4 Component Details](#4-component-details)
  - [4.1 CD-01: JSON Schema Update](#41-cd-01-json-schema-update)
  - [4.2 CD-02: Functional Group Layer Map Update](#42-cd-02-functional-group-layer-map-update)
  - [4.3 CD-03: Software Package Mapping Update](#43-cd-03-software-package-mapping-update)
  - [4.4 CD-04: Role Layer Classification Update](#44-cd-04-role-layer-classification-update)
  - [4.5 CD-05: Functional Group Generator Update](#45-cd-05-functional-group-generator-update)
  - [4.6 CD-06: Cloud-Init Provisioning Templates](#46-cd-06-cloud-init-provisioning-templates)
  - [4.7 CD-07: OpenCHAMI Image Compute Commands](#47-cd-07-openchami-image-compute-commands)
  - [4.8 CD-08: PXE Mapping File Template Update](#48-cd-08-pxe-mapping-file-template-update)
  - [4.9 CD-09: Additional Packages JSON File](#49-cd-09-additional-packages-json-file)
  - [4.10 CD-10: Additional Packages Independent Flow](#410-cd-10-additional-packages-independent-flow)
- [5 Component Interaction Diagram](#5-component-interaction-diagram)
- [6 Dependency Matrix](#6-dependency-matrix)
- [7 Traceability](#7-traceability)

---

## 1. References

| Source | ID | Description |
|--------|----|-------------|
| Engineering Spec (HLD) | ESPEC-9294-2026-001 v0.4 | Parent spec --- defines HOW at architecture level; this document provides the code-level detail |
| Test Spec | TSPEC-9294-2026-001 v1.0 | Test cases mapped to each component |
| Functional Spec | FSPEC-9294-2026-001 v1.0 | System behavior requirements |
| Behaviour Spec | BSPEC-9294-2026-001 v1.0 | Customer-facing acceptance criteria |
| Codebase | Omnia 2.1.0 (`pub/build_stream`) | Implementation target |

---

## 2. Scope

This Component Specification decomposes the Engineering Spec (HLD) into code-level change descriptors. For each of the 10 change descriptors (CD-01 through CD-10), it provides:

- Exact file path and line references
- Before/after code snippets
- Function-level control flow through the code
- Interface contracts (inputs, outputs, error behavior)
- Data model changes
- Dependencies on other components

This is the document that a developer reads immediately before writing code. The HLD tells you **what to change and why**; this document tells you **exactly where and how**.

---

## 3. Component Inventory

| CD | Component | File | Change | Complexity |
|----|-----------|------|--------|------------|
| CD-01 | JSON Schema | `common/library/module_utils/input_validation/schema/functional_groups_config.json` | Modify enum | Low |
| CD-02 | Layer Map | `common/library/module_utils/input_validation/common_utils/config.py` | Add dict entries | Low |
| CD-03 | Software Map | `common/library/modules/image_package_collector.py` | Replace/add dict entries | Low |
| CD-04 | Role Classification | `common/library/modules/fetch_roles_config.py` | Modify set | Low |
| CD-05 | FG Generator | `common/library/modules/generate_functional_groups.py` | Add dict entry | Low |
| CD-06a | Cloud-Init Template (x86) | `discovery/roles/configure_ochami/templates/cloud_init/ci-group-default_x86_64.yaml.j2` | Rename file | Low |
| CD-06b | Cloud-Init Template (arm) | `discovery/roles/configure_ochami/templates/cloud_init/ci-group-os_aarch64.yaml.j2` | Create file | Low |
| CD-07 | Compute Commands | `common/vars/openchami_image_cmd.yml` | Rename variables | Low |
| CD-08 | PXE Mapping Example | `input/pxe_mapping_file.csv` | Add example row | Low |
| CD-09 | Additional Packages | `input/config/{arch}/rhel/10.0/additional_packages.json` | Create file | Low |
| CD-10 | Addl Pkgs (independent flow) | `common/library/modules/image_package_collector.py` | Add independent load logic | Low |

---

## 4. Component Details

### 4.1 CD-01: JSON Schema Update

**File:** `common/library/module_utils/input_validation/schema/functional_groups_config.json`

#### 4.1.1 Responsibility

Defines the set of valid functional group names that user-provided `functional_groups_config.yml` files may contain. Any name not in the `enum` array is rejected by the JSON schema validator.

#### 4.1.2 Interface Contract

| Interface | Direction | Type | Description |
|-----------|-----------|------|-------------|
| `functional_groups[].name` enum | Provided | JSON Schema | Constrains valid FG name values for all downstream consumers |
| Schema validation framework | Required | Python (jsonschema) | Loads this schema and validates user YAML |

#### 4.1.3 Code Change

**Before (line ~39):**
```json
"enum": [
  "default_x86_64",
  "service_kube_node_x86_64",
  "service_kube_control_plane_x86_64",
  "service_kube_control_plane_first_x86_64",
  "login_node_x86_64",
  "login_node_aarch64",
  "login_compiler_node_x86_64",
  "login_compiler_node_aarch64",
  "slurm_control_node_x86_64",
  "default_aarch64",
  "slurm_node_x86_64",
  "slurm_node_aarch64"
]
```

**After:**
```json
"enum": [
  "os_x86_64",
  "service_kube_node_x86_64",
  "service_kube_control_plane_x86_64",
  "service_kube_control_plane_first_x86_64",
  "login_node_x86_64",
  "login_node_aarch64",
  "login_compiler_node_x86_64",
  "login_compiler_node_aarch64",
  "slurm_control_node_x86_64",
  "os_aarch64",
  "slurm_node_x86_64",
  "slurm_node_aarch64"
]
```

#### 4.1.4 Execution Flow

```
User provides functional_groups_config.yml
    │
    ▼
Schema Validator (jsonschema library)
    │
    ├── Load functional_groups_config.json schema
    ├── For each entry in functional_groups[]:
    │     ├── Validate .name against enum array
    │     │     ├── "os_x86_64" → IN enum → PASS
    │     │     ├── "default_x86_64" → NOT IN enum → FAIL
    │     │     └── "slurm_node_x86_64" → IN enum → PASS (unchanged)
    │     └── Validate other fields (.nodes, .group_name, etc.)
    └── Return: validation pass or ValidationError with path
```

#### 4.1.5 Error Behavior

| Condition | Error | Message Pattern |
|-----------|-------|-----------------|
| FG name not in enum | `jsonschema.ValidationError` | `"'default_x86_64' is not one of ['os_x86_64', ...]"` |

#### 4.1.6 Dependencies

| Depends On | Reason |
|-----------|--------|
| None | Schema is the entry point; no upstream dependencies |

#### 4.1.7 Test Cases

TC-1.01, TC-1.02, TC-1.20, TC-1.21

---

### 4.2 CD-02: Functional Group Layer Map Update

**File:** `common/library/module_utils/input_validation/common_utils/config.py`

#### 4.2.1 Responsibility

`FUNCTIONAL_GROUP_LAYER_MAP` is the **single source of truth** for:
1. Whether a functional group name is recognized (validation)
2. Which provisioning layer a group belongs to (`"management"` or `"compute"`)

This is the **most critical change**. All validation, generation, and build components import this dictionary.

#### 4.2.2 Interface Contract

| Interface | Direction | Consumer | Description |
|-----------|-----------|----------|-------------|
| `FUNCTIONAL_GROUP_LAYER_MAP` dict | Provided | `provision_validation.py` | FG name lookup for PXE mapping validation |
| `FUNCTIONAL_GROUP_LAYER_MAP` dict | Provided | `generate_functional_groups.py` | FG filtering during YAML generation |
| `FUNCTIONAL_GROUP_LAYER_MAP` dict | Provided | `build_yaml()` | Layer classification for description generation |

#### 4.2.3 Code Change

**Before (lines ~182--193):**
```python
FUNCTIONAL_GROUP_LAYER_MAP = {
    "service_kube_control_plane_first_x86_64": "management",
    "service_kube_control_plane_x86_64": "management",
    "service_kube_node_x86_64": "management",
    "login_node_x86_64": "management",
    "login_node_aarch64": "management",
    "login_compiler_node_x86_64": "management",
    "login_compiler_node_aarch64": "management",
    "slurm_control_node_x86_64": "management",
    "slurm_node_x86_64": "compute",
    "slurm_node_aarch64": "compute"
}
```

**After:**
```python
FUNCTIONAL_GROUP_LAYER_MAP = {
    "service_kube_control_plane_first_x86_64": "management",
    "service_kube_control_plane_x86_64": "management",
    "service_kube_node_x86_64": "management",
    "login_node_x86_64": "management",
    "login_node_aarch64": "management",
    "login_compiler_node_x86_64": "management",
    "login_compiler_node_aarch64": "management",
    "slurm_control_node_x86_64": "management",
    "slurm_node_x86_64": "compute",
    "slurm_node_aarch64": "compute",
    "os_x86_64": "compute",
    "os_aarch64": "compute"
}
```

#### 4.2.4 Execution Flow --- Validation Path

```
provision_validation.py :: validate_functional_groups_in_mapping_file()
    │
    │  (line ~474)
    ├── for row_idx, row in enumerate(csv_rows):
    │     fg = row["FUNCTIONAL_GROUP_NAME"]
    │     │
    │     ├── if fg not in config.FUNCTIONAL_GROUP_LAYER_MAP.keys():
    │     │     raise ValueError(
    │     │       f"unrecognized functional group name '{fg}' at CSV row {row_idx}"
    │     │     )
    │     │
    │     └── else: continue  ← "os_x86_64" found → PASS
    │
    └── All rows validated → return success
```

#### 4.2.5 Execution Flow --- Generation Path

```
generate_functional_groups.py :: main()
    │
    │  (line ~83)
    ├── for func_group in unique_fg_names_from_csv:
    │     │
    │     ├── if func_group in config.FUNCTIONAL_GROUP_LAYER_MAP:
    │     │     │
    │     │     └── build_yaml(func_group, ...)
    │     │           │
    │     │           ├── layer = config.FUNCTIONAL_GROUP_LAYER_MAP[func_group]
    │     │           │   → "os_x86_64" → "compute"
    │     │           │
    │     │           ├── desc_key = next(
    │     │           │     (k for k in DESCRIPTION_MAP if func_group.startswith(k)),
    │     │           │     func_group
    │     │           │   )
    │     │           │   → "os" matches "os_x86_64" → "OS Node"
    │     │           │
    │     │           └── cluster_name = (
    │     │                 kube_cluster_name if "kube" in fg_lower
    │     │                 else slurm_cluster_name or "slurm_cluster"
    │     │               )
    │     │               → "kube" NOT in "os_x86_64" → slurm_cluster_name
    │     │
    │     └── else: silently dropped (not in map)
    │
    └── Output: functional_groups_config.yml
```

#### 4.2.6 Execution Flow --- Parent Service Tag Path

```
provision_validation.py :: validate_parent_service_tag_hierarchy()
    │
    │  (lines ~480--506)
    ├── for row in csv_rows:
    │     fg = row["FUNCTIONAL_GROUP_NAME"]
    │     layer = config.FUNCTIONAL_GROUP_LAYER_MAP.get(fg)
    │     │
    │     ├── if layer == "management":
    │     │     → PARENT_SERVICE_TAG must be empty or valid
    │     │
    │     └── if layer == "compute":
    │           → PARENT_SERVICE_TAG is optional
    │           → "os_x86_64" → "compute" → optional → PASS
    │
    └── return
```

#### 4.2.7 Error Behavior

| Condition | Error | Function |
|-----------|-------|----------|
| FG not in map | `ValueError("unrecognized functional group name '{fg}' at CSV row {row_idx}")` | `validate_functional_groups_in_mapping_file()` |
| FG not in map | Silently dropped from YAML output | `generate_functional_groups.py` |

#### 4.2.8 Dependencies

| Depends On | Reason |
|-----------|--------|
| None | This is the root dependency; all other components depend on it |

#### 4.2.9 Test Cases

TC-1.03, TC-1.04, TC-1.05, TC-1.06, TC-1.11, TC-1.22, TC-1.23

---

### 4.3 CD-03: Software Package Mapping Update

**File:** `common/library/modules/image_package_collector.py`

#### 4.3.1 Responsibility

Maps each functional group to its list of JSON package definition files. For os_* groups, the software_map includes `default_packages.json` explicitly (no separate base package loading) and excludes `admin_debug_packages.json`. The package collector loads these files, combines them, and produces the final deduplicated package list for image building.

#### 4.3.2 Interface Contract

| Interface | Direction | Type | Description |
|-----------|-----------|------|-------------|
| `software_map` dict | Provided | Python dict | Maps FG name → list of JSON filenames |
| `input/config/{arch}/rhel/10.0/*.json` | Required | JSON files | Package definition files loaded by the collector |
| `compute_images_dict` | Provided | Python dict | Output: FG name → final package list |

#### 4.3.3 Code Change

**Before (lines ~234--251):**
```python
software_map = {
    "default_x86_64": ["openldap.json"],
    "service_kube_node_x86_64": ["service_k8s.json"],
    "service_kube_control_plane_x86_64": ["service_k8s.json"],
    "service_kube_control_plane_first_x86_64": ["service_k8s.json"],
    "login_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "login_node_aarch64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "login_compiler_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json", "ucx.json", "openmpi.json"],
    "login_compiler_node_aarch64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "slurm_control_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "slurm_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "slurm_node_aarch64": ["slurm_custom.json", "openldap.json", "ldms.json"],
}
```

**After:**
```python
software_map = {
    "os_x86_64": ["default_packages.json", "ldms.json"],
    "os_aarch64": ["default_packages.json", "ldms.json"],
    "service_kube_node_x86_64": ["service_k8s.json"],
    "service_kube_control_plane_x86_64": ["service_k8s.json"],
    "service_kube_control_plane_first_x86_64": ["service_k8s.json"],
    "login_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "login_node_aarch64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "login_compiler_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json", "ucx.json", "openmpi.json"],
    "login_compiler_node_aarch64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "slurm_control_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "slurm_node_x86_64": ["slurm_custom.json", "openldap.json", "ldms.json"],
    "slurm_node_aarch64": ["slurm_custom.json", "openldap.json", "ldms.json"],
}
```

**Key changes:**
1. `"default_x86_64": ["openldap.json"]` → `"os_x86_64": ["default_packages.json", "ldms.json"]` (rename + replace mapping; `default_packages.json` included explicitly, `admin_debug_packages.json` excluded)
2. Added `"os_aarch64": ["default_packages.json", "ldms.json"]` (new entry)
3. `openldap.json` removed from all os_* entries
4. `admin_debug_packages.json` is NOT included for os_* groups (other FGs still include it via the shared base image layer)

#### 4.3.4 Execution Flow --- Package Resolution

```
image_package_collector.py :: collect_packages(fg_name)
    │
    │  (line ~257)
    ├── Detect architecture from FG name suffix:
    │     if fg_name.endswith("_x86_64"):
    │         arch = "x86_64"
    │     elif fg_name.endswith("_aarch64"):
    │         arch = "aarch64"
    │     → "os_x86_64" → arch = "x86_64"
    │
    ├── Load FG-specific packages from software_map:
    │     fg_json_files = software_map.get(fg_name, [])
    │     → software_map["os_x86_64"] = ["default_packages.json", "ldms.json"]
    │     │
    │     for json_file in fg_json_files:
    │         fg_pkgs += load_json(base_path + json_file)
    │     → Loads: input/config/x86_64/rhel/10.0/default_packages.json
    │       Contains: kernel, dracut, systemd, NetworkManager, iproute, ...
    │     → Loads: input/config/x86_64/rhel/10.0/ldms.json
    │       Contains: python3-devel, python3-cython, openssl-libs, ovis-ldms
    │
    │  NOTE: For os_* groups, default_packages.json is loaded via software_map
    │        (not via a separate base package step). admin_debug_packages.json
    │        is NOT loaded for os_* groups. additional_packages.json is loaded
    │        separately as an independent optional flow (see CD-10).
    │
    ├── Combine all package lists:
    │     all_pkgs = fg_pkgs   (default_packages + ldms only; no admin_debug)
    │
    ├── Deduplicate:
    │     final_pkgs = list(set(all_pkgs))
    │
    └── Output: compute_images_dict["os_x86_64"] = final_pkgs
```

#### 4.3.5 Data Model --- Package Composition

```
os_x86_64 final package list:
┌──────────────────────────────────────────────────────────┐
│ base (default_packages.json — via software_map):         │
│   kernel, dracut, systemd, NetworkManager, iproute,      │
│   nfs-utils, rsyslog, chrony, sudo, openssh-server, ...  │
├──────────────────────────────────────────────────────────┤
│ FG-specific (ldms.json — via software_map):               │
│   python3-devel, python3-cython, openssl-libs, ovis-ldms │
├──────────────────────────────────────────────────────────┤
│ Optional (additional_packages.json — independent flow):  │
│   podman, podman-docker, skopeo, ... (if file present)   │
├──────────────────────────────────────────────────────────┤
│ NOT included (excluded from os_* groups):                │
│   ✗ admin_debug_packages.json: diagnostic/admin utils    │
│   ✗ openldap.json: openldap-clients, sssd, nss-pam-ldapd│
└──────────────────────────────────────────────────────────┘
```

#### 4.3.6 Error Behavior

| Condition | Behavior |
|-----------|----------|
| FG not in `software_map` | FG gets only base packages (no FG-specific); silent fallback |
| JSON file not found | `FileNotFoundError` raised by `load_json()` |

#### 4.3.7 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-02 (`FUNCTIONAL_GROUP_LAYER_MAP`) | FG must be in layer map for image build pipeline to reach the package collector |
| `input/config/{arch}/rhel/10.0/ldms.json` | Must exist (pre-condition; already present per ESPEC Assumption A-01) |

#### 4.3.8 Test Cases

TC-2.01, TC-2.02, TC-2.03, TC-2.04, TC-2.05, TC-2.06, TC-2.30, TC-2.31

---

### 4.4 CD-04: Role Layer Classification Update

**File:** `common/library/modules/fetch_roles_config.py`

#### 4.4.1 Responsibility

Classifies functional groups into provisioning layers via the `SECOND_LAYER_ROLES` set. The `validate_roles()` function uses this set to enforce that roles belong to either management or compute layer (not both).

#### 4.4.2 Interface Contract

| Interface | Direction | Consumer | Description |
|-----------|-----------|----------|-------------|
| `SECOND_LAYER_ROLES` set | Provided | `validate_roles()` | Determines which FGs are compute-layer |

#### 4.4.3 Code Change

**Before (line ~27):**
```python
SECOND_LAYER_ROLES = {"default_x86_64", "slurm_node_x86_64", "slurm_node_aarch64"}
```

**After:**
```python
SECOND_LAYER_ROLES = {"os_x86_64", "os_aarch64", "slurm_node_x86_64", "slurm_node_aarch64"}
```

#### 4.4.4 Execution Flow

```
fetch_roles_config.py :: validate_roles(assigned_roles)
    │
    ├── management_roles = assigned_roles - SECOND_LAYER_ROLES
    │     → Any FG NOT in SECOND_LAYER_ROLES is considered management
    │
    ├── compute_roles = assigned_roles & SECOND_LAYER_ROLES
    │     → "os_x86_64" ∈ SECOND_LAYER_ROLES → compute_roles includes it
    │
    ├── Validate: no role in both management and compute
    │
    └── Validate: at least one role in expected layer
```

#### 4.4.5 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-02 | Layer map and role classification must be consistent |

#### 4.4.6 Test Cases

TC-1.07, TC-1.08

---

### 4.5 CD-05: Functional Group Generator Update

**File:** `common/library/modules/generate_functional_groups.py`

#### 4.5.1 Responsibility

`DESCRIPTION_MAP` maps functional group base names (without architecture suffix) to human-readable descriptions used in the generated `functional_groups_config.yml`.

#### 4.5.2 Interface Contract

| Interface | Direction | Consumer | Description |
|-----------|-----------|----------|-------------|
| `DESCRIPTION_MAP` dict | Provided | `build_yaml()` | Description string for generated YAML |

#### 4.5.3 Code Change

**Before (lines ~15--23):**
```python
DESCRIPTION_MAP = {
    "slurm_control_node": "Slurm Head",
    "slurm_node": "Slurm Worker",
    "login_node": "Login Node",
    "login_compiler_node": "Login Compiler Node",
    "service_kube_control_plane_first": "Kubernetes Control Plane (Primary)",
    "service_kube_control_plane": "Kubernetes Control Plane",
    "service_kube_node": "Kubernetes Worker Node"
}
```

**After:**
```python
DESCRIPTION_MAP = {
    "os": "OS Node",
    "slurm_control_node": "Slurm Head",
    "slurm_node": "Slurm Worker",
    "login_node": "Login Node",
    "login_compiler_node": "Login Compiler Node",
    "service_kube_control_plane_first": "Kubernetes Control Plane (Primary)",
    "service_kube_control_plane": "Kubernetes Control Plane",
    "service_kube_node": "Kubernetes Worker Node"
}
```

#### 4.5.4 Execution Flow --- Description Lookup

```
build_yaml(func_group="os_x86_64", ...)
    │
    ├── desc_key = next(
    │     (k for k in DESCRIPTION_MAP if func_group.startswith(k)),
    │     func_group   ← fallback if no match
    │   )
    │   │
    │   ├── "os": "os_x86_64".startswith("os") → True → MATCH
    │   └── desc_key = "os"
    │
    ├── description = DESCRIPTION_MAP[desc_key]
    │   → "OS Node"
    │
    └── YAML entry: {name: os_x86_64, description: "OS Node", ...}
```

**Note:** `"os"` is placed first in the dict. The `next()` iterator returns the first match. Since `"os"` is not a prefix of any other key (`"slurm_*"`, `"login_*"`, `"service_*"`), ordering does not cause conflicts. However, placing it first ensures predictable behavior.

#### 4.5.5 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-02 | FG must pass the `FUNCTIONAL_GROUP_LAYER_MAP` filter before `build_yaml()` is called |

#### 4.5.6 Test Cases

TC-1.09, TC-1.10, TC-1.24

---

### 4.6 CD-06: Cloud-Init Provisioning Templates

**Directory:** `discovery/roles/configure_ochami/templates/cloud_init/`

#### 4.6.1 Responsibility

Cloud-init templates define per-functional-group provisioning configuration applied at boot. The template filename must exactly match `ci-group-{functional_group_name}.yaml.j2`.

#### 4.6.2 Interface Contract

| Interface | Direction | Type | Description |
|-----------|-----------|------|-------------|
| Template file at `cloud_init/ci-group-{fg_name}.yaml.j2` | Provided | Jinja2 file | Loaded dynamically by `configure_cloud_init_group.yml` |
| `functional_group_name` | Required | Ansible variable | Set by calling task; used in dynamic path construction |
| `read_ssh_key.stdout` | Required | Ansible variable | OIM SSH public key |
| `hashed_password_output.stdout` | Required | Ansible variable | Root password hash |

#### 4.6.3 CD-06a: Rename x86_64 Template

**Action:** File rename via `git mv`:
```
ci-group-default_x86_64.yaml.j2  →  ci-group-os_x86_64.yaml.j2
```

Content **unchanged**:

```yaml
- name: {{ functional_group_name }}
  description: "{{ functional_group_name }} config"
  file:
    encoding: plain
    content: |
      ## template: jinja
      #cloud-config
      merge_how:
      - name: list
        settings: [append]
      - name: dict
        settings: [no_replace, recurse_list]
      users:
        - name: root
          ssh_authorized_keys: "{{ read_ssh_key.stdout }}"
          lock_passwd: false
          hashed_passwd: "{{ hashed_password_output.stdout }}"
      disable_root: false
```

#### 4.6.4 CD-06b: Create aarch64 Template

**Action:** Create new file `ci-group-os_aarch64.yaml.j2` with identical content to the x86_64 template above.

**Rationale:** The Minimal OS cloud-init template is architecture-independent (SSH root user setup only). Architecture-specific behavior is handled by the image composition layer, not cloud-init.

#### 4.6.5 Execution Flow --- Template Loading

```
discovery/roles/configure_ochami/tasks/main.yml
    │
    ├── with_items: "{{ functional_groups | map(attribute='name') | list }}"
    │     → Iterates: ["os_x86_64", "slurm_node_x86_64", ...]
    │
    └── For each item:
          │
          ├── create_groups.yml
          │     └── Create OpenCHAMI group via API
          │
          └── configure_cloud_init_group.yml
                │
                ├── set_fact: functional_group_name = "os_x86_64"
                │
                ├── template:
                │     src: "cloud_init/ci-group-{{ functional_group_name }}.yaml.j2"
                │     → resolves to: cloud_init/ci-group-os_x86_64.yaml.j2
                │
                ├── Jinja2 renders template with variables:
                │     {{ functional_group_name }} → "os_x86_64"
                │     {{ read_ssh_key.stdout }} → "ssh-rsa AAAA..."
                │     {{ hashed_password_output.stdout }} → "$6$..."
                │
                ├── Push rendered config to OpenCHAMI cloud-init API
                │
                └── rescue:
                      └── msg: "{{ ci_group_load_fail_msg }}"
```

#### 4.6.6 What the Template Does NOT Do

| Excluded Action | Rationale | FSpec Trace |
|----------------|-----------|-------------|
| No `runcmd` block | No services started at boot | FS-EX-04 |
| No `packages` block | Packages come from image, not cloud-init | FS-IC-01 |
| No LDMS sampler start | Telemetry packages installed, not activated | FS-HS-04 |
| No openldap/sssd config | No directory services in Minimal OS | FS-EX-02 |

#### 4.6.7 Error Behavior

| Condition | Behavior |
|-----------|----------|
| Template file missing | Ansible rescue block logs `ci_group_load_fail_msg`; task fails |
| Variable undefined | Jinja2 `UndefinedError`; task fails |

#### 4.6.8 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-02 | FG must be in layer map for discovery pipeline to iterate over it |

#### 4.6.9 Test Cases

TC-7.01, TC-7.02, TC-6.20

---

### 4.7 CD-07: OpenCHAMI Image Compute Commands

**File:** `common/vars/openchami_image_cmd.yml`

#### 4.7.1 Responsibility

Defines per-functional-group command variables that the Jinja2 compute image template resolves during image build. The template uses `lookup('vars', fg_name + '_compute_commands', default=[])`.

#### 4.7.2 Interface Contract

| Interface | Direction | Type | Description |
|-----------|-----------|------|-------------|
| `{fg_name}_compute_commands` variable | Provided | Ansible variable (list) | Commands executed during compute image build |
| Compute image template (`compute_images_templates.j2`) | Consumer | Jinja2 | Resolves variable by name pattern |

#### 4.7.3 Code Change

**Before (lines ~24--29):**
```yaml
#  x86_64 compute commands
default_x86_64_compute_commands:
  - "echo 'Default x86_64 compute'"

default_aarch64_compute_commands:
  - "echo 'Default aarch64 compute'"
```

**After:**
```yaml
#  x86_64 compute commands
os_x86_64_compute_commands:
  - "echo 'Minimal OS x86_64 compute'"

# aarch64 compute commands
os_aarch64_compute_commands:
  - "echo 'Minimal OS aarch64 compute'"
```

#### 4.7.4 Execution Flow --- Variable Resolution

```
compute_images_templates.j2
    │
    ├── {% set command_var = functional_group + '_compute_commands' %}
    │   → functional_group = "os_x86_64"
    │   → command_var = "os_x86_64_compute_commands"
    │
    ├── {% set commands_list = lookup('vars', command_var, default=[]) %}
    │   → Looks up variable "os_x86_64_compute_commands"
    │   → Found → ["echo 'Minimal OS x86_64 compute'"]
    │
    └── {% for cmd in commands_list %}
          {{ cmd }}
        {% endfor %}
        → Executes: echo 'Minimal OS x86_64 compute'
```

#### 4.7.5 Error Behavior

| Condition | Behavior |
|-----------|----------|
| Variable not defined | `lookup('vars', ..., default=[])` returns `[]`; no commands executed (no failure) |

#### 4.7.6 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-02 | FG must pass layer map for build pipeline to reach compute commands |

#### 4.7.7 Test Cases

TC-7.01, TC-7.02

---

### 4.8 CD-08: PXE Mapping File Template Update

**File:** `input/pxe_mapping_file.csv`

#### 4.8.1 Responsibility

Provides an example/template CSV that administrators copy and modify when assigning nodes to functional groups.

#### 4.8.2 Interface Contract

| Interface | Direction | Type | Description |
|-----------|-----------|------|-------------|
| CSV file content | Provided | CSV template | Used by administrators as a starting point |

#### 4.8.3 Code Change

**Before:**
```csv
FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,PARENT_SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
slurm_control_node_x86_64,grp0,ABCD12,,slurm-control-node1,...
```

**After:**
```csv
FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,PARENT_SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
slurm_control_node_x86_64,grp0,ABCD12,,slurm-control-node1,...
os_x86_64,grp5,ABEF56,,minimal-node1,xx:yy:zz:aa:bb:ff,172.16.107.60,xx:yy:zz:aa:bb:ee,172.17.107.60
```

#### 4.8.4 Data Model --- CSV Row

| Column | Value | Notes |
|--------|-------|-------|
| FUNCTIONAL_GROUP_NAME | `os_x86_64` | Must match schema enum |
| GROUP_NAME | `grp5` | User-defined group name |
| SERVICE_TAG | `ABEF56` | Dell service tag |
| PARENT_SERVICE_TAG | (empty) | Optional for compute layer |
| HOSTNAME | `minimal-node1` | Assigned hostname |
| ADMIN_MAC | `xx:yy:zz:aa:bb:ff` | Admin NIC MAC |
| ADMIN_IP | `172.16.107.60` | Admin network IP |
| BMC_MAC | `xx:yy:zz:aa:bb:ee` | BMC/iDRAC MAC |
| BMC_IP | `172.17.107.60` | BMC/iDRAC IP |

#### 4.8.5 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-01 | FG name must be in schema enum for validation to accept it |

#### 4.8.6 Test Cases

TC-1.03 (used as input)

---

### 4.9 CD-09: Additional Packages JSON File

**File:** `input/config/{arch}/rhel/10.0/additional_packages.json`

#### 4.9.1 Responsibility

Provides a user-editable JSON file where administrators can define additional RPM packages to be installed on os_* functional group nodes. This enables extensibility without modifying the core software map or cloud-init templates.

#### 4.9.2 Interface Contract

| Interface | Direction | Type | Description |
|-----------|-----------|------|-------------|
| `additional_packages.json` | Provided | JSON file | Package definition following the same schema as `ldms.json` |
| `image_package_collector.py` | Consumer | Python | Loads this file independently (not via software_map) when building os_* images; gracefully skips if absent |

#### 4.9.3 Code Change

**Action:** Create new files:
- `input/config/x86_64/rhel/10.0/additional_packages.json`
- `input/config/aarch64/rhel/10.0/additional_packages.json`

**Initial content (empty — no additional packages by default):**
```json
{
  "packages": []
}
```

**Example with packages (administrator-customized):**
```json
{
  "packages": [
    "podman",
    "podman-docker",
    "skopeo"
  ]
}
```

#### 4.9.4 Data Model --- JSON Schema

```
additional_packages.json
{
  "packages": [             ← Array of RPM package names (strings)
    "<package-name>",       ← Must be available in local Pulp repository
    ...                     ← for the target architecture
  ]
}
```

Same schema as `ldms.json`, `openldap.json`, and other package definition files.

#### 4.9.5 Graceful Fallback Behavior

| Condition | Behavior |
|-----------|----------|
| File does not exist | Package collector skips it; os_* gets `default_packages.json` + `ldms.json` only (graceful, no error) |
| File exists, `"packages": []` | Empty list merged; no additional packages installed |
| File exists, valid packages | Packages merged into the compute image alongside default + LDMS |
| File exists, invalid JSON | `json.JSONDecodeError` raised by `load_json()` |

#### 4.9.6 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-10 | Package collector must have the independent load logic (CD-10) to discover and load this file |

#### 4.9.7 Test Cases

TC-2.30, TC-2.31

---

### 4.10 CD-10: Additional Packages Independent Flow

**File:** `common/library/modules/image_package_collector.py`

#### 4.10.1 Responsibility

Adds separate logic in the package collector to check for `additional_packages.json` at `input/config/{arch}/rhel/10.0/additional_packages.json`, load and merge its packages if present, and gracefully skip if absent. This file is **NOT** added to `software_map` --- it is loaded as an independent optional flow outside the normal software_map resolution.

#### 4.10.2 Interface Contract

| Interface | Direction | Type | Description |
|-----------|-----------|------|-------------|
| Independent load logic in `collect_packages()` | Added | Python code | Checks for `additional_packages.json` after software_map resolution; loads and merges if present |
| `additional_packages.json` | Required (optional) | JSON file | If present, packages are merged; if absent, gracefully skipped |
| `software_map` dict | **Unchanged** | Python dict | os_* entries remain `["default_packages.json", "ldms.json"]` only |

#### 4.10.3 Code Change

**The `software_map` is NOT modified.** Instead, add logic after the software_map package resolution to independently check for and load `additional_packages.json`:

**Added logic (after software_map resolution, within `collect_packages()`):**
```python
# Independent optional flow: load additional_packages.json if present
# NOT part of software_map — loaded separately for os_* groups
addl_pkg_path = os.path.join(base_path, arch, "rhel", "10.0", "additional_packages.json")
if os.path.exists(addl_pkg_path):
    try:
        addl_pkgs = load_json(addl_pkg_path)
        fg_pkgs.extend(addl_pkgs.get("packages", []))
    except json.JSONDecodeError:
        raise  # Invalid JSON is a hard failure
# If file does not exist → gracefully skip (no error)
```

**Key point:** The `software_map` for os_* groups remains:
```python
"os_x86_64": ["default_packages.json", "ldms.json"],
"os_aarch64": ["default_packages.json", "ldms.json"],
```

#### 4.10.4 Execution Flow --- Package Resolution with Independent Additional Packages

```
image_package_collector.py :: collect_packages("os_x86_64")
    │
    ├── software_map["os_x86_64"]
    │   → ["default_packages.json", "ldms.json"]   (unchanged)
    │
    ├── Load JSON package files from input/config/x86_64/rhel/10.0/:
    │     ├── default_packages.json → kernel, systemd, NetworkManager, ...
    │     └── ldms.json → python3-devel, ovis-ldms, ...
    │
    ├── Independent optional flow: check for additional_packages.json
    │     ├── Path: input/config/x86_64/rhel/10.0/additional_packages.json
    │     ├── File exists? → Yes → load and merge packages
    │     │                → No  → skip (no error)
    │     └── Result: podman, podman-docker, ... (if present)
    │
    ├── Combine: default + ldms [+ additional if present] (no admin_debug)
    │
    ├── Deduplicate
    │
    └── Output: compute_images_dict["os_x86_64"] = final_pkgs
```

#### 4.10.5 Error Behavior

| Condition | Behavior |
|-----------|----------|
| `additional_packages.json` not found | Gracefully skip; image built with `default_packages.json` + `ldms.json` only |
| `additional_packages.json` has invalid JSON | `json.JSONDecodeError`; build fails |
| Package listed but not in Pulp | Image build fails at package installation (RPM dependency resolution error) |

#### 4.10.6 Dependencies

| Depends On | Reason |
|-----------|--------|
| CD-03 | Software map must exist with os_* entries; independent flow runs after software_map resolution |

#### 4.10.7 Test Cases

TC-2.30, TC-2.31

---

## 5. Component Interaction Diagram

```
                                    Administrator
                                        │
                                        │ Creates/edits
                                        ▼
                              ┌─────────────────────┐
                              │ PXE Mapping File    │ (CD-08)
                              │ (pxe_mapping.csv)   │
                              │ FUNCTIONAL_GROUP_    │
                              │ NAME=os_x86_64 │
                              └─────────┬───────────┘
                                        │
                     ┌──────────────────┼──────────────────┐
                     │                  │                  │
                     ▼                  ▼                  ▼
          ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
          │ JSON Schema      │ │ provision_       │ │ generate_        │
          │ Validator        │ │ validation.py    │ │ functional_      │
          │ (CD-01)          │ │                  │ │ groups.py        │
          │                  │ │ Reads:           │ │ (CD-05)          │
          │ Validates FG     │ │ config.py:       │ │                  │
          │ name against     │ │ FUNCTIONAL_GROUP │ │ Reads:           │
          │ enum             │ │ _LAYER_MAP       │ │ config.py:       │
          └──────────────────┘ │ (CD-02)          │ │ FUNCTIONAL_GROUP │
                               │                  │ │ _LAYER_MAP       │
                               │ Reads:           │ │ (CD-02)          │
                               │ fetch_roles_     │ │                  │
                               │ config.py:       │ │ Reads:           │
                               │ SECOND_LAYER_    │ │ DESCRIPTION_MAP  │
                               │ ROLES (CD-04)    │ │ (CD-05)          │
                               └────────┬─────────┘ └────────┬─────────┘
                                        │                    │
                                        │ Validated          │ Generates
                                        ▼                    ▼
                              ┌──────────────────────────────────────┐
                              │ functional_groups_config.yml         │
                              └─────────────────┬────────────────────┘
                                                │
                              ┌─────────────────┼──────────────────┐
                              │                 │                  │
                              ▼                 ▼                  ▼
                   ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
                   │ image_package_   │ │ openchami_   │ │ configure_       │
                   │ collector.py     │ │ image_cmd.yml│ │ ochami/tasks     │
                   │ (CD-03)          │ │ (CD-07)      │ │                  │
                   │                  │ │              │ │ Loads:           │
                   │ software_map     │ │ os_*_        │ │ ci-group-        │
                   │ ["os_*"] =      │ │ compute_     │ │ os_*.j2          │
                   │ ["default_pkgs, │ │ commands     │ │ (CD-06)          │
                   │  ldms"]         │ │              │ │                  │
                   │                  │ └──────┬───────┘ └────────┬─────────┘
                   │ + independent:   │        │                  │
                   │ additional_pkgs  │        │                  │
                   │ (CD-10, optional)│        │                  │
                   └────────┬─────────┘        │                  │
                            │                  │                  │
                            └──────────────────┼──────────────────┘
                                               │
                                               ▼
                                    ┌─────────────────────┐
                                    │ OpenCHAMI           │
                                    │ Build + Boot        │
                                    └─────────────────────┘
```

---

## 6. Dependency Matrix

| Component | Depends On | Depended On By |
|-----------|-----------|----------------|
| **CD-01** (Schema) | None | CD-08 (FG name must be in enum) |
| **CD-02** (Layer Map) | None | CD-03, CD-04, CD-05, CD-06, CD-07 (all downstream components) |
| **CD-03** (Software Map) | CD-02 | CD-10 (independent flow runs after software_map resolution), Image build pipeline |
| **CD-04** (Role Classification) | CD-02 | Validation pipeline |
| **CD-05** (FG Generator) | CD-02 | YAML generation |
| **CD-06** (Cloud-Init) | CD-02 | Discovery pipeline |
| **CD-07** (Compute Commands) | CD-02 | Image build pipeline |
| **CD-08** (PXE Template) | CD-01 | None (documentation/example only) |
| **CD-09** (Additional Packages) | CD-10 | Image build pipeline |
| **CD-10** (Addl Pkgs independent flow) | CD-03 | CD-09, Image build pipeline |

**Implementation Order:**
1. **First:** CD-01 + CD-02 (must be implemented together as they are both entry-point registrations)
2. **Parallel:** CD-03, CD-04, CD-05, CD-06, CD-07, CD-08 (all independent after CD-01+CD-02)
3. **After CD-03:** CD-10 (independent load logic) + CD-09 (create JSON files)

---

## 7. Traceability

| CD | FSpec | BSpec AC | ESPEC Section | Test Cases |
|----|-------|---------|---------------|------------|
| CD-01 | FS-GD-01 | AC-1.1 | §4.1 | TC-1.01, TC-1.02, TC-1.20, TC-1.21 |
| CD-02 | FS-GD-01, FS-GD-02, FS-ER-01 | AC-1.1, AC-1.4, AC-6.1 | §4.1 | TC-1.03--TC-1.06, TC-1.11, TC-1.22, TC-1.23 |
| CD-03 | FS-IC-02, FS-EX-01--05 | AC-2.1--AC-2.7, AC-4.3--AC-4.6 | §4.2 | TC-2.01--TC-2.06, TC-2.20--TC-2.25, TC-2.30 |
| CD-04 | FS-GD-01 | AC-1.4 | §4.1 | TC-1.07, TC-1.08 |
| CD-05 | FS-GD-01 | AC-1.1 | §4.1 | TC-1.09, TC-1.10, TC-1.24 |
| CD-06 | FS-PV-01, FS-PV-04, FS-HS-01, FS-HS-02, FS-EX-04 | AC-4.1, AC-4.2, AC-5.3 | §4.3 | TC-7.01, TC-7.02, TC-6.20 |
| CD-07 | FS-IC-01 | AC-2.7 | §4.2 | TC-7.01, TC-7.02 |
| CD-08 | FS-GD-02 | AC-1.1 | §4.4 | TC-1.03 |
| CD-09 | FS-IC-03 | AC-2.1 | §4.2.3.5 | TC-2.30, TC-2.31 |
| CD-10 | FS-IC-02, FS-IC-03 | AC-2.1 | §4.2.3.5 | TC-2.30, TC-2.31 |

---

## Approvals

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Engineering Lead | | | |
| QA Lead | | | |
| Architecture | | | |

---

*Document Version: 1.2 | Last Updated: 2026-04-09*
*SDD Phase: 5a --- Component Specification*
*Parent: Engineering Specification ESPEC-9294-2026-001 v0.4*
*Companion: Test Specification TSPEC-9294-2026-001 v1.0*
*Capability: 9294 (Minimal OS-Only Functional Group)*
