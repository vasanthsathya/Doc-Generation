===============
OIM cleanup
===============

The ``oim_cleanup.yml`` playbook can be utilized to roll back any configurations made on the OIM. 

Tasks performed by the playbook
================================

The ``oim_cleanup.yml`` playbook performs the following tasks:

* Clean up all containers, log files, and metadata on the OIM node.
* Rollback the firewall ports on the OIM node to its default setting.

Playbook execution
=====================

Use the below command to execute the playbook: ::

    ssh omnia_core
    cd /omnia/utils
    ansible-playbook oim_cleanup.yml


.. note:: After running the ``oim_cleanup.yml`` playbook, ensure to reboot the OIM node.

.. caution::
    * After a clean-up, reprovision your cluster by performing the following.  Alternatively, disable any OS available in the ``Boot Option Enable/Disable`` section of your BIOS settings (``BIOS Settings`` > ``Boot Settings`` > ``UEFI Boot Settings``) on all target nodes.
      
        * To delete the omnia container, click `Step 1 <https://omnia-devel.readthedocs.io/en/latest/OmniaInstallGuide/RHEL_new/omnia_startup.html>`_.
        * To retain the existing omnia container, click `Step 2 <https://omnia-devel.readthedocs.io/en/latest/OmniaInstallGuide/RHEL_new/composable_roles.html>`_.
     
    * On subsequent runs of ``discovery.yml``, if users are unable to log into the server, refresh the ssh key manually and retry. ::

        ssh-keygen -R <node IP>
>