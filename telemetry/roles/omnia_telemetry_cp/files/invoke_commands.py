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


def get_logger():
    # Create a logger with a specific name, so it can be retrieved consistently across modules
    logger = logging.getLogger("invoke_commands")
    if not logger.handlers:
        # Only configure the logger if it doesn't already have handlers
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(process)d-%(levelname)s : %(message)s')
        file_handler = logging.FileHandler('/tmp/demofile2.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def call_command(command):
    logger = get_logger()
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        if output.returncode == 0:
            return output.stdout.strip() if output.stdout else None
        else:
            logger.error(f"Command returned non-zero exit status: {output.returncode}")
            logger.error(f"Error output: {output.stderr}")
            return None

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return None


