.. _troubleshooting-upgrade-issues:

Troubleshooting Omnia Upgrade Issues
====================================

Systematic troubleshooting guidance for resolving common issues that may occur during Omnia core container upgrade, rollback, or input migration operations.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

When upgrade procedures fail or encounter errors, use this guide to identify and resolve issues quickly. The troubleshooting approach follows a symptom-cause-solution format for systematic problem resolution.

.. note::
   This topic is pending SME validation. Content may change before publication.

.. warning::
   Always create backups before attempting troubleshooting procedures. If issues persist, consider using the rollback procedure to restore system stability.

Common Upgrade Issues
---------------------

Upgrade Fails at Pre-Validation Phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
* Upgrade stops during Phase 1 (Pre-upgrade validation)
* Error messages about version incompatibility
* Container health check failures

**Causes:**
* Running incorrect Omnia version
* Target container image not available
* Insufficient disk space
* Container health issues

**Solutions:**

#. Verify current version:

   .. code-block:: bash

      ./omnia.sh --version

   Ensure you're running version 2.0.0.0 before upgrade.

#. Check container image availability:

   .. code-block:: bash

      podman images | grep omnia-core

   Look for the target image (e.g., omnia-core:2.1).

#. Verify disk space:

   .. code-block:: bash

      df -h /opt/omnia

   Ensure at least 2 GB free space available.

#. Check container health:

   .. code-block:: bash

      podman ps | grep omnia-core

   Container should be running and healthy.

#. If image missing, build required image:

   .. code-block:: bash

      ./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev

Backup Creation Failures
~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
* Upgrade stops during Phase 3 (Backup creation)
* Error messages about backup directory creation
* Permission denied errors

**Causes:**
* Insufficient permissions
* Disk space issues
* NFS mount problems
* File system errors

**Solutions:**

#. Check permissions on backup directory:

   .. code-block:: bash

      ls -la /opt/omnia/backups

   Verify write permissions for backup location.

#. Verify NFS mount status:

   .. code-block:: bash

      mount | grep nfs

   Ensure NFS share is properly mounted.

#. Check available disk space:

   .. code-block:: bash

      df -h /opt/omnia

   Free up space if necessary.

#. Manually create backup directory:

   .. code-block:: bash

      sudo mkdir -p /opt/omnia/backups/upgrade_test
      sudo chmod 755 /opt/omnia/backups/upgrade_test

Container Swap Issues
~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
* Upgrade stops during Phase 4 (Container swap)
* Container fails to stop or start
* Timeout errors during container operations

**Causes:**
* Container dependency issues
* Resource constraints
* Configuration problems
* System resource conflicts

**Solutions:**

#. Check container status:

   .. code-block:: bash

      podman ps -a | grep omnia-core

   Note container states and any error messages.

#. Force stop problematic container:

   .. code-block:: bash

      sudo podman stop omnia-core
      sudo podman rm omnia-core

#. Check system resources:

   .. code-block:: bash

      free -h
      df -h

   Ensure sufficient memory and disk space.

#. Review container logs:

   .. code-block:: bash

      sudo podman logs omnia-core

   Look for error messages or startup issues.

#. Restart container services:

   .. code-block:: bash

      sudo systemctl restart podman
      sudo systemctl restart omnia-core

Input Migration Errors
~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
* Migration playbook fails during Phase 5
* Input file transformation errors
* Syntax validation failures
* Missing parameter errors

**Causes:**
* Corrupted backup files
* Invalid input file syntax
* Missing required parameters
* Version incompatibility issues

**Solutions:**

#. Verify backup integrity:

   .. code-block:: bash

      ls -la /opt/omnia/backups/upgrade_*/input

   Check that backup files exist and are not corrupted.

#. Validate input file syntax:

   .. code-block:: bash

      ansible-playbook --syntax-check /omnia/upgrade/upgrade_omnia.yml

   Fix any syntax errors reported.

#. Check migration logs:

   .. code-block:: bash

      cat /var/log/omnia/migration.log

   [TO BE PROVIDED: Actual log location]

#. Manually review input files:

   .. code-block:: bash

      cat /opt/omnia/input/omnia.yml

   Look for obvious syntax or configuration issues.

#. Re-run migration with verbose output:

   .. code-block:: bash

      ansible-playbook -v /omnia/upgrade/upgrade_omnia.yml

Rollback Failures
~~~~~~~~~~~~~~~~

**Symptoms:**
* Rollback process stops midway
* Unable to restore from backup
* Container fails to start after rollback
* Metadata update failures

**Causes:**
* Corrupted backup files
* Missing backup directory
* Container image issues
* Permission problems

**Solutions:**

#. Verify backup exists:

   .. code-block:: bash

      ls -la /opt/omnia/backups/

   Look for timestamped backup directories.

#. Check backup integrity:

   .. code-block:: bash

      find /opt/omnia/backups/upgrade_* -name "*.yml" -exec echo "Checking {}" \; -exec head -1 {} \;

   Verify backup files are not empty or corrupted.

#. Manually restore inputs:

   .. code-block:: bash

      sudo cp -r /opt/omnia/backups/upgrade_*/input/* /opt/omnia/input/

#. Reset metadata manually:

   .. code-block:: bash

      sudo sed -i 's/omnia_version: 2.1.0.0/omnia_version: 2.0.0.0/' /opt/omnia/.data/oim_metadata.yml

#. Restart services:

   .. code-block:: bash

      sudo systemctl restart omnia-core

Performance Issues During Upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
* Upgrade process is very slow
* Timeout errors during operations
* System becomes unresponsive

**Causes:**
* Insufficient system resources
* Network connectivity issues
* Large data volumes
* I/O bottlenecks

**Solutions:**

#. Monitor system resources:

   .. code-block:: bash

      top
      iostat 1 5

   Identify resource bottlenecks.

#. Check network connectivity:

   .. code-block:: bash

      ping google.com
      curl -I https://hub.docker.com

   Verify network access for image operations.

#. Optimize system performance:

   .. code-block:: bash

      echo 3 > /proc/sys/vm/drop_caches
      sync

   Clear system caches if needed.

#. Extend timeout values:

   [TO BE PROVIDED: Method to adjust upgrade timeouts]

Network Connectivity Problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
* Image pull failures
* Connection timeout errors
* DNS resolution issues

**Causes:**
* Firewall restrictions
* Proxy configuration issues
* DNS problems
* Network outages

**Solutions:**

#. Test network connectivity:

   .. code-block:: bash

      curl -I https://registry.hub.docker.com
      nslookup registry.hub.docker.com

#. Check firewall settings:

   .. code-block:: bash

      sudo iptables -L | grep -i docker
      sudo firewall-cmd --list-all

#. Verify proxy configuration:

   .. code-block:: bash

      echo $HTTP_PROXY
      echo $HTTPS_PROXY

#. Configure Docker daemon for proxy:

   [TO BE PROVIDED: Proxy configuration steps]

Validation Failures
~~~~~~~~~~~~~~~~~~

**Symptoms:**
* Post-upgrade validation fails
* Health check timeouts
* Service startup failures

**Causes:**
* Configuration errors
* Service dependency issues
* Resource constraints
* Timing problems

**Solutions:**

#. Check service status:

   .. code-block:: bash

      sudo systemctl status omnia-core
      sudo journalctl -u omnia-core -f

#. Verify configuration:

   .. code-block:: bash

      ansible-playbook --syntax-check /omnia/upgrade/upgrade_omnia.yml

#. Extend health check timeout:

   [TO BE PROVIDED: Health check timeout adjustment]

#. Manual validation:

   .. code-block:: bash

      ./omnia.sh --version
      podman ps | grep omnia-core

Advanced Troubleshooting
------------------------

Log Analysis
~~~~~~~~~~~~

Collect and analyze logs for detailed troubleshooting:

#. System logs:

   .. code-block:: bash

      sudo journalctl -u omnia-core --since "1 hour ago"

#. Upgrade logs:

   .. code-block:: bash

      cat /opt/omnia/logs/upgrade.log

   [TO BE PROVIDED: Actual log locations]

#. Container logs:

   .. code-block:: bash

      sudo podman logs omnia-core --tail 100

#. Migration logs:

   .. code-block:: bash

      cat /var/log/ansible.log

Backup and Recovery
~~~~~~~~~~~~~~~~~~

For critical situations, ensure you have reliable backups:

#. Create manual backup:

   .. code-block:: bash

      sudo cp -r /opt/omnia /opt/omnia_manual_backup_$(date +%Y%m%d_%H%M%S)

#. Verify backup integrity:

   .. code-block:: bash

      find /opt/omnia_manual_backup_* -type f | xargs md5sum

#. Document current state:

   .. code-block:: bash

      ./omnia.sh --version > current_state.txt
      podman ps -a >> current_state.txt

When to Contact Support
~~~~~~~~~~~~~~~~~~~~

Contact support if:

* Multiple upgrade attempts fail
* System becomes unstable after upgrade
* Critical data appears to be lost
* Rollback procedures fail
* [TO BE PROVIDED: Additional support criteria]

Provide the following information when requesting support:

* Current and target Omnia versions
* Complete error messages and logs
* Steps taken before the issue occurred
* System configuration details
* Backup status and availability

**Related topics:**
* :doc:`how-to-perform-upgrade`
* :doc:`how-to-rollback-upgrade`
* :doc:`reference-upgrade-commands`
