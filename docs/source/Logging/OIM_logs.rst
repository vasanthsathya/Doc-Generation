OIM logs
----------

.. caution:: It is not recommended to delete the below log files or the directories they reside in.

.. note::
    * Log files are rotated periodically as a storage consideration. To customize how often logs are rotated, edit the ``/etc/logrotate.conf`` file on the node.
    * If you want log files for specific playbook execution, ensure to use the ``cd`` command to move into the specific directory before executing the playbook. For example, if you want local repo logs, ensure to enter ``cd local_repo`` before executing the playbook. If the directory is not changed, all the playbook execution log files will be consolidated and provided as part of omnia logs located in ``/var/log/omnia.log``.


Omnia containers
-----------------

This table shows the status of Omnia containers running on the OIM:

+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| CONTAINER ID | IMAGE                               | COMMAND              | CREATED     | STATUS      | PORTS                                             | NAMES             |
+==============+=====================================+======================+=============+=============+===================================================+===================+
| 0e327d3addf0 | docker.io/minio/minio:latest        | server /data --co... | 6 days ago  | Up 6 days   | 0.0.0.0:9000-9001->9000-9001/tcp                  | minio-server      |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| 1439b4ba453e | docker.io/library/registry:latest   | /etc/distribution... | 6 days ago  | Up 6 days   | 0.0.0.0:5000->5000/tcp                            | registry          |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| 01c7a7eaeb7d | localhost/omnia_core:latest         |                      | 5 days ago  | Up 5 days   | 2222/tcp                                          | omnia_core        |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| 3087ca8e0324 | docker.io/bitnami/openldap:latest   | /opt/bitnami/scri... | 2 days ago  | Up 2 days   | 0.0.0.0:1389->1389/tcp, 0.0.0.0:1636->1636/tcp    | openldap          |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| bfec21c3e14a | ghcr.io/openchami/local-ca:v0.2.2   | /bin/sh -c exec /... | 2 hours ago | Up 2 hours  | 9000/tcp                                          | step-ca           |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| 577af6a7af16 | docker.io/library/postgres:11.5-alpine | postgres           | 2 hours ago | Up 2 hours | 5432/tcp                                          | postgres          |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| d267d7eee9c8 | docker.io/oryd/hydra:v2.3           | serve -c /etc/con... | 2 hours ago | Up 2 hours  |                                                   | hydra             |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| c609cf73dd4f | ghcr.io/openchami/opaal:v0.3.10     | /opaal/opaal serv... | 2 hours ago | Up 2 hours  |                                                   | opaal-idp         |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| be4dea6159f3 | ghcr.io/openchami/smd:v2.18.0       | /smd                 | 2 hours ago | Up 2 hours  | 27779/tcp                                         | smd               |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| 2aa3b79b9e1f | ghcr.io/openchami/bss:v1.32.0       | /bin/sh -c /usr/l... | 2 hours ago | Up 2 hours  | 27778/tcp                                         | bss               |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| eea83cdfaf93 | ghcr.io/openchami/opaal:v0.3.10     | /opaal/opaal logi... | 2 hours ago | Up 2 hours  |                                                   | opaal             |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| 5d32b95a8083 | ghcr.io/openchami/cloud-init:v1.2.3 | /bin/sh -c /usr/l... | 2 hours ago | Up 2 hours  |                                                   | cloud-init-server |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| 3ad8781f4d1d | cgr.dev/chainguard/haproxy:latest   | haproxy -f /usr/l... | 2 hours ago | Up 2 hours  | 0.0.0.0:8081->80/tcp, 0.0.0.0:8443->443/tcp       | haproxy           |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+
| b08dc56c006f | ghcr.io/openchami/coredhcp:v0.3.0   | /coredhcp            | 2 hours ago | Up 2 hours  |                                                   | coresmd           |
+--------------+-------------------------------------+----------------------+-------------+-------------+---------------------------------------------------+-------------------+


Logs of individual Podman containers in OIM
------------------------------------------------
   1. To view the containers running on OIM, run the following command:

     ``podman ps -a``

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

