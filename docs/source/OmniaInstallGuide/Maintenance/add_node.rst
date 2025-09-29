Add node to the cluster
==========================

Omnia supports new nodes to the cluster. To add the new node, perform the following steps:

Add the node to the cluster without any new functional groups
--------------------------------------------------------------------------------------------

1. Update the mapping file with the new entries. Note: Ensure not to remove the existing nodes from the mapping file.
2. Run the discovery.yml plabook to discover the new nodes.
3. PXE boot the newly added nodes.


Add the node to the cluster with new functional groups
-------------------------------------------------------------

1. Update the functional_group_config.yml with the new functional groups and update the software_config.json as required.
2. Run the local_repo.yml playbook if any update in the software_config.json. For more information, see <link to the local repo>.
3. Run the build_image_x86_64.yml / build_image_aarch64.yml to build the new images. For more information, see <build new images>
4. After the images are created, run the discovery.yml playbook. For more information <see discover topic>.
5. PXE boot the newly added nodes.