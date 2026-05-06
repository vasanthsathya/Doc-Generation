
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Configure Credentials 

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
 * [ Prepare OIM ](prepare_oim.html)
 * Configure Credentials [ Configure Credentials ](configure_credentials.html) Table of contents 
 * [ Overview ](#overview)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
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
 3. [ Setup ](prepare_oim.html)

# Configure Credentials[¶](#configure-credentials "Permanent link")

Create encrypted credentials for Omnia provisioning using the `credentials_utility` playbook. Credentials are stored in an Ansible Vault-encrypted file, ensuring sensitive data (passwords, tokens) is never stored in plain text.

## Overview[¶](#overview "Permanent link")

Omnia requires credentials for:

 * **Provisioning** \-- BMC/iDRAC access, OS root password, and SNMP community strings.
 * **Software stacks** \-- MariaDB passwords, LDAP admin credentials, Kubernetes secrets.

The `get_config_credentials.yml` playbook interactively prompts for these credentials and stores them in an encrypted `omnia_config_credentials.yml` file. This file is consumed by subsequent playbooks (`prepare_oim.yml`, `discovery.yml`, `omnia.yml`) automatically.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Deploy Omnia Core](deploy_omnia_core.html) procedure is complete.
 * The [Configure Inputs](configure_inputs.html) procedure is complete (input files populated).
 * You have the BMC/iDRAC administrator username and password for target servers.
 * You have decided on a root password for provisioned nodes.

## Procedure[¶](#procedure "Permanent link")

 1. **Enter the omnia_core container** :

Run on: OIM host
 
 
 ssh omnia_core
 

 1. **Navigate to the credential utility directory** :

Run on: omnia_core container
 
 
 cd /omnia/utils/credential_utility
 

 1. **Run the credential configuration playbook** with the `provision` tag:

Run on: omnia_core container
 
 
 ansible-playbook get_config_credentials.yml --tags provision
 

The playbook will prompt you for:

.. list-table:: :header-rows: 1 :widths: 35 65
 
 
 * - Prompt
 - Description
 * - `Vault password`
 - Master password to encrypt the credentials file. **Remember this
 password** -- you will need it for all subsequent playbook runs.
 * - `BMC username`
 - iDRAC administrator username (typically `root`)
 * - `BMC password`
 - iDRAC administrator password
 * - `Provision OS password`
 - Root password for provisioned nodes
 * - `SNMP community string`
 - SNMP community string for hardware monitoring (optional)
 

!!! warning
 
 
 The Vault password is the **only** way to decrypt the credentials file.
 If you lose it, you must re-run this playbook and re-enter all
 credentials.
 

 1. **Verify the encrypted file was created** :

Run on: omnia_core container
 
 
 ls -la /opt/omnia/input/project_default/omnia_config_credentials.yml
 

 1. **(Optional) View the encrypted credentials** to confirm values:

Run on: omnia_core container
 
 
 ansible-vault view /opt/omnia/input/project_default/omnia_config_credentials.yml
 

Enter the Vault password when prompted. The decrypted content will display temporarily in the terminal.

## Verification[¶](#verification "Permanent link")

 1. **Confirm the file is Ansible Vault encrypted** :

Run on: omnia_core container
 
 
 head -1 /opt/omnia/input/project_default/omnia_config_credentials.yml
 

Expected output:

Expected output on: omnia_core container
 
 
 $ANSIBLE_VAULT;1.1;AES256
 

 1. **Test decryption** with the Vault password:

Run on: omnia_core container
 
 
 ansible-vault view /opt/omnia/input/project_default/omnia_config_credentials.yml
 

If the password is correct, you will see the decrypted YAML content. If incorrect, Ansible will report a decryption error.

 1. **Verify credential completeness** by checking that all required keys are present in the decrypted output:

 2. `bmc_username`

 3. `bmc_password`
 4. `provision_os_password`

## Next Steps[¶](#next-steps "Permanent link")

 * [Prepare Oim](prepare_oim.html) \-- Prepare OIM services using the configured credentials.
 * [Discover Nodes](discover_nodes.html) \-- Run node discovery (requires BMC credentials).

## Troubleshooting[¶](#troubleshooting "Permanent link")

**"Vault password incorrect" when viewing credentials** Ensure you are entering the exact password used during creation. The password is case-sensitive.

**Need to update a single credential** Edit the encrypted file directly:

Run on: omnia_core container
 
 
 ansible-vault edit /opt/omnia/input/project_default/omnia_config_credentials.yml
 

This opens the decrypted file in your default editor. Save and exit to re-encrypt.

**Need to change the Vault password** Re-key the encrypted file:

Run on: omnia_core container
 
 
 ansible-vault rekey /opt/omnia/input/project_default/omnia_config_credentials.yml
 

**Playbook prompts are not appearing** Ensure you are running the playbook interactively (not piped or redirected). The `--tags provision` flag limits the prompts to provisioning-related credentials only.

**Credentials file already exists** Re-running the playbook will overwrite the existing file. Back up the current file if needed:

Run on: omnia_core container
 
 
 cp /opt/omnia/input/project_default/omnia_config_credentials.yml \
 /opt/omnia/input/project_default/omnia_config_credentials.yml.bak
 

Back to top [ Previous Configure Inputs ](configure_inputs.html) [ Next Create Local Repos ](create_local_repos.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
