
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Deploy Additional Packages 

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
 * [ Use Apptainer ](use_apptainer.html)
 * Deploy Additional Packages [ Deploy Additional Packages ](deploy_additional_packages.html) Table of contents 
 * [ Overview ](#overview)
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
 3. [ Containers ](use_apptainer.html)

# Deploy Additional Packages[¶](#deploy-additional-packages "Permanent link")

Install custom software packages on provisioned cluster nodes using Ansible ad-hoc commands, playbooks, or the Omnia local repository infrastructure.

## Overview[¶](#overview "Permanent link")

After initial cluster provisioning, you may need to install additional packages on some or all nodes:

 * Development tools (compilers, libraries)
 * Scientific libraries (BLAS, LAPACK, FFTW)
 * Monitoring agents
 * Custom in-house software

This guide covers three approaches:

 1. **Ansible ad-hoc commands** \-- Quick one-off installations.
 2. **Custom Ansible playbook** \-- Repeatable, versioned package deployment.
 3. **Local Pulp repository** \-- Add custom RPMs to the Omnia repository infrastructure for automated deployment to new nodes.

## Prerequisites[¶](#prerequisites "Permanent link")

 * Cluster nodes are provisioned and reachable via Ansible.
 * The `omnia_core` container has SSH access to all target nodes.
 * Local repositories are synced (see [Create Local Repos](../Setup/create_local_repos.html)) if installing from OS repos.

## Procedure[¶](#procedure "Permanent link")

### Approach 1: Ansible Ad-Hoc Commands[¶](#approach-1-ansible-ad-hoc-commands "Permanent link")

 1. **Install a package on all compute nodes** :

Run on: omnia_core container
 
 
 ansible slurm_node -m dnf -a "name=htop state=present"
 

 1. **Install multiple packages at once** :

Run on: omnia_core container
 
 
 ansible slurm_node -m dnf -a "name=gcc,gcc-c++,make,cmake state=present"
 

 1. **Install on a specific group of nodes** :

Run on: omnia_core container
 
 
 # Install only on login nodes
 ansible login_node -m dnf -a "name=emacs,vim-enhanced state=present"
 

 1. **Install from a specific repository** :

Run on: omnia_core container
 
 
 ansible slurm_node -m dnf -a "name=openmpi-devel enablerepo=epel state=present"
 

### Approach 2: Custom Ansible Playbook[¶](#approach-2-custom-ansible-playbook "Permanent link")

 1. **Create a custom playbook** for repeatable deployments:

Run on: omnia_core container
 
 
 cat <<'EOF' > /omnia/custom_packages.yml
 ---
 - name: Deploy custom packages to compute nodes
 hosts: slurm_node
 become: true
 tasks:
 - name: Install development tools
 dnf:
 name:
 - gcc
 - gcc-c++
 - gcc-gfortran
 - make
 - cmake
 - autoconf
 - automake
 state: present
 
 - name: Install scientific libraries
 dnf:
 name:
 - openblas-devel
 - lapack-devel
 - fftw-devel
 - hdf5-devel
 state: present
 
 - name: Install Python scientific stack
 pip:
 name:
 - numpy
 - scipy
 - matplotlib
 - pandas
 executable: pip3
 
 - name: Install monitoring tools
 dnf:
 name:
 - htop
 - iotop
 - sysstat
 - perf
 state: present
 EOF
 

 1. **Run the custom playbook** :

Run on: omnia_core container
 
 
 cd /omnia
 ansible-playbook custom_packages.yml
 

### Approach 3: Custom Pulp Repository[¶](#approach-3-custom-pulp-repository "Permanent link")

 1. **Add custom RPMs to Pulp** for automatic deployment to new nodes:

Run on: omnia_core container
 
 
 # Create a custom repository in Pulp
 pulp rpm repository create --name custom-packages
 
 # Upload custom RPMs
 pulp rpm content upload --file /path/to/custom-package.rpm --repository custom-packages
 
 # Create publication and distribution
 pulp rpm publication create --repository custom-packages
 pulp rpm distribution create --name custom-packages \
 --base-path custom-packages \
 --repository custom-packages
 

 1. **Configure nodes to use the custom repository** :

Run on: omnia_core container
 
 
 ansible all -m yum_repository -a "
 name=custom-packages
 description='Custom Omnia Packages'
 baseurl=http://<oim-ip>:8080/pulp/content/custom-packages/
 gpgcheck=0
 enabled=1
 "
 

 1. **Install from the custom repository** :

Run on: omnia_core container
 
 
 ansible slurm_node -m dnf -a "name=custom-package state=present enablerepo=custom-packages"
 

## Verification[¶](#verification "Permanent link")

 1. **Verify packages are installed** :

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "rpm -q gcc cmake htop"
 

 1. **Check package versions** :

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "gcc --version | head -1"
 

 1. **Verify Python packages** :

Run on: omnia_core container
 
 
 ansible slurm_node -m shell -a "pip3 list | grep numpy"
 

 1. **Verify custom Pulp repository** is available:

Run on: compute node
 
 
 dnf repolist | grep custom-packages
 

## Next Steps[¶](#next-steps "Permanent link")

 * [Use Apptainer](use_apptainer.html) \-- Use containers for complex application stacks.
 * [Run Hpc Benchmarks](../Slurm/run_hpc_benchmarks.html) \-- Run benchmarks with the installed packages.

## Troubleshooting[¶](#troubleshooting "Permanent link")

**"No package available" error** Verify the package name and check available repositories:

Run on: compute node
 
 
 dnf search <package-name>
 dnf repolist
 

**Package conflicts** Check for conflicting packages:

Run on: compute node
 
 
 dnf check
 

**Custom Pulp repository not accessible** Verify the distribution URL:

Run on: compute node
 
 
 curl -s http://<oim-ip>:8080/pulp/content/custom-packages/repodata/repomd.xml | head
 

**Pip install fails** Ensure pip and Python are installed:

Run on: compute node
 
 
 dnf install -y python3 python3-pip
 

**Ansible times out on large installations** Increase the Ansible timeout:

Run on: omnia_core container
 
 
 ansible slurm_node -m dnf -a "name=large-package state=present" -e "ansible_timeout=600"
 

Back to top [ Previous Use Apptainer ](use_apptainer.html) [ Next Deploy GitLab ](../BuildStreaM/deploy_gitlab.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
