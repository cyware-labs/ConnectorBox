#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

"""
Reference: https://recon.dev/
Connector Version: 1.0.0
API Version: 1.0.0
API Type: REST
"""


class Recon (object):
    def __init__(self,
                 **kwargs):
        api_version = 'v1'
        self.base_url = "https://recon.dev/"
        self.headers = {"Accept": "application/json"}
        self.SUCCESS = "SUCCESS"
        self.ERROR = "ERROR"
        self.execution_status = "execution_status"
        self.result = "result"
        self.api = 'free-d6f1ad81-f87f-46c9-9558-7bad796666c0'

    def request_handler(self, method, endpoint,
                        **kwargs):
        try:
            base_url = "{0}/{1}".format (self.base_url,
                                         endpoint) 
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

    def action_get_data(self, domain, **kwargs):
        '''
        The action is used to check if the given host contains any leaks
        host: Enter the domain
        '''
        endpoint = 'api/search?key={api}&domain={domain}'.format(api=self.api,
                                                                 domain=domain)
        response = self.request_handler ('GET', endpoint)
        return response


x = Recon ()
data = input ('Enter domain: ')
data = str (data)
x1 = x.action_get_data (domain=data)
print (x1)
