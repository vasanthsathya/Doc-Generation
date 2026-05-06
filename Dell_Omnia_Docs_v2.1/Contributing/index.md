
[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia")

Dell Omnia 

Contributing to Omnia 

[ ](javascript:void\(0\) "Share")



 * [ Home ](../index.html)

[ ![logo](../assets/omnia-logo.png) ](../index.html "Dell Omnia") Dell Omnia 



 * [ Home ](../index.html)

Overview 
 * [ Architecture ](../Overview/architecture.html)

Get Started 
 * [ Prerequisites Checklist ](../GetStarted/prerequisites_checklist.html)

How-to Guides 
 * Setup Setup 
 * [ Prepare OIM ](../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../Reference/SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../Reference/Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](../Reference/SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../Reference/ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Reference/Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Reference/Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Reference/Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](pull_requests.html)

Table of contents 

 * [ Ways to contribute ](#ways-to-contribute)

 1. [ Home ](../index.html)
 2. [ Contributing ](index.html)

# Contributing to Omnia[¶](#contributing-to-omnia "Permanent link")

Omnia is an open-source project licensed under the `Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_. Contributions from the community are welcome and encouraged---whether you are fixing a typo in the documentation, reporting a bug, proposing a new feature, or submitting a pull request with code changes.

Tip

New to open-source contribution? Start with a documentation improvement or bug report. These are great ways to get familiar with the project before submitting code changes.

## Ways to contribute[¶](#ways-to-contribute "Permanent link")

**Documentation** Improve existing documentation, fix errors, add examples, or write new guides. Documentation is written in reStructuredText (RST) and built with Sphinx.

**Bug reports** Found a bug? Open an issue on the `Omnia GitHub repository <https://github.com/dell/omnia/issues>`_ with a clear description of the problem, steps to reproduce, and relevant log output.

**Feature requests** Have an idea for a new feature or improvement? Open a GitHub issue with the `enhancement` label and describe the use case, expected behavior, and any design considerations.

**Code contributions** Fix bugs, implement features, or improve existing functionality. See [Pull Requests](pull_requests.html) for guidelines on submitting code changes.

**Testing** Test Omnia on different hardware configurations, OS versions, or network topologies and report your findings. Community testing helps improve compatibility and stability.

## Getting started[¶](#getting-started "Permanent link")

 1. **Fork the repository** on GitHub:

https://github.com/dell/omnia

 1. **Clone your fork** locally:

 
 
 git clone https://github.com/<your_username>/omnia.git
 cd omnia
 

 1. **Create a feature branch** for your changes:

 
 
 git checkout -b feature/my-improvement
 

 1. **Make your changes** , commit, and push:

 
 
 git add .
 git commit -m "Brief description of the change"
 git push origin feature/my-improvement
 

 1. **Open a pull request** on GitHub from your feature branch to the `main` branch of the upstream repository. See [Pull Requests](pull_requests.html) for detailed guidelines.

## Code of conduct[¶](#code-of-conduct "Permanent link")

All contributors are expected to follow the project's code of conduct. Be respectful, constructive, and collaborative in all interactions.

## Contact[¶](#contact "Permanent link")

 * **GitHub Issues:** https://github.com/dell/omnia/issues
 * **GitHub Discussions:** https://github.com/dell/omnia/discussions

Back to top [ Previous Known Limitations ](../Troubleshooting/known_limitations.html) [ Next Pull Requests ](pull_requests.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
