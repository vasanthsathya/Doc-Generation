================================================
Configure deployment required for LDMS Telemetry 
================================================

Using Omnia, you can deploy Lightweight Distributed Metric Service (LDMS) to collect in-band telemetry from Slurm clusters. The deployment includes installing LDMS producers on Slurm nodes, deploying LDMS aggregator and store components on Service Kubernetes nodes, and integrating LDMS with Kafka for downstream telemetry processing.

LDMS collects system metrics such as CPU, memory, network, I/O, and Slurm job statistics. LDMS includes these components:

- **LDMS producer (collector):** Collects local system metrics and runs on Slurm controller, compute, and login nodes.
- **LDMS aggregator:** Receives and aggregates metrics from producers. Runs as a Kubernetes pod.
- **LDMS store:** Buffers and stores metric batches reliably. Runs as a Kubernetes pod.
- **Kafka broker:** Handles telemetry streaming for consumption by downstream systems..

For more details on LDMS, see `Lightweight Distributed Metric Service <https://github.com/ovis-hpc/ldms>`_


During deployment, Omnia attaches LDMS aggregator and store pods to the admin network using an ipvLAN interface created through Multus CNI. This configuration improves throughput between Slurm nodes and the Kubernetes cluster.

Prerequisites
---------------

* If the internet connection is required on the service Kube node, configure it after the node is booted. 
* All service cluster nodes should have access to the Internet.
* Ensure that ``discovery.yml`` playbook has been executed successfully with ``service_kube_node`` and ``service_kube_node`` in the mapping file.

Steps
-------

1. Build RPM packages for LDMS producer for RHEL 10.
2. Specify the following entries in the ``software_config.json``. If any entry is missing, Omnia skips LDMS deployment and logs an informational message.
For more information, see :doc:`../OmniaInstallGuide/RHEL_new/CreateLocalRepo/InputParameters`

docs\source\OmniaInstallGuide\RHEL_new\CreateLocalRepo\InputParameters.rst

.. code-block:: json

    {"name": "slurm_custom", "arch": ["x86_64","aarch64"]},
    {"name": "service_k8s", "version": "1.34.1", "arch": ["x86_64"]},
    {"name": "ldms", "arch": ["x86_64", "aarch64"]}

3. Ensure the ``ldms.json`` file contains the following entries. 

The following ``ldms.json`` sample is for ``x86_64``. For ``aarch64`` architecture, update the repo name accordingly in the ``ldms.json`` file.

.. code-block:: json

    {
        "ldms": {
            "cluster": [
                {"package": "python3-devel", "type": "rpm", "repo_name": "x86_64_appstream"},
                {"package": "python3-cython", "type": "rpm", "repo_name": "x86_64_appstream"},
                {"package": "openssl-libs", "type": "rpm", "repo_name": "x86_64_baseos"},
                {"package": "ovis-ldms", "type": "rpm", "repo_name": "x86_64_ldms"}
            ]
        }
    }
    
4. In ``local_repo_config.yml``, specify the paths for the ``ovis-ldms`` RPMs accordingly for the ``user_repo_url_x86_64`` and ``user_repo_url_aarch64``.

5. Fill up the ``omnia_config.yml``:

    .. csv-table:: omnia_config.yml
        :file: ../../../Tables/omnia_config_service_cluster.csv
        :header-rows: 1
        :keepspace: 

6. Ensure that the ``telemetry_config.yml`` has the entries specific for LDMS and Kafka deployment.

    .. csv-table:: telemetry_config.yml
        :file: ../../../Tables/telemetry_config.csv
        :header-rows: 1
        :keepspace: