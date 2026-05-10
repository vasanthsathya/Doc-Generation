

Deploy GitLab
=============


Deploy and configure GitLab for BuildStreaM CI/CD pipelines that automate
catalog-driven cluster deployment.


Overview
--------


BuildStreaM uses GitLab as the CI/CD engine to execute catalog-driven
deployment pipelines. GitLab stores:

- The **catalog file** that declaratively defines cluster configuration.
- **Pipeline definitions** (``.gitlab-ci.yml``) that execute Omnia playbooks.
- **Artifacts** (logs, reports) from each pipeline run.

Omnia can deploy GitLab as a Podman container on the OIM or as a Helm
deployment on the K8s service cluster.



Prerequisites
-------------


- The `Prepare Oim <../Setup/prepare_oim.rst>`_ procedure is complete.
- At least 8 GB RAM available for the GitLab container (16 GB recommended).
- At least 50 GB disk space for GitLab data.
- A DNS name or IP address for GitLab access.
- The K8s service cluster is deployed (if using Helm deployment).



Procedure
---------



Option A: Deploy GitLab on the OIM (Podman)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Create persistent storage directories**:


**Run on: OIM host**

.. code-block:: bash
      mkdir -p /opt/gitlab/{config,logs,data}



#. **Deploy the GitLab container**:


**Run on: OIM host**

.. code-block:: bash
      podman run -d \
        --name gitlab \
        --restart=always \
        --hostname gitlab.omnia.local \
        -p 8443:443 \
        -p 8082:80 \
        -p 2222:22 \
        -v /opt/gitlab/config:/etc/gitlab:Z \
        -v /opt/gitlab/logs:/var/log/gitlab:Z \
        -v /opt/gitlab/data:/var/opt/gitlab:Z \
        --shm-size 256m \
        docker.io/gitlab/gitlab-ce:latest



   !!! note

       GitLab takes **3-5 minutes** to fully initialize after the container
       starts. Wait before proceeding.

#. **Retrieve the initial root password**:


**Run on: OIM host**

.. code-block:: bash
      podman exec gitlab cat /etc/gitlab/initial_root_password



   Save this password; it is only available for 24 hours.

#. **Access GitLab** in a browser: ``http://<oim-ip>:8082``

   Log in with:

  - Username: ``root``
  - Password: (from step 3)

#. **Create the BuildStreaM project**:


**Run on: OIM host**

.. code-block:: bash
      # Using GitLab API
      curl -s -X POST "http://localhost:8082/api/v4/projects" \
        -H "PRIVATE-TOKEN: <your-root-token>" \
        -d "name=buildstream-catalog&visibility=private"



#. **Register a GitLab Runner** for pipeline execution:


**Run on: OIM host**

.. code-block:: bash
      podman run -d \
        --name gitlab-runner \
        --restart=always \
        -v /opt/gitlab-runner:/etc/gitlab-runner:Z \
        -v /var/run/podman/podman.sock:/var/run/docker.sock:Z \
        docker.io/gitlab/gitlab-runner:latest
   
      podman exec gitlab-runner gitlab-runner register \
        --non-interactive \
        --url "http://<oim-ip>:8082" \
        --token "<runner-registration-token>" \
        --executor "shell" \
        --description "omnia-runner"





Option B: Deploy GitLab on K8s (Helm)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **(Alternative) Deploy GitLab via Helm**:


**Run on: K8s control plane node**

.. code-block:: bash
      helm repo add gitlab https://charts.gitlab.io/
      helm repo update
   
      helm install gitlab gitlab/gitlab \
        --namespace gitlab \
        --create-namespace \
        --set global.hosts.domain=omnia.local \
        --set global.hosts.externalIP=<metallb-ip> \
        --set certmanager.install=false \
        --set global.ingress.configureCertmanager=false \
        --set gitlab-runner.install=true \
        --set persistence.enabled=true \
        --timeout 600s





Configure GitLab for BuildStreaM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#. **Clone the BuildStreaM catalog repository** template:


**Run on: omnia_core container**

.. code-block:: bash
      cd /opt/omnia
      git clone http://<oim-ip>:8082/root/buildstream-catalog.git
      cd buildstream-catalog



#. **Create the pipeline configuration**:


**Run on: omnia_core container**

.. code-block:: bash
      cat <<'EOF' > .gitlab-ci.yml
      stages:
        - validate
        - provision
        - configure
        - verify
   
      validate_catalog:
        stage: validate
        script:
          - cd /omnia
          - ansible-playbook input_validator.yml
   
      provision_nodes:
        stage: provision
        script:
          - cd /omnia/discovery
          - ansible-playbook discovery.yml --ask-vault-pass
        when: manual
   
      configure_cluster:
        stage: configure
        script:
          - cd /omnia
          - ansible-playbook omnia.yml --ask-vault-pass
        when: manual
   
      verify_cluster:
        stage: verify
        script:
          - ansible all -m ping
          - ssh <slurm-control-ip> sinfo
      EOF



#. **Push the initial configuration**:


**Run on: omnia_core container**

.. code-block:: bash
       git add .
       git commit -m "Initial BuildStreaM catalog"
       git push origin main





Verification
------------


#. **Verify GitLab is running**:


**Run on: OIM host**

.. code-block:: bash
      podman ps --filter name=gitlab
      curl -s http://localhost:8082/users/sign_in | grep "GitLab"



#. **Verify the runner is registered**:


**Run on: OIM host**

.. code-block:: bash
      podman exec gitlab-runner gitlab-runner list



#. **Trigger a test pipeline** by pushing a commit or via the GitLab UI:

   Navigate to **CI/CD** > **Pipelines** in the GitLab web UI and confirm
   the pipeline stages appear.



Next Steps
----------


- `Update Catalog Pipeline <update_catalog_pipeline.rst>`_ -- Update the catalog and run pipelines.
- `Buildstream Troubleshooting <buildstream_troubleshooting.rst>`_ -- Troubleshoot pipeline issues.



Troubleshooting
---------------


**GitLab container takes too long to start**
   Check container logs:


**Run on: OIM host**

.. code-block:: bash
      podman logs -f gitlab



**"502 Bad Gateway" in browser**
   GitLab is still initializing. Wait 3-5 minutes and try again.

**Runner registration fails**
   Verify the registration token from GitLab's admin area:
   **Admin Area** > **CI/CD** > **Runners**

**Insufficient memory**
   GitLab requires at least 8 GB RAM. Check available memory:


**Run on: OIM host**

.. code-block:: bash
      free -h



**Port conflicts**
   Ensure ports 8082, 8443, and 2222 are not in use:


**Run on: OIM host**

.. code-block:: bash
      ss -tlnp | grep -E ':(8082|8443|2222)\b'

