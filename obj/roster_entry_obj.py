"""
#=====================================================================
# roster_entry_obj.py
#=====================================================================
# An object representation of a class entry in a ECE Graduation
# Roster
#
# This should contain all of the necessary information that, given a
# list of RosterEntrys, later code should be able to determine
# whether they match the given requirements
#
# Author: Aidan McNay
# Date: December 2nd, 2023
"""

from typing import Set, Dict

from obj.coordinates_obj import Coordinates
from ui.parser import parse_class_name as pclass, \
                      parse_class_term as pterm,  \
                      parse_grade      as pgrade
import exceptions as excp

#---------------------------------------------------------------------
# Define Validity Levels
#---------------------------------------------------------------------

ERROR     = 10
WARNING   = 5
VALID     = 0
UNCHECKED = -1

#---------------------------------------------------------------------
# Requirement/Checkoff Types
#---------------------------------------------------------------------

req_types: Set[str] = {
    "CALC.",
    "MULTI.",
    "DIFF. EQ.",
    "LIN. ALG.",
    "INTRO. PROG.",
    "GEN. CHEM.",
    "PHYS. 1",
    "EXP. PHYS.",
    "PHYS. 2",
    "PHYS. 3",
    "DIG. LOGIC",
    "PHYS. ED.",
    "CIRCUITS",
    "DATA SCIENCE",
    "ELECTROMAG.",
    "INTRO. PROB.",
    "EMBEDDED SYS.",
    "MICROELECTRONICS",
    "SIG. & SYS.",
    "CDE",
    "4000+",
    "3000+",
    "FWS",
    "LS",
    "OTE",
    "AAE",
    "ENGR. DIST.",
    "ENGR. INTEREST",
    "EXTRA-C"
}

checkoff_types: Set[str] = {
    "ADV. PROGRAMMING",
    "TECH. WRITING"
}

#---------------------------------------------------------------------
# RosterEntry Object
#---------------------------------------------------------------------

class RosterEntry:
    """
    A Python representation of an entry in a graduation roster

    Attributes:

     - req: Requirement or checkoff that the entry is satisfying (see 
            above for options) (str)
     
     - course_used: Name of the course used to satisfy the requirement
                    or checkoff (str)

     - coord: Coordinates used to indicate the requirement index (Coordinates)

     - validity: The validity of the components of the entry 
                 (dict mapping str (component names) to int (validity))

    This is to be used for both requirement and checkoff entries.
    If a course is found to be invalid, it will be stored as an empty string.
    """

    def __init__( self, req: str, course: str, coord: Coordinates ):
        self.req                     = req.upper()
        self.coord                   = coord
        self.validity: Dict[str,int] = {}

        try:
            self.course_used = pclass( course )
        except excp.ui_exceptions.InvalidClassNameError: # Not a real class name
            self.course_used = ""

        assert ( ( self.req in req_types ) or (self.req in checkoff_types ) ), \
               f"Error: Listed requirement {self.req} not recognized"

    def __str__( self ) -> str:
        """
        String representation (for debugging)
        """
        return f"({self.val_str()}) {self.req} satisfied by {self.course_used}"

    def valid( self, component: str ) -> None:
        """Indicates that the entry is valid"""
        self.validity[ component ] = max( self.validity[ component ], VALID )

    def warn( self, component: str ) -> None:
        """Indicates that the entry has a warning"""
        self.validity[ component ] = max( self.validity[ component ], WARNING )

    def error( self, component: str ) -> None:
        """Indicates that the entry has an error"""
        self.validity[ component ] = max( self.validity[ component ], ERROR )

    def val_str( self ) -> str:
        """Returns a string representing the overall validity"""

        if any( x == ERROR   for x in self.validity.values() ): # ERROR
            return "X"
        if any( x == WARNING for x in self.validity.values() ): # WARNING
            return "W"
        if any( x == VALID   for x in self.validity.values() ): # VALID
            return "V"
        return " "

    def get_val( self, component: str ) -> int:
        """Returns the validity of the given component"""
        return self.validity[ component ]

#---------------------------------------------------------------------
# ReqEntry Object
#---------------------------------------------------------------------

class ReqEntry( RosterEntry ):
    """
    A Python representation of an requirement entry in a graduation roster

    Attributes:

     - req: Requirement that the entry is satisfying (see 
            above for options) (str)
     
     - course_used: Name of the course used to satisfy the requirement
                    (str)

     - cred_applied: Credits applied to satisfy the requirement (int)

     - term: Term that the class was taken (str)

     - grade: Grade reported for the class (str)

     - cat: Category for liberal study; if the entry isn't "REQ-LS", this 
            should be set to None (str)

     - validity: The validity of the requirement (dict mapping str to int)   

    If a field is found to be invalid, it will be stored as an empty string (str)
    or -1 (int)        
    """

    def __init__( self, req: str, course: str, coord: Coordinates, cred: str, term: str, grade: str,
                  cat: str ):

        super().__init__( req, course, coord )

        try:
            self.cred_applied = int( cred )
        except ValueError:
            self.cred_applied = -1

        try:
            self.term = pterm( term )
        except excp.ui_exceptions.InvalidTermError:
            self.term = ""

        try:
            self.grade = pgrade( grade )
        except excp.ui_exceptions.InvalidGradeError:
            self.grade = ""

        self.cat          = cat

        self.validity = {
            "req"    : UNCHECKED,
            "course" : UNCHECKED,
            "cred"   : UNCHECKED,
            "term"   : UNCHECKED,
            "grade"  : UNCHECKED,
            "cat"    : UNCHECKED
        }

        assert ( self.req in req_types ), \
               f"Error: Listed requirement {self.req} not recognized"

    def __str__( self ) -> str:
        """
        String representation (for debugging)
        """
        return f"({self.val_str()}) {self.req} satisfied by {self.course_used} ({self.term})"

    def short_str( self ) -> str:
        """Short string representation"""
        return f"{self.course_used} ({self.term})"

#---------------------------------------------------------------------
# CheckoffEntry Object
#---------------------------------------------------------------------

class CheckoffEntry( RosterEntry ):
    """
    A Python representation of an checkoff entry in a graduation roster

    Attributes:

     - req: Checkoff that the entry is satisfying (see 
            above for options) (str)
     
     - course_used: Name of the course used to satisfy the checkoff
                    (str)   

     - validity: The validity of the checkoff (dict mapping str to int)  

    If a course is found to be invalid, it will be stored as an empty string.  
    """

    def __init__( self, req: str, course: str, coord: Coordinates ):

        super().__init__( req, course, coord )

        self.validity = {
            "req"    : UNCHECKED,
            "course" : UNCHECKED
        }

        assert ( self.req in checkoff_types ), \
               f"Error: Listed requirement {self.req} not recognized"

    def __str__( self ) -> str:
        """
        String representation (for debugging)
        """
        return f"({self.val_str()}) {self.req} satisfied by {self.course_used}"
