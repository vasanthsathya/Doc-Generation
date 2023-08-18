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
Module to gather amd gpu metrics
'''

import common_parser
import invoke_commands
import common_logging

# --------------------------------AMD GPU metric collection---------------------------------

def get_amd_gpu_temp():
    '''
    This method collects amd gpu temp from rocm query output
    and stores it in gpu metric dictionary
    '''
    amd_metrics_query = "rocm-smi -t --csv"
    command_result = invoke_commands.call_command(amd_metrics_query)
    if command_result is not None:
        gpu_temp = {}
        command_result_df = common_parser.get_df_format(command_result)
        try:
            gpu_temp['sensor_edge'] = common_parser.get_col_from_df(command_result_df,
                                                                'Temperature (Sensor edge) (C)')
        except Exception as err:
            gpu_temp['sensor_edge'] = None
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                                     "could not parse sensor_edge temp from rocm-smi" + str(err))
        try:
            gpu_temp['sensor_junction'] = common_parser.get_col_from_df(command_result_df,
                                                             'Temperature (Sensor junction) (C)')
        except Exception as err:
            gpu_temp['sensor_junction'] = None
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                                "could not parse sensor_junction temp from rocm-smi" + str(err))
        try:
            gpu_temp['sensor_memory'] = common_parser.get_col_from_df(command_result_df,
                                                                 'Temperature (Sensor memory) (C)')
        except Exception as err:
            gpu_temp['sensor_memory'] = None
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                                   "could not parse sensor_memory temp from rocm-smi" + str(err))
        try:
            gpu_temp['sensor_hbm0'] = common_parser.get_col_from_df(command_result_df,
                                                                'Temperature (Sensor HBM 0) (C)')
        except Exception as err:
            gpu_temp['sensor_hbm0'] = None
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                                     "could not parse sensor_hbm0 temp from rocm-smi" + str(err))
        try:
            gpu_temp['sensor_hbm1'] = common_parser.get_col_from_df(command_result_df,
                                                                'Temperature (Sensor HBM 1) (C)')
        except Exception as err:
            gpu_temp['sensor_hbm1'] = None
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                                     "could not parse sensor_hbm1 temp from rocm-smi" + str(err))
        try:
            gpu_temp['sensor_hbm2'] = common_parser.get_col_from_df(command_result_df,
                                                                'Temperature (Sensor HBM 2) (C)')
        except Exception as err:
            gpu_temp['sensor_hbm2'] = None
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                                     "could not parse sensor_hbm2 temp from rocm-smi" + str(err))
        try:
            gpu_temp['sensor_hbm3'] = common_parser.get_col_from_df(command_result_df,
                                                                'Temperature (Sensor HBM 3) (C)')
        except Exception as err:
            gpu_temp['sensor_hbm3'] = None
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                                     "could not parse sensor_hbm3 temp from rocm-smi" + str(err))
        return gpu_temp

    common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_temp",
                             "rocm-smi command did not give output for gpu temperature metrics.")
    return None


def get_amd_gpu_utilization():
    '''
    This method collects amd gpu utilization from rocm query output
    and stores it in gpu metric dictionary
    '''
    amd_metrics_query = "rocm-smi -u --csv"
    command_result = invoke_commands.call_command(amd_metrics_query)
    if command_result is not None:
        try:
            command_result_df = common_parser.get_df_format(command_result)
            gpu_util_list = common_parser.get_col_from_df(command_result_df, 'GPU use (%)')
            return gpu_util_list
        except Exception as err:
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_utilization",
                                     "could not parse gpu utilization from rocm-smi"+str(err))
            return None
    return None


def get_amd_gpu_avg_utilization():
    '''
    This method calculates average gpu utilization on the node
    and stores it in gpu metric dictionary
    '''
    amd_metrics_query = "rocm-smi -u --csv"
    command_result = invoke_commands.call_command(amd_metrics_query)
    if command_result is not None:
        try:
            command_result_df = common_parser.get_df_format(command_result)
            gpu_util_list = common_parser.get_col_from_df(command_result_df, 'GPU use (%)')
            gpu_average_utilization = sum(gpu_util_list)/len(gpu_util_list)
            return gpu_average_utilization
        except Exception as err:
            common_logging.log_error("data_collector_amd_gpu:get_amd_gpu_avg_utilization",
                                     "could not parse gpu utilization from rocm-smi"+str(err))
            return None
    return None