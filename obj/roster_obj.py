"""
#=====================================================================
# roster_obj.py
#=====================================================================
# An object representation of a student's roster (all the classes on
# their checklist)
#
# Author: Aidan McNay
# Date: December 3rd, 2023
"""

from typing import List, Union

from obj.checklist_obj import Checklist
from obj.coordinates_obj import Coordinates
from obj.roster_entry_obj import ReqEntry, CheckoffEntry

#---------------------------------------------------------------------
# Define Validity Levels
#---------------------------------------------------------------------

ERROR = 10
WARNING = 5
VALID = 0

#---------------------------------------------------------------------
# Roster Object
#---------------------------------------------------------------------

class Roster():
    """
    A Python representation of a student's roster; the classes they
    have taken, according to their checklist

    Attributes:

     - filepath: The filepath that the data was sourced from (str)

     - netid: The student's NetID (str)

     - req_entries_validity: A dict mapping a student's ReqEntrys to their validity
                             (dict mapping ReqEntrys to ints)

     - checkoff_entries_validity: A dict mapping a student's CheckoffEntrys to their validity
                                  (dict mapping CheckoffEntrys to ints)

    Properties: (Dynamically derived)

     - req_entries: A list of a student's ReqEntrys (list of ReqEntrys)

     - checkoff_entries: A list of a student's CheckoffEntrys (list of CheckoffEntrys)

    We begin by assuming all requirements are valid, and that checks will modify their entries 
    if not. Validity can take different degrees, with their corresponding integer values defined 
    above:

     - ERROR: A significant error occurred when interpreting this entry
     - WARNING: The entry may or may not be correct; we cannot say for sure
     - VALID: The entry is valid, and no errors have been found with it

    Validity values are defined to monotonically increase (VALID -> ERROR)
    """

    def __init__( self, checklist: Checklist ):
        self.filepath                  = checklist.filepath
        self.netid                     = checklist.netid
        self.req_entries_validity      = { x : VALID for x in checklist.req_entries }
        self.checkoff_entries_validity = { x : VALID for x in checklist.checkoff_entries }

    @property
    def req_entries( self ) -> List[ReqEntry]:
        """Returns a list of the student's ReqEntrys"""

        return list( self.req_entries_validity.keys() )

    @property
    def checkoff_entries( self ) -> List[CheckoffEntry]:
        """Returns a list of the student's CheckoffEntrys"""

        return list( self.checkoff_entries_validity.keys() )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Modify Validity
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def escalate_validity( self, entry: Union[ReqEntry, CheckoffEntry],
                           validity_level: int ) -> None:
        """Escalates the validity level for the given entry"""

        if isinstance( entry, ReqEntry ):
            if self.req_entries_validity[ entry ] < validity_level:
                self.req_entries_validity[ entry ] = validity_level

        else:
            if self.checkoff_entries_validity[ entry ] < validity_level:
                self.checkoff_entries_validity[ entry ] = validity_level

    def warn( self, entry: Union[ReqEntry, CheckoffEntry] ) -> None:
        """Indicates a warning for the given entry"""

        self.escalate_validity( entry, WARNING )

    def error( self, entry: Union[ReqEntry, CheckoffEntry] ) -> None:
        """Indicates an error for the given entry"""

        self.escalate_validity( entry, ERROR )

    def get_validity( self, coord: Coordinates ) -> int:
        """Gets the validity based off of the coordinate of the entry"""

        for req_entry in self.req_entries:
            if coord == req_entry.coord:
                return self.req_entries_validity[ req_entry ]

        for checkoff_entry in self.checkoff_entries:
            if coord == checkoff_entry.coord:
                return self.checkoff_entries_validity[ checkoff_entry ]

        # Should never get here
        return -1
