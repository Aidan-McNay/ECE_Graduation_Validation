#=====================================================================
# class_api.py
#=====================================================================
# An API for getting information on Cornell classes
# This is a wrapper around the classes.cornell.edu API
# See here for more details: https://classes.cornell.edu/content/FA23/api-details
#
# Author: Aidan McNay
# Date: October 2nd, 2023

import requests, json

def get_rosters():
    """
    Gets all of the rosters that the API has information for

    Returns a list of strings for each term
    """
    url = "https://classes.cornell.edu/api/2.0/config/rosters.json"
    json_data   = requests.get(url).text
    json_object = json.loads(json_data)
    
    rosters = (json_object["data"])["rosters"]

    return [ roster["slug"] for roster in rosters ]

def get_class( course_name, term ):
    """
    Gets the information on a course for the given term
    Returns the information in a dictionary format (derived from JSON)

    Args:
     - course_name: Properly formatted course name (str)
     - term: Properly formatted course term (str)
    """

    course_name_components = course_name.split( " " )
    dept   = course_name_components[0]
    number = course_name_components[1]

    req_url = "https://classes.cornell.edu/api/2.0/search/classes.json?roster={}&subject={}&q={}".format( \
        term,  \
        dept,  \
        number \
    )

    json_data = requests.get( req_url ).text
    return json.loads(json_data)



