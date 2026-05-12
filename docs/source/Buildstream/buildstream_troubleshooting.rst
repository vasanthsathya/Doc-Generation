Troubleshooting BuildStreaM Pipeline Issues
===============================================

This section provides troubleshooting guidance for common BuildStreaM pipeline issues.

Stage: Health Check
-------------------

**Issue**: Health Check stage is failing.

**Possible Cause**: This issue indicates one of the following problems:
- GitLab target IP and host IP of the BuildStream API server should be reachable from each other.
- BuildStream containers are not running properly.

**Resolution**:

1. Ensure the GitLab target IP and BuildStream API server are in the same subnet.

2. Verify that the ``omnia_build_stream`` container and the ``omnia_postgres`` and ``playbook_watcher`` services are running on the OIM node. To check the status of the containers, run the following command:
 
   .. code-block:: bash
   
      systemctl status omnia_build_stream.service
      systemctl status omnia_postgres.service
      systemctl status playbook_watcher.service

3. If there are failures in any of the containers, capture and verify the logs from journalctl using the following command:
   
   .. code-block:: bash
   
      journalctl -u omnia_build_stream --no-pager
      journalctl -u omnia_postgres --no-pager

Stage: API Registration
-----------------------

**Issue**: API-Registration stage is failing.

**Possible Cause**: This issue indicates one of the following problems:
- Maximum client limit reached for BuildStreaM API server registration.
- Other API registration errors.

.. note:: Currently, only one client can be registered with the BuildStreaM API server.

**Resolution**:

1. If you encounter the ``max_clients_limit_reached`` error, do the following:
   - Either run the pipeline from the already registered client.
   - Or perform the ``gitlab_cleanup`` and reconfigure GitLab using the playbook.

2. For other non-successful API responses, on the Omnia Infrastructure Manager (OIM), check the authentication logs at ``/<nfs-dir>/omnia/log/build_stream/auth.log`` for detailed error information.

Stage: Token Generation
-----------------------

**Issue**: Token-Generation stage is failing.

**Possible Cause**: This issue indicates one of the following problems:
- Token generation failed due to authentication issues.
- Token generation failed due to network issues.

**Resolution**:

On the OIM, check the authentication logs at ``/<nfs-dir>/omnia/log/build_stream/auth.log`` for detailed error information.

Stage: Parse Catalog
--------------------

**Issue**: Parse-Catalog stage is failing.

**Possible Cause**: This issue indicates one of the following problems:
- Invalid JSON schema format.
- The ``catalog_rhel.json`` structure does not match the expected catalog schema.

**Resolution**:

* Ensure the JSON is aligned with the schema as shown in the reference examples available at:
   - https://github.com/dell/omnia/tree/pub/build_stream/examples/catalog

* If the issue persists, on the OIM, check the job-specific logs at ``/<nfs-dir>/omnia/log/build_stream/<job-id>/<jobid>.log``


Stage: Create Local Repo
------------------------

**Issue**: Create-Local-Repo stage is failing.

**Possible Cause**: This issue indicates one of the following problems:
- Playbook execution failed.
- Configuration issues in ``local_repo_config.yml``.

**Resolution**:

1.  If there are issues with playbook execution, the log path is available from the API response. Check the logs at the path specified in the ``log_file_path`` field.
   
    **Example API response format**:

        .. code-block:: json
        
            {
                "stage_name": "create-local-repository",
                "stage_state": "FAILED",
                "started_at": "2026-03-11T10:07:58.906785+00:00Z",
                "ended_at": "2026-03-11T10:49:20.639894+00:00Z",
                "error_code": "PLAYBOOK_EXECUTION_FAILED",
                "error_summary": "Playbook exited with code 2",
                "log_file_path": "/nfs/omnia/log/build_stream/5a4f69f4-44df-42eb-b88b-1583ea2610a8/local_repo.yml_20260311_171630.log"
            }

2. Verify the configuration settings in ``local_repo_config.yml``.

3. After fixing the configuration issues, re-run the pipeline.

Stage: Build Images
-------------------

**Issue**: Build Images stage is failing.

**Possible Cause**: This issue indicates one of the following problems:
- Playbook execution failed.
- Catalog does not have predefined functional groups.

**Resolution**:

1. Ensure the catalog has the predefined functional groups. For the supported functional groups, see :ref:`functional-groups-section`.

2. If changes are required in the catalog, make the necessary modifications to the catalog.

3. After fixing catalog issues, re-run the pipeline.

Stage: Deploy Images
--------------------

**Issue**: Deploy Images stage is failing.

**Possible Cause**: This issue indicates one of the following problems:
- Playbook execution failed.
- The functional groups listed in the PXE mapping file do not adhere to functional groups in the ``catalog_rhel.json``.

**Resolution**:

1. Check the log path from the API response for detailed error information.

2. Ensure the functional groups listed in the PXE mapping file matches the functional groups defined in the ``catalog_rhel.json``.

3. After making necessary modifications to the PXE mapping, re-run the pipeline manually.


BuildStreaM Troubleshooting
============================

This section covers BuildStreaM-specific issues including OAuth authentication, storage backend selection, pipeline architecture, and resume and retry functionality.

OAuth Authentication Issues
---------------------------

**Issue**: OAuth token generation fails with ``invalid_client`` or ``invalid_grant`` error.

**Possible Cause**: This issue indicates one of the following problems:
- OAuth client credentials (client_id or client_secret) are incorrect or expired
- OAuth client is not registered with the Omnia Auth service
- Token endpoint URL is misconfigured or unreachable

**Resolution**:

1. Verify OAuth client credentials in ``software_config.json``:

   .. code-block:: bash

      cat /opt/omnia/input/project_default/software_config.json | grep -A 10 omnia_auth

2. Check that the ``omnia_auth`` service is running on the OIM node:

   .. code-block:: bash

      systemctl status omnia_auth.service

3. Verify the OAuth token endpoint URL is accessible from the GitLab node:

   .. code-block:: bash

      curl -k https://<oim_host>:8443/oauth/token

4. Check OAuth service logs for detailed error information:

   .. code-block:: bash

      journalctl -u omnia_auth --no-pager

**Issue**: Pipeline fails with ``insufficient_scope`` error when accessing BuildStream API.

**Possible Cause**: OAuth token does not have the required scopes (``buildstream:read`` or ``buildstream:write``).

**Resolution**:

1. Verify the ``oauth_scope`` parameter in the catalog metadata includes the required scopes.

2. Re-register the OAuth client with the correct scopes in the Omnia Auth service configuration.

3. Generate a new token with the correct scopes and retry the pipeline.


Storage Backend Issues
----------------------

**Issue**: Pipeline fails with ``nfs_mount_failed`` error when using NFS storage backend.

**Possible Cause**: This issue indicates one of the following problems:
- NFS server is unreachable from the OIM node
- NFS export path is incorrect or not exported
- Network firewall is blocking NFS traffic (ports 2049, 111)

**Resolution**:

1. Verify NFS server connectivity from the OIM node:

   .. code-block:: bash

      ping <nfs_server>
      showmount -e <nfs_server>

2. Check NFS server configuration and ensure the export path is exported:

   .. code-block:: bash

      exportfs -v

3. Verify NFS storage backend configuration in ``build_stream_config.yml``:

   .. code-block:: bash

      cat /opt/omnia/input/project_default/build_stream_config.yml | grep -A 5 storage_backend

4. Check firewall rules and ensure NFS ports are open.

**Issue**: Pipeline fails with ``powerscale_connection_failed`` error when using PowerScale storage backend.

**Possible Cause**: This issue indicates one of the following problems:
- PowerScale host is unreachable from the OIM node
- PowerScale API port (default 8080) is blocked by firewall
- PowerScale credentials are incorrect or expired
- Access zone does not exist or user lacks permissions

**Resolution**:

1. Verify PowerScale host connectivity from the OIM node:

   .. code-block:: bash

      ping <powerscale_host>
      telnet <powerscale_host> 8080

2. Check PowerScale storage backend configuration in ``build_stream_config.yml``:

   .. code-block:: bash

      cat /opt/omnia/input/project_default/build_stream_config.yml | grep -A 10 powerscale

3. Verify PowerScale credentials and access zone configuration:

   .. code-block:: bash

      isi auth users list

4. Check PowerScale API logs for authentication and access errors.


Pipeline Architecture Issues
-----------------------------

**Issue**: Parent pipeline fails to trigger child pipeline with ``child_pipeline_generation_failed`` error.

**Possible Cause**: This issue indicates one of the following problems:
- ``pipeline_type`` parameter is missing or invalid in catalog metadata
- Child pipeline template file (``build-pipeline.yml``, ``deploy-pipeline.yml``, or ``cleanup-pipeline.yml``) is missing or misconfigured
- GitLab CI/CD configuration does not allow dynamic child pipeline generation

**Resolution**:

1. Verify the catalog metadata includes the ``pipeline_type`` parameter:

   .. code-block:: json

      {
        "metadata": {
          "pipeline_type": "build"
        }
      }

2. Check that the child pipeline template files exist in the GitLab project repository.

3. Verify GitLab CI/CD settings allow dynamic child pipelines (Settings → CI/CD → Dynamic child pipelines).

4. Check parent pipeline logs for detailed error information:

   .. code-block:: bash

      # In GitLab web interface, navigate to the parent pipeline job logs
      # Look for errors in the "trigger-child-pipeline" stage

**Issue**: Child pipeline fails with ``timeout_exceeded`` error.

**Possible Cause**: Child pipeline execution exceeded the configured timeout (default 3600 seconds).

**Resolution**:

1. Increase the ``child_pipeline_timeout`` parameter in ``build_stream_config.yml`` if the pipeline legitimately requires more time.

2. Check for stuck or hanging jobs in the child pipeline that may be causing the timeout.

3. Review pipeline logs to identify the stage that is taking longer than expected.


Resume and Retry Issues
-----------------------

**Issue**: Resume operation fails with ``resume_state_not_found`` error.

**Possible Cause**: This issue indicates one of the following problems:
- Pipeline execution state was not persisted to the database
- Resume operation is attempted for a pipeline that completed successfully
- Resume operation is attempted for a pipeline that was not interrupted

**Resolution**:

1. Verify the pipeline execution state in the BuildStream database:

   .. code-block:: bash

      # Access PostgreSQL database
      psql -U postgres -d buildstream_db
      SELECT * FROM pipeline_states WHERE pipeline_id = '<pipeline_id>';

2. Check that the pipeline is in an interrupted or failed state before attempting resume.

3. Verify the ``resume_enabled`` parameter is set to ``true`` in ``build_stream_config.yml``.

**Issue**: Retry operation fails with ``max_retry_attempts_exceeded`` error.

**Possible Cause**: The number of retry attempts has exceeded the configured maximum (default 3).

**Resolution**:

1. Check the retry count for the failed stage in the pipeline execution logs.

2. If more retries are needed, increase the ``max_retry_attempts`` parameter in ``build_stream_config.yml``.

3. Investigate the root cause of the persistent failures before increasing retry limits.

**Issue**: Resume operation succeeds but pipeline fails at a different stage.

**Possible Cause**: This issue indicates one of the following problems:
- Pipeline state corruption during the interruption
- Dependency issues between stages that were not handled correctly
- Resource availability changed between the original execution and resume

**Resolution**:

1. Review the pipeline execution logs to identify the new failure point.

2. Check that all required resources (storage, network, services) are available after resume.

3. If the issue persists, consider running a fresh pipeline execution instead of resuming.