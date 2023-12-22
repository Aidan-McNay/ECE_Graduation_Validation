"""
#=====================================================================
# validate_checkoff.py
#=====================================================================
# A general check to validate a checkoff

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple, List, cast

from obj.class_obj import Class
from obj.roster_obj import Roster
from obj.roster_entry_obj import ReqEntry
from checks.utils.uchecks import UcheckType
from checks.checkoffs.course_in_reqs import course_in_reqs, req_course

import exceptions as excp

def validate_checkoff( roster: Roster, logger: Logger, checkoff: str,
                       uchecks: List[UcheckType] ) -> Tuple[int, int]:
    """
    Validates a checkoff of the given type, using the given uchecks to validate semantics
    """

    errors   = 0
    warnings = 0

    # Check that only one entry was supplied

    entry_list = roster.get_checkoff( checkoff )
    if len( entry_list ) != 1:
        logger.error( "Expected 1 entry for the %s checkoff, found %d",
                      checkoff, len( entry_list ) )
        for entry in entry_list:
            entry.error( "req" )
        errors += 1
        return errors, warnings

    entry = entry_list[0]

    # Check that the entry appears in the roster

    if course_in_reqs( roster, entry.course_used ):
        logger.info( "%s found in the checklists' requirements", entry.course_used )
        entry.valid( "course" )
    else:
        logger.error( "%s not found in the checklists' requirements", entry.course_used )
        entry.error( "course" )
        entry.error( "req" )
        errors += 1
        return errors, warnings

    # Check that the entry satisfies the requirements - assume that it was found

    req_entry = cast( ReqEntry, req_course( roster, entry.course_used ) )

    try:
        class_obj = Class( req_entry.course_used, req_entry.term )
    except ( excp.api_exceptions.TermNotFoundError,
             excp.api_exceptions.DeptNotFoundError,
             excp.api_exceptions.ClassNotFoundError ):
        logger.error( "%s wasn't offered during %s", req_entry.course_used, req_entry.term )
        entry.error( "course" )
        entry.error( "req" )
        errors += 1
        return errors, warnings

    if all( check( class_obj ) for check in uchecks ):
        logger.info( "%s checkoff fully satisfied by %s", checkoff, entry.course_used )
        entry.valid( "req" )
    else:
        logger.error( "%s checkoff not satisfied by %s", checkoff, entry.course_used )
        entry.error( "req" )
        errors += 1

    return errors, warnings
