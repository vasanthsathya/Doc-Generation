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

from gpu_metric_collector import GPUMetricCollector as GMC

class DictConditional(dict):
    def __init__(self, cond=lambda x: x is not None):
        self.cond = cond
    def __setitem__(self, key, value):
        if not self.cond(value):
            if key in self:
                del self[key]
        else:
            dict.__setitem__(self, key, value)


def main():
    
    gpu_metric_output_dict = DictConditional(lambda x: x is not None)
    cmd_output_dict = {}

    gpu_metric_collector = GMC()
    #if collect_regular_metrics == true:
    gpu_metric_collector.metric_collector("node", gpu_metric_output_dict)

    #print output
    print("print result: "+ str(gpu_metric_output_dict))

if __name__ == "__main__":
    main()