
Install RHEL 10 on aarch64 bare-metal server
---------------------------------------------
1. 







Build OpenCHAMI image for aarch64
----------------------------------

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
