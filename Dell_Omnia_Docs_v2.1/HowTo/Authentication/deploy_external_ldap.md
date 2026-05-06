
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Deploy External LDAP 

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
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](setup_openldap.html)
 * Deploy External LDAP [ Deploy External LDAP ](deploy_external_ldap.html) Table of contents 
 * [ Overview ](#overview)
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
 3. [ Authentication ](setup_openldap.html)

# Deploy External LDAP[¶](#deploy-external-ldap "Permanent link")

Deploy a standalone, external OpenLDAP server using Bitnami containers for environments that require a dedicated authentication server separate from the OIM.

## Overview[¶](#overview "Permanent link")

While Omnia includes OpenLDAP in the `omnia_auth` container on the OIM, some deployments benefit from a dedicated LDAP server:

 * Separation of concerns (authentication independent of management node).
 * Dedicated resources for LDAP operations.
 * Existing infrastructure integration requirements.

This guide deploys OpenLDAP using Bitnami's container image on a dedicated server (or K8s cluster), then configures Omnia cluster nodes to authenticate against it.

## Prerequisites[¶](#prerequisites "Permanent link")

 * A dedicated server or the Omnia K8s service cluster is available.
 * Podman or Docker is installed on the dedicated server (or Helm for K8s).
 * Network connectivity between cluster nodes and the LDAP server.
 * A planned base DN, admin credentials, and organizational structure.

## Procedure[¶](#procedure "Permanent link")

### Standalone Server Deployment (Podman)[¶](#standalone-server-deployment-podman "Permanent link")

 1. **Log in to the LDAP server host** :

Run on: dedicated LDAP server
 
 
 ssh root@<ldap-server-ip>
 

 1. **Create persistent storage directories** :

Run on: dedicated LDAP server
 
 
 mkdir -p /opt/ldap/data
 mkdir -p /opt/ldap/config
 

 1. **Deploy the Bitnami OpenLDAP container** :

Run on: dedicated LDAP server
 
 
 podman run -d \
 --name openldap \
 --restart=always \
 -p 389:1389 \
 -p 636:1636 \
 -e LDAP_ADMIN_USERNAME=admin \
 -e LDAP_ADMIN_PASSWORD=YourAdminPassword \
 -e LDAP_ROOT=dc=omnia,dc=example,dc=com \
 -e LDAP_ADMIN_DN=cn=admin,dc=omnia,dc=example,dc=com \
 -e LDAP_CUSTOM_LDIF_DIR=/ldifs \
 -v /opt/ldap/data:/bitnami/openldap:Z \
 -v /opt/ldap/config:/ldifs:Z \
 docker.io/bitnami/openldap:latest
 

 1. **Create initial LDIF** for organizational structure:

Run on: dedicated LDAP server
 
 
 cat <<'EOF' > /opt/ldap/config/01-org.ldif
 dn: ou=People,dc=omnia,dc=example,dc=com
 objectClass: organizationalUnit
 ou: People
 
 dn: ou=Groups,dc=omnia,dc=example,dc=com
 objectClass: organizationalUnit
 ou: Groups
 EOF
 

 1. **Load the initial LDIF** :

Run on: dedicated LDAP server
 
 
 podman exec openldap ldapadd -x \
 -D "cn=admin,dc=omnia,dc=example,dc=com" \
 -w YourAdminPassword \
 -f /ldifs/01-org.ldif
 

 1. **Add users and groups** :

Run on: dedicated LDAP server
 
 
 cat <<'EOF' > /opt/ldap/config/02-users.ldif
 dn: cn=hpcusers,ou=Groups,dc=omnia,dc=example,dc=com
 objectClass: posixGroup
 cn: hpcusers
 gidNumber: 10000
 
 dn: uid=hpcuser1,ou=People,dc=omnia,dc=example,dc=com
 objectClass: inetOrgPerson
 objectClass: posixAccount
 objectClass: shadowAccount
 uid: hpcuser1
 cn: HPC User 1
 sn: User1
 uidNumber: 10001
 gidNumber: 10000
 homeDirectory: /home/hpcuser1
 loginShell: /bin/bash
 EOF
 
 podman exec openldap ldapadd -x \
 -D "cn=admin,dc=omnia,dc=example,dc=com" \
 -w YourAdminPassword \
 -f /ldifs/02-users.ldif
 

Set the user password:

Run on: dedicated LDAP server
 
 
 podman exec openldap ldappasswd -x \
 -D "cn=admin,dc=omnia,dc=example,dc=com" \
 -w YourAdminPassword \
 -S "uid=hpcuser1,ou=People,dc=omnia,dc=example,dc=com"
 

### Kubernetes Deployment (Helm)[¶](#kubernetes-deployment-helm "Permanent link")

 1. **(Alternative) Deploy on K8s** using Helm:

Run on: K8s control plane node
 
 
 helm repo add bitnami https://charts.bitnami.com/bitnami
 helm repo update
 
 helm install openldap bitnami/openldap \
 --namespace auth \
 --create-namespace \
 --set adminUsername=admin \
 --set adminPassword=YourAdminPassword \
 --set root=dc=omnia,dc=example,dc=com \
 --set service.type=LoadBalancer \
 --set persistence.enabled=true \
 --set persistence.size=10Gi
 

### Configure Omnia Nodes[¶](#configure-omnia-nodes "Permanent link")

 1. **Update omnia_config.yml** to point to the external LDAP:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 auth_type: "external_ldap"
 external_ldap_uri: "ldap://<ldap-server-ip>:389"
 external_ldap_base_dn: "dc=omnia,dc=example,dc=com"
 external_ldap_bind_dn: "cn=admin,dc=omnia,dc=example,dc=com"
 

 1. **Run the auth playbook** to configure SSSD on cluster nodes:

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook auth.yml --ask-vault-pass
 

## Verification[¶](#verification "Permanent link")

 1. **Verify the LDAP container is running** :

Run on: dedicated LDAP server
 
 
 podman ps --filter name=openldap
 

 1. **Test LDAP search** :

Run on: OIM host
 
 
 ldapsearch -x -H ldap://<ldap-server-ip> \
 -b "dc=omnia,dc=example,dc=com" "(uid=hpcuser1)"
 

 1. **Verify user resolution on cluster nodes** :

Run on: compute node
 
 
 getent passwd hpcuser1
 id hpcuser1
 

 1. **Test SSH login** :

Run on: any node
 
 
 ssh hpcuser1@<compute-node-ip>
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Replicate Ldap](replicate_ldap.html) \-- Replicate the external LDAP for redundancy.
 * [Setup Openldap Proxy](setup_openldap_proxy.html) \-- Proxy an existing directory through Omnia.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Container fails to start** Check container logs:

Run on: dedicated LDAP server
 
 
 podman logs openldap
 

**Port 389 already in use** Check for existing LDAP processes:

Run on: dedicated LDAP server
 
 
 ss -tlnp | grep 389
 # Kill or stop the conflicting process
 

**SSSD cannot connect to external LDAP** Verify connectivity from a cluster node:

Run on: compute node
 
 
 ldapsearch -x -H ldap://<ldap-server-ip> -b "dc=omnia,dc=example,dc=com" "(objectClass=*)" dn
 

**Users not visible after LDAP add** Clear SSSD cache on cluster nodes:

Run on: omnia_core container
 
 
 ansible all -m shell -a "sss_cache -E && systemctl restart sssd"
 

Back to top [ Previous OpenLDAP Proxy ](setup_openldap_proxy.html) [ Next Replicate LDAP ](replicate_ldap.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
