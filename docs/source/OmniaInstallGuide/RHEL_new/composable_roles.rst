Step 2: Create composable functional groups
============================================

In Omnia, nodes are organized using **functional groups**. Functional groups provide a unified approach to managing large-scale node infrastructures, combining logical organization, physical placement, and resource optimization.

A functional group defines the role or purpose of a node within the system. Nodes are categorized based on their functionality, such as Login servers, Compilers, Kubernetes Workers (K8Worker), or SLURM Workers (SLURMWorker). Each functional group can also include a location, specifying where the node is physically placed (for example, a particular rack or Scalable Unit). This ensures both functional and physical organization are managed together.

Functional groups offered by Omnia
-------------------------------------

.. note:: 
    
    * At least one functional group is mandatory, and you must not change the name of functional groups.
    * The functional groups are case-sensitive in nature.
    * Omnia supports HA functionality for the ``service_cluster``. For more information, `click here <HighAvailability/index.html>`_.
    * To set up a service cluster, the ``service_kube_node`` must be present in the ``/opt/omnia/input/project_default/functional_groups_config.yml``.

.. csv-table:: Types of Functional Groups
   :file: ../../Tables/omnia_roles.csv
   :header-rows: 1
   :keepspace:

  
Sample
-------

Here's a sample (using mapping file) for your reference:

::
    
    functional_groups:
        - name: "default_x86_64"
          location_id: SU-1.RACK-1
          cluster_name: ""
          parent: ""

        - name: "slurm_node_x86_64"
          location_id: SU-1.RACK-2
          cluster_name: ""
          parent: ""

        - name: "slurm_control_node_x86_64"
          location_id: SU-1.RACK-1
          cluster_name: ""
          parent: ""
   



