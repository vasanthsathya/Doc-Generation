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

#collector.py
#!/usr/bin/env python3
'''
   This is an interface to call telemetry collector.
   This will collect all supported metric values of different categories
   Steps are as below:
   step1: get all required input values from ini
   step2: understand platform environment and generate command set
   step3: generate random number in the range of 0-fuzzy offset
   step4: collect metrices in loop
     step41: sleep for generated random number
     step42: collect all metrices in dictionary
     step43: add collected values in DB on control plane
     step44: sleep for collection interval time
'''
