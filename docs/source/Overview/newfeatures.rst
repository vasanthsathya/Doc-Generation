New Features
=============

The following sections describe the new features and enhancements introduced in Omnia 2.1 releases.


BuildStream: Catalog-Driven Build Automation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Omnia BuildStreaM provides a comprehensive automation solution for managing infrastructure build workflows. It uses a catalog-driven approach where you define your build requirements in a structured catalog file, and BuildStreaM executes automated pipelines to create and deploy images according to your specifications.

BuildStreaM addresses the key challenges in HPC cluster image management:

* Automation: Eliminates manual build and deployment processes
* Integration: Works seamlessly with existing Omnia deployments
* Traceability: Provides complete audit trails for all build operations


Support for Installation of Additional Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enables the installation of additional packages on the cluster nodes, allowing to extend cluster functionality with custom software and tools.

Add and Remove Slurm Compute Nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provides the ability to add and remove Slurm compute nodes from the cluster, allowing for dynamic scaling of the cluster.

Support for Apptainer
^^^^^^^^^^^^^^^^^^^^^

Run apptainer pull to store the SIF container image on the cluster's NFS-mounted shared storage. This ensures uniform access across all compute nodes, enabling them to run jobs from the same SIF file.


Telemetry Collection from OME and SFM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enables collection of telemetry data from OpenManage Enterprise (OME) and Smart Fabric Manager (SFM), providing insights into cluster health, performance, and resource utilization.


PowerVault Storage Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PowerVault integration, with a preconfigured volume, provides persistent storage for critical Slurm controller components using iSCSI block storage with multipath support. This ensures data persistence for Slurm’s StateSaveLocation and the MariaDB/MySQL database.

InfiniBand Networking Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provides comprehensive support for InfiniBand (IB) networking in HPC clusters, including automatic DOCA-OFED driver installation for Mellanox InfiniBand cards, and static IP assignment for IB interfaces. InfiniBand Networking requires an InfiniBand subnet manager (SM) configured and running to manage the IB fabric.

Minimal OS Functional Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Introduces new Minimal OS functional groups (``os_x86_64`` and ``os_aarch64``) that provide a clean operating system baseline designed specifically for downstream platform software installation. These groups address the key need for a truly minimal OS environment without conflicts from pre-installed components.

The Minimal OS functional groups deliver:

* **Clean OS Baseline**: Only essential operating system packages and LDMS telemetry packages are included, with no schedulers, container runtimes, or orchestration software
* **Downstream Platform Support**: Ideal for deploying RKE2, custom Kubernetes, or other platform software that requires a clean environment
* **Telemetry Readiness**: LDMS packages are pre-installed for future observability, though services are not activated at handoff
* **Architecture Support**: Separate groups for x86_64 and AArch64 architectures ensure hardware-optimized deployments
* **Stateless Provisioning**: Maintains Omnia's diskless, stateless provisioning model with deterministic node states

Use Minimal OS functional groups when you need to deploy platform software without conflicts from Slurm, Kubernetes, or other pre-installed components, while maintaining cluster-wide telemetry capabilities.