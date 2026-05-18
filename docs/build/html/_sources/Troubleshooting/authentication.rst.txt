

Authentication Issues
=====================


Issues related to LDAP authentication, user login, the ``omnia_auth``
container, and TLS certificate errors.


LDAP bind failures
------------------


???+ note "Symptom"

    LDAP client operations fail with bind errors:


.. code-block:: text

       ldap_bind: Invalid credentials (49)



    Or Ansible playbooks fail when attempting to configure LDAP with
    authentication errors.

??? note "Cause"

    - The LDAP admin bind DN or password is incorrect.
    - The LDAP server is not running.
    - TLS certificate verification fails, preventing the secure bind.

??? note "Resolution"

    #. Verify the LDAP server is running:


.. code-block:: bash

          # If running as a container on the auth_server node
          ssh <auth_server> podman ps | grep ldap
          # or
          ssh <auth_server> systemctl status slapd



    #. Test a manual bind:


.. code-block:: bash

          ldapsearch -x -H ldap://<auth_server>:389 \
            -D "cn=admin,dc=example,dc=com" \
            -W -b "dc=example,dc=com" "(objectClass=*)"



    #. Verify credentials in the Omnia vault:


.. code-block:: bash

          ssh omnia_core
          ansible-vault view /omnia/input/credentials.yml



       Confirm the LDAP bind DN and password match what the LDAP server expects.

    #. If TLS is the issue, test without TLS first to isolate:


.. code-block:: bash

          ldapsearch -x -H ldap://<auth_server>:389 \
            -D "cn=admin,dc=example,dc=com" -W -b "dc=example,dc=com"



       Then test with TLS:


.. code-block:: bash

          ldapsearch -x -H ldaps://<auth_server>:636 \
            -D "cn=admin,dc=example,dc=com" -W -b "dc=example,dc=com"




User login fails on cluster nodes
---------------------------------


???+ note "Symptom"

    Users cannot log in to Slurm compute nodes or login nodes via SSH. Login
    attempts fail with:


.. code-block:: text

       Permission denied, please try again.



    Even though the user exists in LDAP and can authenticate on the auth server
    directly.

??? note "Cause"

    - The LDAP client (``sssd`` or ``nslcd``) is not running on the target node.
    - The LDAP client is configured with the wrong server URI or search base.
    - NSS (Name Service Switch) is not configured to use LDAP.
    - The user's home directory does not exist on the target node.

??? note "Resolution"

    #. Check SSSD status on the target node:


.. code-block:: bash

          ssh <node> systemctl status sssd



       If not running:


.. code-block:: bash

          ssh <node> systemctl start sssd



    #. Verify SSSD configuration:


.. code-block:: bash

          ssh <node> cat /etc/sssd/sssd.conf | grep -E 'ldap_uri|ldap_search_base'



    #. Test user lookup via NSS:


.. code-block:: bash

          ssh <node> getent passwd <username>



       If the user does not appear, SSSD or NSS is misconfigured.

    #. Check if the home directory exists:


.. code-block:: bash

          ssh <node> ls -la /home/<username>



       If it does not exist, enable automatic home directory creation:


.. code-block:: bash

          ssh <node> authconfig --enablemkhomedir --update



    #. Clear the SSSD cache and restart:


.. code-block:: bash

          ssh <node> sss_cache -E
          ssh <node> systemctl restart sssd




`omnia_auth` container not starting
-----------------------------------


???+ note "Symptom"

    The ``omnia_auth`` container fails to start or repeatedly crashes. ``podman
    ps -a`` shows it in ``Exited`` state.

??? note "Cause"

    - Port conflicts (another service is using ports 389 or 636).
    - Missing or corrupt TLS certificates.
    - Insufficient permissions on data volumes.
    - The container image is missing or corrupt.

??? note "Resolution"

    #. Check container logs:


.. code-block:: bash

          podman logs omnia_auth



    #. Check for port conflicts:


.. code-block:: bash

          ss -tlnp | grep -E '389|636'



       If another service is using the ports, stop it or reconfigure:


.. code-block:: bash

          systemctl stop <conflicting_service>



    #. Verify TLS certificate files exist and are readable:


.. code-block:: bash

          ls -la /etc/omnia/certs/ldap/



    #. Verify data directory permissions:


.. code-block:: bash

          ls -la /var/lib/omnia/ldap/



    #. Re-pull the container image if it is corrupt:


.. code-block:: bash

          podman pull <registry>/omnia_auth:<tag>



    #. Re-run the authentication playbook:


.. code-block:: bash

          ssh omnia_core
          cd /omnia
          ansible-playbook playbooks/auth.yml




Certificate errors
------------------


???+ note "Symptom"

    LDAP or other services fail with TLS certificate errors:


.. code-block:: text

       TLS: peer cert untrusted or revoked
       SSL routines:ssl3_get_server_certificate:certificate verify failed



??? note "Cause"

    - The CA certificate used by step-ca is not installed on the client node.
    - The service certificate has expired.
    - The certificate's Subject Alternative Name (SAN) does not match the
      hostname or IP being used to connect.

??? note "Resolution"

    #. Check the certificate expiry:


.. code-block:: bash

          # Using openssl
          openssl x509 -in /etc/step/certs/server.crt -noout -dates
   
          # Using step-cli
          step certificate inspect /etc/step/certs/server.crt --short



    #. If expired, renew the certificate:


.. code-block:: bash

          step ca renew /etc/step/certs/server.crt /etc/step/certs/server.key



    #. Verify the CA certificate is installed on client nodes:


.. code-block:: bash

          ssh <client_node> ls /etc/pki/ca-trust/source/anchors/



       If the CA cert is missing, copy it and update the trust store:


.. code-block:: bash

          scp /etc/step/certs/root_ca.crt <client_node>:/etc/pki/ca-trust/source/anchors/
          ssh <client_node> update-ca-trust



    #. Verify the SAN matches the connection target:


.. code-block:: bash

          openssl x509 -in /etc/step/certs/server.crt -noout -ext subjectAltName



       If the SAN does not include the correct hostname or IP, reissue the
       certificate:


.. code-block:: bash

          step ca certificate <hostname> /etc/step/certs/server.crt \
            /etc/step/certs/server.key --san <hostname> --san <ip_address>



    #. Restart services after updating certificates:


.. code-block:: bash

          systemctl restart sssd
          podman restart omnia_auth




.. note::


   - :doc:`Setup Openldap <../HowTo/Authentication/setup_openldap>` -- OpenLDAP setup guide.
   - :doc:`Security Hardening <../Operations/security_hardening>` -- TLS and LDAP hardening.
   - :doc:`Security Hardening <../Operations/security_hardening>` -- Credential rotation procedures.

