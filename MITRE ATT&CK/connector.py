# Import STIX dependancies
from stix2 import TAXIICollectionSource
from stix2 import Filter
from stix2 import MemoryStore
from stix2 import CompositeDataSource
from stix2.v20 import AttackPattern
# Import TAXII requirements
from taxii2client.v20 import Collection
# Import Requests and RegEx modules
import requests
import re


class MitreAttack (object):
    # Method to connect to MITRE ATT&CK TAXII SERVER and return stix data
    def get_data(self):
        collections = {
            "enterprise_attack": "95ecc380-afe9-11e4-9b6c-751b66dd541e",
            "pre_attack": "062767bd-02d2-4b72-84ba-56caef0f8658",
            "mobile_attack": "2f669986-b40b-4423-b720-4396ca6a462b"
        }

        collection = Collection (f"https://cti-taxii.mitre.org/stix/collections/{collections['enterprise_attack']}/")
        src = TAXIICollectionSource (collection)
        return src

    # Method to search retreived TAXII data to filter techniques by name
    def get_technique_by_name(self, thesrc, name):
        filt = [
            Filter ('type', '=', 'attack-pattern'),
            Filter ('name', '=', name)
        ]
        return thesrc.query (filt)

    # Method to search retreived TAXII data to filter techniques by keywords/ content
    def get_techniques_by_content(self, thesrc, content):
        techniques = thesrc.query ([Filter ('type', '=', 'attack-pattern')])
        return list (techniques)

    # Method to search retreived TAXII data to filter techniques by APT's who used them
    def get_group_by_alias(self, thesrc, alias):
        return thesrc.query ([
            Filter ('type', '=', 'intrusion-set'),
            Filter ('aliases', '=', alias)
        ])

    def get_data_with_STIX(self, thesrc, data):
        groups = thesrc.query ([Filter ("type", "=", data)])
        return groups

    def main(self):
        # Connect to TAXII server and retreive data
        src = self.get_data ()

        # Get user input on their search parameter
        option = int (input ("How do you want to query the MITRE data? \n 1= by technique name\n 2= by keyword\n 3= "
                             "by group \n 4= "
                             "STIX pattern\nEnter option: "))

        # Analyse the given option and make the repective call
        # Make a call for search via technique name
        if option == 1:
            technique_name = input ("Enter technique name: ")
            technique_name = str (technique_name)
            results = self.get_technique_by_name (src, technique_name)
            print (results)

        # Make a call for search via keyword
        elif option == 2:
            keyword = input ("Enter keyword: ")
            keyword = str (keyword)
            results = self.get_techniques_by_content (src, keyword)
            print (results)

        # Make a call for search via Threat Actor name
        elif option == 3:
            group_name = input ("Enter group name: ")
            group_name = str (group_name)
            results = self.get_group_by_alias (src, group_name)
            print (results)

        # Make a call using STIX pattern
        elif option == 4:
            stix_object = input ("Enter STIX object: ")
            stix_object = str (stix_object)
            results = self.get_data_with_STIX (src, stix_object)
            print (results)

        # Invalid option
        else:
            print ("Enter valid option ...")


x = MitreAttack ()
x.main ()
