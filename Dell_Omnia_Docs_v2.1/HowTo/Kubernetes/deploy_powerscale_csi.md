
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Deploy PowerScale CSI 

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
 * Deploy PowerScale CSI [ Deploy PowerScale CSI ](deploy_powerscale_csi.html) Table of contents 
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

# Deploy PowerScale CSI[¶](#deploy-powerscale-csi "Permanent link")

Integrate Dell PowerScale (Isilon) with Kubernetes as a persistent storage backend using the Dell CSI driver for PowerScale.

## Overview[¶](#overview "Permanent link")

The Dell CSI driver for PowerScale enables Kubernetes pods to use PowerScale NFS shares as persistent volumes. This provides enterprise-grade, scalable shared storage for containerized workloads running on the Omnia K8s service cluster.

Key features:

 * Dynamic provisioning of PersistentVolumes backed by PowerScale NFS exports.
 * Support for ReadWriteMany (RWX) access mode for shared storage.
 * Snapshots and volume cloning.
 * Multi-cluster support.

## Prerequisites[¶](#prerequisites "Permanent link")

 * A Kubernetes service cluster is deployed (see [Setup Service K8S](setup_service_k8s.html)).
 * A Dell PowerScale (Isilon) cluster is accessible from the K8s worker nodes.
 * PowerScale OneFS 8.2+ or later.
 * An API user on PowerScale with appropriate permissions (ISI_PRIV_NFS, ISI_PRIV_QUOTA).
 * Helm 3.x is installed on a K8s control-plane node.
 * Network connectivity between K8s worker nodes and PowerScale data LIFs.

## Procedure[¶](#procedure "Permanent link")

 1. **Install Helm** on a K8s control-plane node (if not already installed):

Run on: K8s control plane node
 
 
 curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
 helm version
 

 1. **Create a namespace** for the CSI driver:

Run on: K8s control plane node
 
 
 kubectl create namespace csi-powerscale
 

 1. **Create the PowerScale secret** with cluster connection details:

Run on: K8s control plane node
 
 
 cat <<'EOF' > /tmp/powerscale-secret.yaml
 apiVersion: v1
 kind: Secret
 metadata:
 name: isilon-creds
 namespace: csi-powerscale
 type: Opaque
 stringData:
 config: |
 isilonClusters:
 - clusterName: "cluster1"
 username: "csi_user"
 password: "YourPowerScalePassword"
 endpoint: "https://10.5.1.100"
 endpointPort: "8080"
 isDefault: true
 isiPath: "/ifs/csi"
 isiVolumePathPermissions: "0755"
 EOF
 
 kubectl apply -f /tmp/powerscale-secret.yaml
 

!!! warning
 
 
 Replace `username`, `password`, and `endpoint` with your actual
 PowerScale credentials and management IP. Delete the temporary file
 after applying.
 

Run on: K8s control plane node
 
 
 rm -f /tmp/powerscale-secret.yaml
 

 1. **Add the Dell CSI Helm repository** :

Run on: K8s control plane node
 
 
 helm repo add dell https://dell.github.io/helm-charts
 helm repo update
 

 1. **Install the PowerScale CSI driver** :

Run on: K8s control plane node
 
 
 helm install isilon dell/csi-isilon \
 --namespace csi-powerscale \
 --set controller.replicas=2 \
 --set isiAuthType=1 \
 --version 2.8.0
 

Execution time: **2-5 minutes**.

 1. **Create a StorageClass** for dynamic provisioning:

Run on: K8s control plane node
 
 
 cat <<'EOF' | kubectl apply -f -
 apiVersion: storage.k8s.io/v1
 kind: StorageClass
 metadata:
 name: powerscale-nfs
 provisioner: csi-isilon.dellemc.com
 reclaimPolicy: Delete
 allowVolumeExpansion: true
 parameters:
 AccessZone: "System"
 IsiPath: "/ifs/csi"
 IsiVolumePathPermissions: "0755"
 RootClientEnabled: "false"
 mountOptions:
 - nfsvers=3
 EOF
 

## Verification[¶](#verification "Permanent link")

 1. **Verify CSI driver pods are running** :

Run on: K8s control plane node
 
 
 kubectl get pods -n csi-powerscale
 

Expected: controller pods (2 replicas) and node pods (one per worker) in `Running` state.

 1. **Verify the StorageClass was created** :

Run on: K8s control plane node
 
 
 kubectl get storageclass powerscale-nfs
 

 1. **Test dynamic provisioning** by creating a PVC:

Run on: K8s control plane node
 
 
 cat <<'EOF' | kubectl apply -f -
 apiVersion: v1
 kind: PersistentVolumeClaim
 metadata:
 name: test-pvc
 spec:
 accessModes:
 - ReadWriteMany
 resources:
 requests:
 storage: 5Gi
 storageClassName: powerscale-nfs
 EOF
 
 kubectl get pvc test-pvc
 

The PVC should transition from `Pending` to `Bound`.

 1. **Clean up the test PVC** :

Run on: K8s control plane node
 
 
 kubectl delete pvc test-pvc
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Setup Telemetry](../Telemetry/setup_telemetry.html) \-- Deploy telemetry with PowerScale-backed persistent storage.
 * [Configure Nfs](../Storage/configure_nfs.html) \-- Configure NFS for Slurm compute nodes to share the same PowerScale storage.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**CSI pods stuck in CrashLoopBackOff** Check the driver logs:

Run on: K8s control plane node
 
 
 kubectl logs -n csi-powerscale -l app=isilon-controller --tail=50
 

**PVC stuck in Pending** Check the CSI provisioner events:

Run on: K8s control plane node
 
 
 kubectl describe pvc test-pvc
 kubectl get events -n csi-powerscale
 

**Authentication failure to PowerScale** Verify the secret credentials:

Run on: K8s control plane node
 
 
 kubectl get secret isilon-creds -n csi-powerscale -o jsonpath='{.data.config}' | base64 -d
 

Test API connectivity:

Run on: K8s worker node
 
 
 curl -sk https://10.5.1.100:8080/platform/latest/protocols/nfs/exports
 

**Mount failure on worker nodes** Ensure NFS client packages are installed:

Run on: K8s worker node
 
 
 dnf install -y nfs-utils
 showmount -e 10.5.1.100
 

Back to top [ Previous Configure HA ](configure_ha.html) [ Next Configure NFS ](../Storage/configure_nfs.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
