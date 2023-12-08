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

import obj
import checks
from ui.logger import logger, gen_file_logger, gen_v_file_logger, set_verbosity, SUCCESS

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
parser.add_argument( "-l", default = "logs", help = "Set the location of the logs directory",
                     metavar = "LOGS_DIR", dest = "logs" )

parser.add_argument( "-g", "--grades",
                     help = "Verify the checklist against the given grades/credits",
                     action = "append",
                     metavar = "GRADES-CSV" )

parser.add_argument( "-v", "--verbose", action="store_true",
                     help = "Provide verbose output" )

#---------------------------------------------------------------------
# Logging
#---------------------------------------------------------------------

LOG_DIR = "logs"

def setlogdir( directory: str ) -> None:
    """Sets the logging dir"""

    global LOG_DIR
    if os.path.isabs( directory ):
        LOG_DIR = directory
    else:
        cwd = os.getcwd()
        LOG_DIR = os.path.join( cwd, directory )

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

# Name and function of checks to run
#  - functions should take in 2 arguments; the roster to operate on,
#    and a Logger to log information. The output should be the number
#    of errors encountered
checks_to_run: dict = {}

# Errors for each check run
errors: dict = {}

if __name__ == "__main__":
    args = parser.parse_args()
    set_verbosity( args.verbose )
    setlogdir( args.logs )
    removelogdir()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Instantiate main logger
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    log_dir = makelogdir()
    summary_file = os.path.join( log_dir, "summary.log" )
    summary_logger = gen_file_logger( summary_file )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Obtain the rosters from the checklists
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    rosters = []
    netids_found: Dict[str, str] = {}

    summary_logger.info( "Checking NetID uniqueness across checklists..." )

    for checklist_path in args.checklists:
        checklist = obj.checklist_obj.Checklist( checklist_path )
        roster = obj.roster_obj.Roster( checklist.netid )
        roster.populate_entries( checklist.req_entries, checklist.checkoff_entries )

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

        checks_to_run[ "grade-validation" ] = lambda x, y : checks.grade_check.grade_check( x,
                                                                                     grades,
                                                                                     y )

        checks_to_run[ "credits-validation" ] = lambda x, y : checks.credits_check.credits_check( x,
                                                                                     grades,
                                                                                     y )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Run Checks
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if len( checks_to_run ) > 0:
        log_dir = makelogdir()

        for check_name, check_func in checks_to_run.items():
            result_dir = os.path.join( log_dir, check_name )
            os.makedirs( result_dir, exist_ok = True )

            logger.info( "Running %s...", check_name )

            for roster in rosters:
                netid = roster.netid
                log_file = os.path.join( result_dir, f"{netid}.log" )
                check_logger = gen_v_file_logger( log_file )

                if netid not in errors:
                    errors[ netid ] = {}

                errors[ netid ][ check_name ] = check_func( roster, check_logger )

        summary_logger.info( "Summary:" )

        TOTAL_ERRORS = 0

        for netid, error_logs in errors.items():
            netid_errors = sum( error_logs.values() )
            TOTAL_ERRORS += netid_errors
            summary_logger.info( " - %s: %d errors", netid, netid_errors )

            for check_name, check_errors in error_logs.items():
                summary_logger.info( "    - %s: %d errors", check_name, check_errors )

        if TOTAL_ERRORS > 0:
            summary_logger.error( "Overall: %d errors", TOTAL_ERRORS )
        else:
            summary_logger.log( SUCCESS, "All checks passed!" )

    summary_logger.info( "Run logs in the %s directory", args.logs )
