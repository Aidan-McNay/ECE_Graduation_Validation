"""
#=====================================================================
# logger.py
#=====================================================================
# Utility functions for logging
#
# Author: Aidan McNay
# Date: December 3rd, 2023
"""

import logging
import os
import sys

from io import TextIOWrapper

#---------------------------------------------------------------------
# Define Formatters
#---------------------------------------------------------------------

file_formatter  = logging.Formatter( fmt = "%(asctime)s [%(levelname)s] %(message)s" )
print_formatter = logging.Formatter( fmt = "[%(levelname)s] %(message)s" )

#---------------------------------------------------------------------
# Verbosity Filter
#---------------------------------------------------------------------
# Filter out messages when not verbose

class VerboseFilter( logging.Filter ):
    """
    A filter to determine when we want to output messages that
    depend on verbosity

    Attributes:

     - verbose: Whether we're verbose or not (bool)
    """

    def __init__( self ) -> None:
        logging.Filter.__init__( self )
        self.verbose = True # Set default verbosity, to be overwritten

    def set_verbosity( self, verbose: bool ) -> None:
        """Set whether we're verbose"""
        self.verbose = verbose

    def filter( self, record: logging.LogRecord ) -> bool:
        """Determines whether we should output a message, given the verbosity"""
        if record.levelno >= logging.CRITICAL:
            return True # Should output

        return self.verbose # Output when we're verbose

verbose_filter = VerboseFilter()

def set_verbosity( verbose: bool ) -> None:
    """Sets the verbosity for the verbosity filter"""
    verbose_filter.set_verbosity( verbose )

#---------------------------------------------------------------------
# Define Handlers
#---------------------------------------------------------------------
# These determine how we handle logging events
#
# Additionally, we want the capability to dynamically create handlers
# for different file logging

always_print = logging.StreamHandler( stream = sys.stdout )
always_print.setFormatter( print_formatter )

verbose_print = logging.StreamHandler( stream = sys.stdout )
verbose_print.setFormatter( print_formatter )
verbose_print.addFilter( verbose_filter )

def get_file_handler( file_path: str ) -> logging.FileHandler:
    """Gets a handler to log to the specific file"""
    handler = logging.FileHandler( file_path )
    handler.setFormatter( file_formatter )
    return handler

#---------------------------------------------------------------------
# Define Loggers
#---------------------------------------------------------------------
# These handle the logging of different events
#
# Additionally, we want the capability to dynamically create loggers
# for different file logging
#
# NOTE: We do not use logging.basicConfig, to avoid using the
# lastResort handler (default) when we don't want to print anything

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# logger
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# A logger to always print

logger = logging.getLogger( "always_log" )
logger.addHandler( always_print )

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# vlogger
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# A logger to print based on verbosity

vlogger = logging.getLogger( "verbose_logger" )
logger.addHandler( verbose_print )

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# gen_file_logger
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Create a logger to log to a specific file, as well as print based
# on verbosity

def gen_v_file_logger( file_path: str ) -> logging.Logger:
    """Generates a file logger with verbose printing"""
    v_file_logger = logging.getLogger( f"{os.path.basename( file_path )} logger" )
    v_file_logger.addHandler( verbose_print )
    v_file_logger.addHandler( get_file_handler( file_path ) )
    return v_file_logger


def printl( string_to_log: str, file: TextIOWrapper, verbose: bool = True ) -> None:
    """
    Logs a given statement to the file

    We also print the statement if we're verbose
    """

    if verbose:
        print( string_to_log )
    file.write( string_to_log + "\n" )
