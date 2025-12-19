===============
OIM Cleanup
===============

The ``oim_cleanup.yml`` playbook can be utilized to roll back any configurations made on the OIM. 

Tasks performed by the playbook
================================

The ``oim_cleanup.yml`` playbook performs the following tasks:

* Clean up all containers, log files, and metadata on the OIM node.
* Rollback the firewall ports on the OIM node to its default setting.

Playbook Execution
=====================

Use the below command to execute the playbook: ::

    ssh omnia_core
    cd /omnia/utils
    ansible-playbook oim_cleanup.yml


.. note:: After running the ``oim_cleanup.yml`` playbook, ensure to reboot the OIM node. The ``oim_cleanup.yml`` playbook does not remove data stored under the NFS ``server_share_path``. Using the same ``server_share_path`` may cause deployment failures, or inconsistent Kubernetes and Slurm behavior after redeployment. For a fresh deployment, you must manually clean the contents of ``server_share_path`` or use a new NFS export/path. NFS ``server_share_path`` is available in ``storage_config.yml``.

.. caution::
    * After a clean-up, when re-provisioning your cluster by re-running the ``discovery.yml`` playbook, ensure to use a different ``admin_nic_subnet`` in ``input/provision_config.yml`` to avoid a conflict with newly assigned servers. Alternatively, disable any OS available in the ``Boot Option Enable/Disable`` section of your BIOS settings (``BIOS Settings`` > ``Boot Settings`` > ``UEFI Boot Settings``) on all target nodes.
    * On subsequent runs of ``discovery.yml``, if users are unable to log into the server, refresh the ssh key manually and retry. ::

        ssh-keygen -R <node IP>