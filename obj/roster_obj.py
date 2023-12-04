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

from typing import List

from obj.roster_entry_obj import ReqEntry, CheckoffEntry
from obj.class_obj import Class

class Roster():
    """
    A Python representation of a student's roster; the classes they
    have taken, according to their checklist

    Attributes:

     - netid: The student's NetID (str)

     - entries: A list of RosterEntrys (list of RosterEntrys)

     - classes: A list of the classes that the student has taken
                (list of Classes)

    Note: entries and classes may or may not be populated, and are
    initialized to None
    """

    def __init__( self, netid: str ):
        self.netid                                 = netid
        self.req_entries:      List[ReqEntry]      = []
        self.checkoff_entries: List[CheckoffEntry] = []
        self.classes:          List[Class]         = []

    def populate_entries( self, req_entries: List[ReqEntry],
                                checkoff_entries: List[CheckoffEntry] ) -> None:
        """
        Populates the checklist entries from a given list of 
        RosterEntrys
        """
        self.req_entries      = req_entries
        self.checkoff_entries = checkoff_entries
