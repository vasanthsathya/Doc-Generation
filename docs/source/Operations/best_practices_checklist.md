# Best Practices Checklist

A consolidated checklist of recommendations for deploying and operating an Omnia cluster. Each item links to the relevant documentation section for detailed procedures.

## BIOS and firmware

| Best Practice | Reference 
---|---|--- 

## Playbook execution

| Best Practice | Reference 
---|---|--- 

## Storage and telemetry

| Best Practice | Reference 
---|---|--- 

## System administration

| Best Practice | Reference 
---|---|--- 

## Pre-deployment summary

Use this condensed list as a quick pre-flight check before running any Omnia deployment:

 1. ☐ BIOS: PowerCap disabled, Performance mode set.
 2. ☐ iDRAC firmware updated to the latest supported version.
 3. ☐ Network: admin and BMC VLANs configured, NFS accessible.
 4. ☐ System clocks synchronized (chrony/NTP).
 5. ☐ OIM meets minimum requirements (4+ cores, 32+ GB RAM, 256+ GB disk).
 6. ☐ Input files reviewed and populated (mapping file, config files).
 7. ☐ Credentials encrypted with Ansible Vault.
 8. ☐ Sufficient NFS storage allocated for telemetry.
 9. ☐ Firefox updated (if using AWX web UI).
 10. ☐ Security updates applied: `yum update --security`.

Copyright © 2025 Dell Technologies. All rights reserved.