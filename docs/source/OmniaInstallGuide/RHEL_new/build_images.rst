Step 11: Build cluster node images
====================================

The ``build_image_x86_64.yml`` and ``build_image_aarch64.yml`` playbooks are used to build diskless images for ``x86_64`` and ``aarch64`` cluster nodes, respectively. 
Each image is created based on the functional groups defined in the 
``functional_groups_config.yml`` file. 

Alternately, to build images for aarch64 cluster nodes, perform the steps provided in :doc:`../AdvancedConfigurations/build_arm_ochami_image`.

.. caution:: Limited validation has been performed on aarch64 platform.

**Prerequisites**: 

   * Ensure that the ``functional_groups_config.yml`` file defines the functional groups required for your environment. For more information on functional groups, see :doc:`composable_roles`.
   * Make sure the ``local_repo.yml`` is executed with software packages matching the target architecture. If the build is for ``x86_64``, include software defined with ``x86_64``. If the build is for ``aarch64``, include software with ``aarch64``.
     If the build needs to support both architectures, ensure ``local_repo.yml`` is executed with ``software_config.json`` that include both ``x86_64`` and ``aarch64``.
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

2. To build the image, run the following playbook::

       ansible-playbook build_image_x86_64.yml

3. To verify that images are created for each functional group defined in ``functional_groups_config.yml``, run the following command on OIM::

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

       [admin_aarch64]
       10.0.0.1

3. To verify that images are created for each functional group defined in ``functional_groups_config.yml``, run the following command on the OIM::

       s3cmd ls -Hr s3://boot-images

   The images created for each functional group are listed in the boot-images directory.

