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

from typing import Optional, List

from obj.checklist_obj import Checklist
from obj.coordinates_obj import Coordinates
from obj.roster_entry_obj import RosterEntry, ReqEntry, CheckoffEntry

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

     - req_entries: A list of the student's ReqEntrys (list of ReqEntrys)

     - checkoff_entries: A list of the student's CheckoffEntrys (list of CheckoffEntrys)
    """

    def __init__( self, checklist: Checklist ):
        self.filepath         = checklist.filepath
        self.netid            = checklist.netid
        self.req_entries      = checklist.req_entries
        self.checkoff_entries = checklist.checkoff_entries

    def get_entry( self, coord: Coordinates ) -> Optional[ RosterEntry ]:
        """Gets the entry based off of the coordinate of the entry"""

        for req_entry in self.req_entries:
            if coord == req_entry.coord:
                return req_entry

        for checkoff_entry in self.checkoff_entries:
            if coord == checkoff_entry.coord:
                return checkoff_entry

        # Should never get here
        return None

    def get_req( self, req: str ) -> List[ReqEntry]:
        """Gets all of the requirements matching the given req string"""
        entries = []

        for entry in self.req_entries:
            if entry.req == req:
                entries.append( entry )

        return entries

    def get_checkoff( self, req: str ) -> List[CheckoffEntry]:
        """Gets all of the checkoffs matching the given req string"""
        entries = []

        for entry in self.checkoff_entries:
            if entry.req == req:
                entries.append( entry )

        return entries
