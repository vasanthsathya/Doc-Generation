
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Ports 

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
 * [ Prepare OIM ](../../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](minimum_nodes.html)
 * Ports [ Ports ](ports.html) Table of contents 
 * [ OIM (Management Node) ports ](#oim-management-node-ports)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ OIM (Management Node) ports ](#oim-management-node-ports)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Cluster Requirements ](minimum_nodes.html)

# Required Ports[¶](#required-ports "Permanent link")

This page lists all TCP and UDP ports used by Omnia services across the OIM and cluster nodes. Open these ports in firewalld or your network firewall before deploying.

## OIM (Management Node) ports[¶](#oim-management-node-ports "Permanent link")

Port | Protocol | Service | Description 
---|---|---|--- 
67 | UDP | CoreDHCP (server) | DHCP server for node provisioning. OIM listens for DHCP requests. 
68 | UDP | CoreDHCP (client) | DHCP client responses. 
69 | UDP | TFTP | Trivial File Transfer Protocol for PXE boot file delivery. 
80 | TCP | HTTP | HTTP service for provisioning images, kickstart files, and repository metadata. 
443 | TCP | HTTPS | Secure HTTP for Pulp API, AWX web interface, and repository access. 
8443 | TCP | OpenCHAMI API | RESTful API for node lifecycle management and inventory queries. 
8444 | TCP | OpenCHAMI BSS | Boot Script Service API for iPXE boot script generation. 
5432 | TCP | PostgreSQL | Database backend for Pulp and OpenCHAMI (local connections only). 
6817 | TCP | Slurm (srun) | Slurm srun command communication (if Slurm client on OIM). 
 
## Podman container and service ports[¶](#podman-container-and-service-ports "Permanent link")

Port | Protocol | Container Name / Service | Description 
---|---|---|--- 
2222 | TCP | omnia_core | SSH access to the Omnia core container. 
2225 | TCP | pulp | Pulp repository container. 
5001 | TCP | Omnia nerdctl registry | Container image registry for Omnia services. 
636, 389 | TCP | omnia_auth | OpenLDAP authentication container (LDAPS and LDAP). 
 
## Slurm cluster ports[¶](#slurm-cluster-ports "Permanent link")

Port | Protocol | Service | Description 
---|---|---|--- 
6817 | TCP | slurmctld | Slurm controller daemon. Accepts job submissions and scheduling requests from slurmd and client commands. 
6818 | TCP | slurmd | Slurm compute daemon. Receives job launch instructions from slurmctld. 
6819 | TCP | slurmdbd | Slurm database daemon. Handles job accounting queries from slurmctld. 
3306 | TCP | MariaDB / MySQL | Database for slurmdbd job accounting. Local connections from slurmdbd only. 
22 | TCP | SSH | Remote access for administration and user login (login nodes). 
111 | TCP/UDP | rpcbind | RPC port mapper for NFS. Required when using NFS-shared Slurm configuration. 
2049 | TCP/UDP | NFS | NFS file sharing for shared /home, /scratch, and Slurm configuration (`nfs_share` installation type). 
88 | TCP/UDP | Kerberos KDC | Kerberos Key Distribution Center (if Kerberos is enabled). 
389 | TCP | LDAP | OpenLDAP directory service (unencrypted). 
636 | TCP | LDAPS | OpenLDAP with TLS encryption. 
 
## Kubernetes cluster ports[¶](#kubernetes-cluster-ports "Permanent link")

Port | Protocol | Service | Description 
---|---|---|--- 
6443 | TCP | K8s API server | Kubernetes API server. Used by kubectl, kubelet, and all K8s components. 
2379 | TCP | etcd (client) | etcd client communication. Used by the API server to read/write cluster state. 
2380 | TCP | etcd (peer) | etcd peer communication for cluster replication. 
10250 | TCP | kubelet | kubelet API. Used by the API server to communicate with node agents. 
10259 | TCP | kube-scheduler | Kubernetes scheduler HTTPS endpoint. 
10257 | TCP | kube-controller-manager | Controller manager HTTPS endpoint. 
30000--32767 | TCP | NodePort services | Default range for Kubernetes NodePort services. 
179 | TCP | Calico (BGP) | BGP peering for Calico pod network routing. 
4789 | UDP | Calico (VXLAN) | VXLAN overlay network for Calico (if VXLAN mode is used). 
5473 | TCP | Calico (Typha) | Calico Typha daemon for large-cluster performance. 
7472 | TCP/UDP | MetalLB | MetalLB memberlist for speaker-to-speaker communication. 
7946 | TCP/UDP | MetalLB | MetalLB node discovery. 
8285 | UDP | Flannel (UDP) | Flannel UDP backend for pod network overlay. 
8472 | UDP | Flannel (VXLAN) | Flannel VXLAN backend for pod network overlay. 
 
## Telemetry ports[¶](#telemetry-ports "Permanent link")

Port | Protocol | Service | Description 
---|---|---|--- 
8161 | TCP | ActiveMQ console | ActiveMQ web management console. 
61613 | TCP | ActiveMQ message broker | ActiveMQ STOMP message broker for telemetry data. 
3306, 33060 | TCP | MySQL | MySQL database for telemetry data storage. 
9092 | TCP | Apache Kafka | Kafka broker for telemetry data streaming. 
9093 | TCP | Apache Kafka (TLS) | Kafka broker TLS port. 
9094 | TCP | Kafka LoadBalancer | Kafka LoadBalancer service port. 
2181 | TCP | ZooKeeper | ZooKeeper coordination service for Kafka (if applicable). 
8428 | TCP | VictoriaMetrics | VictoriaMetrics HTTP API for metric ingestion and queries. 
8443 | TCP | VictoriaMetrics service | VictoriaMetrics HTTPS service port. 
8480 | TCP | VictoriaMetrics LB (insert) | VictoriaMetrics LoadBalancer insert service. 
8481 | TCP | VictoriaMetrics LB (query) | VictoriaMetrics LoadBalancer query service. 
3000 | TCP | Grafana | Grafana web interface for dashboards and visualization. 
9100 | TCP | Node Exporter | Prometheus-compatible node metrics exporter. 
6001--6100 | TCP | LDMS Aggregator | LDMS aggregator daemon for collecting node-level metrics. 
6001--6100 | TCP | LDMS Store Daemon | LDMS store daemon port. 
10001--10100 | TCP | LDMS Sampler | LDMS sampler daemon on compute nodes. 
 
## Authentication ports[¶](#authentication-ports "Permanent link")

Port | Protocol | Service | Description 
---|---|---|--- 
389 | TCP | LDAP | OpenLDAP directory queries (unencrypted). 
636 | TCP | LDAPS | OpenLDAP directory queries (TLS-encrypted). 
88 | TCP/UDP | Kerberos KDC | Kerberos authentication ticket requests. 
464 | TCP/UDP | Kerberos kpasswd | Kerberos password change service. 
749 | TCP | Kerberos kadmin | Kerberos administration daemon. 
80 / 443 | TCP | FreeIPA Web UI | FreeIPA web interface and API (if FreeIPA is deployed). 
 
## BuildStreaM / GitLab ports[¶](#buildstream-gitlab-ports "Permanent link")

Port | Protocol | Service | Description 
---|---|---|--- 
443 | TCP | GitLab HTTPS | GitLab web interface, API, and Git HTTPS operations. 
22 | TCP | GitLab SSH | Git SSH operations (push/pull). 
8093 | TCP | GitLab Runner | Runner communication with the GitLab server. 
 
## OpenCHAMI ports[¶](#openchami-ports "Permanent link")

Port | Protocol | Service | Description 
---|---|---|--- 
9000, 9001 | TCP | minio-server | MinIO S3-compatible object storage for OpenCHAMI. 
5000 | TCP | registry | Container image registry for OpenCHAMI services. 
9000 | TCP | step-ca | Internal certificate authority for TLS certificate issuance. 
5432 | TCP | postgres | PostgreSQL database for OpenCHAMI state management. 
27779 | TCP | smd | State Manager Daemon for node inventory and hardware discovery. 
27778 | TCP | bss | Boot Script Service for iPXE boot script generation. 
80, 443 | TCP | haproxy | HAProxy load balancer for OpenCHAMI services. 
22 | UDP | ssh-udp | SSH over UDP. 
67 | UDP | dhcp-udp | DHCP service for node provisioning. 
68 | UDP | bootpc | BOOTP client responses. 
69 | UDP | tftp-udp | TFTP for PXE boot file delivery. 
 
## Firewall rule summary[¶](#firewall-rule-summary "Permanent link")

Note

When `enable_firewall: true` is set in `security_config.yml`, Omnia automatically configures firewalld rules for all required ports on each node based on its assigned role. Manual firewall configuration is only necessary when using external firewalls (e.g., network-level ACLs on switches).

Info

 * [Security Config](../Configuration/security_config.html) \-- Firewall and security settings.
 * [Telemetry Config](../Configuration/telemetry_config.html) \-- Telemetry port configuration.
 * [Minimum Nodes](minimum_nodes.html) \-- Node counts per deployment scenario.

Back to top [ Previous Disk Space ](disk_space.html) [ Next Playbook Reference ](../Playbooks/playbook_reference.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
