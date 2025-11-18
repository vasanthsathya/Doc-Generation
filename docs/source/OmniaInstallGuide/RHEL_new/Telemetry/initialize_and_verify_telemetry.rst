Step 14: Initialize telemetry and verify telemetry
============================================

To initiate the iDRAC telemetry service on the the service cluster, run the ``telemetry.yml`` playbook.::

    cd telemetry
    ansible-playbook telemetry.yml -i inventory

.. note:: You do not need to run ``telemetry.yml`` if the service cluster is configured only for LDMS. By default, LDMS begins collecting data after ``discovery.yml`` is executed.

Collect telemetry on external nodes
------------------------------------

To collect telemetry from the external nodes, do the following:
1. Open the ``bmc_group_data.csv`` available at the location ``/opt/omnia/telemetry/``.
2. Add the BMC IP address for the external nodes from which you need to collect telemetry. Use the following format ``<BMC_IP>,,``. The group name and parent name must be left blank.
3. Run the ``telemetry.yml`` playbook.

Sample::

    BMC_IP, GROUP_NAME, PARENT
    <IP ADRESS>,,