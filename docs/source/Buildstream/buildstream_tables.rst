BuildStreaM Configuration Tables
==================================

This section contains the configuration tables referenced throughout the BuildStreaM documentation.

.. _buildstream-tables-buildstream-configuration:

BuildStreaM Configuration
--------------------------

.. csv-table:: build_stream_config.yml
   :file: ../Tables/build_stream_config.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-high-availability-configuration:

High Availability Configuration
-------------------------------

.. csv-table:: high_availability_config.yml
   :file: ../Tables/service_k8s_high_availability.csv
   :header-rows: 1
   :keepspace:

.. _buildstream-tables-local-repository-configuration:

Local Repository Configuration
------------------------------

.. csv-table:: local_repo_config.yml
   :file: ../Tables/local_repo_config_rhel.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-network-configuration:

Network Configuration
---------------------

.. csv-table:: network_spec.yml
   :file: ../Tables/network_spec.csv
   :header-rows: 1
   :keepspace:

.. _buildstream-tables-oma-configuration:

Omnia Configuration
-------------------

.. csv-table:: omnia_config.yml
   :file: ../Tables/omnia_config_service_cluster.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-provisioning-configuration:

Provisioning Configuration
--------------------------

.. csv-table:: provision_config.yml
   :file: ../Tables/Provision_config.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-security-configuration:

Security Configuration
----------------------

.. csv-table:: security_config.yml
   :file: ../Tables/security_config.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-storage-configuration:

Storage Configuration
---------------------

.. csv-table:: storage_config.yml
   :file: ../Tables/storage_config.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-telemetry-configuration:

Telemetry Configuration
-----------------------

.. csv-table:: telemetry_config.yml
   :file: ../Tables/telemetry_config.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-gitlab-configuration:

GitLab Configuration
--------------------

.. csv-table:: gitlab_config.yml
   :file: ../Tables/build_stream_gitlab_config.csv
   :header-rows: 1
   :keepspace:


.. _buildstream-tables-release2-oauth-configuration:

BuildStreaM OAuth 2.0 Configuration
----------------------------------------------

The following table describes the OAuth 2.0 configuration parameters added in BuildStreaM . These parameters are configured in the ``software_config.json`` file under the ``omnia_auth`` section.

.. list-table:: OAuth 2.0 Configuration Parameters
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - ``oauth_enabled``
     - Enable or disable OAuth 2.0 authentication for BuildStream API access. Set to ``true`` to enable OAuth, ``false`` to use legacy authentication.
     - ``false``
   * - ``oauth_client_id``
     - OAuth 2.0 client identifier registered with the Omnia Auth service. This client ID is used to obtain JWT access tokens for API authentication.
     - ``buildstream-client``
   * - ``oauth_client_secret``
     - OAuth 2.0 client secret corresponding to the client ID. This secret is used to authenticate the client when requesting access tokens.
     - (generated during setup)
   * - ``oauth_token_url``
     - URL endpoint for obtaining OAuth 2.0 access tokens. Typically points to the Omnia Auth service token endpoint.
     - ``https://<oim_host>:8443/oauth/token``
   * - ``oauth_scope``
     - OAuth 2.0 token scope defining the permissions granted to the access token. Valid scopes include ``buildstream:read`` and ``buildstream:write``.
     - ``buildstream:read buildstream:write``
   * - ``oauth_token_expiry``
     - Access token expiry time in seconds. After this time, the token must be refreshed.
     - ``3600``


.. _buildstream-tables-release2-storage-backend-configuration:

BuildStreaM Storage Backend Configuration
--------------------------------------------------

BuildStreaM supports multiple storage backends for build artifacts. The following table describes the storage backend selection parameters configured in ``build_stream_config.yml``.

.. list-table:: Storage Backend Configuration Parameters
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - ``storage_backend``
     - Storage backend type for BuildStream artifacts. Valid values: ``nfs`` (Network File System) or ``powerscale`` (Dell PowerScale).
     - ``nfs``
   * - ``nfs_server``
     - NFS server hostname or IP address (required when ``storage_backend`` is ``nfs``).
     - (required)
   * - ``nfs_export_path``
     - NFS export path for BuildStream artifacts (required when ``storage_backend`` is ``nfs``).
     - ``/omnia/buildstream``
   * - ``powerscale_host``
     - Dell PowerScale host address (required when ``storage_backend`` is ``powerscale``).
     - (required)
   * - ``powerscale_port``
     - Dell PowerScale port number for API access (required when ``storage_backend`` is ``powerscale``).
     - ``8080``
   * - ``powerscale_access_zone``
     - PowerScale access zone for BuildStream artifacts (required when ``storage_backend`` is ``powerscale``).
     - ``System``
   * - ``powerscale_username``
     - PowerScale username for authentication (required when ``storage_backend`` is ``powerscale``).
     - (required)
   * - ``powerscale_password``
     - PowerScale password for authentication (required when ``storage_backend`` is ``powerscale``).
     - (required)


.. _buildstream-tables-release2-automation-framework-configuration:

BuildStreaM Automation Framework Configuration
---------------------------------------------------------

BuildStreaM includes an automation framework based on Molecule for validating Ansible playbooks. The following table describes the automation framework configuration parameters.

.. list-table:: Automation Framework Configuration Parameters
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - ``automation_framework_enabled``
     - Enable or disable the automation framework for Ansible playbook validation. Set to ``true`` to enable Molecule-based testing.
     - ``false``
   * - ``molecule_driver``
     - Molecule driver type for test environment provisioning. Valid values: ``podman`` (Podman containers) or ``docker`` (Docker containers).
     - ``podman``
   * - ``molecule_platform``
     - Target platform for Molecule tests. Valid values: ``rhel``, ``ubuntu``, or ``centos``.
     - ``rhel``
   * - ``molecule_test_scenario``
     - Molecule test scenario to execute. Scenarios define the test sequence and validation steps.
     - ``default``
   * - ``validation_timeout``
     - Timeout in seconds for Molecule test execution. If validation exceeds this time, the test is marked as failed.
     - ``1800``


.. _buildstream-tables-release2-pipeline-configuration:

BuildStreaM Pipeline Configuration
---------------------------------------------

The following table describes the pipeline configuration parameters added in BuildStreaM for the three-pipeline architecture.

.. list-table:: Pipeline Configuration Parameters
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - ``pipeline_architecture``
     - Pipeline architecture type. Valid values: ``multi`` (parent + child pipelines).
     - ``multi``
   * - ``parent_pipeline_timeout``
     - Timeout in seconds for parent pipeline execution. If the parent pipeline exceeds this time, it is terminated.
     - ``600``
   * - ``child_pipeline_timeout``
     - Timeout in seconds for child pipeline execution. If a child pipeline exceeds this time, it is terminated.
     - ``3600``
   * - ``parallel_build_enabled``
     - Enable parallel execution of independent image builds within the BUILD pipeline.
     - ``true``
   * - ``max_parallel_builds``
     - Maximum number of parallel build jobs to execute simultaneously.
     - ``4``
   * - ``retry_on_failure``
     - Enable automatic retry of failed pipeline stages. If ``true``, failed stages are retried according to the retry policy.
     - ``true``
   * - ``max_retry_attempts``
     - Maximum number of retry attempts for failed pipeline stages.
     - ``3``:
