"""
#=====================================================================
# course_in_reqs.py
#=====================================================================
# Verifies that a course is present in a student's requirements, used
# to make sure that courses used for Checkoffs are present elsewhere

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from typing import Optional

from obj.roster_obj import Roster
from obj.roster_entry_obj import ReqEntry

def course_in_reqs( roster: Roster, course_name: str ) -> bool:
    """
    Returns whether the given course is present in the requirements
    
    Due to the difficulties of parsing API errors in this scenario if they came up,
    I chose not to detect aliases; however, I believe the common case is to list a
    course as a checkoff as the same name in the requirements, so it shouldn't be
    an issue
    """

    for entry in roster.req_entries:
        if entry.course_used == course_name:
            return True

    return False

def req_course( roster: Roster, course_name: str ) -> Optional[ReqEntry]:
    """
    Returns the ReqEntry that satisfies the given Checkoff (indicated by the
    course name)
    """

    for entry in roster.req_entries:
        if entry.course_used == course_name:
            return entry

    return None
