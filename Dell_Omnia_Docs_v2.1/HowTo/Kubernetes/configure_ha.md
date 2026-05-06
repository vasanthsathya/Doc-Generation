
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Configure HA 

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
 * [ Prepare OIM ](../Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](setup_service_k8s.html)
 * Configure HA [ Configure HA ](configure_ha.html) Table of contents 
 * [ Overview ](#overview)
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
 3. [ Kubernetes ](setup_service_k8s.html)

# Configure Kubernetes HA[¶](#configure-kubernetes-ha "Permanent link")

Enable high availability (HA) for the Kubernetes control plane using a virtual IP (VIP) that floats between control-plane nodes for API server redundancy.

## Overview[¶](#overview "Permanent link")

By default, the Kubernetes API server is accessible on each control-plane node's individual IP address. For production deployments, a virtual IP (VIP) provides a single, stable endpoint for the API server. If the active control-plane node fails, the VIP automatically migrates to a healthy node.

Omnia uses **kube-vip** or **keepalived** to manage the virtual IP, depending on your configuration.

## Prerequisites[¶](#prerequisites "Permanent link")

 * A Kubernetes cluster deployed with 3 control-plane nodes (see [Setup Service K8S](setup_service_k8s.html)).
 * A free IP address on the admin network subnet for the VIP.
 * The VIP address must not be in the MetalLB address range or assigned to any other device.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure the virtual IP** in `omnia_config.yml`:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

Add or update the HA parameters:

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # Kubernetes HA configuration
 k8s_ha_enabled: true
 k8s_vip: "10.5.0.200"
 k8s_vip_interface: "eno1"
 

!!! warning
 
 
 The `k8s_vip` must be a free IP address on the same subnet as the
 control-plane nodes. Do **not** use an IP from the MetalLB range.
 

 1. **Run the omnia.yml playbook** (or re-run to apply HA changes):

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook omnia.yml --ask-vault-pass
 

If the cluster is already deployed, the playbook will:

 * Deploy kube-vip or keepalived on control-plane nodes.
 * Configure the VIP as the API server endpoint.
 * Update kubeconfig on all nodes to use the VIP.
 * Reconfigure the kube-apiserver with the new advertised address.

 * **Alternatively, configure HA manually** on an existing cluster:

a. **Install keepalived** on all control-plane nodes:
 
 
 ```bash title="Run on: each K8s control plane node"
 dnf install -y keepalived
 ```
 

b. **Configure keepalived** on the primary control-plane node:
 
 
 ```bash title="Run on: K8s control plane node 1 (MASTER)"
 cat <<'EOF' > /etc/keepalived/keepalived.conf
 vrrp_instance K8S_VIP {
 state MASTER
 interface eno1
 virtual_router_id 51
 priority 100
 advert_int 1
 authentication {
 auth_type PASS
 auth_pass k8s_vip_secret
 }
 virtual_ipaddress {
 10.5.0.200/24
 }
 }
 EOF
 
 systemctl enable --now keepalived
 ```
 

c. **Configure keepalived** on backup control-plane nodes:
 
 
 ```bash title="Run on: K8s control plane nodes 2 and 3 (BACKUP)"
 cat <<'EOF' > /etc/keepalived/keepalived.conf
 vrrp_instance K8S_VIP {
 state BACKUP
 interface eno1
 virtual_router_id 51
 priority 90
 advert_int 1
 authentication {
 auth_type PASS
 auth_pass k8s_vip_secret
 }
 virtual_ipaddress {
 10.5.0.200/24
 }
 }
 EOF
 
 systemctl enable --now keepalived
 ```
 
 
 !!! note
 
 Set `priority 80` on the third control-plane node.
 

## Verification[¶](#verification "Permanent link")

 1. **Verify the VIP is active** :

Run on: OIM host
 
 
 ping -c 3 10.5.0.200
 

 1. **Check which node currently holds the VIP** :

Run on: each K8s control plane node
 
 
 ip addr show eno1 | grep "10.5.0.200"
 

Only one node should show the VIP.

 1. **Access the Kubernetes API via the VIP** :

Run on: K8s control plane node
 
 
 kubectl --server=https://10.5.0.200:6443 get nodes
 

 1. **Test failover** by stopping keepalived on the active node:

Run on: active K8s control plane node
 
 
 systemctl stop keepalived
 

Then verify the VIP migrated:

Run on: OIM host
 
 
 ping -c 3 10.5.0.200
 # Should still respond -- VIP migrated to a backup node
 

Re-enable keepalived:

Run on: previously active node
 
 
 systemctl start keepalived
 

 1. **Update kubeconfig** to use the VIP:

Run on: K8s control plane node
 
 
 kubectl config set-cluster kubernetes --server=https://10.5.0.200:6443
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Deploy Powerscale Csi](deploy_powerscale_csi.html) \-- Deploy enterprise storage integration.
 * [Setup Telemetry](../Telemetry/setup_telemetry.html) \-- Deploy telemetry on the HA cluster.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**VIP is not reachable** Check keepalived status on all control-plane nodes:

Run on: each K8s control plane node
 
 
 systemctl status keepalived
 journalctl -u keepalived --no-pager -n 20
 

**VIP does not failover** Verify VRRP traffic is allowed on the network. Check for firewall rules blocking multicast:

Run on: K8s control plane node
 
 
 firewall-cmd --add-protocol=vrrp --permanent
 firewall-cmd --reload
 

**Both nodes claim the VIP (split-brain)** Ensure all control-plane nodes have the same `virtual_router_id` and `auth_pass` in keepalived.conf. Check network connectivity between control-plane nodes.

**kubectl fails with "connection refused" on VIP** Verify the API server is listening on the VIP address:

Run on: K8s control plane node
 
 
 ss -tlnp | grep 6443
 

Back to top [ Previous Set Up Kubernetes ](setup_service_k8s.html) [ Next Deploy PowerScale CSI ](deploy_powerscale_csi.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
