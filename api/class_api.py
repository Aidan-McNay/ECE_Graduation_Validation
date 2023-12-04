"""
#=====================================================================
# class_api.py
#=====================================================================
# An API for getting information on Cornell classes
# This is a wrapper around the classes.cornell.edu API
# See here for more details: https://classes.cornell.edu/content/FA23/api-details
#
# Author: Aidan McNay
# Date: October 2nd, 2023
"""

import json
import copy
from typing import List, Tuple

import requests

import exceptions as excp
import ui

#---------------------------------------------------------------------
# Primary API functions
#---------------------------------------------------------------------

# Cache get_rosters response in an external variable
_CACHED_ROSTERS = None

def get_rosters() -> List[str]:
    """
    Gets all of the rosters that the API has information for

    Returns a list of strings for each term
    """
    global _CACHED_ROSTERS

    if _CACHED_ROSTERS is not None: # Use cached result
        return _CACHED_ROSTERS.copy()

    url = "https://classes.cornell.edu/api/2.0/config/rosters.json"
    json_data   = requests.get( url, timeout = 10 ).text
    json_object = json.loads( json_data )

    rosters      = ( json_object["data"] )[ "rosters" ]
    roster_names = [ roster["slug"] for roster in rosters ]

    _CACHED_ROSTERS = roster_names # Cache the names for later

    return roster_names.copy()

# Cache get_class responses in an external variable
_cached_classes = {}

def populate_data( term: str, dept: str ) -> None:
    """
    Populates the cached classes with the requested data
    """
    req_url =  "https://classes.cornell.edu/api/2.0/search/classes.json?" + \
              f"roster={ term }&subject={ dept }"

    json_data   = requests.get( req_url, timeout = 10 ).text
    json_object = json.loads( json_data )

    if json_object[ "status" ] != "success": # The department wasn't found for this term
        raise excp.api_exceptions.DeptNotFoundError( dept, term )

    # Store the data for that department and term
    _cached_classes[ ( dept, term ) ] = json_object[ "data" ][ "classes" ]

def get_class( course_name: str, term: str,
               dump: bool = False, file_name: str = "" ) -> dict:
    """
    Gets the information on a course for the given term
    Returns the information in a dictionary format (derived from JSON), or
    -1 if not found

    For debugging purposes, the function also allows the option to dump
    the JSON data to a file for looking at the response

    Args:
     - course_name: Properly formatted course name (str)
     - term: Properly formatted course term (str)
     - dump: Whether to dump the information or not (bool)
     - file_name: The file to dump to, if dumping information (str)

    Possible Exceptions (defined in exceptions.api_exceptions)
     - TermNotFoundError: We don't have information on the given term
     - DeptNotFoundError: Either the department doesn't exist, or it didn't
                          offer any classes that term
     - ClassNotFoundError: The given class wasn't found during that term
    """

    course_name_components = course_name.split( " " )
    dept   = course_name_components[0]
    number = course_name_components[1]
    data_key = ( dept, term )

    if term not in get_rosters(): # The requested term isn't one we have data for
        raise excp.api_exceptions.TermNotFoundError( term )

    if data_key not in _cached_classes: # Need to populate with the relevant information
        populate_data( term, dept )

    # Find the data for our given class in the term
    class_entry = None
    for entry in _cached_classes[ data_key ]:
        if entry[ "catalogNbr" ] == number:
            class_entry = copy.deepcopy( entry )
            break

    if class_entry is None: # The class wasn't found
        raise excp.api_exceptions.ClassNotFoundError( course_name, term )

    # Dumpt the data, if requested
    if dump:
        with open( file_name, "w", encoding = "utf-8" ) as file:
            file.write( json.dumps( class_entry, indent = 2 ) )

    return class_entry

#---------------------------------------------------------------------
# Derived Functions
#---------------------------------------------------------------------

def in_future( term: str ) -> bool:
    """
    Determines if a term is offered in the future (based on our available rosters)
    Returns the corresponding bool

    Args:
     - term (str): The relevant term we want to check
    """
    for avail_roster in get_rosters():
        if ui.parser.term_is_later( avail_roster, term ):
            # The avail_roster occurs later than the given term
            return False
    return True

def most_recent_term( course_name: str, future_term: str ) -> Tuple[dict, str]:
    """
    Assumes that the user is trying to take the course in the future, and grabs
    data from the most recent offering, returning the JSON data and term sourced

    This will check every roster available, going back from most to least recent, and
    is therefore very API-intensive; calls to this should be sparse, even with JSON caching
    """

    # Get the rosters, in order from most to least recent
    rosters = get_rosters()
    rosters.sort( key = ui.parser.term_index, reverse = True )

    # Go through them until we get a match
    for term in rosters:
        try:
            json_object = get_class( course_name, term )
            return json_object, term
        except ( excp.api_exceptions.ClassNotFoundError, excp.api_exceptions.DeptNotFoundError ):
            continue # Didn't find it, so just move on to the next roster

    # If we got here, we didn't find it in any rosters
    raise excp.api_exceptions.NoClassInfoError( course_name, future_term )
