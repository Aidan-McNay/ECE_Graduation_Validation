"""
#=====================================================================
# grade_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's grades
#
# Author: Aidan McNay
# Date: December 3rd, 2023
"""

from ui.logger import printl
import exceptions as excp

from obj.roster_obj import Roster
from obj.grades_obj import Grades

def grade_check( roster: Roster, grades: Grades, log_path: str, verbose: bool = False ) -> int:
    """
    Validates all of the grades reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    errors = 0

    with open( log_path, 'w', encoding = "utf-8" ) as file:
        file.write( f"Grade Check for {netid}:\n" )

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
                message = f" - [ERROR] Proposed grade for {course} ({proposed_grade}) + "\
                                    f" doesn't match our records ({real_grade})"
                errors += 1
            else:
                message = f" - Grade match for {course}"

            printl( message, file, verbose )

        if errors == 0:
            printl( " - [SUCCESS] All grades match", file, verbose )

    return errors
