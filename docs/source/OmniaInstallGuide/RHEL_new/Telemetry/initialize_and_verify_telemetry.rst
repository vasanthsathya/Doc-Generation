Step 15: Initialize telemetry and verify telemetry
============================================

To initiate the iDRAC telemetry service on the the service cluster, run the ``telemetry.yml`` playbook.::

    cd telemetry
    ansible-playbook telemetry.yml -i inventory

.. note:: You do not need to run ``telemetry.yml`` if the service cluster is configured only for LDMS. By default, LDMS begins collecting data after ``discovery.yml`` is executed.

Collect telemetry on external nodes
------------------------------------

To collect telemetry from the external nodes, do the following:

1. Update ``<BMC_IP>,,`` in the ``/opt/omnia/telemetry/bmc_group_data.csv``.  
   The ``GROUP_NAME`` and ``PARENT`` fields must be left blank.

2. Run the ``telemetry.yml`` playbook using the following command::

       ansible-playbook telemetry.yml

Sample::

    BMC_IP,GROUP_NAME,PARENT
    <IP Address>,,
