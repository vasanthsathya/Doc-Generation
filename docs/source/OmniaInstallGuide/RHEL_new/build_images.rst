Step 8: Build cluster node images
============================

The ``build_image.yml`` playbook is used to build diskless images for cluster nodes. 
Each image is created based on the functional groups defined in the 
``functional_groups_config.yml`` file. 

**Prerequisites**: 

   * Ensure that the ``functional_groups_config.yml`` file defines the functional groups required for your environment. For more information on functional groups, see :doc:`composable_roles`.
   * Ensure that the local_repo.yml playbook is run and the images are downloaded into the Pulp container.
   * Ensure the ISO provided has downloaded seamlessly (No corruption). Verify the SHA checksum or download size of the ISO file before provisioning to avoid failures. 
   * Ensure that OIMs running RHEL have an active subscription or are configured to access local repositories.
   * Note the compatibility between cluster OS and OIM OS below:

        +---------------------+--------------------+------------------+
        |                     |                    |                  |
        | OIM OS              | Cluster  Node OS   | Compatibility    |
        +=====================+====================+==================+
        |                     |                    |                  |
        | RHEL                | RHEL               | Yes              |
        +---------------------+--------------------+------------------+
   
To build images for the nodes present in each functional group, do the following.

1. Navigate to the image build directory::

       cd /omnia/build_image

2. To build the image, run the following playbook::

       ansible-playbook build_image.yml

3. To verify that images are created for each functional group defined in ``functional_groups_config.yml``, run the following command::

       s3cmd ls -Hr s3://boot-images

   The images created for each functional group are listed in the boot-images directory.