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
	Module to invoke all system commands
'''
import subprocess
import common_logging
import utility
import common_parser


def call_command(command):
    """
    Call a command using subprocess and return the output or log errors using syslog.

    Args:
        command (str or list): The command to be executed, as a string or a list of arguments.

    Returns:
        str or None: The output of the command or None if an error occurred.
    """
    try:
        if isinstance(command, str):
            # Split the command by space into a list of tokens
            command = common_parser.split_by_regex(command," ")
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
                                timeout=float(utility.dict_telemetry_ini["metric_collection_timeout"]),universal_newlines=True, check=False)
        # A return code of 0 means success,while a non-zero return code means failure.
        if output.returncode == 0:
            return output.stdout.strip() if output.stdout else None
        # Log an error message with the error output
        common_logging.log_error('invoke_commands:call_command', f"Error output: {output.stderr}")
    except subprocess.TimeoutExpired:
        common_logging.log_error('invoke_commands:call_command', f"Command invocation timeout: {command}")
    except Exception as exc:
        common_logging.log_error('invoke_commands:call_command', f"An error occurred: {exc}")
    return None


def run_command(command):
    """
        Call a command using subprocess and return the output or log errors using syslog.
        Args:
            command (str): The command to be executed.
        Returns:
            str or None: The output of the command or None if an error occurred.
       """
    try:
        command = command.split()
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True, check=False)

        return output.stdout.strip() if output.stdout else None
    except Exception as exc:
        common_logging.log_error('invoke_commands:run_command', f"An error occurred: {exc}")
    return None
