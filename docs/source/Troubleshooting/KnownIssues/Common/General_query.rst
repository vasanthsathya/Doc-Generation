General Issues
================

⦾ **Why are Omnia containers not coming up after rebooting the OIM?**

**Probable Cause**: The Admin NIC on the OIM may have its autoconnect settings disabled (``autoconnect=no``), which stops it from reconnecting automatically after a reboot.