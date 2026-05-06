
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Operating Systems 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../../index.html)

[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../../index.html)

Overview 
 * [ Architecture ](../../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](../../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](servers.html)
 * Operating Systems [ Operating Systems ](operating_systems.html) Table of contents 
 * [ OS support matrix ](#os-support-matrix)
 * Configuration Configuration 
 * [ Omnia Config ](../Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ OS support matrix ](#os-support-matrix)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Support Matrix ](servers.html)

# Supported Operating Systems[¶](#supported-operating-systems "Permanent link")

Omnia v2.1 requires RHEL 10.0 on both the OIM (management node) and cluster nodes. This page documents the supported OS versions and installation profiles.

## OS support matrix[¶](#os-support-matrix "Permanent link")

Operating System | Version | Node Role | Installation Profile 
---|---|---|--- 
Red Hat Enterprise Linux | 10.0 | OIM (Omnia Infrastructure Manager) | **Server with GUI** \-- full graphical desktop environment and development tools. Required for the OIM management stack. 
Red Hat Enterprise Linux | 10.0 | Slurm control node | **Minimal Install** \-- base system with no GUI. Omnia installs all required packages during provisioning. 
Red Hat Enterprise Linux | 10.0 | Slurm compute node | **Minimal Install** 
Red Hat Enterprise Linux | 10.0 | Login node | **Minimal Install** 
Red Hat Enterprise Linux | 10.0 | Kubernetes control plane | **Minimal Install** 
Red Hat Enterprise Linux | 10.0 | Kubernetes worker node | **Minimal Install** 
Red Hat Enterprise Linux | 10.0 | Auth server | **Minimal Install** 
 
## Architecture-specific requirements[¶](#architecture-specific-requirements "Permanent link")

Architecture | OS Image Build Playbook | Notes 
---|---|--- 
x86_64 (Intel, AMD) | `build_image_x86_64.yml` | Standard RHEL 10.0 x86_64 ISO. Both Intel and AMD servers use the same image. 
AArch64 (ARM Grace CPU) | `build_image_aarch64.yml` | RHEL 10.0 AArch64 ISO. ARM nodes **must** be provisioned with a separate image built specifically for AArch64. 
 
## OIM operating system details[¶](#oim-operating-system-details "Permanent link")

The OIM must be installed with the **Server with GUI** profile before running any Omnia playbooks. The following packages are expected to be present on the OIM:

Package / Group | Purpose 
---|--- 
`podman` | Container runtime for OIM services (OpenCHAMI, Pulp, omnia_core). 
`ansible-core` | Automation engine (installed inside the omnia_core container). 
`python3` | Python interpreter for Ansible modules and Omnia utilities. 
`git` | Cloning the Omnia repository. 
`NetworkManager` | Network configuration management. 
 
## RHEL subscription requirements[¶](#rhel-subscription-requirements "Permanent link")

A valid Red Hat subscription is required on the OIM to access RHEL repositories. Cluster nodes provisioned by Omnia receive packages from the local Pulp mirror and do not require individual subscriptions.

Repository | Required For 
---|--- 
`rhel-10-for-x86_64-baseos-rpms` | Base operating system packages for x86_64 nodes. 
`rhel-10-for-x86_64-appstream-rpms` | Application stream packages (Python, Podman, development tools). 
`rhel-10-for-aarch64-baseos-rpms` | Base operating system packages for ARM nodes. 
`rhel-10-for-aarch64-appstream-rpms` | Application stream packages for ARM nodes. 
`codeready-builder-for-rhel-10-x86_64-rpms` | Build dependencies and development libraries. 
 
Note

The `local_repo.yml` playbook mirrors all required repositories to the OIM so that cluster nodes can install packages without direct internet access. Configure repository URLs in [Local Repo Config](../Configuration/local_repo_config.html).

Info

 * [Servers](servers.html) \-- Supported server models.
 * [Provision Config](../Configuration/provision_config.html) \-- Provisioning configuration parameters.
 * [Local Repo Config](../Configuration/local_repo_config.html) \-- Local repository mirror configuration.

Back to top [ Previous Servers ](servers.html) [ Next Network Topologies ](network_topologies.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
