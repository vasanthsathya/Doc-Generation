# Configure Credentials

Create encrypted credentials for Omnia provisioning using the `credentials_utility` playbook. Credentials are stored in an Ansible Vault-encrypted file, ensuring sensitive data (passwords, tokens) is never stored in plain text.

## Overview

Omnia requires credentials for:

 * **Provisioning** \-- BMC/iDRAC access, OS root password, and SNMP community strings.
 * **Software stacks** \-- MariaDB passwords, LDAP admin credentials, Kubernetes secrets.

The `get_config_credentials.yml` playbook interactively prompts for these credentials and stores them in an encrypted `omnia_config_credentials.yml` file. This file is consumed by subsequent playbooks (`prepare_oim.yml`, `discovery.yml`, `omnia.yml`) automatically.

## Prerequisites

 * You have the BMC/iDRAC administrator username and password for target servers.
 * You have decided on a root password for provisioned nodes.

## Procedure

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

## Verification

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

## Next Steps

## Troubleshooting

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

Copyright © 2025 Dell Technologies. All rights reserved.