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

import subprocess  # Importing the subprocess module to execute commands
import logging  # Importing the logging module to handle logging

'''

Module to get output of command

'''

import syslog

import subprocess


def call_command(command):
    """
    Call a command using subprocess and return the output or log errors using syslog.
    Args:
        command (str): The command to be executed.
    Returns:
        str or None: The output of the command or None if an error occurred.
    """
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                shell=True, check=False)
        if output.returncode == 0:
            return output.stdout.strip() if output.stdout else None
        # Log an error message with the command's non-zero exit status and the error output
        syslog.openlog(ident="invoke_commands", logoption=syslog.LOG_PID)
        syslog.syslog(syslog.LOG_ERR, f"Command returned non-zero exit status: {output.returncode}")
        syslog.syslog(syslog.LOG_ERR, f"Error output: {output.stderr}")
        return None

    except Exception as exc:
        syslog.openlog(ident="invoke_commands", logoption=syslog.LOG_PID)
        syslog.syslog(syslog.LOG_ERR, f"An error occurred: {exc}")
        return None