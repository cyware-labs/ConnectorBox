#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
import re
import csv

"""
Reference: https://shield.mitre.org/
Connector Version: 1.0.0
API Version: 1.0.0
API Type: REST
"""

class ShieldConnector(object):
    def __init__(self,
                 **kwargs):
        api_version = 'v1'
        self.base_url = "https://shield.mitre.org/"
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
            base_url = "{0}/{1}".format(self.base_url, endpoint)
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

    def action_get_details(self, type, ID, **kwargs):
        '''
        This action is to query and get back information regarding a particular Shield item
        Type: Is it a technique or tactic ?
        ID: Enter the ID of the Item we wish to search for
        '''
        endpoint='{0}/{1}'.format(type,ID)
        response = self.request_handler('GET',endpoint)
        return response

    def get_required_data(self, data, **kwargs):
        '''
        This function is to query information from the raw html data
        '''
        soup = BeautifulSoup(data, 'html.parser')
        summary = soup.find('div', {'class':'col-xs-12 col-sm-8'})
        summary = summary.text
        a = soup.find_all('tbody')
        opportunities = a[0].text
        use_cases = a[1].text
        proceure = a[2].text
        attack_techniques = a[3].text

        print(opportunities)
        print(use_cases)
        print(attack_techniques)

    def get_summary(self, data, **kwargs):
        soup = BeautifulSoup(data, 'html.parser')
        summary = soup.find('div', {'class':'col-xs-12 col-sm-8'})
        summary = summary.text
        return summary

    def get_opportunities(self, data, **kwargs):
        soup = BeautifulSoup(data, 'html.parser')
        a = soup.find_all('tbody')
        opportunities = a[0].text
        return opportunities

    def get_usecases(self, data, **kwargs):
        soup = BeautifulSoup(data, 'html.parser')
        a = soup.find_all('tbody')
        use_cases = a[1].text
        return use_cases

    def get_procedure(self, data, **kwargs):
        soup = BeautifulSoup(data, 'html.parser')
        a = soup.find_all('tbody')
        procedure = a[2].text
        return procedure

    def get_attacktechnique(self, data, **kwargs):
        soup = BeautifulSoup(data, 'html.parser')
        a = soup.find_all('tbody')
        attack_techniques = a[3].text
        return attack_techniques

    def populate(self, list, **kwargs):
        file = open('shield.csv','w')
        writer = csv.writer(file)
        writer.writerow(["ID", "summary", "opportunities", "usecases", "procedure", "attack techniques"])
        for id in list:
            response = self.action_get_details(type = "techniques", ID= id.strip())
            summary = self.get_summary(response)
            opportunities = self.get_opportunities(response)
            usecases = self.get_usecases(response)
            procedure = self.get_procedure(response)
            attack_techniques = self.get_attacktechnique(response)
            print("writing")
            writer.writerow([id.strip(), summary.strip(), opportunities.strip(), usecases.strip(), procedure.strip(), attack_techniques.strip()])

    def get_ids(self):
        baseurl = 'https://shield.mitre.org/techniques/'
        response = requests.get(baseurl)
        soup = BeautifulSoup(response.text, "html.parser")

        link_list_temp = []
        link_list_temp1 = []
        link_list = []

        for link in soup.find_all('a', href=True):
            link_list_temp.append(link['href'])
        for link in link_list_temp:
            if "/techniques" in link:
                filtered = link.partition("/techniques/")[2]
                link_list_temp1.append(filtered)

        for link in link_list_temp1:
            if "/" in link:
                link = link.replace("/"," ")
                link_list.append(link)

        link_list = list(dict.fromkeys(link_list))
        link_list.sort()
        return link_list

x=ShieldConnector()
ids = x.get_ids()
x.populate(ids)
#id = str(input("Enter technique ID: "))
#response = x.action_get_details(type="techniques", ID=id)
#if response == False:
#    print("Check the entered data")
#results = x.get_summary(response)
#print(results)
