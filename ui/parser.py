#=====================================================================
# parser.py
#=====================================================================
# A tool for parsing various kinds of user input
#
# Author: Aidan McNay
# Date: October 2nd, 2023

def parse_class_name( ugly_name ):
    """
    Parses non-optimal user input into a usable class name for making
    API requests.

    Ex. " ecE2720" -> "ECE 2720"
    """
    stripped_name = ugly_name.strip()

    letters = [ x for x in stripped_name if x.isalpha() ]
    digits  = [ x for x in stripped_name if x.isdigit() ]

    return ( "".join(letters) ).upper() + " " + "".join(digits)

def parse_class_term( ugly_term ):
    """
    Parses non-optimal user input into a usable term ID

    Ex. " fA '2 2" -> "FA22"
    """
    stripped_term = ugly_term.strip()

    letters = [x for x in stripped_term if x.isalpha() ]
    digits  = [x for x in stripped_term if x.isdigit() ]

    return ( "".join(letters) ).upper() + "".join(digits)

def validate_class_term( term ):
    """
    Validates that the given string represents an actual term, and
    returns the corresponding boolean

    AB42 -> False
    FA23 -> True

    Note: terms in the future are considered valid
    """
    
    result = len( term ) == 4
    result = result and ( ( term[2:4] ).isdigit() )
    result = result and ( term[0:2] in [ "SP", "SU", "FA", "WI" ] )
    return result