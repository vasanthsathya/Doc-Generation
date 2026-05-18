

Deploy PowerScale CSI
=====================


Integrate Dell PowerScale (Isilon) with Kubernetes as a persistent storage
backend using the Dell CSI driver for PowerScale.


Overview
--------


The Dell CSI driver for PowerScale enables Kubernetes pods to use PowerScale
NFS shares as persistent volumes. This provides enterprise-grade, scalable
shared storage for containerized workloads running on the Omnia K8s service
cluster.

Key features:

- Dynamic provisioning of PersistentVolumes backed by PowerScale NFS exports.
- Support for ReadWriteMany (RWX) access mode for shared storage.
- Snapshots and volume cloning.
- Multi-cluster support.



Prerequisites
-------------


- A Kubernetes service cluster is deployed (see :doc:`Setup Service K8S <setup_service_k8s>`).
- A Dell PowerScale (Isilon) cluster is accessible from the K8s worker nodes.
- PowerScale OneFS 8.2+ or later.
- An API user on PowerScale with appropriate permissions (ISI_PRIV_NFS,
  ISI_PRIV_QUOTA).
- Helm 3.x is installed on a K8s control-plane node.
- Network connectivity between K8s worker nodes and PowerScale data LIFs.



Procedure
---------


#. **Install Helm** on a K8s control-plane node (if not already installed):


**Run on: K8s control plane node**

.. code-block:: bash
      curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
      helm version



#. **Create a namespace** for the CSI driver:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl create namespace csi-powerscale



#. **Create the PowerScale secret** with cluster connection details:


**Run on: K8s control plane node**

.. code-block:: bash
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

       Replace ``username``, ``password``, and ``endpoint`:doc:` with your actual
       PowerScale credentials and management IP. Delete the temporary file
       after applying.


**Run on: K8s control plane node**

.. code-block:: bash
      rm -f /tmp/powerscale-secret.yaml



#. **Add the Dell CSI Helm repository**:


**Run on: K8s control plane node**

.. code-block:: bash
      helm repo add dell https://dell.github.io/helm-charts
      helm repo update



#. **Install the PowerScale CSI driver**:


**Run on: K8s control plane node**

.. code-block:: bash
      helm install isilon dell/csi-isilon \
        --namespace csi-powerscale \
        --set controller.replicas=2 \
        --set isiAuthType=1 \
        --version 2.8.0



   Execution time: **2-5 minutes**.

#. **Create a StorageClass** for dynamic provisioning:


**Run on: K8s control plane node**

.. code-block:: bash
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





Verification
------------


#. **Verify CSI driver pods are running**:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl get pods -n csi-powerscale



   Expected: controller pods (2 replicas) and node pods (one per worker) in
   ``Running`` state.

#. **Verify the StorageClass was created**:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl get storageclass powerscale-nfs



#. **Test dynamic provisioning** by creating a PVC:


**Run on: K8s control plane node**

.. code-block:: bash
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



   The PVC should transition from ``Pending`` to ``Bound``.

#. **Clean up the test PVC**:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl delete pvc test-pvc





Next Steps
----------


- `Setup Telemetry <../Telemetry/setup_telemetry>` -- Deploy telemetry with
  PowerScale-backed persistent storage.
- :doc:`Configure Nfs <../Storage/configure_nfs>` -- Configure NFS for Slurm compute
  nodes to share the same PowerScale storage.



Troubleshooting
---------------


**CSI pods stuck in CrashLoopBackOff**
   Check the driver logs:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl logs -n csi-powerscale -l app=isilon-controller --tail=50



**PVC stuck in Pending**
   Check the CSI provisioner events:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl describe pvc test-pvc
      kubectl get events -n csi-powerscale



**Authentication failure to PowerScale**
   Verify the secret credentials:


**Run on: K8s control plane node**

.. code-block:: bash
      kubectl get secret isilon-creds -n csi-powerscale -o jsonpath='{.data.config}' | base64 -d



   Test API connectivity:


**Run on: K8s worker node**

.. code-block:: bash
      curl -sk https://10.5.1.100:8080/platform/latest/protocols/nfs/exports



**Mount failure on worker nodes**
   Ensure NFS client packages are installed:


**Run on: K8s worker node**

.. code-block:: bash
      dnf install -y nfs-utils
      showmount -e 10.5.1.100

