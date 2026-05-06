
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Replicate LDAP 

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
 * Replicate LDAP [ Replicate LDAP ](replicate_ldap.html) Table of contents 
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

# Replicate LDAP[¶](#replicate-ldap "Permanent link")

Set up LDAP replication between the primary `omnia_auth` OpenLDAP server and a secondary replica for redundancy and fault tolerance.

## Overview[¶](#overview "Permanent link")

LDAP replication ensures that:

 * User authentication continues if the primary LDAP server is unavailable.
 * Login latency is reduced for nodes closer to the replica.
 * Data consistency is maintained across all replicas.

Omnia supports **provider-consumer** (master-slave) replication using OpenLDAP's `syncrepl` mechanism. The primary server pushes changes to the replica, which maintains a read-only copy of the directory.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Setup Openldap](setup_openldap.html) procedure is complete (primary OpenLDAP is running in the `omnia_auth` container).
 * A secondary server (or container) is available to host the replica.
 * Network connectivity between the primary and replica LDAP servers.
 * The secondary server has OpenLDAP packages installed.

## Procedure[¶](#procedure "Permanent link")

 1. **Configure the primary server** (provider) for replication:

Run on: OIM host
 
 
 podman exec -it omnia_auth bash
 

Run on: omnia_auth container (primary)
 
 
 cat <<'EOF' > /tmp/enable_syncprov.ldif
 dn: cn=module{0},cn=config
 changetype: modify
 add: olcModuleLoad
 olcModuleLoad: syncprov
 
 dn: olcOverlay=syncprov,olcDatabase={1}mdb,cn=config
 changetype: add
 objectClass: olcOverlayConfig
 objectClass: olcSyncProvConfig
 olcOverlay: syncprov
 olcSyncProvCheckpoint: 50 10
 olcSyncProvSessionlog: 100
 EOF
 
 ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f /tmp/enable_syncprov.ldif
 

 1. **Create a replication service account** on the primary:

Run on: omnia_auth container (primary)
 
 
 cat <<'EOF' > /tmp/repl_user.ldif
 dn: cn=replicator,dc=omnia,dc=example,dc=com
 objectClass: simpleSecurityObject
 objectClass: organizationalRole
 cn: replicator
 userPassword: {SSHA}ReplicaPassword
 EOF
 
 ldapadd -x -D "cn=admin,dc=omnia,dc=example,dc=com" -W -f /tmp/repl_user.ldif
 

 1. **Configure the replica** (consumer) server:

Run on: replica LDAP server
 
 
 cat <<'EOF' > /tmp/syncrepl.ldif
 dn: olcDatabase={1}mdb,cn=config
 changetype: modify
 add: olcSyncRepl
 olcSyncRepl: rid=001
 provider=ldap://<primary-oim-ip>:389
 bindmethod=simple
 binddn="cn=replicator,dc=omnia,dc=example,dc=com"
 credentials=ReplicaPassword
 searchbase="dc=omnia,dc=example,dc=com"
 scope=sub
 schemachecking=on
 type=refreshAndPersist
 retry="30 5 300 3"
 interval=00:00:05:00
 EOF
 
 ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f /tmp/syncrepl.ldif
 

Replace `<primary-oim-ip>` with the actual IP of the OIM.

 1. **Configure SSSD on cluster nodes** to use both LDAP servers:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 ldap_uris:
 - "ldap://<primary-oim-ip>"
 - "ldap://<replica-ip>"
 

 1. **Re-run the auth playbook** to update SSSD configuration:

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook auth.yml --ask-vault-pass
 

## Verification[¶](#verification "Permanent link")

 1. **Verify replication status** on the replica:

Run on: replica LDAP server
 
 
 ldapsearch -x -H ldap://localhost -b "dc=omnia,dc=example,dc=com" "(uid=testuser)"
 

The user created on the primary should be visible on the replica.

 1. **Add a user on the primary** and verify it replicates:

Run on: omnia_auth container (primary)
 
 
 cat <<'EOF' > /tmp/new_user.ldif
 dn: uid=repltest,ou=People,dc=omnia,dc=example,dc=com
 objectClass: inetOrgPerson
 objectClass: posixAccount
 uid: repltest
 cn: Replication Test
 sn: Test
 uidNumber: 10099
 gidNumber: 10099
 homeDirectory: /home/repltest
 loginShell: /bin/bash
 EOF
 
 ldapadd -x -D "cn=admin,dc=omnia,dc=example,dc=com" -W -f /tmp/new_user.ldif
 

Then check the replica:

Run on: replica LDAP server
 
 
 ldapsearch -x -H ldap://localhost -b "dc=omnia,dc=example,dc=com" "(uid=repltest)"
 

 1. **Test failover** by stopping the primary and verifying authentication still works:

Run on: OIM host
 
 
 podman stop omnia_auth
 

Run on: compute node
 
 
 # SSSD should failover to the replica
 id testuser
 ssh testuser@localhost
 

Remember to restart the primary:

Run on: OIM host
 
 
 podman start omnia_auth
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Deploy External Ldap](deploy_external_ldap.html) \-- Deploy a fully external LDAP setup.
 * [Setup Slurm](../Slurm/setup_slurm.html) \-- Slurm users authenticate via the replicated LDAP.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Replica does not receive updates** Check the syncrepl connection from the replica logs:

Run on: replica LDAP server
 
 
 journalctl -u slapd --no-pager -n 30
 

**"Invalid credentials" during replication** Verify the replicator account password matches between the provider configuration and the consumer's syncrepl credentials.

**Data is stale on the replica** Force a full resync by removing and re-adding the syncrepl configuration:

Run on: replica LDAP server
 
 
 ldapmodify -Q -Y EXTERNAL -H ldapi:/// <<'EOF'
 dn: olcDatabase={1}mdb,cn=config
 changetype: modify
 delete: olcSyncRepl
 EOF
 

Then re-apply the syncrepl configuration from step 3.

**SSSD does not failover to the replica** Check the SSSD configuration on the compute node:

Run on: compute node
 
 
 cat /etc/sssd/sssd.conf | grep ldap_uri
 

Ensure both LDAP URIs are listed with the primary first.

Back to top [ Previous Deploy External LDAP ](deploy_external_ldap.html) [ Next Set Up Telemetry ](../Telemetry/setup_telemetry.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
