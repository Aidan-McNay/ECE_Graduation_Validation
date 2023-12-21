#!/usr/bin/env python3
"""
#=====================================================================
# grad_val.py
#=====================================================================
# The main code for validating checklists

# Author: Aidan McNay
# Date: December 3rd, 2023
"""

import argparse
import os
from typing import NoReturn, Dict
import shutil
import sys

from api.bulk_api import bulk_populate_roster_data
import obj
import checks
from ui.logger import gen_file_logger, set_verbosity, SUCCESS
from ui.annotate import make_annotated_checklist

from checks.common_core.common_core_check import common_core_check
from checks.ece_core.ece_core_check       import ece_core_check
from checks.ece_found.ece_found_check     import ece_found_check

#---------------------------------------------------------------------
# Argument Parsing
#---------------------------------------------------------------------

# Define custom parser to print help message on an error
class DefaultHelpParser( argparse.ArgumentParser ):
    """
    A thin wrapper around argparse.ArgumentParser to print the help message
    on an error
    """

    def error( self, message: str ) -> NoReturn:
        """Displays the error and help message on an error"""
        sys.stderr.write( f'error: {message}\n' )
        self.print_help()
        sys.exit( 2 )

parser = DefaultHelpParser( description = "Validates an ECE student's checklist for graduation",
                            usage = "%(prog)s CHECKLIST(S)" )

# Mandatory arguments
parser.add_argument( "checklists", help = "The checklist(s) to validate",
                     metavar = "CHECKLIST(S)", action = "append" )

# Optional arguments
parser.add_argument( "-g", "--grades",
                     help = "Verify the checklist against the given grades/credits",
                     action = "append",
                     metavar = "GRADES-CSV" )

parser.add_argument( "-l", default = "logs", help = "Set the location of the logs directory",
                     metavar = "LOGS_DIR", dest = "logs" )

parser.add_argument( "-s", action="store_true", dest="semantics",
                     help = "Run semantics checks (the requirement is satisfied by the class)" )

parser.add_argument( "-v", "--verbose", action="store_true",
                     help = "Provide verbose output" )

#---------------------------------------------------------------------
# Logging
#---------------------------------------------------------------------

def get_abs_path( path: str ) -> str:
    """Makes a file path absolute, if it isn't already"""
    if os.path.isabs( path ):
        return path
    # Otherwise, need to add to current working directory
    cwd = os.getcwd()
    return os.path.join( cwd, path )

LOG_DIR = "logs"

def setlogdir( directory: str ) -> None:
    """Sets the logging dir"""

    global LOG_DIR
    LOG_DIR = get_abs_path( directory )

def makelogdir() -> str:
    """
    Creates a logs directory if one doesn't exist, returning the
    logging directory
    """

    os.makedirs( LOG_DIR, exist_ok = True )
    return LOG_DIR

def removelogdir() -> None:
    """Removes the logging directory, if it's there"""

    if os.path.exists( LOG_DIR ) and os.path.isdir( LOG_DIR ):
        shutil.rmtree( LOG_DIR )

#---------------------------------------------------------------------
# Main Code
#---------------------------------------------------------------------

# Errors for each check run
errors: dict = {}

if __name__ == "__main__":
    args = parser.parse_args()
    set_verbosity( args.verbose )
    setlogdir( args.logs )
    removelogdir()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Instantiate main logger and CheckManager
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    log_dir = makelogdir()
    summary_file = os.path.join( log_dir, "summary.log" )
    summary_logger = gen_file_logger( summary_file )

    checks_mngr = checks.checks_manager.ChecksManager()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Obtain the rosters from the checklists
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    rosters = []
    netids_found: Dict[str, str] = {}

    summary_logger.info( "Checking NetID uniqueness across checklists..." )

    for checklist_path in args.checklists:
        # Use the absolute path, for clarity
        checklist = obj.checklist_obj.Checklist( get_abs_path( checklist_path ) )
        roster = obj.roster_obj.Roster( checklist )

        rosters.append( roster )

        if roster.netid in netids_found:
            summary_logger.error( "NetID %s (in %s) is a duplicate (previously found in %s)",
                                  roster.netid, os.path.relpath( checklist_path ),
                                                os.path.relpath( netids_found[ roster.netid ] ) )
            sys.exit( 1 )

        else:
            netids_found[ roster.netid ] = checklist_path

    summary_logger.log( SUCCESS, "No duplicate NetIDs detected" )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Grade/Credits Validation
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if args.grades :
        # Form grades
        grades = obj.grades_obj.Grades()

        for grade_file in args.grades:
            grades += obj.grades_obj.Grades( grade_file )

        checks_mngr.add_check( "grade-validation",
                               lambda x, y : checks.grade_check.grade_check( x, grades, y ) )

        checks_mngr.add_check( "credits-validation",
                               lambda x, y : checks.credits_check.credits_check( x, grades, y ) )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Populate API Information
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if args.semantics:

        summary_logger.info( "Adding class data from API..." )

        for roster in rosters:
            bulk_populate_roster_data( roster.req_entries )

        # Add semantics checks

        checks_mngr.add_check( "common-core", common_core_check )
        checks_mngr.add_check( "ece-core",    ece_core_check    )
        checks_mngr.add_check( "ece-found",   ece_found_check    )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Run Checks
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    checks_mngr.run_checks( rosters, log_dir, summary_logger )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Summary
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    checks_mngr.summary( summary_logger )
    summary_logger.info( "Run logs in the %s directory", args.logs )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Output Annotated Checklists
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    annotated_checklists_dir = os.path.join( log_dir, "annotated-checklists" )
    os.makedirs( annotated_checklists_dir, exist_ok = True )

    for roster in rosters:
        make_annotated_checklist( roster, annotated_checklists_dir )
