#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
import re

"""
Reference: https://www.github.com/
Connector Version: 1.0.0
API Version: 1.0.0
API Type: REST
"""

class GithubConnector(object):
    def __init__(self,
                 **kwargs):
        api_version = 'v1'
        self.base_url = "https://www.github.com"
        self.headers = {"Accept": "*"}
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
            url = "{0}".format(self.base_url) #https://cvedetails.com
            response = requests.request("GET", url)
            if response.status_code < 500:
                return True
            else:
                return False
        except KeyError:
            return False

    def request_handler(self, method, endpoint,
                        **kwargs):
        try:
            base_url = "{0}/{1}".format(self.base_url, endpoint)
            base_url=str(base_url)
            if method == "GET":
                response = requests.get(base_url)
                #print(response.text)
                if response.status_code == 200:
                    return response.text
                else:
                    return false
            else:
                return {self.result: 'Invalid Method {}\
                         Requested!'.format(method),
                        self.execution_status: self.ERROR}

        except Exception as e:
            response_data = {'response': str(e)}
            execution_status = self.ERROR
        return {self.result: response_data,
                self.execution_status: execution_status}

    def search_repo_according_to_stars(self, search, **kwargs):
        '''
        This action is to query and get back information regarding a topic on github
        seach: Enter the search we want to search for
        '''
        endpoint='search?o=desc&q={}&s=stars&type=Repositories'.format(search)
        response = self.request_handler('GET',endpoint)
        return response

    def search_repo_accoring_to_relavance(self, search, **kwargs):
        '''
        This action is to query and get back information regarding a topic on github based on search_repo_accoring_to_relavance
        search: Enter the search term we want to search for
        '''
        endpoint = 'search?q={}'.format(search)
        response = self.request_handler('GET', endpoint)
        return response


    def check_if_valid(self, data, **kwargs):
        '''
        This function is to check if the entered CVE ID is check_if_valid
        '''
        if """We couldn’t find any repositories matching """ in data:
            return False
        else:
            return True

    def get_required_data(self, data, **kwargs):
        '''
        This function is to query information from the raw html data
        '''
        soup = BeautifulSoup(data, 'html.parser')
        list = soup.findall('li', {'class':'repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source'})
        return list.text.strip()

    def format_search(self, search, **kwargs):
        '''
        This function is used to format a normal search string into a github search
        '''
        search=search.replace(" ","+")
        return search

x=GithubConnector()
search=str(input("Enter search string: "))
search=x.format_search(search=search)
x1=x.search_repo_according_to_stars(search=search)
status=x.check_if_valid(x1)
if(status==True):
    a=x.get_required_data(x1)
    print(a)
else:
    print("We couldn’t find any repositories matching ")
