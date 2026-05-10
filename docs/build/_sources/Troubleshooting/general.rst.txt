

General Issues
==============


Common issues that affect the OIM, SSH connectivity, containers, and Ansible
Vault operations.


Hostname changes after OIM reboot
---------------------------------


???+ note "Symptom"

    After rebooting the OIM, the hostname reverts to ``localhost`` or a different
    value, causing Ansible playbooks and service connections to fail.

??? note "Cause"

    The OIM's hostname was set temporarily with ``hostnamectl`` but not persisted
    in ``/etc/hostname``, or a DHCP-assigned hostname overrides the static
    setting on boot.

??? note "Resolution"

    #. Set the hostname permanently:


.. code-block:: bash

          hostnamectl set-hostname oim.example.com



    #. Verify it persisted in ``/etc/hostname``:


.. code-block:: bash

          cat /etc/hostname



    #. Ensure the hostname is also in ``/etc/hosts``:


.. code-block:: text

          127.0.0.1   localhost
          <oim_ip>    oim.example.com oim



    #. If DHCP is overriding the hostname, configure the DHCP client to preserve
       the static hostname by adding the following to
       ``/etc/NetworkManager/conf.d/90-hostname.conf``:


.. code-block:: ini

          [main]
          hostname-mode=none




SSH key mismatches
------------------


???+ note "Symptom"

    SSH connections from the OIM to cluster nodes fail with:


.. code-block:: text

       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
       @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



??? note "Cause"

    The target node was re-provisioned or re-imaged, generating new SSH host
    keys that conflict with the cached keys in ``~/.ssh/known_hosts`` on the
    OIM.

??? note "Resolution"

    #. Remove the stale key for the affected host:


.. code-block:: bash

          ssh-keygen -R <node_hostname_or_ip>



    #. Reconnect to accept the new key:


.. code-block:: bash

          ssh <node_hostname_or_ip>



    #. To prevent this issue across bulk re-provisions, clear all known_hosts
       entries for cluster nodes:


.. code-block:: bash

          # Remove entries for a range of IPs
          for i in $(seq 101 110); do
              ssh-keygen -R 10.5.0.$i
          done




Container startup failures
--------------------------


???+ note "Symptom"

    One or more Podman containers fail to start after an OIM reboot, or
    ``podman ps`` shows containers in ``Exited`` or ``Error`` state.

??? note "Cause"

    Possible causes include:

    - The Podman service (``podman.socket``) did not start.
    - Containers were not configured to auto-restart.
    - Disk space exhaustion prevents container layer extraction.
    - Port conflicts with another service.

??? note "Resolution"

    #. Check the container status and error message:


.. code-block:: bash

          podman ps -a
          podman logs <container_name>



    #. Attempt a manual restart:


.. code-block:: bash

          podman start <container_name>



    #. If disk space is the issue:


.. code-block:: bash

          df -h /
          podman system prune --force



    #. If a port conflict is reported, identify the conflicting process:


.. code-block:: bash

          ss -tlnp | grep <port_number>



    #. If containers consistently fail after reboot, verify that Podman pods
       have auto-start enabled:


.. code-block:: bash

          podman generate systemd --name <pod_name> --files
          systemctl enable pod-<pod_name>.service




`ssh omnia_core` fails after `sudo`
-----------------------------------


???+ note "Symptom"

    Running ``ssh omnia_core`` as a non-root user (or after ``sudo su``) returns
    a connection error or permission denied:


.. code-block:: text

       Permission denied (publickey).



??? note "Cause"

    The ``omnia_core`` container is configured with SSH keys for the ``root``
    user. When you use ``sudo su`` to become root, the SSH agent and key
    environment may not be inherited.

??? note "Resolution"

    Log in as ``root`` directly instead of using ``sudo``:


.. code-block:: bash

       # Instead of:
       sudo su
       ssh omnia_core    # <-- fails
   
       # Do this:
       ssh root@<oim_ip>
       ssh omnia_core    # <-- works



    Alternatively, explicitly specify the SSH key:


.. code-block:: bash

       ssh -i /root/.ssh/id_rsa omnia_core




Ansible Vault encrypted file issues
-----------------------------------


???+ note "Symptom"

    Ansible playbooks fail with:


.. code-block:: text

       ERROR! Attempting to decrypt but no vault secrets found



    Or you cannot view the contents of encrypted credential files.

??? note "Cause"

    The vault password was not provided when running the playbook, or the
    vault password file path is incorrect.

??? note "Resolution"

    #. **View an encrypted file** without editing:


.. code-block:: bash

          ansible-vault view input/credentials.yml



    #. **Edit an encrypted file:**


.. code-block:: bash

          ansible-vault edit input/credentials.yml



    #. **Run a playbook with vault password prompt:**


.. code-block:: bash

          ansible-playbook playbooks/omnia.yml --ask-vault-pass



    #. **Run a playbook with a vault password file:**


.. code-block:: bash

          ansible-playbook playbooks/omnia.yml --vault-password-file /root/.vault_pass



    #. If you have forgotten the vault password, you will need to recreate the
       credentials file. There is no way to recover an AES-256 encrypted vault
       without the original password:


.. code-block:: bash

          # Back up the old file
          cp input/credentials.yml input/credentials.yml.bak
   
          # Create a new encrypted file
          ansible-vault create input/credentials.yml




.. note::


   - `Log Management <../Operations/log_management.rst>`_ -- Where to find logs for deeper
     diagnosis.
   - `Oim Cleanup <../Operations/oim_cleanup.rst>`_ -- Full OIM reset if issues persist.

