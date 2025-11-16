================================================
Deploy LDMS Telemetry 
================================================

Using Omnia, you can deploy Lightweight Distributed Metric Service (LDMS) to collect in-band telemetry from Slurm clusters. The deployment includes installing LDMS producers on Slurm nodes, deploying LDMS aggregator and store components on Service Kubernetes nodes, and integrating LDMS with Kafka for downstream telemetry processing.

LDMS collects system metrics such as CPU, memory, network, I/O, and Slurm job statistics. LDMS includes these components:

- **LDMS producer (collector):** Collects local system metrics and runs on Slurm controller, compute, and login nodes.
- **LDMS aggregator:** Receives and aggregates metrics from producers. Runs as a Kubernetes pod.
- **LDMS store:** Buffers and stores metric batches reliably. Runs as a Kubernetes pod.
- **Kafka broker:** Handles telemetry streaming for consumption by downstream systems.


During deployment, Omnia attaches LDMS aggregator and store pods to the admin network using an ipvLAN interface created through Multus CNI. This configuration improves throughput between Slurm nodes and the Kubernetes cluster.


Steps
-------

1. Build RPM packages for LDMS producer for RHEL 10.
2. Updload LDMS aggregator and LDMS store container images in the Dell DockerHub registry.
3. Open network port for LDMS (default: ``10001``)
4. Ensure the following entries exist in the ``software_config.json``. If any entry is missing, Omnia skips LDMS deployment and logs an informational message.
   For more information, see :doc:`../OmniaInstallGuide/RHEL_new/CreateLocalRepo/InputParameters`

.. code-block:: json

   {"name": "slurm_custom", "arch": ["x86_64","aarch64"]},
   {"name": "service_k8s", "version": "1.34.1", "arch": ["x86_64"]},
   {"name": "ldms", "arch": ["x86_64", "aarch64"]}

5. In the ``local_repo_config.yml``, ensure the user repo paths defined for ``user_repo_url_x86_64`` and ``user_repo_url_aarch64`` contains the LDMS producer RPM for both ``x86_64`` and ``aarch64`` architectures. 
   For more information on creating local repo, see :doc:`../OmniaInstallGuide/RHEL_new/CreateLocalRepo/InputParameters`

6. Ensure the ``ldms.json`` file contains the following entries for both ``x86_64`` and ``aarch64`` architectures.

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


7. Ensure that the ``telemetry_config.yml`` has the entries specific LDMS and Kafka deployment.

    .. csv-table:: telemetry_config.yml
        :file: ../Tables/telemetry_config.csv
        :header-rows: 1
        :keepspace:


5. Run the ``discovery.yml`` playbook. The ``discovery.yml`` playbook peforms the following:

    - Validates LDMS and telemetry configuration.
    - Installs the LDMS producer RPM on the Slurm controller, compute nodes, and login node.
    - Deploys the LDMS aggregator pod on a Service Kubernetes worker node with ipvLAN attachment through Multus CNI.
    - Deploys the LDMS store pod on a Service Kubernetes worker node.
    - Installs or integrates with Kafka, and creates the ``ldms`` topic.


Verify LDMS telemetry generation  
====================================
Use the following steps to verify that LDMS is deployed correctly and that telemetry flows through the entire pipeline:

Producer → Aggregator → Store → Kafka

Verify LDMS producer service
--------------------------------

Verify telemetry arrives at the LDMS aggregator
--------------------------------------------------


Verify telemetry moves from aggregator to store
-------------------------------------------------

Verify telemetry is forwarded from store to Kafka
-------------------------------------------------

Verify telemetry is available in Kafka
-----------------------------------------

