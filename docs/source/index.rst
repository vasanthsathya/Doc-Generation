
Omnia Documentation
===================


.. image:: https://img.shields.io/github/v/release/dell/omnia?include_prereleases
   :target: https://github.com/dell/omnia/releases
   :alt: Omnia version


.. image:: https://img.shields.io/github/downloads/dell/omnia/total
   :target: https://github.com/dell/omnia/releases
   :alt: Downloads


.. image:: https://img.shields.io/github/last-commit/dell/omnia
   :target: https://github.com/dell/omnia/commits
   :alt: Last Commit


.. image:: https://img.shields.io/github/contributors/dell/omnia
   :target: https://github.com/dell/omnia/graphs/contributors
   :alt: Contributors


.. image:: https://img.shields.io/github/forks/dell/omnia
   :target: https://github.com/dell/omnia/network/members
   :alt: Forks


.. image:: https://img.shields.io/github/license/dell/omnia
   :target: https://github.com/dell/omnia/blob/main/LICENSE
   :alt: License


Omnia is an open-source, Ansible-based toolkit by Dell Technologies that
automates the deployment and management of HPC, AI, and data analytics clusters
on Dell PowerEdge servers. From bare-metal provisioning to job scheduling,
telemetry, and storage configuration, Omnia turns a rack of servers into a
production-ready cluster.

The project is hosted on `GitHub <https://github.com/dell/omnia>`_, where you can:

- Access the source code
- Report issues
- Ask questions
- Contribute to development


How This Documentation is Organized
-----------------------------------


.. toctree::
   :maxdepth: 2
   :caption: Main Documentation

   Overview/index
   GetStarted/index
   HowTo/index
   Operations/index
   Reference/index
   Troubleshooting/index
   Contributing/index


.. grid:: 2 2 2 2
   :gutter: 3
   :class-container: sd-mb-4

   .. grid-item-card:: :material-book-open-variant: Overview
      :link: Overview/index
      :link-type: doc

      Architecture, components, network topologies, and design concepts. Start here if you are new to Omnia.

   .. grid-item-card:: :material-book-open-variant: Get Started  
      :link: GetStarted/index
      :link-type: doc

      End-to-end tutorials that take you from a bare set of PowerEdge servers to a fully operational cluster. Choose from Slurm-only, full deployment, Kubernetes + telemetry, or BuildStreaM paths.

   .. grid-item-card:: :material-book-open-variant: How-to Guides
      :link: HowTo/index
      :link-type: doc

      Task-oriented procedures for provisioning, configuring Slurm, Kubernetes, storage, networking, authentication, telemetry, and BuildStreaM.

   .. grid-item-card:: :material-book-open-variant: Reference
      :link: Reference/index
      :link-type: doc

      Configuration parameters, support matrices, playbook references, API documentation, and network port listings.

   .. grid-item-card:: :material-book-open-variant: Operations & Maintenance
      :link: Operations/index
      :link-type: doc

      Day-2 operations: adding and removing nodes, re-provisioning, OIM cleanup, log management, security hardening, and best practices.

   .. grid-item-card:: :material-book-open-variant: Troubleshooting
      :link: Troubleshooting/index
      :link-type: doc

      Symptom-driven guides for diagnosing and resolving issues with provisioning, Slurm, Kubernetes, telemetry, authentication, and more.


Quick Links
-----------



.. list-table::
   :header-rows: 1
   :widths: auto

   * - Resource
     - Description
   * - `Slurm Quickstart <GetStarted/slurm_quickstart.rst>`_
     - Fastest path to a working Slurm cluster (~2 hours, 4 nodes).
   * - `Full Deployment <GetStarted/full_deployment.rst>`_
     - Production deployment with Slurm, Kubernetes, telemetry, and LDAP.
   * - `Servers <Reference/SupportMatrix/servers.rst>`_
     - Supported OS versions, hardware, firmware, and software combinations.
   * - `Provision Config <Reference/Configuration/provision_config.rst>`_
     - Complete reference for all Omnia input configuration files.



Licensing
---------

Omnia is made available under the `Apache 2.0 license <https://opensource.org/licenses/Apache-2.0>`_.


.. note::

   Omnia playbooks are licensed under the Apache 2.0 license. Once an end-user initiates Omnia, that end-user will deploy other open-source and/or third-party software that is licensed separately by their respective developer communities and/or third parties. For a comprehensive list of software and their licenses, `click here <Reference/SupportMatrix/installed_software.rst>`_. Dell (or any other contributors) shall have no liability regarding (and no responsibility to provide support for) an end-user's use of any open-source and/or third-party software and Omnia users are solely responsible for ensuring that they are complying with all such licenses. Omnia is provided "as is" without any warranty, express or implied. Dell (or any other contributors) shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for an end-user's use of Omnia.



Previous Versions
-----------------

*For a better understanding of what Omnia does, check out the following:*

- `1.x documentation <https://omnia-doc.readthedocs.io/en/latest/index.html>`_: supports diskful provisioning.
- `2.x documentation <https://omnia.readthedocs.io/en/latest/index.html>`_: supports diskless provisioning and containerized deployment.


.. note::

   Upgrade from Omnia 1.x to 2.x is not supported due to architectural changes.



Omnia Community Members
-----------------------

* Dell Technologies: https://www.dell.com
* Intel: https://www.intel.com  
* University of Pisa: https://www.unipi.it
* Community Members
* VIZIAS
* Liqid: https://www.liqid.com


----


*If you have any feedback about Omnia documentation, please reach out at `omnia.readme@dell.com <mailto:omnia.readme@dell.com>`_.*
