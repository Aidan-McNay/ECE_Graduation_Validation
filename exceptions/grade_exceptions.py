"""
#=====================================================================
# grade_exceptions.py
#=====================================================================
# Exceptions that our grade parser may need to throw
#
# Author: Aidan McNay
# Date: November 10th, 2023
"""

class StudentNotFoundError( Exception ):
    """
    Indicates that we don't have grade information on the given student

    Attributes:
     - netid: NetID of the student that wasn't found (str)
    """

    def __init__( self, netid ):
        self.netid = netid

        err_msg = f"Information on grades for {netid} wasn't found"
        super().__init__( err_msg )

class TermNotFoundError( Exception ):
    """
    Indicates that we don't have grade information on the given student
    for a specific term

    Attributes:
     - netid: NetID of the student that wasn't found (str)
     - term: Term that wasn't found (str)
    """

    def __init__( self, netid, term ):
        self.netid = netid
        self.term  = term

        err_msg = f"Information on grades for {netid} wasn't found for {term}"
        super().__init__( err_msg )

class ClassNotFoundError( Exception ):
    """
    Indicates that we don't have grade information on the given student
    for a specific class in a given term

    Attributes:
     - netid: NetID of the student that wasn't found (str)
     - term: Specified term (str)
     - class: Class that wasn't found (str)
    """

    def __init__( self, netid, term, class_str ):
        self.netid     = netid
        self.term      = term
        self.class_str = class_str

        err_msg = f"Information on grades for {class_str} wasn't found for {netid} in {term}"
        super().__init__( err_msg )
