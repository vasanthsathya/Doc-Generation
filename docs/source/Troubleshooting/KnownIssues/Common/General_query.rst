General Issues
================

⦾ **Why are Omnia containers not coming up after rebooting the OIM?**

**Probable Cause**: The Admin NIC on the OIM may have its autoconnect settings disabled (``autoconnect=no``), which stops it from reconnecting automatically after a reboot.

**Resolution**: Ensure that the Admin NIC on the OIM is configured with ``autoconnect=yes`` so it automatically reconnects after reboot. If you changed this configuration, reboot your OIM once to nullify any cache-related or stale configuration issues.

⦾ **After successful discovery, PowerEdge R7615 and R6615 nodes might fail to complete PXE boot or become unresponsive during the provisioning process.**

**Resolution**: Not available. For more information about the issue, see `PowerEdge: C6615 Red Hat Enterprise Linux Install May Fail When Media Is Mounted on Remote File Share' <https://www.dell.com/support/kbdoc/en-us/000193828/poweredge-c6615-red-hat-enterprise-linux-install-may-fail-when-media-is-mounted-on-remote-file-share>`_.