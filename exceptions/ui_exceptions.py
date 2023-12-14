"""
#=====================================================================
# ui_exceptions.py
#=====================================================================
# Exceptions that our user interface functions may need to throw
#
# Author: Aidan McNay
# Date: October 11th, 2023
"""

class InvalidClassNameError( Exception ):
    """
    Indicates that the provided class name isn't a valid class name

    Attributes:
     - term: Term that isn't valid (str)
    """

    def __init__( self, class_name: str ):
        self.class_name = class_name

        err_msg = f"{class_name} is not a valid class name"
        super().__init__( err_msg )

class InvalidTermError( Exception ):
    """
    Indicates that the provided term isn't a valid term

    Attributes:
     - term: Term that isn't valid (str)
    """

    def __init__( self, term: str ):
        self.term = term

        err_msg = f"{term} is not a valid term"
        super().__init__( err_msg )

class InvalidGradeError( Exception ):
    """
    Indicates that the provided grade isn't a valid grade

    Attributes:
     - grade: Grade that isn't valid (str)
    """

    def __init__( self, grade: str ):
        self.term = grade

        err_msg = f"{grade} is not a valid grade"
        super().__init__( err_msg )
