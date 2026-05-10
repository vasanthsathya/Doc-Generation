
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
   :margin: 2 0 2 0

   .. grid-item-card:: :material-book-open-variant: Overview
      :link: Overview/index
      :link-type: doc
      :class-card: grid-card

      Architecture, components, network topologies, and design concepts. Start here if you are new to Omnia.

   .. grid-item-card:: :material-rocket-launch: Get Started  
      :link: GetStarted/index
      :link-type: doc
      :class-card: grid-card

      End-to-end tutorials that take you from a bare set of PowerEdge servers to a fully operational cluster. Choose from Slurm-only, full deployment, Kubernetes + telemetry, or BuildStreaM paths.

   .. grid-item-card:: :material-tools: How-to Guides
      :link: HowTo/index
      :link-type: doc
      :class-card: grid-card

      Task-oriented procedures for provisioning, configuring Slurm, Kubernetes, storage, networking, authentication, telemetry, and BuildStreaM.

   .. grid-item-card:: :material-book: Reference
      :link: Reference/index
      :link-type: doc
      :class-card: grid-card

      Configuration parameters, support matrices, playbook references, API documentation, and network port listings.

   .. grid-item-card:: :material-cog: Operations & Maintenance
      :link: Operations/index
      :link-type: doc
      :class-card: grid-card

      Day-2 operations: adding and removing nodes, re-provisioning, OIM cleanup, log management, security hardening, and best practices.

   .. grid-item-card:: :material-bug: Troubleshooting
      :link: Troubleshooting/index
      :link-type: doc
      :class-card: grid-card

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

.. raw:: html

   <div class="community-logos">
     <a href="https://www.dell.com" target="_blank" rel="noopener noreferrer">
       <img src="images/logos/delltech.jpg" alt="Dell Technologies" style="height: 60px;">
     </a>
     <a href="https://www.intel.com" target="_blank" rel="noopener noreferrer">
       <img src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Intel_logo_%282020%2C_light_blue%29.svg" alt="Intel" style="height: 40px;">
     </a>
     <a href="https://www.unipi.it" target="_blank" rel="noopener noreferrer">
       <img src="images/logos/pisa.png" alt="University of Pisa" style="height: 60px;">
     </a>
     <img src="https://user-images.githubusercontent.com/83095575/117071024-64956c80-ace3-11eb-9d90-2dac7daef11c.png" alt="Community Member" style="height: 60px;">
     <img src="https://images.squarespace-cdn.com/content/v1/660f1a48587dbb2769709a33/9ac5520f-a308-4751-80f4-415d07a23473/VIZIAS+Blue.png" alt="VIZIAS" style="height: 60px;">
     <img src="https://user-images.githubusercontent.com/5414112/153955170-0a4b199a-54f0-42af-939c-03eac76881c0.png" alt="Community Member" style="height: 60px;">
     <a href="https://www.liqid.com" target="_blank" rel="noopener noreferrer">
       <img src="images/logos/Liqid.png" alt="Liqid" style="height: 50px;">
     </a>
   </div>


----


*If you have any feedback about Omnia documentation, please reach out at `omnia.readme@dell.com <mailto:omnia.readme@dell.com>`_.*
