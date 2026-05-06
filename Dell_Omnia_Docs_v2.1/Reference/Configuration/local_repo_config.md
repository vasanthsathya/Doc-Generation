
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Local Repo Config 

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
 * [ Servers ](../SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](omnia_config.html)
 * Local Repo Config [ Local Repo Config ](local_repo_config.html) Table of contents 
 * [ Parameter reference ](#parameter-reference)
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

 * [ Parameter reference ](#parameter-reference)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Configuration ](omnia_config.html)

# local_repo_config.yml Reference[¶](#local_repo_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/local_repo_config.yml`

This file configures the local repository mirror on the OIM. The `local_repo.yml` playbook uses these settings to synchronize RHEL, third-party, and custom package repositories to the OIM via Pulp, enabling air-gapped or bandwidth-efficient deployments.

## Parameter reference[¶](#parameter-reference "Permanent link")

### General settings[¶](#general-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`repo_store_path` | String | No | `/opt/omnia/repo_store` | Directory on the OIM where mirrored repositories are stored. Must have sufficient disk space (see [Disk Space](../ClusterRequirements/disk_space.html)). 
`repo_sync_on_run` | Boolean | No | `true` | Synchronize repositories every time `local_repo.yml` is run. Set to `false` to skip sync and use previously cached content. 
 
### RHEL repository settings[¶](#rhel-repository-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`rhel_os_url` | String | Yes | (none) | URL of the RHEL BaseOS repository to mirror (e.g., `https://cdn.redhat.com/content/dist/rhel/server/10/10.0/x86_64/baseos/os` or a local HTTP mirror). 
`rhel_appstream_url` | String | Yes | (none) | URL of the RHEL AppStream repository. 
`rhel_crb_url` | String | No | (none) | URL of the CodeReady Builder repository. Required for build dependencies. 
`rhel_subscription_username` | String | Conditional | (none) | Red Hat subscription username. Required when mirroring from the Red Hat CDN (`cdn.redhat.com`). Not needed for local mirrors. 
`rhel_subscription_password` | String | Conditional | (vault-managed) | Red Hat subscription password. Set via `credentials_utility.yml`. 
 
### Third-party repository settings[¶](#third-party-repository-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`epel_url` | String | No | Auto-detected | URL for the Extra Packages for Enterprise Linux (EPEL) repository. 
`nvidia_gpu_repo_url` | String | No | (none) | URL for the NVIDIA CUDA repository. Required when deploying NVIDIA GPU drivers. 
`amd_gpu_repo_url` | String | No | (none) | URL for the AMD ROCm repository. Required when deploying AMD GPU drivers. 
`docker_repo_url` | String | No | (none) | URL for the Docker CE repository (used by K8s container runtime if applicable). 
`kubernetes_repo_url` | String | No | (none) | URL for the Kubernetes package repository. 
`beegfs_repo_url` | String | No | (none) | URL for the BeeGFS package repository. 
 
### Custom repositories[¶](#custom-repositories "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`custom_repos` | List | No | `[]` | List of additional repository definitions to mirror. 
`custom_repos[].name` | String | Yes | (none) | Repository identifier (e.g., `my-internal-repo`). 
`custom_repos[].url` | String | Yes | (none) | Repository base URL. 
`custom_repos[].gpgcheck` | Boolean | No | `true` | Whether to verify GPG signatures for packages in this repository. 
`custom_repos[].gpgkey` | String | No | (none) | URL or local path to the GPG public key for signature verification. 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/local_repo_config.yml
 
 
 repo_store_path: "/opt/omnia/repo_store"
 repo_sync_on_run: true
 
 rhel_os_url: "http://mirror.example.com/rhel/10.0/x86_64/baseos/"
 rhel_appstream_url: "http://mirror.example.com/rhel/10.0/x86_64/appstream/"
 rhel_crb_url: "http://mirror.example.com/rhel/10.0/x86_64/crb/"
 
 nvidia_gpu_repo_url: "https://developer.download.nvidia.com/compute/cuda/repos/rhel10/x86_64/"
 kubernetes_repo_url: "https://pkgs.k8s.io/core:/stable:/v1.29/rpm/"
 
 custom_repos:
 - name: "internal-tools"
 url: "http://repo.internal.example.com/tools/"
 gpgcheck: false
 

Info

 * [Playbook Reference](../Playbooks/playbook_reference.html) \-- The `local_repo.yml` playbook.
 * [Disk Space](../ClusterRequirements/disk_space.html) \-- Disk space for the repository mirror.
 * [Software Config](software_config.html) \-- Which packages are selected for installation.

Back to top [ Previous HA Config ](ha_config.html) [ Next BuildStreaM Config ](buildstream_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
