"""
#=====================================================================
# class_records_obj.py
#=====================================================================
# A record of a student taking a class, containing their grade,
# credits taken, and credits applied towards requirements
#
# Author: Aidan McNay
# Date: December 4th, 2023
"""

from typing import Optional

from obj.grades_obj import Grades

#---------------------------------------------------------------------
# ClassRecord Object
#---------------------------------------------------------------------

class ClassRecord:
    """
    A Python implementation of a record of taking a class

    A list of these should indicate all of the classes that a student
    has taken, and can be used for keeping track of requirements

    Attributes:

     - class_name: Name of the class (str)

     - term: Term the class was taken (str)

     - cred_taken: Credits that the student took the class for (int)

     - cred_applied: Credits applied to requirements already (int)

     - grade: Grade achieved in the class (str)
    """

    def __init__( self, class_name: str, term: str, cred_taken: int, grade: str ):
        self.class_name   = class_name
        self.term         = term
        self.cred_taken   = cred_taken
        self.cred_applied = 0
        self.grade        = grade

    def use_cred( self, num_cred: int ) -> None:
        """Indicate that credits for the class have been applied"""

        if self.cred_applied + num_cred > self.cred_taken:
            assert False, "Error: Not enough credits"
        else:
            self.cred_applied += num_cred

#---------------------------------------------------------------------
# ClassRecords Object
#---------------------------------------------------------------------

class ClassRecords:
    """
    A Python implementation of many records of taking classes

    Attributes:

     - netid: The student the records are for (str)

     - records: Records of taking classes (list of ClassRecord)
    """

    def __init__( self, netid: str, grades: Grades ):
        """Gets all records for the given NetID, using their grades"""

        self.netid = netid
        self.records = grades.gen_records( netid )

    def use_cred( self, class_name: str, term: str, num_cred: int ) -> None:
        """Indicate that credits for the class have been applied"""

        # First, find the relevant record

        correct_record: ClassRecord
        record_found = False

        for record in self.records:
            if( record.class_name == class_name ) and ( record.term == term ):
                correct_record = record
                record_found = True
                break

        if not record_found: # Didn't find it
            assert False, "Error: Couldn't find correct record"

        correct_record.use_cred( num_cred )
