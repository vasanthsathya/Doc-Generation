
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

GPU Metrics 

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
 * [ iDRAC Metrics ](idrac_metrics.html)
 * GPU Metrics [ GPU Metrics ](gpu_metrics.html) Table of contents 
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

# GPU Metrics[¶](#gpu-metrics "Permanent link")

This page catalogs the GPU telemetry metrics collected by the Omnia telemetry pipeline. Metrics are available for both NVIDIA and AMD GPUs.

## Collection method[¶](#collection-method "Permanent link")

Property | NVIDIA | AMD 
---|---|--- 
**Collection tool** | DCGM (Data Center GPU Manager) or `nvidia-smi` | `rocm-smi` or ROCm SMI library 
**Protocol** | DCGM exporter (Prometheus-compatible) or Kafka producer | ROCm exporter (Prometheus-compatible) or Kafka producer 
**Default interval** | 10 seconds | 10 seconds 
**Kafka topic** | `gpu_telemetry` | `gpu_telemetry` 
**Storage** | VictoriaMetrics | VictoriaMetrics 
 
## NVIDIA GPU metrics[¶](#nvidia-gpu-metrics "Permanent link")

### Utilization metrics[¶](#utilization-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`nvidia_gpu_utilization` | Percent | Percentage of time the GPU was executing one or more kernels over the sampling interval. 
`nvidia_gpu_memory_utilization` | Percent | Percentage of time the GPU memory controller was active. 
`nvidia_gpu_encoder_utilization` | Percent | Hardware video encoder utilization (if applicable). 
`nvidia_gpu_decoder_utilization` | Percent | Hardware video decoder utilization (if applicable). 
 
### Temperature metrics[¶](#temperature-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`nvidia_gpu_temperature` | Celsius | Current GPU die temperature. 
`nvidia_gpu_memory_temperature` | Celsius | HBM (High Bandwidth Memory) temperature. Available on A100, H100, and similar data center GPUs. 
`nvidia_gpu_temperature_threshold_shutdown` | Celsius | Temperature at which the GPU will trigger a thermal shutdown. 
`nvidia_gpu_temperature_threshold_slowdown` | Celsius | Temperature at which the GPU begins throttling clocks. 
 
### Memory metrics[¶](#memory-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`nvidia_gpu_memory_total` | MiB | Total GPU memory (e.g., 40960 MiB for A100 40GB). 
`nvidia_gpu_memory_used` | MiB | GPU memory currently allocated by processes. 
`nvidia_gpu_memory_free` | MiB | GPU memory available for allocation. 
`nvidia_gpu_bar1_memory_total` | MiB | Total BAR1 memory (used for CPU-GPU memory mapping). 
`nvidia_gpu_bar1_memory_used` | MiB | BAR1 memory currently in use. 
 
### Power metrics[¶](#power-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`nvidia_gpu_power_draw` | Watts | Current GPU power consumption. 
`nvidia_gpu_power_limit` | Watts | Current power limit (may be software-configured). 
`nvidia_gpu_power_default_limit` | Watts | Factory default power limit. 
`nvidia_gpu_power_max_limit` | Watts | Maximum power limit configurable for this GPU. 
`nvidia_gpu_energy_consumption` | Joules | Cumulative energy consumed since last driver reload. 
 
### Clock and performance metrics[¶](#clock-and-performance-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`nvidia_gpu_clock_sm` | MHz | Current SM (Streaming Multiprocessor) clock frequency. 
`nvidia_gpu_clock_memory` | MHz | Current memory clock frequency. 
`nvidia_gpu_pstate` | Enum | GPU performance state (P0 = maximum performance, P12 = idle). 
`nvidia_gpu_throttle_reason` | Bitmask | Active clock throttle reasons (thermal, power, API-initiated). 
 
### Error metrics[¶](#error-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`nvidia_gpu_ecc_errors_corrected` | Count | Corrected (single-bit) ECC errors. Per-memory type (SRAM, DRAM). 
`nvidia_gpu_ecc_errors_uncorrected` | Count | Uncorrected (double-bit) ECC errors. Indicates potential data corruption. 
`nvidia_gpu_retired_pages_single_bit` | Count | GPU memory pages retired due to single-bit ECC errors. 
`nvidia_gpu_retired_pages_double_bit` | Count | GPU memory pages retired due to double-bit ECC errors. 
`nvidia_gpu_xid_errors` | Count | NVIDIA Xid error events (logged by the GPU driver). 
 
## AMD GPU metrics[¶](#amd-gpu-metrics "Permanent link")

### Utilization metrics[¶](#utilization-metrics_1 "Permanent link")

Metric | Unit | Description 
---|---|--- 
`amd_gpu_utilization` | Percent | GPU compute unit utilization over the sampling interval. 
`amd_gpu_memory_utilization` | Percent | GPU memory controller utilization. 
 
### Temperature metrics[¶](#temperature-metrics_1 "Permanent link")

Metric | Unit | Description 
---|---|--- 
`amd_gpu_temperature_edge` | Celsius | GPU edge temperature. 
`amd_gpu_temperature_junction` | Celsius | GPU junction (hotspot) temperature. 
`amd_gpu_temperature_memory` | Celsius | HBM temperature. 
 
### Memory metrics[¶](#memory-metrics_1 "Permanent link")

Metric | Unit | Description 
---|---|--- 
`amd_gpu_memory_total` | MiB | Total GPU memory. 
`amd_gpu_memory_used` | MiB | GPU memory currently allocated. 
`amd_gpu_memory_free` | MiB | Available GPU memory. 
 
### Power metrics[¶](#power-metrics_1 "Permanent link")

Metric | Unit | Description 
---|---|--- 
`amd_gpu_power_draw` | Watts | Current GPU power consumption. 
`amd_gpu_power_cap` | Watts | Current power cap. 
`amd_gpu_power_cap_default` | Watts | Factory default power cap. 
 
### Clock metrics[¶](#clock-metrics "Permanent link")

Metric | Unit | Description 
---|---|--- 
`amd_gpu_clock_sclk` | MHz | Current GPU engine (shader) clock frequency. 
`amd_gpu_clock_mclk` | MHz | Current memory clock frequency. 
 
## Metric labels[¶](#metric-labels "Permanent link")

All GPU metrics include the following common labels:

Label | Description 
---|--- 
`host` | Hostname of the compute node. 
`gpu_index` | GPU index on the node (0, 1, 2, ...). 
`gpu_uuid` | Unique identifier for the GPU. 
`gpu_model` | GPU model name (e.g., `NVIDIA A100-SXM4-80GB`, `AMD Instinct MI250X`). 
`pci_bus_id` | PCI bus address of the GPU. 
 
Info

 * [Telemetry Config](../Configuration/telemetry_config.html) \-- Telemetry pipeline configuration.
 * [Omnia Config](../Configuration/omnia_config.html) \-- GPU deployment settings (`enable_nvidia_gpu`, `enable_amd_gpu`).
 * [Idrac Metrics](idrac_metrics.html) \-- Server-level hardware metrics.
 * [Ldms Metrics](ldms_metrics.html) \-- OS-level metrics from LDMS.

Back to top [ Previous iDRAC Metrics ](idrac_metrics.html) [ Next LDMS Metrics ](ldms_metrics.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
