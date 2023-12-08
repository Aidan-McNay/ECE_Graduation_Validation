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

from obj.checklist_obj import Checklist
from obj.class_obj import Class

class Roster():
    """
    A Python representation of a student's roster; the classes they
    have taken, according to their checklist

    Attributes:

     - filepath: The filepath that the data was sourced from (str)

     - netid: The student's NetID (str)

     - entries: A list of RosterEntrys (list of RosterEntrys)

     - classes: A list of the classes that the student has taken
                (list of Classes)

    Note: entries and classes may or may not be populated, and are
    initialized to None
    """

    def __init__( self, checklist: Checklist ):
        self.filepath             = checklist.filepath
        self.netid                = checklist.netid
        self.req_entries          = checklist.req_entries
        self.checkoff_entries     = checklist.checkoff_entries
        self.classes: List[Class] = []
