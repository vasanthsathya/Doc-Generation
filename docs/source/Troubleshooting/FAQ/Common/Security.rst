Centralized authentication
=============================

⦾ **Why am I unable to login using LDAP credentials after successfully creating a user account?**

**Potential Cause**: Whitespaces in the LDIF file may have caused an encryption error. Verify whether there are any whitespaces in the file by running ``cat -vet <filename>``.

**Resolution**: Remove the whitespaces and re-run the LDIF file.

