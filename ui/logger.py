"""
#=====================================================================
# logger.py
#=====================================================================
# Utility functions for logging
#
# Author: Aidan McNay
# Date: December 3rd, 2023
"""

from io import TextIOWrapper

def printl( string_to_log: str, file: TextIOWrapper, verbose: bool = True ):
    """
    Logs a given statement to the file

    We also print the statement if we're verbose
    """

    if verbose:
        print( string_to_log )
    file.write( string_to_log + "\n" )
