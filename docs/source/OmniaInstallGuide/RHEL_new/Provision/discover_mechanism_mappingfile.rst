Create mapping file with the target node information
========================================================

Depending on the values provided in ``/opt/omnia/input/project_default/provision_config.yml``, target nodes can be discovered only using the mapping file.
Manually collect PXE NIC information for target servers and manually define them to Omnia using the **pxe_mapping_file.csv** file. Provide the file path to the ``pxe_mapping_file`` variable in ``/opt/omnia/input/project_default/provision_config.yml``. 
A sample format is shown below:

::

    FUNCTIONAL_GROUP_NAME,SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
    slurm_controller_node_x86_64,x1000c1s7b1n0,n1,xx:yy:zz:aa:bb:cc,10.5.0.101,xx:yy:zz:aa:bb:dd,10.3.0.101
    slurm_node_x86_64,x1000c1s7b1n1,n2,aa:bb:cc:dd:ee:ff,10.5.0.102,aa:bb:cc:dd:ee:gg,10.3.0.102

.. note::
    * The header fields mentioned above are case sensitive.
    * The service tags provided in the mapping file are not validated by Omnia. Ensure that correct service tags are provided. Incorrect service tags can cause unexpected failures.
    * The hostnames provided should not contain the domain name of the nodes.
    * All fields mentioned in the mapping file are mandatory.
    * The ADMIN_MAC and BMC_MAC addresses provided in ``pxe_mapping_file.csv`` should refer to the PXE NIC and BMC NIC on the target nodes respectively.
    * Target servers should be configured to boot in PXE mode with the appropriate NIC as the first boot device.


+---------------------------------------------------------+------------------------------------------------------+
| Pros                                                    | Cons                                                 |
+=========================================================+======================================================+
| Easily customizable if the user maintains a list of     | The user needs to be aware of the MAC/IP mapping     |
| MAC addresses.                                          | required in the network.                             |
+---------------------------------------------------------+------------------------------------------------------+
|                                                         | Servers require a manual PXE boot if iDRAC IPs are   |
|                                                         | not configured.                                      |
+---------------------------------------------------------+------------------------------------------------------+

