"""
#=====================================================================
# grade_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's grades
#
# Author: Aidan McNay
# Date: December 3rd, 2023
"""

from logging import Logger

import exceptions as excp
from obj.roster_obj import Roster
from obj.grades_obj import Grades
from ui.logger import SUCCESS

def grade_check( roster: Roster, grades: Grades, logger: Logger ) -> int:
    """
    Validates all of the grades reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    errors = 0

    logger.info( "Grade Check for %s:", netid )

    for entry in roster.req_entries:

        term           = entry.term
        course         = entry.course_used
        proposed_grade = entry.grade

        try:
            real_grade = grades.get_grade( netid, term, course )
        except (excp.grade_exceptions.TermNotFoundError,
                    excp.grade_exceptions.ClassNotFoundError):
            real_grade = "No Entry"

        if real_grade != proposed_grade: #The student lied :(
            logger.error( "Proposed grade for %s (%s) doesn't match our records (%s)",
                          course, proposed_grade, real_grade )
            roster.error( entry )
            errors += 1
        else:
            logger.info( " - Grade match for %s", course )

    if errors == 0:
        logger.log( SUCCESS, "All grades match" )

    return errors
