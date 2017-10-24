import os
import json
import requests

from datetime import datetime

BASE_URL = 'https://handbooks.data.cardiff.ac.uk'
ASPECTS = {
    'module_list': 'modulesrunning',
    'module': 'module'
}

def get_module_list(school, year=datetime.now().year):
    """
    Retrieves the list of all modules running in the supplied school and year

    If no module list is returned from the API, returns None
    """

    # API expects uppercase school acronym
    school = school.upper()

    # Construct the API url
    module_list_url = '%s/%s/%s/%s' % (BASE_URL, ASPECTS['module_list'], school, year)

    # Retrieve the data
    r = requests.get(module_list_url)
    data = r.json()

    # Check we got something back
    if data.get('modRunning'):
        return data['modRunning']
    else:
        return None

def get_module_handbook(module_code, occurence = ''):
    """
    Retrieves the module handbook for the supplied module code and occurence (if any)
    """

    module_code = module_code.upper()

    # Construct the API url
    module_handbook_url = '%s/%s/%s/%s' % (BASE_URL, ASPECTS['module'], module_code, occurence)

    # Retrieve and return the data
    r = requests.get(module_handbook_url)
    data = r.json()

    return data
