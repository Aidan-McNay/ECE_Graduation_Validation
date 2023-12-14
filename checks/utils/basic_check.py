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
from obj.class_obj import Class

import exceptions as excp

def basic_check( roster: Roster, logger: Logger,
                 req: str, valid_class_names: List[str] ) -> Tuple[int, int]:
    """
    Checks that the student satisfies a requirement with a valid class.

    Specifically, we verify that:
     - The requirement only appears once
     - The entry notes a course that satisfies the requirement
     - The course was actually offered during the reported term
     - All of the credits for the course were applied towards the requirement
    """
    errors   = 0
    warnings = 0

    entry_list = roster.get_req( req )
    if len( entry_list ) != 1:
        logger.error( "Expected 1 entry for the %s requirement, found %d", req, len( entry_list ) )
        for entry in entry_list:
            entry.error( "req" )
        errors += 1

    for entry in entry_list: # Should be just one

        # Check that a course was supplied
        if entry.course_used == "":
            logger.error( "No course indicated for %s requirement", req )
            errors += 1
            entry.error( "req" )
            entry.error( "course" )
            entry.error( "term" )
            continue

        entry.valid( "course" )

        # Check that a valid class was supplied
        if entry.course_used not in valid_class_names:
            logger.error( "%s requirement is not satisfied by %s", req, entry.course_used )
            errors += 1
            entry.error( "req" )
            entry.error( "term" )
            continue

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

        # Finally, verify that the reporting was for the full number of credits
        if class_obj.max_credits != entry.cred_applied:
            logger.error( "Didn't report taking %s for the full" +
                          "number of credits for the %s requirement", req )
            errors += 1
            entry.error( "req" )
        else:
            logger.info( "%s requirement fully satisfied by %s", req, entry.course_used )
            entry.valid( "req" )

    return errors, warnings
