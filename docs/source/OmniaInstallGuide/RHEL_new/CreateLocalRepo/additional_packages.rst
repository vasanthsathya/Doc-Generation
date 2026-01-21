Configure Additional Packages
=============================

Use ``additional_packages.json`` to specify additional RPMs and container images to be deployed on cluster nodes.

File location
-------------

``/opt/omnia/input/project_default/additional_packages.json``

Scope
-----

* Entries under ``additional_packages -> cluster`` are deployed on all cluster nodes.
* Entries under each functional group (for example, ``service_kube_control_plane``) are deployed only on nodes in that functional group.

Supported package types
-----------------------

* ``rpm``: Requires ``repo_name``.
* ``image``: Requires ``tag`` or ``digest``.

The following table lists the supported sections in ``additional_packages.json`` and the required parameters for each package type.

.. csv-table:: Additional software packages
   :file: ../../../Tables/additional_software_packages.csv
   :header-rows: 1
   :keepspace:
   :widths: auto

Sample file
-----------

.. code-block:: json

   {
     "additional_packages": {
       "cluster": [
         { "package": "fuse-overlayfs", "type": "rpm", "repo_name": "x86_64_appstream" },
         { "package": "python3-PyMySQL", "type": "rpm", "repo_name": "x86_64_appstream" },
         { "package": "sssd", "type": "rpm", "repo_name": "x86_64_baseos" },
         { "package": "oddjob-mkhomedir", "type": "rpm", "repo_name": "x86_64_appstream" },
         { "package": "quay.io/strimzi/kafka-bridge", "type": "image", "tag": "0.33.1" },
         {
           "package": "registry.k8s.io/pause",
           "type": "image",
           "digest": "sha256:7031c1b283388c2c47cc389c74e7a6a1f91e3c23f7f9c2d9e25f7c8b1a2d3e4f"
         }
       ]
     },
     "service_kube_control_plane": {
       "cluster": [
         { "package": "git", "type": "rpm", "repo_name": "x86_64_appstream" },
         { "package": "docker.io/curlimages/curl", "type": "image", "tag": "8.17.0" },
         { "package": "docker.io/mohr/activemq", "type": "image", "tag": "5.15.9" }
       ]
     },
     "service_kube_control_plane_first": {
       "cluster": [
         { "package": "kernel-devel", "type": "rpm", "repo_name": "x86_64_appstream" },
         { "package": "kernel-headers", "type": "rpm", "repo_name": "x86_64_appstream" }
       ]
     }
   }
