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
from typing import Tuple

import exceptions as excp
from obj.roster_obj import Roster
from obj.grades_obj import Grades
from ui.logger import SUCCESS

def grade_check( roster: Roster, grades: Grades, logger: Logger ) -> Tuple[int, int]:
    """
    Validates all of the grades reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    errors = 0
    warnings = 0

    logger.info( "Grade Check for %s:", netid )

    for entry in roster.req_entries:

        term           = entry.term
        course         = entry.course_used
        proposed_grade = entry.grade

        if ( term == "" ) or ( course == "" ):
            logger.warning( " - Not enough information provided for %s to locate grade record",
                            entry.req )
            warnings += 1
            if term == "":
                entry.warn( "term" )
            if course == "":
                entry.warn( "course" )
            entry.warn( "grade" )
            continue

        if proposed_grade == "":
            logger.warning( " - No grade supplied for %s", course )
            warnings += 1
            entry.warn( "grade" )
            continue

        try:
            real_grade = grades.get_grade( netid, term, course )
        except (excp.grade_exceptions.TermNotFoundError,
                    excp.grade_exceptions.ClassNotFoundError):
            real_grade = "No Entry"

        if real_grade != proposed_grade: #The student lied :(
            logger.error( "Proposed grade for %s (%s) doesn't match our records (%s)",
                          course, proposed_grade, real_grade )
            entry.error( "grade" )
            errors += 1
        else:
            logger.info( " - Grade match for %s", course )
            entry.valid( "grade" )

    if errors == 0:
        logger.log( SUCCESS, "All grades match" )

    return errors, warnings
