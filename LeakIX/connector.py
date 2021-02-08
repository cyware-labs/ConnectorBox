#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

"""
Reference: https://leakix.net/
Connector Version: 1.0.0
API Version: 1.0.0
API Type: REST
"""


class LeakIXConnector (object):
    def __init__(self,
                 **kwargs):
        api_version = 'v1'
        self.base_url = "https://leakix.net"
        self.headers = {"Accept": "application/json"}
        self.SUCCESS = "SUCCESS"
        self.ERROR = "ERROR"
        self.execution_status = "execution_status"
        self.result = "result"

    def test_connection(self, **kwargs):
        """
        Test Connection
        Used for checking the connectivity of the base url.
        :return: boolean (True/False)
        """
        try:
            url = "{0}".format (self.base_url)  # https://leakix.net
            response = requests.request ("GET", url)
            if response.status_code < 500:
                return True
            else:
                return False
        except KeyError:
            return False

    def request_handler(self, method, endpoint,
                        **kwargs):
        try:
            base_url = "{0}/{1}".format (self.base_url,
                                         endpoint)  # Eg. Base url= https://www.leaix.net #endpoint= host/10.10.10.10
            if method == "GET":
                response = requests.request ("GET", base_url,
                                             headers=self.headers)
            else:
                return {self.result: 'Invalid Method {}\
                         Requested!'.format (method),
                        self.execution_status: self.ERROR}

            status_code = response.status_code
            response_data = {'status_code': status_code}
            # response handling
            if status_code < 300:
                execution_status = self.SUCCESS
                response_data['response'] = response.json ()
            elif status_code < 500:
                execution_status = self.ERROR
                if status_code == 401:
                    response_data['response'] = 'Missing authentication data.'
                elif status_code == 403:
                    response_data['response'] = 'You do not have permission\
                                                 to perform this task'
                else:
                    response_data['response'] = response.json ()
            else:
                execution_status = self.ERROR
                response_data['response'] = 'Server Error, Try again'
        except Exception as e:
            response_data = {'response': str (e)}
            execution_status = self.ERROR
        return {self.result: response_data,
                self.execution_status: execution_status}

    def action_get_leak(self, host, **kwargs):
        '''
        The action is used to check if the given host contains any leaks
        host: Enter the host IP. (Eg: 10.10.10.10)
        '''
        endpoint = 'search?q=ip:"{}"&scope=leak'.format (host)
        response = self.request_handler ('GET', endpoint)
        return response

    def action_get_service(self, host, **kwargs):
        '''
        The action is used to check if the given host contains any services
        host: Enter the host IP. (Eg: 10.10.10.10)
        '''
        endpoint = 'search?q=ip:"{}"&scope=service'.format (host)
        response = self.request_handler ('GET', endpoint)
        return response

    def action_search_host(self, host, **kwargs):
        '''
        This action is used to check a particular host for both leaks and services
        host: Enter the host IP
        '''
        endpoint = 'host/{}'.format (host)
        response = self.request_handler ('GET', endpoint)
        return response

    def action_search_by_query_for_leak(self, host, **kwargs):
        '''
        This action is used to get data based off a query from the user
        host: Enter the host IP
        '''
        endpoint = 'search?q={}&scope=leak'.format (host)
        response = self.request_handler ('GET', endpoint)
        return response

    def action_search_by_query_for_service(self, host, **kwargs):
        '''
        This action is used to get data based off a query from the user
        host: Enter the host IP
        '''
        endpoint = 'search?q={}&scope=service'.format (host)
        response = self.request_handler ('GET', endpoint)
        return response


x = LeakIXConnector ()
data = input ('Enter IP: ')
data = str (data)
x1 = x.action_get_service (host=data)
print (x1)
