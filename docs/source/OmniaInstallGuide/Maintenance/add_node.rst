Add node to the cluster
==========================

Omnia supports adding new nodes to the cluster. 

Add node to the cluster without any new functional groups
----------------------------------------------------------

1. Update the mapping file with the new entries. 

.. Note:: While updating the mapping file, ensure that the existing nodes are not removed from the mapping file.

2. Run the ``discovery.yml`` plabook to discover the new nodes.

3. PXE boot the newly added nodes.


Add node to the cluster with new functional groups
--------------------------------------------------------

1. Update the ``functional_groups_config.yml`` with the new functional groups and update the ``software_config.json`` as required.

2. Run the ``local_repo.yml`` playbook if there are any update made to the ``software_config.json``. For more information, see :doc:`../RHEL_new/CreateLocalRepo/RunningLocalRepo`.
3. Run the ``build_image_x86_64.yml`` or ``build_image_aarch64.yml`` to build new images. For more information, see :doc:`../RHEL_new/build_images`.
4. After the images are created, run the discovery.yml playbook. For more information, see :doc:`../RHEL_new/Provision/installprovisiontool`.
5. PXE boot the newly added nodes.