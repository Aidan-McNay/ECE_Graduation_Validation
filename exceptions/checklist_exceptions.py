"""
#=====================================================================
# checklist_exceptions.py
#=====================================================================
# Exceptions that our checklist parser may need to throw
#
# Author: Aidan McNay
# Date: November 10th, 2023
"""

import os

class UnsupportedFileTypeError( Exception ):
    """
    Indicates that we don't support a checklist file of the given type

    Attributes:
     - file: File type that the user attempted to access
    """

    def __init__( self, file: str ):
        self.file = os.path.basename( file )

        err_msg = f"{self.file} isn't a supported checklist file format. "
        err_msg += "Please use a file ending in .xlsx or .csv"
        super().__init__( err_msg )

class MultipleAttributeError( Exception ):
    """
    Indicates that we found multiple locations for a given attribute

    Attributes:
     - attr: Attribute that occurs multiple times
    """

    def __init__( self, attr: str ):
        self.attr = attr

        err_msg = f"The attributs {self.attr} is found multiple times in your checklist. "
        err_msg += "Please ensure that this text only occurs once"
        super().__init__( err_msg )
