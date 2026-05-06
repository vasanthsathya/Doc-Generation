
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Best Practices Checklist 

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
 * Best Practices Checklist [ Best Practices Checklist ](best_practices_checklist.html) Table of contents 
 * [ BIOS and firmware ](#bios-and-firmware)

Troubleshooting 
 * [ General ](../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ BIOS and firmware ](#bios-and-firmware)

 1. [ Home ](../index.html)
 2. [ Operations ](index.html)

# Best Practices Checklist[¶](#best-practices-checklist "Permanent link")

A consolidated checklist of recommendations for deploying and operating an Omnia cluster. Each item links to the relevant documentation section for detailed procedures.

## BIOS and firmware[¶](#bios-and-firmware "Permanent link")

| Best Practice | Reference 
---|---|--- 
☐ | **Disable PowerCap** on all compute nodes to ensure maximum CPU performance. PowerCap can throttle compute-intensive HPC workloads. | [Prerequisites Checklist](../GetStarted/prerequisites_checklist.html) 
☐ | **Set BIOS to Performance mode** on all compute nodes. The `Performance` power profile maximizes clock speeds and disables power-saving C-states that introduce latency. | [Prerequisites Checklist](../GetStarted/prerequisites_checklist.html) 
☐ | **Keep iDRAC firmware current** on all nodes. Firmware updates fix bugs, improve Redfish API reliability, and patch security vulnerabilities. Use Dell Repository Manager or `racadm` for updates. | [Security Hardening](security_hardening.html) 
 
## Playbook execution[¶](#playbook-execution "Permanent link")

| Best Practice | Reference 
---|---|--- 
☐ | **Run playbooks from their directory** using `cd`. Omnia playbooks use relative paths for roles and configuration files. Always `cd /omnia` before running `ansible-playbook`. | [Index](../HowTo/index.html) 
☐ | **Review prerequisites before running playbooks.** Each playbook has specific input files and environment requirements. Check the corresponding how-to guide before execution. | [Index](../HowTo/index.html) 
 
## Storage and telemetry[¶](#storage-and-telemetry "Permanent link")

| Best Practice | Reference 
---|---|--- 
☐ | **Provision sufficient NFS storage for telemetry.** The telemetry pipeline (VictoriaMetrics, Kafka) can generate significant data volumes. Allocate at least 500 GB of NFS-backed persistent storage for telemetry retention. | [Setup Telemetry](../HowTo/Telemetry/setup_telemetry.html) 
☐ | **Prefer the PowerScale CSI driver over external NFS** for Kubernetes persistent volumes. The CSI driver provides dynamic provisioning, better performance, and snapshot support compared to static NFS mounts. | [Deploy Powerscale Csi](../HowTo/Kubernetes/deploy_powerscale_csi.html) 
☐ | **Ensure external NFS is accessible via the admin network.** If using external NFS (not PowerScale), verify that the NFS server is reachable from all nodes on the admin network and that firewall rules allow NFS traffic (ports 2049, 111). | [Configure Nfs](../HowTo/Storage/configure_nfs.html) 
 
## System administration[¶](#system-administration "Permanent link")

| Best Practice | Reference 
---|---|--- 
☐ | **Minimize OIM reboots.** The OIM hosts critical Podman containers that provide provisioning, DHCP, and management services. Rebooting the OIM interrupts these services and may cause hostname or IP changes. Plan reboots during maintenance windows only. | [General](../Troubleshooting/general.html) 
☐ | **Keep Firefox updated on RHEL OIM.** If you use the AWX web UI on the OIM, ensure Firefox (the default RHEL browser) is updated to avoid TLS compatibility and rendering issues. | [Security Hardening](security_hardening.html) 
☐ | **Run** `yum update --security` **routinely.** Apply security patches on the OIM and all cluster nodes on a regular schedule (monthly recommended). Drain Slurm nodes before applying updates. | [Security Hardening](security_hardening.html) 
☐ | **Sync system time across the OIM and all nodes.** Use `chrony` or `ntpd` to maintain synchronized clocks. Time drift causes Kerberos authentication failures, Slurm scheduling issues, and inaccurate telemetry timestamps. | [Prerequisites Checklist](../GetStarted/prerequisites_checklist.html) 
 
## Pre-deployment summary[¶](#pre-deployment-summary "Permanent link")

Use this condensed list as a quick pre-flight check before running any Omnia deployment:

 1. ☐ BIOS: PowerCap disabled, Performance mode set.
 2. ☐ iDRAC firmware updated to the latest supported version.
 3. ☐ Network: admin and BMC VLANs configured, NFS accessible.
 4. ☐ System clocks synchronized (chrony/NTP).
 5. ☐ OIM meets minimum requirements (4+ cores, 32+ GB RAM, 256+ GB disk).
 6. ☐ Input files reviewed and populated (mapping file, config files).
 7. ☐ Credentials encrypted with Ansible Vault.
 8. ☐ Sufficient NFS storage allocated for telemetry.
 9. ☐ Firefox updated (if using AWX web UI).
 10. ☐ Security updates applied: `yum update --security`.

Info

 * [Prerequisites Checklist](../GetStarted/prerequisites_checklist.html) \-- Detailed prerequisites for all deployment paths.
 * [Security Hardening](security_hardening.html) \-- Full security hardening procedures.
 * [Log Management](log_management.html) \-- Log monitoring and rotation configuration.

Back to top [ Previous Security Hardening ](security_hardening.html) [ Next Troubleshooting ](../Troubleshooting/index.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
