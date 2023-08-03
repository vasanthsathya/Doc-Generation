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
#---

from io import StringIO
import syslog
import pandas as pd

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
        syslog.syslog(syslog.LOG_ERR, "Exception in csv parsing: "+ err)
        return None

def get_col_from_csv(command_input, col_name):
    '''
    i/p: gets dataframe and column name as input
    o/p: extract column data from dataframe into a list and return
    '''
    try:
        dataframe = get_df_format(command_input)
        return dataframe[col_name].tolist()
    except Exception as err:
        syslog.syslog(syslog.LOG_ERR, "Exception in parsing column from dataframe: " + err)
        return None