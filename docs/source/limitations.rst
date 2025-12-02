Limitations
===========

- Omnia supports only diskless provisioning of servers.
- Omnia supports nodes discovered only through mapping file.
- Omnia does not support automatic deletion of the nodes using playbooks. However, you can reprovision the nodes. To reprovision the nodes, see :ref:`reprovision-cluster`. 
- Dell Technologies provides support only for the Dell-developed modules of Omnia. Third-party tools deployed by Omnia are not covered under Dell support.
- In a single node cluster, the login node and Slurm functionalities are not applicable.
- Containerized benchmark job execution is not supported on Slurm clusters.
- All iDRACs must use the same username and password.
- Omnia playbooks will fail if the OIM is unable to access online resources or the Internet.