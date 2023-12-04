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

from obj.roster_entry_obj import RosterEntry
from obj.class_obj import Class

class Roster():
    """
    A Python representation of a student's roster; the classes they
    have taken, according to their checklist

    Attributes:

     - netid: The student's NetID (str)

     - entries: A list of RosterEntrys (list of RosterEntrys or None)

     - classes: A list of the classes that the student has taken
                (list of Classes or None)

    Note: entries and classes may or may not be populated, and are
    initialized to None
    """

    def __init__( self, netid: str ):
        self.netid   = netid
        self.entries: List[RosterEntry] = []
        self.classes: List[Class]       = []

    def populate_entries( self, entries: List[RosterEntry] ) -> None:
        """
        Populates the checklist entries from a given list of 
        RosterEntrys
        """
        self.entries = entries
