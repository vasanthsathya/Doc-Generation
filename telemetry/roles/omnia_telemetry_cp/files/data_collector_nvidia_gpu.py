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
Module to gather nvidia gpu metrics
'''

import common_parser
import invoke_commands
import common_logging

# --------------------------------NVIDIA GPU metric collection---------------------------------
def get_nvidia_metrics_output():
    '''
    This method collects command output for nvidia-smi command for gpu metrics
    :return: nvidia query output
    '''
    nvidia_metrics_query = "nvidia-smi --query-gpu=temperature.gpu,utilization.gpu " \
                           "--format=csv,nounits"
    command_result = invoke_commands.call_command(nvidia_metrics_query)
    if command_result is not None:
        command_result_df = common_parser.get_df_format(command_result)
        return command_result_df
    common_logging.log_error("data_collector_nvidia_gpu:get_nvidia_metrics_output",
                             "nvidia-smi command did not give output for gpu metrics.")
    return None


def get_nvidia_gpu_temp(nvidia_metrics_cmd_result):
    '''
    This method collects nvidia gpu temp from nvidia query output
    and stores it in gpu metric dictionary
    :param nvidia_metrics_cmd_result: nvidia query output
    :param gpu_metric_output_dict: dictionary with nvidia gpu temperature data added
    '''
    if nvidia_metrics_cmd_result is not None:
        try:
            gpu_temp_list = common_parser.get_col_from_df(nvidia_metrics_cmd_result, 'temperature.gpu')
            return gpu_temp_list
        except Exception as err:
            common_logging.log_error("data_collector_nvidia_gpu:get_nvidia_gpu_temp",
                                     "could not parse gpu temperature from nvidia-smi"+str(err))
            return None
    return None


def get_nvidia_gpu_utilization(nvidia_metrics_cmd_result):
    '''
    This method collects nvidia gpu utilization from nvidia query output
    and stores it in gpu metric dictionary
    :param nvidia_metrics_cmd_result: nvidia query output
    :param gpu_metric_output_dict: dictionary with nvidia gpu utilization data added
    '''
    if nvidia_metrics_cmd_result is not None:
        try:
            gpu_util_list = common_parser.get_col_from_df(nvidia_metrics_cmd_result, 'utilization.gpu [%]')
            return gpu_util_list
        except Exception as err:
            common_logging.log_error("data_collector_nvidia_gpu:get_nvidia_gpu_utilization",
                                     "could not parse gpu utilization from nvidia-smi"+str(err))
            return None
    return None


def get_nvidia_gpu_avg_utilization(nvidia_metrics_cmd_result):
    '''
    This method calculates average gpu utilization on the node
    and stores it in gpu metric dictionary
    :param nvidia_metrics_cmd_result: nvidia query output
    :param gpu_metric_output_dict: dictionary with nvidia gpu average utilization data added
    '''
    if nvidia_metrics_cmd_result is not None:
        try:
            gpu_util_list = common_parser.get_col_from_df(nvidia_metrics_cmd_result, 'utilization.gpu [%]')
            gpu_average_utilization = sum(gpu_util_list)/len(gpu_util_list)
            return gpu_average_utilization
        except Exception as err:
            common_logging.log_error("data_collector_nvidia_gpu:get_nvidia_gpu_avg_utilization",
                                     "could not parse gpu utilization from nvidia-smi"+str(err))
            return None
    return None