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
Module to gather health check metrics.
'''

import data_collector_kubernetes
import data_collector_storage
import data_collector_os


class HealthCheckMetricCollector:
    '''
    HealthCheckMetricCollector class is responsible for collecting all health check metrics.
    '''
    def __init__(self):
        self.health_check_metric_output_dict={}

    def get_using_kubernetes(self):
        '''
        This method initiates kubernetes calls to data_collector_kubernetes and retrieves necessary values.
        '''
        #get using "kubectl get pods" commands
        kubernetes_pods_dict=data_collector_kubernetes.get_kubectl_get_pods()
        self.health_check_metric_output_dict["Kubernetespodsstatus"]=\
            kubernetes_pods_dict["Kubernetespodsstatus"]
        #get using "kubectl get nodes" commands
        kubernetes_nodes_dict=data_collector_kubernetes.get_kubectl_get_nodes()
        self.health_check_metric_output_dict["Kuberneteschildnode"]=\
            kubernetes_nodes_dict["Kuberneteschildnode"]
        self.health_check_metric_output_dict["kubernetesnodesstatus"]=\
            kubernetes_nodes_dict["kubernetesnodesstatus"]
        #get using "kubectl get componentstatus" commands
        kubernetes_component_status_dict=data_collector_kubernetes.get_kubectl_get_cs()
        self.health_check_metric_output_dict["kubernetescomponentsstatus"]=\
            kubernetes_component_status_dict["kubernetescomponentsstatus"]

    def get_health_node_dmesg(self):
        '''
           This method checks if dmesg is giving some output or not.
        '''
        dmesg_op_dict = data_collector_os.get_health_node_dmesg()
        self.health_check_metric_output_dict["Dmesg"] = dmesg_op_dict["Dmesg"]

    def get_beegfs_details(self):
        '''
            This method checks if beeGFS client is reachable or not.
        '''
        beegfs_op_dict = data_collector_storage.get_beegfs_details()
        self.health_check_metric_output_dict["Beegfs client Reachable"] = beegfs_op_dict["Beegfs client Reachable"]

    def metric_collector(self, aggregation_level="compute"):
        '''
        This method aggregates all the health check parameters.
        '''
        self.health_check_metric_output_dict={}
        self.get_health_node_dmesg()
        self.get_beegfs_details()
        if aggregation_level in ["manager", "manager, login"]:
            # Get following information's through kubernetes
            # 1.Kubernetespodsstatus
            # 2.Kuberneteschildnode
            # 3.kubernetesnodesstatus
            # 4.kubernetescomponentsstatus
            self.get_using_kubernetes()
