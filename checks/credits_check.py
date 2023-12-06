"""
#=====================================================================
# credits_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's credits
# taken
#
# Author: Aidan McNay
# Date: December 3rd, 2023
"""

from logging import Logger

import exceptions as excp
from obj.roster_obj import Roster
from obj.grades_obj import Grades
from ui.logger import SUCCESS

def credits_check( roster: Roster, grades: Grades, logger: Logger ) -> int:
    """
    Validates all of the credits reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    errors = 0

    logger.info( "Credits Check for %s:", netid )

    for entry in roster.req_entries:

        term             = entry.term
        course           = entry.course_used
        proposed_credits = entry.cred_applied
        cred_applied     = False

        try:
            real_credits = grades.get_credits( netid, term, course )
        except (excp.grade_exceptions.TermNotFoundError,
                excp.grade_exceptions.ClassNotFoundError):
            real_credits = -1

        if real_credits != proposed_credits: #The student lied :(
            logger.error( "Proposed credits for %s (%d) doesn't match our records (%d)",
                          course, proposed_credits, real_credits )
            errors += 1
        else:
            logger.info( " - Credits match for %s", course )

    if errors == 0:
        logger.log( SUCCESS, "All credits match" )

    return errors
