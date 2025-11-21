Step 2: Create mapping file with node information
===================================================

In Omnia, nodes are discovered and provisioned based on the  **groups** and **functional groups** defined in the mapping file. By combining both groups and functional groups, Omnia offers a powerful and flexible approach to manage large-scale node infrastructures, ensuring both logical organization and physical optimization of resources.


* A **group** is based on the physical characteristics of the nodes. It refers to nodes that are located in the same place or have similar hardware. For example, nodes in the same rack or SU (Scalable Unit) might be grouped together, with specific functional groups like **Service Kube Node** or **Slurm Control Node**. Groups help with physical organization and management of nodes.

   
* A **functional group** defines what a node does in the system. It is a way to categorize nodes based on their functionality. Functional groups help group nodes that perform similar tasks, making it easier to manage and assign resources.
  For example, a node could belong to a functional group such as:

  - **Service Kube Control Plane** 
  - **Service Kube Node** 
  - **Login Node** 
  - **Login Compiler Node** 
  - **Slurm Control Node** 
  - **Slurm Node**


Create mapping file
-----------------------
Manually collect PXE NIC information of the nodes to be provisioned and manually define them to Omnia using the **pxe_mapping_file.csv** file. Provide the file path to the ``pxe_mapping_file`` variable in ``/opt/omnia/input/project_default/provision_config.yml``.
Each node listed in the mapping file must be assigned with the following values: 
``FUNCTIONAL_GROUP_NAME``, ``GROUP_NAME``, ``SERVICE_TAG``, ``PARENT_SERVICE_TAG``, ``HOSTNAME``, ``ADMIN_MAC``, 
``ADMIN_IP``, ``BMC_MAC``, and ``BMC_IP``.

Refer to the `Group Attributes`_ table to assign the appropriate ``GROUP_NAME`` and the 
`Types of Functional Groups`_ table to assign the correct ``FUNCTIONAL_GROUP_NAME`` 
for each node in the mapping file.

.. _Group Attributes: ../../Tables/group_attributes.csv
.. _Types of Functional Groups: ../../Tables/omnia_roles.csv



The following is the sample format of a mapping file.:: 

Example::

    FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,PARENT_SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
    slurm_control_node_x86_64,grp0,ABCD12,,slurm-control-node1,xx:yy:zz:aa:bb:cc,172.16.107.52,xx:yy:zz:aa:bb:dd,172.17.107.52
    slurm_node_x86_64,grp1,ABCD34,ABFL82,slurm-node1,aa:bb:cc:dd:ee:ff,172.16.107.43,aa:bb:cc:dd:ee:gg,172.17.107.43
    slurm_node_x86_64,grp1,ABFG34,ABKD88,slurm-node2,aa:bb:cc:dd:ee:ff,172.16.107.44,aa:bb:cc:dd:ff:gg,172.17.107.44
    login_compiler_node_x86_64,grp8,ABCD78,,login-compiler-node1,aa:bb:cc:dd:ee:gg,172.16.107.41,aa:bb:cc:dd:ee:bb,172.17.107.41
    login_compiler_node_x86_64,grp8,ABFG78,,login-compiler-node2,aa:bb:cc:dd:ee:gg,172.16.107.42,aa:bb:cc:dd:ee:bb,172.17.107.42
    service_kube_control_plane_x86_64,grp3,ABFG79,,service-kube-control-plane1,aa:bb:cc:dd:ee:ff,172.16.107.53,xx:yy:zz:aa:bb:ff,172.17.107.53
    service_kube_control_plane_x86_64,grp4,ABFH78,,service-kube-control-plane2,aa:bb:cc:dd:ee:hh,172.16.107.54,xx:yy:zz:aa:bb:hh,172.17.107.54
    service_kube_control_plane_x86_64,grp4,ABFH80,,service-kube-control-plane3,aa:bb:cc:dd:ee:ii,172.16.107.55,xx:yy:zz:aa:bb:ii,172.17.107.55
    service_kube_node_x86_64,grp5,ABFL82,,service-kube-node1,aa:bb:cc:dd:ee:jj,172.16.107.56,xx:yy:zz:aa:bb:jj,172.17.107.56
    service_kube_node_x86_64,grp5,ABKD88,,service-kube-node2,aa:bb:cc:dd:ee:kk,172.16.107.57,xx:yy:zz:aa:bb:ff,172.17.107.57


.. note::
    * The header fields mentioned above are case sensitive.
    * The IP address provided in the mapping file are not validated by Omnia. Ensure that the correct IP addresses are provided. Incorrect IP address can cause unexpected failures.
    * The service tags provided in the mapping file are not validated by Omnia. Ensure that correct service tags are provided. Incorrect service tags can cause unexpected failures.
    * The hostnames provided should not contain the domain name of the nodes.
    * All fields mentioned in the mapping file are mandatory.
    * The ADMIN_MAC and BMC_MAC addresses provided in ``pxe_mapping_file.csv`` should refer to the PXE NIC and BMC NIC on the target nodes respectively.
    * Target servers should be configured to boot in PXE mode with the appropriate NIC as the first boot device.


Groups
------

Nodes that are located in the same place or similar hardware can be grouped together. To do so, update the mapping file with all necessary attributes for the nodes, based on their role within the cluster. Each group will have following attributes as indicated in the table below:


.. csv-table:: Group attributes
   :file: ../../Tables/group_attributes.csv
   :header-rows: 1
   :keepspace:


Functional groups
------------------------

Nodes with similar functional roles or functionalities can be grouped together. The following table lists the functional groups available in Omnia.

.. note:: 
    
    * At least one functional group is mandatory, and you must not change the name of functional groups.
    * Ensure that the group nodes intended for a specific role must be associated with the corresponding functional group and must not be associated under multiple functional groups.
    * The functional groups are case-sensitive.
    * Omnia supports HA functionality for the ``service_cluster``. For more information, `click here <HighAvailability/index.html>`_.
    * To set up a service cluster, the ``service_kube_node`` must be present in the mapping file.

.. csv-table:: Types of Functional Groups
   :file: ../../Tables/omnia_roles.csv
   :header-rows: 1
   :keepspace:

  
Recommended Software by functional groups
------------------------------------------

.. caution:: Ensure that the ``software_config.json`` file contains all required inputs for the software to be deployed on each functional group.  For more information, see `Input parameters for Local Repositories <https://omnia-devel.readthedocs.io/en/latest/OmniaInstallGuide/RHEL_new/CreateLocalRepo/InputParameters.html>`_.

The following table lists the functional groups along with the recommended software to be deployed on each group.  

+-----------------------------------------+--------------------------------------------------------------------------------------+
| Functional Group Name                   | Recommended Software                                                                 |
+=========================================+======================================================================================+
| service_kube_control_plane_first_x86_64 | service_k8s.json and nfs.json                                                        |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| service_kube_control_plane_x86_64       | service_k8s.json and nfs.json                                                        |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| service_kube_node_x86_64                | service_k8s.json, nfs.json                                                           |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| slurm_control_node_x86_64               | slurm_custom.json, nfs.json, openldap.json, ldms.json                                |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| slurm_node_x86_64                       | slurm_custom.json, nfs.json, openldap.json, ldms.json                                |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| slurm_node_aarch64                      | slurm_custom.json, nfs.json, openldap.json, ldms.json                                |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| login_node_x86_64                       | slurm_custom.json, nfs.json, openldap.json, ldms.json                                |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| login_node_aarch64                      | slurm_custom.json, nfs.json, openldap.json, ldms.json                                |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| login_compiler_node_x86_64              | slurm_custom.json, nfs.json, openldap.json, ucx.json, openmpi.json, ldms.json        |
+-----------------------------------------+--------------------------------------------------------------------------------------+
| login_compiler_node_aarch64             | slurm_custom.json, nfs.json, openldap.json, ucx.json, openmpi.json, ldms.json        |
+-----------------------------------------+--------------------------------------------------------------------------------------+




   



