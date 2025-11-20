Step 15: Initialize telemetry and verify telemetry
==================================================

Prerequisites
---------------

* Ensure that ``discovery.yml`` playbook has been executed successfully with ``service_kube_control_plane`` and ``service_kube_node`` in the mapping file.

Steps
------

To initiate the iDRAC telemetry service on the the service cluster, run the ``telemetry.yml`` playbook.::

    cd telemetry
    ansible-playbook telemetry.yml 

.. note::
   Metadata automatically captures the Kubernetes Control Plane Virtual IP (KUBE CP VIP).
   As a result, the ``telemetry.yml`` playbook is executed against the VIP rather than an
   individual control plane node.

.. note:: You do not need to run ``telemetry.yml`` if the service cluster is configured only for LDMS. By default, LDMS begins collecting data after ``discovery.yml`` is executed.

Collect telemetry on external nodes
------------------------------------

To collect telemetry from the external nodes, do the following:

1. Update the BMC IP of the external nodes in the ``/opt/omnia/telemetry/bmc_group_data.csv``.  
   The ``GROUP_NAME`` and ``PARENT`` fields must be left blank.

2. Run the ``telemetry.yml`` playbook using the following command::

       ansible-playbook telemetry.yml

Sample::

    BMC_IP,GROUP_NAME,PARENT
    <IP Address>,,
