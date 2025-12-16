General Issues
================

⦾ **Why are Omnia containers not coming up after rebooting the OIM?**

**Probable Cause**: The Admin NIC on the OIM may have its autoconnect settings disabled (``autoconnect=no``), which stops it from reconnecting automatically after a reboot.

**Resolution**: Ensure that the Admin NIC on the OIM is configured with ``autoconnect=yes`` so it automatically reconnects after reboot. If you changed this configuration, reboot your OIM once to nullify any cache-related or stale configuration issues.

⦾ **When you PXE boot the devices after discovery, the following devices may not PXE boot as expected:**
 * R7615
 * R6615