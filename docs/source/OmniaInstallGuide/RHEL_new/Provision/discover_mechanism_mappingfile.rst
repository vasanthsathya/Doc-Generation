Create mapping file with the target node information
========================================================

Depending on the values provided in ``/opt/omnia/input/project_default/provision_config.yml``, target nodes can be discovered only using the mapping file.
Manually collect PXE NIC information for target servers and manually define them to Omnia using the **pxe_mapping_file.csv** file. Provide the file path to the ``pxe_mapping_file`` variable in ``/opt/omnia/input/project_default/provision_config.yml``. 
A sample format is shown below:

::

    FUNCTIONAL_GROUP_NAME,GROUP_NAME,SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
    slurm_control_node_x86_64,grp0,ABCD12,slurm-control-node1,xx:yy:zz:aa:bb:cc,172.16.107.52,xx:yy:zz:aa:bb:dd,172.17.107.52
    slurm_node_x86_64,grp1,ABCD34,slurm-node1,aa:bb:cc:dd:ee:ff,172.16.107.43,aa:bb:cc:dd:ee:gg,172.17.107.43
    slurm_node_x86_64,grp1,ABFG34,slurm-node2,aa:bb:cc:dd:ee:ff,172.16.107.44,aa:bb:cc:dd:ff:gg,172.17.107.44
    login_compiler_node_x86_64,grp8,ABCD78,login-compiler-node1,aa:bb:cc:dd:ee:gg,172.16.107.41,aa:bb:cc:dd:ee:bb,172.17.107.41
    login_compiler_node_x86_64,grp8,ABFG78,login-compiler-node2,aa:bb:cc:dd:ee:gg,172.16.107.42,aa:bb:cc:dd:ee:bb,172.17.107.42
    service_kube_control_plane_first_x86_64,grp3,ABFG79,service-kube-control-plane1,aa:bb:cc:dd:ee:ff,172.16.107.53,xx:yy:zz:aa:bb:ff,172.17.107.53
    service_kube_control_plane_x86_64,grp4,ABFH78,service-kube-control-plane2,aa:bb:cc:dd:ee:hh,172.16.107.54,xx:yy:zz:aa:bb:hh,172.17.107.54
    service_kube_control_plane_x86_64,grp4,ABFH80,service-kube-control-plane3,aa:bb:cc:dd:ee:ii,172.16.107.55,xx:yy:zz:aa:bb:ii,172.17.107.55
    service_kube_node_x86_64,grp5,ABFL82,service-kube-node1,aa:bb:cc:dd:ee:jj,172.16.107.56,xx:yy:zz:aa:bb:jj,172.17.107.56
    service_kube_node_x86_64,grp5,ABKD88,service-kube-node2,aa:bb:cc:dd:ee:kk,172.16.107.57,xx:yy:zz:aa:bb:ff,172.17.107.57

.. note::
    * The header fields mentioned above are case sensitive.
    * The IP address provided in the mapping file are not validated by Omnia. Ensure that the correct IP addresses are provided. Incorrect IP address can cause unexpected failures.
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

