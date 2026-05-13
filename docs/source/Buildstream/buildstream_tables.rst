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


.. _buildstream-tables-oauth-configuration:

BuildStreaM OAuth 2.0 Configuration
----------------------------------------------

The following table describes the OAuth 2.0 configuration parameters configured in the ``software_config.json`` file under the ``omnia_auth`` section.

.. list-table:: OAuth 2.0 Configuration Parameters
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - ``oauth_enabled``
     - Enable or disable OAuth 2.0 authentication for BuildStreaM API access. Set to ``true`` to enable OAuth, ``false`` to use legacy authentication.
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
