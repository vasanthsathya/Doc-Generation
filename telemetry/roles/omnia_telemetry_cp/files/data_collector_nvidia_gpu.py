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
Module to gather nvidia gpu metrics
'''

import parser
import syslog
import invoke_commands as ic

# --------------------------------NVIDIA GPU metric collection---------------------------------
def get_nvidia_metrics_output():
    '''
    This method collects command output for nvidia-smi command for gpu metrics
    :return: nvidia query output
    '''
    nvidia_metrics_query = "nvidia-smi --query-gpu=temperature.gpu,utilization.gpu " \
                           "--format=csv,nounits"
    command_result = ic.call_command(nvidia_metrics_query)
    return command_result


def get_nvidia_gpu_temp(nvidia_metrics_cmd_result, gpu_metric_output_dict):
    '''
    This method collects nvidia gpu temp from nvidia query output
    and stores it in gpu metric dictionary
    :param nvidia_metrics_cmd_result: nvidia query output
    :param gpu_metric_output_dict: dictionary with nvidia gpu temperature data added
    '''
    if nvidia_metrics_cmd_result is not None:
        try:
            gpu_temp_list = parser.get_col_from_csv(nvidia_metrics_cmd_result, 'temperature.gpu')
            for index, item in enumerate(gpu_temp_list):
                gpu_metric_output_dict["gpu_temperature:gpu" + str(index)] = item
        except Exception as err:
            syslog.syslog(syslog.LOG_ERR, "Exception thrown in get_nvidia_gpu_temp :" + err)
    else:
        syslog.syslog(syslog.LOG_ERR, "nvidia-smi command did not give output for gpu metrics.")


def get_nvidia_gpu_utilization(nvidia_metrics_cmd_result, gpu_metric_output_dict):
    '''
    This method collects nvidia gpu utilization from nvidia query output
    and stores it in gpu metric dictionary
    :param nvidia_metrics_cmd_result: nvidia query output
    :param gpu_metric_output_dict: dictionary with nvidia gpu utilization data added
    '''
    if nvidia_metrics_cmd_result is not None:
        try:
            gpu_utilization_list = parser. \
                get_col_from_csv(nvidia_metrics_cmd_result, 'utilization.gpu [%]')
            for index, item in enumerate(gpu_utilization_list):
                gpu_metric_output_dict["gpu_utilization:gpu" + str(index)] = item
        except Exception as err:
            syslog. \
                syslog(syslog.LOG_ERR, "Exception thrown in get_nvidia_gpu_utilization :" + err)
    else:
        syslog.syslog(syslog.LOG_ERR, "nvidia-smi command did not give output for gpu metrics.")


def get_nvidia_gpu_avg_utilization(nvidia_metrics_cmd_result, gpu_metric_output_dict):
    '''
    This method calculates average gpu utilization on the node
    and stores it in gpu metric dictionary
    :param nvidia_metrics_cmd_result: nvidia query output
    :param gpu_metric_output_dict: dictionary with nvidia gpu average utilization data added
    '''
    if nvidia_metrics_cmd_result is not None:
        try:
            gpu_utilization_list = parser. \
                get_col_from_csv(nvidia_metrics_cmd_result, 'utilization.gpu [%]')
            gpu_metric_output_dict["gpu_utilization:average"] = \
                sum(gpu_utilization_list) / len(gpu_utilization_list)
        except Exception as err:
            syslog.syslog(syslog.LOG_ERR, "Exception thrown in get_nvidia_gpu_avg_utilization :" + err)
    else:
        syslog.syslog(syslog.LOG_ERR, "nvidia-smi command did not give output for gpu metrics.")