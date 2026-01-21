Input Parameters for Local Repositories
==========================================

The ``local_repo.yml`` playbook is dependent on the inputs provided to the following input files:

* ``/opt/omnia/input/project_default/software_config.json``
* ``/opt/omnia/input/project_default/local_repo_config.yml``

``/opt/omnia/input/project_default/software_config.json``
----------------------------------------------------------

Based on the inputs provided to the ``/opt/omnia/input/project_default/software_config.json``, the software packages/images are accessed from the Pulp container and the desired software stack is deployed on the cluster nodes.

.. csv-table:: Parameters for Software Configuration
   :file: ../../../Tables/software_config_rhel.csv
   :header-rows: 1
   :keepspace:
   :widths: auto

The following is the sample ``software_config.json`` for RHEL clusters:

::

    {
    "cluster_os_type": "rhel",
    "cluster_os_version": "10.0",
    "repo_config": "always",
    "softwares": [
        {"name": "default_packages", "arch": ["x86_64","aarch64"]},
        {"name": "openldap", "arch": ["x86_64"]},
        {"name": "nfs", "arch": ["x86_64","aarch64"]},
        {"name": "service_k8s","version": "1.31.4", "arch": ["x86_64"]},
        {"name": "slurm_custom", "arch": ["x86_64","aarch64"]}
    ],
    "slurm_custom": [
        {"name": "slurm_control_node"},
        {"name": "slurm_node"},
        {"name": "login_node"},
        {"name": "login_compiler_node"}
    ],
    "service_k8s": [
        {"name": "service_kube_control_plane"},
        {"name": "service_etcd"},
        {"name": "service_kube_node"}
    ]
    }


.. csv-table:: Architecture information for softwares
   :file: ../../../Tables/Software_arch.csv
   :header-rows: 1
   :keepspace:
   :widths: auto

.. note::

    * To download a software with both x86_64 and aarch64 architectures, the arch key input is mandatory. Ensure that you check if the .json files for all the specified architectures are available in the input or configuration file. Else, update the .json files. See the following sample:

    ::
     
        {
            "cluster_os_type": "rhel",
            "cluster_os_version": "10.0",
            "repo_config": "always",
            "softwares": [
                {"name": "default_packages", "arch": ["x86_64","aarch64"]},
                {"name": "openldap", "arch": ["x86_64","aarch64"]},
                {"name": "service_k8s","version": "1.34.1", "arch": ["x86_64"]},
                {"name": "slurm_custom", "arch": ["x86_64","aarch64"]},
                {"name": "ldms", "arch": ["x86_64","aarch64"]}
            ],
            "slurm_custom": [
                {"name": "slurm_control_node"},
                {"name": "slurm_node"},
                {"name": "login_node"},
                {"name": "login_compiler_node"}
            ],
            "service_k8s": [
                {"name": "service_kube_control_plane_first"},
                {"name": "service_kube_control_plane"},
                {"name": "service_kube_node"}
            ]

        }
        

    * For additional_software support, update the input/config/{arch}/rhel/10.0/additional_software.json file with the required {arch} data, where {arch} can either be x86_64 or aarch64, or a combination of both.

.. note::

    * For a list of accepted ``softwares``, go to the ``/opt/omnia/input/project_default/config/<cluster_os_type>/<cluster_os_version>`` and view the list of JSON files available. The filenames present in this location are the list of accepted softwares. For a cluster running RHEL 10.0, go to ``/opt/omnia/input/project_default/config/<architecture>/rhel/10.0/`` and view the file list for accepted softwares.
    * Omnia supports a single version of any software packages in the ``software_config.json`` file. Ensure that multiple versions of the same package are not mentioned.
    * For software packages that do not have a pre-defined json file in ``/opt/omnia/input/project_default/config/<architecture>/<cluster_os_type>/<cluster_os_version>``, you need to create a ``custom.json`` file with the package details.

``/opt/omnia/input/project_default/local_repo_config.yml``
-----------------------------------------------------------

.. csv-table:: Parameters for Local Repository Configuration
   :file: ../../../Tables/local_repo_config_rhel.csv
   :header-rows: 1
   :keepspace:
   :widths: auto

.. note::

    * For systems with RedHat subscription, subscription URLs override ``rhel_os_urls`` and are processed automatically by the ``local_repo.yml`` playbook.