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

import obj
import checks
from ui.logger import printl

#---------------------------------------------------------------------
# Argument Parsing
#---------------------------------------------------------------------

parser = argparse.ArgumentParser( description =
                                  "Validates an ECE student's checklist for graduation" )

# Mandatory arguments
parser.add_argument( "checklists", help = "The checklist(s) to validate",
                     metavar = "<checklists>", action = "append" )

# Optional arguments
parser.add_argument( "-g", "--grades",
                     help = "Verify the checklist against the given grades/credits",
                     action = "append",
                     metavar = "<grades-csv>" )

parser.add_argument( "-v", "--verbose", action="store_true",
                     help = "Provide verbose output" )

#---------------------------------------------------------------------
# Logging
#---------------------------------------------------------------------

def makelogdir() -> str:
    """
    Creates a logs directory if one doesn't exist, returning the
    logging directory
    """

    cwd = os.getcwd()
    logging_dir = os.path.join( cwd, "logs" )
    os.makedirs( logging_dir, exist_ok = True )
    return logging_dir

#---------------------------------------------------------------------
# Main Code
#---------------------------------------------------------------------

# Name and function of checks to run
#  - functions should take in 2 arguments; the roster to operate on,
#    and where to store the logs. The output should be the number of
#    errors encountered
checks_to_run: dict = {}

# Errors for each check run
errors: dict = {}

if __name__ == "__main__":
    args = parser.parse_args()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Obtain the rosters from the checklists
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    rosters = []

    for checklist_path in args.checklists:
        checklist = obj.checklist_obj.Checklist( checklist_path )
        roster = obj.roster_obj.Roster( checklist.netid )
        roster.populate_entries( checklist.req_entries, checklist.checkoff_entries )

        rosters.append( roster )

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
                                                                                     y,
                                                                                     args.verbose )

        checks_to_run[ "credits-validation" ] = lambda x, y : checks.credits_check.credits_check( x,
                                                                                     grades,
                                                                                     y,
                                                                                     args.verbose )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Run Checks
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if len( checks_to_run ) > 0:
        log_dir = makelogdir()

        for check_name, check_func in checks_to_run.items():
            errors[ check_name ] = {}
            result_dir = os.path.join( log_dir, check_name )
            os.makedirs( result_dir, exist_ok = True )

            for roster in rosters:
                netid = roster.netid
                log_file = os.path.join( result_dir, f"{netid}.log" )

                print( f"Running {check_name} for {netid}..." )
                errors[ check_name ][ netid ] = check_func( roster, log_file )

            print( f" - Log in { os.path.relpath( log_file ) }\n")

        summary_file = os.path.join( log_dir, "summary.log" )
        with open( summary_file, 'w', encoding = "utf-8" ) as file:

            printl( "Summary:", file )

            for check_name, error_logs in errors.items():
                total_errors = sum( error_logs.values() )
                printl( f" - {check_name}: {total_errors} errors", file )

                for netid, num_errors in error_logs.items():
                    printl( f"    - {netid}: {num_errors} errors", file )
