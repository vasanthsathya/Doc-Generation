.. _cli-reference-index:

CLI Reference
=============

This section provides comprehensive reference documentation for Omnia command-line interface commands.

.. note::
   This topic is pending SME validation. Content may change before publication.

.. toctree::
   :maxdepth: 2

   omnia-upgrade

Command Overview
----------------

The Omnia CLI provides commands for:

* **Cluster Management**: Provision, configure, and manage HPC clusters
* **Upgrade Operations**: Upgrade between Omnia versions with rollback capability
* **System Status**: Check version information and system health
* **Configuration Management**: Validate and modify cluster configurations

Upgrade Commands
----------------

Omnia 2.1 introduces new commands for upgrade management:

* ``omnia.sh --upgrade``: Initiate core container upgrade process
* ``omnia.sh --rollback``: Roll back to previous version using backups
* ``omnia.sh --version``: Display current version and system information

For detailed command reference, see :doc:`omnia-upgrade`.

Command Usage
------------

**Basic Usage Pattern**:
.. code-block:: bash

   ./omnia.sh [OPTIONS] COMMAND

**Common Options**:
- ``--help``: Display help information
- ``--version``: Show version information
- ``--verbose``: Enable verbose output

**Working Directory**:
Always run commands from the appropriate directory containing the correct version of the ``omnia.sh`` script for your target operation.

Related Topics
--------------

* :doc:`../../upgrade/how-to-upgrade-core`
* :doc:`../../upgrade/how-to-rollback-upgrade`
* :doc:`../../upgrade/concept-core-upgrade`
