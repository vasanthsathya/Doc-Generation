
Provisioning and Preparing aarch64 Node
========================================

To provision aarch64 node, you need to install RHEL 10 OS and optionally build OpenCHAMI image for aarch64 node.


Install RHEL 10 on aarch64 bare-metal node
--------------------------------------------
1. Manually install the RHEL 10 OS on one of the aarch64 nodes with the root password enabled.

  .. note:: 
      * The root password must be at least 8 characters long, contain alphanumeric characters, and must not include commas (,), hyphens (-), single quotes ('), double quotes ("), or backslashes (\).
      * During RHEL installation on an aarch64 node, ensure that the password set during installation is supplied as ``provision_password`` when running ``discovery.yml``.

2. Use the **host IP address** of the node in the ``admin_aarch64`` inventory file.  
   **Sample aarch64 inventory:**

   ::

      [admin_aarch64]
      <host IP address>

Build OpenCHAMI image for aarch64 [Optional]
---------------------------------------------

Perform the following steps to build the OpenCHAMI aarch64 image:

1. Clone the https://github.com/OpenCHAMI/image-builder.git repository using the following command: 

   .. code-block:: bash

      git clone https://github.com/OpenCHAMI/image-builder.git

2. Run the following command to navigate to the ``image-builder`` directory:

   .. code-block:: bash

      cd image-builder

3. Run the following command to build the arch64 container image:

   .. code-block:: bash

      podman build -f dockerfiles/dnf/Dockerfile -t localhost/ochami-arm64

4. Run the following command to verify that the aarch64 image is created:

   .. code-block:: bash

      podman images

Ensure that **localhost/ochami-arm64** appears in the output to confirm that the image was successfully built.
