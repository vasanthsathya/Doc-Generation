# Glossary

This glossary defines key terms used throughout the Omnia documentation. Terms are listed alphabetically. Where applicable, entries link to the documentation page that provides a full explanation.

**OIM**
**BMC**
 Baseboard Management Controller. A dedicated microcontroller embedded in server motherboards that provides out-of-band management capabilities (power control, hardware monitoring, remote console) independent of the host operating system. On Dell PowerEdge servers, the BMC is implemented as **iDRAC**.
**iDRAC**
**PXE**
 Preboot Execution Environment. An industry-standard protocol that allows servers to boot an operating system image over the network rather than from local disk. Omnia uses PXE for initial node discovery and OS provisioning.
**TFTP**
 Trivial File Transfer Protocol. A simple file transfer protocol used during PXE boot to deliver the initial bootloader binary (typically **iPXE**) to bare-metal nodes.
**iPXE**
 An open-source network bootloader that extends **PXE** with HTTP, iSCSI, and scripting capabilities. Omnia uses iPXE to chain to the **BSS** endpoint, which returns a customized boot script for each node.
**OpenCHAMI**
**SMD**
 State Manager Daemon. The inventory and state-tracking service within **OpenCHAMI**. SMD maintains a real-time record of every node's hardware configuration, power state, and component hierarchy.
**BSS**
 Boot Script Service. A component of **OpenCHAMI** that dynamically generates per-node boot scripts based on the node's hardware profile and assigned role. BSS is queried by **iPXE** during network boot.
**LDMS**
**Slurm**
**AWX**
 The open-source upstream project for Red Hat Ansible Automation Platform (formerly Ansible Tower). Provides a web-based UI and REST API for managing Ansible playbooks, inventories, and job scheduling. AWX is an optional component in Omnia.
**Podman**
**MetalLB**
 A bare-metal load balancer for Kubernetes. MetalLB assigns external IP addresses to Kubernetes `LoadBalancer` services in environments without a cloud provider. Omnia deploys MetalLB automatically in the Kubernetes cluster.
**Calico**
 A CNI (Container Network Interface) plugin for Kubernetes that provides pod-to-pod networking and network policy enforcement. Omnia deploys Calico as the default CNI in the Kubernetes cluster.
**NFS CSI**
 NFS Container Storage Interface driver. A Kubernetes CSI driver that provisions persistent volumes backed by NFS shares, enabling shared storage across pods and Slurm compute nodes.
**Apptainer**
 Formerly known as Singularity. A container runtime designed for HPC environments that allows users to run containers without root privileges. Supported on Slurm compute nodes in Omnia 2.1+.
**ROCm**
 Radeon Open Compute. AMD's open-source software platform for GPU-accelerated computing. Omnia supports ROCm installation on nodes with AMD Instinct GPUs for AI/ML and HPC workloads.
**BuildStreaM**
**Composable Roles**
**Functional Groups**
**Pulp**
**Kafka**
**VictoriaMetrics**
**Grafana**

Copyright © 2025 Dell Technologies. All rights reserved.