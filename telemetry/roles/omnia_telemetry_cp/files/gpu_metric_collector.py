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
# ---
'''
Module to gather gpu check metrics
'''

import data_collector_nvidia_gpu

class GPUMetricCollector:
    '''
    GPUMetricCollector class is responsible for collecting all gpu metrics
    '''
    def __init__(self):
        self.gpu_metric_output_dict = {}

    def get_nvidia_metrics(self):
        # run nvidia-smi command and store output in a variable
        nvidia_metrics_cmd_output = data_collector_nvidia_gpu.get_nvidia_metrics_output()

        # get temperature details for NVIDIA GPU
        gpu_temp = data_collector_nvidia_gpu.get_nvidia_gpu_temp(nvidia_metrics_cmd_output)
        if gpu_temp is not None:
            for index, item in enumerate(gpu_temp):
                self.gpu_metric_output_dict["gpu_temperature:gpu" + str(index)] = item

        # get utilization details for NVIDIA GPU
        gpu_util = data_collector_nvidia_gpu.get_nvidia_gpu_utilization(nvidia_metrics_cmd_output)
        if gpu_util is not None:
            for index, item in enumerate(gpu_util):
                self.gpu_metric_output_dict["gpu_utilization:gpu" + str(index)] = item

        # get average of utilization of all GPUs in the system
        gpu_avg_util = data_collector_nvidia_gpu.get_nvidia_gpu_avg_utilization(nvidia_metrics_cmd_output)
        self.gpu_metric_output_dict["gpu_utilization:average"] = gpu_avg_util

    def metric_collector(self, aggregation_level):
        '''
        Method to make method calls to collect all metrics for gpu
        '''
        if aggregation_level == 'node':
            self.get_nvidia_metrics()
