"""
#=====================================================================
# parser.py
#=====================================================================
# A tool for parsing various kinds of user input
#
# Author: Aidan McNay
# Date: October 2nd, 2023
"""

import exceptions as excp

#---------------------------------------------------------------------
# Parsing for Class Names
#---------------------------------------------------------------------

def parse_class_name( ugly_name: str ) -> str:
    """
    Parses non-optimal user input into a usable class name for making
    API requests.

    Ex. " ecE2720" -> "ECE 2720"
    """
    stripped_name = ugly_name.strip()

    letters = [ x for x in stripped_name if x.isalpha() ]
    digits  = [ x for x in stripped_name if x.isdigit() ]

    return ( "".join(letters) ).upper() + " " + "".join(digits)

def get_dept_from_name( class_name: str ) -> str:
    """
    Gets the department name from a class name

    Assumes that class_name is in the correct format
    """
    return class_name.split( " " )[0]

def get_nbr_from_name( class_name: str ) -> str:
    """
    Gets the class number from a class name

    Assumes that class_name is in the correct format
    """
    return class_name.split( " " )[1]

#---------------------------------------------------------------------
# Parsing for Class Terms
#---------------------------------------------------------------------

def parse_class_term( ugly_term: str ) -> str:
    """
    Parses non-optimal user input into a usable term ID

    Ex. " fA '2 2" -> "FA22"
    """
    stripped_term = ugly_term.strip()

    letters = [ x for x in stripped_term if x.isalpha() ]
    digits  = [ x for x in stripped_term if x.isdigit() ]

    term = ( "".join(letters) ).upper() + "".join(digits)

    if not validate_class_term( term ): # Still not a valid term
        raise excp.ui_exceptions.InvalidTermError( ugly_term )

    return term

def validate_class_term( term: str ) -> bool:
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

def term_index( term: str ) -> float:
    """
    Returns a value for each term such that chronologically later
    terms will have higher values than terms that come before

    Assumes that the term passed in is formatted properly
    """

    if not validate_class_term( term ):
        raise excp.ui_exceptions.InvalidTermError( term )

    term_season =   "".join( [ x for x in term if x.isalpha() ] )
    term_year = int("".join( [ x for x in term if x.isdigit() ] ) )

    seasons = {
        "WI": 0,
        "SP": 0.25,
        "SU": 0.5,
        "FA": 0.75
    }

    return term_year + seasons[term_season]

def term_is_later( term1: str, term2: str ) -> bool:
    """
    Returns a bool representing whether the first term occurs
    later than the second term

    Assumes that the terms passed in are formatted properly
    """

    return term_index( term1 ) > term_index( term2 )

#---------------------------------------------------------------------
# Parsing for Grades
#---------------------------------------------------------------------

def parse_grade( ugly_grade: str ) -> str:
    """
    Parses non-optimal user input into a usable grade

    Ex. " + a" -> "A+
    """

    stripped_grade = ugly_grade.strip()

    letters = [ x for x in stripped_grade if x.isalpha() ]
    mods    = [ x for x in stripped_grade if x in ( "+", "-" ) ]

    grade = ( "".join(letters) ).upper() + "".join(mods)

    if not validate_grade( grade ): # Still not a valid grade
        raise excp.ui_exceptions.InvalidTermError( ugly_grade )

    return grade

VALID_GRADES = {
    "A+",
    "A",
    "A-",
    "B+",
    "B",
    "B-",
    "C+",
    "C",
    "C-",
    "D+",
    "D",
    "D-",
    "F",
    "S",
    "U",
    "SX",
    "UX"
}

def validate_grade( grade: str ) -> bool:
    """
    Validates that a given string corresponds to an actual grade;
    returns True if yes, False if no
    """

    return grade in VALID_GRADES
