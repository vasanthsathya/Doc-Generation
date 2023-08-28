# Copyright 2023 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Module to initiate omnia telemetry data collection
'''
import time
import sys
import signal
import common_logging
import dbupdate
import utility
from regular_metric_collector import RegularMetricCollector
from gpu_metric_collector import GPUMetricCollector
from health_check_metric_collector import HealthCheckMetricCollector

def cleanup(signum, frame):
    '''
    Cleanup operations to be executed during graceful shutdown.
    '''
    try:
        # Close database connection

        # Close syslog
        common_logging.close_syslog()

    except Exception as err:
        pass

def handle_sigterm(signum, frame):
    '''
    sigterm handler for stop telemetry
    '''
    cleanup(signum, frame)
    sys.exit(0)

def main():
    '''
    Module main to initiate the telemetry data collection functionality
    '''

    common_logging.setup_syslog('omnia_telemetry')

    # Register signal handler for SIGTERM
    #signal.signal(signal.SIGTERM, handle_sigterm)

    # Copy telemetry ini to dictionary dict_telemetry_ini
    if utility.set_telemetry_ini_values() is True:
        # Sleep for fuzzt_offset value
        time.sleep(utility.generate_random_fuzzy_offset(utility.dict_telemetry_ini["fuzzy_offset"]))

        if utility.dict_telemetry_ini["collect_regular_metrics"] =="true":
            regular_metric_collector_obj=RegularMetricCollector()
        if utility.dict_telemetry_ini["collect_health_check_metrics"]=="true":
            health_metric_collector_obj=HealthCheckMetricCollector()
        if utility.dict_telemetry_ini["collect_gpu_metrics"]=="true":
            gpu_metric_collector_obj=GPUMetricCollector()
        while True:
            combined_result_dict={"Regular Metric":{},"Health Check Metric":{},"GPU Metric":{}}

            if utility.dict_telemetry_ini["collect_regular_metrics"] == "true":
                regular_metric_collector_obj.metric_collector(utility.dict_telemetry_ini["group_info"])
                combined_result_dict["Regular Metric"]=regular_metric_collector_obj.regular_metric_output_dict

            if utility.dict_telemetry_ini["collect_health_check_metrics"] == "true":
                health_metric_collector_obj.metric_collector(utility.dict_telemetry_ini["group_info"])
                combined_result_dict["Health Check Metric"]=health_metric_collector_obj.health_check_metric_output_dict

            if utility.dict_telemetry_ini["collect_gpu_metrics"] == "true":
                gpu_metric_collector_obj.metric_collector(utility.dict_telemetry_ini["group_info"])
                combined_result_dict["GPU Metric"]=gpu_metric_collector_obj.gpu_metric_output_dict
            #DB Update
            dbupdate(combined_result_dict["Regular Metric"],combined_result_dict["Health Check Metric"],combined_result_dict["GPU Metric"],utility.get_system_name())
            #sleep for omnia_telemetry_collection_interval time
            time.sleep(int(utility.dict_telemetry_ini["omnia_telemetry_collection_interval"]))

if __name__ == "__main__":
    main()