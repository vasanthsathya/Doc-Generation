

Best Practices Checklist
========================


A consolidated checklist of recommendations for deploying and operating an
Omnia cluster. Each item links to the relevant documentation section for
detailed procedures.


BIOS and firmware
-----------------



.. list-table::
   :header-rows: 1
   :widths: auto

   * - 
     - Best Practice
     - Reference
   * - ☐
     - **Disable PowerCap** on all compute nodes to ensure maximum CPU performance. PowerCap can throttle compute-intensive HPC workloads.
     - :doc:`Prerequisites Checklist <../GetStarted/prerequisites_checklist>`
   * - ☐
     - **Set BIOS to Performance mode** on all compute nodes. The ``Performance`` power profile maximizes clock speeds and disables power-saving C-states that introduce latency.
     - :doc:`Prerequisites Checklist <../GetStarted/prerequisites_checklist>`
   * - ☐
     - **Keep iDRAC firmware current** on all nodes. Firmware updates fix bugs, improve Redfish API reliability, and patch security vulnerabilities. Use Dell Repository Manager or ``racadm`` for updates.
     - :doc:`Security Hardening <security_hardening>`



Playbook execution
------------------



.. list-table::
   :header-rows: 1
   :widths: auto

   * - 
     - Best Practice
     - Reference
   * - ☐
     - **Run playbooks from their directory** using ``cd``. Omnia playbooks use relative paths for roles and configuration files. Always ``cd /omnia`` before running ``ansible-playbook``.
     - :doc:`Index <../HowTo/index>`
   * - ☐
     - **Review prerequisites before running playbooks.** Each playbook has specific input files and environment requirements. Check the corresponding how-to guide before execution.
     - :doc:`Index <../HowTo/index>`



Storage and telemetry
---------------------



.. list-table::
   :header-rows: 1
   :widths: auto

   * - 
     - Best Practice
     - Reference
   * - ☐
     - **Provision sufficient NFS storage for telemetry.** The telemetry pipeline (VictoriaMetrics, Kafka) can generate significant data volumes. Allocate at least 500 GB of NFS-backed persistent storage for telemetry retention.
     - :doc:`Setup Telemetry <../HowTo/Telemetry/setup_telemetry>`
   * - ☐
     - **Prefer the PowerScale CSI driver over external NFS** for Kubernetes persistent volumes. The CSI driver provides dynamic provisioning, better performance, and snapshot support compared to static NFS mounts.
     - :doc:`Deploy Powerscale Csi <../HowTo/Kubernetes/deploy_powerscale_csi>`
   * - ☐
     - **Ensure external NFS is accessible via the admin network.** If using external NFS (not PowerScale), verify that the NFS server is reachable from all nodes on the admin network and that firewall rules allow NFS traffic (ports 2049, 111).
     - :doc:`Configure Nfs <../HowTo/Storage/configure_nfs>`



System administration
---------------------



.. list-table::
   :header-rows: 1
   :widths: auto

   * - 
     - Best Practice
     - Reference
   * - ☐
     - **Minimize OIM reboots.** The OIM hosts critical Podman containers that provide provisioning, DHCP, and management services. Rebooting the OIM interrupts these services and may cause hostname or IP changes. Plan reboots during maintenance windows only.
     - :doc:`General <../Troubleshooting/general>`
   * - ☐
     - **Keep Firefox updated on RHEL OIM.** If you use the AWX web UI on the OIM, ensure Firefox (the default RHEL browser) is updated to avoid TLS compatibility and rendering issues.
     - :doc:`Security Hardening <security_hardening>`
   * - ☐
     - **Run** ``yum update --security`` **routinely.** Apply security patches on the OIM and all cluster nodes on a regular schedule (monthly recommended). Drain Slurm nodes before applying updates.
     - :doc:`Security Hardening <security_hardening>`
   * - ☐
     - **Sync system time across the OIM and all nodes.** Use ``chrony`` or ``ntpd`` to maintain synchronized clocks. Time drift causes Kerberos authentication failures, Slurm scheduling issues, and inaccurate telemetry timestamps.
     - :doc:`Prerequisites Checklist <../GetStarted/prerequisites_checklist>`



Pre-deployment summary
----------------------


Use this condensed list as a quick pre-flight check before running any Omnia
deployment:

#. ☐ BIOS: PowerCap disabled, Performance mode set.
#. ☐ iDRAC firmware updated to the latest supported version.
#. ☐ Network: admin and BMC VLANs configured, NFS accessible.
#. ☐ System clocks synchronized (chrony/NTP).
#. ☐ OIM meets minimum requirements (4+ cores, 32+ GB RAM, 256+ GB disk).
#. ☐ Input files reviewed and populated (mapping file, config files).
#. ☐ Credentials encrypted with Ansible Vault.
#. ☐ Sufficient NFS storage allocated for telemetry.
#. ☐ Firefox updated (if using AWX web UI).
#. ☐ Security updates applied: ``yum update --security``.




.. note::


   - :doc:`Prerequisites Checklist <../GetStarted/prerequisites_checklist>` -- Detailed prerequisites for
     all deployment paths.
   - :doc:`Security Hardening <security_hardening>` -- Full security hardening procedures.
   - :doc:`Log Management <log_management>` -- Log monitoring and rotation configuration.

