#=====================================================================
# class_api.py
#=====================================================================
# An API for getting information on Cornell classes
# This is a wrapper around the classes.cornell.edu API
# See here for more details: https://classes.cornell.edu/content/FA23/api-details
#
# Author: Aidan McNay
# Date: October 2nd, 2023

import api
import requests, json, copy

#---------------------------------------------------------------------
# Primary API functions
#---------------------------------------------------------------------

# Cache get_rosters response in an external variable
_cached_rosters = None

def get_rosters():
    """
    Gets all of the rosters that the API has information for

    Returns a list of strings for each term
    """
    global _cached_rosters

    if( _cached_rosters != None ): # Use cached result
        return _cached_rosters.copy()
    
    url = "https://classes.cornell.edu/api/2.0/config/rosters.json"
    json_data   = requests.get( url ).text
    json_object = json.loads( json_data )
    
    rosters      = ( json_object["data"] )[ "rosters" ]
    roster_names = [ roster["slug"] for roster in rosters ]

    _cached_rosters = roster_names # Cache the names for later

    return roster_names.copy()

# Cache get_class responses in an external variable
_cached_classes = {}

def get_class( course_name, term, dump = False, file_name = None ):
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

    Possible Exceptions (defined in api.api_exceptions)
     - TermNotFoundError: We don't have information on the given term
     - DeptNotFoundError: Either the department doesn't exist, or it didn't
                          offer any classes that term
     - ClassNotFoundError: The given class wasn't found during that term
    """

    course_name_components = course_name.split( " " )
    dept   = course_name_components[0]
    number = course_name_components[1]
    data_key = ( dept, term )

    if( term not in get_rosters() ): # The requested term isn't one we have data for
        raise api.api_exceptions.TermNotFoundError( term )

    if( data_key not in _cached_classes.keys() ): # Need to populate with the relevant information
        req_url = "https://classes.cornell.edu/api/2.0/search/classes.json?roster={}&subject={}".format( \
            term,  \
            dept
        )
        json_data   = requests.get( req_url ).text
        json_object = json.loads( json_data )

        if( json_object[ "status" ] != "success" ): # The department wasn't found for this term
            raise api.api_exceptions.DeptNotFoundError( dept, term )
        
        # Store the data for that department and term
        _cached_classes[ data_key ] = json_object[ "data" ][ "classes" ]

    # Find the data for our given class in the term
    class_entry = None
    correct_entry = lambda x : ( x[ "catalogNbr" ] == number )
    for entry in _cached_classes[ data_key ]:
        if correct_entry( entry ):
            class_entry = copy.deepcopy( entry )
            break
    
    if( class_entry == None ): # The class wasn't found
        raise api.api_exceptions.ClassNotFoundError( course_name, term )
        
    # Dumpt the data, if requested
    if( dump ):
        formatted_str = json.dumps( class_entry, indent = 2 )
        f = open( file_name, "w" )
        f.write( formatted_str )
        f.close()

    return class_entry



