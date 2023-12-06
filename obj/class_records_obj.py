"""
#=====================================================================
# class_records_obj.py
#=====================================================================
# Records of a student taking classes
#
# Author: Aidan McNay
# Date: December 4th, 2023
"""

from obj.grades_obj import Grades
from obj.class_record_obj import ClassRecord

from exceptions.class_records_exceptions import RecordNotFoundError

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
            raise RecordNotFoundError( self.netid, class_name, term )

        correct_record.use_cred( num_cred )
