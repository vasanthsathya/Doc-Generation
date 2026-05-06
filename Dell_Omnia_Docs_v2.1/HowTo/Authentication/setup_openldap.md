
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Set Up OpenLDAP 

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
 * Set Up OpenLDAP [ Set Up OpenLDAP ](setup_openldap.html) Table of contents 
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

# Setup OpenLDAP[¶](#setup-openldap "Permanent link")

Configure OpenLDAP on the Omnia Auth container for centralized user authentication across Slurm and Kubernetes clusters.

## Overview[¶](#overview "Permanent link")

Omnia deploys OpenLDAP inside the `omnia_auth` Podman container on the OIM. Running `auth.yml` configures:

 * An OpenLDAP directory server with a base DN for your organization.
 * SSSD (System Security Services Daemon) clients on all cluster nodes.
 * PAM (Pluggable Authentication Modules) integration for SSH login.
 * Slurm user accounting tied to LDAP users.

This ensures consistent user credentials, UIDs, GIDs, and home directories across all nodes.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Prepare Oim](../Setup/prepare_oim.html) procedure is complete (`omnia_auth` container is running).
 * The `omnia_config.yml` file has authentication parameters configured.
 * Cluster nodes are provisioned and reachable.
 * NFS shared storage is configured for user home directories (see [Configure Nfs](../Storage/configure_nfs.html)).

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Configure authentication parameters** in `omnia_config.yml`:

Run on: omnia_core container
 
 
 vi /opt/omnia/input/project_default/omnia_config.yml
 

Add or update the LDAP parameters:

File: /opt/omnia/input/project_default/omnia_config.yml
 
 
 ---
 # Authentication configuration
 auth_type: "openldap"
 ldap_base_dn: "dc=omnia,dc=example,dc=com"
 ldap_admin_password: "" # Set via credentials utility
 ldap_organization: "Omnia HPC Cluster"
 

 1. **Run the auth.yml playbook** :

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook auth.yml --ask-vault-pass
 

The playbook performs:

 * Configures the OpenLDAP directory in the `omnia_auth` container.
 * Sets the admin (cn=admin) password.
 * Creates the organizational structure (OUs for users and groups).
 * Installs and configures SSSD on all cluster nodes.
 * Configures PAM for LDAP authentication.
 * Sets up automatic home directory creation on first login.

Execution time: **10-20 minutes**.

 1. **Add LDAP users** from the omnia_auth container:

Run on: OIM host
 
 
 podman exec -it omnia_auth bash
 

Run on: omnia_auth container
 
 
 # Create an LDIF file for a new user
 cat <<'EOF' > /tmp/add_user.ldif
 dn: uid=testuser,ou=People,dc=omnia,dc=example,dc=com
 objectClass: inetOrgPerson
 objectClass: posixAccount
 objectClass: shadowAccount
 uid: testuser
 cn: Test User
 sn: User
 uidNumber: 10001
 gidNumber: 10001
 homeDirectory: /home/testuser
 loginShell: /bin/bash
 userPassword: {SSHA}TemporaryPassword
 EOF
 
 ldapadd -x -D "cn=admin,dc=omnia,dc=example,dc=com" -W -f /tmp/add_user.ldif
 

 1. **Set the user's password** :

Run on: omnia_auth container
 
 
 ldappasswd -x -D "cn=admin,dc=omnia,dc=example,dc=com" -W \
 -S "uid=testuser,ou=People,dc=omnia,dc=example,dc=com"
 

## Verification[¶](#verification "Permanent link")

 1. **Verify OpenLDAP is running** in the omnia_auth container:

Run on: OIM host
 
 
 podman exec omnia_auth slapcat | head -20
 

 1. **Test LDAP search** from the omnia_core container:

Run on: omnia_core container
 
 
 ldapsearch -x -H ldap://omnia_auth -b "dc=omnia,dc=example,dc=com" "(uid=testuser)"
 

 1. **Verify SSSD is running** on cluster nodes:

Run on: omnia_core container
 
 
 ansible all -m shell -a "systemctl is-active sssd"
 

 1. **Test user resolution** on a compute node:

Run on: compute node
 
 
 id testuser
 getent passwd testuser
 

Expected output:

Expected output on: compute node
 
 
 uid=10001(testuser) gid=10001(testuser) groups=10001(testuser)
 

 1. **Test SSH login** as the LDAP user:

Run on: any node with network access
 
 
 ssh testuser@<compute-node-ip>
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Setup Openldap Proxy](setup_openldap_proxy.html) \-- Configure LDAP proxy to an external directory.
 * [Replicate Ldap](replicate_ldap.html) \-- Set up LDAP replication for redundancy.
 * [Setup Slurm](../Slurm/setup_slurm.html) \-- Slurm accounting will use LDAP users.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**SSSD cannot connect to LDAP** Verify network connectivity and the LDAP URI:

Run on: compute node
 
 
 ldapsearch -x -H ldap://<oim-ip> -b "dc=omnia,dc=example,dc=com"
 

**User not found (getent returns nothing)** \- Clear the SSSD cache:
 
 
 ```bash title="Run on: compute node"
 sss_cache -E
 systemctl restart sssd
 ```
 

 * Check SSSD logs:

Run on: compute node
 
 journalctl -u sssd --no-pager -n 30
 

**ldapadd returns "invalid credentials"** Ensure you are using the correct admin DN and password:

Run on: omnia_auth container
 
 
 ldapwhoami -x -D "cn=admin,dc=omnia,dc=example,dc=com" -W
 

**Home directory not created on first login** Verify the `pam_mkhomedir` module is configured:

Run on: compute node
 
 
 grep mkhomedir /etc/pam.d/system-auth
 

**Auth playbook fails with "omnia_auth container not found"** Ensure the container is running:

Run on: OIM host
 
 
 systemctl status omnia_auth.service
 podman ps --filter name=omnia_auth
 

Back to top [ Previous Configure RoCE ](../Networking/configure_roce.html) [ Next OpenLDAP Proxy ](setup_openldap_proxy.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
