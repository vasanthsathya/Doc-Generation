
[ ![logo](../../assets/omnia-logo.png) ](../../index.html "Dell Omnia")

Dell Omnia 

Timezone List 

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
 * [ iDRAC Metrics ](../Metrics/idrac_metrics.html)
 * Appendices Appendices 
 * [ Hostname Requirements ](hostname_requirements.html)
 * Timezone List [ Timezone List ](timezones.html) Table of contents 
 * [ UTC and special values ](#utc-and-special-values)

Operations 
 * [ Add / Remove Nodes ](../../Operations/add_remove_nodes.html)

Troubleshooting 
 * [ General ](../../Troubleshooting/general.html)

Contributing 
 * [ Pull Requests ](../../Contributing/pull_requests.html)

Table of contents 

 * [ UTC and special values ](#utc-and-special-values)

 1. [ Home ](../../index.html)
 2. [ Reference ](../index.html)
 3. [ Appendices ](hostname_requirements.html)

# Supported Timezone Values[¶](#supported-timezone-values "Permanent link")

The `timezone` parameter in `provision_config.yml` accepts any valid IANA timezone string. This page lists commonly used values. For the complete list, consult the [IANA Time Zone Database](https://www.iana.org/time-zones).

## UTC and special values[¶](#utc-and-special-values "Permanent link")

Value | Description 
---|--- 
`UTC` | Coordinated Universal Time. **Default** if `timezone` is not specified. Recommended for clusters spanning multiple geographic locations. 
`Etc/UTC` | Equivalent to `UTC`. 
 
## Americas[¶](#americas "Permanent link")

Timezone | UTC Offset | Common Name 
---|---|--- 
`America/New_York` | UTC-5 (EST) / UTC-4 (EDT) | US Eastern 
`America/Chicago` | UTC-6 (CST) / UTC-5 (CDT) | US Central 
`America/Denver` | UTC-7 (MST) / UTC-6 (MDT) | US Mountain 
`America/Los_Angeles` | UTC-8 (PST) / UTC-7 (PDT) | US Pacific 
`America/Anchorage` | UTC-9 (AKST) / UTC-8 (AKDT) | US Alaska 
`Pacific/Honolulu` | UTC-10 (HST) | US Hawaii 
`America/Toronto` | UTC-5 (EST) / UTC-4 (EDT) | Canada Eastern 
`America/Vancouver` | UTC-8 (PST) / UTC-7 (PDT) | Canada Pacific 
`America/Sao_Paulo` | UTC-3 (BRT) | Brazil 
`America/Mexico_City` | UTC-6 (CST) / UTC-5 (CDT) | Mexico Central 
`America/Argentina/Buenos_Aires` | UTC-3 (ART) | Argentina 
 
## Europe[¶](#europe "Permanent link")

Timezone | UTC Offset | Common Name 
---|---|--- 
`Europe/London` | UTC+0 (GMT) / UTC+1 (BST) | United Kingdom 
`Europe/Paris` | UTC+1 (CET) / UTC+2 (CEST) | Central European 
`Europe/Berlin` | UTC+1 (CET) / UTC+2 (CEST) | Germany 
`Europe/Amsterdam` | UTC+1 (CET) / UTC+2 (CEST) | Netherlands 
`Europe/Rome` | UTC+1 (CET) / UTC+2 (CEST) | Italy 
`Europe/Madrid` | UTC+1 (CET) / UTC+2 (CEST) | Spain 
`Europe/Moscow` | UTC+3 (MSK) | Russia (Moscow) 
`Europe/Istanbul` | UTC+3 (TRT) | Turkey 
`Europe/Helsinki` | UTC+2 (EET) / UTC+3 (EEST) | Finland 
`Europe/Warsaw` | UTC+1 (CET) / UTC+2 (CEST) | Poland 
 
## Asia and Pacific[¶](#asia-and-pacific "Permanent link")

Timezone | UTC Offset | Common Name 
---|---|--- 
`Asia/Kolkata` | UTC+5:30 (IST) | India 
`Asia/Shanghai` | UTC+8 (CST) | China 
`Asia/Tokyo` | UTC+9 (JST) | Japan 
`Asia/Seoul` | UTC+9 (KST) | South Korea 
`Asia/Singapore` | UTC+8 (SGT) | Singapore 
`Asia/Hong_Kong` | UTC+8 (HKT) | Hong Kong 
`Asia/Taipei` | UTC+8 (CST) | Taiwan 
`Asia/Dubai` | UTC+4 (GST) | UAE 
`Asia/Riyadh` | UTC+3 (AST) | Saudi Arabia 
`Asia/Jakarta` | UTC+7 (WIB) | Indonesia (Western) 
`Asia/Bangkok` | UTC+7 (ICT) | Thailand 
`Asia/Karachi` | UTC+5 (PKT) | Pakistan 
`Australia/Sydney` | UTC+10 (AEST) / UTC+11 (AEDT) | Australia Eastern 
`Australia/Perth` | UTC+8 (AWST) | Australia Western 
`Pacific/Auckland` | UTC+12 (NZST) / UTC+13 (NZDT) | New Zealand 
 
## Africa and Middle East[¶](#africa-and-middle-east "Permanent link")

Timezone | UTC Offset | Common Name 
---|---|--- 
`Africa/Cairo` | UTC+2 (EET) | Egypt 
`Africa/Lagos` | UTC+1 (WAT) | Nigeria (West Africa) 
`Africa/Johannesburg` | UTC+2 (SAST) | South Africa 
`Africa/Nairobi` | UTC+3 (EAT) | Kenya (East Africa) 
`Africa/Casablanca` | UTC+1 (WEST) | Morocco 
 
Note

 * The timezone is applied to all nodes provisioned by Omnia. To use different timezones on different nodes, modify the timezone post- provisioning via `timedatectl`.
 * UTC offsets shown are standard time. Daylight saving adjustments are handled automatically by the OS.

Info

 * [Provision Config](../Configuration/provision_config.html) \-- Where `timezone` is configured.

Back to top [ Previous Hostname Requirements ](hostname_requirements.html) [ Next BeeGFS Server Setup ](beegfs_server_setup.html)

Copyright © 2025 Dell Technologies. All rights reserved. 

[ ](https://github.com/dell/omnia "github.com")
