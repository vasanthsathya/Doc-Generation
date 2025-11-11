High Availability (HA) for the Service Kubernetes Cluster
==========================================================

Prerequisites
--------------

* Ensure that the ``local_repo.yml`` playbook has been run successfully at least once. Before running it, verify that the ``/opt/omnia/input/project_default/software_config.json`` file contains ``{"name": "service_k8s"}`` in the ``softwares`` list.

* To enable and configure the HA for Service cluster, fill up the necessary parameters in the ``high_availability_config.yml`` config file present in the ``/opt/omnia/input/project_default/`` directory.

    .. csv-table:: Parameters for Service Cluster HA
        :file: ../../../Tables/service_k8s_high_availability.csv
        :header-rows: 1
        :keepspace:

.. note:: 
  
    * Once the ``discovery.yml`` playbook has been executed, any subsequent edits to the ``high_availability_config.yml`` or ``functional_groups_config.yml`` files will not take effect. To apply changes made to these configuration files, you must re-run the ``discovery.yml`` playbook.
    * The virtual IP addresses specified in the ``high_availability_config.yml`` file must be within the same subnet as the admin network.


Sample
-------

::
    
    service_k8s_cluster_ha:
        - cluster_name: service_cluster
          enable_k8s_ha: true
          virtual_ip_address: ""
          