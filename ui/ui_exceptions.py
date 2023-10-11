#=====================================================================
# ui_exceptions.py
#=====================================================================
# Exceptions that our user interface functions may need to throw
#
# Author: Aidan McNay
# Date: October 11th, 2023

class InvalidTermError( Exception ):
    """
    Indicates that the provided term isn't a valid term

    Attributes:
     - term: Term that isn't valid (str)
    """

    def __init__( self, term ):
        self.term = term

        err_msg = f"{term} is not a valid term"
        super().__init__( err_msg )