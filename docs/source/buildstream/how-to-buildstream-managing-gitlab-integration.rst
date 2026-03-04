.. _how-to-buildstream-managing-gitlab-integration:

Managing GitLab Integration
===========================

Manage BuildStreaM's integration with GitLab to enable automated CI/CD pipelines for your HPC infrastructure. This guide covers project configuration, pipeline setup, and monitoring pipeline execution.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before managing GitLab integration, ensure you have:

* BuildStreaM enabled in Omnia (see :doc:`how-to-buildstream-enabling-buildstream`)
* GitLab server with administrator access
* Understanding of GitLab CI/CD concepts
* Access to the BuildStreaM configuration files
* Network connectivity between Omnia and GitLab

GitLab Project Configuration
-----------------------------

Configure the GitLab project that will host your BuildStreaM pipelines.

#. Access the GitLab project created during BuildStreaM setup.

   Navigate to your GitLab instance and open the `omnia-buildstream` project.

#. Verify project settings.

   Click **Settings** > **General** and verify:

   * **Project name**: `omnia-buildstream`
   * **Visibility**: Private or Public (as configured during setup)
   * **Default branch**: `main`

#. Configure project permissions.

   Click **Settings** > **Members** and ensure:

   * BuildStreaM service account has **Maintainer** role
   * Required team members have appropriate access levels
   * Guest access is disabled for private projects

Pipeline Configuration
---------------------

Set up the CI/CD pipeline that automates your BuildStreaM workflows.

#. Access the pipeline configuration.

   In your GitLab project, click **Set up CI/CD** or navigate to the `.gitlab-ci.yml` file.

#. Review the pipeline stages.

   The default BuildStreaM pipeline includes these stages:

   .. code-block:: yaml

      stages:
        - local_repo
        - build_image
        - discovery
        - authentication
        - registration

   Each stage corresponds to a traditional Omnia playbook:

   * **local_repo**: Creates local repositories for package management
   * **build_image**: Builds container images based on catalog definitions
   * **discovery**: Discovers and provisions target nodes
   * **authentication**: Configures authentication and access control
   * **registration**: Registers nodes with cluster management

#. Configure pipeline triggers.

   Ensure the pipeline is configured to trigger automatically:

   .. code-block:: yaml

      # Trigger on catalog changes
      workflow:
        rules:
          - if: $CI_PIPELINE_SOURCE == "push"
            changes:
              - catalog.yml
              - "catalogs/**/*"

   This configuration ensures that any changes to catalog files automatically trigger a new pipeline execution.

Pipeline Monitoring
-------------------

Monitor pipeline execution to ensure successful deployment of your HPC infrastructure.

#. Access pipeline status.

   In your GitLab project, click **CI/CD** > **Pipelines** to view all pipeline executions.

#. Interpret pipeline status indicators.

   Pipeline status indicators:

   * **Passed** (green): All stages completed successfully
   * **Failed** (red): One or more stages failed
   * **Running** (blue): Pipeline is currently executing
   * **Canceled** (gray): Pipeline was manually canceled

#. View stage details.

   Click on a specific pipeline to view individual stage execution:

   * Each stage shows execution time and status
   * Click on a stage name to view detailed logs
   * Failed stages show error messages and diagnostic information

#. Monitor job execution.

   Click **Jobs** to view detailed job information:

   * **Job logs**: Real-time output from pipeline execution
   * **Artifacts**: Generated files and reports
   * **Dependencies**: Job relationships and execution order

Runner Management
-----------------

Ensure GitLab runners are properly configured and operational.

#. Check runner status.

   In GitLab, navigate to **Settings** > **CI/CD** and expand the **Runners** section.

   Verify that:

   * At least one runner is **online** (green dot)
   * Runner has appropriate tags for BuildStreaM jobs
   * Runner is not locked to specific projects (unless required)

#. Verify runner configuration.

   The BuildStreaM runner should have these characteristics:

   * **Type**: Docker or Shell
   * **Tags**: `buildstream`, `omnia`
   * **Maximum job timeout**: 2 hours (or as required)
   * **Concurrent jobs**: 1 (to avoid resource conflicts)

.. important:: The GitLab runner must be online and active for pipelines to execute. If the runner is offline, pipelines will remain in pending state.

Catalog Management in GitLab
----------------------------

Manage your BuildStreaM catalogs through the GitLab interface.

#. Access catalog files.

   In your GitLab project, navigate to the **Repository** > **Files** section.

   You will find:

   * `catalog.yml`: Main catalog file
   * `catalogs/`: Directory for additional catalog files
   * `.gitlab-ci.yml`: Pipeline configuration

#. Modify catalog definitions.

   To update your catalog:

   .. code-block:: bash

      # Clone the repository
      git clone http://192.168.1.100/omnia-buildstream/omnia-buildstream.git
      cd omnia-buildstream

      # Edit catalog file
      vi catalog.yml

      # Commit and push changes
      git add catalog.yml
      git commit -m "Update catalog: add new compute role"
      git push origin main

   The push will automatically trigger a new pipeline execution.

#. Review catalog structure.

   A typical catalog includes:

   .. code-block:: yaml

      catalog:
        version: "1.0"
        roles:
          - name: "compute-node"
            packages:
              - name: "rocky-linux"
                version: "8.8"
              - name: "kubernetes"
                version: "1.28"
        validation:
          - name: "basic-connectivity"
            type: "network"

.. note:: Catalog changes trigger automatic pipeline execution. Ensure your catalog definitions are valid before committing changes.

Pipeline Troubleshooting
-----------------------

Resolve common issues with GitLab pipeline execution.

**Pipeline stuck in pending state**

   Check runner status:

   .. code-block:: bash

      # Verify runner is online
      curl -H "Private-Token: [GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/runners"

   Common solutions:
   * Restart the GitLab runner service
   * Check network connectivity between GitLab and runner
   * Verify runner tags match job requirements

**Stage failures**

   Investigate failed stages:

   1. Click on the failed stage to view logs
   2. Look for error messages and stack traces
   3. Check catalog file syntax and structure
   4. Verify Omnia services are running and accessible

   Common failure causes:
   * Invalid catalog syntax
   * Missing required packages in repositories
   * Network connectivity issues
   * Insufficient resources on target nodes

**Authentication errors**

   Verify BuildStreaM GitLab credentials:

   .. code-block:: bash

      # Test GitLab API access
      curl -H "Private-Token: [GITLAB_TOKEN]" \
           "http://192.168.1.100/api/v4/user"

   Common solutions:
   * Regenerate GitLab access token
   * Update BuildStreaM configuration with new token
   * Verify token has required permissions (api scope)

Advanced Configuration
----------------------

Configure advanced GitLab integration features for enhanced BuildStreaM functionality.

#. Set up pipeline notifications.

   Configure email or Slack notifications for pipeline events:

   .. code-block:: yaml

      notify:
        email:
          enabled: true
          recipients:
            - admin@company.com
            - devops@company.com
        slack:
          enabled: true
          webhook_url: "[SLACK_WEBHOOK_URL]"
          channel: "#omnia-deployments"

#. Configure pipeline artifacts.

   Set up artifact retention and storage:

   .. code-block:: yaml

      artifacts:
        reports:
          junit: test-results.xml
          coverage: coverage.xml
        paths:
          - logs/
          - reports/
        expire_in: 1 week

#. Set up protected branches.

   Configure branch protection for production catalogs:

   .. code-block:: bash

      # In GitLab UI: Settings > Repository > Protected branches
      # Protect main branch
      # Require merge requests
      # Require pipeline success

.. AI_REVIEW: Advanced configuration details inferred from GitLab best practices - verify against specific BuildStreaM requirements

Best Practices
--------------

Follow these best practices for optimal GitLab integration:

**Catalog Management**

* Use version control for all catalog changes
* Test catalog changes in development before production
* Use descriptive commit messages for catalog updates
* Maintain catalog documentation and change logs

**Pipeline Monitoring**

* Set up alerts for pipeline failures
* Regularly review pipeline execution times
* Monitor runner resource utilization
* Keep pipeline configurations under version control

**Security**

* Use GitLab personal access tokens with minimal required scope
* Regularly rotate access tokens
* Restrict project access to authorized personnel
* Use protected branches for production catalogs

**Performance**

* Optimize catalog size and complexity
* Use appropriate runner resources for your workload
* Monitor pipeline execution times and optimize stages
* Clean up old pipeline artifacts and logs

Related Topics
--------------

* :doc:`concepts-buildstream-catalog`
* :doc:`how-to-buildstream-working-with-pipelines`
* :doc:`troubleshooting-buildstream-pipeline-failures`
