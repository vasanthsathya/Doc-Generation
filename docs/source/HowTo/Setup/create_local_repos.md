# Create Local Repositories

Synchronize RPM repositories to the OIM's local Pulp server so that provisioned nodes can install packages without direct internet access.

## Overview

The `local_repo.yml` playbook uses the Pulp repository management service on the OIM to:

 1. Mirror upstream RPM repositories (RHEL BaseOS, AppStream, EPEL, CUDA, etc.) based on the software stack defined in `software_config.json`.
 2. Create Pulp publications and distributions so nodes can access packages via the OIM's HTTP endpoint.
 3. Generate `*.repo` files that are automatically deployed to provisioned nodes during the imaging and discovery phases.

This ensures all cluster nodes install packages from a consistent, local mirror, reducing external network dependencies and improving reproducibility.

## Prerequisites

 * **For RHEL** : An active Red Hat subscription is registered on the OIM, **or** you have configured local repository paths in `software_config.json`.
 * **For Rocky Linux** : Internet access or pre-downloaded RPM repositories.
 * Sufficient disk space on the OIM for repository data (50-200 GB depending on selected software stacks).

## Procedure

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

## Verification

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

## Next Steps

## Troubleshooting

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

Copyright © 2025 Dell Technologies. All rights reserved.