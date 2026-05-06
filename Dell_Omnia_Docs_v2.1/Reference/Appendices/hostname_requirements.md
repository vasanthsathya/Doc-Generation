
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Hostname Requirements 

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
 * Hostname Requirements [ Hostname Requirements ](hostname_requirements.html) Table of contents 
 * [ Rules ](#rules)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Rules ](#rules)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Appendices ](hostname_requirements.html)

# Hostname Requirements[¶](#hostname-requirements "Permanent link")

This page documents the hostname constraints that Omnia enforces on all cluster nodes. Hostnames are assigned via the `HOSTNAME` column in the PXE mapping CSV and must comply with the rules below.

## Rules[¶](#rules "Permanent link")

# | Rule | Details | | | | 
---|---|---|---|---|---|--- 
1 | **Lowercase only** | Hostnames must consist entirely of lowercase characters. Uppercase letters are rejected by `input_validator.yml`. | | | | 
2 | **No domain suffix** | Do not include a domain name in the hostname field. Use `slurm-ctrl-01`, not `slurm-ctrl-01.hpc.example.com`. The domain suffix is appended automatically from `domain_name` in `provision_config.yml`. | | | | 
3 | **RFC 952 / RFC 1123 compliant** | Hostnames must: | Start with a letter (`a`\--`z`). | Contain only letters (`a`\--`z`), digits (`0`\--`9`), and hyphens (`-`). | Not start or end with a hyphen. | Be between 1 and 63 characters long. 
4 | **No underscores** | Underscores (`_`) are not permitted in hostnames per RFC 952. Use hyphens (`-`) instead: `slurm-node-01`, not `slurm_node_01`. | | | | 
5 | **No consecutive hyphens** | Avoid double hyphens (`--`) as some DNS implementations handle them inconsistently. | | | | 
6 | **Unique across the cluster** | Every hostname in the PXE mapping file must be unique. Duplicate hostnames cause provisioning failures. | | | | 
7 | **No reserved names** | Do not use `localhost`, `gateway`, `dns`, or any hostname that conflicts with system services. | | | | 
 
## Valid and invalid examples[¶](#valid-and-invalid-examples "Permanent link")

Hostname | Valid? | Reason 
---|---|--- 
`slurm-ctrl-01` | Yes | Lowercase, starts with letter, uses hyphens. 
`kube-cp-01` | Yes | Short and descriptive. 
`gpu-node-r760xa-03` | Yes | Includes model info for identification. 
`Slurm-Ctrl-01` | **No** | Contains uppercase letters. 
`slurm_node_01` | **No** | Contains underscores. 
`slurm-ctrl-01.hpc.example.com` | **No** | Includes domain suffix (appended automatically). 
`-slurm-01` | **No** | Starts with a hyphen. 
`01-slurm` | **No** | Starts with a digit. 
`a` | Yes | Minimum 1 character (though descriptive names are recommended). 
`a-very-long-hostname-that-exceeds-sixty-three-characters-in-total-length` | **No** | Exceeds 63-character maximum. 
 
## Recommended naming conventions[¶](#recommended-naming-conventions "Permanent link")

Role | Pattern | Example 
---|---|--- 
Slurm control | `slurm-ctrl-NN` | `slurm-ctrl-01` 
Slurm compute | `slurm-<type>-NN` | `slurm-gpu-01`, `slurm-cpu-01` 
Login node | `login-NN` | `login-01` 
K8s control plane | `kube-cp-NN` | `kube-cp-01`, `kube-cp-02` 
K8s worker | `kube-wk-NN` | `kube-wk-01` 
Auth server | `auth-NN` | `auth-01` 
 
Tip

Using a consistent naming scheme with zero-padded numbers (`01`, `02`) allows Slurm node ranges (`slurm-gpu-[01-04]`) and simplifies inventory management.

Info

 * [Pxe Mapping File](../SampleFiles/pxe_mapping_file.html) \-- PXE mapping CSV where hostnames are assigned.
 * [Provision Config](../Configuration/provision_config.html) \-- `domain_name` parameter that provides the DNS suffix.

Back to top [ Previous LDMS Metrics ](../Metrics/ldms_metrics.html) [ Next Timezone List ](timezones.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
