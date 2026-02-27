.. _troubleshooting-upgrade-issues:

Troubleshooting Omnia Upgrade Issues
=====================================

.. note::
   This topic is pending SME validation. Content may change before publication.

Resolve common issues that may occur during the Omnia 2.0 to 2.1 upgrade process. This guide helps you identify symptoms, understand causes, and apply solutions for upgrade failures, backup problems, and container issues.

.. contents:: On This Page
   :local:
   :depth: 2

Upgrade Validation Failures
---------------------------

**Symptoms**: Upgrade stops during pre-upgrade validation with error messages.

**Common Causes**:
- Incorrect current version (not 2.0.0.0)
- Missing 2.1 container image
- Insufficient disk space
- Permission issues
- Network connectivity problems

**Solutions**:

#. Verify current version.

.. code-block:: bash

   ./omnia.sh --version

Expected output should show version 2.0.0.0 with core container 1.0.

#. Pull the required container image.

.. code-block:: bash

   ./build_images.sh core core_tag=2.1 omnia_branch=pub/q1_dev

#. Check available disk space.

.. code-block:: bash

   df -h /opt/omnia

Ensure at least 2 GB of free space is available.

#. Verify permissions.

.. code-block:: bash

   ls -la /opt/omnia
   sudo chown -R omnia:omnia /opt/omnia  # if needed

**Prevention**:
- Always verify prerequisites before starting upgrade
- Ensure sufficient disk space is available
- Test network connectivity to container registries

Backup Creation Failures
------------------------

**Symptoms**: Upgrade fails during backup creation phase with file copy errors.

**Common Causes**:
- Insufficient disk space for backup
- Permission denied on source files
- Network file system issues
- Corrupted source files

**Solutions**:

#. Check disk space.

.. code-block:: bash

   df -h /opt/omnia/backups

If space is insufficient, clean up old backups or expand storage.

#. Verify file permissions.

.. code-block:: bash

   ls -la /opt/omnia/input/
   sudo chmod -R 644 /opt/omnia/input/  # if needed

#. Test file system integrity.

.. code-block:: bash

   fsck -n /dev/sdX  # replace with actual file system device

#. Manually create test backup.

.. code-block:: bash

   mkdir -p /tmp/test_backup
   cp -r /opt/omnia/input/* /tmp/test_backup/
   ls -la /tmp/test_backup/

**Prevention**:
- Regular cleanup of old backup directories
- Monitor disk space usage trends
- Implement file system health checks

Container Swap Problems
-----------------------

**Symptoms**: Upgrade fails during container swap with timeout or start failures.

**Common Causes**:
- Container image corruption
- Insufficient system resources
- Port conflicts
- Configuration file errors
- Network issues

**Solutions**:

#. Check container status.

.. code-block:: bash

   podman ps -a | grep omnia-core
   podman logs omnia-core

#. Verify container image integrity.

.. code-block:: bash

   podman images | grep omnia
   podman inspect omnia-core:1.1

#. Check system resources.

.. code-block:: bash

   free -h
   df -h
   top

#. Force stop problematic containers.

.. code-block:: bash

   podman kill omnia-core
   podman rm omnia-core

#. Manually start container.

.. code-block:: bash

   podman run -d --name omnia-core omnia-core:1.1

**Prevention**:
- Monitor system resource usage
- Regular container health checks
- Keep container images updated

Input File Migration Issues
---------------------------

**Symptoms**: Migration playbook fails or produces invalid configurations.

**Common Causes**:
- Corrupted backup files
- YAML syntax errors in source files
- Missing required parameters
- Permission issues on target files
- Lock file conflicts

**Solutions**:

#. Check backup file integrity.

.. code-block:: bash

   ls -la /opt/omnia/backups/upgrade_*/input/
   yaml-lint /opt/omnia/backups/upgrade_*/input/*.yml

#. Remove lock file if present.

.. code-block:: bash

   rm -f /opt/omnia/.data/upgrade_in_progress.lock

#. Manually validate YAML syntax.

.. code-block:: bash

   ansible-playbook --syntax-check /omnia/upgrade/upgrade_omnia.yml

#. Test migration with dry run.

.. code-block:: bash

   ansible-playbook --check /omnia/upgrade/upgrade_omnia.yml

#. Manually edit problematic files.

.. code-block:: bash

   vi /opt/omnia/input/problem_file.yml

**Prevention**:
- Validate input files before upgrade
- Keep backup files secure and accessible
- Test migration in non-production environment

Rollback Failures
-----------------

**Symptoms**: Rollback process fails to restore previous version.

**Common Causes**:
- Missing or corrupted backup
- Container image unavailable
- Metadata file corruption
- Permission issues
- Insufficient disk space

**Solutions**:

#. Verify backup availability.

.. code-block:: bash

   ls -la /opt/omnia/backups/
   find /opt/omnia/backups/ -name "upgrade_*" -type d

#. Check backup integrity.

.. code-block:: bash

   ls -la /opt/omnia/backups/upgrade_<timestamp>/
   cat /opt/omnia/backups/upgrade_<timestamp>/manifest.txt

#. Verify required container image.

.. code-block:: bash

   podman images | grep omnia-core:1.0

#. Check metadata file.

.. code-block:: bash

   cat /opt/omnia/.data/oim_metadata.yml
   yaml-lint /opt/omnia/.data/oim_metadata.yml

#. Perform manual rollback if needed.

.. code-block:: bash

   # Stop current container
   podman stop omnia-core
   
   # Restore files manually
   cp -r /opt/omnia/backups/upgrade_<timestamp>/input/* /opt/omnia/input/
   
   # Start previous container
   podman run -d --name omnia-core omnia-core:1.0

**Prevention**:
- Verify backup integrity immediately after creation
- Keep multiple backup versions when possible
- Regularly test rollback procedures

Command and Script Issues
-------------------------

**Symptoms**: ``omnia.sh`` commands fail with unexpected errors or permission denied.

**Common Causes**:
- Incorrect script version
- Permission issues on script file
- Missing dependencies
- Environment variable problems
- Path issues

**Solutions**:

#. Verify script version and permissions.

.. code-block:: bash

   ./omnia.sh --version
   ls -la omnia.sh
   chmod +x omnia.sh

#. Check script dependencies.

.. code-block:: bash

   which podman
   which ansible
   which python3

#. Verify environment variables.

.. code-block:: bash

   env | grep -i omnia
   echo $PATH

#. Test script with verbose output.

.. code-block:: bash

   bash -x ./omnia.sh --version

**Prevention**:
- Use correct script version for target Omnia version
- Maintain proper file permissions
- Keep dependencies updated

Performance and Resource Issues
------------------------------

**Symptoms**: System becomes slow or unresponsive during upgrade.

**Common Causes**:
- Insufficient memory
- High CPU usage
- Disk I/O bottlenecks
- Network congestion
- Resource contention

**Solutions**:

#. Monitor system resources.

.. code-block:: bash

   top
   iotop
   df -h
   free -h

#. Check process status.

.. code-block:: bash

   ps aux | grep omnia
   ps aux | grep podman

#. Optimize system performance.

.. code-block:: bash

   # Clear caches if needed
   echo 3 > /proc/sys/vm/drop_caches
   
   # Stop non-essential services
   sudo systemctl stop non-essential-service

#. Schedule upgrade during low-usage periods.

**Prevention**:
- Monitor resource usage trends
- Plan upgrades during maintenance windows
- Have resource monitoring in place

Network and Connectivity Issues
------------------------------

**Symptoms**: Upgrade fails due to network problems or connectivity issues.

**Common Causes**:
- Firewall blocking
- DNS resolution problems
- Container registry access issues
- Network file system problems
- Bandwidth limitations

**Solutions**:

#. Test network connectivity.

.. code-block:: bash

   ping docker.io
   nslookup registry.docker.io
   curl -I https://registry.docker.io

#. Check firewall rules.

.. code-block:: bash

   sudo iptables -L
   sudo firewall-cmd --list-all

#. Verify NFS connectivity (if using).

.. code-block:: bash

   showmount -e nfs-server
   mount | grep nfs

#. Test container registry access.

.. code-block:: bash

   podman login docker.io
   podman pull hello-world

**Prevention**:
- Test network connectivity before upgrade
- Ensure firewall rules allow required traffic
- Monitor network performance during upgrade

Diagnostic Commands
-------------------

Use these commands to diagnose upgrade issues:

**System Information**:
.. code-block:: bash

   uname -a
   cat /etc/os-release
   df -h
   free -h

**Container Status**:
.. code-block:: bash

   podman ps -a
   podman images
   podman logs omnia-core

**Omnia Status**:
.. code-block:: bash

   ./omnia.sh --version
   cat /opt/omnia/.data/oim_metadata.yml
   ls -la /opt/omnia/

**Backup Status**:
.. code-block:: bash

   ls -la /opt/omnia/backups/
   find /opt/omnia/backups/ -name "upgrade_*" -type d -exec ls -la {} \;

**Process Status**:
.. code-block:: bash

   ps aux | grep omnia
   ps aux | grep podman
   netstat -tulpn | grep :8080

**Log Files**:
.. code-block:: bash

   tail -f /var/log/omnia/upgrade.log
   journalctl -u omnia-service
   tail -f /var/log/podman/podman.log

Getting Help
------------

If you encounter issues not covered in this guide:

#. **Collect Diagnostic Information**:
   - Save error messages and logs
   - Document the exact steps taken
   - Note system state and configuration

#. **Check Documentation**:
   - Review :doc:`../../upgrade/concept-core-upgrade`
   - Consult :doc:`../../upgrade/how-to-upgrade-core`
   - Reference :doc:`../../reference/cli/omnia-upgrade`

#. **Contact Support**:
   - Provide complete error messages
   - Include system information and logs
   - Describe troubleshooting steps already attempted

#. **Community Resources**:
   - Check Omnia GitHub issues
   - Review community forums
   - Consult release notes and known issues

Related Topics
--------------

* :doc:`../../upgrade/how-to-upgrade-core`
* :doc:`../../upgrade/how-to-rollback-upgrade`
* :doc:`../../upgrade/how-to-migrate-inputs`
* :doc:`../../upgrade/concept-core-upgrade`
