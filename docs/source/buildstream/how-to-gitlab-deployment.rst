.. _how-to-buildstream-gitlab-deployment:

GitLab Deployment
=================

.. note::
   This topic is pending SME validation. Content may change before publication.

Deploy GitLab as part of BuildStreaM integration to enable automated pipeline execution, catalog management, and build monitoring. This procedure covers GitLab installation, project setup, runner verification, and service validation.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before deploying GitLab for BuildStreaM:

* BuildStreaM configuration completed (see :doc:`how-to-prepare-buildstream`)
* prepare.yaml playbook completed successfully
* Sufficient system resources for GitLab (minimum 4 GB RAM, 2 CPU cores)
* Network connectivity for GitLab services
* Administrator access on the target server

.. important::
   Omnia does not support existing customer GitLab. This procedure deploys a new GitLab instance specifically for BuildStreaM.

Procedure
---------

#. Navigate to the GitLab installation directory.

Change to the BuildStreaM GitLab directory:

.. code-block:: bash

   cd /omnia/build_stream/gitlab

#. Deploy GitLab using the installation playbook.

Run the GitLab installation playbook for a fresh install:

.. code-block:: bash

   ansible-playbook gitlab.yml

This installs:
- GitLab server with web interface
- GitLab runner for pipeline execution
- Integration components for BuildStreaM
- Default project structure

.. note::
   The installation may take 10-15 minutes to complete.

#. Verify GitLab service status.

Check that GitLab is running and accessible:

.. code-block:: bash

   curl -I https://gitlab.example.com

Expected response shows GitLab is accessible:

.. code-block:: text

   HTTP/1.1 200 OK
   Server: nginx
   Date: Wed, 01 Mar 2026 12:00:00 GMT

#. Access the GitLab project.

Navigate to the GitLab project URL to verify project creation:

.. code-block:: text

   https://gitlab.example.com/omnia-catalog

The project should contain:
- **README.MD** - Project documentation
- **catalog_rhel.json** - Default catalog file
- **.gitlab-ci.yml** - Pipeline configuration file

#. Verify GitLab runner status.

Check that the GitLab runner is running as a Podman container:

.. code-block:: bash

   podman ps | grep gitlab-runner

Expected output shows the runner container:

.. code-block:: text

   gitlab-runner      Up   5 minutes ago

Alternatively, verify runner status through GitLab web interface:

1. Navigate to **Settings** → **CI/CD**
2. Expand **Runners** section
3. Verify the runner shows a **green** status indicator
4. Confirm runner is set to **Running Always** with **Podman Container**

#. Review pipeline configuration.

Examine the .gitlab-ci.yml file that defines the BuildStreaM pipeline:

.. code-block:: yaml

   # .gitlab-ci.yml
   stages:
     - parse-catalog
     - generate-input-files
     - prepare-repos
     - build-image
     - validate-image

   buildstream-pipeline:
     stage: parse-catalog
     script:
       - /opt/omnia/buildstream/scripts/trigger-pipeline.sh
     artifacts:
       reports:
         junit: buildstream-results.xml
     only:
       - main

.. note::
   The .gitlab-ci.yml pipeline file invokes BuildStreaM REST APIs chronologically from a GitLab runner acting as a remote client.

#. Test GitLab integration.

Verify that GitLab can communicate with BuildStreaM:

.. code-block:: bash

   # Test API connectivity from GitLab runner
   podman exec gitlab-runner curl -X GET "http://buildstream-api:8080/api/v1/health"

Expected response:

.. code-block:: json

   {
     "status": "healthy",
     "version": "1.0.0"
   }

#. Verify repository access.

Check that you can access project files through the GitLab interface:

1. Navigate to the project
2. Go to **Check** → **Code** → **Repository**
3. Verify the following files are present:
   - README.MD
   - catalog_rhel.json
   - .gitlab-ci.yml

Result
------

GitLab is now deployed and integrated with BuildStreaM for automated pipeline execution. The system can automatically trigger builds based on catalog changes and provide monitoring through the GitLab web interface.

Verification
------------

Verify the GitLab deployment is working correctly:

#. Check GitLab service health:

.. code-block:: bash

   # Monitor GitLab services
   podman logs gitlab --tail 20

#. Verify runner functionality:

.. code-block:: bash

   # Check runner logs
   podman logs gitlab-runner --tail 20

#. Test project access:

.. code-block:: bash

   # Clone the project to test access
   git clone https://gitlab.example.com/omnia-catalog.git

#. Validate pipeline configuration:

.. code-block:: bash

   # Check pipeline syntax
   cd omnia-catalog
   gitlab-ci-lint .gitlab-ci.yml

Expected output shows no syntax errors and all services are healthy.

Next Steps
----------

After completing GitLab deployment:

* **Update catalog files** - Modify catalog_rhel.json to define your build requirements
* **Trigger first pipeline** - Make catalog changes to test automated pipeline execution
* **Monitor pipeline execution** - Use GitLab Build > Pipeline interface to track progress
* **Verify job execution** - Use GitLab Build > Jobs interface to verify all jobs run

.. warning::
   If the GitLab runner shows offline status, restart the runner service and check network connectivity between GitLab and BuildStreaM.

For catalog update procedures, see :doc:`how-to-update-catalog-pipeline`.

Related Topics
--------------

* :doc:`concept-overview`
* :doc:`how-to-prepare-buildstream`
* :doc:`how-to-update-catalog-pipeline`
