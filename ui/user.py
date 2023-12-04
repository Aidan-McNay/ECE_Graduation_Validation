"""
#=====================================================================
# user.py
#=====================================================================
# Helper functions for interacting with users
#
# Author: Aidan McNay
# Date: October 2nd, 2023
"""

from typing import List

import ui.parser

#---------------------------------------------------------------------
# General prompting functions
#---------------------------------------------------------------------

def get_idx( str_to_convert: str ) -> int:
    '''
    Attempts to convert a string into a number
    Returns -1 if not possible
    '''
    try:
        return int( str_to_convert )

    except ValueError:
        return -1

def prompt_usr( msg: str ) -> str:
    '''
    Prompts the user for input, using the given message
    '''

    print( msg )
    response = input( "Response: ")
    print( "" ) # New line for further prompting
    return response

def prompt_usr_list( msg: str, options: List[str], default_idx: int ) -> str:
    '''
    Prompts the user to pick one of the options listed.

    Users can respond with:
     - The exact option (case-insensitive)
     - The number of the option when printed
     - <RETURN> (where the default option will be selected)

    Returns: The selected option, in the format it was passed in
    
    Args:
     - msg: The message to be printed to the user when selecting (str)

     - options: List of possible options, to be printed as strings (list)

     - default_idx: Index of the default selection 
                    (int, 0 <= default_idx < len( options ) )
    '''
    options_lowercase = [ x.lower() for x in options ]

    print( msg )

    option_string = "Options: "
    option_string += "".join( [ ( "\n " + str( idx+1 ) + ". " + option )
                                for idx, option in enumerate( options ) ] )
    option_string += f"\nDefault: [{options[ default_idx ]}]"
    option_string += "\nSelection: "

    response = input( option_string )

    while(     not ( response.lower() in options_lowercase )          \
           and not ( response == "" )                                \
           and not   0 < get_idx( response ) <= len( options ) ):
        print( "\nOops - that's not an option! Try again" )
        response = input( option_string )

    print("") # New line for spacing

    # Default response
    if response == "":
        return options[ default_idx ]

    # Enumerated response
    if get_idx( response ) != -1:
        if 0 < get_idx( response ) <= len( options ):
            return options[ get_idx( response ) - 1 ]

    # Verbose response
    response_index = options_lowercase.index( response.lower() )
    return options[ response_index ]

#---------------------------------------------------------------------
# Class-Specific Prompts
#---------------------------------------------------------------------

def prompt_term( course_name: str ) -> str:
    '''
    Prompts the user for the term that should be associated with the 
    given course name

    Assumes that the course name (str) is already in the desired format
    '''

    valid_response = False

    while not valid_response:
        prompt_msg = f"Looks like {course_name} doesn't have an associated term. " + \
                      "What term did/will you take this course?"

        response = prompt_usr( prompt_msg )
        response = ui.parser.parse_class_term( response )
        valid_response = ui.parser.validate_class_term( response )

        if not valid_response:
            print( "Oops! That doesn't look like a valid term - please try again" )

    return response
