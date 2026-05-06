
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Verify OIM Services 

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
 * [ Prepare OIM ](prepare_oim.html)
 * Verify OIM Services [ Verify OIM Services ](verify_oim_services.html) Table of contents 
 * [ Overview ](#overview)
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
 * [ Deploy GitLab ](../BuildStreaM/deploy_gitlab.html)

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
 3. [ Setup ](prepare_oim.html)

# Verify OIM Services[¶](#verify-oim-services "Permanent link")

Perform a comprehensive health check of all Omnia Infrastructure Manager (OIM) services after running `prepare_oim.yml`. This guide walks through every service in the `omnia.target` dependency tree.

## Overview[¶](#overview "Permanent link")

After the OIM is prepared, the following services should be running as systemd-managed Podman containers:

 * **omnia_core** \-- Ansible control plane
 * **OpenCHAMI stack** \-- SMD, BSS, CoreDHCP, TFTP, DNS, and related services
 * **Pulp** \-- RPM repository management
 * **MinIO** \-- S3-compatible object storage
 * **Registry** \-- Local container image registry
 * **Omnia Auth** _(optional)_ \-- Centralized authentication

This guide helps you verify each service is healthy and troubleshoot any that are not.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Prepare Oim](prepare_oim.html) procedure has been completed.
 * You have `root` or `sudo` access to the OIM host.

## Procedure[¶](#procedure "Permanent link")

 1. **Check the omnia_core service** :

Run on: OIM host
 
 
 systemctl status omnia_core.service
 

Expected: `Active: active (running)`

 1. **List the complete omnia.target dependency tree** :

Run on: OIM host
 
 
 systemctl list-dependencies omnia.target
 

Expected output:

Expected output on: OIM host
 
 
 omnia.target
 ├─minio.service
 ├─omnia_auth.service
 ├─omnia_core.service
 ├─pulp.service
 ├─registry.service
 └─openchami.target
 ├─bss.service
 ├─coredhcp.service
 ├─cloud-init-server.service
 ├─dnsmasq.service
 ├─hydra.service
 ├─image-server.service
 ├─opaal.service
 ├─smd.service
 └─tftpd.service
 

 1. **Check each top-level service individually** :

Run on: OIM host
 
 
 for svc in minio omnia_auth omnia_core pulp registry; do
 echo "=== $svc ==="
 systemctl is-active ${svc}.service
 done
 

 1. **Check OpenCHAMI sub-services** :

Run on: OIM host
 
 
 for svc in bss coredhcp cloud-init-server dnsmasq hydra image-server opaal smd tftpd; do
 echo "=== $svc ==="
 systemctl is-active ${svc}.service
 done
 

 1. **Verify running Podman containers** :

Run on: OIM host
 
 
 podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
 

 1. **Test the OpenCHAMI CLI** :

Run on: OIM host
 
 
 ssh omnia_core
 

Run on: omnia_core container
 
 
 ochami --help
 

Useful `ochami` commands:

Run on: omnia_core container
 
 
 # List discovered nodes
 ochami node list
 
 # Check SMD status
 ochami smd status
 
 # List boot configurations
 ochami bss list
 

 1. **Test MinIO / S3 access** :

Run on: omnia_core container
 
 
 s3cmd ls
 

 1. **Test Pulp accessibility** :

Run on: OIM host
 
 
 curl -s http://localhost:8080/pulp/api/v3/status/ | python3 -m json.tool
 

Expected: a JSON response with `"online_workers"` and `"versions"`.

## Verification[¶](#verification "Permanent link")

All services should report `active (running)`. Use this summary check:

Run on: OIM host
 
 
 systemctl is-active omnia.target
 

Expected output: `active`

If any service is `inactive` or `failed`, note which one and refer to the Troubleshooting section below.

**Quick health summary script** :

Run on: OIM host
 
 
 echo "=== Omnia Service Health ==="
 echo "omnia.target: $(systemctl is-active omnia.target)"
 echo "omnia_core: $(systemctl is-active omnia_core.service)"
 echo "openchami.target:$(systemctl is-active openchami.target)"
 echo "pulp: $(systemctl is-active pulp.service)"
 echo "minio: $(systemctl is-active minio.service)"
 echo "registry: $(systemctl is-active registry.service)"
 echo "omnia_auth: $(systemctl is-active omnia_auth.service)"
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Create Local Repos](create_local_repos.html) \-- Sync RPM repositories via Pulp.
 * [Build Cluster Images](build_cluster_images.html) \-- Build OS boot images.
 * [Discover Nodes](discover_nodes.html) \-- Discover and provision bare-metal servers.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**A service shows "inactive (dead)"** Restart the specific service:

Run on: OIM host
 
 
 systemctl restart <service-name>.service
 journalctl -u <service-name>.service --no-pager -n 50
 

**OpenCHAMI services fail with connection errors** Verify the SMD service is running first, as other OpenCHAMI services depend on it:

Run on: OIM host
 
 
 systemctl restart smd.service
 sleep 10
 systemctl restart openchami.target
 

**Pulp API returns connection refused** Check that the Pulp container is running and listening on port 8080:

Run on: OIM host
 
 
 podman logs pulp
 ss -tlnp | grep 8080
 

**MinIO not accessible** Verify MinIO container status and port binding:

Run on: OIM host
 
 
 podman logs minio
 ss -tlnp | grep 9000
 

**omnia.target not found** Re-run the `prepare_oim.yml` playbook to regenerate systemd unit files:

Run on: omnia_core container
 
 
 cd /omnia/prepare_oim
 ansible-playbook prepare_oim.yml --ask-vault-pass
 

**Container images missing** Rebuild the container images:

Run on: OIM host
 
 
 cd /opt/omnia
 bash build_images.sh core
 

Back to top [ Previous Build Cluster Images ](build_cluster_images.html) [ Next Verify Cluster ](verify_cluster.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
