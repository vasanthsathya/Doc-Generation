# Module Specification: Cloud-Init Phone-Home Verification

| **Field**              | **Value**                                                                 |
|------------------------|---------------------------------------------------------------------------|
| **Document ID**        | MS-002                                                                    |
| **Module Name**        | Cloud-Init Phone-Home Verification                                        |
| **Status**             | Draft                                                                     |
| **Version**            | 1.0                                                                       |
| **Date Created**       | 2026-05-01                                                                |
| **Date Updated**       | 2026-05-04                                                               |
| **Author**             | Sowjanya Jagadish                                                         |

---

## 1. Overview

The **Cloud-Init Phone-Home Verification** module enables the Omnia Infrastructure Manager (OIM) to deterministically confirm that PXE-booted compute nodes have successfully completed their cloud-init bootstrapping. It integrates the standard cloud-init `cc_phone_home` module with the Omnia BuildStream provisioning workflow, producing a verifiable readiness signal **before** downstream BuildStream tasks (failed-node tracking, JSON state writes, GitLab uploads) execute.

This module ensures that artifacts such as `failed_nodes.json`, `passed_nodes.json`, and persistent state files accurately reflect **actual node provisioning completion** — not merely iDRAC reboot success.

### Problem Statement

Prior to this module, the `set_pxe_boot.yml` playbook treated successful iDRAC PXE reboot as the success indicator. This produced false positives: a node could reboot via iDRAC successfully but fail mid-provisioning (kernel panic, network failure, cloud-init crash), resulting in inaccurate BuildStream state files being committed to GitLab.

### Solution

Capture a UTC epoch timestamp before PXE reboot, configure nodes via cloud-init to POST a `phone_home` callback upon successful boot completion, then poll the `cloud-init-server` systemd journal on the OIM (time-gated to the captured epoch) until **all** target nodes confirm completion.

---

## 2. Objective & Scope

### 2.1 Purpose

| Goal | Description |
|---|---|
| Deterministic readiness signal | Confirm cloud-init completed on every node before BSM writes state |
| Accurate state artifacts | `failed_nodes.json` reflects real provisioning outcome |
| Time-gated journal polling | Distinguish current-run phone-homes from historical ones |
| Concurrent multi-node detection | Detect any node's success on first poll, not sequentially |
| Conditional invocation | Active only when `enable_build_stream: true` |

### 2.2 In Scope

- New task file `cloudinit_phone_home.yml` inside `pxe_buildstream_manager` role.
- Modifications to `set_pxe_boot.yml` for epoch capture and task invocation.
- Addition of `phone_home` template to OpenCHAMI Dell deployment recipe.
- Default variables for retry count, polling interval, and initial pause.
- Documentation and validation procedures.

### 2.3 Out of Scope

- Modifying the OpenCHAMI cloud-init-server source code (uses native `phone_home` receiver).
- WireGuard tunnel setup (existing `enable_wireguard` flag respected, default `false`).
- SMD state-machine integration (handled internally by cloud-init-server).
- Per-node SSH validation (phone-home callback is the sole readiness signal).

---

## 3. Architecture & Design

### 3.1 High-Level Architecture

```
┌────────────────────────── OIM (Control Plane) ──────────────────────────┐
│                                                                          │
│   ┌──────── cloud-init-server (port 8081) ─────────┐                     │
│   │  /meta-data  /user-data  /vendor-data           │                    │
│   │  /phone-home/<instance_id>/  ← receiver         │                    │
│   └─────────────────────────────────────────────────┘                    │
│              ▲                          │                                │
│              │ (4) POST phone_home      │ (1) renders user-data          │
│              │                          │     with phone_home stanza     │
│   ┌──────── set_pxe_boot.yml playbook ──┴────────────┐                   │
│   │  Play 3:  set_fact pxe_start_epoch (UTC)         │                   │
│   │  Play 4:  iDRAC PXE reboot                       │                   │
│   │  Play 7:  pxe_buildstream_manager →              │                   │
│   │           cloudinit_phone_home.yml ← THIS MODULE │                   │
│   │  Play 8:  BSM writes failed_nodes.json           │                   │
│   └──────────────────────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────────┘
              │ (2) DHCP+PXE              ▲ (4) phone_home POST
              ▼                           │
        ┌────────────────┐                │
        │ Compute Node   │ (3) cloud-init │
        │ (de0001 ...)   │────────────────┘
        └────────────────┘
```

### 3.2 Sequence of Operations

| Step | Component | Action |
|---|---|---|
| 1 | OIM Playbook (Play 3) | Captures `pxe_start_epoch` via `ansible_date_time.epoch` |
| 2 | OIM Playbook (Play 4) | Triggers iDRAC PXE reboot for nodes in `bmc` group |
| 3 | Compute Node | PXE boots; cloud-init renders `phone_home` stanza in user-data |
| 4 | Compute Node | cloud-init `cc_phone_home` (Final stage) POSTs to `/phone-home/<id>/` |
| 5 | OIM cloud-init-server | Logs `INF Phone home request from <ip>` to systemd journal |
| 6 | OIM Playbook (Play 7) | Polls journal time-gated by epoch until all nodes confirm |
| 7 | OIM Playbook (Play 8) | BSM writes accurate `failed_nodes.json` |

### 3.3 Dependencies

| Layer | Dependency |
|---|---|
| OS | RHEL 10 / Rocky 10 / Ubuntu 24.04 (cloud-init 24.4+) |
| Container Runtime | Podman with quadlet support |
| Cloud-Init Server | `ghcr.io/openchami/cloud-init` (with native `phone_home` receiver) |
| Ansible Collections | `community.general` (for `read_csv`), `dellemc.openmanage` |
| Hardware | Dell iDRAC 9/10 with Boot Source Override API |
| Network | OIM admin IP reachable from compute nodes on TCP port 8081 |
| Inventory | `pxe_mapping_file.csv` containing `ADMIN_IP` column |

---

## 4. Module Components

### 4.1 New Files Created

| Path | Purpose |
|---|---|
| `omnia/utils/roles/pxe_buildstream_manager/tasks/cloudinit_phone_home.yml` | Phone-home polling task file |

### 4.2 Files Modified

| Path | Change Summary |
|---|---|
| `omnia/utils/set_pxe_boot.yml` | Added Play 3 epoch capture, Play 7 phone-home invocation, reordered BSM post-processing to run after phone-home |
| `omnia/utils/roles/pxe_buildstream_manager/defaults/main.yml` | Added `phone_home_retries`, `phone_home_delay`, `phone_home_initial_pause` |

### 4.3 OpenCHAMI Deployment Recipe Changes (Dell)

| Path | Change Summary |
|---|---|
| `deployment-recipes/dell/podman-quadlets/configs/cloud-init/cluster-defaults.yaml` | Added `phone_home` template entry to `cluster_cloud_init_templates`; added `cloud_init_base_url` to `cluster_cloud_init_metadata.compute`; fixed `enable_wiregaurd` typo |

---

## 5. Configuration Parameters

### 5.1 Role Defaults — `pxe_buildstream_manager/defaults/main.yml`

| Variable | Type | Default | Description |
|---|---|---|---|
| `phone_home_retries` | Integer | `120` | Maximum poll attempts (120 × 15s = 30 min) |
| `phone_home_delay` | Integer | `15` | Seconds between poll attempts |
| `phone_home_initial_pause` | Integer | `5` | Minutes to pause before polling begins |

### 5.2 Required Facts (Set in Play 3 of `set_pxe_boot.yml`)

| Fact | Source | Description |
|---|---|---|
| `pxe_start_epoch` | `ansible_date_time.epoch` | UTC epoch captured before PXE reboot, used for journal time-gating |
| `target_node_admin_ips` | `pxe_mapping_file.csv` (`ADMIN_IP` column) | List of node admin IPs to verify |

### 5.3 Cloud-Init Vendor-Data Variables (Dell Recipe)

| Variable | Default | Description |
|---|---|---|
| `enable_wireguard` | `false` | Toggles WireGuard endpoint vs admin IP |
| `cluster_boot_ip` | OIM admin IP | Used as endpoint when WireGuard disabled |
| `cloud_init_base_port` | `8081` | Cloud-init-server port |
| `cloud_init_base_url` | `http://<endpoint>:<port>` | Full URL injected into vendor-data |

---

## 6. Implementation Details

### 6.1 New Task File — `cloudinit_phone_home.yml`

```yaml
# Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
---
# ─────────────────────────────────────────────────────────────────────────
# Task: cloudinit_phone_home.yml
# Purpose: Wait for all PXE-booted nodes to complete cloud-init
#          and send phone-home callback to cloud-init-server.
# Called from: set_pxe_boot.yml (Play 7)
# Condition: Only runs when enable_build_stream is true
# ─────────────────────────────────────────────────────────────────────────

- name: "[Phone-Home] Assert required facts are available"
  ansible.builtin.assert:
    that:
      - pxe_start_epoch is defined
      - pxe_start_epoch | string | length > 0
      - target_node_admin_ips is defined
      - target_node_admin_ips | length > 0
    fail_msg: |
      FATAL: Required facts missing for phone-home verification.
      pxe_start_epoch = {{ pxe_start_epoch | default('UNDEFINED') }}
      target_node_admin_ips = {{ target_node_admin_ips | default('UNDEFINED') }}
      Ensure Play 3 ran with gather_facts: true and set_fact cacheable: true.
    success_msg: >
      [Phone-Home] Facts confirmed.
      epoch={{ pxe_start_epoch }}
      nodes={{ target_node_admin_ips }}

- name: "[Phone-Home] Wait {{ phone_home_initial_pause }} minutes for nodes to begin cloud-init"
  ansible.builtin.pause:
    minutes: "{{ phone_home_initial_pause | default(5) }}"
    prompt: >
      Waiting for nodes to boot and begin cloud-init
      before starting phone-home polling...

- name: "[Phone-Home] Wait for cloud-init phone-home from all nodes"
  ansible.builtin.shell: |
    set -o pipefail
    MISSING_NODES=0
    OUTPUT=""

    JOURNAL_OUT=$(journalctl -u cloud-init-server \
      --since "@{{ pxe_start_epoch }}" \
      --no-pager 2>/dev/null)

    for ip in {{ target_node_admin_ips | join(' ') }}; do
      if echo "$JOURNAL_OUT" | grep -w "Phone home request from $ip" > /dev/null 2>&1; then
        OUTPUT="${OUTPUT}✅ Phone-home confirmed: $ip\n"
      else
        OUTPUT="${OUTPUT}⏳ Still waiting for phone-home: $ip\n"
        MISSING_NODES=1
      fi
    done

    echo -e "$OUTPUT"
    exit $MISSING_NODES
  args:
    executable: /bin/bash
  register: phone_home_poll_result
  until: phone_home_poll_result.rc == 0
  retries: "{{ phone_home_retries | default(120) }}"
  delay: "{{ phone_home_delay | default(15) }}"
  changed_when: false
  become: true

- name: "[Phone-Home] Display phone-home status per node"
  ansible.builtin.debug:
    msg: "{{ phone_home_poll_result.stdout_lines }}"

- name: "[Phone-Home] All nodes completed cloud-init successfully"
  ansible.builtin.debug:
    msg: >
      [Phone-Home] ✅ All {{ target_node_admin_ips | length }}
      nodes completed cloud-init and phoned home successfully.
      Proceeding with BuildStream post-processing.
```

### 6.2 Modified `set_pxe_boot.yml` (Relevant Sections)

```yaml
# Play 3: Compute effective inventory + capture pre-boot state
- name: "[BSM] Compute effective restart inventory (diff + failed retry)"
  hosts: localhost
  connection: local
  gather_facts: true
  tasks:
    - name: Compute effective restart inventory
      ansible.builtin.include_role:
        name: pxe_buildstream_manager
        tasks_from: compute_effective_inventory
      when: enable_build_stream | default(false) | bool

    - name: Capture PXE boot start epoch for phone-home time-gating
      ansible.builtin.set_fact:
        pxe_start_epoch: "{{ ansible_date_time.epoch }}"
        cacheable: true

    - name: Read PXE mapping file for admin IPs
      community.general.read_csv:
        path: "{{ input_project_dir | default('/opt/omnia/input/project_default') }}/pxe_mapping_file.csv"
      register: pxe_csv_for_phone_home
      when: groups['bmc'] is defined and groups['bmc'] | length > 0

    - name: Build list of target node admin IPs for phone-home verification
      ansible.builtin.set_fact:
        target_node_admin_ips: "{{ pxe_csv_for_phone_home.list | map(attribute='ADMIN_IP') | list }}"
        cacheable: true
      when:
        - groups['bmc'] is defined
        - groups['bmc'] | length > 0
        - pxe_csv_for_phone_home is defined
        - pxe_csv_for_phone_home.list is defined

# Play 7: Phone-home verification via BSM role
- name: "[Phone-Home] Wait for cloud-init completion on all nodes"
  hosts: oim
  connection: ssh
  gather_facts: false
  become: true
  tasks:
    - name: Run cloud-init phone-home verification via BSM role
      ansible.builtin.include_role:
        name: pxe_buildstream_manager
        tasks_from: cloudinit_phone_home
      when: hostvars['localhost']['enable_build_stream'] | default(false) | bool
      vars:
        pxe_start_epoch: "{{ hostvars['localhost']['pxe_start_epoch'] }}"
        target_node_admin_ips: "{{ hostvars['localhost']['target_node_admin_ips'] }}"
```

### 6.3 OpenCHAMI Cloud-Init Template Addition

Append to `cluster_cloud_init_templates` in the Dell deployment recipe:

```yaml
- name: phone_home
  description: "Phone-home callback when cloud-init completes successfully"
  file:
    encoding: plain
    content: |
      ## template: jinja
      #cloud-config
      {{ _cloud_init_merge | to_yaml }}
      {% raw %}
      phone_home:
        post:
          - pub_key_rsa
          - pub_key_ecdsa
          - pub_key_ed25519
          - instance_id
          - hostname
          - fqdn
        tries: 5
        url: {{ ds.meta_data.instance_data.v1.vendor_data.cloud_init_base_url }}/phone-home/{{ v1.instance_id }}/
      {% endraw %}
```

Add to `cluster_cloud_init_metadata.compute.meta-data`:

```yaml
cloud_init_base_url: "{{ cloud_init_base_url }}"
```

### 6.4 POST Payload Sent by Each Compute Node

```
POST /phone-home/<instance_id>/ HTTP/1.1
Host: <cluster_boot_ip>:8081
Content-Type: application/x-www-form-urlencoded

pub_key_rsa=AAAA...&pub_key_ecdsa=AAAA...&pub_key_ed25519=AAAA...
&instance_id=de0001&hostname=de0001&fqdn=de0001.cluster.local
```

---

## 7. Polling Logic Design Decisions

| Decision | Rationale |
|---|---|
| **Single bash loop checks all IPs** | Avoids Ansible's sequential `until` per-IP blocking; first booted node detected immediately |
| **`set -o pipefail` + redirect to `/dev/null`** | Avoids SIGPIPE rc=141 caused by `grep -m 1` killing `journalctl` mid-stream |
| **`grep -w` (whole word match)** | Prevents partial IP collisions (e.g. `182.11.0.5` matching `182.11.0.51`) |
| **`set_fact ... cacheable: true`** | Variables persist across play boundaries via `hostvars['localhost']` |
| **`ansible_date_time.epoch` (UTC)** | Timezone-immune; consistent regardless of node/server TZ settings |
| **`become: true`** | `journalctl -u <service>` requires root for non-root users |
| **5-minute initial pause** | Eliminates wasted retries during the deterministic boot window |
| **Conditional on `enable_build_stream`** | Consistent with all other tasks in `pxe_buildstream_manager` |
| **Run on `oim` host via SSH** | Journal lives on the OIM, not on Ansible controller |

---

## 8. Integration with `set_pxe_boot.yml` — Updated Play Order

| Play | Purpose | Status |
|---|---|
| 1 | Validate BMC inventory | Unchanged |
| 2 | Fetch credentials | Unchanged |
| 3 | BSM compute inventory + capture `pxe_start_epoch` + read PXE mapping | **Modified** |
| 4 | iDRAC PXE reboot | Unchanged |
| 5 | Synchronized iDRAC reboot reporting | Unchanged |
| 6 | Create `oim` group | Unchanged |
| 7 | **Phone-home verification (`include_role` from BSM)** | **NEW** |
| 8 | BSM post-processing (writes `failed_nodes.json`) | **Reordered after Play 7** |
| 9 | GitLab upload | Unchanged |

---

## 9. Expected Outcomes & Success Criteria

### 9.1 Success Path

- Every IP in `target_node_admin_ips` produces a matching `INF Phone home request from <ip>` entry in the `cloud-init-server` journal **after** `pxe_start_epoch`.
- Final shell rc = 0 → `until` loop exits cleanly.
- BSM proceeds to write accurate `failed_nodes.json`.
- Playbook completes successfully.
- GitLab upload reflects accurate provisioning state.

### 9.2 Failure Path

- One or more IPs never produce a phone-home entry within 30 minutes (120 retries × 15s).
- Final retry returns rc=1 → Ansible marks task FAILED.
- Playbook stops; BSM does **not** write inaccurate state.
- Operator sees explicit per-node status: `⏳ Still waiting: <ip>` for offending nodes.

### 9.3 Sample Successful Output

```
TASK [pxe_buildstream_manager : [Phone-Home] Wait 5 minutes for nodes to begin cloud-init]
[oim] Pausing for 300 seconds...

TASK [pxe_buildstream_manager : [Phone-Home] Wait for cloud-init phone-home from all nodes]
FAILED - RETRYING: [oim] (120 retries left).
FAILED - RETRYING: [oim] (119 retries left).
ok: [oim]

TASK [pxe_buildstream_manager : [Phone-Home] Display phone-home status per node]
ok: [oim] => {
    "msg": [
        "✅ Phone-home confirmed: 182.11.0.51",
        "✅ Phone-home confirmed: 182.11.0.52"
    ]
}

TASK [pxe_buildstream_manager : [Phone-Home] All nodes completed cloud-init successfully]
ok: [oim] => {
    "msg": "[Phone-Home] ✅ All 2 nodes completed cloud-init and phoned home successfully."
}
```

---

## 10. Error Handling & Diagnostics

### 10.1 Common Failure Scenarios

| Symptom | Likely Cause | Resolution |
|---|---|---|
| `FATAL: Required facts missing` from assert | Play 3 did not run or `gather_facts: true` missing | Verify Play 3 executes with facts and `cacheable: true` |
| `Phone home request not found` for all nodes | `cloud_init_base_url` missing in vendor-data | Add `cloud_init_base_url` to `cluster_cloud_init_metadata.compute` |
| `phone_home` template returns 13 bytes (empty) | Group missing from cloud-init-server memstore (lost on restart) | Re-post template via `ochami` CLI or persistent seed |
| Permission denied reading journal | Task missing `become: true` | Confirm `become: true` is set on the play |
| Sequential blocking on first IP only | Old per-IP `loop` with `until` | Use single bash loop iterating all IPs |
| Shell exits rc=141 with `grep -m 1` | SIGPIPE + `pipefail` | Replace `grep -m 1` with `grep ... > /dev/null` |
| Wrong timezone in journal filter | Used `date "+%Y-%m-%d %H:%M:%S"` (local TZ) | Use `ansible_date_time.epoch` + `--since "@<epoch>"` |
| `oim` host/group collision warning | `create_container_group` registers same name | Warning is benign; Ansible resolves correctly |

### 10.2 Manual Verification Commands

```bash
# 1. Confirm cloud-init-server is running
systemctl status cloud-init-server

# 2. Confirm phone-home entries exist in the journal
journalctl -u cloud-init-server --no-pager | grep "Phone home request"

# 3. Test the exact polling logic
EPOCH=$(date "+%s")
journalctl -u cloud-init-server --since "@${EPOCH}" --no-pager | \
  grep -w "Phone home request from <node_ip>"

# 4. Confirm cloud-init-server is listening on port 8081
ss -tlnp | grep 8081

# 5. Check that phone_home group is registered with the server
curl -s http://<cluster_boot_ip>:8081/cloud-init/admin/groups | \
  jq '.[] | select(.name=="phone_home")'

# 6. Verify rendered user-data for a specific node
curl -s "http://<cluster_boot_ip>:8081/cloud-init/<node_id>/user-data" | grep -A6 phone_home
```

---

## 11. Testing Strategy

### 11.1 Unit Tests

- **Task syntax validation:** `ansible-lint utils/roles/pxe_buildstream_manager/tasks/cloudinit_phone_home.yml`
- **Variable assertion:** Run task without setting `pxe_start_epoch` — confirm assert fires.
- **Idempotency:** Re-running phone-home task with already-confirmed nodes should pass instantly.

### 11.2 Integration Tests

| Scenario | Expected Outcome |
|---|---|
| All nodes phone home within timeout | Playbook succeeds; `failed_nodes.json` empty |
| One node fails to phone home | Playbook fails with explicit `⏳ Still waiting: <ip>` for that node |
| `enable_build_stream: false` | Phone-home task skipped entirely |
| Cloud-init-server restarts mid-run | Polling continues; journal entries persist |
| Multiple nodes boot at different times | Each detected as it phones home, no sequential blocking |

### 11.3 Edge Cases

- Empty `pxe_mapping_file.csv` → `target_node_admin_ips` empty → assert fails fast.
- Mixed IP formats in CSV → `grep -w` ensures exact match prevents false positives.
- Cloud-init-server unavailable → `journalctl` returns empty → all nodes flagged as missing → fails after timeout.
- Pre-existing phone-home entries from older runs → epoch filter excludes them.

---

## 12. Security & Performance Considerations

### 12.1 Security

| Concern | Mitigation |
|---|---|
| SSH host key exposure in phone-home payload | Cloud-init payload only sent to internally-trusted OIM admin IP |
| `become: true` on OIM | Required only for journal access; no destructive operations |
| Journal log access | Standard systemd permission model; audited via `journalctl` |
| `phone_home` URL injection | Rendered server-side from trusted vendor-data; no user input |

### 12.2 Performance

| Aspect | Value |
|---|---|
| Initial pause | 5 minutes (configurable) |
| Maximum polling duration | 30 minutes (120 × 15s, configurable) |
| Journal query frequency | One full read per 15-second cycle |
| Memory overhead | Negligible (single bash invocation per cycle) |
| Network overhead | None (all polling local to OIM) |
| Best-case completion | ~5 min 15s (pause + first poll) |
| Typical completion | ~8–12 min for 2-node cluster |

---

**End of Module Specification — Cloud-Init Phone-Home Verification (v1.0)**
