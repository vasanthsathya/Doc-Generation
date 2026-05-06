
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

General 

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
 * [ Add / Remove Nodes ](../Operations/add_remove_nodes.html)

Troubleshooting 
 * General [ General ](general.html) Table of contents 
 * [ Hostname changes after OIM reboot ](#hostname-changes-after-oim-reboot)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ Hostname changes after OIM reboot ](#hostname-changes-after-oim-reboot)

 1. [ Home ](../index.html)
 2. [ Troubleshooting ](index.html)

# General Issues[¶](#general-issues "Permanent link")

Common issues that affect the OIM, SSH connectivity, containers, and Ansible Vault operations.

## Hostname changes after OIM reboot[¶](#hostname-changes-after-oim-reboot "Permanent link")

Symptom

After rebooting the OIM, the hostname reverts to `localhost` or a different value, causing Ansible playbooks and service connections to fail.

Cause

The OIM's hostname was set temporarily with `hostnamectl` but not persisted in `/etc/hostname`, or a DHCP-assigned hostname overrides the static setting on boot.

Resolution

 1. Set the hostname permanently:

 
 
 hostnamectl set-hostname oim.example.com
 

 1. Verify it persisted in `/etc/hostname`:

 
 
 cat /etc/hostname
 

 1. Ensure the hostname is also in `/etc/hosts`:

 
 
 127.0.0.1 localhost
 <oim_ip> oim.example.com oim
 

 1. If DHCP is overriding the hostname, configure the DHCP client to preserve the static hostname by adding the following to `/etc/NetworkManager/conf.d/90-hostname.conf`:

 
 
 [main]
 hostname-mode=none
 

## SSH key mismatches[¶](#ssh-key-mismatches "Permanent link")

Symptom

SSH connections from the OIM to cluster nodes fail with:
 
 
 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 @ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 

Cause

The target node was re-provisioned or re-imaged, generating new SSH host keys that conflict with the cached keys in `~/.ssh/known_hosts` on the OIM.

Resolution

 1. Remove the stale key for the affected host:

 
 
 ssh-keygen -R <node_hostname_or_ip>
 

 1. Reconnect to accept the new key:

 
 
 ssh <node_hostname_or_ip>
 

 1. To prevent this issue across bulk re-provisions, clear all known_hosts entries for cluster nodes:

 
 
 # Remove entries for a range of IPs
 for i in $(seq 101 110); do
 ssh-keygen -R 10.5.0.$i
 done
 

## Container startup failures[¶](#container-startup-failures "Permanent link")

Symptom

One or more Podman containers fail to start after an OIM reboot, or `podman ps` shows containers in `Exited` or `Error` state.

Cause

Possible causes include:

 * The Podman service (`podman.socket`) did not start.
 * Containers were not configured to auto-restart.
 * Disk space exhaustion prevents container layer extraction.
 * Port conflicts with another service.

Resolution

 1. Check the container status and error message:

 
 
 podman ps -a
 podman logs <container_name>
 

 1. Attempt a manual restart:

 
 
 podman start <container_name>
 

 1. If disk space is the issue:

 
 
 df -h /
 podman system prune --force
 

 1. If a port conflict is reported, identify the conflicting process:

 
 
 ss -tlnp | grep <port_number>
 

 1. If containers consistently fail after reboot, verify that Podman pods have auto-start enabled:

 
 
 podman generate systemd --name <pod_name> --files
 systemctl enable pod-<pod_name>.service
 

## `ssh omnia_core` fails after `sudo`[¶](#ssh-omnia_core-fails-after-sudo "Permanent link")

Symptom

Running `ssh omnia_core` as a non-root user (or after `sudo su`) returns a connection error or permission denied:
 
 
 Permission denied (publickey).
 

Cause

The `omnia_core` container is configured with SSH keys for the `root` user. When you use `sudo su` to become root, the SSH agent and key environment may not be inherited.

Resolution

Log in as `root` directly instead of using `sudo`:
 
 
 # Instead of:
 sudo su
 ssh omnia_core # <-- fails
 
 # Do this:
 ssh root@<oim_ip>
 ssh omnia_core # <-- works
 

Alternatively, explicitly specify the SSH key:
 
 
 ssh -i /root/.ssh/id_rsa omnia_core
 

## Ansible Vault encrypted file issues[¶](#ansible-vault-encrypted-file-issues "Permanent link")

Symptom

Ansible playbooks fail with:
 
 
 ERROR! Attempting to decrypt but no vault secrets found
 

Or you cannot view the contents of encrypted credential files.

Cause

The vault password was not provided when running the playbook, or the vault password file path is incorrect.

Resolution

 1. **View an encrypted file** without editing:

 
 
 ansible-vault view input/credentials.yml
 

 1. **Edit an encrypted file:**

 
 
 ansible-vault edit input/credentials.yml
 

 1. **Run a playbook with vault password prompt:**

 
 
 ansible-playbook playbooks/omnia.yml --ask-vault-pass
 

 1. **Run a playbook with a vault password file:**

 
 
 ansible-playbook playbooks/omnia.yml --vault-password-file /root/.vault_pass
 

 1. If you have forgotten the vault password, you will need to recreate the credentials file. There is no way to recover an AES-256 encrypted vault without the original password:

 
 
 # Back up the old file
 cp input/credentials.yml input/credentials.yml.bak
 
 # Create a new encrypted file
 ansible-vault create input/credentials.yml
 

Info

 * [Log Management](../Operations/log_management.html) \-- Where to find logs for deeper diagnosis.
 * [Oim Cleanup](../Operations/oim_cleanup.html) \-- Full OIM reset if issues persist.

Back to top [ Previous Troubleshooting ](index.html) [ Next Provisioning ](provisioning.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
