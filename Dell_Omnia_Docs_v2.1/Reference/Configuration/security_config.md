
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Security Config 

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
 * [ Omnia Config ](omnia_config.html)
 * Security Config [ Security Config ](security_config.html) Table of contents 
 * [ Authentication method ](#authentication-method)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../ClusterRequirements/minimum_nodes.html)
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

 * [ Authentication method ](#authentication-method)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Configuration ](omnia_config.html)

# security_config.yml Reference[¶](#security_configyml-reference "Permanent link")

File path: `/opt/omnia/input/project_default/security_config.yml`

This file configures centralized authentication and security services for the cluster, including LDAP, Kerberos, and FreeIPA integration.

## Authentication method[¶](#authentication-method "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`auth_type` | String | No | `ldap` | Authentication backend to deploy. Accepted values: `ldap` (OpenLDAP), `freeipa` (FreeIPA). Determines which subsequent parameters are required. 
 
## LDAP settings[¶](#ldap-settings "Permanent link")

These parameters apply when `auth_type` is `ldap`.

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`ldap_uri` | String | Conditional | (none) | URI of the LDAP server (e.g., `ldap://10.5.0.50` or `ldaps://ldap.hpc.example.com`). Required when `auth_type` is `ldap`. 
`ldap_base_dn` | String | Conditional | (none) | Base Distinguished Name for LDAP queries (e.g., `dc=hpc,dc=example,dc=com`). 
`ldap_bind_dn` | String | Conditional | (none) | Bind DN for LDAP authentication (e.g., `cn=admin,dc=hpc,dc=example,dc=com`). 
`ldap_bind_password` | String | Conditional | (vault-managed) | Password for the bind DN. Set via `credentials_utility.yml`. 
`ldap_user_search_base` | String | No | `ou=People,<ldap_base_dn>` | Subtree where user entries are stored. 
`ldap_group_search_base` | String | No | `ou=Group,<ldap_base_dn>` | Subtree where group entries are stored. 
`ldap_tls_enabled` | Boolean | No | `false` | Enable TLS encryption for LDAP connections (`ldaps://`). 
`ldap_tls_ca_cert` | String | No | (none) | Path to the CA certificate file for TLS verification. 
 
## Kerberos settings[¶](#kerberos-settings "Permanent link")

Kerberos can be enabled alongside LDAP or FreeIPA for ticket-based authentication.

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`enable_kerberos` | Boolean | No | `false` | Enable Kerberos authentication on cluster nodes. 
`kerberos_realm` | String | Conditional | (none) | Kerberos realm name (e.g., `HPC.EXAMPLE.COM`). Must be uppercase. Required when `enable_kerberos` is `true`. 
`kerberos_kdc` | String | Conditional | (none) | Hostname or IP of the Key Distribution Center. 
`kerberos_admin_server` | String | Conditional | (none) | Hostname or IP of the Kerberos admin server (kadmind). 
 
## FreeIPA settings[¶](#freeipa-settings "Permanent link")

These parameters apply when `auth_type` is `freeipa`.

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`freeipa_server` | String | Conditional | (none) | Hostname or IP of the FreeIPA server. Required when `auth_type` is `freeipa`. 
`freeipa_domain` | String | Conditional | (none) | FreeIPA domain name (e.g., `hpc.example.com`). 
`freeipa_realm` | String | Conditional | (none) | FreeIPA Kerberos realm (e.g., `HPC.EXAMPLE.COM`). Uppercase. 
`freeipa_admin_password` | String | Conditional | (vault-managed) | FreeIPA admin password. Set via `credentials_utility.yml`. 
 
## General security settings[¶](#general-security-settings "Permanent link")

Parameter | Type | Required | Default | Description 
---|---|---|---|--- 
`enable_firewall` | Boolean | No | `true` | Configure firewalld rules on cluster nodes for required services. 
`enable_selinux` | Boolean | No | `true` | Enforce SELinux on cluster nodes. Omnia configures necessary SELinux booleans and file contexts. 
`ssh_key_auth_only` | Boolean | No | `false` | Disable SSH password authentication and require key-based auth only. 
 
## Usage example[¶](#usage-example "Permanent link")

File: /opt/omnia/input/project_default/security_config.yml
 
 
 auth_type: "ldap"
 ldap_uri: "ldap://10.5.0.50"
 ldap_base_dn: "dc=hpc,dc=example,dc=com"
 ldap_bind_dn: "cn=admin,dc=hpc,dc=example,dc=com"
 ldap_tls_enabled: false
 
 enable_kerberos: false
 
 enable_firewall: true
 enable_selinux: true
 ssh_key_auth_only: false
 

Info

 * [Playbook Reference](../Playbooks/playbook_reference.html) \-- The `auth.yml` playbook that deploys authentication services.
 * [Ports](../ClusterRequirements/ports.html) \-- Ports required by LDAP, Kerberos, and FreeIPA.

Back to top [ Previous Storage Config ](storage_config.html) [ Next HA Config ](ha_config.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
