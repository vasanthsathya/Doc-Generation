.. _how-to-migrate-inputs:

Migrating Input Files After Core Container Upgrade
=================================================

.. note::
   This topic is pending SME validation. Content may change before publication.

After completing the core container upgrade, migrate your Omnia 2.0 input files to the 2.1 format to enable new features and ensure compatibility with the upgraded system. This procedure transforms your existing configurations while preserving your custom settings.

.. contents:: On This Page
   :local:
   :depth: 2

Prerequisites
-------------

Before migrating input files:

* Complete the core container upgrade from 2.0 to 2.1
* Access to the upgraded Omnia core 1.1 container
* Verify the backup directory contains your original 2.0 input files
* Ensure you have the upgrade lock file removed if previous migration was attempted

.. important::
   You must be inside the upgraded Omnia core container to perform input file migration. Access the container using ``podman exec -it omnia-core bash``.

Procedure
---------

#. Access the upgraded Omnia core container.

.. code-block:: bash

   podman exec -it omnia-core bash

You should now be inside the Omnia core 1.1 container running version 2.1.

#. Navigate to the upgrade directory.

.. code-block:: bash

   cd /omnia/upgrade

#. Verify the backup contains your original input files.

.. code-block:: bash

   ls -la /opt/omnia/backups/upgrade_*/input/

Expected output shows your original 2.0 input files:

.. code-block:: text

   network_config.yml
   storage_config.yml
   scheduler_config.yml
   security_config.yml

#. Run the input file migration playbook.

.. code-block:: bash

   ansible-playbook /omnia/upgrade/upgrade_omnia.yml

The migration process:
- Reads existing 2.0 input files from backup
- Transforms configurations to 2.1 format
- Adds new parameters and structure
- Validates migrated file syntax
- Preserves your custom settings

#. Review the migration results.

The playbook displays:
- Files successfully migrated
- New parameters added
- Manual configuration requirements
- Validation results

Example output:

.. code-block:: text

   PLAY [Upgrade Omnia input files from 2.0 to 2.1] *************************

   TASK [upgrade_oim : Read 2.0 input files] *********************************
   ok: [localhost]

   TASK [upgrade_oim : Transform to 2.1 format] ******************************
   changed: [localhost]

   TASK [upgrade_oim : Add new parameters] ***********************************
   changed: [localhost]

   TASK [upgrade_oim : Validate migrated files] *****************************
   ok: [localhost]

   PLAY RECAP *****************************************************************
   localhost : ok=4    changed=2    unreachable=0    failed=0

#. Address any manual configuration requirements.

The migration may identify parameters that need manual attention:

**New IB Network Configuration**:
- ``ib_network`` parameter added to network configuration
- Default value provided but may need customization

**Enhanced Configuration Sources**:
- ``config_sources`` parameter structure updated
- Multiple source types now supported

Review the migration output for specific manual steps needed.

#. Validate the migrated input files.

.. code-block:: bash

   ansible-playbook /omnia/upgrade/validate_migrated_inputs.yml

Expected output shows validation results:

.. code-block:: text

   PLAY [Validate migrated input files] *************************************

   TASK [validate : Check YAML syntax] **************************************
   ok: [localhost]

   TASK [validate : Verify required parameters] ****************************
   ok: [localhost]

   TASK [validate : Check parameter values] *********************************
   ok: [localhost]

   PLAY RECAP *****************************************************************
   localhost : ok=3    changed=0    unreachable=0    failed=0

#. Review the new configuration structure.

Examine the migrated input files to understand the changes:

.. code-block:: bash

   cat /opt/omnia/input/network_config.yml

Look for new sections like:

.. code-block:: yaml

   # New in 2.1
   ib_network:
     enabled: true
     interface: ib0
     subnet: 192.168.100.0/24

   # Enhanced in 2.1
   config_sources:
     - type: local
       path: /opt/omnia/config
     - type: nfs
       server: nfs.example.com
       path: /shared/config

Result
------

Your input files are now migrated to Omnia 2.1 format with:
- Original custom settings preserved
- New parameters added with default values
- Configuration structure updated for 2.1 compatibility
- YAML syntax validated

Verification
------------

Verify the migration completed successfully:

#. Check input file locations and permissions.

.. code-block:: bash

   ls -la /opt/omnia/input/

Expected output shows migrated files with proper permissions.

#. Test configuration syntax.

.. code-block:: bash

   ansible-playbook /omnia/upgrade/test_syntax.yml

Expected output shows all files pass syntax validation.

#. Verify new parameters are present.

.. code-block:: bash

   grep -r "ib_network" /opt/omnia/input/
   grep -r "config_sources" /opt/omnia/input/

Expected output shows new parameters in appropriate configuration files.

#. Confirm the upgrade lock is removed.

.. code-block:: bash

   ls -la /opt/omnia/.data/upgrade_in_progress.lock

Expected output: No such file or directory (lock file should be removed).

Next Steps
----------

After completing input file migration:

#. **Review New Parameters**: Examine new 2.1 parameters and customize as needed for your environment.

#. **Test Configuration**: Validate that the migrated configuration works with your cluster setup.

#. **Plan Cluster Reprovisioning**: If you want to use new 2.1 features, plan for cluster reprovisioning.

#. **Document Changes**: Update your documentation to reflect the new configuration structure.

.. tip::
   Keep a copy of the migration output for your records. It provides a valuable audit trail of the changes made during the upgrade.

Manual Reconfiguration Option
-----------------------------

If you prefer not to use the automatic migration, you can manually reconfigure the default input files:

#. Remove the upgrade lock file.

.. code-block:: bash

   rm /opt/omnia/.data/upgrade_in_progress.lock

#. Manually edit the default 2.1 input files.

.. code-block:: bash

   vi /opt/omnia/input/network_config.yml

#. Copy your custom settings from the backup.

.. code-block:: bash

   cp /opt/omnia/backups/upgrade_*/input/custom_settings.yml /opt/omnia/input/

.. warning::
   Manual reconfiguration requires careful attention to parameter compatibility between 2.0 and 2.1 formats. Use the automatic migration unless you have specific reasons to manual configure.

Troubleshooting
---------------

Common migration issues and solutions:

**Migration Playbook Fails**:
- Check backup file permissions and accessibility
- Verify sufficient disk space for migration operations
- Review playbook error messages for specific issues

**Validation Errors**:
- Check YAML syntax in migrated files
- Verify required parameters are present
- Review parameter value formats and types

**Missing Parameters**:
- Compare with backup files to identify missing settings
- Add missing parameters manually if needed
- Run validation again after corrections

**Lock File Issues**:
- Remove lock file if migration was interrupted: ``rm /opt/omnia/.data/upgrade_in_progress.lock``
- Ensure no other migration processes are running

For detailed troubleshooting guidance, see :doc:`../troubleshooting/upgrade-issues`.

Related Topics
--------------

* :doc:`concept-core-upgrade`
* :doc:`how-to-upgrade-core`
* :doc:`how-to-rollback-upgrade`
* :doc:`../reference/config/input-files`
