Omnia Global Prechecks and Troubleshooting Runbook
===================================================

**Audience**
  OIM administrators deploying Omnia 2.x on RHEL 10 Server with GUI.

**Scope**
  Mirrors the official RHEL installation flow and provides fast triage,
  diagnostics, and fixes for common deployment issues.

How to Use This Runbook
----------------------

- Follow the sections **in order**, aligned with the Omnia installation flow.
- Each section is organized as:

  **Symptoms → Checks → Fixes**

- Use the commands as provided.
- If blocked, jump to the **Quick Decision Tree** at the end.

---

Global Pre-Checks (Run Once)
---------------------------

These checks eliminate the majority of installation failures and should be
completed before starting the Omnia deployment.

Validate OS, Resources, and Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verify the operating system version, memory, and disk availability.

.. code-block:: bash

   cat /etc/os-release | egrep 'Red Hat Enterprise Linux|VERSION_ID'
   free -h
   df -h /

**Fixes**

- Resize the VM if resources are insufficient.
- Move container storage (``/var/lib/containers``) to a larger disk or NFS share
  if space is limited.

---

Validate Time Synchronization (CRITICAL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TLS communication between Omnia containers depends on accurate time
synchronization.

.. code-block:: bash

   timedatectl status
   chronyc tracking || chronyc sources -v

**Fixes**

- Enable Chrony or NTP.
- Re-synchronize time before continuing.

---

Validate Podman Runtime
~~~~~~~~~~~~~~~~~~~~~~~~

Ensure that the Podman container runtime is installed and functioning correctly.

.. code-block:: bash

   dnf -y install podman
   podman info

**Fixes**

- Resolve any Podman errors before proceeding.

---

Validate Registry Reachability (Pulls Happen Often)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verify registry access and authentication.

.. code-block:: bash

   podman login docker.io
   podman run --rm registry.access.redhat.com/ubi10/ubi sh -lc 'curl -sSf https://raw.githubusercontent.com >/dev/null'

**Fixes**

- Configure proxy environment variables for Podman or systemd if required.
- Authenticate to registries to avoid pull throttling.

---

Troubleshooting Runbook
----------------------------

Deploy Omnia Core Container (omnia.sh)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**

- Script aborts early
- ``podman pull`` fails
- Core container starts but cannot write to the shared path

**Checks**

List running containers:

.. code-block:: bash

   podman ps --format 'table {{.Names}}\t{{.Status}}'

View container logs:

.. code-block:: bash

   podman logs -n 200 omnia_core

**Common Causes and Fixes**

**Hostname validation failure**

Rules:
- No dot, underscore, or comma
- No leading or trailing ``-``
- No uppercase characters
- Must not start with a digit
- FQDN length must be ≤ 64 characters

**Fix**
Rename the host to comply with these rules and re-run the script.

---

**Podman missing or image pull blocked**

**Fix**
- Install Podman
- Run ``podman login``
- Verify outbound network connectivity

---

**NFS shared path with SELinux**

**Fix**
- Export NFS with ``no_root_squash``
- Ensure 755 permissions
- Bind the shared path with SELinux relabeling:

.. code-block:: bash

   podman run --rm -v /shared:/mnt:z registry.access.redhat.com/ubi10/ubi sh -lc 'touch /mnt/.rw'

If unsure, start with a **local** shared path and switch to NFS later.

---

Credentials and project_default Inputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration files are located under:

``/opt/omnia/input/project_default/``

**Common Symptoms**

- Services missing later in the deployment
- Network services misbehave

**Checks**

.. code-block:: bash

   ls network_spec.yml software_config.json local_repo_config.yml telemetry_config.yml

**Fixes**

- Validate YAML and JSON syntax.
- Ensure values match the intended architecture (x86_64 or aarch64).

---

Network Specification (network_spec.yml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Common Symptoms**

- DHCP or PXE not working
- iDRAC unreachable
- IP address conflicts

**Checks**

.. code-block:: bash

   nmcli connection
   ip -4 addr show

**Fixes**

- ``oim_nic_name`` must match the actual NIC.
- ``primary_oim_admin_ip``, ``netmask_bits``, and ``dynamic_range`` must not
  overlap with other networks.
- Ensure iDRAC interfaces are reachable from the OIM admin network.

---

Prepare the OIM (prepare_oim.yml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step brings up OpenCHAMI, Omnia Auth, and Pulp services.

**Common Symptoms**

- Certificate or TLS failures
- Expected containers not created
- Services running but unreachable

**Checks**

.. code-block:: bash

   podman ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'

Re-check time synchronization:

.. code-block:: bash

   timedatectl status

**Common Causes and Fixes**

**Time skew causing TLS failures**

**Fix**
Synchronize time on the OIM and nodes, then re-run the playbook.

**Firewall blocking access**

**Fix**
Open the required OIM ports for enabled services (OpenCHAMI, Omnia Auth, Pulp).

---

Local Repositories (Pulp)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Common Symptoms**

- Repository synchronization failures
- Incorrect package versions

**Checks**

.. code-block:: bash

   podman ps | grep pulp
   podman logs -n 200 pulp

**Fixes**

- Verify RHEL subscription and ensure BaseOS and AppStream repositories are enabled.
- If required, pin the RHEL release before repository creation:

.. code-block:: bash

   subscription-manager release --show
   subscription-manager release --set=10.0

- Ensure upstream repositories or mirrors are reachable.

---

Discover and Provision Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Common Symptoms**

- Nodes never PXE boot
- Provisioning stalls

**Checks**

.. code-block:: bash

   nmcli connection
   ip link show

**Fixes**

- Set nodes to PXE boot before running discovery.
- Ensure admin and BMC switches are configured and reachable.
- Build OS images first:
  - ``build_image_x86_64.yml``
  - ``build_image_aarch64.yml``

---

Inventory and Cluster Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**

- Inventory is empty or incomplete
- Cluster services fail to configure

**Fixes**

- Verify that all required OIM services are running.
- Re-run ``prepare_oim.yml`` after changing any service-related inputs.
- Check firewall ports between the OIM and the cluster nodes.

---

SELinux and Podman Quick Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Use ``:z`` (shared) or ``:Z`` (private) on bind mounts to apply
  ``container_file_t``.
- Be cautious: relabeling affects host paths.

---

Logs and Debugging Shortcuts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   podman ps -a
   podman logs -n 200 <container>
   podman exec -it <container> sh -lc 'curl -I https://example.com'

---

Quick Decision Tree
-------------------

- Core not running → Check Podman, hostname, shared path SELinux
- Prepare OIM failed → Check time sync → inputs → firewall ports
- Repository failures → Check subscription/pinning → outbound access
- Provisioning stalls → Check PXE, NIC names, OS images

---

Appendix: Safe Re-Runs
----------------------

- It is generally safe to fix inputs and re-run ``prepare_oim.yml``.
- Avoid changing the OIM node mid-deployment; redeploy if required.

**Tip**
Treat each step as a gate. Do not proceed to the next step until the current step
completes cleanly.
