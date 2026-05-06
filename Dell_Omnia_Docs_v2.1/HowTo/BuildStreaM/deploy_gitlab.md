
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Deploy GitLab 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../../index.html)

[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../../index.html)

Overview 
 * [ Architecture ](../../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](../Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * Deploy GitLab [ Deploy GitLab ](deploy_gitlab.html) Table of contents 
 * [ Overview ](#overview)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Overview ](#overview)

 1. [ Home ](../../index.html)
 2. [ How-to Guides ](../index.html)
 3. [ BuildStreaM ](deploy_gitlab.html)

# Deploy GitLab[¶](#deploy-gitlab "Permanent link")

Deploy and configure GitLab for BuildStreaM CI/CD pipelines that automate catalog-driven cluster deployment.

## Overview[¶](#overview "Permanent link")

BuildStreaM uses GitLab as the CI/CD engine to execute catalog-driven deployment pipelines. GitLab stores:

 * The **catalog file** that declaratively defines cluster configuration.
 * **Pipeline definitions** (`.gitlab-ci.yml`) that execute Omnia playbooks.
 * **Artifacts** (logs, reports) from each pipeline run.

Omnia can deploy GitLab as a Podman container on the OIM or as a Helm deployment on the K8s service cluster.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Prepare Oim](../Setup/prepare_oim.html) procedure is complete.
 * At least 8 GB RAM available for the GitLab container (16 GB recommended).
 * At least 50 GB disk space for GitLab data.
 * A DNS name or IP address for GitLab access.
 * The K8s service cluster is deployed (if using Helm deployment).

## Procedure[¶](#procedure "Permanent link")

### Option A: Deploy GitLab on the OIM (Podman)[¶](#option-a-deploy-gitlab-on-the-oim-podman "Permanent link")

 1. **Create persistent storage directories** :

Run on: OIM host
 
 
 mkdir -p /opt/gitlab/{config,logs,data}
 

 1. **Deploy the GitLab container** :

Run on: OIM host
 
 
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
 

 1. **Retrieve the initial root password** :

Run on: OIM host
 
 
 podman exec gitlab cat /etc/gitlab/initial_root_password
 

Save this password; it is only available for 24 hours.

 1. **Access GitLab** in a browser: `http://<oim-ip>:8082`

Log in with:

 * Username: `root`
 * Password: (from step 3)

 * **Create the BuildStreaM project** :

Run on: OIM host
 
 
 # Using GitLab API
 curl -s -X POST "http://localhost:8082/api/v4/projects" \
 -H "PRIVATE-TOKEN: <your-root-token>" \
 -d "name=buildstream-catalog&visibility=private"
 

 1. **Register a GitLab Runner** for pipeline execution:

Run on: OIM host
 
 
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
 

### Option B: Deploy GitLab on K8s (Helm)[¶](#option-b-deploy-gitlab-on-k8s-helm "Permanent link")

 1. **(Alternative) Deploy GitLab via Helm** :

Run on: K8s control plane node
 
 
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
 

### Configure GitLab for BuildStreaM[¶](#configure-gitlab-for-buildstream "Permanent link")

 1. **Clone the BuildStreaM catalog repository** template:

Run on: omnia_core container
 
 
 cd /opt/omnia
 git clone http://<oim-ip>:8082/root/buildstream-catalog.git
 cd buildstream-catalog
 

 1. **Create the pipeline configuration** :

Run on: omnia_core container
 
 
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
 

 1. **Push the initial configuration** :

Run on: omnia_core container
 
 git add .
 git commit -m "Initial BuildStreaM catalog"
 git push origin main
 

## Verification[¶](#verification "Permanent link")

 1. **Verify GitLab is running** :

Run on: OIM host
 
 
 podman ps --filter name=gitlab
 curl -s http://localhost:8082/users/sign_in | grep "GitLab"
 

 1. **Verify the runner is registered** :

Run on: OIM host
 
 
 podman exec gitlab-runner gitlab-runner list
 

 1. **Trigger a test pipeline** by pushing a commit or via the GitLab UI:

Navigate to **CI/CD** > **Pipelines** in the GitLab web UI and confirm the pipeline stages appear.

## Next Steps[¶](#next-steps "Permanent link")

 * [Update Catalog Pipeline](update_catalog_pipeline.html) \-- Update the catalog and run pipelines.
 * [Buildstream Troubleshooting](buildstream_troubleshooting.html) \-- Troubleshoot pipeline issues.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**GitLab container takes too long to start** Check container logs:

Run on: OIM host
 
 
 podman logs -f gitlab
 

**"502 Bad Gateway" in browser** GitLab is still initializing. Wait 3-5 minutes and try again.

**Runner registration fails** Verify the registration token from GitLab's admin area: **Admin Area** > **CI/CD** > **Runners**

**Insufficient memory** GitLab requires at least 8 GB RAM. Check available memory:

Run on: OIM host
 
 
 free -h
 

**Port conflicts** Ensure ports 8082, 8443, and 2222 are not in use:

Run on: OIM host
 
 
 ss -tlnp | grep -E ':(8082|8443|2222)\b'
 

Back to top [ Previous Deploy Additional Packages ](../Containers/deploy_additional_packages.html) [ Next Update Catalog Pipeline ](update_catalog_pipeline.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
