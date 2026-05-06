# BuildStreaM Issues

Issues related to the BuildStreaM catalog-driven CI/CD deployment workflow, including GitLab pipelines, container registry operations, catalog parsing, and OAuth credentials.

## GitLab pipeline failures

A BuildStreaM pipeline in GitLab fails with a red status indicator. The pipeline log shows errors in one or more stages (build, deploy, test).

 * The GitLab Runner is not registered or is offline.
 * Pipeline variables (credentials, URLs) are missing or incorrect.
 * The runner does not have network access to the OIM or cluster nodes.
 * A previous pipeline left stale state that conflicts with the current run.

 1. Check the pipeline log in GitLab:

 2. Navigate to **CI/CD > Pipelines** in the BuildStreaM project.

 3. Click the failed pipeline, then click the failed job to see its log.

 4. Verify the GitLab Runner is registered and online:

 gitlab-runner list
 gitlab-runner verify

 1. Check pipeline variables:

 2. Navigate to **Settings > CI/CD > Variables** in the GitLab project.

 3. Verify all required variables are set (OIM IP, credentials, registry URL).

 4. Test network connectivity from the runner to the OIM:

 # From the GitLab Runner host
 ping <oim_ip>
 ssh root@<oim_ip> hostname

 1. If stale state is the issue, clean up and retry:

 # Clear the runner's build cache
 gitlab-runner clear-cache

 # Retry the pipeline from GitLab UI

## Registry push failures

The BuildStreaM pipeline fails during the image push stage with errors such as:

 Error: failed to push image: authentication required
 Error: failed to push image: denied: requested access to the resource is denied

 * Container registry credentials are incorrect or expired.
 * The registry URL in the pipeline configuration is wrong.
 * The registry's TLS certificate is not trusted by the runner.
 * The registry storage is full.

 1. Verify registry credentials:

 podman login <registry_url>

 1. Check that the registry URL matches the pipeline configuration:

 grep -i registry .gitlab-ci.yml

 1. If TLS is the issue, add the registry's CA certificate:

 cp <registry_ca.crt> /etc/pki/ca-trust/source/anchors/
 update-ca-trust

Or configure Podman to trust the registry:

 # /etc/containers/registries.conf.d/buildstream.conf
 [[registry]]
 location = "<registry_url>"
 insecure = true # Not recommended for production

 1. Check registry storage:

 df -h <registry_data_dir>

## Catalog parse errors

The BuildStreaM pipeline fails during the catalog parsing stage with errors such as:

 Error: Failed to parse catalog: invalid YAML syntax at line 42
 Error: Unknown component type 'slurm_cluser' in catalog entry

 * The catalog YAML file has syntax errors (indentation, missing colons, invalid characters).
 * A catalog entry references a component type that does not exist (typo).
 * Required fields are missing from a catalog entry.

 1. Validate the catalog file syntax:

 python3 -c "import yaml; yaml.safe_load(open('catalog.yml'))"

 1. Use a YAML linter for more detailed error reporting:

 pip install yamllint
 yamllint catalog.yml

 1. Check for typos in component types. Valid types include:

 2. `slurm_cluster`

 3. `kubernetes_cluster`
 4. `telemetry`
 5. `authentication`
 6. `storage`

 8. After fixing errors, commit and push to trigger a new pipeline:

 git add catalog.yml
 git commit -m "Fix catalog syntax errors"
 git push

## OAuth credential issues

BuildStreaM operations fail with OAuth authentication errors when communicating with GitLab or external services:

 Error: OAuth token expired or revoked
 Error: 401 Unauthorized: invalid_token

 * The OAuth token has expired.
 * The OAuth application was deleted or its secret was rotated in GitLab.
 * The token scope does not include the required permissions (`api`, `read_registry`, `write_registry`).

 1. Check the current token status:

 curl -H "Authorization: Bearer <token>" \
 https://<gitlab_url>/api/v4/user

A `401` response confirms the token is invalid.

 1. Generate a new personal access token in GitLab:

 2. Navigate to **User Settings > Access Tokens**.

 3. Create a new token with scopes: `api`, `read_registry`, `write_registry`.

 4. Update the token in pipeline variables:

 5. Navigate to **Settings > CI/CD > Variables**.

 6. Update the `GITLAB_TOKEN` (or equivalent) variable with the new token.

 7. If using an OAuth application (rather than personal token):

 8. Navigate to **Admin Area > Applications** (or **User Settings > Applications**).

 9. Verify the application exists and note the Application ID and Secret.
 10. Update the pipeline variables with the new credentials.

 11. Re-run the failed pipeline from the GitLab UI.

Copyright © 2025 Dell Technologies. All rights reserved.