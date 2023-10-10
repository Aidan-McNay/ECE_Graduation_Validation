#=====================================================================
# parser.py
#=====================================================================
# A tool for parsing various kinds of user input
#
# Author: Aidan McNay
# Date: October 2nd, 2023

import ui

#---------------------------------------------------------------------
# Parsing for Class Names
#---------------------------------------------------------------------

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

def get_dept_from_name( class_name ):
    """
    Gets the department name from a class name

    Assumes that class_name is in the correct format
    """
    return class_name.split( " " )[0]

def get_nbr_from_name( class_name ):
    """
    Gets the class number from a class name

    Assumes that class_name is in the correct format
    """
    return class_name.split( " " )[1]

#---------------------------------------------------------------------
# Parsing for Class Terms
#---------------------------------------------------------------------

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

def term_index( term ):
  """
  Returns a value for each term such that chronologically later
  terms will have higher values than terms that come before

  Assumes that the term passed in is formatted properly
  """

  if not validate_class_term( term ):
      raise ui.ui_exceptions.InvalidTermError( term )

  term_season =   "".join( [ x for x in term if x.isalpha() ] )
  term_year = int("".join( [ x for x in term if x.isdigit() ] ) )

  seasons = {
    "WI": 0,
    "SP": 0.25,
    "SU": 0.5,
    "FA": 0.75
  }

  return ( term_year + seasons[term_season] )

def term_is_later( term1, term2 ):
    """
    Returns a bool representing whether the first term occurs
    later than the second term

    Assumes that the terms passed in are formatted properly
    """

    return( term_index( term1 ) > term_index( term2 ) )