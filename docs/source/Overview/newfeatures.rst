=========================
New Features
=========================

This release introduces significant enhancements to deployment flexibility, security, 
and high availability on the service clusters.

Containerization and Repository Management
------------------------------------------

- **Omnia containerization using Podman**  
   Core Omnia components are now containerized with Podman, improving portability 
   and lifecycle management.

- **Local repository creation with Pulp container**  
   A Pulp-based containerized repository service enables self-contained package 
   distribution without external dependencies.

- **Containerized LDAP Server**
   LDAP server is now containerized for simplified authentication and directory services.

- **Containerized iDRAC Telemetry Receiver**
   Supports air-gapped/offline telemetry collection for secure environments.

- **Containerized KafkaPump and VictoriaPump**
   KafkaPump and VictoriaPump services are now containerized for better scalability and easier deployment.


Service Cluster Enhancements
-----------------------------

- **Service cluster configuration**  
   Automated configuration workflows for establishing dedicated service clusters.

- **High availability for service Kubernetes cluster**  
   Built-in HA capabilities ensure resilience and failover protection for Kubernetes-based control planes.

- **iDRAC Telemetry integration on service Kubernetes cluster**  
   Telemetry data from iDRAC interfaces can now be collected and processed natively within the cluster.

- **LDMS Integration on Service Kubernetes Cluster**
   LDMS metrics can now be collected and processed natively within the cluster for distributed performance monitoring.


Telemetry and Metrics
----------------------
- **LDMS Support**
   Full integration of LDMS for distributed metric collection and performance monitoring.

- **Enabled support for two iDRAC telemetry collectors** 
   Kafka-based flow and VictoriaPump flow, with VictoriaPump storing telemetry metrics efficiently in VictoriaMetrics DB.


Functional Groups for Cluster Deployment
-----------------------------------------

- **Composable functional groups for nodes**  
   Nodes can be dynamically assigned roles based on modular functional profiles.

- **Support for image creation based on functional groups (Slurm and Kubernetes)**  
   Customized OS images can be generated automatically depending on workload type.

- **Multiple node types supported within functional groups. Includes support for:**  
    - Login Compiler Node  
    - Login Node  
    - Slurm Node
    - Slurm Control Node  
    - Service Kube Node
    - Service Kube Control Plane

Platform and Security Updates
-----------------------------

- **Support for x86_64 and aarch64 architectures**
   x86_64 and aarch64 platforms are now enabled.

- **Support for RHEL 10.0 (diskless OS) using OpenCHAMI**  
   Diskless provisioning is now available using OpenCHAMI workflows.

- **CUDA Installation on Slurm Cluster Nodes with Diskless Provisioning**
   GPU-enabled workloads supported with CUDA installation during diskless provisioning.

- **Input templates**  
   Predefined templates allow customized deployments tailored to specific infrastructure configurations.

- **Input validator**  
   Early validation of configuration inputs reduces deployment errors.

- **Encrypted storage of input credentials**  
   Sensitive credentials are now stored securely using encrypted formats.