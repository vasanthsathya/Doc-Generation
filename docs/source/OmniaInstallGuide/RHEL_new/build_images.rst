Step 11: Build cluster node images
====================================

The ``build_image_x86_64.yml`` and ``build_image_aarch64.yml`` playbooks are used to build diskless images for ``x86_64`` and ``aarch64`` cluster nodes, respectively. 
Each image is created based on the functional groups defined in the 
``functional_groups_config.yml`` file. 

If you have aarch64 cluster nodes to be booted, then to build OpenCHAMI image for aarch64, perform the steps provided in :doc:`../AdvancedConfigurations/build_arm_ochami_image`.


**Prerequisites**: 

   * Ensure that the ``functional_groups_config.yml`` file defines the functional groups required for your environment. For more information on functional groups, see :doc:`composable_roles`.
   * Ensure that the local_repo.yml playbook is run and the images are downloaded into the Pulp container.
   * Ensure that OIMs running RHEL have an active subscription or are configured to access local repositories.
   * Note the compatibility between cluster OS and OIM OS below:

        +---------------------+--------------------+------------------+
        |                     |                    |                  |
        | OIM OS              | Cluster  Node OS   | Compatibility    |
        +=====================+====================+==================+
        |                     |                    |                  |
        | RHEL                | RHEL               | Yes              |
        +---------------------+--------------------+------------------+
   
Build images for x86_64 cluster nodes
----------------------------------------

To build images for the nodes present in each functional group, do the following.

1. Navigate to the image build directory::

       cd /omnia/build_image_x86_64

2. To build the image, run the following playbook:

       ansible-playbook build_image_x86_64.yml

3. To verify that images are created for each functional group defined in ``functional_groups_config.yml``, run the following command::

       s3cmd ls -Hr s3://boot-images

   The images created for each functional group are listed in the boot-images directory.


Build images for aarch64 cluster nodes
------------------------------------------

To build images for the nodes present in each functional group, do the following.

1. Navigate to the image build directory::

       cd /omnia/build_image_aarch64

2. To build the image, run the appropriate playbook based on the node architecture::

       ansible-playbook build_image_aarch64.yml -i inventory

**Sample aarch64 inventory**::
-----------------
    [admin_aarch64]
    10.0.0.1

.. note:: The IP address in the inventory must be 

3. To verify that images are created for each functional group defined in ``functional_groups_config.yml``, run the following command::

       s3cmd ls -Hr s3://boot-images

   The images created for each functional group are listed in the boot-images directory.

