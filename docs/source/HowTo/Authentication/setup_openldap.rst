

Setup OpenLDAP
==============


Configure OpenLDAP on the Omnia Auth container for centralized user
authentication across Slurm and Kubernetes clusters.


Overview
--------


Omnia deploys OpenLDAP inside the ``omnia_auth`` Podman container on the OIM.
Running ``auth.yml`` configures:

- An OpenLDAP directory server with a base DN for your organization.
- SSSD (System Security Services Daemon) clients on all cluster nodes.
- PAM (Pluggable Authentication Modules) integration for SSH login.
- Slurm user accounting tied to LDAP users.


This ensures consistent user credentials, UIDs, GIDs, and home directories
across all nodes.



Prerequisites
-------------


- The :doc:`Prepare Oim <../Setup/prepare_oim>` procedure is complete (``omnia_auth``
  container is running).
- The ``omnia_config.yml`` file has authentication parameters configured.
- Cluster nodes are provisioned and reachable.
- NFS shared storage is configured for user home directories (see
  :doc:`Configure Nfs <../Storage/configure_nfs>`).



Procedure
---------


1. Enter the omnia_core container:

.. code-block:: bash
   :caption: Run on: OIM host

   ssh omnia_core



2. Configure authentication parameters in ``omnia_config.yml``:

.. code-block:: bash
   :caption: Run on: omnia_core container

   vi /opt/omnia/input/project_default/omnia_config.yml



Add or update the LDAP parameters:

.. code-block:: yaml
   :caption: File: /opt/omnia/input/project_default/omnia_config.yml

   ---
   # Authentication configuration
   auth_type: "openldap"
   ldap_base_dn: "dc=omnia,dc=example,dc=com"
   ldap_admin_password: ""  # Set via credentials utility
   ldap_organization: "Omnia HPC Cluster"



3. Run the auth.yml playbook:

.. code-block:: bash
   :caption: Run on: omnia_core container

   cd /omnia
   ansible-playbook auth.yml --ask-vault-pass



The playbook performs:

- Configures the OpenLDAP directory in the ``omnia_auth`` container.
- Sets the admin (cn=admin) password.
- Creates the organizational structure (OUs for users and groups).
- Installs and configures SSSD on all cluster nodes.
- Configures PAM for LDAP authentication.
- Sets up automatic home directory creation on first login.

Execution time: **10-20 minutes**.

4. Add LDAP users from the omnia_auth container:

.. code-block:: bash
   :caption: Run on: OIM host

   podman exec -it omnia_auth bash

.. code-block:: bash
   :caption: Run on: omnia_auth container

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



5. Set the user's password:

.. code-block:: bash
   :caption: Run on: omnia_auth container

   ldappasswd -x -D "cn=admin,dc=omnia,dc=example,dc=com" -W \
     -S "uid=testuser,ou=People,dc=omnia,dc=example,dc=com"





Verification
------------


1. Verify OpenLDAP is running in the omnia_auth container:

.. code-block:: bash
   :caption: Run on: OIM host

   podman exec omnia_auth slapcat | head -20



2. Test LDAP search from the omnia_core container:

.. code-block:: bash
   :caption: Run on: omnia_core container

   ldapsearch -x -H ldap://omnia_auth -b "dc=omnia,dc=example,dc=com" "(uid=testuser)"



3. Verify SSSD is running on cluster nodes:

.. code-block:: bash
   :caption: Run on: omnia_core container

   ansible all -m shell -a "systemctl is-active sssd"



4. Test user resolution on a compute node:

.. code-block:: bash
   :caption: Run on: compute node

   id testuser
   getent passwd testuser

Expected output:

.. code-block:: text
   :caption: Expected output on: compute node

   uid=10001(testuser) gid=10001(testuser) groups=10001(testuser)



5. Test SSH login as the LDAP user:

.. code-block:: bash
   :caption: Run on: any node with network access

   ssh testuser@<compute-node-ip>





Next Steps
----------


- :doc:`Setup Openldap Proxy <setup_openldap_proxy>` -- Configure LDAP proxy to an external
  directory.
- :doc:`Replicate Ldap <replicate_ldap>` -- Set up LDAP replication for redundancy.
- :doc:`Setup Slurm <../Slurm/setup_slurm>` -- Slurm accounting will use LDAP users.






Troubleshooting
---------------


**SSSD cannot connect to LDAP**
Verify network connectivity and the LDAP URI:

.. code-block:: bash
   :caption: Run on: compute node

   ldapsearch -x -H ldap://<oim-ip> -b "dc=omnia,dc=example,dc=com"



**User not found (getent returns nothing)**
- Clear the SSSD cache:

.. code-block:: bash
   :caption: Run on: compute node

   sss_cache -E
   systemctl restart sssd

- Check SSSD logs:

.. code-block:: bash
   :caption: Run on: compute node

   journalctl -u sssd --no-pager -n 30



**ldapadd returns "invalid credentials"**
Ensure you are using the correct admin DN and password:

.. code-block:: bash
   :caption: Run on: omnia_auth container

   ldapwhoami -x -D "cn=admin,dc=omnia,dc=example,dc=com" -W



**Home directory not created on first login**
Verify the ``pam_mkhomedir`` module is configured:

.. code-block:: bash
   :caption: Run on: compute node

   grep mkhomedir /etc/pam.d/system-auth



**Auth playbook fails with "omnia_auth container not found"**
Ensure the container is running:

.. code-block:: bash
   :caption: Run on: OIM host

   systemctl status omnia_auth.service
   podman ps --filter name=omnia_auth

