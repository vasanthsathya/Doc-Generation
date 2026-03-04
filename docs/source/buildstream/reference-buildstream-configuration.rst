.. _reference-buildstream-configuration:

BuildStreaM Configuration Reference
===================================

Complete reference for all BuildStreaM configuration parameters, their accepted values, defaults, and interdependencies. This reference helps administrators configure BuildStreaM for their specific HPC infrastructure requirements.

.. contents:: On This Page
   :local:
   :depth: 2

Configuration Overview
---------------------

BuildStreaM configuration is managed through the main `omnia.yml` configuration file. BuildStreaM-specific parameters are defined under the `buildstream` section of this file.

**Configuration File Location**

   .. code-block:: bash

      /opt/omnia/config/omnia.yml

**Configuration Structure**

   .. code-block:: yaml

      # Main Omnia configuration
      omnia:
        # ... other Omnia configuration ...
      
      # BuildStreaM configuration
      buildstream:
        enabled: true
        # ... BuildStreaM-specific parameters ...

Core Configuration Parameters
------------------------------

### enabled

   **Description**: Enable or disable BuildStreaM functionality
   
   **Type**: Boolean
   
   **Default**: `false`
   
   **Required**: Yes
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        enabled: true

   **Notes**:
   * When set to `false`, BuildStreaM containers and services will not be started
   * Must be set to `true` for all BuildStreaM functionality
   * Requires restart of Omnia services to take effect

### api

   **Description**: API server configuration for BuildStreaM
   
   **Type**: Object
   
   **Required**: Yes
   
   **Parameters**:

#### base_uri

   **Description**: Base URI for BuildStreaM API endpoints
   
   **Type**: String
   
   **Default**: `"https://localhost:8080/api/v1"`
   
   **Required**: Yes
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        api:
          base_uri: "https://buildstream.company.com/api/v1"

   **Validation**:
   * Must be a valid HTTPS URL
   * Hostname must resolve to BuildStreaM API server
   * Port must be accessible from GitLab runners

#### port

   **Description**: Port number for BuildStreaM API server
   
   **Type**: Integer
   
   **Default**: `8080`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        api:
          port: 9090

   **Validation**:
   * Must be between 1024 and 65535
   * Port must not conflict with other services
   * Firewall must allow traffic on specified port

#### timeout

   **Description**: API request timeout in seconds
   
   **Type**: Integer
   
   **Default**: `300`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        api:
          timeout: 600

   **Validation**:
   * Must be between 30 and 3600 seconds
   * Longer timeouts may be needed for complex operations

GitLab Integration Parameters
------------------------------

### gitlab

   **Description**: GitLab server integration configuration
   
   **Type**: Object
   
   **Required**: Yes
   
   **Parameters**:

#### host

   **Description**: GitLab server IP address or hostname
   
   **Type**: String
   
   **Default**: None
   
   **Required**: Yes
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        gitlab:
          host: "192.168.1.100"

   **Validation**:
   * Must be a valid IP address or hostname
   * Must be accessible from BuildStreaM API server
   * GitLab API must be available on the specified host

#### project_name

   **Description**: Name of the GitLab project for BuildStreaM
   
   **Type**: String
   
   **Default**: `"omnia-buildstream"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        gitlab:
          project_name: "company-hpc-buildstream"

   **Validation**:
   * Must follow GitLab project naming conventions
   * Cannot contain special characters other than hyphens and underscores
   * Must be unique within the GitLab instance

#### visibility

   **Description**: GitLab project visibility level
   
   **Type**: String
   
   **Default**: `"private"`
   
   **Required**: No
   
   **Accepted Values**:
   * `"private"`: Project accessible only to authorized users
   * `"public"`: Project accessible to all users
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        gitlab:
          visibility: "public"

   **Notes**:
   * Public projects expose catalog definitions to all users
   * Private projects require authentication for access
   * Consider security requirements when choosing visibility

#### main_branch

   **Description**: Default branch name for the GitLab project
   
   **Type**: String
   
   **Default**: `"main"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        gitlab:
          main_branch: "master"

   **Validation**:
   * Must follow Git branch naming conventions
   * Cannot contain spaces or special characters
   * Must exist in the GitLab repository

#### access_token

   **Description**: GitLab personal access token for API access
   
   **Type**: String
   
   **Default**: None
   
   **Required**: Yes
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        gitlab:
          access_token: "glpat-xxxxxxxxxxxxxxxxxxxx"

   **Security Notes**:
   * Token must have `api` scope
   * Token should have minimal required permissions
   * Store token securely and rotate regularly
   * Never commit tokens to version control

.. AI_REVIEW: Access token management process - verify against GitLab security best practices

Admission Control Parameters
-----------------------------

### admission_control

   **Description**: Resource management and concurrency control
   
   **Type**: Object
   
   **Required**: No
   
   **Parameters**:

#### max_concurrent_builds

   **Description**: Maximum number of concurrent build jobs
   
   **Type**: Integer
   
   **Default**: `1`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        admission_control:
          max_concurrent_builds: 2

   **Validation**:
   * Must be between 1 and 10
   * Higher values require more system resources
   * Consider infrastructure capacity when setting this value

#### max_parallel_validations

   **Description**: Maximum number of parallel validation jobs
   
   **Type**: Integer
   
   **Default**: `1`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        admission_control:
          max_parallel_validations: 3

   **Validation**:
   * Must be between 1 and 5
   * Validation jobs are typically resource-intensive
   * Monitor system resource utilization

#### job_timeout

   **Description**: Default timeout for jobs in minutes
   
   **Type**: Integer
   
   **Default**: `120`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        admission_control:
          job_timeout: 240

   **Validation**:
   * Must be between 30 and 1440 minutes
   * Longer timeouts may be needed for complex builds
   * Consider typical job duration when setting this value

Database Configuration Parameters
---------------------------------

### database

   **Description**: PostgreSQL database configuration for BuildStreaM
   
   **Type**: Object
   
   **Required**: No
   
   **Parameters**:

#### host

   **Description**: PostgreSQL server hostname or IP address
   
   **Type**: String
   
   **Default**: `"localhost"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        database:
          host: "postgres-buildstream.company.com"

   **Validation**:
   * Must be accessible from BuildStreaM containers
   * PostgreSQL server must accept connections from BuildStreaM

#### port

   **Description**: PostgreSQL server port
   
   **Type**: Integer
   
   **Default**: `5432`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        database:
          port: 5433

   **Validation**:
   * Must be between 1024 and 65535
   * Must match PostgreSQL server configuration

#### database_name

   **Description**: Name of the BuildStreaM database
   
   **Type**: String
   
   **Default**: `"buildstream"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        database:
          database_name: "omnia_buildstream"

   **Validation**:
   * Must follow PostgreSQL database naming conventions
   * Database must exist and be accessible
   * User must have required permissions

#### username

   **Description**: Database username for BuildStreaM
   
   **Type**: String
   
   **Default**: `"buildstream"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        database:
          username: "omnia_buildstream"

   **Validation**:
   * User must exist in PostgreSQL
   * User must have required database permissions
   * Use strong, unique passwords

#### password

   **Description**: Database password for BuildStreaM
   
   **Type**: String
   
   **Default**: None
   
   **Required**: Yes
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        database:
          password: "[SECURE_PASSWORD]"

   **Security Notes**:
   * Use strong, complex passwords
   * Store password securely
   * Rotate passwords regularly
   * Never commit passwords to version control

Logging Configuration Parameters
-------------------------------

### logging

   **Description**: Logging and monitoring configuration
   
   **Type**: Object
   
   **Required**: No
   
   **Parameters**:

#### level

   **Description**: Logging level for BuildStreaM services
   
   **Type**: String
   
   **Default**: `"info"`
   
   **Required**: No
   
   **Accepted Values**:
   * `"debug"`: Detailed debugging information
   * `"info"`: General information messages
   * `"warn"`: Warning messages
   * `"error"`: Error messages only
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        logging:
          level: "debug"

   **Notes**:
   * Debug logging may impact performance
   * Use info level for production environments
   * Error level may miss important operational information

#### log_file

   **Description**: Path to BuildStreaM log file
   
   **Type**: String
   
   **Default**: `"/var/log/omnia/buildstream.log"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        logging:
          log_file: "/var/log/omnia/buildstream-debug.log"

   **Validation**:
   * Directory must exist and be writable
   * Sufficient disk space must be available
   * Log rotation should be configured for long-running systems

#### max_log_size

   **Description**: Maximum log file size in MB
   
   **Type**: Integer
   
   **Default**: `100`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        logging:
          max_log_size: 500

   **Validation**:
   * Must be between 10 and 1000 MB
   * Larger values require more disk space
   * Consider log retention policies

Security Configuration Parameters
---------------------------------

### security

   **Description**: Security and authentication configuration
   
   **Type**: Object
   
   **Required**: No
   
   **Parameters**:

#### tls_enabled

   **Description**: Enable TLS encryption for API communication
   
   **Type**: Boolean
   
   **Default**: `true`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        security:
          tls_enabled: true

   **Notes**:
   * TLS should always be enabled in production
   * Disable only for development or testing
   * Requires valid TLS certificates

#### cert_file

   **Description**: Path to TLS certificate file
   
   **Type**: String
   
   **Default**: `"/etc/ssl/certs/omnia-buildstream.crt"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        security:
          cert_file: "/etc/ssl/certs/company-buildstream.crt"

   **Validation**:
   * Certificate file must exist and be readable
   * Certificate must be valid and not expired
   * Certificate must match the server hostname

#### key_file

   **Description**: Path to TLS private key file
   
   **Type**: String
   
   **Default**: `"/etc/ssl/private/omnia-buildstream.key"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        security:
          key_file: "/etc/ssl/private/company-buildstream.key"

   **Security Notes**:
   * Private key file must have restricted permissions (600)
   * Store private key securely
   * Use strong encryption for private key

#### ca_file

   **Description**: Path to CA certificate file for client verification
   
   **Type**: String
   
   **Default**: `"/etc/ssl/certs/ca-bundle.crt"`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        security:
          ca_file: "/etc/ssl/certs/company-ca-bundle.crt"

   **Validation**:
   * CA file must contain valid certificates
   * Client certificates must be signed by included CA
   * Regularly update CA certificates

Performance Configuration Parameters
-----------------------------------

### performance

   **Description**: Performance tuning parameters
   
   **Type**: Object
   
   **Required**: No
   
   **Parameters**:

#### worker_threads

   **Description**: Number of worker threads for API processing
   
   **Type**: Integer
   
   **Default**: `4`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        performance:
          worker_threads: 8

   **Validation**:
   * Must be between 1 and 16
   * Consider CPU cores when setting this value
   * Monitor system resource utilization

#### cache_size

   **Description**: Cache size for frequently accessed data in MB
   
   **Type**: Integer
   
   **Default**: `512`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        performance:
          cache_size: 1024

   **Validation**:
   * Must be between 128 and 4096 MB
   * Larger values require more memory
   * Monitor memory usage and adjust as needed

#### connection_pool_size

   **Description**: Database connection pool size
   
   **Type**: Integer
   
   **Default**: `10`
   
   **Required**: No
   
   **Example**:
   
   .. code-block:: yaml

      buildstream:
        performance:
          connection_pool_size: 20

   **Validation**:
   * Must be between 5 and 50
   * Consider database server capacity
   * Monitor database connection usage

Complete Configuration Example
--------------------------------

Here is a complete BuildStreaM configuration example:

.. code-block:: yaml

   buildstream:
     enabled: true
     
     api:
       base_uri: "https://buildstream.company.com/api/v1"
       port: 8080
       timeout: 600
     
     gitlab:
       host: "gitlab.company.com"
       project_name: "company-hpc-buildstream"
       visibility: "private"
       main_branch: "main"
       access_token: "[GITLAB_ACCESS_TOKEN]"
     
     admission_control:
       max_concurrent_builds: 2
       max_parallel_validations: 3
       job_timeout: 240
     
     database:
       host: "postgres-buildstream.company.com"
       port: 5432
       database_name: "omnia_buildstream"
       username: "omnia_buildstream"
       password: "[DATABASE_PASSWORD]"
     
     logging:
       level: "info"
       log_file: "/var/log/omnia/buildstream.log"
       max_log_size: 500
     
     security:
       tls_enabled: true
       cert_file: "/etc/ssl/certs/company-buildstream.crt"
       key_file: "/etc/ssl/private/company-buildstream.key"
       ca_file: "/etc/ssl/certs/company-ca-bundle.crt"
     
     performance:
       worker_threads: 8
       cache_size: 1024
       connection_pool_size: 20

Configuration Validation
-----------------------

Validate your BuildStreaM configuration before applying:

.. code-block:: bash

   # Validate configuration syntax
   python -c "import yaml; yaml.safe_load(open('/opt/omnia/config/omnia.yml'))"
   
   # Test BuildStreaM configuration
   python scripts/validate_buildstream_config.py /opt/omnia/config/omnia.yml

Expected output for valid configuration:

.. code-block:: text

   ✓ Configuration syntax is valid
   ✓ All required parameters are present
   ✓ Parameter values are within valid ranges
   ✓ Network connectivity to GitLab verified
   ✓ Database connection successful
   ✓ TLS certificates are valid

.. AI_REVIEW: Configuration validation script referenced - verify actual script availability and validation checks

Configuration Troubleshooting
-----------------------------

**Common Configuration Issues**

**GitLab Connection Failures**

   Symptoms: Pipeline fails with GitLab connection errors
   
   Solutions:
   * Verify GitLab host accessibility
   * Check GitLab access token validity
   * Validate GitLab API permissions

**Database Connection Issues**

   Symptoms: BuildStreaM fails to start or connect to database
   
   Solutions:
   * Verify database server is running
   * Check database connection parameters
   * Validate database user permissions

**TLS Certificate Problems**

   Symptoms: HTTPS connections fail with certificate errors
   
   Solutions:
   * Verify certificate file paths and permissions
   * Check certificate validity and expiration
   * Ensure certificate matches server hostname

**Performance Issues**

   Symptoms: Slow API response times or timeouts
   
   Solutions:
   * Adjust worker threads and connection pool size
   * Monitor system resource utilization
   * Optimize cache size and configuration

Related Topics
--------------

* :doc:`how-to-buildstream-enabling-buildstream`
* :doc:`concepts-buildstream-architecture`
* :doc:`overview-buildstream`
