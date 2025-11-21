Re-provisioning the cluster
=============================

In the event that an existing Omnia cluster needs a fresh installation, the cluster can be re-provisioned.


Re-provision existing nodes without any modifications
------------------------------------------------------

To re-provision the existing nodes without any modifications, PXE boot the required nodes to be reprovisioned.

The OS is automatically installed on every PXE boot if there are no modification in the cluster.


Re-provision the nodes with modifications
------------------------------------------

1. Update the mapping file and ``software_config.json`` as required.
2. In the event of any modification to the ``software_config.json``, run the ``local_repo.yml`` playbook, and then run the ``build_image_x86_64.yml`` or ``build_image_aarch64.yml`` to build the new images. For more information, see :doc:`../RHEL_new/CreateLocalRepo/RunningLocalRepo`.
3. After the images are created, run the ``discovery.yml`` playbook. For more information, see :doc:`../RHEL_new/Provision/installprovisiontool`.
4. PXE boot the required nodes to be reprovisioned.
   
..Note:: The entire cluster needs to be reprovisioned, if you want to reprovision Slurm Control node and Kube Control Plane.

      





