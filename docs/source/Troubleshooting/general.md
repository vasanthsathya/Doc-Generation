# General Issues

Common issues that affect the OIM, SSH connectivity, containers, and Ansible Vault operations.

## Hostname changes after OIM reboot

After rebooting the OIM, the hostname reverts to `localhost` or a different value, causing Ansible playbooks and service connections to fail.

The OIM's hostname was set temporarily with `hostnamectl` but not persisted in `/etc/hostname`, or a DHCP-assigned hostname overrides the static setting on boot.

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

## SSH key mismatches

SSH connections from the OIM to cluster nodes fail with:

 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 @ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

The target node was re-provisioned or re-imaged, generating new SSH host keys that conflict with the cached keys in `~/.ssh/known_hosts` on the OIM.

 1. Remove the stale key for the affected host:

 ssh-keygen -R <node_hostname_or_ip>

 1. Reconnect to accept the new key:

 ssh <node_hostname_or_ip>

 1. To prevent this issue across bulk re-provisions, clear all known_hosts entries for cluster nodes:

 # Remove entries for a range of IPs
 for i in $(seq 101 110); do
 ssh-keygen -R 10.5.0.$i
 done

## Container startup failures

One or more Podman containers fail to start after an OIM reboot, or `podman ps` shows containers in `Exited` or `Error` state.

Possible causes include:

 * The Podman service (`podman.socket`) did not start.
 * Containers were not configured to auto-restart.
 * Disk space exhaustion prevents container layer extraction.
 * Port conflicts with another service.

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

## `ssh omnia_core` fails after `sudo`

Running `ssh omnia_core` as a non-root user (or after `sudo su`) returns a connection error or permission denied:

 Permission denied (publickey).

The `omnia_core` container is configured with SSH keys for the `root` user. When you use `sudo su` to become root, the SSH agent and key environment may not be inherited.

Log in as `root` directly instead of using `sudo`:

 # Instead of:
 sudo su
 ssh omnia_core # <-- fails

 # Do this:
 ssh root@<oim_ip>
 ssh omnia_core # <-- works

Alternatively, explicitly specify the SSH key:

 ssh -i /root/.ssh/id_rsa omnia_core

## Ansible Vault encrypted file issues

Ansible playbooks fail with:

 ERROR! Attempting to decrypt but no vault secrets found

Or you cannot view the contents of encrypted credential files.

The vault password was not provided when running the playbook, or the vault password file path is incorrect.

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

Copyright © 2025 Dell Technologies. All rights reserved.