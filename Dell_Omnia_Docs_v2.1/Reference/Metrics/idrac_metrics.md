
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

iDRAC Metrics 

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
 * [ PXE Mapping File ](../SampleFiles/pxe_mapping_file.html)
 * Cluster Requirements Cluster Requirements 
 * [ Minimum Nodes ](../ClusterRequirements/minimum_nodes.html)
 * Playbooks Playbooks 
 * [ Playbook Reference ](../Playbooks/playbook_reference.html)
 * Metrics Metrics 
 * iDRAC Metrics [ iDRAC Metrics ](idrac_metrics.html) Table of contents 
 * [ Collection method ](#collection-method)
 * Appendices Appendices 
 * [ Hostname Requirements ](../Appendices/hostname_requirements.html)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ Collection method ](#collection-method)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Metrics ](idrac_metrics.html)

# iDRAC Metrics[¶](#idrac-metrics "Permanent link")

This page catalogs the metrics collected by the Omnia iDRAC telemetry collector via the Redfish API. These metrics are streamed to Kafka and stored in VictoriaMetrics for visualization in Grafana.

## Collection method[¶](#collection-method "Permanent link")

Property | Value 
---|--- 
**Protocol** | Redfish (HTTPS REST API) 
**Source** | iDRAC on each managed server 
**Default interval** | 300 seconds (configurable via `idrac_telemetry_interval` in `telemetry_config.yml`) 
**Kafka topic** | `idrac_telemetry` (configurable via `kafka_topic_idrac`) 
**Storage** | VictoriaMetrics time-series database 
 
## Power metrics[¶](#power-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`idrac_power_consumed_watts` | Watts | Current total server power consumption. 
`idrac_power_capacity_watts` | Watts | Maximum power capacity of the server's power supply units. 
`idrac_power_input_voltage` | Volts | Input voltage from the power source to the PSU. 
`idrac_power_output_voltage` | Volts | Output voltage from PSU to server components. 
`idrac_power_psu_status` | Enum | Power supply unit health status (`OK`, `Warning`, `Critical`). 
`idrac_power_avg_watts` | Watts | Average power consumption over the collection interval. 
`idrac_power_peak_watts` | Watts | Peak power consumption recorded during the interval. 
 
## Thermal metrics[¶](#thermal-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`idrac_thermal_inlet_temp_celsius` | Celsius | Temperature at the server inlet (ambient air entering the chassis). 
`idrac_thermal_outlet_temp_celsius` | Celsius | Temperature at the server outlet (exhaust air). 
`idrac_thermal_cpu_temp_celsius` | Celsius | CPU package temperature. One metric per socket (labeled `cpu=0`, `cpu=1`). 
`idrac_thermal_memory_temp_celsius` | Celsius | DIMM temperature. One metric per DIMM slot. 
`idrac_thermal_storage_temp_celsius` | Celsius | Storage drive temperature (NVMe, SSD, or HDD). 
 
## Fan metrics[¶](#fan-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`idrac_fan_speed_rpm` | RPM | Current fan rotational speed. One metric per fan (labeled `fan=Fan.Embedded.1`, etc.). 
`idrac_fan_speed_percent` | Percent | Fan speed as a percentage of maximum. Useful for alerting on fan degradation. 
`idrac_fan_status` | Enum | Fan health status (`OK`, `Warning`, `Critical`, `Absent`). 
 
## Voltage metrics[¶](#voltage-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`idrac_voltage_reading` | Volts | Voltage reading from each voltage sensor. Labeled by sensor name (e.g., `sensor=PS1_Voltage_1`). 
`idrac_voltage_status` | Enum | Voltage sensor health status (`OK`, `Warning`, `Critical`). 
`idrac_voltage_upper_threshold` | Volts | Upper critical threshold for the voltage sensor. 
`idrac_voltage_lower_threshold` | Volts | Lower critical threshold for the voltage sensor. 
 
## CPU health metrics[¶](#cpu-health-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`idrac_cpu_status` | Enum | CPU health status (`OK`, `Warning`, `Critical`). One per socket. 
`idrac_cpu_model` | String (label) | CPU model string (e.g., `Intel(R) Xeon(R) Gold 6448Y`). Exposed as a metric label, not a numeric value. 
`idrac_cpu_core_count` | Count | Number of physical cores per CPU socket. 
`idrac_cpu_thread_count` | Count | Number of logical threads per CPU socket. 
 
## Memory health metrics[¶](#memory-health-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`idrac_memory_status` | Enum | DIMM health status (`OK`, `Warning`, `Critical`). One per DIMM slot. 
`idrac_memory_size_gb` | GB | Capacity of each DIMM. 
`idrac_memory_speed_mhz` | MHz | Operating speed of each DIMM. 
`idrac_memory_correctable_errors` | Count | Correctable ECC error count per DIMM. Non-zero values may indicate impending DIMM failure. 
 
## Storage health metrics[¶](#storage-health-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`idrac_storage_disk_status` | Enum | Physical disk health (`OK`, `Warning`, `Critical`, `Failed`). 
`idrac_storage_disk_capacity_gb` | GB | Reported capacity of each physical disk. 
`idrac_storage_disk_media_type` | String (label) | Media type (`SSD`, `HDD`, `NVMe`). Exposed as a label. 
`idrac_storage_virtual_disk_status` | Enum | RAID virtual disk health status. 
 
## Metric labels[¶](#metric-labels "Permanent link")

All iDRAC metrics include the following common labels:

Label | Description 
---|--- 
`host` | Hostname of the server (as assigned in the PXE mapping file). 
`service_tag` | Dell service tag of the server. 
`bmc_ip` | IP address of the iDRAC interface. 
 
Info

 * [Telemetry Config](../Configuration/telemetry_config.html) \-- iDRAC telemetry configuration parameters.
 * [Ldms Metrics](ldms_metrics.html) \-- OS-level metrics from LDMS.
 * [Gpu Metrics](gpu_metrics.html) \-- GPU telemetry metrics.

Back to top [ Previous Playbook Reference ](../Playbooks/playbook_reference.html) [ Next GPU Metrics ](gpu_metrics.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
