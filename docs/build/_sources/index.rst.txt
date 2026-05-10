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

.. raw:: html

   <div class="grid cards">
   <ul>
   <li>
   <p><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.5c-1.35-.85-3.8-1.5-5.5-1.5-1.65 0-3.35.3-4.75 1.05-.1.05-.15.05-.25.05-.25 0-.5-.25-.5-.5V6c.6-.45 1.25-.75 2-1 1.11-.35 2.33-.5 3.5-.5 1.95 0 4.05.4 5.5 1.5 1.45-1.1 3.55-1.5 5.5-1.5 1.17 0 2.39.15 3.5.5.75.25 1.4.55 2 1v14.6c0 .25-.25.5-.5.5-.1 0-.15 0-.25-.05-1.4-.75-3.1-1.05-4.75-1.05-1.7 0-4.15.65-5.5 1.5M12 8v11.5c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5V7c-1.1-.35-2.3-.5-3.5-.5-1.7 0-4.15.65-5.5 1.5m1 3.5c1.11-.68 2.6-1 4.5-1 .91 0 1.76.09 2.5.28V9.23c-.87-.15-1.71-.23-2.5-.23q-2.655 0-4.5.84zm4.5.17c-1.71 0-3.21.26-4.5.79v1.69c1.11-.65 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24v-1.5c-.87-.16-1.71-.23-2.5-.23m2.5 2.9c-.87-.16-1.71-.24-2.5-.24-1.83 0-3.33.27-4.5.8v1.69c1.11-.66 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24z"/></svg></span> <strong><a href="Overview/index.html">Overview</a></strong></p>
   <hr />
   <p>Architecture, components, network topologies, and design concepts. Start here if you are new to Omnia.</p>
   </li>
   <li>
   <p><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.5c-1.35-.85-3.8-1.5-5.5-1.5-1.65 0-3.35.3-4.75 1.05-.1.05-.15.05-.25.05-.25 0-.5-.25-.5-.5V6c.6-.45 1.25-.75 2-1 1.11-.35 2.33-.5 3.5-.5 1.95 0 4.05.4 5.5 1.5 1.45-1.1 3.55-1.5 5.5-1.5 1.17 0 2.39.15 3.5.5.75.25 1.4.55 2 1v14.6c0 .25-.25.5-.5.5-.1 0-.15 0-.25-.05-1.4-.75-3.1-1.05-4.75-1.05-1.7 0-4.15.65-5.5 1.5M12 8v11.5c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5V7c-1.1-.35-2.3-.5-3.5-.5-1.7 0-4.15.65-5.5 1.5m1 3.5c1.11-.68 2.6-1 4.5-1 .91 0 1.76.09 2.5.28V9.23c-.87-.15-1.71-.23-2.5-.23q-2.655 0-4.5.84zm4.5.17c-1.71 0-3.21.26-4.5.79v1.69c1.11-.65 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24v-1.5c-.87-.16-1.71-.23-2.5-.23m2.5 2.9c-.87-.16-1.71-.24-2.5-.24-1.83 0-3.33.27-4.5.8v1.69c1.11-.66 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24z"/></svg></span> <strong><a href="GetStarted/index.html">Get Started</a></strong></p>
   <hr />
   <p>End-to-end tutorials that take you from a bare set of PowerEdge servers to a fully operational cluster. Choose from Slurm-only, full deployment, Kubernetes + telemetry, or BuildStreaM paths.</p>
   </li>
   <li>
   <p><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.5c-1.35-.85-3.8-1.5-5.5-1.5-1.65 0-3.35.3-4.75 1.05-.1.05-.15.05-.25.05-.25 0-.5-.25-.5-.5V6c.6-.45 1.25-.75 2-1 1.11-.35 2.33-.5 3.5-.5 1.95 0 4.05.4 5.5 1.5 1.45-1.1 3.55-1.5 5.5-1.5 1.17 0 2.39.15 3.5.5.75.25 1.4.55 2 1v14.6c0 .25-.25.5-.5.5-.1 0-.15 0-.25-.05-1.4-.75-3.1-1.05-4.75-1.05-1.7 0-4.15.65-5.5 1.5M12 8v11.5c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5V7c-1.1-.35-2.3-.5-3.5-.5-1.7 0-4.15.65-5.5 1.5m1 3.5c1.11-.68 2.6-1 4.5-1 .91 0 1.76.09 2.5.28V9.23c-.87-.15-1.71-.23-2.5-.23q-2.655 0-4.5.84zm4.5.17c-1.71 0-3.21.26-4.5.79v1.69c1.11-.65 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24v-1.5c-.87-.16-1.71-.23-2.5-.23m2.5 2.9c-.87-.16-1.71-.24-2.5-.24-1.83 0-3.33.27-4.5.8v1.69c1.11-.66 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24z"/></svg></span> <strong><a href="HowTo/index.html">How-to Guides</a></strong></p>
   <hr />
   <p>Task-oriented procedures for provisioning, configuring Slurm, Kubernetes, storage, networking, authentication, telemetry, and BuildStreaM.</p>
   </li>
   <li>
   <p><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.5c-1.35-.85-3.8-1.5-5.5-1.5-1.65 0-3.35.3-4.75 1.05-.1.05-.15.05-.25.05-.25 0-.5-.25-.5-.5V6c.6-.45 1.25-.75 2-1 1.11-.35 2.33-.5 3.5-.5 1.95 0 4.05.4 5.5 1.5 1.45-1.1 3.55-1.5 5.5-1.5 1.17 0 2.39.15 3.5.5.75.25 1.4.55 2 1v14.6c0 .25-.25.5-.5.5-.1 0-.15 0-.25-.05-1.4-.75-3.1-1.05-4.75-1.05-1.7 0-4.15.65-5.5 1.5M12 8v11.5c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5V7c-1.1-.35-2.3-.5-3.5-.5-1.7 0-4.15.65-5.5 1.5m1 3.5c1.11-.68 2.6-1 4.5-1 .91 0 1.76.09 2.5.28V9.23c-.87-.15-1.71-.23-2.5-.23q-2.655 0-4.5.84zm4.5.17c-1.71 0-3.21.26-4.5.79v1.69c1.11-.65 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24v-1.5c-.87-.16-1.71-.23-2.5-.23m2.5 2.9c-.87-.16-1.71-.24-2.5-.24-1.83 0-3.33.27-4.5.8v1.69c1.11-.66 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24z"/></svg></span> <strong><a href="Reference/index.html">Reference</a></strong></p>
   <hr />
   <p>Configuration parameters, support matrices, playbook references, API documentation, and network port listings.</p>
   </li>
   <li>
   <p><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.5c-1.35-.85-3.8-1.5-5.5-1.5-1.65 0-3.35.3-4.75 1.05-.1.05-.15.05-.25.05-.25 0-.5-.25-.5-.5V6c.6-.45 1.25-.75 2-1 1.11-.35 2.33-.5 3.5-.5 1.95 0 4.05.4 5.5 1.5 1.45-1.1 3.55-1.5 5.5-1.5 1.17 0 2.39.15 3.5.5.75.25 1.4.55 2 1v14.6c0 .25-.25.5-.5.5-.1 0-.15 0-.25-.05-1.4-.75-3.1-1.05-4.75-1.05-1.7 0-4.15.65-5.5 1.5M12 8v11.5c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5V7c-1.1-.35-2.3-.5-3.5-.5-1.7 0-4.15.65-5.5 1.5m1 3.5c1.11-.68 2.6-1 4.5-1 .91 0 1.76.09 2.5.28V9.23c-.87-.15-1.71-.23-2.5-.23q-2.655 0-4.5.84zm4.5.17c-1.71 0-3.21.26-4.5.79v1.69c1.11-.65 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24v-1.5c-.87-.16-1.71-.23-2.5-.23m2.5 2.9c-.87-.16-1.71-.24-2.5-.24-1.83 0-3.33.27-4.5.8v1.69c1.11-.66 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24z"/></svg></span> <strong><a href="Operations/index.html">Operations &amp; Maintenance</a></strong></p>
   <hr />
   <p>Day-2 operations: adding and removing nodes, re-provisioning, OIM cleanup, log management, security hardening, and best practices.</p>
   </li>
   <li>
   <p><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 21.5c-1.35-.85-3.8-1.5-5.5-1.5-1.65 0-3.35.3-4.75 1.05-.1.05-.15.05-.25.05-.25 0-.5-.25-.5-.5V6c.6-.45 1.25-.75 2-1 1.11-.35 2.33-.5 3.5-.5 1.95 0 4.05.4 5.5 1.5 1.45-1.1 3.55-1.5 5.5-1.5 1.17 0 2.39.15 3.5.5.75.25 1.4.55 2 1v14.6c0 .25-.25.5-.5.5-.1 0-.15 0-.25-.05-1.4-.75-3.1-1.05-4.75-1.05-1.7 0-4.15.65-5.5 1.5M12 8v11.5c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5V7c-1.1-.35-2.3-.5-3.5-.5-1.7 0-4.15.65-5.5 1.5m1 3.5c1.11-.68 2.6-1 4.5-1 .91 0 1.76.09 2.5.28V9.23c-.87-.15-1.71-.23-2.5-.23q-2.655 0-4.5.84zm4.5.17c-1.71 0-3.21.26-4.5.79v1.69c1.11-.65 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24v-1.5c-.87-.16-1.71-.23-2.5-.23m2.5 2.9c-.87-.16-1.71-.24-2.5-.24-1.83 0-3.33.27-4.5.8v1.69c1.11-.66 2.6-.99 4.5-.99 1.04 0 1.88.08 2.5.24z"/></svg></span> <strong><a href="Troubleshooting/index.html">Troubleshooting</a></strong></p>
   <hr />
   <p>Symptom-driven guides for diagnosing and resolving issues with provisioning, Slurm, Kubernetes, telemetry, authentication, and more.</p>
   </li>
   </ul>
   </div>

.. toctree::
   :hidden:

   Home <self>
   Overview/index
   GetStarted/index
   HowTo/index
   Operations/index
   Reference/index
   Troubleshooting/index
   Contributing/index


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


*If you have any feedback about Omnia documentation, please reach out at omnia.readme@dell.com.*
