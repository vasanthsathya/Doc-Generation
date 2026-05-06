
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Create Mapping File 

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
 * Create Mapping File [ Create Mapping File ](create_mapping_file.html) Table of contents 
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

# Create a Mapping File[¶](#create-a-mapping-file "Permanent link")

Create the `pxe_mapping_file.csv` that tells Omnia how to discover and provision each bare-metal server. This file maps service tags, MAC addresses, IP addresses, and functional group assignments for every target node.

## Overview[¶](#overview "Permanent link")

The PXE mapping file is a CSV file that Omnia's discovery playbook uses to:

 * Identify each server by its Dell service tag.
 * Assign admin and BMC network addresses.
 * Place nodes into functional groups (e.g., `slurm_control_node`, `slurm_node`, `kube_control_plane`, `kube_node`, `login_node`).
 * Map blade servers to their parent chassis (for PowerEdge MX and C-series).

The file must be created **before** running the discovery playbook.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Deploy Omnia Core](deploy_omnia_core.html) procedure is complete and `omnia_core` is running.
 * You have the service tag, admin MAC address, and BMC MAC address for every target server. These are available from:

 * iDRAC web UI (System > Overview)

 * Physical label on the server front panel
 * OpenManage Enterprise (OME) inventory

 * Admin and BMC IP ranges are planned and do not conflict with existing allocations.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

Or alternatively:

Run on: OIM host
 
 
 podman exec -it -u root omnia_core bash
 

 1. **Navigate to the input directory** :

Run on: omnia_core container
 
 
 cd /opt/omnia/input/project_default
 

 1. **Create the mapping file** using a text editor:

Run on: omnia_core container
 
 
 vi pxe_mapping_file.csv
 

 1. **Add the CSV header and node entries**. The file must contain the following columns in this exact order:

File: /opt/omnia/input/project_default/pxe_mapping_file.csv
 
 
 FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,PARENT_SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
 slurm_control_node,slurm_cluster,ABCDEF1,,,aa:bb:cc:dd:ee:01,10.5.0.101,aa:bb:cc:dd:ff:01,10.3.0.101
 slurm_node,slurm_cluster,ABCDEF2,,,aa:bb:cc:dd:ee:02,10.5.0.102,aa:bb:cc:dd:ff:02,10.3.0.102
 slurm_node,slurm_cluster,ABCDEF3,,,aa:bb:cc:dd:ee:03,10.5.0.103,aa:bb:cc:dd:ff:03,10.3.0.103
 login_node,slurm_cluster,ABCDEF4,,,aa:bb:cc:dd:ee:04,10.5.0.104,aa:bb:cc:dd:ff:04,10.3.0.104
 kube_control_plane,k8s_cluster,ABCDEF5,,,aa:bb:cc:dd:ee:05,10.5.0.105,aa:bb:cc:dd:ff:05,10.3.0.105
 kube_node,k8s_cluster,ABCDEF6,,,aa:bb:cc:dd:ee:06,10.5.0.106,aa:bb:cc:dd:ff:06,10.3.0.106
 

### Column Reference[¶](#column-reference "Permanent link")

Column | Required | Description 
---|---|--- 
`FUNCTIONAL_GROUP_NAME` | Yes | Node role. Valid values: `slurm_control_node`, `slurm_node`, `login_node`, `kube_control_plane`, `kube_node`, `auth_server` 
`GROUP_NAME` | Yes | Logical cluster grouping (e.g., `slurm_cluster`, `k8s_cluster`) 
`SERVICE_TAG` | Yes | Dell service tag of the server (7-character alphanumeric string) 
`PARENT_SERVICE_TAG` | Yes | Service tag of the parent chassis for blade servers. Leave empty for rack servers. 
`HOSTNAME` | Yes | Custom hostname. Leave empty to let Omnia auto-generate from the service tag. 
`ADMIN_MAC` | Yes | MAC address of the PXE-capable NIC on the admin network 
`ADMIN_IP` | Yes | Static IP address to assign on the admin network 
`BMC_MAC` | Yes | MAC address of the BMC/iDRAC network interface 
`BMC_IP` | Yes | Static IP address to assign on the BMC network 
 
Warning

 * Column headers are **case-sensitive**. Use uppercase exactly as shown.
 * All fields are **mandatory**. Use an empty value (two consecutive commas) for fields that should be auto-generated (`PARENT_SERVICE_TAG`, `HOSTNAME`).
 * `ADMIN_MAC` must be the MAC address of the NIC used for PXE boot.
 * `BMC_MAC` must be the MAC address of the BMC/iDRAC interface.
 * Do **not** add spaces after commas.

 1. **Save and exit** the editor (`:wq` in vi).

## Verification[¶](#verification "Permanent link")

 1. **Validate the CSV format** by checking the header row:

Run on: omnia_core container
 
 
 head -1 /opt/omnia/input/project_default/pxe_mapping_file.csv
 

Expected output:

Expected output on: omnia_core container
 
 
 FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,PARENT_SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
 

 1. **Count the entries** (excluding the header):

Run on: omnia_core container
 
 
 tail -n +2 /opt/omnia/input/project_default/pxe_mapping_file.csv | wc -l
 

The count should match the number of target servers you intend to provision.

 1. **Check for formatting issues** (trailing spaces, empty lines):

Run on: omnia_core container
 
 
 cat -A /opt/omnia/input/project_default/pxe_mapping_file.csv
 

Ensure there are no trailing spaces (`$` should immediately follow the last field value) and no blank lines.

## Next Steps[¶](#next-steps "Permanent link")

 * [Configure Inputs](configure_inputs.html) \-- Configure software and cluster input files.
 * [Configure Credentials](configure_credentials.html) \-- Set up encrypted provisioning credentials.
 * [Discover Nodes](discover_nodes.html) \-- Run the discovery playbook using this mapping file.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Discovery playbook fails with "invalid mapping file" error** \- Verify column headers are uppercase and match exactly. \- Ensure no trailing spaces or hidden characters (use `cat -A` to check). \- Confirm every row has exactly 9 comma-separated fields.

**MAC address not found during discovery** \- Verify the `ADMIN_MAC` matches the PXE NIC (not an onboard NIC that is disabled in BIOS). \- Check that the BMC MAC corresponds to the iDRAC dedicated NIC, not a shared LOM.

**IP address conflict** \- Ensure no duplicate IPs exist in the `ADMIN_IP` or `BMC_IP` columns. \- Verify the IP ranges do not overlap with the OIM's own addresses or any DHCP scope on the network.

**Blade server not discovered** \- Populate the `PARENT_SERVICE_TAG` column with the chassis service tag for all blade servers in PowerEdge MX or C-series chassis.

Back to top [ Previous Discover Nodes ](discover_nodes.html) [ Next PXE Boot Nodes ](pxe_boot_nodes.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
