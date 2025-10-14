Configuring specific local repositories
-----------------------------------------

**NFS**

    To install NFS, include the following line under ``softwares`` in ``software_config.json``: ::

            {"name": "nfs", "arch": ["x86_64","aarch64"]},

    For information on deploying NFS after setting up the cluster, `click here <../OmniaCluster/BuildingCluster/Storage/NFS.html>`_.

**Kubernetes**

    To install Kubernetes, include the following line under ``softwares`` in ``software_config.json``: ::

            {"name": "service_k8s", "version":"1.31.4", "arch": ["x86_64"]},

    For more information about installing Kubernetes, `click here <../OmniaCluster/BuildingCluster/install_kubernetes.html>`_.

.. note:: The version of ``service_k8s`` provided above is the only version of the package that Omnia supports.

**Slurm**

    To install Slurm, include the following line under ``softwares`` in ``software_config.json``: ::

            {"name": "slurm_custom", "arch": ["x86_64","aarch64"]},

    For more information about installing Slurm, `click here <../OmniaCluster/BuildingCluster/install_slurm.html>`_.

.. note:: If ``slurm_custom`` is defined in ``software_config.json``, provide the corresponding repository information in the ``user_repo_url_<arch>`` field of ``local_repo-config.yml``.


**OpenLDAP**

    To install OpenLDAP, include the following line under ``softwares`` in ``software_config.json``: ::

            {"name": "openldap","arch": ["x86_64"]},

    For more information on OpenLDAP, `click here <../OmniaCluster/BuildingCluster/Authentication.html#configuring-freeipa-openldap-security>`_.


**OpenMPI**

    To install OpenMPI, include the following line under ``softwares`` in ``software_config.json``: ::

            {"name": "openmpi", "version":"5.0.8","arch": ["x86_64"]},

    OpenMPI is deployed on the cluster when the above configurations are complete and `omnia.yml <../OmniaCluster/BuildingCluster/installscheduler.html>`_ playbook is executed.

    For more information on OpenMPI configurations, `click here <../../AdvancedConfigurations/install_ucx_openmpi.html>`_.

.. note:: The default OpenMPI version for Omnia is 4.1.6. If you change the version in the ``software_config.json`` file, make sure to update it in the ``openmpi.json`` file in the ``config`` directory as well.


**Unified Communication X**

    To install UCX, include the following line under ``softwares`` in ``software_config.json``: ::

            {"name": "ucx", "version":"1.19.0", "arch": ["x86_64"]},

    UCX is deployed on the cluster when ``local_repo.yml`` playbook is executed, followed by the execution of `omnia.yml <../OmniaCluster/BuildingCluster/installscheduler.html>`_.

    For more information on UCX configurations, `click here <../../AdvancedConfigurations/install_ucx_openmpi.html>`_.



**Custom packages**

    Include the following line under ``softwares`` in ``software_config.json``: ::

                {"name": "additional_software"},

    Create an ``additional_software.json`` file in the following directory: ``/opt/omnia/input/project_default/config/<arch>/<cluster_os_type>/<cluster_os_version>`` and add your choice of additional software. For a cluster running RHEL 10.0, go to ``/opt/omnia/input/project_default/congig/<arch>/rhel/10.0/`` and create the file there. For more information, `click here <../../../Utils/software_update.html>`_.
