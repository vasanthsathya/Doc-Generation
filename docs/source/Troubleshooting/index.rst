
Troubleshooting
===============


Symptom-driven guides for diagnosing and resolving issues with your Omnia
cluster. Each entry follows a consistent **Symptom > Cause > Resolution**
format so you can quickly identify the problem and apply the fix.


Troubleshooting approach
------------------------


When you encounter an issue, follow this general diagnostic flow:

#. **Check logs first.** Most issues leave a clear trace in the logs. See
   :doc:`Log Management <../Operations/log_management>` for log locations.

  - Playbook logs: ``/opt/omnia/log/core/playbooks/``
  - Container logs: ``podman logs <container_name>``
  - Slurm logs: ``/var/log/slurm/``

#. **Verify prerequisites.** Many failures stem from unmet prerequisites
   (missing packages, wrong OS version, misconfigured networks). Re-check the
   :doc:`Prerequisites Checklist <../GetStarted/prerequisites_checklist>` for your deployment path.

#. **Use the ochami CLI.** For provisioning issues, the ``ochami-cli`` provides
   direct access to the OpenCHAMI state manager for inspecting node inventory,
   boot status, and hardware state:


.. code-block:: bash

      ssh omnia_core
      ochami-cli smd components list
      ochami-cli bss bootscript list



#. **Search this section.** Browse the topic-specific pages below or use your
   browser's search (Ctrl+F) to find your symptom.


.. tip::


   If you cannot resolve an issue using this guide, open an issue on the
   `Omnia GitHub repository <https://github.com/dell/omnia/issues>`_ with
   the relevant log output and a description of your environment.


.. toctree::
   :maxdepth: 2
   :caption: Troubleshooting

   general
   provisioning
   slurm
   kubernetes
   telemetry
   authentication
   buildstream
   known_limitations

