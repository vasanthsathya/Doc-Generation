# Kubernetes Issues

Issues related to the Kubernetes service cluster, including control plane initialization, pod scheduling, networking, storage, and load balancing.

## Control plane not initializing

The Kubernetes control plane fails to initialize. `kubectl get nodes` returns a connection error, or the `omnia.yml` playbook fails during the Kubernetes deployment phase.

 * Required ports (6443, 2379-2380, 10250-10252) are blocked by a firewall.
 * The `kubelet` service failed to start.
 * Insufficient resources (CPU, memory) on the control plane node.
 * A previous Kubernetes installation was not fully cleaned up.

 1. Check `kubelet` status on the control plane node:

 ssh <kube_control_plane> systemctl status kubelet
 ssh <kube_control_plane> journalctl -u kubelet --no-pager -n 50

 1. Verify required ports are open:

 ssh <kube_control_plane> ss -tlnp | grep -E '6443|2379|10250'

 1. Check for leftover state from a previous installation:

 ssh <kube_control_plane> ls /etc/kubernetes/manifests/

If stale files exist, reset Kubernetes:

 ssh <kube_control_plane> kubeadm reset -f
 ssh <kube_control_plane> rm -rf /etc/kubernetes/ /var/lib/etcd/

 1. Re-run the Omnia Kubernetes deployment:

 ssh omnia_core
 cd /omnia
 ansible-playbook playbooks/omnia.yml --tags kubernetes

## Pod scheduling failures

Pods remain in `Pending` state indefinitely. `kubectl describe pod <pod_name>` shows scheduling errors:

 Warning FailedScheduling 0/3 nodes are available: 3 node(s) had taint
 {node-role.kubernetes.io/control-plane: }, that the pod didn't tolerate.

 * No worker nodes are available (only control plane nodes exist).
 * Worker nodes are in `NotReady` state.
 * Resource requests exceed available capacity on worker nodes.
 * Taints on nodes prevent pod scheduling.

 1. Check node status:

 kubectl get nodes

 1. If worker nodes are `NotReady`, check kubelet on those nodes:

 ssh <kube_worker> systemctl status kubelet
 ssh <kube_worker> journalctl -u kubelet --no-pager -n 50

 1. If only control plane nodes exist, either add worker nodes or allow scheduling on control planes (not recommended for production):

 # Add worker nodes via Omnia
 ssh omnia_core
 cd /omnia
 ansible-playbook playbooks/add_node.yml

 1. Check resource availability:

 kubectl describe nodes | grep -A 5 "Allocated resources"

 1. Remove problematic taints if appropriate:

 kubectl taint nodes <node_name> <taint_key>-

## MetalLB not assigning IP addresses

Services of type `LoadBalancer` remain in `<pending>` state and never receive an external IP:

 kubectl get svc
 # EXTERNAL-IP shows <pending>

 * MetalLB is not deployed or its pods are not running.
 * The MetalLB IP address pool is not configured or is exhausted.
 * The MetalLB speaker pods cannot reach the network.

 1. Verify MetalLB pods are running:

 kubectl get pods -n metallb-system

 1. Check MetalLB logs:

 kubectl logs -n metallb-system -l app=metallb,component=controller
 kubectl logs -n metallb-system -l app=metallb,component=speaker

 1. Verify the IP address pool configuration:

 kubectl get ipaddresspool -n metallb-system -o yaml

If no pool exists, create one:

 apiVersion: metallb.io/v1beta1
 kind: IPAddressPool
 metadata:
 name: default-pool
 namespace: metallb-system
 spec:
 addresses:
 - 10.5.1.100-10.5.1.200

 1. Verify the L2 advertisement is configured:

 kubectl get l2advertisement -n metallb-system

## NFS CSI mount failures

Pods that use NFS-backed persistent volumes fail to start. `kubectl describe pod` shows mount errors:

 Warning FailedMount Unable to attach or mount volumes: timed out waiting
 for the condition

 * The NFS server is unreachable from the Kubernetes worker nodes.
 * The NFS CSI driver pods are not running.
 * The NFS export path is incorrect in the PersistentVolume definition.
 * Firewall rules block NFS traffic (ports 2049, 111).

 1. Verify the NFS CSI driver is running:

 kubectl get pods -n kube-system | grep nfs

 1. Test NFS connectivity from a worker node:

 ssh <kube_worker> showmount -e <nfs_server_ip>

 1. Verify the PersistentVolume configuration:

 kubectl get pv -o yaml | grep -A 5 nfs

 1. Check NFS firewall rules on the NFS server:

 ssh <nfs_server> firewall-cmd --list-all | grep -E 'nfs|2049|111'

 1. If the NFS server is unreachable, verify it is on the admin network:

 ssh <kube_worker> ping <nfs_server_ip>

## Calico networking issues

Pods cannot communicate with each other across nodes. `kubectl exec` into a pod and pinging another pod's IP fails. Calico pods may show errors in their logs.

 * Calico pods are not running on all nodes.
 * The pod CIDR overlaps with an existing network range.
 * BGP peering is misconfigured (in BGP mode).
 * IP-in-IP or VXLAN encapsulation is blocked by network infrastructure.

 1. Check Calico pod status:

 kubectl get pods -n calico-system
 # or
 kubectl get pods -n kube-system | grep calico

 1. Check Calico node status:

 kubectl get nodes -o wide
 calicoctl node status # if calicoctl is installed

 1. Verify the pod CIDR does not overlap with existing networks:

 kubectl cluster-info dump | grep -m 1 cluster-cidr

 1. Check Calico logs for errors:

 kubectl logs -n calico-system -l k8s-app=calico-node --tail=50

 1. If encapsulation is blocked, switch Calico to VXLAN mode:

 kubectl patch felixconfiguration default \
 --type='merge' \
 -p '{"spec":{"vxlanEnabled":true,"ipipEnabled":false}}'

Copyright © 2025 Dell Technologies. All rights reserved.