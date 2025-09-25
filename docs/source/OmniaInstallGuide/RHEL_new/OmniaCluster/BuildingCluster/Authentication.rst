Step 4: Setup OpenLDAP for centralized authentication 
======================================================

The security feature allows cluster admin users to set up OpenLDAP in order to allow or deny access to the user(s).

Configuring OpenLDAP security
--------------------------------------

**Prerequisites**

* To set up OpenLDAP, ensure that the following entry is present in the ``/opt/omnia/input/project_default/software_config.json``: ::

    {"name": "openldap", "arch": ["x86_64"]}

* Run ``local_repo.yml`` to create offline repositories of OpenLDAP. Ensure that the non-required software is removed from ``/opt/omnia/input/project_default/software_config.json`` before running ``security.yml``. For more information, `click here <../../CreateLocalRepo/index.html>`_.


Running the security role
--------------------------

The wrapper playbook ``omnia.yml`` handles execution of the security or authentication role. Alternatively: ::

    cd security
    ansible-playbook security.yml -i inventory

The provided inventory should contain ``auth_server`` and ``login_node`` [optional] groups. The inventory file is case-sensitive. Follow the format provided in the `sample files <../../../samplefiles.html#inventory-file>`_.

    * Do not include the IP of the OIM or local host in the ``auth_server`` group of the inventory file.
    * For `secure login node functionality <Authentication.html#configuring-login-node-security>`_, ensure to add the ``login_node`` group in the provided inventory file. To customize the security features on the login node, update the desired parameters in ``/opt/omnia/input/project_default/login_node_security_config.yml``.
    * If a subsequent run of ``security.yml`` fails, the ``/opt/omnia/input/project_default/security_config.yml`` file will be unencrypted.

.. note:: Installation of OpenLDAP server or FreeIPA server on OIM is not supported.

.. caution:: No users will be created by Omnia.

Create a new user on OpenLDAP
-----------------------------

1. Create an LDIF file (eg: ``create_user.ldif``) on the auth server containing the following information:

    * DN: The distinguished name that indicates where the user will be created.
    * objectClass: The object class specifies the mandatory and optional attributes that can be associated with an entry of that class. Here, the values are ``inetOrgPerson``, ``posixAccount``, and ``shadowAccount``.
    * UID: The username of the replication user.
    * sn: The surname of the intended user.
    * cn: The given name of the intended user.

Below is a sample file: ::

    # User Creation
    dn: uid=ldapuser,ou=People,dc=omnia,dc=test
    objectClass: inetOrgPerson
    objectClass: posixAccount
    objectClass: shadowAccount
    cn: ldapuser
    sn: ldapuser
    loginShell:/bin/bash
    uidNumber: 2000
    gidNumber: 2000
    homeDirectory: /home/ldapuser
    shadowLastChange: 0
    shadowMax: 0
    shadowWarning: 0

    # Group Creation
    dn: cn=ldapuser,ou=Group,dc=omnia,dc=test
    objectClass: posixGroup
    cn: ldapuser
    gidNumber: 2000
    memberUid: ldapuser

.. note:: Avoid whitespaces when using an LDIF file for user creation. Extra spaces in the input data may be encrypted by OpenLDAP and cause access failures.

2. Run the command ``ldapadd -D <enter admin binddn > -w < bind_password > -f create_user.ldif`` to execute the LDIF file and create the account.
3. To set up a password for this account, use the command ``ldappasswd -D <enter admin binddn > -w < bind_password > -S <user_dn>``. The value of ``user_dn`` is the distinguished name that indicates where the user was created. (In this example, ``uid=ldapuser,ou=People,dc=omnia,dc=test``)

Setting up Passwordless SSH for the OpenLDAP/FreeIPA users
-----------------------------------------------------------

Once user accounts are created, admins can enable passwordless SSH for users to run HPC jobs on the cluster nodes.

.. note:: Once user accounts are created on the auth server, use the accounts to login to the cluster nodes to reset the password and create a corresponding home directory.

To customize your setup of passwordless ssh, input custom parameters in ``/opt/omnia/input/project_default/passwordless_ssh_config.yml``:

+-----------------------+--------------------------------------------------------------------------------------------------------------------+
| Parameter             | Details                                                                                                            |
+=======================+====================================================================================================================+
| user_name             | The list of users that requires password-less SSH. Separate the list of users using a comma.                       |
|      ``string``       |  Eg: ``user1,user2,user3``                                                                                         |
|      Required         |                                                                                                                    |
+-----------------------+--------------------------------------------------------------------------------------------------------------------+
| authentication_type   | Indicates whether LDAP or FreeIPA is in use on the cluster.                                                        |
|      ``string``       |                                                                                                                    |
|      Required         |      Choices:                                                                                                      |
|                       |                                                                                                                    |
|                       |      * ``freeipa``                                                                                                 |
|                       |                                                                                                                    |
|                       |      * ``ldap``   <- Default                                                                                       |
+-----------------------+--------------------------------------------------------------------------------------------------------------------+


Use the below command to enable passwordless SSH: ::

    ansible-playbook user_passwordless_ssh.yml -i inventory

Where inventory follows the format defined under inventory file in the provided `sample files. <../../../sample files.html>`_ The inventory file is case-sensitive. Follow the format provided in the sample file link.

.. caution:: Do not run ssh-keygen commands after passwordless SSH is set up on the nodes.

Setting up OpenLDAP as a proxy server
--------------------------------------

Omnia allows the internal OpenLDAP server to be configured as a proxy, where it utilizes the external LDAP servers as a backend database to store user data and acts as an authentication entity to allow/deny them access to the cluster. OpenLDAP client will be configured through the proxy server which means that there won't be any direct communication between OpenLDAP client and the external LDAP server.

.. note:: If the OpenLDAP server is set up as a proxy, the user database is not replicated onto the server.

Perform the following steps to configure OpenLDAP as a proxy server:

1. Go to ``/opt/omnia/authservice/slapd.conf``, replace the ``slapd.conf`` with the updated ``slapd.conf`` file, and run the following command to restart the ``omnia_auth`` container.::

		podman restart omnia_auth

2. Now, locate the ``slapd.conf`` config file present in ``/opt/omnia/authservice/`` and modify the file to add the new LDAP configurations. Add the following lines to the config file based on the operating system running on the cluster:

    For RHEL: ::

        include        /etc/openldap/schema/core.schema
        include        /etc/openldap/schema/cosine.schema
        include        /etc/openldap/schema/nis.schema
        include        /etc/openldap/schema/inetorgperson.schema
        
        
        pidfile         /run/openldap/slapd.pid
        argsfile        /run/openldap/slapd.args
        
        # Load dynamic backend modules:
        modulepath      /usr/lib64/openldap
        moduleload      back_ldap.la
        moduleload      back_meta.la

        #######################################################################
        # Meta database definitions
        #######################################################################
        database        meta
        suffix          "dc=phantom,dc=test"
        rootdn          cn=admin,dc=phantom,dc=test
        rootpw          Dell1234

        uri             "ldap://10.5.0.104:389/dc=phantom,dc=test"
        suffixmassage   "dc=phantom,dc=test" "dc=perf,dc=test"
        idassert-bind
         bindmethod=simple
         binddn="cn=admin,dc=perf,dc=test"
         credentials="Dell1234"
         flags=override
         mode=none
        TLSCACertificateFile    /etc/openldap/certs/ldapserver.crt
        TLSCertificateFile      /etc/openldap/certs/ldapserver.crt
        TLSCertificateKeyFile   /etc/pki/tls/certs/ldapserver.key

Change the **<parameter>** values in the config file, as described below:

* **database**: Database used in the ``slapd.conf`` file, that captures the details of the external LDAP server to be used. For example, ``meta``.
* **suffix**: Captures the domain name of internal OpenLDAP user, to refine the user search while attempting to authenticate the user. For example, ``"dc=omnia,dc=test"``.
* **rootdn**: Admin or root username of the internal OpenLDAP server set up by Omnia. For example, ``cn=admin,dc=omnia,dc=test``.
* **rootpw**: Admin password for the internal OpenLDAP server. For example, ``Dell1234``.

* **uri**: Captures the IP of the external LDAP server along with the port and the domain of the user in ``"ldap://<IP  of external LDAP server>:<Port number>/<suffix>"`` format. For example, ``"ldap://10.5.0.104:389/dc=omnia,dc=test"``.
* **suffixmassage**: ``suffixmassage`` allows you to dynamically move the LDAP client information from the existing internal OpenLDAP server to the external LDAP server that you want to configure as a proxy. This is provided in the ``suffixmassage <suffix1> <suffix2>`` format.

        * ``<suffix1>`` is the internal OpenLDAP server suffix (base DN).
        * ``<suffix2>`` is the external LDAP server suffix (base DN).

* **binddn**: Admin username and domain of the external LDAP server.
* **credentials**: Admin password for the external LDAP server.

* **TLSCACertificateFile**: Omnia, by default, creates the TLSA certificate in ``/etc/openldap/certs/ldapserver.crt``.
* **TLSCertificateFile**: Omnia, by default, creates the TLS certificate in ``/etc/openldap/certs/ldapserver.crt``.
* **TLSCertificateKeyFile**: Omnia, by default, creates the certificate key file in ``/etc/pki/tls/certs/ldapserver.key``.

.. note::
   * The values for ``suffix`` and ``rootdn`` parameters in the ``slapd.conf`` file must be the same as those provided in the ``get_config_credentials.yml`` file.

   * Multiple external LDAP servers can also be configured on the proxy server. The OpenLDAP proxy server allows users from multiple external LDAP servers to authenticate onto the cluster. You can provide two sets of external LDAP server details as shown below: ::

            uri "ldap://10.5.0.104:389/dc=omnia1,dc=test"
            idassert-bind
             bindmethod=simple
             binddn="cn=admin,dc=omnia,dc=test"
             credentials="Dell1234"
             flags=override
             mode=none

            uri "ldap://10.5.0.105:389/dc=omnia2,dc=test"
            idassert-bind
             bindmethod=simple
             binddn="cn=admin,dc=omnia,dc=test"
             credentials="Dell12345"
             flags=override
             mode=none

3. Once the new configurations are present in the ``slapd.conf`` file, restart the ``omnia_auth`` container: ::

    podman restart omnia_auth

5. Restart the internal OpenLDAP server to seal in the configurations. Execute the following command to restart the server: ::

    systemctl restart slapd-ltb.service


Once these configurations are applied on the internal OpenLDAP server, it sets up the external LDAP server as an authentication server. The internal OpenLDAP server doesn't store any kind of user data and no users can be created/modified from here.