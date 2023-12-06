"""
#=====================================================================
# class_record_obj.py
#=====================================================================
# A record of a student taking a class, containing their grade,
# credits taken, and credits applied towards requirements
#
# Author: Aidan McNay
# Date: December 4th, 2023
"""

from exceptions.class_records_exceptions import InsufficientCreditsError

#---------------------------------------------------------------------
# ClassRecord Object
#---------------------------------------------------------------------

class ClassRecord:
    """
    A Python implementation of a record of taking a class

    A list of these should indicate all of the classes that a student
    has taken, and can be used for keeping track of requirements

    Attributes:

     - netid: Name of the student who took the class

     - class_name: Name of the class (str)

     - term: Term the class was taken (str)

     - cred_taken: Credits that the student took the class for (int)

     - cred_applied: Credits applied to requirements already (int)

     - grade: Grade achieved in the class (str)
    """

    def __init__( self, netid: str, class_name: str, term: str, cred_taken: int, grade: str ):
        self.netid        = netid
        self.class_name   = class_name
        self.term         = term
        self.cred_taken   = cred_taken
        self.cred_applied = 0
        self.grade        = grade

    def use_cred( self, num_cred: int ) -> None:
        """Indicate that credits for the class have been applied"""

        if self.cred_applied + num_cred > self.cred_taken:
            raise InsufficientCreditsError( self.netid, self.class_name, self.term, 
                                            num_cred, self.cred_taken, self.cred_applied )
        else:
            self.cred_applied += num_cred
