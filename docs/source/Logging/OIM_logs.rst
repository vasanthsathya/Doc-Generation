OIM logs
----------

.. caution:: It is not recommended to delete the below log files or the directories they reside in.

.. note:: If you want log files for specific playbook execution, ensure to use the ``cd`` command to move into the specific directory before executing the playbook. For example, if you want local repo logs, ensure to enter ``cd local_repo`` before executing the playbook. If the directory is not changed, all the playbook execution log files will be consolidated and provided as part of omnia logs located in ``/opt/omnia/log/core/playbooks``.

   
Omnia Logs
-----------

The following table provides an overview of the various Omnia log files, their locations, and their purposes for monitoring.

+------------------------------------------------------------------------+---------------------------------------------+
| Location                                                               | Purpose                                     |
+========================================================================+=============================================+
| /opt/omnia/log/core/playbooks/discovery.log                            | Discovery logs                              |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/local_repo.log                           | Local Repository logs                       |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/prepare_oim.log                          | Prepare OIM Logs                            |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/provision.log                            | Provision Logs                              |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/scheduler.log                            | Scheduler Logs                              |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/telemetry.log                            | Telemetry logs                              |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/utils.log                                | Utility logs                                |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/credential_utility.log                   | Credential utility logs                     |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/openchami/*log                                          | OpenCHAMI playbook logs                     |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/pulp/*log                                               | Pulp container logs                         |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/local_repo/*log                                         | Local repo logs                             |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/container/*log                                     | Core container logs                         |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/validation_omnia_project_default.log     | Omnia input validation report logs          |
+------------------------------------------------------------------------+---------------------------------------------+
| /opt/omnia/log/core/playbooks/input_validation.log                     | Omnia input validation playbook logs        |
+------------------------------------------------------------------------+---------------------------------------------+


Logs of individual Podman containers in OIM
------------------------------------------------
   1. To view the containers running on OIM, run the following command:

     ``podman ps -a``

      The following table shows the status of Omnia containers running on the OIM:

       .. csv-table:: Podman Logs
        :file: ../Tables/podman_logs.csv
        :header-rows: 1
        :keepspace:

   2. To view the logs from a specific container, run the following command:

     ``podman logs <container name>``
     
   3. Alternatively, if the container is managed as a systemd service, you can view the logs using the following command:

     ``journalctl -xeu <container name>``


Logs of individual K8s containers on service cluster
-----------------------------------------------------
   1. A list of namespaces and their corresponding pods can be obtained using:

      ``kubectl get pods -A``

   2. Get a list of containers for the pod in question using:

      ``kubectl get pods <pod_name> -o jsonpath='{.spec.containers[*].name}'``

   3. Once you have the namespace, pod and container names, run the below command to get the required logs:

      ``kubectl logs pod <pod_name> -n <namespace> -c <container_name>``

