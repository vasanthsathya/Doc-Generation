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

#!/usr/bin/env python3

'''
    This module contains tasks required for database update
    The query should be created along with timestamp before updating
    the database.
'''

import psycopg2
import common_parser
import common_logging
import time
import datetime

filepath = "/opt/omnia/telemetry/.timescaledb/config.yml"

def db_connect(dbdata):
    '''
    This module creates Database Connection
    '''

    dbuser = dbdata['username']
    dbpwd = dbdata['password']
    dbhost = dbdata['host']
    dbport = dbdata['port']
    dbtelemetry = dbdata['database']
    #Create connection string for connecting to db
    connection_string = f"postgres://{dbuser}:{dbpwd}@{dbhost}:{dbport}/{dbtelemetry}".format(
        dbuser = dbuser, dbpwd = dbpwd, dbhost = dbhost, dbport = dbport, dbtelemetry = dbtelemetry)
    try:
        conn = psycopg2.connect(connection_string)
        if conn is not None:
            conn.autocommit = True
    except Exception as ex:
        # Log the error message with the error output
        common_logging.log_error("dbupdate:db_connect",
                                 "Error in connecting to timescaledb" + str(ex))
    return conn

def db_close(db_conn):
    '''
    This module closes the database connection object
    '''

    db_conn.close()

def create_db_query(regular_metric_output_dict,health_check_metric_output_dict,gpu_metric_output_dict,service_tag):
    '''
    Database query creation
    :param regular_metric_output_dict: Regular metrics data dictionary
    :param health_check_metric_output_dict: health check metrics data dictionary
    :param gpu_metric_output_dict: GPU metrics data dictionary
    :param service_tag: System serial number/service tag
    '''
    if service_tag is not None:
        db_query_list=[]
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        if regular_metric_output_dict:
            for key,value in regular_metric_output_dict.items():
                if value!="":
                    label = key+" Regular Metric"
                    db_data_tuple = (key,"Regular Metric",label,value,service_tag,timestamp)
                    db_query_list.append(db_data_tuple)
        
        if health_check_metric_output_dict:
            for key,value in health_check_metric_output_dict.items():
                if value!="":
                    label = key+" Health Check Metric"
                    db_data_tuple = (key,"Health Metric",label,value,service_tag,timestamp)
                    db_query_list.append(db_data_tuple)

        if gpu_metric_output_dict:
            for key,value in gpu_metric_output_dict.items():
                if value!="":
                    label = key+" GPU Metric"
                    db_data_tuple = (key,"GPU Metric",label,value,service_tag,timestamp)
                    db_query_list.append(db_data_tuple)
        return db_query_list
    else:
         common_logging.log_error("dbupdate:create_db_query","Service Tag is empty.")

def db_insert(db_conn, db_query):
    '''
    This module inserts data into database
    '''

    try:
        db_cursor = db_conn.cursor()
        sql_insert_query = """INSERT INTO omnia_telemetry.metrics \
                           (id, context, label, value, system, time )\
                           VALUES (%s,%s,%s,%s,%s,%s)"""
        db_cursor.executemany(sql_insert_query, db_query)
        db_conn.commit()
        db_cursor.close()
    except Exception as ex:
        # Log the error message with the error output
        common_logging.log_error("dbupdate:db_insert",
                                 "Error in inserting data to Database" + str(ex))
        db_close(db_conn)

def dbupdate(regular_metric_output_dict, health_check_metric_output_dict, gpu_metric_output_dict,\
             service_tag):
    '''
    This module updates the Timescaledb on the control plane with telemetry data

    Args:
       Regular metric {dict}, GPU Metric {dict}, Health Check Metric {dict}
    '''

    #Fetch the db connect info from config file
    dbdata = common_parser.parse_yaml_file(filepath)

    #Connect to the database
    db_conn = db_connect(dbdata)

    if db_conn is not None:
        #Create sql query
        db_query = create_db_query(regular_metric_output_dict,health_check_metric_output_dict,gpu_metric_output_dict,service_tag)

        #Insert into database
        db_insert(db_conn, db_query)

        db_close(db_conn)
