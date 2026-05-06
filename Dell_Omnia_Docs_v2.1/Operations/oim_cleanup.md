
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

OIM Cleanup 

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
 * OIM Cleanup [ OIM Cleanup ](oim_cleanup.html) Table of contents 
 * [ When to use OIM cleanup ](#when-to-use-oim-cleanup)

Troubleshooting 
 * [ General ](../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ When to use OIM cleanup ](#when-to-use-oim-cleanup)

 1. [ Home ](../index.html)
 2. [ Operations ](index.html)

# OIM Cleanup[¶](#oim-cleanup "Permanent link")

The `oim_cleanup.yml` playbook tears down the Omnia Infrastructure Manager (OIM) configuration, removing containers, services, and state so you can start fresh. This is a **destructive operation** \--- use it only when you need to completely reset the OIM.

## When to use OIM cleanup[¶](#when-to-use-oim-cleanup "Permanent link")

 * **Fresh start** \-- You want to redeploy Omnia from scratch after a failed or experimental deployment.
 * **Version upgrade** \-- You are upgrading to a new major version of Omnia that requires a clean OIM.
 * **Environment reset** \-- Lab or test environments where the OIM is frequently rebuilt.

Danger

`oim_cleanup.yml` removes Podman containers, configuration files, and state data from the OIM. **This operation cannot be undone.** Ensure you have backed up any critical data (mapping files, custom configurations, credentials) before proceeding.

## Prerequisites[¶](#prerequisites "Permanent link")

 * You are logged in as `root` on the OIM host (not inside the `omnia_core` container).
 * All cluster workloads have been drained or stopped.
 * Critical data has been backed up:

 * `/omnia/input/` (mapping files, configuration files)

 * Custom Ansible inventories
 * Any modified playbook files
 * AES-256 encrypted credential vaults

## Procedure[¶](#procedure "Permanent link")

 1. **Log in to the OIM as root:**

 
 
 ssh root@<oim_ip>
 

!!! note
 
 
 Do **not** run this playbook from inside the `omnia_core` container.
 The cleanup process removes the container itself.
 

 1. **Navigate to the Omnia utils directory:**

 
 
 cd /omnia/utils/
 

 1. **Run the cleanup playbook:**

 
 
 ansible-playbook oim_cleanup.yml
 

The playbook performs the following actions:

 * Stops and removes all Omnia-managed Podman containers (`omnia_core`, OpenCHAMI, CoreDHCP, TFTP, Pulp, telemetry services).
 * Removes Podman pods and networks created by Omnia.
 * Deletes OIM service configuration files.
 * Cleans up SSH keys and known_hosts entries for provisioned nodes.
 * Removes cached OS images and repository data.

 * **Verify the cleanup:**

 
 
 # Confirm no Omnia containers remain
 podman ps -a | grep -i omnia
 
 # Confirm no Omnia pods remain
 podman pod ls
 

## Selective cleanup options[¶](#selective-cleanup-options "Permanent link")

If you do not need a full teardown, `oim_cleanup.yml` supports selective cleanup through extra variables:

Option | Description 
---|--- 
`cleanup_provisioning=true` | Remove only provisioning-related services (OpenCHAMI, CoreDHCP, TFTP) while keeping the `omnia_core` container and telemetry stack. 
`cleanup_telemetry=true` | Remove only telemetry services (Kafka, VictoriaMetrics, Grafana) while keeping provisioning and core services. 
`cleanup_repos=true` | Remove Pulp repository data and cached packages, freeing disk space without affecting running services. 
 
Example of selective cleanup:

Run on: OIM host
 
 
 cd /omnia/utils/
 ansible-playbook oim_cleanup.yml -e "cleanup_telemetry=true"
 

Tip

Selective cleanup is useful when troubleshooting a specific subsystem. For example, if telemetry is misconfigured, you can tear down only the telemetry stack and redeploy it without disturbing the rest of the OIM.

## Post-cleanup steps[¶](#post-cleanup-steps "Permanent link")

After a full cleanup, you will need to redeploy Omnia from the beginning:

 1. Re-run the OIM preparation playbook (see [Prepare Oim](../HowTo/Setup/prepare_oim.html)).
 2. Rebuild the `omnia_core` container (see [Deploy Omnia Core](../HowTo/Setup/deploy_omnia_core.html)).
 3. Reconfigure inputs and credentials (see [Configure Inputs](../HowTo/Setup/configure_inputs.html) and [Configure Credentials](../HowTo/Setup/configure_credentials.html)).
 4. Re-discover and provision nodes (see [Discover Nodes](../HowTo/Setup/discover_nodes.html)).

Info

 * [Reprovision Cluster](reprovision_cluster.html) \-- Re-image individual nodes without tearing down the entire OIM.
 * [General](../Troubleshooting/general.html) \-- Common issues that may arise after cleanup and redeployment.

Back to top [ Previous Reprovision Cluster ](reprovision_cluster.html) [ Next Log Management ](log_management.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
