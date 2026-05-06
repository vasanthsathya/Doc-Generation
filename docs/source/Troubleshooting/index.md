# Troubleshooting

Symptom-driven guides for diagnosing and resolving issues with your Omnia cluster. Each entry follows a consistent **Symptom > Cause > Resolution** format so you can quickly identify the problem and apply the fix.

## Troubleshooting approach

When you encounter an issue, follow this general diagnostic flow:

 2. Playbook logs: `/opt/omnia/log/core/playbooks/`

 3. Container logs: `podman logs <container_name>`
 4. Slurm logs: `/var/log/slurm/`

 6. **Use the ochami CLI.** For provisioning issues, the `ochami-cli` provides direct access to the OpenCHAMI state manager for inspecting node inventory, boot status, and hardware state:

 ssh omnia_core
 ochami-cli smd components list
 ochami-cli bss bootscript list

 1. **Search this section.** Browse the topic-specific pages below or use your browser's search (Ctrl+F) to find your symptom.

Copyright © 2025 Dell Technologies. All rights reserved.