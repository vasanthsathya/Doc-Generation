Set up Slurm
==============

**Prerequisites**

* Ensure that ``slurm`` entry is present in the ``softwares`` list in ``software_config.json``, as mentioned below:
  
  ::
    
    "softwares": [
                    {"name": "slurm" },
                 ]
    
    OR,

    "softwares": [
                    {"name": "custom_slurm" },
                 ]
    Ensure that you provide the ``custom_slurm.json`` by adding the user_repo_url: slurm-repo data in ``local_repo_config.yml``.

* Ensure that the following sub-group entry is also present in the ``software_config.json`` file: ::

            "slurm": [
                    {"name": "slurm_control_node"},
                    {"name": "slurm_node"},
                    {"name": "login_node"}
                ]

* Ensure to run ``local_repo.yml`` with the ``slurm`` entry present in ``software_config.json`` to download all required slurm packages.

* Once all the required parameters in `omnia_config.yml <../schedulerinputparams.html#id13>`_ are filled in, ``discovery.yml`` can be used to set up Slurm.

* ``slurm installation_type`` is configless by default. Ensure that ``slurm_share`` is set to ``true`` in `storage_config.yml <../schedulerinputparams.html#id17>`_, for one of the entries in ``nfs_client_params``.




**Install Slurm**

Run either of the following commands:

    1. ::

           cd /omnia/discovery ansible-playbook discovery.yml

    
    
