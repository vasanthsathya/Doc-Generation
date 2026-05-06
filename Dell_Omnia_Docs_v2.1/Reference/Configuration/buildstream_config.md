
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

BuildStreaM Config 

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
 * BuildStreaM Config [ BuildStreaM Config ](buildstream_config.html) Table of contents 
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

# build_stream_config.yml Reference[¶](#build_stream_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/build_stream_config.yml`

This file configures the BuildStreaM catalog-driven CI/CD deployment pipeline, including GitLab integration and pipeline behavior settings.

## Parameter reference[¶](#parameter-reference "Permanent link")

### GitLab settings[¶](#gitlab-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`gitlab_enabled` | Boolean | No | `false` | Enable GitLab deployment for BuildStreaM CI/CD pipelines. 
`gitlab_server` | String | Conditional | (none) | Hostname or IP of the GitLab server. Required when `gitlab_enabled` is `true`. 
`gitlab_port` | Integer | No | `443` | HTTPS port for the GitLab web interface and API. 
`gitlab_external_url` | String | Conditional | (none) | Public-facing URL of the GitLab instance (e.g., `https://gitlab.hpc.example.com`). Used in pipeline configuration and webhook URLs. 
`gitlab_admin_password` | String | Conditional | (vault-managed) | GitLab root/admin password. Set via `credentials_utility.yml`. 
`gitlab_runner_token` | String | Conditional | (vault-managed) | Registration token for GitLab Runners. Set via `credentials_utility.yml`. 
 
### Pipeline settings[¶](#pipeline-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`buildstream_catalog_path` | String | No | `/opt/omnia/buildstream/catalog` | Path to the BuildStreaM declarative catalog on the OIM. The catalog defines the desired cluster state. 
`buildstream_pipeline_branch` | String | No | `main` | Git branch in the BuildStreaM repository that triggers pipeline execution. 
`buildstream_auto_trigger` | Boolean | No | `true` | Automatically trigger pipelines when catalog changes are pushed. Set to `false` for manual pipeline execution only. 
`buildstream_retry_count` | Integer | No | `3` | Number of retry attempts for failed pipeline stages. 
`buildstream_timeout` | Integer | No | `3600` | Maximum pipeline execution time in seconds (default: 1 hour). 
 
### GitLab Runner settings[¶](#gitlab-runner-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`runner_executor` | String | No | `shell` | GitLab Runner executor type. Accepted values: `shell`, `docker`, `kubernetes`. 
`runner_concurrent` | Integer | No | `4` | Maximum number of concurrent pipeline jobs per runner. 
`runner_tags` | List | No | `["omnia", "buildstream"]` | Tags assigned to the runner for job matching. 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/build_stream_config.yml
 
 
 gitlab_enabled: true
 gitlab_server: "10.5.0.100"
 gitlab_port: 443
 gitlab_external_url: "https://gitlab.hpc.example.com"
 
 buildstream_catalog_path: "/opt/omnia/buildstream/catalog"
 buildstream_pipeline_branch: "main"
 buildstream_auto_trigger: true
 buildstream_retry_count: 3
 buildstream_timeout: 3600
 
 runner_executor: "shell"
 runner_concurrent: 4
 runner_tags:
 - omnia
 - buildstream
 

Info

 * [Playbook Reference](../Playbooks/playbook_reference.html) \-- BuildStreaM-related playbooks.
 * [Minimum Nodes](../ClusterRequirements/minimum_nodes.html) \-- Minimum nodes for BuildStreaM deployments (8+).

Back to top [ Previous Local Repo Config ](local_repo_config.html) [ Next PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
