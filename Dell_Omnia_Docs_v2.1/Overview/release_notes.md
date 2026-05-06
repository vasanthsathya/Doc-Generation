
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Release Notes 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../index.html)

[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../index.html)

Overview 
 * [ Architecture ](architecture.html)
 * Release Notes [ Release Notes ](release_notes.html) Table of contents 
 * [ Omnia 2.1.0.0 ](#omnia-2100)

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
 * [ General ](../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../Contributing/pull_requests.html)

Table of contents 

 * [ Omnia 2.1.0.0 ](#omnia-2100)

 1. [ Home ](../index.html)
 2. [ Overview ](index.html)

# Release Notes[¶](#release-notes "Permanent link")

This page summarizes the features, enhancements, and changes introduced in each Omnia release. For detailed upgrade instructions, see the migration guide in [Index](../GetStarted/index.html).

## Omnia 2.1.0.0[¶](#omnia-2100 "Permanent link")

_Release type: Feature release_

Omnia 2.1 builds on the containerized architecture introduced in 2.0, adding CI/CD-driven automation, expanded hardware support, and enhanced telemetry capabilities.

### BuildStreaM -- GitLab CI automation[¶](#buildstream-gitlab-ci-automation "Permanent link")

Omnia 2.1 introduces **BuildStreaM** , a GitLab CI-based automation pipeline that enables catalog-driven deployment. Administrators define the desired cluster state in a YAML catalog, and BuildStreaM translates it into an ordered pipeline of CI/CD jobs that execute Ansible playbooks.

 * Declarative catalog format for specifying roles, packages, and configurations.
 * Automatic pipeline generation from catalog definitions.
 * Full audit trail via GitLab commit history and merge-request reviews.
 * Idempotent re-execution---pipelines can be safely re-run.

See [Components](components.html) for a detailed explanation of BuildStreaM's architecture.

### Additional packages and software[¶](#additional-packages-and-software "Permanent link")

 * **Apptainer** (formerly Singularity) support for running HPC containers on Slurm compute nodes without requiring root privileges.
 * Expanded package deployment options for scientific libraries and AI/ML frameworks.
 * Support for deploying additional custom RPM packages via the local Pulp repository.

### Slurm cluster management[¶](#slurm-cluster-management "Permanent link")

 * **Add and remove Slurm nodes** dynamically without disrupting running jobs. Administrators update the mapping file and re-run the Slurm playbook to scale the cluster up or down.
 * Improved Slurm configuration management for heterogeneous node types.

### Telemetry enhancements[¶](#telemetry-enhancements "Permanent link")

 * **OpenManage Enterprise (OME) telemetry** \-- Ingest fleet-level health and compliance data from OME into the Kafka → VictoriaMetrics → Grafana pipeline.
 * **Smart Fabric Manager (SFM) telemetry** \-- Collect network fabric metrics (switch port utilization, link errors, fabric health) for unified infrastructure monitoring.
 * Enhanced Grafana dashboards for OME and SFM data.

### Storage integration[¶](#storage-integration "Permanent link")

 * **Dell PowerVault integration** \-- Configure and mount PowerVault storage arrays as shared storage for Slurm compute nodes and Kubernetes persistent volumes.

### Network enhancements[¶](#network-enhancements "Permanent link")

 * **InfiniBand support** \-- Automated configuration of InfiniBand adapters and subnet manager settings for high-speed MPI and RDMA workloads.

## Omnia 2.0.0.0[¶](#omnia-2000 "Permanent link")

_Release type: Major release_

Omnia 2.0 is a major architectural evolution that introduces Podman containerization, local repository management, centralized authentication, and a comprehensive telemetry pipeline.

### Podman containerization[¶](#podman-containerization "Permanent link")

Omnia 2.0 moves the entire control plane into Podman containers running on the OIM:

 * **omnia_core container** \-- All Ansible playbooks execute inside a Podman container, ensuring reproducible and isolated management operations.
 * **Service containers** \-- OpenCHAMI, Pulp, OpenLDAP, and telemetry services each run as dedicated Podman containers.
 * Rootless container execution for improved security.
 * No Docker daemon required; Podman is available in default RHEL / Rocky Linux repositories.

See [Architecture](architecture.html) for the full containerization architecture.

### Local repository management with Pulp[¶](#local-repository-management-with-pulp "Permanent link")

 * **Pulp** deployed as a Podman container on the OIM, mirroring RPM repositories, container images, and Python packages.
 * Full support for air-gapped deployments---all packages are served from local Pulp mirrors.
 * Repository snapshots ensure consistent package versions across all nodes.
 * Dramatically faster provisioning via local high-speed network access.

See [Components](components.html) for details on Pulp's capabilities.

### Centralized authentication[¶](#centralized-authentication "Permanent link")

 * **OpenLDAP** deployed as a Podman container for centralized user and group management.
 * **SSSD** configured on all managed nodes for LDAP-based authentication with local credential caching.
 * Consistent UIDs and GIDs across all cluster nodes.

See [Security Model](security_model.html) for the full authentication architecture.

### Telemetry pipeline[¶](#telemetry-pipeline "Permanent link")

 * **iDRAC telemetry** \-- Out-of-band hardware metrics (power, thermal, health) collected via Redfish and streamed through Kafka.
 * **LDMS telemetry** \-- In-band OS metrics (CPU, memory, network, I/O) collected via Lightweight Distributed Metric Service.
 * **Apache Kafka** as the central message broker for decoupled, buffered metric transport.
 * **VictoriaMetrics** for high-performance time-series storage with PromQL compatibility.
 * **Grafana** with pre-built HPC dashboards for cluster, node, GPU, and job monitoring.

See [Telemetry Architecture](telemetry_architecture.html) for the full pipeline architecture.

### Kubernetes high availability[¶](#kubernetes-high-availability "Permanent link")

 * Support for multiple `kube_control_plane` nodes behind a virtual IP for Kubernetes control-plane high availability.
 * Automatic failover if the primary control-plane node becomes unavailable.

### Composable functional groups[¶](#composable-functional-groups "Permanent link")

 * **Composable roles system** \-- Servers are assigned to functional groups via a CSV mapping file, decoupling physical hardware from logical roles.
 * A single server can hold multiple roles (e.g., Slurm control node + login node).
 * User-defined groups for physical characteristics (GPU type, CPU architecture, memory capacity).

See [Composable Roles](composable_roles.html) for the full explanation.

### Stateless boot[¶](#stateless-boot "Permanent link")

 * **Stateless (diskless) boot** support for RHEL-based nodes, where the OS runs entirely from a network-delivered image. This simplifies node replacement (swap hardware, PXE boot, ready) and reduces local disk requirements.

### GPU and accelerator support[¶](#gpu-and-accelerator-support "Permanent link")

 * **CUDA auto-install** \-- Automatic detection and installation of NVIDIA GPU drivers and CUDA toolkit on nodes with NVIDIA GPUs.
 * **ROCm support** \-- AMD ROCm platform support for nodes with AMD Instinct GPUs.
 * Slurm GRES (Generic RESource) configuration for GPU-aware job scheduling.

### Security enhancements[¶](#security-enhancements "Permanent link")

 * **AES-256 encryption** via Ansible Vault for all credentials at rest.
 * **step-ca** internal certificate authority for automated TLS certificate management.
 * **Hydra** OAuth 2.0 / OIDC provider for service-to-service authentication.
 * Credential utility for generating, rotating, and rekeying encrypted passwords.

See [Security Model](security_model.html) for details.

### Multi-architecture support[¶](#multi-architecture-support "Permanent link")

 * **x86_64** (Intel and AMD) -- Full support for Intel Xeon and AMD EPYC processors.
 * **aarch64** (ARM) -- Support for NVIDIA Grace CPU-based servers (e.g., PowerEdge configurations with Grace ARM processors).

### Input templates and validator[¶](#input-templates-and-validator "Permanent link")

 * **YAML input templates** \-- Pre-filled configuration templates that guide administrators through all required settings.
 * **Input validator** \-- A pre-flight check tool that validates all configuration files before playbook execution, catching errors (duplicate IPs, invalid service tags, missing fields) before any changes are made to the cluster.

## Supported platforms[¶](#supported-platforms "Permanent link")

Category | Details 
---|--- 
**Operating systems** | RHEL 8.8+, RHEL 9.2+, Rocky Linux 8.x, Rocky Linux 9.x 
**Architectures** | x86_64 (Intel, AMD), aarch64 (NVIDIA Grace ARM) 
**Dell PowerEdge servers** | R660, R760, R770, C6620, XE9680 (and other 15th/16th generation models) 
**License** | Apache License 2.0 (open source) 
 
Back to top [ Previous Security Model ](security_model.html) [ Next Blogs about Omnia ](blogs.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
