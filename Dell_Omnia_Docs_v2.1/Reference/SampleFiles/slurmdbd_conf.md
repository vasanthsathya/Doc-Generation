
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

slurmdbd.conf 

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
 * [ Prepare OIM ](../../HowTo/Setup/prepare_oim.html)
 * Slurm Slurm 
 * [ Set Up Slurm ](../../HowTo/Slurm/setup_slurm.html)
 * Kubernetes Kubernetes 
 * [ Set Up Kubernetes ](../../HowTo/Kubernetes/setup_service_k8s.html)
 * Storage Storage 
 * [ Configure NFS ](../../HowTo/Storage/configure_nfs.html)
 * Networking Networking 
 * [ Configure InfiniBand ](../../HowTo/Networking/configure_infiniband.html)
 * Authentication Authentication 
 * [ Set Up OpenLDAP ](../../HowTo/Authentication/setup_openldap.html)
 * Telemetry Telemetry 
 * [ Set Up Telemetry ](../../HowTo/Telemetry/setup_telemetry.html)
 * Containers Containers 
 * [ Use Apptainer ](../../HowTo/Containers/use_apptainer.html)
 * BuildStreaM BuildStreaM 
 * [ Deploy GitLab ](../../HowTo/BuildStreaM/deploy_gitlab.html)

Reference 
 * Support Matrix Support Matrix 
 * [ Servers ](../SupportMatrix/servers.html)
 * Configuration Configuration 
 * [ Omnia Config ](../Configuration/omnia_config.html)
 * Sample Files Sample Files 
 * [ PXE Mapping File ](pxe_mapping_file.html)
 * slurmdbd.conf [ slurmdbd.conf ](slurmdbd_conf.html) Table of contents 
 * [ Complete sample ](#complete-sample)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * [ iDRAC Metrics ](../Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Complete sample ](#complete-sample)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Sample Files ](pxe_mapping_file.html)

# Sample slurmdbd.conf[¶](#sample-slurmdbdconf "Permanent link")

This page provides a sample `slurmdbd.conf` with inline comments. The Slurm Database Daemon (`slurmdbd`) stores job accounting, user associations, and cluster usage data in a relational database.

## Complete sample[¶](#complete-sample "Permanent link")

File: /etc/slurm/slurmdbd.conf
 
 
 # ===========================================================================
 # slurmdbd.conf -- Slurm Database Daemon configuration
 # This file must be readable only by the SlurmUser (typically 'slurm').
 # Permissions: 0600, owned by slurm:slurm.
 # ===========================================================================
 
 # ---------------------------------------------------------------------------
 # Daemon identification
 # ---------------------------------------------------------------------------
 DbdHost=slurm-ctrl-01 # Hostname where slurmdbd runs.
 # Must match the SlurmctldHost or be
 # reachable from the controller.
 DbdPort=6819 # Port slurmdbd listens on.
 # Must match AccountingStoragePort in
 # slurm.conf.
 SlurmUser=slurm # User account under which slurmdbd runs.
 
 # ---------------------------------------------------------------------------
 # Authentication
 # ---------------------------------------------------------------------------
 AuthType=auth/munge # Must match AuthType in slurm.conf.
 
 # ---------------------------------------------------------------------------
 # Logging
 # ---------------------------------------------------------------------------
 LogFile=/var/log/slurmdbd.log
 DebugLevel=info # Log level: quiet, fatal, error, info,
 # verbose, debug, debug2-debug5.
 PidFile=/var/run/slurmdbd.pid
 
 # ---------------------------------------------------------------------------
 # Database connection
 # ---------------------------------------------------------------------------
 StorageType=accounting_storage/mysql # Database backend. MySQL/MariaDB
 # is the only supported option.
 StorageHost=localhost # Database server hostname or IP.
 # Use localhost if the database runs
 # on the same node as slurmdbd.
 StoragePort=3306 # MySQL/MariaDB port.
 StorageLoc=slurm_acct_db # Database name. Omnia creates this
 # database automatically.
 StorageUser=slurm_db_user # Database username.
 StoragePass=/run/secrets/slurmdbd_db_pass # Path to a file containing the
 # database password, or the
 # password string directly.
 # File-based is recommended for
 # security.
 
 # ---------------------------------------------------------------------------
 # Purge settings
 # ---------------------------------------------------------------------------
 PurgeEventAfter=12months # Purge cluster event records older than
 # this. Format: Nmonths, Ndays, Nhours.
 PurgeJobAfter=12months # Purge completed job records.
 PurgeStepAfter=6months # Purge job step records.
 PurgeResvAfter=6months # Purge reservation records.
 PurgeSuspendAfter=1month # Purge job suspend records.
 PurgeTXNAfter=12months # Purge transaction records.
 
 # ---------------------------------------------------------------------------
 # Archive settings (optional)
 # ---------------------------------------------------------------------------
 # ArchiveEvents=yes
 # ArchiveJobs=yes
 # ArchiveDir=/var/spool/slurmdbd/archive
 # ArchiveScript=/usr/local/bin/slurm_archive.sh
 
 # ---------------------------------------------------------------------------
 # Performance tuning
 # ---------------------------------------------------------------------------
 CommitDelay=1 # Seconds to batch database commits.
 # Reduces database write load at the
 # cost of slight data lag.
 MessageTimeout=10 # Seconds before an RPC times out.
 TCPTimeout=120 # TCP connection timeout in seconds.
 

## Key parameter reference[¶](#key-parameter-reference "Permanent link")

Parameter | Description 
---|--- 
`DbdHost` | Hostname or IP where `slurmdbd` listens. Usually the Slurm control node. 
`DbdPort` | TCP port for `slurmdbd` connections (default: `6819`). 
`StorageType` | `accounting_storage/mysql` for MySQL/MariaDB backend. 
`StorageHost` | Database server address. Use `localhost` when co-located with `slurmdbd`. 
`StorageLoc` | Database name. Omnia creates this automatically during setup. 
`StorageUser` | Database user with privileges on `StorageLoc`. 
`StoragePass` | Database password or path to password file. 
`PurgeJobAfter` | Retention period for completed job records. Prevents unbounded database growth. 
`CommitDelay` | Batching interval for database writes. Higher values reduce I/O but increase data-loss risk on crash. 
 
## File permissions[¶](#file-permissions "Permanent link")

Warning

`slurmdbd.conf` contains database credentials and must have restrictive permissions:
 
 
 chown slurm:slurm /etc/slurm/slurmdbd.conf
 chmod 0600 /etc/slurm/slurmdbd.conf
 

Slurmdbd refuses to start if the file is world-readable.

## Database prerequisites[¶](#database-prerequisites "Permanent link")

Requirement | Details 
---|--- 
MariaDB or MySQL installed | Omnia installs MariaDB from the RHEL repository by default. 
Database created | Omnia creates the `slurm_acct_db` database and grants privileges to `slurm_db_user` during `omnia.yml` execution. 
innodb_buffer_pool_size | For clusters with > 500 nodes, increase this MySQL parameter to at least 1 GB for acceptable accounting query performance. 
 
Info

 * [Slurm Conf](slurm_conf.html) \-- Companion `slurm.conf` configuration.
 * [Omnia Config](../Configuration/omnia_config.html) \-- Omnia-level Slurm settings.
 * [Ports](../ClusterRequirements/ports.html) \-- Port 6819 for slurmdbd.
 * [Slurm documentation](https://slurm.schedmd.com/slurmdbd.conf.html) \-- Upstream parameter reference.

Back to top [ Previous slurm.conf ](slurm_conf.html) [ Next software_config.json ](software_config_json.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
