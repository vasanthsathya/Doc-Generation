
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

How-to Guides 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../index.html)

[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../index.html)

Overview 
 * [ Architecture ](../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](BuildStreaM/deploy_gitlab.html)

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

 * [ Initial Setup & Provisioning ](#initial-setup-provisioning)

 1. [ Home ](../index.html)
 2. [ How-to Guides ](index.html)

# How-to Guides[¶](#how-to-guides "Permanent link")

Task-oriented procedures for deploying, configuring, and managing Omnia clusters. Each guide follows a consistent structure: **Overview** , **Prerequisites** , **Procedure** , **Verification** , **Next Steps** , and **Troubleshooting**.

Tip

If you are new to Omnia, start with the [Index](../GetStarted/index.html) tutorials first. How-to guides assume you understand Omnia's architecture and have a working OIM.

## Initial Setup & Provisioning[¶](#initial-setup-provisioning "Permanent link")

Get Omnia installed on your OIM and provision bare-metal servers into a working cluster.

## Slurm Job Scheduling[¶](#slurm-job-scheduling "Permanent link")

Deploy and manage Slurm-based HPC clusters, including GPU-accelerated workloads and dynamic node management.

## Kubernetes Services[¶](#kubernetes-services "Permanent link")

Deploy and configure the Kubernetes service cluster used for platform services, monitoring, and storage.

## Storage[¶](#storage "Permanent link")

Configure shared storage for your cluster, including NFS and PowerVault block storage.

## Networking[¶](#networking "Permanent link")

Set up high-performance interconnects for your compute fabric, including InfiniBand and RoCE.

## Authentication[¶](#authentication "Permanent link")

Configure centralized user authentication across your cluster using LDAP.

## Telemetry & Monitoring[¶](#telemetry-monitoring "Permanent link")

Deploy and configure the telemetry pipeline for cluster-wide metrics collection, aggregation, and visualization.

## Containers & Packages[¶](#containers-packages "Permanent link")

Run containerized workloads and deploy additional software packages on provisioned nodes.

## BuildStreaM (CI/CD)[¶](#buildstream-cicd "Permanent link")

Automate cluster deployment using GitLab CI/CD pipelines and the BuildStreaM catalog-driven workflow.

Back to top [ Previous Path D: BuildStreaM ](../GetStarted/buildstream_deployment.html) [ Next Prepare OIM ](Setup/prepare_oim.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
