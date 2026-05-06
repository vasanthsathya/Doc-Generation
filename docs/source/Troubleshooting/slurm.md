# Slurm Issues

Issues related to the Slurm job scheduler, including controller failures, node state problems, job submission errors, and GPU detection.

## `slurmctld` not starting

The Slurm controller daemon fails to start. Running `systemctl status slurmctld` shows the service as `failed` or `inactive`.

 * The `slurm.conf` file has syntax errors or references non-existent nodes.
 * The `munge` authentication service is not running.
 * File permissions on `/var/spool/slurmctld/` are incorrect.
 * The Slurm database daemon (`slurmdbd`) is unreachable and `AccountingStorageEnforce` is set.

 1. Check the slurmctld log for specific errors:

 tail -100 /var/log/slurm/slurmctld.log

 1. Verify munge is running:

 systemctl status munge

If munge is not running, start it:

 systemctl start munge

 1. Validate the Slurm configuration:

 slurmd -C # Show computed configuration
 slurmctld -Dvvv # Run in foreground with verbose logging

 1. Fix spool directory permissions:

 chown -R slurm:slurm /var/spool/slurmctld/
 chmod 755 /var/spool/slurmctld/

 1. If slurmdbd is the issue, see the `slurmdbd connection issues`_ section below.

## Nodes stuck in DOWN state

`sinfo` shows one or more nodes in `down` or `down*` state:

 PARTITION AVAIL TIMELIMIT NODES STATE NODELIST
 normal* up infinite 1 down* compute-03

 * The `slurmd` service on the compute node is not running.
 * Network connectivity between the control node and the compute node is broken.
 * The node was manually set to DOWN and not resumed.
 * Hardware issues (memory errors, disk failures) triggered an automatic drain.

 1. Check why the node is down:

 scontrol show node compute-03 | grep -i reason

 1. Verify `slurmd` is running on the compute node:

 ssh compute-03 systemctl status slurmd

If not running:

 ssh compute-03 systemctl start slurmd

 1. Test network connectivity:

 ping compute-03
 ssh compute-03 hostname

 1. Resume the node after fixing the underlying issue:

 scontrol update NodeName=compute-03 State=RESUME

 1. Verify the node returns to `idle`:

 sinfo -n compute-03

## Job submission failures

Submitting a job with `sbatch` or `srun` fails with errors such as:

 sbatch: error: Batch job submission failed: Invalid account or account/partition combination specified
 srun: error: Unable to allocate resources: No partition specified or system default partition

 * The user's account is not configured in Slurm accounting.
 * No default partition is defined in `slurm.conf`.
 * The requested resources exceed what is available in the cluster.

 1. Check available partitions:

 sinfo

 1. Verify the user's Slurm account:

 sacctmgr show user <username>

If the user is not configured:

 sacctmgr add user <username> account=default

 1. Verify a default partition exists in `slurm.conf`:

 # /etc/slurm/slurm.conf
 PartitionName=normal Nodes=compute-[01-10] Default=YES MaxTime=INFINITE State=UP

 1. If resources are the issue, check available resources:

 sinfo -N -l
 squeue # Check for jobs consuming resources

## `slurmdbd` connection issues

`slurmctld` logs show errors connecting to the Slurm database daemon:

 error: slurmdbd: Sending PersistInit msg: CONNECTION REFUSED
 error: slurmdbd: DBD_ID_REGISTER failed

 * The `slurmdbd` service is not running.
 * The MySQL/MariaDB database backend is down.
 * Network or firewall issues between the controller and the database node.
 * Incorrect database credentials in `slurmdbd.conf`.

 1. Check `slurmdbd` status:

 systemctl status slurmdbd

 1. Check the database backend:

 systemctl status mariadb # or mysql

 1. Verify `slurmdbd.conf` settings:

 grep -i storage /etc/slurm/slurmdbd.conf

 1. Test database connectivity:

 mysql -u slurm -p -h localhost slurm_acct_db -e "SELECT 1;"

 1. Check the `slurmdbd` log:

 tail -100 /var/log/slurm/slurmdbd.log

 1. If credentials changed, update `slurmdbd.conf` and restart:

 systemctl restart slurmdbd
 systemctl restart slurmctld

## GPU not detected by Slurm

GPU nodes are provisioned but Slurm does not show GPU resources. Running `scontrol show node <gpu_node>` shows no `Gres` entries, or GPU jobs fail with:

 srun: error: Unable to allocate resources: Requested node configuration is not available

 * GPU drivers (CUDA or ROCm) are not installed on the compute node.
 * The `gres.conf` file does not list the GPUs.
 * The `slurm.conf` does not define GRES for the GPU nodes.
 * The `nvidia-smi` or `rocm-smi` tool does not detect the GPU hardware.

 1. Verify the GPU is visible to the OS:

 # NVIDIA
 ssh <gpu_node> nvidia-smi

 # AMD
 ssh <gpu_node> rocm-smi

 1. If the GPU driver is not installed, re-run the Omnia playbook with GPU tags:

 ssh omnia_core
 cd /omnia
 ansible-playbook playbooks/omnia.yml --tags gpu

 1. Verify `gres.conf` on the compute node:

 ssh <gpu_node> cat /etc/slurm/gres.conf

Expected content:

 # /etc/slurm/gres.conf
 NodeName=gpu-01 Name=gpu Type=a100 File=/dev/nvidia[0-3]

 1. Verify `slurm.conf` includes GRES definitions:

 GresTypes=gpu
 NodeName=gpu-01 Gres=gpu:a100:4 ...

 1. After updating configuration files, restart Slurm services:

 # On the control node
 systemctl restart slurmctld

 # On the GPU compute node
 ssh <gpu_node> systemctl restart slurmd

 1. Confirm GPUs are registered:

 scontrol show node <gpu_node> | grep Gres

Copyright © 2025 Dell Technologies. All rights reserved.