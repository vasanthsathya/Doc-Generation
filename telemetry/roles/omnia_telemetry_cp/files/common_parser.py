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

#common_parser.py
#!/usr/bin/env python3
'''
	This module contains all the parsing related methods.
	For parsing any command prompt output, 
    this module should be imported and relevant methods should be used.
'''

from io import StringIO
import pandas as pd
import yaml
import common_logging

#-----------------------dataframe parser-----------------------------------------------

def get_df_format(command_input):
    '''
    i/p: gets csv format output of any command as input and the column name whose data is required
    o/p: convert df to dict of list and return.
    '''
    try:
        csv_string = StringIO(command_input)
        dataframe = pd.read_csv(csv_string, sep=",", header=0)
        dataframe.columns = dataframe.columns.str.strip()
        return dataframe
    except Exception as err:
        common_logging.log_error("data_collector_nvidia_gpu:get_nvidia_metrics_output",
                                 "nvidia-smi command did not give output for gpu metrics." + str(err))
        return None

def get_col_from_df(dataframe, col_name):
    '''
    i/p: gets dataframe and column name as input
    o/p: extract column data from dataframe into a list and return
    '''
    try:
        return dataframe[col_name].tolist()
    except Exception as err:
        common_logging.log_error("data_collector_nvidia_gpu:get_nvidia_metrics_output",
                                 "nvidia-smi command did not give output for gpu metrics." + str(err))
        return None

def parse_yaml_file(filepath):

    '''
    This module parses yaml file and provides the dictionary output

    Args:
        filepath (str): The file path along with filename
    '''

    cfg = {}
    try:
        with open(f'{filepath}', 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        return cfg
    except Exception as ex:
        # Log the error message with the error output
        common_logging.log_error("common_parser:parse_yaml_file",
                                 "Error in parsing inputs for timescaledb connection" + str(ex))
        return cfg