Discover the cluster nodes
============================

The ``discovery.yml`` playbook discovers the probable bare-metal cluster nodes. This playbook is dependent on inputs from the following input files:

* ``/opt/omnia/input/project_default/provision_config.yml``
* ``/opt/omnia/input/project_default/functional_groups_config.yml``
* ``/opt/omnia/input/project_default/network_spec.yml``

.. note:: The first PXE device on target nodes should be the designated active NIC for PXE booting.

    .. image:: ../../../images/BMC_PXE_Settings.png
        :width: 600px

Configurations made by the ``discovery.yml`` playbook
-----------------------------------------------------------------

* Discovers all target servers.
* Configures the boot script based on the functional groups.
* Configures the cloud-init based on the functional groups.


Playbook execution
----------------------

To deploy the Omnia provision tool, execute the following commands: ::

    ssh omnia_core
    cd /omnia/discovery
    ansible-playbook discovery.yml

.. note::

    * If the ``/opt/omnia/input/project_default/software_config.json`` has OFED and NVIDIA CUDA drivers mentioned, the OFED network drivers and NVIDIA accelerator drivers are installed on the nodes post provisioning.

    * After executing ``discovery.yml`` playbook, you can check the log files available at ``/opt/omnia/log`` for more information.

    * Ansible playbooks by default run concurrently on 5 nodes. To change this, update the ``forks`` value in ``ansible.cfg`` present in the respective playbook directory.

    * While the ``admin_nic`` on cluster nodes is configured by Omnia to be static, the public NIC IP address should be configured by user.

    * All ports required by OpenCHAMI will be opened (For a complete list, see :doc:`Omnia Ports <omnia_ports>`).

    * After running ``discovery.yml``, the file ``/opt/omnia/input/project_default/omnia_config_credentials.yml`` will be encrypted. To edit the file, use the command: ``ansible-vault edit omnia_config_credentials.yml --vault-password-file .omnia_config_credentials_key``

    * Post execution of ``discovery.yml``, IPs/hostnames cannot be re-assigned by changing the mapping file.

.. caution::

    * To avoid breaking the password-less SSH channel on the OIM, do not run ``ssh-keygen`` commands post execution of ``discovery.yml`` to create a new key.

    * Do not delete the Omnia shared path or the NFS directory.

**Next steps**:

* After successfully running the ``discovery.yml`` playbook, you can either manually PXE boot the nodes or use the ``set_pxe_boot.yml`` playbook. PXE booting allows the nodes to load diskless images from the Omnia Infrastructure Manager (OIM). For detailed steps on using ``set_pxe_boot.yml``, see :doc:`Set PXE Boot Order <../docs/source/OmniaInstallGuide/samplefiles.rst>`.
* Execute ``telemetry.yml`` to start the telmetry collection.