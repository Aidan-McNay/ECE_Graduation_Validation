"""
#=====================================================================
# bulk_api.py
#=====================================================================
# A wrapper around class_api for bulk data population
#
# Author: Aidan McNay
# Date: December 8th, 2023
"""

import json
from typing import List, Tuple, Set, cast

# For whatever reason, grequests must be imported before requests
# - https://github.com/spyoungtech/grequests/issues/103

import grequests # Asynchronous parallel requests
import requests

from api import class_api
from obj.roster_entry_obj import ReqEntry
from ui.parser import get_dept_from_name

#---------------------------------------------------------------------
# Bulk Data Population
#---------------------------------------------------------------------
# Populates the stored cached class data in *parallel* for speedup
# <flashbacks to Operating Systems>

def bulk_populate_data( req_list: List[ Tuple[ str, str ] ] ) -> None:
    """
    Populates the stored data from a large list of data
    
    Each tuple in the provided list should be a (term, dept)
    """

    req_urls = [ class_api.api_url( x[0], x[1] ) for x in req_list ]

    # Create a set of unsent requests
    rs = ( grequests.get( u, timeout = 10 ) for u in req_urls )

    # Send all requests at the same time
    resps = grequests.map( rs )

    # Cache the responses
    for req_tuple, resp in zip( req_list, resps ):
        # Indicate the type to prevent "Any" propagation
        typed_resp = cast( requests.Response, resp )

        term = req_tuple[ 0 ]
        dept = req_tuple[ 1 ]

        json_object = json.loads( typed_resp.text )
        if json_object[ "status" ] != "success":
            # The department wasn't found for this term - deal with later
            continue

        # Store the data for that department and term
        class_api.cache_data( dept, term, json_object )

def bulk_populate_roster_data( req_entries: List[ ReqEntry ] ) -> None:
    """Populates the class data for all the classes in the Rosters"""

    term_dept_tuples: Set[ Tuple[ str, str ] ] = set()

    for entry in req_entries:
        term = entry.term
        dept = get_dept_from_name( entry.course_used )

        term_dept_tuples.add( (term, dept) )

    bulk_populate_data( list( term_dept_tuples ) )