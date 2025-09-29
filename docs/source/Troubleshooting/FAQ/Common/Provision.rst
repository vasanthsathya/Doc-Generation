Provision
==========

⦾ **Why is the provisioning status of my target servers stuck at** ``powering-on`` **in the** ``cluster.nodeinfo`` **table (omniadb)?**

**Potential Cause**:

    * Hardware issues (Auto-reboot may fail due to hardware tests failing)
    * The target node may already have an OS and the first boot PXE device is not configured correctly.

**Resolution**:

    * Resolve/replace the faulty hardware and PXE boot the node.
    * Target servers should be configured to boot in PXE mode with the appropriate NIC as the first boot device.


⦾ **What to do if user login fails when accessing a cluster node?**

.. image:: ../../../images/UserLoginError.png

**Potential Cause**: SSH key on the OIM may be outdated.

**Resolution**:

   * Refresh the key using ``ssh-keygen -R <hostname/server IP>``.
   * Retry login.

⦾ **How is the gracefull shutdown of an Omnia cluster is achieved?**

**Potential Cause**: Manage OIM reboot/shutdown scenario.

**Resolution**: In the case of a planned shutdown, ensure that the OIM is shut down after the compute nodes. When powering back up, the OIM should be powered on and OpenCHAMI resumed before bringing up the compute nodes. In short, have the OIM as the first node up and the last node down.

For more information, `click here <https://github.com/xcat2/xcat-core/issues/7374>`_

⦾ **What to do if the Lifecycle Controller (LC) is not ready?**

**Resolution**:

* Verify that the LC is in a ready state for all servers using: ``racadm getremoteservicesstatus``
* PXE boot the target server.