=========================
New Features
=========================

The following are the new features and enhancements introduced in the Omnia 2.0.0.0 release:


Support for Podman Containers
-----------------------------
Supports deployment of the following key services as Podman containers, enabling simplified lifecycle management and easier updates:

- **Omnia Core**: Orchestrates HPC cluster management and operations.
- **Omnia Auth**: Provides secure authentication services based on LDAP.
- **OpenCHAMI**: Supports diskless provisioning workflows.
- **Pulp Repository Service**: Hosts local package repositories to enable deployments on air-gapped environments.

Repository Management
---------------------
Enables deployment of a Pulp-based local repository service as a Podman container, allowing you to manage local repositories and distribute packages seamlessly in air-gapped environments.

Authentication Service
----------------------
Supports deployment of the LDAP server as part of the Omnia Auth Podman container, simplifying authentication and directory services.

Telemetry Collection and Monitoring
-----------------------------------
- Enables automated configuration of dedicated Kubernetes Service Clusters that host essential monitoring components for telemetry collection and monitoring.
- Supports telemetry collection using both iDRAC Telemetry service and LDMS (Lightweight Distributed Metric Service) in HPC environments:

  - **iDRAC Telemetry service** collects out-of-band system metrics from Dell servers, including power, thermal, and hardware health information. The iDRAC Telemetry data can be collected and streamed as time-series data to Kafka or VictoriaMetrics, depending on deployment needs, with VictoriaPump storing telemetry metrics in VictoriaMetrics DB.
  - **LDMS Telemetry** collects in-band performance metrics from Slurm cluster nodes such as CPU, memory, network, and I/O statistics from compute nodes. The LDMS Telemetry data can be collected and streamed as time-series data to Kafka.

- Supports air-gapped or offline telemetry collection for secure environments.

High Availability
-----------------
Provides support for built-in high-availability (HA) failover protection for Service Kubernetes Cluster control plane nodes.

Provisioning and Deployment Based on Functional Groups
-------------------------------------------------------
Support for provisioning and image deployment on HPC clusters based on groups and functional groups defined in a mapping file:

- Nodes are automatically assigned roles (for example, Slurm Control Node, Service Kubernetes Node, Login Node) based on the functional group specified in the mapping file.
- Customized OS images are deployed on nodes according to their assigned roles, ensuring workload-specific configurations for Slurm and Kubernetes environments.
- Supports provisioning for multiple node types within functional groups, including:

  - Login Node
  - Login Compiler Node
  - Slurm Node
  - Slurm Control Node
  - Service Kubernetes Node
  - Service Kubernetes Control Plane

Diskless Boot
-------------
- Support for diskless provisioning for RHEL 10.0 using OpenCHAMI.
- Automatic CUDA installation during diskless provisioning of Slurm cluster nodes ensures nodes are ready for GPU-enabled workloads immediately after deployment.

Security Updates
----------------
Sensitive credentials are now stored securely using encrypted formats.

Platform Support
----------------
Support for x86_64 and aarch64 architectures.

Input Template and Validator
----------------------------
- **Input Template**: Provides predefined configuration file templates to provision nodes for specific deployment requirements.
- **Input Validator**: Performs early validation of configuration file inputs to avoid issues during deployment.
