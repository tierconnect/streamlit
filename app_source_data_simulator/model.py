import os
import json
import requests
from utilities import Utilities


class Resources:
    def __init__(self, utilities: Utilities):
        self.gtin_resource = ""
        self.location_resource = ""
        self.organization_map = None
        self.utils = utilities
        self.load_files()

    def load_files(self):
        file = self.utils.getenv('GLN_MAP')
        self.organization_map = json.loads(requests.get(file).text)

    def return_organizations(self):
        # This element is basically an array of Names
        only_org_sites_array = []
        for every_site in self.organization_map:
            only_org_sites_array.append(every_site['organization_name'])
        return only_org_sites_array

    def return_sites(self, organization):
        # This element is basically an array of items
        # that contains tuples of Site and the GLN itself
        only_sites_array = []

        for every_site in self.organization_map:
            if every_site['organization_name'] == organization:
                return every_site['sites']
        pass


util_class = Utilities()
resource = Resources(util_class)
