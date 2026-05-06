
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Create Local Repos 

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
 * [ Prepare OIM ](prepare_oim.html)
 * Create Local Repos [ Create Local Repos ](create_local_repos.html) Table of contents 
 * [ Overview ](#overview)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Overview ](#overview)

 1. [ Home ](../../index.html)
 2. [ How-to Guides ](../index.html)
 3. [ Setup ](prepare_oim.html)

# Create Local Repositories[¶](#create-local-repositories "Permanent link")

Synchronize RPM repositories to the OIM's local Pulp server so that provisioned nodes can install packages without direct internet access.

## Overview[¶](#overview "Permanent link")

The `local_repo.yml` playbook uses the Pulp repository management service on the OIM to:

 1. Mirror upstream RPM repositories (RHEL BaseOS, AppStream, EPEL, CUDA, etc.) based on the software stack defined in `software_config.json`.
 2. Create Pulp publications and distributions so nodes can access packages via the OIM's HTTP endpoint.
 3. Generate `*.repo` files that are automatically deployed to provisioned nodes during the imaging and discovery phases.

This ensures all cluster nodes install packages from a consistent, local mirror, reducing external network dependencies and improving reproducibility.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Prepare Oim](prepare_oim.html) procedure is complete (Pulp is running).
 * The [Configure Inputs](configure_inputs.html) procedure is complete (`software_config.json` is configured with the desired software stacks).
 * **For RHEL** : An active Red Hat subscription is registered on the OIM, **or** you have configured local repository paths in `software_config.json`.
 * **For Rocky Linux** : Internet access or pre-downloaded RPM repositories.
 * Sufficient disk space on the OIM for repository data (50-200 GB depending on selected software stacks).

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Verify software_config.json is configured** with the desired software stacks:

Run on: omnia_core container
 
 
 cat /opt/omnia/input/project_default/software_config.json | python3 -m json.tool
 

Confirm the `softwares` list includes all packages you need (e.g., `slurm`, `cuda`, `openldap`, `apptainer`).

 1. **Run the local_repo playbook** :

Run on: omnia_core container
 
 
 cd /omnia/local_repo
 ansible-playbook local_repo.yml
 

!!! note
 
 
 If credentials are Vault-encrypted:
 
 ```bash title="Run on: omnia_core container"
 ansible-playbook local_repo.yml --ask-vault-pass
 ```
 

The playbook will:

 * Query `software_config.json` to determine which repositories to sync.
 * Create Pulp remotes for each upstream repository.
 * Sync repository metadata and RPM packages to local storage.
 * Create Pulp publications and distributions.

!!! warning
 
 
 Initial synchronization can take **1-3 hours** depending on the number
 of repositories, internet bandwidth, and selected software stacks.
 CUDA and ROCm repositories are particularly large (10-30 GB each).
 

 1. **Monitor synchronization progress** (in a separate terminal):

Run on: OIM host
 
 
 podman logs -f pulp
 

## Verification[¶](#verification "Permanent link")

 1. **Check Pulp repository status** via the API:

Run on: OIM host
 
 
 curl -s http://localhost:8080/pulp/api/v3/distributions/rpm/rpm/ | python3 -m json.tool
 

Each synced repository should have a distribution with a `base_url`.

 1. **List available repositories** from a node's perspective:

Run on: OIM host
 
 
 curl -s http://localhost:8080/pulp/content/ | grep -oP 'href="[^"]*"'
 

 1. **Test package availability** by querying a specific repository:

Run on: OIM host
 
 
 curl -s http://localhost:8080/pulp/content/baseos/repodata/repomd.xml | head -5
 

Expected: XML content from the repository metadata.

 1. **Verify disk usage** to ensure sync completed:

Run on: OIM host
 
 
 df -h /var/lib/containers
 du -sh /var/lib/pulp/
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Build Cluster Images](build_cluster_images.html) \-- Build OS boot images using the local repos.
 * [Discover Nodes](discover_nodes.html) \-- Discover and PXE-boot target nodes.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Sync fails with "authentication required" (RHEL)** Ensure the OIM has an active RHEL subscription:

Run on: OIM host
 
 
 subscription-manager status
 subscription-manager repos --list-enabled
 

If the subscription is not active, register:

Run on: OIM host
 
 
 subscription-manager register --username <rhn-user> --password <rhn-pass>
 subscription-manager attach --auto
 

**Sync fails with network timeout** Check internet connectivity from the Pulp container:

Run on: OIM host
 
 
 podman exec pulp curl -I https://dl.fedoraproject.org
 

**Insufficient disk space** Pulp repositories can consume significant storage. Free up space or expand the partition:

Run on: OIM host
 
 
 du -sh /var/lib/pulp/*
 # Remove old repository versions if needed
 podman exec pulp pulpcore-manager repository-version-cleanup
 

**Playbook hangs during sync** Large repositories may take several hours. Check that the Pulp workers are active:

Run on: OIM host
 
 
 curl -s http://localhost:8080/pulp/api/v3/status/ | python3 -c "
 import sys, json
 data = json.load(sys.stdin)
 for w in data.get('online_workers', []):
 print(f'{w[\"name\"]}: {w[\"last_heartbeat\"]}')
 "
 

Back to top [ Previous Configure Credentials ](configure_credentials.html) [ Next Deploy Omnia Core ](deploy_omnia_core.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
