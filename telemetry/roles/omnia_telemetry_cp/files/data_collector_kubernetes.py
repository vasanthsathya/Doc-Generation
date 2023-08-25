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
Module to fetch parameters related to kubernetes.
'''

import common_parser
import invoke_commands
import common_logging
import utility

def get_kubectl_get_pods():
    '''
    Gets the following parameters
    Kubernetespodsstatus:Is the status for all pods OK
    '''
    dict_cluster_parameter_kubectl_pods={}
    dict_cluster_parameter_kubectl_pods["Kubernetespodsstatus"]=utility.Result.UNKNOWN.value
    flag_kubernetes_pods_status= True

    output=invoke_commands.call_command('kubectl get pods -A -o json')
    if output is not None:
        #Convert output to to json format
        pods_json=common_parser.get_json_format(output)
        if pods_json is not None:
            try:
                #Iterate over each entries in json. Each entry/item corresponds to individual pods of the command output : kubectl get pods -A
                for index in range(len(pods_json["items"])):
                    #Get the status and check if it is "Running" or not
                    if pods_json["items"][index]["status"]["phase"]!= "Running":
                        #Not Running so Fail
                        flag_kubernetes_pods_status= False
                        break
                if flag_kubernetes_pods_status is True:
                    dict_cluster_parameter_kubectl_pods["Kubernetespodsstatus"]=\
                        utility.Result.SUCCESS.value
                else:
                    dict_cluster_parameter_kubectl_pods["Kubernetespodsstatus"]=\
                        utility.Result.FAILURE.value
            except Exception as err:
                common_logging.log_error("data_collector_kubernetes:get_kubectl_get_pods",\
 "kubectl get pods -A json parsing issue: " + str(type(err)) +" "+ str(err))
        else:
            common_logging.log_error("data_collector_kubernetes:get_kubectl_get_pods",\
 "kubectl get pods -A json parsed output is None")
    else:
        common_logging.log_error("data_collector_kubernetes:get_kubectl_get_pods",\
 "kubectl get pods -A command output is None")
    return dict_cluster_parameter_kubectl_pods


def get_kubectl_get_nodes():
    '''
    Gets the following parameters
    Kuberneteschildnode: Are all Kubernetes child nodes up
    kubernetesnodesstatus: Is the status for all Kubernetes nodes OK
    '''
    dict_cluster_parameter_kubectl_nodes={}
    dict_cluster_parameter_kubectl_nodes["Kuberneteschildnode"]=utility.Result.UNKNOWN.value
    dict_cluster_parameter_kubectl_nodes["kubernetesnodesstatus"]=utility.Result.UNKNOWN.value
    flag_child_nodes_up=True
    flag_all_nodes_up=True
    #index of status (type) in json output
    index_status=4

    output=invoke_commands.call_command('kubectl get nodes -o json')
    if output is not None:
        nodes_json=common_parser.get_json_format(output)
        if nodes_json is not None:
            try:
                #Iterate over each entries in json. Each entry/item corresponds to individual nodes of the command output : kubectl get nodes
                #First entry will be for master node and the rest are for the child nodes
                for index in range(len(nodes_json["items"])):
                    #Get the status and check if it is "Ready" or not
                    if nodes_json["items"][index]["status"]["conditions"][index_status]["type"] != "Ready":
                        flag_all_nodes_up = False
                        #Check if child node
                        if index!=0:
                            flag_child_nodes_up = False
                            #break since we found non ready status in child nodes
                            break

                #set the parameters
                #kubernetesnodesstatus
                if flag_all_nodes_up is True:
                    dict_cluster_parameter_kubectl_nodes["kubernetesnodesstatus"]=\
                        utility.Result.SUCCESS.value
                else:
                    dict_cluster_parameter_kubectl_nodes["kubernetesnodesstatus"]=\
                        utility.Result.FAILURE.value
                #Kuberneteschildnode
                if flag_child_nodes_up is True:
                    dict_cluster_parameter_kubectl_nodes["Kuberneteschildnode"]=\
                        utility.Result.SUCCESS.value
                else:
                    dict_cluster_parameter_kubectl_nodes["Kuberneteschildnode"]=\
                        utility.Result.FAILURE.value
            except Exception as err:
                common_logging.log_error("data_collector_kubernetes:get_kubectl_get_nodes",\
 "kubectl get nodes json parsing issue: " +str(type(err)) +" "+ str(err))
        else:
            common_logging.log_error("data_collector_kubernetes:get_kubectl_get_nodes",\
 "kubectl get nodes json parsed output is None")
    else:
        common_logging.log_error("data_collector_kubernetes:get_kubectl_get_nodes",\
 "kubectl get nodes command output is None")

    return dict_cluster_parameter_kubectl_nodes


def get_kubectl_get_cs():
    '''
    Gets the following parameters
    kubernetescomponentsstatus:Are all expected agents and services up and running for active nodes?
    '''
    dict_cluster_parameter_kubectl_cs={}
    dict_cluster_parameter_kubectl_cs["kubernetescomponentsstatus"]=\
        utility.Result.UNKNOWN.value
    #index of component status (type) in json output
    index_cs=0

    output=invoke_commands.call_command('kubectl get componentstatus -o json')
    if output is not None:
        cs_json=common_parser.get_json_format(output)
        if cs_json is not None:
            try:
                #Iterate over each entries in json. Each entry/item corresponds to individual components of the command output : kubectl get componentstatus
                for index in range(len(cs_json["items"])):
                    if cs_json["items"][index]["metadata"]["name"] == "etcd-0":
                        if  cs_json["items"][index]["conditions"][index_cs]["type"] == "Healthy":
                            dict_cluster_parameter_kubectl_cs["kubernetescomponentsstatus"]=\
                                utility.Result.SUCCESS.value
                        else:
                            dict_cluster_parameter_kubectl_cs["kubernetescomponentsstatus"]=\
                                utility.Result.FAILURE.value
                        break
            except Exception as err:
                common_logging.log_error("data_collector_kubernetes:get_kubectl_get_cs",\
 "kubectl get componentstatus json parsing issue: " +str(type(err)) +" "+ str(err))
        else:
            common_logging.log_error("data_collector_kubernetes:get_kubectl_get_cs",\
 "kubectl get componentstatus json parsed output is None")
    else:
        common_logging.log_error("data_collector_kubernetes:get_kubectl_get_cs",\
 "kubectl get componentstatus command output is None")
    return dict_cluster_parameter_kubectl_cs