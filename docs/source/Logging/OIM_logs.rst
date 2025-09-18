OIM logs
----------

.. caution:: It is not recommended to delete the below log files or the directories they reside in.

.. note::
    * Log files are rotated periodically as a storage consideration. To customize how often logs are rotated, edit the ``/etc/logrotate.conf`` file on the node.
    * If you want log files for specific playbook execution, ensure to use the ``cd`` command to move into the specific directory before executing the playbook. For example, if you want local repo logs, ensure to enter ``cd local_repo`` before executing the playbook. If the directory is not changed, all the playbook execution log files will be consolidated and provided as part of omnia logs located in ``/var/log/omnia.log``.

Logs of individual Podman containers in OIM
------------------------------------------------
   1. To view the containers running on the OIM, run the following command:

     ``podman ps -a``
   2. To view the logs from a specific container, run the following command:

     ``podman logs <container name>``

Logs of individual K8s containers on service cluster
-----------------------------------------------------
   1. A list of namespaces and their corresponding pods can be obtained using:
      ``kubectl get pods -A``
   2. Get a list of containers for the pod in question using:
      ``kubectl get pods <pod_name> -o jsonpath='{.spec.containers[*].name}'``
   3. Once you have the namespace, pod and container names, run the below command to get the required logs:
      ``kubectl logs pod <pod_name> -n <namespace> -c <container_name>``

