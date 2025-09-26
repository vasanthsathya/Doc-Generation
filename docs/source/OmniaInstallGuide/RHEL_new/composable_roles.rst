Step 2: Create groups and assign functional roles to the nodes
================================================================

In Omnia, nodes are organized based on their assigned **functional groups** and **groups**. By combining both functional groups and groups, Omnia offers a powerful and flexible approach to manage large-scale node infrastructures, ensuring both logical organization and physical optimization of resources.


* A **functional group** defines what a node does in the system. It is a way to categorize nodes based on their functionality. Functional groups help group nodes that perform similar tasks, making it easier to manage and assign resources.
  For example, a node could belong to a functional group such as:

  - **Service Kube Node** 
  - **Login Node** 
  - **Login Compiler Node** 
  - **Slurm Control Node** 

 
 * A **group** is based on the physical characteristics of the nodes. It refers to nodes that are located in the same place or have similar hardware. For example, nodes in the same rack or SU (Scalable Unit) might be grouped together, with specific functional groups like **Service Kube Node** or **Slurm Control Node**. Groups help with physical organization and management of nodes.

   Both **functional groups** and **groups** must be configured in the ``functional_groups_config.yml`` input file. This file defines how nodes are organized in Omnia, including their functional roles and group assignments.


Create Functional groups
------------------

Nodes with similar functional roles or functionalities can be grouped together. The following table lists the functional groups available in Omnia.

.. note:: 
    
    * At least one functional group is mandatory, and you must not change the name of functional groups.
    * Each **group name** must be unique across all functional groups in the ``functional_groups_config.yml`` file.
    * The functional groups are case-sensitive in nature.
    * Omnia supports HA functionality for the ``service_cluster``. For more information, `click here <HighAvailability/index.html>`_.
    * To set up a service cluster, the ``service_kube_node`` must be present in the ``/opt/omnia/input/project_default/functional_groups_config.yml``.

.. csv-table:: Types of Functional Groups
   :file: ../../Tables/omnia_roles.csv
   :header-rows: 1
   :keepspace:

  
Recommended Software by functional groups
------------------------------------------

The following table lists the functional groups along with the recommended software to be deployed on each group.  
Ensure that the corresponding ``software_config.json`` file contains the required inputs for proper deployment.  
For more information, see the `Input parameters for Local Repositories <https://omnia-devel.readthedocs.io/en/latest/OmniaInstallGuide/RHEL_new/CreateLocalRepo/InputParameters.html>`_.

+----------------------------------+--------------------------------------------------------------------------------------+
| Functional Group Name            | Recommended Software                                                                 |
+==================================+======================================================================================+
| service_kube_node_x86_64         | service_k8s.json, nfs.json, openldap.json, ofed.json                                 |
+----------------------------------+--------------------------------------------------------------------------------------+
| slurm_control_node_x86_64        | slurm_custom.json, nfs.json, openldap.json, ofed.json                                |
+----------------------------------+--------------------------------------------------------------------------------------+
| slurm_node_x86_64                | slurm_custom.json, nfs.json, openldap.json, ofed.json                                |                                               
+----------------------------------+--------------------------------------------------------------------------------------+
| slurm_node_aarch64               | slurm_custom.json, nfs.json, openldap.json, ofed.json                                |
+----------------------------------+--------------------------------------------------------------------------------------+
| login_node_x86_64                | slurm_custom.json, nfs.json, openldap.json, ofed.json                                |
+----------------------------------+--------------------------------------------------------------------------------------+
| login_node_aarch64               | slurm_custom.json, nfs.json, openldap.json, ofed.json                                |
+----------------------------------+--------------------------------------------------------------------------------------+
| login_compiler_node_x86_64       | slurm_custom.json, nfs.json, openldap.json, ofed.json, ucx.json, openmpi.json        |
+----------------------------------+--------------------------------------------------------------------------------------+
| login_compiler_node_aarch64      | slurm_custom.json, nfs.json, openldap.json, ofed.json, ucx.json, openmpi.json        |                                                                               
+-------------------------------------------------------------------------------------------------------------------------+

Create Groups
----------------

Nodes that are located in the same place or similar hardware can be grouped together. To do so, update the ``functional_groups_config.yml`` input file in the ``/opt/omnia/input/project_default`` directory which includes all necessary attributes for the nodes, based on their role within the cluster. Each group will have following attributes as indicated in the table below:

.. note:: Groups associated with the ``service_kube_control_plane``, ``service_etcd``, ``service_kube_node``, and ``oim_ha_node`` roles should not be used to fulfill any other roles.

.. csv-table:: Group attributes
   :file: ../../Tables/group_attributes.csv
   :header-rows: 1
   :keepspace:


Sample
-------

Here's a sample (using mapping file) for your reference:

::

    groups:
      grp0:
        location_id: SU-1.RACK-1
        parent: ""
    
      grp1:
        location_id: SU-1.RACK-1
        parent: ""
    
    functional_groups:              
        - name: "slurm_node_x86_64"
          cluster_name: ""
          
        - name: "slurm_control_node_x86_64"
          cluster_name: ""
          
   



