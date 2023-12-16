"""
#=====================================================================
# basic_check.py
#=====================================================================
# A simple check that a requirement was satisfied by a given class,
# intended for re-use across many checks
#
# Author: Aidan McNay
# Date: December 14th, 2023
"""

from logging import Logger
from typing import Tuple, List

from obj.roster_obj import Roster
from obj.roster_entry_obj import ReqEntry
from obj.class_obj import Class

import exceptions as excp

def basic_check( roster: Roster, logger: Logger, req: str, valid_prefixes: List[str],
                 req_num_expected: int = 1 ) -> Tuple[int, int, ReqEntry]:
    """
    Checks that the student satisfies a requirement with a valid class.

    Specifically, we verify that:
     - The requirement only appears once
     - The course was actually offered during the reported term
     - The entry notes a course that begins with one of the given prefixes (often the course name)
     - All of the credits for the course were applied towards the requirement

    The function returns the number of errors and warnings encountered (respectively), as well as 
    the first entry found for the given requirement (useful for some checks expecting only one 
    entry, and which take action based on it). Finally, you can optionally specify if you expect 
    more than one requirement to be found
    """
    errors   = 0
    warnings = 0

    entry_list = roster.get_req( req )
    if len( entry_list ) != req_num_expected:
        logger.error( "Expected %d entry for the %s requirement, found %d",
                      req_num_expected, req, len( entry_list ) )
        for entry in entry_list:
            entry.error( "req" )
        errors += 1

    entry_to_return = entry_list[0]

    for entry in entry_list:

        # Check that a course was supplied
        if entry.course_used == "":
            logger.error( "No course indicated for %s requirement", req )
            errors += 1
            entry.error( "req" )
            entry.error( "course" )
            entry.error( "term" )
            continue

        entry.valid( "course" )

        # Check that it was offered during the reported term
        try:
            class_obj = Class( entry.course_used, entry.term )
            entry.valid( "term" )
        except excp.api_exceptions.TermNotFoundError:
            logger.warning( "No data for the term %s, so can't check %s",
                            entry.term, entry.course_used )
            warnings += 1
            entry.warn( "term" )
            entry.warn( "req" )
            continue
        except ( excp.api_exceptions.DeptNotFoundError, excp.api_exceptions.ClassNotFoundError ):
            logger.error( "%s wasn't offered during %s", entry.course_used, entry.term )
            errors += 1
            entry.error( "term" )
            entry.error( "req" )
            continue

        # Check that a valid class was supplied
        class_is_valid = False

        for prefix in valid_prefixes:
            if any( name.startswith( prefix ) for name in class_obj.all_names ):
                class_is_valid = True

        if not class_is_valid:
            logger.error( "%s requirement is not satisfied by %s", req, entry.course_used )
            errors += 1
            entry.error( "req" )
            continue

        # Finally, verify that the reporting was for the full number of credits
        if class_obj.max_credits != entry.cred_applied:
            logger.error( "Reported taking %s for different credits (%d) than the full " +
                          "number of credits (%d) for the %s requirement", 
                          entry.course_used, entry.cred_applied, class_obj.max_credits, req )
            errors += 1
            entry.error( "req" )
        else:
            logger.info( "%s requirement fully satisfied by %s", req, entry.course_used )
            entry.valid( "req" )

    return errors, warnings, entry_to_return
