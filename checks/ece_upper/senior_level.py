"""
#=====================================================================
# senior_level.py
#=====================================================================
# A check to verify both 4000+ ECE Upper-Level Requirements

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple, Dict, Callable

from obj.roster_obj import Roster
from obj.class_obj import Class
from checks.utils.basic_check import basic_check
from checks.ece_upper.tech_courses import is_technical

# Define a ucheck to see if the course is at the senior level

valid_cs_courses = [
    "CS 4120",
    "CS 4121",
    "CS 4410",
    "CS 4411"
]

def is_junior_level( class_obj: Class ) -> bool:
    """Checks whether the given class is a valid CDE"""

    if any( name in class_obj.all_names for name in valid_cs_courses ):
        return True

    if ( "ECE" in class_obj.all_departments ) and \
       ( int( class_obj.course_number ) >= 4000 ) and \
       ( is_technical( class_obj ) ):
        return True

    return False

# Describe the uchecks to run, and the corresponding error messages
# (we need to explicitly type this, to avoid incorrect type inference
# of is_senior_level with named parameters)

uchecks_to_run: Dict[Callable[[Class], bool], str] = {
    is_junior_level: "Class isn't a valid 4000+ ECE technical elective"
}

def senior_level_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the 4000+ requirement with 2 4000+ ECE technical classes
    """
    return basic_check( roster, logger, "4000+", uchecks_to_run, req_num_expected = 2 )[:2]
