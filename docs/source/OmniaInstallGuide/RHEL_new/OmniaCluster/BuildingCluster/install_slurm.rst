Set up Slurm
==============

**Prerequisites**

* Ensure that ``slurm`` entry is present in the ``softwares`` list in ``software_config.json``, as mentioned below:
  
  ::

    "softwares": [
                    {"name": "slurm_custom", "arch": ["x86_64","aarch64"]},
                 ]
    
Ensure that you provide the ``slurm_custom.json`` by adding the ``user_repo_url: slurm-repo data`` in ``local_repo_config.yml``.

* Ensure that the following sub-group entry is also present in the ``software_config.json`` file: ::

            "slurm": [
                    {"name": "slurm_control_node"},
                    {"name": "slurm_node"},
                    {"name": "login_node"}
                ]

* Ensure to run ``local_repo.yml`` with the ``slurm_custom`` entry present in ``software_config.json`` to download all required slurm packages.

* Once all the required parameters in `omnia_config.yml <../schedulerinputparams.html#id13>`_ are filled in, ``discovery.yml`` can be used to set up Slurm.

* ``slurm installation_type`` is configless by default. Ensure that ``nfs_client_params`` are filled in ``storage_config.yml`` before running the ``discovery.yml`` playbook to deploy Slurm.




**Install Slurm**

Run the following command:

     ::

           cd /omnia/discovery
           ansible-playbook discovery.yml

    
    
