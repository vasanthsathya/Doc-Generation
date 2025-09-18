Best Practices
==============

* Ensure that PowerCap policy is disabled and the BIOS system profile is set to 'Performance' on the OIM.
* Always run playbooks inside the Omnia core container from the directory where they are located. Use the ``cd`` command to navigate to the playbook's directory before executing it.
* Omnia recommends using an NFS share with at least 100GB storage for OIM and cluster configuration.
* Use a `PXE mapping file <OmniaInstallGuide/samplefiles.html#pxe-mapping-file-csv>`_ even when using DHCP configuration to ensure that IP assignments remain persistent across OIM reboots.
* Avoid rebooting the OIM as much as possible to prevent disruptions to the network configuration.
* Review all the prerequisites and input files before running Omnia playbooks.
* Ensure that the Firefox version being used on the RHEL OIM is the latest available. This can be achieved using ``dnf update firefox -y``
* Run ``yum update --security`` routinely on the RHEL OIM to get the latest security updates.