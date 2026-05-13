# Module Specification: Dell PowerScale S3 Backend Integration for OpenCHAMI Image Repository

| **Field** | **Value** |
|---|---|
| **Document ID** | MS-003 |
| **Module Name** | Dell PowerScale S3 Backend Integration |
| **Status** | Final |
| **Version** | 1.0 |
| **Date Created** | 2026-05-08 |
| **Date Updated** | 2026-05-11 |
| **Author** | Sowjanya Jagadish |
| **Source Repository** | `dell/omnia` at `pub/q2_dev` |

---

## Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 - 9.0 | May 2026 | Earlier iterations |
| 10.0 | May 2026 | Maximum reuse: s3cmd, backend-aware s3cfg.j2, backend-aware credential prompts |
| **11.0** | **May 2026** | **Codebase-aligned revision: (1) JSON Schema (not YAML). (2) Credential framework integration corrected -- no `username_prompt`/`password_prompt` support; use `conditional_mandatory` + `credential_rules.json` descriptions. (3) `policy_update.yml` backend-awareness added. (4) aarch64 template included. (5) `storage_config.yml` loading added to credential utility validation and deploy_openchami. (6) Removed non-existent `S3_ACCESS`/`S3_SECRET` references. (7) Total: 13 files updated, 0 new files.** |

### Key Changes in v11.0 (vs v10.0)

1. **Schema format corrected** -- actual codebase uses JSON Schema (`storage_config.json`), not YAML
2. **Credential framework accurately mapped** -- `username_prompt`/`password_prompt` keys do NOT exist; prompts are built from `[field_name] TYPE_INPUT CREDENTIAL_RULE.msg Enter value`
3. **`minio_s3_username` added to credential system** -- currently hardcoded "admin" in `common/vars/common_vars.yml`, not prompted; now added as `conditional_mandatory` for S3 backend
4. **`S3_ACCESS`/`S3_SECRET` references removed** -- these variables do not exist in the codebase; template already uses `minio_s3_username`/`minio_s3_password`
5. **`policy_update.yml` addressed** -- has hardcoded MinIO endpoint (`--host={{ cluster_boot_ip }}:9000`), needs backend-aware update
6. **aarch64 template included** -- `build_image_aarch64/.../compute_images_templates.j2` needs identical changes
7. **`storage_config.yml` loading** -- must be loaded in credential utility validation and in `deploy_openchami.yml` for `openchami_storage_backend` to be available
8. **`deploy_openchami.yml` update** -- add `| default('admin', true)` fallback for NFS username

---

## 1. Critical Architectural Insight: Maximum Reuse of Existing `s3_bucket.yml`

### 1.1 What's Already in `s3_bucket.yml` (Verified from Codebase)

The existing file at `prepare_oim/roles/deploy_containers/openchami/tasks/configs/s3_bucket.yml` already contains:

```yaml
- name: Import EPEL GPG key
  ansible.builtin.rpm_key:
    key: "{{ epel10_gpg_key }}"
    state: present

- name: Install EPEL release RPM
  ansible.builtin.dnf:
    name: "{{ epel10_url }}"
    state: present

- name: Install s3cmd
  ansible.builtin.dnf:
    name: s3cmd
    state: present

- name: Create s3cfg
  ansible.builtin.template:
    src: s3/s3cfg.j2
    dest: /root/.s3cfg
    mode: "{{ file_perm_rw }}"

- name: Verify s3 bucket
  ansible.builtin.command: s3cmd ls
  ...

- name: Create S3 bucket 'efi'
  ansible.builtin.command: s3cmd mb s3://efi
  ...

- name: Create S3 bucket 'boot-images'
  ansible.builtin.command: s3cmd mb s3://boot-images
  ...
```

### 1.2 What This Means

**We don't need to create or replace anything for bucket creation logic.** We just need to make sure the `s3cfg.j2` template generates the right `~/.s3cfg` file based on the selected backend:

- **NFS:** `~/.s3cfg` points to `http://{{ cluster_name }}.{{ cluster_domain }}:9000` (MinIO) with MinIO credentials
- **S3:** `~/.s3cfg` points to `https://10.43.1.11:9021` (PowerScale) with PowerScale credentials

The existing `s3cmd mb` tasks then automatically create buckets in whichever backend the `~/.s3cfg` points to. **No code logic changes needed for bucket creation.**

### 1.3 Why This is Better Than `amazon.aws.s3_bucket`

| Aspect | `amazon.aws.s3_bucket` Module | Existing `s3cmd` Tasks |
|---|---|---|
| Dependency | Requires `amazon.aws` collection | Uses `s3cmd` (already installed) |
| Code changes | New tasks needed | **Zero new tasks** |
| Backend agnostic | Yes (via `endpoint_url`) | Yes (via `~/.s3cfg`) |
| boto3 dependency | Yes | No (s3cmd is standalone Python) |
| Aligns with existing flow | No (parallel implementation) | **Yes (extends existing)** |
| Footprint | New code | **Just template tweak** |

**Decision:** Reuse existing `s3cmd` tasks. Only modify `s3cfg.j2` template to be backend-aware.

---

## 2. Final Module Components (Codebase-Aligned)

### 2.1 Files to Modify

| # | Path | Action | Notes |
|---|---|---|---|
| 1 | `input/storage_config.yml` | UPDATE (+5 lines) | Add `openchami_storage_backend` and `openchami_s3.endpoint_url` |
| 2 | `common/library/module_utils/input_validation/schema/storage_config.json` | UPDATE (+35 lines) | Add JSON Schema validation for new fields |
| 3 | `common/library/module_utils/input_validation/schema/credential_rules.json` | UPDATE (+8 lines) | Add `minio_s3_username` validation rule |
| 4 | `utils/credential_utility/roles/create_config/templates/omnia_credential.j2` | UPDATE (+1 line) | Add `minio_s3_username: ""` |
| 5 | `utils/credential_utility/roles/update_config/vars/main.yml` | UPDATE | Add `minio_s3_username` to `conditional_mandatory` |
| 6 | `utils/credential_utility/roles/validation/tasks/main.yml` | UPDATE (+6 lines) | Load `storage_config.yml` for backend-aware conditions |
| 7 | `prepare_oim/roles/deploy_containers/openchami/tasks/deploy_openchami.yml` | UPDATE | Load `storage_config.yml`, update `set_fact` with default |
| 8 | `prepare_oim/roles/deploy_containers/openchami/tasks/configs/main.yml` | UPDATE | Backend router; conditional MinIO and s3_bucket inclusion |
| 9 | `prepare_oim/roles/deploy_containers/openchami/tasks/configs/s3_bucket.yml` | UPDATE | Add PowerScale validation + post-creation tasks (bucket tasks UNCHANGED) |
| 10 | `prepare_oim/roles/deploy_containers/openchami/tasks/configs/policy_update.yml` | UPDATE | Backend-aware host endpoints |
| 11 | `prepare_oim/roles/deploy_containers/openchami/templates/s3/s3cfg.j2` | UPDATE | Backend-aware endpoint and credentials |
| 12 | `build_image_x86_64/roles/image_creation/templates/compute_images_templates.j2` | UPDATE | PREFIX boto3 env vars + default username fallback |
| 13 | `build_image_aarch64/roles/image_creation/templates/compute_images_templates.j2` | UPDATE | Same changes as x86_64 |

### 2.2 Files Untouched (PRESERVED)

| Path | Reason |
|---|---|
| `prepare_oim/roles/deploy_containers/openchami/tasks/configs/minio.yml` | Existing MinIO container deployment unchanged |
| Existing `s3cmd mb` and `s3cmd setacl` tasks in `s3_bucket.yml` | Already functional for bucket creation |
| `common/vars/common_vars.yml` | Keep `minio_s3_username: "admin"` as fallback default |

### 2.3 No New Files, No New Collections

- Zero new files
- Zero new Ansible collections required
- Zero new system packages (s3cmd already installed by existing tasks)

---

## 3. Credential Framework Integration (Codebase-Accurate)

### 3.1 How Omnia's Credential Framework Actually Works

The credential prompt framework constructs prompts dynamically from three components:

```
[FIELD_NAME] TYPE_INPUT_MESSAGE CREDENTIAL_RULE.msg Enter value
```

**Example:**
```
[minio_s3_password] is a [MANDATORY] credential and cannot be left empty.
Password for Minio S3 bucket. Should not be kept 'admin'. Length must be between 5
and 128 characters... Enter value
```

**Key findings from codebase analysis:**
- Prompts are built in `prompt_username.yml` and `prompt_password.yml`
- The `TYPE_INPUT_MESSAGE` comes from `lookup('vars', type.key ~ '_input')` -- e.g., `mandatory_input`, `conditional_mandatory_input`
- The `CREDENTIAL_RULE.msg` comes from `credential_rules.json` via the `fetch_credential_rule` module
- **There are NO `username_prompt` / `password_prompt` custom key fields** in the framework
- Backend-aware messaging must be achieved via the `credential_rules.json` description field

### 3.2 Current State (Verified)

```yaml
# utils/credential_utility/roles/update_config/vars/main.yml
prepare_oim:
  optional:
    - { username: docker_username, password: docker_password }
  mandatory:
    - { password: pulp_password }
    - { password: minio_s3_password }          # <-- password-only, no username
  conditional_mandatory:
    - username: build_stream_auth_username
      password: build_stream_auth_password
      condition: "{{ enable_build_stream | default(false) | bool }}"
      file: "{{ credential_files[1].file_path }}"
    - username: postgres_user
      password: postgres_password
      condition: "{{ enable_build_stream | default(false) | bool }}"
```

- `minio_s3_username` is NOT in the credential system -- it's hardcoded as `"admin"` in `common/vars/common_vars.yml`
- `minio_s3_password` is a mandatory credential (password-only, always prompted)
- The vault template (`omnia_credential.j2`) has `minio_s3_password: ""` but NO `minio_s3_username`

### 3.3 Updated State (v11.0)

```yaml
# utils/credential_utility/roles/update_config/vars/main.yml
prepare_oim:
  optional:
    - { username: docker_username, password: docker_password }
  mandatory:
    - { password: pulp_password }
    - { password: minio_s3_password }          # Kept as mandatory (both backends need it)
  conditional_mandatory:
    # PowerScale S3 Access Key -- only prompted when storage backend is 's3'
    # For NFS backend, minio_s3_username defaults to 'admin' from common_vars.yml
    - username: minio_s3_username
      condition: "{{ openchami_storage_backend | default('nfs') == 's3' }}"
    - username: build_stream_auth_username
      password: build_stream_auth_password
      condition: "{{ enable_build_stream | default(false) | bool }}"
      file: "{{ credential_files[1].file_path }}"
    - username: postgres_user
      password: postgres_password
      condition: "{{ enable_build_stream | default(false) | bool }}"
```

### 3.4 Why This Design Works

| Backend | `minio_s3_password` | `minio_s3_username` | UX Impact |
|---|---|---|---|
| NFS (default) | Prompted as mandatory | NOT prompted; defaults to "admin" | **Zero change** from current behavior |
| S3 (PowerScale) | Prompted as mandatory; user enters Secret Key | Prompted as conditional_mandatory; user enters Access Key | New prompt for username |

### 3.5 Credential Rules Update

Add to `credential_rules.json`:
```json
"minio_s3_username": {
  "minLength": 1,
  "maxLength": 128,
  "pattern": "^[^\\\\\\-'\"]+$",
  "description": "Dell PowerScale S3 Access Key (required when openchami_storage_backend is 's3'). Length must be between 1 and 128 characters and must not contain backslashes (\\), hyphens (-), single quotes ('), or double quotes (\")."
}
```

### 3.6 Variable Precedence Handling

**Problem:** `common_vars.yml` sets `minio_s3_username: "admin"` via `include_vars`. The credential vault also has `minio_s3_username: ""`. The LAST `include_vars` wins.

**Solution chain:**
1. `include_input_dir.yml` loads `common_vars.yml` -- sets `minio_s3_username: "admin"`
2. Credential utility loads vault -- overrides to `minio_s3_username: ""`
3. For NFS: not prompted (condition false), stays `""`
4. For S3: prompted (condition true), user enters PowerScale Access Key
5. In `deploy_openchami.yml`: `minio_s3_username: "{{ hostvars['localhost']['minio_s3_username'] | default('admin', true) }}"` -- falls back to "admin" when empty (NFS)
6. In templates: `minio_s3_username: "{{ minio_s3_username | default('admin', true) }}"` -- same fallback

### 3.7 Pre-requisite: Load storage_config.yml Before Credential Prompts

The credential utility's validation role must load `storage_config.yml` so that `openchami_storage_backend` is available when evaluating conditional_mandatory conditions:

```yaml
# utils/credential_utility/roles/validation/tasks/main.yml (APPEND)
- name: Load storage_config.yml for backend-aware credential prompts
  ansible.builtin.include_vars:
    file: "{{ input_project_dir }}/storage_config.yml"
  failed_when: false
  no_log: true
```

---

## 4. Implementation Details

### 4.1 `input/storage_config.yml` (UPDATE -- Append)

```yaml
# ============================================================
# OpenCHAMI Image Repository Backend Selector
# ============================================================
openchami_storage_backend: "nfs"

# Required ONLY if openchami_storage_backend: "s3"
openchami_s3:
  endpoint_url: "https://10.43.1.11:9021"
```

### 4.2 `common/library/module_utils/input_validation/schema/storage_config.json` (UPDATE -- Append to properties)

**Note:** The actual schema file is JSON Schema draft-07 format, NOT YAML. Append these properties inside the `"properties"` object, before the closing `"required": []` line:

```json
"openchami_storage_backend": {
  "type": "string",
  "description": "OpenCHAMI image repository backend: 'nfs' (default, MinIO) or 's3' (Dell PowerScale)",
  "enum": ["nfs", "s3"],
  "default": "nfs"
},
"openchami_s3": {
  "type": "object",
  "description": "Dell PowerScale S3 configuration. Required when openchami_storage_backend is 's3'.",
  "properties": {
    "endpoint_url": {
      "type": "string",
      "description": "PowerScale S3 endpoint URL (e.g., https://10.43.1.11:9021)",
      "pattern": "^https?://[a-zA-Z0-9.-]+(:[0-9]+)?(/.*)?$"
    }
  },
  "required": ["endpoint_url"],
  "additionalProperties": false
}
```

### 4.3 `common/library/module_utils/input_validation/schema/credential_rules.json` (UPDATE)

Add after the `minio_s3_password` entry:

```json
"minio_s3_username": {
  "minLength": 1,
  "maxLength": 128,
  "pattern": "^[^\\\\\\-'\"]+$",
  "description": "Dell PowerScale S3 Access Key (required when openchami_storage_backend is 's3'). Length must be between 1 and 128 characters and must not contain backslashes (\\), hyphens (-), single quotes ('), or double quotes (\")."
}
```

### 4.4 `utils/credential_utility/roles/create_config/templates/omnia_credential.j2` (UPDATE)

Add `minio_s3_username: ""` in the Prepare_oim credentials section:

```yaml
# Prepare_oim credentials
minio_s3_username: ""
minio_s3_password: ""
```

### 4.5 `utils/credential_utility/roles/update_config/vars/main.yml` (UPDATE)

```yaml
prepare_oim:
  optional:
    - { username: docker_username, password: docker_password }
  mandatory:
    - { password: pulp_password }
    - { password: minio_s3_password }
  conditional_mandatory:
    # PowerScale S3 Access Key -- only prompted when storage backend is 's3'
    - username: minio_s3_username
      condition: "{{ openchami_storage_backend | default('nfs') == 's3' }}"
    - username: build_stream_auth_username
      password: build_stream_auth_password
      condition: "{{ enable_build_stream | default(false) | bool }}"
      file: "{{ credential_files[1].file_path }}"
    - username: postgres_user
      password: postgres_password
      condition: "{{ enable_build_stream | default(false) | bool }}"
```

### 4.6 `utils/credential_utility/roles/validation/tasks/main.yml` (UPDATE -- Append after build_stream_config block)

```yaml
- name: Load storage_config.yml for backend-aware credential prompts
  ansible.builtin.include_vars:
    file: "{{ input_project_dir }}/storage_config.yml"
  failed_when: false
  no_log: true
```

### 4.7 `prepare_oim/roles/deploy_containers/openchami/tasks/deploy_openchami.yml` (UPDATE)

**Add storage_config.yml loading** (after network_spec include block):

```yaml
- name: Include storage_config.yml
  block:
    - name: Include storage_config.yml file
      ansible.builtin.include_vars:
        file: "{{ hostvars['localhost']['input_project_dir'] }}/storage_config.yml"
      no_log: true
  rescue:
    - name: Set default storage backend if storage_config.yml not found
      ansible.builtin.set_fact:
        openchami_storage_backend: "nfs"
```

**Update `set_fact` for minio credentials** (add `default('admin', true)` fallback):

```yaml
- name: Set minio_username and minio_password
  ansible.builtin.set_fact:
    minio_s3_username: "{{ hostvars['localhost']['minio_s3_username'] | default('admin', true) }}"
    minio_s3_password: "{{ hostvars['localhost']['minio_s3_password'] }}"
  no_log: true
```

**Add storage backend fact** (after minio credentials set_fact):

```yaml
- name: Set storage backend fact
  ansible.builtin.set_fact:
    storage_backend: "{{ openchami_storage_backend | default('nfs') | lower }}"
```

### 4.8 `prepare_oim/roles/deploy_containers/openchami/tasks/configs/main.yml` (UPDATE -- Backend Router)

Replace the current unconditional `import_tasks` chain with conditional `include_tasks`:

```yaml
---
# Copyright 2026 Dell Inc. or its subsidiaries. All Rights Reserved.
# (license header preserved)
---

- name: Import packages task
  ansible.builtin.import_tasks: packages.yml

- name: Import configs task
  ansible.builtin.import_tasks: create_dirs.yml

- name: Import hosts task
  ansible.builtin.import_tasks: hosts.yml

# --- NFS PATH (Existing MinIO Flow) ---
- name: Import minio task (NFS backend only)
  ansible.builtin.include_tasks: minio.yml
  when: storage_backend | default('nfs') == 'nfs'

- name: Import registry task
  ansible.builtin.import_tasks: registry.yml

- name: Import ochami task
  ansible.builtin.import_tasks: ochami.yml

- name: Import firewall task
  ansible.builtin.import_tasks: firewall.yml

- name: Import verify task
  ansible.builtin.import_tasks: verify.yml

- name: Import regctl tasks
  ansible.builtin.import_tasks: regctl.yml

# --- BUCKET CREATION (BOTH BACKENDS) ---
- name: Import s3 bucket tasks
  ansible.builtin.import_tasks: s3_bucket.yml

# --- POLICY UPDATE (Backend-aware) ---
- name: Import policy update tasks
  ansible.builtin.include_tasks: policy_update.yml
```

**Key change:** MinIO container deployment (`minio.yml`) is now conditional -- only runs when `storage_backend == 'nfs'`. Changed from `import_tasks` to `include_tasks` for minio.yml to support the `when:` condition at inclusion time.

### 4.9 `prepare_oim/roles/deploy_containers/openchami/tasks/configs/s3_bucket.yml` (UPDATE -- Existing File, Minimal Additions)

**The existing bucket creation tasks REMAIN UNCHANGED.** We only ADD:
1. PowerScale endpoint validation (when backend is `s3`) -- prepended
2. Post-creation tasks: regex update and fact persistence (when backend is `s3`) -- appended

```yaml
---
# Copyright 2026 Dell Inc. or its subsidiaries. All Rights Reserved.
# (license header preserved)
---

# === NEW: PowerScale endpoint validation (S3 backend only) ===
- name: Validate PowerScale S3 endpoint configuration
  ansible.builtin.assert:
    that:
      - openchami_s3 is defined
      - openchami_s3.endpoint_url is defined
      - minio_s3_username is defined
      - minio_s3_username | length > 0
      - minio_s3_password is defined
    fail_msg: |
      PowerScale S3 backend requires:
        - openchami_s3.endpoint_url in storage_config.yml
        - minio_s3_username (PowerScale Access Key -- prompted by prepare_oim)
        - minio_s3_password (PowerScale Secret Key -- prompted by prepare_oim)
  when: storage_backend | default('nfs') == 's3'

- name: Test PowerScale endpoint reachability
  ansible.builtin.uri:
    url: "{{ openchami_s3.endpoint_url }}"
    method: GET
    validate_certs: false
    status_code: [200, 403, 404, 405]
    timeout: 10
  register: ps_endpoint_check
  failed_when: false
  when: storage_backend | default('nfs') == 's3'

- name: Fail if PowerScale unreachable
  ansible.builtin.fail:
    msg: |
      Cannot reach PowerScale S3 endpoint: {{ openchami_s3.endpoint_url }}
      Check: network connectivity, S3 service enabled, firewall rules
  when:
    - storage_backend | default('nfs') == 's3'
    - ps_endpoint_check.status is not defined or ps_endpoint_check.status not in [200, 403, 404, 405]

# === EXISTING TASKS (UNCHANGED -- work for both backends via ~/.s3cfg) ===
- name: Import EPEL GPG key
  ansible.builtin.rpm_key:
    key: "{{ epel10_gpg_key }}"
    state: present

- name: Install EPEL release RPM
  ansible.builtin.dnf:
    name: "{{ epel10_url }}"
    state: present

- name: Install s3cmd
  ansible.builtin.dnf:
    name: s3cmd
    state: present

- name: Create s3cfg
  ansible.builtin.template:
    src: s3/s3cfg.j2
    dest: /root/.s3cfg
    mode: "{{ file_perm_rw }}"

- name: Verify s3 bucket
  ansible.builtin.command: s3cmd ls
  changed_when: false
  failed_when: false
  register: s3_bucket_output

- name: Create S3 bucket 'efi'
  ansible.builtin.command: s3cmd mb s3://efi
  register: efi_bucket
  changed_when: "'Bucket' in efi_bucket.stdout"
  when: '"s3://efi" not in s3_bucket_output.stdout'

- name: Set ACL to public for 'efi'
  ansible.builtin.command: s3cmd setacl s3://efi --acl-public
  changed_when: true
  when: '"s3://efi" not in s3_bucket_output.stdout'

- name: Create S3 bucket 'boot-images'
  ansible.builtin.command: s3cmd mb s3://boot-images
  register: boot_images_bucket
  changed_when: "'Bucket' in boot_images_bucket.stdout"
  when: '"s3://boot-images" not in s3_bucket_output.stdout'

- name: Set ACL to public for 'boot-images'
  ansible.builtin.command: s3cmd setacl s3://boot-images --acl-public
  changed_when: true
  when: '"s3://boot-images" not in s3_bucket_output.stdout'

- name: Verify s3 bucket after creation
  ansible.builtin.command: s3cmd ls
  changed_when: false
  register: s3_bucket_output_final

- name: Verify s3 bucket output
  ansible.builtin.debug:
    msg: "{{ s3_bucket_output_final.stdout_lines }}"

# === NEW: PowerScale-specific post-creation tasks (S3 backend only) ===
- name: Update publish_s3 in rhel-base-compute.yaml.j2 to PowerScale endpoint
  ansible.builtin.replace:
    path: /opt/omnia/openchami/deployment-recipes/dell/podman-quadlets/roles/image/templates/images/rhel-base-compute.yaml.j2
    regexp: "^(\\s*publish_s3:\\s*)'http://\\{\\{\\s*cluster_name\\s*\\}\\}\\.\\{\\{\\s*cluster_domain\\s*\\}\\}:9000'(.*)$"
    replace: "\\1'{{ openchami_s3.endpoint_url }}'\\2"
    backup: true
  when: storage_backend | default('nfs') == 's3'

- name: Ensure OpenCHAMI configs directory exists
  ansible.builtin.file:
    path: /etc/openchami/configs
    state: directory
    mode: '0755'
  when: storage_backend | default('nfs') == 's3'

- name: Persist unified S3 facts (S3 backend only)
  ansible.builtin.copy:
    dest: /etc/openchami/configs/openchami_storage.yml
    mode: '0600'
    owner: root
    group: root
    content: |
      ---
      # Auto-generated by prepare_oim -- DO NOT EDIT MANUALLY
      storage_backend: "s3"
      unified_s3_endpoint: "{{ openchami_s3.endpoint_url }}"
      unified_s3_boot_bucket: "boot-images"
      unified_s3_efi_bucket: "efi"
      generated_at: "{{ ansible_date_time.iso8601 }}"
  when: storage_backend | default('nfs') == 's3'
  no_log: true
```

### 4.10 `prepare_oim/roles/deploy_containers/openchami/tasks/configs/policy_update.yml` (UPDATE -- Backend-Aware)

**Current state (codebase):**
```yaml
- name: Update the boot policy
  ansible.builtin.command: >
    s3cmd setpolicy {{ s3_work_dir }}/s3-public-read-boot.json s3://boot-images
    --host={{ cluster_boot_ip }}:9000
    --host-bucket={{ cluster_boot_ip }}:9000
```

**Problem:** The `--host=` and `--host-bucket=` are hardcoded to MinIO port 9000. For S3 backend, these should use the PowerScale endpoint. However, when `~/.s3cfg` is already configured for the right backend, the explicit `--host=` override is unnecessary for NFS and wrong for S3.

**Updated:**
```yaml
- name: Load boot policy file
  ansible.builtin.template:
    src: s3/s3-public-read-boot.json.j2
    dest: "{{ s3_work_dir }}/s3-public-read-boot.json"
    mode: "{{ file_perm_rw }}"

- name: Load efi policy file
  ansible.builtin.template:
    src: s3/s3-public-read-efi.json.j2
    dest: "{{ s3_work_dir }}/s3-public-read-efi.json"
    mode: "{{ file_perm_rw }}"

- name: Update the boot policy (NFS/MinIO)
  ansible.builtin.command: >
    s3cmd setpolicy {{ s3_work_dir }}/s3-public-read-boot.json s3://boot-images
    --host={{ cluster_boot_ip }}:9000
    --host-bucket={{ cluster_boot_ip }}:9000
  changed_when: true
  when: storage_backend | default('nfs') == 'nfs'

- name: Update the efi policy (NFS/MinIO)
  ansible.builtin.command: >
    s3cmd setpolicy {{ s3_work_dir }}/s3-public-read-efi.json s3://efi
    --host={{ cluster_boot_ip }}:9000
    --host-bucket={{ cluster_boot_ip }}:9000
  changed_when: true
  when: storage_backend | default('nfs') == 'nfs'

- name: Update the boot policy (S3/PowerScale)
  ansible.builtin.command: >
    s3cmd setpolicy {{ s3_work_dir }}/s3-public-read-boot.json s3://boot-images
  changed_when: true
  when: storage_backend | default('nfs') == 's3'

- name: Update the efi policy (S3/PowerScale)
  ansible.builtin.command: >
    s3cmd setpolicy {{ s3_work_dir }}/s3-public-read-efi.json s3://efi
  changed_when: true
  when: storage_backend | default('nfs') == 's3'
```

**Note:** For S3/PowerScale, we omit `--host=` and `--host-bucket=` so `s3cmd` uses the endpoint from `~/.s3cfg` (which was already configured by `s3_bucket.yml`). For NFS/MinIO, we keep the existing explicit host overrides for backward compatibility.

### 4.11 `prepare_oim/roles/deploy_containers/openchami/templates/s3/s3cfg.j2` (UPDATE -- Backend-Aware)

**Current state (codebase):**
```
# Setup endpoint
host_base = {{ cluster_name }}.{{ cluster_domain }}:9000
host_bucket = {{ cluster_name }}.{{ cluster_domain }}:9000
bucket_location = us-east-1
use_https = False

# Setup access keys
access_key = {{ minio_s3_username }}
secret_key = {{ minio_s3_password }}

# Enable S3 v4 signature APIs
signature_v2 = False
```

**Updated:**
```jinja2
[default]
access_key = {{ minio_s3_username }}
secret_key = {{ minio_s3_password }}
{% if storage_backend | default('nfs') == 's3' %}
host_base = {{ openchami_s3.endpoint_url | regex_replace('^https?://', '') }}
host_bucket = {{ openchami_s3.endpoint_url | regex_replace('^https?://', '') }}
use_https = {{ 'True' if openchami_s3.endpoint_url.startswith('https') else 'False' }}
check_ssl_certificate = False
check_ssl_hostname = False
{% else %}
host_base = {{ cluster_name }}.{{ cluster_domain }}:9000
host_bucket = {{ cluster_name }}.{{ cluster_domain }}:9000
use_https = False
check_ssl_certificate = False
check_ssl_hostname = False
{% endif %}
signature_v2 = False
bucket_location = us-east-1
human_readable_sizes = True
multipart_chunk_size_mb = 50
```

### 4.12 `build_image_x86_64/roles/image_creation/templates/compute_images_templates.j2` (UPDATE)

**Current state (codebase):**
```jinja2
rhel_base_compute_mounts: --user 0 --privileged -v {{ oim_shared_path }}/omnia/pulp/settings/certs/pulp_webserver.crt:/etc/pki/ca-trust/source/anchors/pulp_webserver.crt:z -v {{ openchami_work_dir }}/images/{{ rhel_base_compute_image_name }}-{{ rhel_tag }}.yaml:/home/builder/config.yaml:z
...
minio_s3_username: "{{ minio_s3_username }}"
minio_s3_password: "{{ minio_s3_password }}"
```

**Updated:**
```jinja2
rhel_base_compute_mounts: -e AWS_REQUEST_CHECKSUM_CALCULATION=when_required -e AWS_RESPONSE_CHECKSUM_VALIDATION=when_required --user 0 --privileged -v {{ oim_shared_path }}/omnia/pulp/settings/certs/pulp_webserver.crt:/etc/pki/ca-trust/source/anchors/pulp_webserver.crt:z -v {{ openchami_work_dir }}/images/{{ rhel_base_compute_image_name }}-{{ rhel_tag }}.yaml:/home/builder/config.yaml:z
...
minio_s3_username: "{{ minio_s3_username | default('admin', true) }}"
minio_s3_password: "{{ minio_s3_password }}"
```

**Changes:**
1. Prefixed boto3 env vars `-e AWS_REQUEST_CHECKSUM_CALCULATION=when_required -e AWS_RESPONSE_CHECKSUM_VALIDATION=when_required` to `rhel_base_compute_mounts` (harmless for MinIO, required for PowerScale)
2. Added `| default('admin', true)` to `minio_s3_username` to fall back to "admin" when vault has empty value (NFS backend)

### 4.13 `build_image_aarch64/roles/image_creation/templates/compute_images_templates.j2` (UPDATE)

Same changes as 4.12 -- prefix boto3 env vars and add default fallback:

```jinja2
rhel_base_compute_mounts: -e AWS_REQUEST_CHECKSUM_CALCULATION=when_required -e AWS_RESPONSE_CHECKSUM_VALIDATION=when_required --user 0 --privileged -v {{ oim_shared_path }}/omnia/pulp/settings/certs/pulp_webserver.crt:/etc/pki/ca-trust/source/anchors/pulp_webserver.crt:z -v {{ openchami_work_dir }}/images/{{ rhel_base_compute_image_name }}-{{ rhel_tag }}.yaml:/home/builder/config.yaml:z
...
minio_s3_username: "{{ minio_s3_username | default('admin', true) }}"
minio_s3_password: "{{ minio_s3_password }}"
```

---

## 5. End-to-End Flow

### 5.1 NFS Backend (Default)

#### User Configuration
```yaml
# input/storage_config.yml
openchami_storage_backend: "nfs"
```

#### Step-by-Step Execution

1. **Credential Phase**
   - `get_config_credentials.yml` runs
   - Validation role loads `storage_config.yml` -- `openchami_storage_backend = "nfs"`
   - `pulp_password` prompted (mandatory)
   - `minio_s3_password` prompted (mandatory) -- user enters MinIO password
   - `minio_s3_username` conditional_mandatory condition evaluates to false (`'nfs' == 's3'` = false) -- **NOT prompted**, stays `""` in vault

2. **OpenCHAMI Backend Setup**
   - `deploy_openchami.yml` loads `storage_config.yml` -- sets `storage_backend = 'nfs'`
   - `minio_s3_username` set_fact with `default('admin', true)` -- resolves to `"admin"` (vault value is empty)
   - `configs/main.yml` includes `minio.yml` -- MinIO container deploys
   - `s3_bucket.yml` runs:
     - PowerScale validation tasks SKIPPED (`when: storage_backend == 's3'`)
     - `s3cfg.j2` renders with MinIO endpoint (`http://<cluster>:9000`)
     - Existing `s3cmd mb` tasks create buckets in MinIO
     - Post-creation tasks SKIPPED
   - `policy_update.yml` runs NFS branch -- sets policies with MinIO host

3. **Build Images Phase**
   - `compute_images_templates.j2` renders:
     - `minio_s3_username: "admin"` (default fallback)
     - `minio_s3_password: "<user_entered_password>"`
   - boto3 env vars prefixed in `rhel_base_compute_mounts` (harmless to MinIO)
   - Image-builder publishes to MinIO

### 5.2 PowerScale S3 Backend

#### User Configuration
```yaml
# input/storage_config.yml
openchami_storage_backend: "s3"
openchami_s3:
  endpoint_url: "https://10.43.1.11:9021"
```

#### Step-by-Step Execution

1. **Credential Phase**
   - `get_config_credentials.yml` runs
   - Validation role loads `storage_config.yml` -- `openchami_storage_backend = "s3"`
   - `pulp_password` prompted (mandatory)
   - `minio_s3_password` prompted (mandatory) -- user enters PowerScale Secret Key
   - `minio_s3_username` conditional_mandatory condition evaluates to true (`'s3' == 's3'` = true):
     ```
     [minio_s3_username] is a [CONDITIONAL MANDATORY] credential and cannot be left
     empty when the feature is enabled. Dell PowerScale S3 Access Key... Enter value
     ```
   - User enters PowerScale Access Key

2. **OpenCHAMI Backend Setup**
   - `deploy_openchami.yml` loads `storage_config.yml` -- sets `storage_backend = 's3'`
   - `minio_s3_username` set_fact resolves to PowerScale Access Key (vault has user-entered value)
   - `configs/main.yml` **SKIPS** `minio.yml` (`when: storage_backend == 'nfs'` = false)
   - `s3_bucket.yml` runs:
     - **PowerScale validation runs** (endpoint reachability check)
     - `s3cfg.j2` renders with PowerScale endpoint (`https://10.43.1.11:9021`)
     - Existing `s3cmd mb` tasks create buckets on PowerScale
     - `rhel-base-compute.yaml.j2` updated via regex
     - Facts persisted to `/etc/openchami/configs/openchami_storage.yml`
   - `policy_update.yml` runs S3 branch -- uses `~/.s3cfg` endpoint (no explicit host override)

3. **Build Images Phase**
   - `compute_images_templates.j2` renders:
     - `minio_s3_username: "<PowerScale_Access_Key>"`
     - `minio_s3_password: "<PowerScale_Secret_Key>"`
   - boto3 env vars prefixed enable PowerScale compatibility
   - Image-builder publishes to PowerScale `s3://boot-images/`

---

## 6. Variable Mapping Reference

| Variable | Source | NFS Backend | S3 Backend |
|---|---|---|---|
| `openchami_storage_backend` | User input | `"nfs"` | `"s3"` |
| `openchami_s3.endpoint_url` | User input | (not used) | `"https://10.43.1.11:9021"` |
| `minio_s3_username` | Prompted/Default | `"admin"` (default, not prompted) | PowerScale Access Key (prompted) |
| `minio_s3_password` | Prompted | MinIO password | PowerScale Secret Key |
| `~/.s3cfg` `host_base` | Rendered from `s3cfg.j2` | `<cluster>:9000` | `10.43.1.11:9021` |
| `s3cmd mb s3://efi` target | Determined by `~/.s3cfg` | MinIO | PowerScale |

---

## 7. Design Decisions

### 7.1 Reuse Existing `s3cmd` Bucket Creation Tasks

| Decision | Use existing `s3cmd mb` and `s3cmd setacl` tasks unchanged |
|---|---|
| **Rationale** | The bucket creation logic is already implemented and proven. Backend differentiation is achieved purely via the `~/.s3cfg` template. |

### 7.2 Backend-Aware `s3cfg.j2` Template

| Decision | Use Jinja `if/else` to switch endpoint and SSL settings based on `storage_backend` |
|---|---|
| **Rationale** | Single template handles both backends. The downstream `s3cmd` commands work identically for both. |

### 7.3 Credential Integration via `conditional_mandatory` (Not Custom Prompts)

| Decision | Add `minio_s3_username` as `conditional_mandatory` with S3 condition; update `credential_rules.json` for descriptive prompt |
|---|---|
| **Rationale** | The Omnia credential framework does NOT support `username_prompt`/`password_prompt` keys. Backend-specific guidance is provided via the `credential_rules.json` description field. NFS UX is UNCHANGED (username not prompted). |

### 7.4 `s3_bucket.yml` Runs for BOTH Backends

| Decision | Run existing `s3_bucket.yml` for both `nfs` and `s3` |
|---|---|
| **Rationale** | Both backends need the same buckets created. The `~/.s3cfg` determines which backend gets them. |

### 7.5 boto3 Env Vars PREFIXED (Always)

| Decision | Prefix env vars at start of `rhel_base_compute_mounts` for BOTH backends |
|---|---|
| **Rationale** | These are harmless for MinIO but required for PowerScale. Simplifies template (no conditional logic). |

### 7.6 `policy_update.yml` Backend-Aware

| Decision | Separate NFS and S3 policy update commands |
|---|---|
| **Rationale** | NFS needs explicit `--host=` override (existing behavior preserved). S3 relies on `~/.s3cfg` endpoint (no explicit host needed). |

### 7.7 `minio_s3_username` Default Fallback

| Decision | Use `| default('admin', true)` in `deploy_openchami.yml` and templates |
|---|---|
| **Rationale** | The vault stores `""` for NFS (not prompted). The fallback ensures MinIO gets "admin" as username. For S3, the vault has the user-entered value. |

---

## 8. NFS Flow Verification

### 8.1 NFS Backend Behavior Matrix

| Step | Behavior | Status |
|---|---|---|
| Credential prompts | `minio_s3_password` prompted (mandatory). `minio_s3_username` NOT prompted. | **Unchanged** |
| `configs/main.yml` runs | Sets `storage_backend = 'nfs'` | New (informational) |
| `configs/main.yml` includes `minio.yml` | MinIO container deploys | **Unchanged** |
| `s3cfg.j2` template | Renders with MinIO endpoint | Backend-aware, defaults to existing |
| `s3cmd mb` tasks | Create buckets in MinIO | **Unchanged** |
| `s3_bucket.yml` PowerScale validation | Skipped (`when: storage_backend == 's3'`) | Skipped |
| `s3_bucket.yml` regex update | Skipped | Skipped |
| `s3_bucket.yml` persist facts | Skipped | Skipped |
| `policy_update.yml` | NFS branch runs with existing host overrides | **Unchanged** |
| `compute_images_templates.j2` boto3 env vars | Prefixed but harmless to MinIO | Safe |
| `compute_images_templates.j2` credentials | `minio_s3_username: "admin"` via default fallback | **Unchanged** |
| Image-builder run | Uses MinIO endpoint as before | **Unchanged** |

### 8.2 Pre/Post Comparison Test

```bash
ansible-playbook prepare_oim.yml -e openchami_storage_backend=nfs
ansible-playbook build_images.yml
```

Compare outputs (image YAMLs, MinIO state, image-builder env, published artifacts) to pre-module run. Functional behavior must be identical.

---

## 9. Final File Layout

```
omnia/
  input/
    storage_config.yml                                              [UPDATE +5]
  common/library/module_utils/input_validation/schema/
    storage_config.json                                             [UPDATE +35]
    credential_rules.json                                           [UPDATE +8]
  utils/credential_utility/
    roles/create_config/templates/
      omnia_credential.j2                                           [UPDATE +1]
    roles/update_config/vars/
      main.yml                                                      [UPDATE -- add conditional_mandatory]
    roles/validation/tasks/
      main.yml                                                      [UPDATE +6]
  prepare_oim/roles/deploy_containers/openchami/
    tasks/
      deploy_openchami.yml                                          [UPDATE -- load storage_config, defaults]
      configs/
        main.yml                                                    [UPDATE -- Backend Router]
        minio.yml                                                   [UNCHANGED]
        s3_bucket.yml                                               [UPDATE -- Add validation + post-creation]
        policy_update.yml                                           [UPDATE -- Backend-aware endpoints]
    templates/s3/
      s3cfg.j2                                                      [UPDATE -- Backend-aware]
  build_image_x86_64/roles/image_creation/templates/
    compute_images_templates.j2                                     [UPDATE -- boto3 env vars + default]
  build_image_aarch64/roles/image_creation/templates/
    compute_images_templates.j2                                     [UPDATE -- boto3 env vars + default]
```

**Total: 0 NEW files, 13 UPDATED files, 1 UNCHANGED file (`minio.yml`).**

---

## 10. Error Handling & Diagnostics

### 10.1 Common Failure Scenarios

| Symptom | Likely Cause | Resolution |
|---|---|---|
| `openchami_storage_backend` rejected by schema | Invalid value | Correct to `nfs` or `s3` |
| `PowerScale S3 backend requires` assert failure | Missing `openchami_s3` config or credentials | Add `openchami_s3.endpoint_url` to `storage_config.yml`; ensure credentials are prompted |
| `Cannot reach PowerScale S3 endpoint` | Network failure | Verify connectivity, S3 service enabled, firewall |
| `minio_s3_username` prompt appears unexpectedly | `openchami_storage_backend` set to `s3` | Expected behavior -- enter PowerScale Access Key |
| MinIO container not starting | Storage backend is `s3` | Expected -- MinIO is skipped for S3 backend |

### 10.2 Manual Verification Commands

```bash
# 1. Verify PowerScale S3 endpoint reachability
curl -k https://10.43.1.11:9021

# 2. Check s3cfg configuration
cat /root/.s3cfg

# 3. List buckets on configured backend
s3cmd ls

# 4. Check persisted storage facts (S3 only)
cat /etc/openchami/configs/openchami_storage.yml

# 5. Verify image YAML was updated (S3 backend only)
grep publish_s3 /opt/omnia/openchami/deployment-recipes/dell/podman-quadlets/roles/image/templates/images/rhel-base-compute.yaml.j2
```

---

## 11. Testing Strategy

### 11.1 Unit Tests

- **Schema validation:** Add `openchami_storage_backend: "invalid"` -- confirm JSON Schema rejection
- **Credential prompt:** Run with `openchami_storage_backend: "s3"` -- confirm `minio_s3_username` prompt appears
- **Credential default:** Run with `openchami_storage_backend: "nfs"` -- confirm `minio_s3_username` is NOT prompted

### 11.2 Integration Tests

| Scenario | Expected Outcome |
|---|---|
| NFS backend (default) | Zero functional changes; MinIO deploys; buckets in MinIO |
| NFS backend (explicit) | Identical to default |
| S3 backend with valid PowerScale | Endpoint validated; buckets on PowerScale; facts persisted |
| S3 backend with unreachable endpoint | Clear failure: `Cannot reach PowerScale S3 endpoint` |
| Pre/post comparison (NFS) | Output identical to pre-module behavior |

### 11.3 Edge Cases

- `openchami_storage_backend` omitted entirely -- defaults to `nfs`; no S3 tasks execute
- Empty `openchami_s3` dict when backend is `s3` -- assert fails with helpful message
- PowerScale endpoint with non-standard port -- handled by `endpoint_url`
- `minio_s3_username` vault entry is empty on NFS -- `default('admin', true)` provides fallback

---

## 12. Security & Performance

### 12.1 Security

| Concern | Mitigation |
|---|---|
| Credentials in playbook output | `no_log: true` on all credential tasks |
| Persisted facts file | `mode: 0600`, `owner: root` |
| No external cloud connectivity | All S3 operations target local endpoint |

### 12.2 Performance

| Aspect | Value |
|---|---|
| S3 setup overhead | ~10-15s added when S3 backend selected |
| NFS backend overhead | ~0s (informational tasks only) |

---

**End of Module Specification -- Dell PowerScale S3 Backend Integration for OpenCHAMI Image Repository (v11.0)**
