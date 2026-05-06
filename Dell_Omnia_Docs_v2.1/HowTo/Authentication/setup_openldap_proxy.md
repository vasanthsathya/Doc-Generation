
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

OpenLDAP Proxy 

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
 * OpenLDAP Proxy [ OpenLDAP Proxy ](setup_openldap_proxy.html) Table of contents 
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

# Setup OpenLDAP as Proxy[¶](#setup-openldap-as-proxy "Permanent link")

Configure OpenLDAP on the `omnia_auth` container as a proxy to an external LDAP server, allowing your cluster to authenticate against an existing corporate directory without migrating users.

## Overview[¶](#overview "Permanent link")

In many enterprise environments, a central LDAP directory (Active Directory, OpenLDAP, 389 Directory Server) already exists. Rather than duplicating users, Omnia can configure OpenLDAP in proxy mode to:

 * Forward authentication requests to the external LDAP server.
 * Cache user and group data locally for improved performance.
 * Provide a consistent LDAP interface to cluster nodes.
 * Maintain cluster operation even if the external LDAP is temporarily unreachable (via caching).

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Prepare Oim](../Setup/prepare_oim.html) procedure is complete (`omnia_auth` container is running).
 * You have the external LDAP server's connection details:

 * Server URI (e.g., `ldaps://ldap.corp.example.com:636`)

 * Base DN (e.g., `dc=corp,dc=example,dc=com`)
 * Bind DN and password for a read-only service account
 * CA certificate if using LDAPS

 * Network connectivity from the OIM to the external LDAP server.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure proxy LDAP parameters** in `omnia_config.yml`:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 auth_type: "openldap_proxy"
 external_ldap_uri: "ldaps://ldap.corp.example.com:636"
 external_ldap_base_dn: "dc=corp,dc=example,dc=com"
 external_ldap_bind_dn: "cn=omnia-readonly,ou=ServiceAccounts,dc=corp,dc=example,dc=com"
 external_ldap_bind_password: "" # Set via credentials utility
 external_ldap_user_search_base: "ou=People,dc=corp,dc=example,dc=com"
 external_ldap_group_search_base: "ou=Groups,dc=corp,dc=example,dc=com"
 external_ldap_tls_ca_cert: "/etc/ssl/certs/corp-ca.pem"
 

 1. **(If using LDAPS) Copy the CA certificate** to the omnia_auth container:

Run on: OIM host
 
 
 podman cp /path/to/corp-ca.pem omnia_auth:/etc/ssl/certs/corp-ca.pem
 

 1. **Run the auth.yml playbook** :

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook auth.yml --ask-vault-pass
 

The playbook will:

 * Configure OpenLDAP's `slapd-ldap` backend for proxy pass-through.
 * Set up SSSD on cluster nodes to use the local proxy.
 * Configure TLS certificates if using LDAPS.
 * Enable caching for offline resilience.

 * **(Alternative) Manual proxy configuration** inside the `omnia_auth` container:

Run on: OIM host
 
 
 podman exec -it omnia_auth bash
 

Run on: omnia_auth container
 
 
 cat <<'EOF' >> /etc/openldap/slapd.d/cn=config/olcDatabase={2}ldap.ldif
 dn: olcDatabase={2}ldap
 objectClass: olcDatabaseConfig
 objectClass: olcLDAPConfig
 olcDatabase: {2}ldap
 olcSuffix: dc=corp,dc=example,dc=com
 olcDbURI: ldaps://ldap.corp.example.com:636
 olcDbRebindAsUser: TRUE
 EOF
 

## Verification[¶](#verification "Permanent link")

 1. **Test proxy connectivity** to the external LDAP:

Run on: omnia_auth container
 
 
 ldapsearch -x -H ldaps://ldap.corp.example.com:636 \
 -D "cn=omnia-readonly,ou=ServiceAccounts,dc=corp,dc=example,dc=com" \
 -W -b "ou=People,dc=corp,dc=example,dc=com" "(uid=*)" dn | head -20
 

 1. **Test local proxy** from the omnia_core container:

Run on: omnia_core container
 
 
 ldapsearch -x -H ldap://omnia_auth -b "dc=corp,dc=example,dc=com" "(uid=someuser)"
 

 1. **Verify user resolution** on a compute node:

Run on: compute node
 
 
 getent passwd someuser
 id someuser
 

 1. **Test SSH login** with a corporate LDAP user:

Run on: any node
 
 
 ssh someuser@<compute-node-ip>
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Replicate Ldap](replicate_ldap.html) \-- Set up replication for the proxy.
 * [Setup Slurm](../Slurm/setup_slurm.html) \-- Slurm will authenticate users via the LDAP proxy.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**Proxy returns "connection refused"** Verify the external LDAP server is reachable:

Run on: OIM host
 
 
 openssl s_client -connect ldap.corp.example.com:636
 

**Certificate verification failed** Ensure the CA certificate is correct and accessible:

Run on: omnia_auth container
 
 
 openssl verify -CAfile /etc/ssl/certs/corp-ca.pem /etc/ssl/certs/corp-ca.pem
 

**Users not found via proxy** Check the search base DN matches the external LDAP tree structure:

Run on: omnia_auth container
 
 
 ldapsearch -x -H ldaps://ldap.corp.example.com:636 \
 -D "<bind-dn>" -W -b "<base-dn>" "(objectClass=*)" dn | head
 

**SSSD cache stale data** Clear and restart:

Run on: compute node
 
 
 sss_cache -E
 systemctl restart sssd
 

Back to top [ Previous Set Up OpenLDAP ](setup_openldap.html) [ Next Deploy External LDAP ](deploy_external_ldap.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
