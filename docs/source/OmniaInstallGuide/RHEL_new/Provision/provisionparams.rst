Update the input parameters for discovering the nodes
========================================================

Fill in all required parameters in ``/opt/omnia/input/project_default/provision_config.yml``, ``/opt/omnia/input/project_default/omnia_config_credentials.yml``, ``/opt/omnia/input/project_default/software_config.json``, and ``/opt/omnia/input/project_default/network_spec.yml``.

.. caution:: Do not remove or comment any lines in the above mentioned ``.yml`` files.

.. csv-table:: provision_config.yml
   :file: ../../../Tables/Provision_config.csv
   :header-rows: 1
   :keepspace:

.. [1] Boolean parameters do not need to be passed with double or single quotes.

.. note::

    The ``/opt/omnia/input/project_default/omnia_config_credentials.yml`` file is encrypted on the first execution of the ``discovery_provision.yml`` or ``local_repo.yml`` playbooks.

      * To view the encrypted parameters: ::

          ansible-vault view omnia_config_credentials.yml --vault-password-file .omnia_config_credentials_key

      * To edit the encrypted parameters: ::

          ansible-vault edit omnia_config_credentials.yml --vault-password-file .omnia_config_credentials_key


.. csv-table:: software_config.json
   :file: ../../../Tables/software_config_rhel.csv
   :header-rows: 1
   :keepspace:


.. csv-table:: network_spec.yml
   :file: ../../../Tables/network_spec.csv
   :header-rows: 1
   :keepspace:


.. caution::
    * All provided network ranges and NIC IP addresses should be distinct with no overlap in the ``/opt/omnia/input/project_default/network_spec.yml``.
    * Ensure that all the iDRACs are reachable from the OIM.

A sample of the ``/opt/omnia/input/project_default/network_spec.yml`` where nodes are discovered using a mapping file is provided below: ::

    ---
         Networks:
         - admin_network:
            oim_nic_name: "eno1"
            netmask_bits: "16"
            primary_oim_admin_ip: "10.5.255.254"
            primary_oim_bmc_ip: ""
            dynamic_range: "10.5.1.1-10.5.1.200"