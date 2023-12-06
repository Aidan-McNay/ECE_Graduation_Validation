"""
#=====================================================================
# grade_exceptions.py
#=====================================================================
# Exceptions that our grade parser may need to throw
#
# Author: Aidan McNay
# Date: November 10th, 2023
"""

class RecordNotFoundError( Exception ):
    """
    Indicates that we didn't find a record of the student taking
    a given class in a given term

    Attributes:
     - netid: NetID of the student (str)
     - class_str: Class that wasn't found (str)
     - term: Term that wasn't found (term)
    """

    def __init__( self, netid: str, class_str: str, term: str ):
        self.netid     = netid
        self.class_str = class_str
        self.term      = term

        self.err_msg = f"No record found of {netid} taking {class_str} in {term}"
        super().__init__( self.err_msg )

class InsufficientCreditsError( Exception ):
    """
    Indicates that the student doesn't have enough credits left for the
    given class to apply

    Attributes:
     - netid: NetID of the student (str)
     - class_str: Class that wasn't found (str)
     - term: Term that wasn't found (term)
     - num_cred: Number of credits attempted to apply
     - num_taken: Number of credits the class was taken for
     - num_applied: Number of credits already applied
    """

    def __init__( self, netid: str, class_str: str, term: str,
                        num_cred: int, num_taken: int, num_applied: int ):
        self.netid       = netid
        self.class_str   = class_str
        self.term        = term
        self.num_cred    = num_cred
        self.num_taken   = num_taken
        self.num_applied = num_applied

        self.err_msg = f"Too many credits applied towards {class_str} in {term} for {netid} " + \
                       f"(Took the class for {num_taken}, attempted to apply {num_cred} with " + \
                       f"{num_applied} already applied)"
        super().__init__( self.err_msg )
