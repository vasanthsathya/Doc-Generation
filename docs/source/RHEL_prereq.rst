Omnia common prerequisites
==========================

This section outlines the key prerequisites for setting up Omnia components, including
NFS configuration, OIM setup, and service Kubernetes cluster preparation.


NFS Server Prerequisites
----------------------------

* Choose an NFS server located outside your cluster.
* The NFS share has **755 permissions** and ``no_root_squash`` is enabled during mount.
* To enable ``no_root_squash``, edit the ``/etc/exports`` file on the NFS server and include the option for the exported path, run the following command:

  .. code-block:: bash

     /<your_exported_path>  *(rw,sync,no_root_squash,no_subtree_check)

* Ensure that the external NFS share is accessible from all nodes (both diskless and diskful)
  and is reachable via the admin network.


OIM (Omnia Infrastructure Manager) Prerequisites
-------------------------------------------------

* Choose a **server outside of your intended cluster** that meets the required :doc:`Storage Requirements <OmniaInstallGuide/RHEL_new/RHELSpace>` to function as the Omnia Infrastructure Manager (OIM).
* Ensure that the OIM has a full-featured RHEL operating system (OS) installed. For a complete list of supported RHEL versions, see the See :doc:`Support Matrix <Overview/SupportMatrix>`.
* Ensure that **Podman** container engine is installed on the OIM.
* The OIM must have **two active Network Interface Cards (NICs)**:
   * One connected to the **public network** (for downloading and storing packages and images).
   * One dedicated to **internal cluster communication**.
* Ensure that the OIM has **internet access**.
* Verify that **Git** is installed. If not, install it using:

     .. code-block:: bash

        dnf install git -y

* All target bare-metal servers (cluster nodes) must be **reachable from the OIM**.
* Clone the `Omnia artifacts repository <https://github.com/dell/omnia-artifactory/tree/omnia-container>`_  and build the container images as shown below:

     .. code-block:: bash

        git clone https://github.com/dell/omnia-artifactory.git
        cd omnia-artifactory
        ./build_images.sh all omnia_branch=<branch_name/tag name>

   * For detailed build instructions, refer to the
     `Omnia Artifacts README <https://github.com/dell/omnia-artifactory/blob/omnia-container/README.md>`_.

* Make sure that the required ports are open on the OIM node for cluster deployment. For detailed information on the required ports, refer to the :doc:`Omnia Ports <omnia_ports>`.


Repository Prerequisites
---------------------------

* Enable the **AppStream** and **BaseOS** repositories via the RHEL subscription manager.
* Ensure that RHEL has an **active subscription** or is configured to access **local repositories**.
* Verify that all **repository URLs** for the software packages are **accessible** — downloads will fail for inaccessible packages.
* For RHEL systems without a subscription, the repository URLs for ``x86_64_codeready-builder``, ``x86_64_appstream``, and ``x86_64_baseos`` are mandatory.
* Docker credentials are a mandatory requirement to pull in the essential packages during local repository deployment. 


Service Kubernetes Cluster Prerequisites
-------------------------------------

* A minimum of **three Kubernetes controller nodes** are available.

iDRAC Telemetry Metric Collection Prerequisites
-----------------------------------------------

* **Redfish** is enabled in iDRAC.
* **iDRAC firmware** is updated to the latest version.
* A **Datacenter license** is installed on all iDRAC interfaces.
* **Correct node service tags** are displayed on the iDRAC interface.
* For telemetry collection on the service cluster, ensure all **BMC (iDRAC) IPs** are **reachable** from the service cluster nodes.

Lightweight Directory Access Protocol (LDAP) Prerequisites
-----------------------------------------------------------

* LDAP server details required to configure the ``omnia_auth`` container as a proxy. The LDAP server details are required to configure OpenLDAP as a proxy server. See :doc:`Configure OpenLDAP as a proxy server <OmniaInstallGuide/RHEL_new/Authentication/OpenLDAP>`.

Lightweight Distributed Metric Service (LDMS) Prerequisites
-------------------------------------------------------------

* The LDMS RPM must be available in the user repository, and the ``ldms.json`` file should be updated accordingly. 
  If the LDMS RPM is not available, refer to  `Building LDMS PRODUCER RPM Package <https://github.com/dell/omnia-artifactory?tab=readme-ov-file#building-ldms-producer-rpm-package>`_ for instructions on building LDMS RPMs. 

Slurm Prerequisites
--------------------
* The Slurm RPM must be available in the user repository. If the Slurm RPM is not available, refer to `Slurm Quick Start Administrator Guide <https://slurm.schedmd.com/quickstart_admin.html>`_ for instructions on building Slurm RPMs.

