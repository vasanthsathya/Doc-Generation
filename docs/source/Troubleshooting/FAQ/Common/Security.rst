Centralized authentication
=============================

⦾ **Why am I unable to login using LDAP credentials after successfully creating a user account?**

**Potential Cause**: Whitespaces in the LDIF file may have caused an encryption error. Verify whether there are any whitespaces in the file by running ``cat -vet <filename>``.

**Resolution**: Remove the whitespaces and re-run the LDIF file.


⦾ **Why does the user login fail for an OpenLDAP user?**

**Potential Cause**: Incorrect OpenLDAP service is running on the authentication server.

**Resolution**: Ensure that ``slapd-ltb.service`` is running on the authentication server. Use the following command to check if the service running: ::

    systemctl status slapd-ltb.service