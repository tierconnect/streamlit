import os
import requests


class Utilities:
    def __init__(self):
        self.environment = None
        self.defaults = {
            'GTIN_FILE': 'https://storage.googleapis.com/mojix-devops-wildfire-bucket/source/gtin_sample.txt',
            'GLN_MAP': 'https://storage.googleapis.com/mojix-devops-wildfire-bucket/source/location_map.json',
            'EVENT_TYPES': 'ObjectEvent, TransformationEvent',
            'BIZSTEPS': 'commissioning, shipping, receiving, retail_selling'
        }

    def get_gtins(self):
        gtin = requests.get(self.getenv('GTIN_FILE'))
        gtin_list = gtin.text
        return gtin_list.split("\n")

    def getenv(self, variable):
        if variable in os.environ:
            return os.getenv(variable)
        else:
            return self.get_default(variable)

    def get_default(self, variable):
        if variable not in self.defaults.keys():
            return None
        return self.defaults[variable]
