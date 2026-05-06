
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Build Slurm Repo 

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
 * [ Set Up Slurm ](setup_slurm.html)
 * Build Slurm Repo [ Build Slurm Repo ](build_slurm_repo.html) Table of contents 
 * [ Overview ](#overview)
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
 3. [ Slurm ](setup_slurm.html)

# Build Slurm Repository[¶](#build-slurm-repository "Permanent link")

Build a custom Slurm RPM repository for use with Omnia's local repository infrastructure. This is useful when you need a specific Slurm version or custom build options.

## Overview[¶](#overview "Permanent link")

By default, Omnia installs Slurm from pre-built RPM packages in the local Pulp repositories. If you need a specific Slurm version, custom compile options, or patches, you can build Slurm RPMs from source and host them in a local repository.

## Prerequisites[¶](#prerequisites "Permanent link")

 * The [Create Local Repos](../Setup/create_local_repos.html) procedure is complete (Pulp is running and base OS repos are synced).
 * A build host with:

 * RHEL 8.x / 9.x or Rocky Linux matching your cluster OS

 * `rpm-build`, `rpmbuild`, and development tools installed
 * At least 10 GB free disk space

 * Slurm source tarball (download from `<https://www.schedmd.com/downloads.php>`_).

## Procedure[¶](#procedure "Permanent link")

 1. **Install build dependencies** on the build host:

Run on: build host (OIM or dedicated build server)
 
 
 dnf groupinstall -y "Development Tools"
 dnf install -y rpm-build munge-devel munge-libs pam-devel \
 perl-ExtUtils-MakeMaker readline-devel openssl-devel \
 mariadb-devel hwloc-devel lua-devel numactl-devel \
 http-parser-devel json-c-devel libcurl-devel
 

 1. **Create the RPM build directory structure** :

Run on: build host
 
 
 mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
 

 1. **Download the Slurm source tarball** :

Run on: build host
 
 
 cd ~/rpmbuild/SOURCES
 wget https://download.schedmd.com/slurm/slurm-23.11.4.tar.bz2
 

!!! note
 
 
 Replace the version number with your desired Slurm version.
 

 1. **Extract the spec file** :

Run on: build host
 
 
 tar xjf slurm-23.11.4.tar.bz2 --strip-components=1 -C /tmp slurm-23.11.4/slurm.spec
 cp /tmp/slurm.spec ~/rpmbuild/SPECS/
 

 1. **Build the RPMs** :

Run on: build host
 
 
 rpmbuild -ba ~/rpmbuild/SPECS/slurm.spec
 

This process takes **10-30 minutes** depending on hardware. The resulting RPMs will be in `~/rpmbuild/RPMS/x86_64/`.

 1. **Create a local repository** from the built RPMs:

Run on: build host
 
 
 dnf install -y createrepo_c
 mkdir -p /opt/omnia/custom_repos/slurm
 cp ~/rpmbuild/RPMS/x86_64/slurm-*.rpm /opt/omnia/custom_repos/slurm/
 createrepo_c /opt/omnia/custom_repos/slurm/
 

 1. **Upload to Pulp** (from the omnia_core container):

Run on: omnia_core container
 
 
 # Create a Pulp repository for custom Slurm RPMs
 pulp rpm repository create --name slurm-custom
 
 # Upload RPMs
 for rpm in /opt/omnia/custom_repos/slurm/*.rpm; do
 pulp rpm content upload --file "$rpm" --repository slurm-custom
 done
 
 # Create a publication and distribution
 pulp rpm publication create --repository slurm-custom
 pulp rpm distribution create --name slurm-custom \
 --base-path slurm-custom \
 --repository slurm-custom
 

## Verification[¶](#verification "Permanent link")

 1. **List the custom repository contents** :

Run on: build host
 
 
 ls -la /opt/omnia/custom_repos/slurm/
 

 1. **Verify the repository metadata** :

Run on: build host
 
 
 ls /opt/omnia/custom_repos/slurm/repodata/
 

You should see `repomd.xml` and related files.

 1. **Test package availability via Pulp** :

Run on: OIM host
 
 
 curl -s http://localhost:8080/pulp/content/slurm-custom/repodata/repomd.xml | head
 

 1. **Verify RPM versions** :

Run on: build host
 
 
 rpm -qip ~/rpmbuild/RPMS/x86_64/slurm-23*.rpm | grep -E "^(Name|Version)"
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Setup Slurm](setup_slurm.html) \-- Deploy Slurm using the custom RPMs.
 * [Create Local Repos](../Setup/create_local_repos.html) \-- Integrate the custom repo with Omnia's repo management.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**rpmbuild fails with missing dependency** Install the missing development package:

Run on: build host
 
 
 dnf install -y <missing-package>-devel
 

**Spec file not found in tarball** Download the spec file separately from SchedMD's GitHub:

Run on: build host
 
 
 wget -O ~/rpmbuild/SPECS/slurm.spec \
 https://raw.githubusercontent.com/SchedMD/slurm/slurm-23-11-4-1/slurm.spec
 

**createrepo_c fails** Ensure the package is installed:

Run on: build host
 
 
 dnf install -y createrepo_c
 

**Custom RPMs conflict with existing Slurm packages** Remove existing Slurm packages before installing custom ones:

Run on: compute node
 
 
 dnf remove -y slurm slurm-slurmd slurm-slurmctld
 dnf install -y --disablerepo='*' --enablerepo='slurm-custom' slurm slurm-slurmd
 

Back to top [ Previous Set Up Slurm ](setup_slurm.html) [ Next Slurm with GPU ](slurm_with_gpu.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
