
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Log Management 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../index.html)

[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../index.html)

Overview 
 * [ Architecture ](../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](add_remove_nodes.html)
 * Log Management [ Log Management ](log_management.html) Table of contents 
 * [ Log locations ](#log-locations)

Troubleshooting 
 * [ General ](../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ Log locations ](#log-locations)

 1. [ Home ](../index.html)
 2. [ Operations ](index.html)

# Log Management[¶](#log-management "Permanent link")

Omnia generates logs at multiple levels: Ansible playbook execution, container service logs, cluster service logs, and operating system logs. Understanding where logs are stored and how they are rotated is essential for diagnosing issues and maintaining a healthy cluster.

## Log locations[¶](#log-locations "Permanent link")

### Playbook logs[¶](#playbook-logs "Permanent link")

All Ansible playbook execution logs are written to the OIM host filesystem, even though playbooks run inside the `omnia_core` Podman container:

Path | Description 
---|--- 
`/opt/omnia/log/core/playbooks/` | Primary log directory for all Omnia playbook runs. Each playbook generates a timestamped log file (for example, `omnia_2024-01-15.log`). 
`/opt/omnia/log/core/playbooks/discovery.log` | Node discovery and provisioning log. 
`/opt/omnia/log/core/playbooks/local_repo.log` | Local repository logs. 
`/opt/omnia/log/core/playbooks/prepare_oim.log` | Prepare OIM logs. 
`/opt/omnia/log/core/playbooks/provision.log` | Provision logs. 
`/opt/omnia/log/core/playbooks/omnia.log` | Main cluster deployment log (Slurm, Kubernetes, authentication). 
`/opt/omnia/log/core/playbooks/scheduler.log` | Scheduler logs. 
`/opt/omnia/log/core/playbooks/telemetry.log` | Telemetry stack deployment log. 
`/opt/omnia/log/core/playbooks/utils.log` | Utility logs. 
`/opt/omnia/log/core/playbooks/credential_utility.log` | Credential utility logs. 
`/opt/omnia/log/core/playbooks/validation_omnia_project_default.log` | Omnia input validation report logs. 
`/opt/omnia/log/core/playbooks/input_validation.log` | Omnia input validation playbook logs. 
`/opt/omnia/log/openchami/*.log` | OpenCHAMI playbook logs. 
`/opt/omnia/log/pulp/*.log` | Pulp container logs. 
`/opt/omnia/log/local_repo/*.log` | Local repo logs. 
`/opt/omnia/log/core/container/*.log` | Core container logs. 
 
Additionally, an aggregate of the events taking place during storage, scheduler, and network role installation called `omnia.log` is created in `/var/log`.

Tip

To follow a playbook log in real time while a playbook is running, open a second terminal on the OIM host:
 
 
 tail -f /opt/omnia/log/core/playbooks/omnia.log
 

### Container logs[¶](#container-logs "Permanent link")

OIM services run as Podman containers. Access their logs with the `podman logs` command:

Run on: OIM host
 
 
 # List all running containers
 podman ps
 
 # View logs for a specific container
 podman logs omnia_core
 podman logs ochami-smd
 podman logs ochami-bss
 podman logs coredhcp
 
 # Follow logs in real time
 podman logs -f omnia_core
 
 # View only the last 100 lines
 podman logs --tail 100 omnia_core
 

Container | What it logs 
---|--- 
`omnia_core` | Ansible execution output, SSH connections to managed nodes. 
`ochami-smd` | OpenCHAMI State Manager Daemon: node inventory, hardware discovery. 
`ochami-bss` | Boot Script Service: PXE boot script generation, boot requests. 
`coredhcp` | DHCP lease assignments during provisioning. 
`pulp` | Repository sync status, package downloads. 
 
### OpenCHAMI logs[¶](#openchami-logs "Permanent link")

OpenCHAMI components write structured JSON logs accessible via Podman:

Run on: OIM host
 
 
 # SMD logs (node state changes)
 podman logs ochami-smd 2>&1 | jq '.'
 
 # BSS logs (boot requests)
 podman logs ochami-bss 2>&1 | jq '.'
 

### Slurm logs[¶](#slurm-logs "Permanent link")

On Slurm cluster nodes, logs are stored in standard Slurm log directories:

Path | Description 
---|--- 
`/var/log/slurm/slurmctld.log` | Slurm controller daemon log (on the control node). 
`/var/log/slurm/slurmd.log` | Slurm compute daemon log (on each compute node). 
`/var/log/slurm/slurmdbd.log` | Slurm database daemon log (job accounting). 
 
Run on: Slurm nodes
 
 
 # On the Slurm control node
 tail -f /var/log/slurm/slurmctld.log
 
 # On a compute node
 tail -f /var/log/slurm/slurmd.log
 

### Kubernetes logs[¶](#kubernetes-logs "Permanent link")

On Kubernetes cluster nodes, use `kubectl` or `journalctl` to access logs:

Run on: Kubernetes nodes
 
 
 # Pod logs
 kubectl logs <pod_name> -n <namespace>
 
 # Kubelet logs on a specific node
 ssh <kube_node> journalctl -u kubelet -f
 

## Logrotate configuration[¶](#logrotate-configuration "Permanent link")

Omnia configures `logrotate` to manage log file sizes on the OIM and prevent disk exhaustion. The default configuration rotates logs based on size and age.

### Default settings[¶](#default-settings "Permanent link")

File: /etc/logrotate.d/omnia
 
 
 # /etc/logrotate.d/omnia
 /opt/omnia/log/core/playbooks/*.log {
 weekly
 rotate 12
 compress
 delaycompress
 missingok
 notifempty
 create 0640 root root
 }
 

This configuration:

 * Rotates log files **weekly**.
 * Keeps **12 rotated files** (approximately 3 months of history).
 * **Compresses** rotated files with gzip (after a one-rotation delay).
 * Skips rotation if the log file is missing or empty.

### Customizing logrotate[¶](#customizing-logrotate "Permanent link")

To adjust the rotation policy (for example, to rotate daily in high-throughput environments):

 1. Edit the logrotate configuration:

 
 
 vi /etc/logrotate.d/omnia
 

 1. Change `weekly` to `daily` and adjust `rotate` to the desired number of files:

 
 
 /opt/omnia/log/core/playbooks/*.log {
 daily
 rotate 30
 compress
 delaycompress
 missingok
 notifempty
 create 0640 root root
 }
 

 1. Test the configuration:

 
 
 logrotate -d /etc/logrotate.d/omnia
 

 1. Force an immediate rotation (optional):

 
 
 logrotate -f /etc/logrotate.d/omnia
 

### Slurm logrotate[¶](#slurm-logrotate "Permanent link")

Slurm logs are rotated separately. Omnia installs a Slurm-specific logrotate configuration on the control node:

File: /etc/logrotate.d/slurm
 
 
 # /etc/logrotate.d/slurm
 /var/log/slurm/*.log {
 weekly
 rotate 8
 compress
 delaycompress
 missingok
 notifempty
 sharedscripts
 postrotate
 /usr/bin/pkill -HUP slurmctld 2>/dev/null || true
 /usr/bin/pkill -HUP slurmd 2>/dev/null || true
 endscript
 }
 

## Sample log output[¶](#sample-log-output "Permanent link")

A sample of the `omnia.log` is provided below:

Sample omnia.log output
 
 
 2021-02-15 15:17:36,877 p=2778 u=omnia n=ansible | [WARNING]: provided hosts
 list is empty, only localhost is available. Note that the implicit localhost does not
 match 'all'
 2021-02-15 15:17:37,396 p=2778 u=omnia n=ansible | PLAY [Executing omnia roles]
 ************************************************************************************
 2021-02-15 15:17:37,454 p=2778 u=omnia n=ansible | TASK [Gathering Facts]
 *****************************************************************************************
 2021-02-15 15:17:38,856 p=2778 u=omnia n=ansible | ok: [localhost]
 2021-02-15 15:17:38,885 p=2778 u=omnia n=ansible | TASK [common : Mount Path]
 **************************************************************************************
 2021-02-15 15:17:38,969 p=2778 u=omnia n=ansible | ok: [localhost]
 

These logs are intended to enable debugging.

Note

The Omnia product recommends that product users apply masking rules on personal identifiable information (PII) in the logs before sending to external monitoring applications or sources.

## Logging format[¶](#logging-format "Permanent link")

Every log message begins with a timestamp and also carries information on the invoking play and task. The format is described in the following table:

Field | Format | Sample Value 
---|---|--- 
Timestamp | `yyyy-mm-dd h:m:s` | `2021-02-15 15:17` 
Process ID | `p=xxxx` | `p=2778` 
User | `u=xxxx` | `u=omnia` 
Name of the process executing | `n=xxxx` | `n=ansible` 
The task being executed/invoked | `PLAY/TASK` | `PLAY [Executing omnia roles]` / `TASK [Gathering Facts]` 
Error | `fatal: [hostname]: Error Message` | `fatal: [localhost]: FAILED! => {"msg": "lookup_plugin.lines}` 
Warning | `[WARNING]: warning message` | `[WARNING]: provided hosts list is empty` 
 
## Troubleshooting log issues[¶](#troubleshooting-log-issues "Permanent link")

Issue | Resolution 
---|--- 
**Disk full on OIM** | Check log sizes: `du -sh /opt/omnia/log/core/playbooks/`. Force logrotate: `logrotate -f /etc/logrotate.d/omnia`. Remove old compressed logs if needed. 
**No playbook logs appearing** | Verify the `omnia_core` container is running: `podman ps`. Check that the log volume is mounted: `podman inspect omnia_core \| grep -A5 Mounts`. 
**Container logs too verbose** | Adjust the log level in the container's configuration file and restart the container: `podman restart <container_name>`. 
**Slurm logs not rotating** | Verify logrotate configuration exists: `cat /etc/logrotate.d/slurm`. Test with: `logrotate -d /etc/logrotate.d/slurm`. Check if `crond` is running: `systemctl status crond`. 
 
Info

 * [General](../Troubleshooting/general.html) \-- General troubleshooting that uses logs as a primary diagnostic tool.
 * [Best Practices Checklist](best_practices_checklist.html) \-- Storage and maintenance best practices.

Back to top [ Previous OIM Cleanup ](oim_cleanup.html) [ Next Security Hardening ](security_hardening.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
