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

from typing import Set, Optional
from obj.coordinates_obj import Coordinates

#---------------------------------------------------------------------
# Requirement/Checkoff Types
#---------------------------------------------------------------------

req_types: Set[str] = {
    "REQ-MATH 1910",
    "REQ-MATH 1920",
    "REQ-MATH 2930",
    "REQ-MATH 2940",
    "REQ-CS 1110/1112",
    "REQ-CHEM 2090",
    "REQ-PHYS 1112/1116",
    "REQ-PHYS 1110",
    "REQ-PHYS 2213/2217",
    "REQ-PHYS 2214/2218",
    "REQ-ECE 2300",
    "REQ-PE",
    "REQ-ECE 2100",
    "REQ-ECE 2720",
    "REQ-ECE 3030",
    "REQ-ECE 3100",
    "REQ-ECE 3140",
    "REQ-ECE 3150",
    "REQ-ECE 3250",
    "REQ-CDE",
    "REQ-4000+",
    "REQ-3000+",
    "REQ-FWS",
    "REQ-LS",
    "REQ-OTE",
    "REQ-AAE",
    "REQ-ENGRD",
    "REQ-ENGRI",
    "REQ-EXTRA",
}

checkoff_types: Set[str] = {
    "CKOFF-ADVPROG",
    "CKOFF-TECHWRIT"
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

    This is to be used for both requirement and checkoff entries           
    """

    def __init__( self, req: str, course: str, coord: Coordinates ):
        self.req          = req
        self.course_used  = course
        self.coord        = coord

        assert ( ( self.req.upper() in req_types ) or (self.req.upper() in checkoff_types ) ), \
               f"Error: Listed requirement {self.req} not recognized"

    def __str__( self ) -> str:
        """
        String representation (for debugging)
        """
        return f"{self.req} satisfied by {self.course_used}"

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

     - cred_applied: Credits applied to satisfy the requirement (int or None)

     - term: Term that the class was taken (str or None)

     - grade: Grade reported for the class (str or None)

     - cat: Category for liberal study; if the entry isn't "REQ-LS", this 
            should be set to None (str or None)

    Note that the primary attributes are meant for requirements; checkoffs will
    have only `req` and `course_used`, with the rest set to None
           
    """

    def __init__( self, req: str, course: str, coord: Coordinates, cred: int, term: str, grade: str,
                  cat: Optional[str] = None ):

        super().__init__( req, course, coord )
        self.cred_applied = cred
        self.term         = term
        self.grade        = grade
        self.cat          = cat

        assert ( self.req.upper() in req_types ), \
               f"Error: Listed requirement {self.req} not recognized"

    def __str__( self ) -> str:
        """
        String representation (for debugging)
        """
        return f"{self.req} satisfied by {self.course_used} ({self.term})"

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
    """

    def __init__( self, req: str, course: str, coord: Coordinates ):

        super().__init__( req, course, coord )

        assert ( self.req.upper() in checkoff_types ), \
               f"Error: Listed requirement {self.req} not recognized"

    def __str__( self ) -> str:
        """
        String representation (for debugging)
        """
        return f"{self.req} satisfied by {self.course_used}"
