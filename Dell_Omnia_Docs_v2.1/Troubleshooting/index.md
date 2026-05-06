
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Troubleshooting 

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
 * [ General ](general.html)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ Troubleshooting approach ](#troubleshooting-approach)

 1. [ Home ](../index.html)
 2. [ Troubleshooting ](index.html)

# Troubleshooting[¶](#troubleshooting "Permanent link")

Symptom-driven guides for diagnosing and resolving issues with your Omnia cluster. Each entry follows a consistent **Symptom > Cause > Resolution** format so you can quickly identify the problem and apply the fix.

## Troubleshooting approach[¶](#troubleshooting-approach "Permanent link")

When you encounter an issue, follow this general diagnostic flow:

 1. **Check logs first.** Most issues leave a clear trace in the logs. See [Log Management](../Operations/log_management.html) for log locations.

 2. Playbook logs: `/opt/omnia/log/core/playbooks/`

 3. Container logs: `podman logs <container_name>`
 4. Slurm logs: `/var/log/slurm/`

 5. **Verify prerequisites.** Many failures stem from unmet prerequisites (missing packages, wrong OS version, misconfigured networks). Re-check the [Prerequisites Checklist](../GetStarted/prerequisites_checklist.html) for your deployment path.

 6. **Use the ochami CLI.** For provisioning issues, the `ochami-cli` provides direct access to the OpenCHAMI state manager for inspecting node inventory, boot status, and hardware state:

 
 
 ssh omnia_core
 ochami-cli smd components list
 ochami-cli bss bootscript list
 

 1. **Search this section.** Browse the topic-specific pages below or use your browser's search (Ctrl+F) to find your symptom.

Tip

If you cannot resolve an issue using this guide, open an issue on the [Omnia GitHub repository](https://github.com/dell/omnia/issues) with the relevant log output and a description of your environment.

Back to top [ Previous Best Practices Checklist ](../Operations/best_practices_checklist.html) [ Next General ](general.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
