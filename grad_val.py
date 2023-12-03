#!/usr/bin/env python3

#=====================================================================
# grad_val.py
#=====================================================================
# The main code for validating checklists
#
# Author: Aidan McNay
# Date: December 3rd, 2023

import argparse, os
import obj, checks

#---------------------------------------------------------------------
# Argument Parsing
#---------------------------------------------------------------------

parser = argparse.ArgumentParser( description = "Validates an ECE student's checklist for graduation" )

# Mandatory arguments
parser.add_argument( "checklist", help = "The checklist to validate", metavar = "<checklist>" )

# Optional arguments
parser.add_argument( "-g", "--grades", 
                     help = "Verify the checklist against the given grades",
                     action = "append",
                     metavar = "<grades-csv>" )

parser.add_argument( "-v", "--verbose", action="store_true",
                     help = "Provide verbose output" )

#---------------------------------------------------------------------
# Logging
#---------------------------------------------------------------------

def makelogdir():
    """
    Creates a logs directory if one doesn't exist, returning the
    logging directory
    """

    cwd = os.getcwd()
    log_dir = os.path.join( cwd, "logs" )
    os.makedirs( log_dir, exist_ok = True )
    return log_dir

#---------------------------------------------------------------------
# Main Code
#---------------------------------------------------------------------

# Name and function of checks to run
#  - functions should take in 2 arguments; the roster to operate on,
#    and where to store the logs. The output should be the number of
#    errors encountered
checks_to_run = {}

# Errors for each check run
errors = {}

if __name__ == "__main__":
    args = parser.parse_args()
    print( args )

    # Obtain the checklist
    checklist = obj.checklist_obj.Checklist( args.checklist )

    # Populate the roster based on the checklist
    roster = obj.roster_obj.Roster( checklist.netid )
    roster.populate_entries( checklist.entries )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Grade Validation
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if( args.grades ):
        # Form grades
        grades = obj.grades_obj.Grades()

        for grade_file in args.grades:
            grades += obj.grades_obj.Grades( grade_file )

        checks_to_run[ "grade-validation" ] = lambda x, y : checks.grade_check.grade_check( x, 
                                                                                     grades,
                                                                                     y,
                                                                                     args.verbose )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Run Checks
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if( len( checks_to_run ) > 0 ):
        log_dir = makelogdir()

        for check_name, check_func in checks_to_run.items():
            print( f"Running {check_name}..." )
            result_dir = os.path.join( log_dir, check_name )
            os.makedirs( result_dir, exist_ok = True )
            log_file = os.path.join( result_dir, f"{roster.netid}.log" )

            errors[ check_name ] = check_func( roster, log_file )

            print( f" - Log in { os.path.relpath( log_file ) }\n")
        
        print( "Summary:" )

        for check_name, error_count in errors.items():
            print( f"{check_name}: {error_count} errors" )
