"""
#=====================================================================
# phys_1.py
#=====================================================================
# A check to see that the PHYS. 1 requirement is satisfied (as well as
# EXP. PHYS., if necessary)

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from obj.class_obj import Class
from checks.utils.basic_check import basic_check
from ui.parser import term_is_later

import exceptions as excp

def exp_phys_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the EXP. PHYS. requirement with PHYS 1110
    """
    return basic_check( roster, logger, "EXP. PHYS.", ["PHYS 1110"] )

def phys_1_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfied the PHYS. 1 requirement, as well as the
    PHYS 1110 requirement if needed.

    This looks very similar to basic_check, but also calls exp_phys_check if needed
    """
    req = "PHYS. 1"
    valid_class_names = ["PHYS 1112", "PHYS 1116"]
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
            logger.error( "Reported taking %s for fewer credits (%d) than the full " +
                          "number of credits (%d) for the %s requirement", 
                          entry.course_used, entry.cred_applied, class_obj.max_credits, req )
            errors += 1
            entry.error( "req" )
        else:
            logger.info( "%s requirement fully satisfied by %s", req, entry.course_used )
            entry.valid( "req" )

        if ( entry.course_used == "PHYS 1112" ) and term_is_later( entry.term, "SU23" ):
            # If so, they also need to take PHYS 1110
            phys_1110_result = exp_phys_check( roster, logger )
            errors   += phys_1110_result[0]
            warnings += phys_1110_result[1]

    return errors, warnings
