

Verify OIM Services
===================


Perform a comprehensive health check of all Omnia Infrastructure Manager (OIM)
services after running ``prepare_oim.yml``. This guide walks through every
service in the ``omnia.target`` dependency tree.


Overview
--------


After the OIM is prepared, the following services should be running as
systemd-managed Podman containers:

- **omnia_core** -- Ansible control plane
- **OpenCHAMI stack** -- SMD, BSS, CoreDHCP, TFTP, DNS, and related services
- **Pulp** -- RPM repository management
- **MinIO** -- S3-compatible object storage
- **Registry** -- Local container image registry
- **Omnia Auth** *(optional)* -- Centralized authentication

This guide helps you verify each service is healthy and troubleshoot any that
are not.



Prerequisites
-------------


- The :doc:`Prepare Oim <prepare_oim>` procedure has been completed.
- You have ``root`` or ``sudo`` access to the OIM host.



Procedure
---------


#. **Check the omnia_core service**:


**Run on: OIM host**

.. code-block:: bash

      systemctl status omnia_core.service



   Expected: ``Active: active (running)``

#. **List the complete omnia.target dependency tree**:


**Run on: OIM host**

.. code-block:: bash

      systemctl list-dependencies omnia.target



   Expected output:


**Expected output on: OIM host**

.. code-block:: text

      omnia.target
      ├─minio.service
      ├─omnia_auth.service
      ├─omnia_core.service
      ├─pulp.service
      ├─registry.service
      └─openchami.target
        ├─bss.service
        ├─coredhcp.service
        ├─cloud-init-server.service
        ├─dnsmasq.service
        ├─hydra.service
        ├─image-server.service
        ├─opaal.service
        ├─smd.service
        └─tftpd.service



#. **Check each top-level service individually**:


**Run on: OIM host**

.. code-block:: bash

      for svc in minio omnia_auth omnia_core pulp registry; do
        echo "=== $svc ==="
        systemctl is-active ${svc}.service
      done



#. **Check OpenCHAMI sub-services**:


**Run on: OIM host**

.. code-block:: bash

      for svc in bss coredhcp cloud-init-server dnsmasq hydra image-server opaal smd tftpd; do
        echo "=== $svc ==="
        systemctl is-active ${svc}.service
      done



#. **Verify running Podman containers**:


**Run on: OIM host**

.. code-block:: bash

      podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"



#. **Test the OpenCHAMI CLI**:


**Run on: OIM host**

.. code-block:: bash

      ssh omnia_core




**Run on: omnia_core container**

.. code-block:: bash

      ochami --help



   Useful ``ochami`` commands:


**Run on: omnia_core container**

.. code-block:: bash

      # List discovered nodes
      ochami node list

      # Check SMD status
      ochami smd status

      # List boot configurations
      ochami bss list



#. **Test MinIO / S3 access**:


**Run on: omnia_core container**

.. code-block:: bash

      s3cmd ls



#. **Test Pulp accessibility**:


**Run on: OIM host**

.. code-block:: bash

      curl -s http://localhost:8080/pulp/api/v3/status/ | python3 -m json.tool



   Expected: a JSON response with ``"online_workers"`` and ``"versions"``.



Verification
------------


All services should report ``active (running)``. Use this summary check:


**Run on: OIM host**

.. code-block:: bash

   systemctl is-active omnia.target



Expected output: ``active``

If any service is ``inactive`` or ``failed``, note which one and refer to the
Troubleshooting section below.

**Quick health summary script**:


**Run on: OIM host**

.. code-block:: bash

   echo "=== Omnia Service Health ==="
   echo "omnia.target:    $(systemctl is-active omnia.target)"
   echo "omnia_core:      $(systemctl is-active omnia_core.service)"
   echo "openchami.target:$(systemctl is-active openchami.target)"
   echo "pulp:            $(systemctl is-active pulp.service)"
   echo "minio:           $(systemctl is-active minio.service)"
   echo "registry:        $(systemctl is-active registry.service)"
   echo "omnia_auth:      $(systemctl is-active omnia_auth.service)"





Next Steps
----------


- :doc:`Create Local Repos <create_local_repos>` -- Sync RPM repositories via Pulp.
- :doc:`Build Cluster Images <build_cluster_images>` -- Build OS boot images.
- :doc:`Discover Nodes <discover_nodes>` -- Discover and provision bare-metal servers.



Troubleshooting
---------------


**A service shows "inactive (dead)"**
   Restart the specific service:


**Run on: OIM host**

.. code-block:: bash

      systemctl restart <service-name>.service
      journalctl -u <service-name>.service --no-pager -n 50



**OpenCHAMI services fail with connection errors**
   Verify the SMD service is running first, as other OpenCHAMI services
   depend on it:


**Run on: OIM host**

.. code-block:: bash

      systemctl restart smd.service
      sleep 10
      systemctl restart openchami.target



**Pulp API returns connection refused**
   Check that the Pulp container is running and listening on port 8080:


**Run on: OIM host**

.. code-block:: bash

      podman logs pulp
      ss -tlnp | grep 8080



**MinIO not accessible**
   Verify MinIO container status and port binding:


**Run on: OIM host**

.. code-block:: bash

      podman logs minio
      ss -tlnp | grep 9000



**omnia.target not found**
   Re-run the ``prepare_oim.yml`` playbook to regenerate systemd unit files:


**Run on: omnia_core container**

.. code-block:: bash

      cd /omnia/prepare_oim
      ansible-playbook prepare_oim.yml --ask-vault-pass



**Container images missing**
   Rebuild the container images:


**Run on: OIM host**

.. code-block:: bash

      cd /opt/omnia
      bash build_images.sh core

