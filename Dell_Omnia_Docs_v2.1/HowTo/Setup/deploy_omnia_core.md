
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Deploy Omnia Core 

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
 * Deploy Omnia Core [ Deploy Omnia Core ](deploy_omnia_core.html) Table of contents 
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

# Deploy omnia_core[¶](#deploy-omnia_core "Permanent link")

Install the `omnia_core` Podman container on your Omnia Infrastructure Manager (OIM). The `omnia_core` container encapsulates the Ansible toolchain and all Omnia playbooks, providing a reproducible and isolated control plane for cluster management.

## Overview[¶](#overview "Permanent link")

The `omnia_core` deployment process consists of three stages:

 1. **Clone** the Omnia repository from Dell's artifact repository.
 2. **Build** the container images using the `build_images.sh` script.
 3. **Install** the `omnia_core` service using `omnia.sh --install`.

Once installed, `omnia_core` runs as a systemd-managed Podman container that starts automatically on boot.

## Prerequisites[¶](#prerequisites "Permanent link")

Requirement | Details 
---|--- 
**Operating system** | RHEL 8.8+ / 9.2+ or Rocky Linux 8.x / 9.x on the OIM 
**RAM** | Minimum 64 GB (128 GB recommended for clusters > 100 nodes) 
**Disk** | Minimum 256 GB free (SSD recommended) 
**Network interfaces** | At least 2 NICs: one for the admin network, one for the BMC/iDRAC network 
**Podman** | Podman 4.x or later installed (`dnf install -y podman`) 
**Internet access** | Required to clone the repository and pull base container images 
**Git** | Git 2.x or later (`dnf install -y git`) 
 
Note

Ensure that SELinux is set to `permissive` or `enforcing` with the appropriate container policies. Disabling SELinux is **not recommended** in production environments.

## Procedure[¶](#procedure "Permanent link")

 1. **Log in to the OIM** as `root` or a user with `sudo` privileges:

Run on: OIM host
 
 
 ssh root@<oim-ip-address>
 

 1. **Clone the Omnia repository** from Dell's artifact repository:

Run on: OIM host
 
 
 cd /opt
 git clone https://github.com/dell/omnia.git
 cd omnia
 

!!! note
 
 
 To use a specific release, check out the corresponding tag:
 
 ```bash title="Run on: OIM host"
 git checkout v2.1.0.0
 ```
 

 1. **Build the container images** using the provided build script:

Run on: OIM host
 
 
 bash build_images.sh core
 

This builds the `omnia_core` container image locally. The build process takes approximately 10-15 minutes depending on network speed and hardware.

 1. **Install the omnia_core service** :

Run on: OIM host
 
 
 bash omnia.sh --install
 

This script:

 * Creates the `omnia_core` Podman container.
 * Registers it as a systemd service (`omnia_core.service`).
 * Mounts the necessary volumes for configuration and playbook storage.
 * Starts the container automatically.

 * **Verify the service is running** :

Run on: OIM host
 
 
 systemctl status omnia_core.service
 

Expected output:

Expected output on: OIM host
 
 
 ● omnia_core.service - Omnia Core Container
 Loaded: loaded (/etc/systemd/system/omnia_core.service; enabled; vendor preset: disabled)
 Active: active (running) since ...
 

## Verification[¶](#verification "Permanent link")

 1. **Check the container is running** :

Run on: OIM host
 
 
 podman ps --filter name=omnia_core
 

You should see a running container named `omnia_core`.

 1. **Enter the omnia_core container** and verify Ansible is available:

Run on: OIM host
 
 
 podman exec -it -u root omnia_core bash
 

Run on: omnia_core container
 
 
 ansible --version
 

 1. **Verify playbooks are accessible** :

Run on: omnia_core container
 
 
 ls /omnia/*.yml
 

You should see the key playbooks: `omnia_startup.yml`, `input_validator.yml`, `credentials_utility.yml`, `prepare_oim.yml`, `local_repo.yml`, `discovery.yml`, and others.

 1. **Verify input directory exists** :

Run on: omnia_core container
 
 
 ls /opt/omnia/input/project_default/
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Create Mapping File](create_mapping_file.html) \-- Create the PXE mapping file for node discovery.
 * [Configure Inputs](configure_inputs.html) \-- Configure Omnia input files.
 * [Configure Credentials](configure_credentials.html) \-- Set up encrypted credentials.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Container fails to start** Check the Podman logs for detailed error output:

Run on: OIM host
 
 
 podman logs omnia_core
 

**systemd service not found** Re-run the installation script:

Run on: OIM host
 
 
 bash omnia.sh --install
 

**Build fails with network errors** Ensure the OIM has internet access and DNS is configured correctly:

Run on: OIM host
 
 
 ping -c 3 github.com
 cat /etc/resolv.conf
 

**Podman not installed** Install Podman from the default OS repositories:

Run on: OIM host
 
 
 dnf install -y podman
 systemctl enable --now podman.socket
 

**Insufficient disk space** Check available disk space. At least 256 GB is required:

Run on: OIM host
 
 
 df -h /opt
 

Back to top [ Previous Create Local Repos ](create_local_repos.html) [ Next Discover Nodes ](discover_nodes.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
