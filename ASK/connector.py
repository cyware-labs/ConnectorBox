#!/usr/bin/env python
# -*- coding: utf-8 -*-
import html2text
import json
import requests
from bs4 import BeautifulSoup
import re
import csv

file = open('temp.txt','w')
"""
Reference: https://docs.splunksecuritye        #print(row[2])
ssentials.com/
Connector Version: 1.0.0
API Version: 1.0.0
API Type: REST
"""

class ShieldConnector(object):
    def __init__(self,
                 **kwargs):
        api_version = 'v1'
        self.base_url = "https://docs.splunksecurityessentials.com/"
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
            url = "{0}".format(self.base_url)
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
            base_url = "{0}{1}".format(self.base_url, endpoint)
            base_url=str(base_url)
            if method == "GET":
                response = requests.get(base_url)
                if response.status_code == 200:
                    return response.text
                else:
                    return False
            else:
                return {self.result: 'Invalid Method {}\
                         Requested!'.format(method),
                        self.execution_status: self.ERROR}

        except Exception as e:
            response_data = {'response': str(e)}
            execution_status = self.ERROR
        return {self.result: response_data,
                self.execution_status: execution_status}

    def action_initial_data(self,**kwargs):
        '''
        This action to get the initial response data
        '''

        endpoint='content-detail/uc0107/'
        response = self.request_handler('GET',endpoint)
        return response

    def action_get_details(self, keyword, **kwargs):
        '''
        This action is to query and get back information regarding a particular Splunk analytic
        Keyword: Enter the endpoint value from the get link list
        '''

        endpoint='content-detail/{}'.format(keyword)
        response = self.request_handler('GET',endpoint)
        return response

    def get_query(self, data, **kwargs):
        '''
        This function is to query the splunk get_query
        '''
        soup = BeautifulSoup(data, 'html.parser')
        query = soup.find_all('td',{'class':'splside'})
        list = []
        if query == "None" or len(query) == 0:
            backup = soup.find_all('pre', {'class':'search'})
            if backup != "None":
                for item in backup:
                    list.append(item.text)
                return list
            else:
                last = soup.find_all('code', {'class':'spl hljs'})
                for item in last:
                    list.append(item.text)
        else:
            for item in query:
                list.append(item.text)
            return list

    def get_mitre_techniques(self, data, **kwargs):
        soup = BeautifulSoup(data, 'html.parser')
        mitre_techniques=soup.find_all('div',{'class':'primary mitre_technique_displayElements'})
        list = []
        if str(mitre_techniques) != "None" :
            for technique in mitre_techniques:
                list.append(technique.text)
            return list

    def get_threat_actors(self, data, **kwargs):
        soup = BeautifulSoup(data, 'html.parser')
        threat_actor_detection = soup.find_all('div', {'class': 'mitre_threat_groupsElements'})
        list = []
        if str(threat_actor_detection) != "None":
            for actors in threat_actor_detection:
                list.append(actors.text)
            return list

    def populate(self, list, response, **kwargs):
        file = open('splunk_results.csv','w')
        writer = csv.writer(file)
        writer.writerow(["item", "query", "techniques", "actors"])
        for item in list:
            response = x.action_get_details(item)
            query = self.get_query(response)
            techniques = self.get_mitre_techniques(response)
            actors = self.get_threat_actors(response)
            print("writing ...")
            writer.writerow([item, str(query)[1:-1], str(techniques)[1:-1], str(actors)[1:-1]])


    def get_link_list(self, data, **kwargs):
        '''
        This function is to query the links present in the tags
        '''
        soup = BeautifulSoup(data, 'html.parser')
        link_list_temp = []
        link_list = []

        for link in soup.find_all('a', href=True):
            link_list_temp.append(link['href'])

        for link in link_list_temp:
            if "content-detail" in link:
                filtered = link.partition("content-detail/")[2]
                link_list.append(filtered)
        return link_list

x = ShieldConnector()
response = x.action_initial_data()
link_list = x.get_link_list(response)
count = 0

for link in link_list:
    count+=1
    print(str(count)+".", end= " ")
    print(str(link[:-1]))

endpoint = str(input("[+] Enter splunk analytic you want to query: "))
response = x.action_get_details(endpoint)

x.populate(link_list, response)
#query = x.get_query(response)
#techniques = x.get_mitre_techniques(response)
#actors = x.get_threat_actors(response)
#print(query)
