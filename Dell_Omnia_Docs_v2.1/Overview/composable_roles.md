
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Composable Roles 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../index.html)

[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../index.html)

Overview 
 * [ Architecture ](architecture.html)
 * Composable Roles [ Composable Roles ](composable_roles.html) Table of contents 
 * [ What are composable roles? ](#what-are-composable-roles)

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

 * [ What are composable roles? ](#what-are-composable-roles)

 1. [ Home ](../index.html)
 2. [ Overview ](index.html)

# Composable Roles[¶](#composable-roles "Permanent link")

Omnia uses a _composable roles_ system that lets administrators define what each server does by assigning it to one or more **functional groups**. Rather than hard-coding server purposes, Omnia reads a mapping file that declaratively associates physical servers with the roles they should perform. This page explains the concept, the mapping file format, and the design decisions behind this approach.

## What are composable roles?[¶](#what-are-composable-roles "Permanent link")

In a traditional cluster deployment, each server typically serves a single purpose: it is either a compute node, a login node, or a management node. This one-to-one mapping is simple but inflexible---it wastes resources on under-utilized servers and makes it difficult to adapt the cluster as workloads change.

Omnia's composable roles system decouples _physical servers_ from _logical functions_. A single Dell PowerEdge server can simultaneously act as:

 * A Slurm compute node **and** a Kubernetes worker node.
 * A Slurm control node **and** a login node (common in small clusters).
 * A Kubernetes control-plane node **and** an authentication server.

This composability allows administrators to right-size their clusters, making full use of available hardware without deploying dedicated machines for every function.

## Functional groups[¶](#functional-groups "Permanent link")

A **functional group** is a named role that defines a set of software and configuration to be applied to a server. Omnia defines the following built-in functional groups:

**Built-in functional groups**

Functional group | Description 
---|--- 
`slurm_control_node` | Runs the Slurm controller daemon (`slurmctld`). Manages job queues, scheduling, and resource accounting. Exactly one node per Slurm cluster should hold this role. 
`slurm_node` | Runs the Slurm compute daemon (`slurmd`). Executes batch jobs and parallel workloads. This is the most common role in an HPC cluster. 
`login_node` | Provides an interactive shell environment for users to submit jobs, compile code, and manage data. Login nodes do not run compute workloads. 
`login_compiler_node` | A login node that also includes development toolchains (compilers, debuggers, profilers) for users who need to build software on the cluster. 
`service_kube_control_plane` | Runs the Kubernetes control-plane components (API server, etcd, scheduler, controller-manager). For high availability, multiple nodes can hold this role. 
`service_kube_node` | Runs Kubernetes worker components (kubelet, kube-proxy). Hosts containerized application pods. 
`auth_server` | Runs centralized authentication services (OpenLDAP in a Podman container). Provides the LDAP directory that all cluster nodes authenticate against. 
 
Note

Functional groups are **additive**. Assigning a server to both `slurm_node` and `service_kube_node` causes Omnia to install and configure both Slurm and Kubernetes on that server. There is no conflict resolution---the administrator is responsible for ensuring that combined roles make sense for the workload.

## Groups based on physical characteristics[¶](#groups-based-on-physical-characteristics "Permanent link")

In addition to functional groups, Omnia supports grouping servers by their **physical characteristics** \---such as CPU architecture, GPU type, memory capacity, or network connectivity. These physical groups enable administrators to target Ansible playbooks at specific hardware profiles.

For example:

 * A group named `gpu_a100` might contain all servers with NVIDIA A100 GPUs.
 * A group named `arm_nodes` might contain all servers with NVIDIA Grace ARM CPUs.
 * A group named `high_memory` might contain servers with 1 TB+ RAM for large-memory workloads.

These groups are user-defined and can be combined freely with functional groups in the mapping file.

## The mapping file[¶](#the-mapping-file "Permanent link")

The mapping file is a CSV file that tells Omnia which servers exist, what roles they should play, and how they connect to the network. It is the single source of truth for cluster composition.

### Format[¶](#format "Permanent link")

Each row in the mapping file represents one server. The columns are:

**Mapping file columns**

Column | Required | Description 
---|---|--- 
`FUNCTIONAL_GROUP_NAME` | Yes | The functional group(s) this server belongs to (e.g., `slurm_node`, `service_kube_node`). 
`GROUP_NAME` | Yes | A user-defined group name for physical characteristics or organizational grouping (e.g., `gpu_a100`, `rack_01`). 
`SERVICE_TAG` | Yes | The Dell service tag uniquely identifying the server (found on the physical chassis or via iDRAC). 
`PARENT_SERVICE_TAG` | No | For blade servers or multi-node chassis, the service tag of the parent chassis. 
`HOSTNAME` | No | The desired hostname for the server. If omitted, Omnia generates one automatically. 
`ADMIN_MAC` | No | MAC address of the server's admin network NIC. Used for PXE boot identification. 
`ADMIN_IP` | No | Static IP address to assign on the admin network. 
`BMC_MAC` | No | MAC address of the server's BMC/iDRAC interface. 
`BMC_IP` | No | IP address of the server's BMC/iDRAC interface for out-of-band management. 
 
### Example[¶](#example "Permanent link")

Example: mapping.csv
 
 
 FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,PARENT_SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
 slurm_control_node,manager,ABC1234,,head01,aa:bb:cc:dd:ee:01,10.10.1.10,aa:bb:cc:dd:ff:01,10.20.1.10
 slurm_node,gpu_a100,DEF5678,,gpu01,aa:bb:cc:dd:ee:02,10.10.1.11,aa:bb:cc:dd:ff:02,10.20.1.11
 slurm_node,gpu_a100,GHI9012,,gpu02,aa:bb:cc:dd:ee:03,10.10.1.12,aa:bb:cc:dd:ff:03,10.20.1.12
 service_kube_control_plane,kube_mgmt,JKL3456,,k8s-cp01,aa:bb:cc:dd:ee:04,10.10.1.20,aa:bb:cc:dd:ff:04,10.20.1.20
 service_kube_node,kube_workers,MNO7890,,k8s-w01,aa:bb:cc:dd:ee:05,10.10.1.21,aa:bb:cc:dd:ff:05,10.20.1.21
 login_node,login,PQR1234,,login01,aa:bb:cc:dd:ee:06,10.10.1.30,aa:bb:cc:dd:ff:06,10.20.1.30
 auth_server,auth,STU5678,,auth01,aa:bb:cc:dd:ee:07,10.10.1.40,aa:bb:cc:dd:ff:07,10.20.1.40
 

In this example:

 * `ABC1234` is the Slurm controller.
 * `DEF5678` and `GHI9012` are GPU compute nodes grouped as `gpu_a100`.
 * `JKL3456` is the Kubernetes control-plane node.
 * `MNO7890` is a Kubernetes worker node.
 * `PQR1234` is a login node.
 * `STU5678` runs the authentication server.

## How Omnia processes the mapping file[¶](#how-omnia-processes-the-mapping-file "Permanent link")

When you run Omnia's provisioning or deployment playbooks, the following sequence occurs:

 1. **Parsing** \-- Omnia reads the mapping file and constructs an Ansible inventory dynamically. Each `FUNCTIONAL_GROUP_NAME` becomes an Ansible host group; each `GROUP_NAME` becomes a child group.

 2. **Validation** \-- The input validator checks for duplicate service tags, conflicting IP assignments, and missing required fields. Errors are reported before any changes are made to the cluster.

 3. **Role application** \-- Ansible playbooks are executed against the appropriate host groups. For example, the Slurm playbook targets the `slurm_control_node` and `slurm_node` groups, while the Kubernetes playbook targets `service_kube_control_plane` and `service_kube_node`.

 4. **Idempotent convergence** \-- Playbooks are idempotent; re-running them with the same mapping file produces no changes. Modifying the mapping file (e.g., adding a new `slurm_node` row) and re-running the playbook provisions only the new node.

Tip

Always run the Omnia input validator before applying changes. The validator catches common mistakes---such as assigning the same IP to two servers or using an invalid service tag---before any disruptive changes are made.

## Design rationale[¶](#design-rationale "Permanent link")

**Declarative over imperative** \-- The mapping file is a declarative specification of the cluster's desired state. Administrators say _what_ they want, not _how_ to get there. Omnia figures out the steps.

**Single source of truth** \-- All node-to-role assignments live in one file. There is no need to maintain separate inventory files for Slurm, Kubernetes, and provisioning---the mapping file drives all of them.

**Flexibility for heterogeneous hardware** \-- HPC clusters often contain a mix of server generations, CPU architectures, and accelerators. The combination of functional groups and physical groups allows administrators to target specific configurations to specific hardware without duplication.

**Multi-role servers** \-- In small or budget-constrained clusters, dedicating a server to each role is impractical. Composable roles let a three-server cluster run a Slurm controller, Kubernetes control plane, and login node on a single machine, with the remaining two servers handling compute workloads.

Info

 * [Architecture](architecture.html) \-- How the three cluster types map to functional groups.
 * [Network Topologies](network_topologies.html) \-- How Admin and BMC IP addresses in the mapping file relate to network segments.

Back to top [ Previous Network Topologies ](network_topologies.html) [ Next Telemetry Architecture ](telemetry_architecture.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
