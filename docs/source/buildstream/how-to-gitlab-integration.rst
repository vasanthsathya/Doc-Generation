.. _how-to-buildstream-gitlab-integration:

BuildStreaM GitLab Integration
===============================

.. note::
   This topic is pending SME validation. Content may change before publication.

Integrate BuildStreaM with GitLab for automated pipeline execution, catalog management, and build monitoring. This procedure covers GitLab installation, project setup, and pipeline configuration.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before integrating BuildStreaM with GitLab:

* BuildStreaM installed and configured (see :doc:`how-to-get-started`)
* GitLab server (self-hosted or GitLab.com)
* Administrator access to GitLab instance
* Network connectivity between BuildStreaM and GitLab
* GitLab runner configured and online
* Valid SSL certificates for GitLab (if using HTTPS)

.. important::
   Ensure the GitLab runner is always online and accessible, as it executes the BuildStreaM pipelines.

Procedure
---------

#. Configure GitLab connection parameters.

Update the BuildStreaM configuration to include GitLab settings:

.. code-block:: yaml

   buildstream:
     gitlab:
       enabled: true
       host: "gitlab.example.com"
       project_name: "omnia-buildstream"
       visibility: "private"
       main_branch: "main"
       access_token: "your-gitlab-access-token"

.. note::
   Set visibility to "private" for secure repositories or "public" for open-source projects.

#. Install GitLab using the gitlab.yaml playbook.

Run the GitLab installation playbook:

.. code-block:: bash

   cd /path/to/omnia
   ansible-playbook playbooks/gitlab.yml

This installs GitLab on the specified server and creates the BuildStreaM project.

#. Verify GitLab installation.

Check that GitLab is running and accessible:

.. code-block:: bash

   curl -I https://gitlab.example.com

Expected response shows GitLab is accessible:

.. code-block:: text

   HTTP/1.1 200 OK
   Server: nginx
   Date: Wed, 01 Mar 2026 12:00:00 GMT

#. Access the GitLab project.

Navigate to the GitLab project URL:

.. code-block:: text

   https://gitlab.example.com/omnia-buildstream

Verify the project contains:
- **GitLab CA file**: Certificate authority for secure connections
- **Catalog file**: Default Omnia template catalog
- **Pipeline definition**: GitLab CI configuration (.gitlab-ci.yml)

#. Configure the default catalog.

The default catalog provides a template for defining build requirements:

.. code-block:: yaml

   # Default catalog structure
   catalog_version: "1.0"
   description: "Omnia BuildStreaM Default Catalog"
   
   roles:
     - name: "management-node"
       description: "Cluster management node"
       packages:
         - name: "rocky-linux"
           version: "8.8"
         - name: "kubernetes"
           version: "1.28"
         - name: "etcd"
           version: "3.5"
   
   packages:
     - name: "rocky-linux"
       type: "os"
       source: "https://download.rockylinux.org"
     - name: "kubernetes"
       type: "container-runtime"
       source: "https://kubernetes.io"

.. note::
   The catalog file can be up to 4000 lines for complex configurations. Use the catalog generation script for large catalogs.

#. Set up the GitLab runner.

Verify the GitLab runner is online and configured:

.. code-block:: bash

   podman ps | grep gitlab-runner

Expected output shows the runner container:

.. code-block:: text

   gitlab-runner      Up   5 minutes ago

Check runner status in GitLab:
1. Navigate to **Settings** → **CI/CD**
2. Expand **Runners** section
3. Verify the runner shows a **green** status indicator

#. Configure the pipeline definition.

The .gitlab-ci.yml file defines the BuildStreaM pipeline stages:

.. code-block:: yaml

   # .gitlab-ci.yml
   stages:
     - parse-catalog
     - generate-input-files
     - prepare-repos
     - build-image
     - validate-image
     - validate-image-on-test
     - promote

   buildstream-pipeline:
     stage: parse-catalog
     script:
       - /opt/omnia/buildstream/scripts/trigger-pipeline.sh
     artifacts:
       reports:
         junit: buildstream-results.xml
     only:
       - main

#. Test catalog changes and pipeline triggering.

Modify the catalog to test automatic pipeline triggering:

.. code-block:: bash

   # Edit catalog version to trigger pipeline
   sed -i 's/catalog_version: "1.0"/catalog_version: "1.1"/' catalog.yaml

Commit the changes:

.. code-block:: bash

   git add catalog.yaml
   git commit -m "Update catalog version to 1.1"
   git push origin main

#. Monitor the pipeline execution.

Navigate to the GitLab project and monitor the pipeline:

1. Go to **Build** → **Pipelines**
2. Click on the running pipeline
3. Monitor each stage:
   - **Green** checkmark: Stage completed successfully
   - **Red** X: Stage failed (click for error details)

.. tip::
   Pipeline stages execute in sequence. If any stage fails, subsequent stages will not run until the issue is resolved.

#. Review pipeline results.

When the pipeline completes successfully:

1. Check the **Jobs** tab for detailed execution logs
2. Review **Artifacts** for build outputs and validation reports
3. Verify build images in the artifact repository

.. code-block:: bash

   # List build artifacts
   ls -la /opt/omnia/artifacts/buildstream/

Expected output:

.. code-block:: text

   job-20240301-002/
   ├── management-node.img
   ├── management-node.sbom
   ├── validation-report.json
   └── pipeline-manifest.json

Result
------

BuildStreaM is now integrated with GitLab for automated pipeline execution. Catalog changes automatically trigger build pipelines, and you can monitor progress through the GitLab interface.

Verification
------------

Verify the GitLab integration is working correctly:

#. Test pipeline triggering with catalog changes:

.. code-block:: bash

   # Make a minor catalog change
   echo "# Test change" >> catalog.yaml
   git add catalog.yaml
   git commit -m "Test pipeline trigger"
   git push origin main

#. Verify pipeline starts automatically within 30 seconds.

#. Check that all 7 pipeline stages execute successfully.

#. Validate that build artifacts are created and accessible.

.. code-block:: bash

   # Verify artifact integrity
   sha256sum /opt/omnia/artifacts/buildstream/*/management-node.img

Next Steps
----------

After completing GitLab integration:

* **Configure advanced pipelines**: Add custom stages and parallel execution
* **Set up notifications**: Configure email or Slack notifications for pipeline status
* **Implement approval gates**: Add manual approval stages for critical builds
* **Monitor runner performance**: Track runner utilization and scale as needed

.. warning::
   If a pipeline stage fails, review the error logs in the GitLab job output. Common issues include catalog validation errors, resource constraints, or external service unavailability.

For troubleshooting GitLab integration issues, see :doc:`../troubleshooting/buildstream-issues`.

Related Topics
--------------

* :doc:`concept-architecture`
* :doc:`how-to-get-started`
* :doc:`how-to-configure-catalogs`
* :doc:`../reference/api/buildstream`
