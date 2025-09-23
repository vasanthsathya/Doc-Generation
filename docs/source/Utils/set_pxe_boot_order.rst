Set PXE Boot Order
====================

When PXE boot order is set on a node in Omnia, the node automatically retrieves and boots into the diskless image provided by the Omnia Infrastructure Manager (OIM).

To configure PXE boot for nodes after they are discovered with the ``discovery.yml`` playbook, do the following:

1. Generate the inventory file based on the mapping file. For the sample map and inventory files, see :doc:`Sample Files <../OmniaInstallGuide/samplefiles>`.

2. Run the following playbook to configure PXE boot on the nodes using the inventory file::

      ssh omnia_core
      cd /omnia/utils
      ansible-playbook set_pxe_boot.yml -i inventory

