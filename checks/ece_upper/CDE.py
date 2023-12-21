"""
#=====================================================================
# CDE.py
#=====================================================================
# A check to verify the CDE Requirement

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple, Callable, Dict

from obj.roster_obj import Roster
from obj.class_obj import Class
from checks.utils.basic_check import basic_check

# Define a ucheck to see if the course is a valid CDE

valid_ece_classes = [
    "ECE 4530",
    "ECE 4670",
    "ECE 4740",
    "ECE 4750",
    "ECE 4760"
]

valid_cs_courses = [
    "CS 4120",
    "CS 4121",
    "CS 4410",
    "CS 4411"
]

def is_CDE( class_obj: Class ) -> bool:
    """Checks whether the given class is a valid CDE"""

    if any( name in class_obj.all_names for name in valid_cs_courses ):
        return True

    if ( "ECE" in class_obj.all_departments ) and \
       ( int( class_obj.course_number ) >= 4000 ) and \
       ( any( name in class_obj.all_names for name in valid_ece_classes ) or class_obj.is_CDE ):
        return True

    return False

# Describe the uchecks to run, and the corresponding error messages
# (we need to explicitly type this for CDEs, to avoid incorrect type inference
# of is_CDE with named parameters)

uchecks_to_run: Dict[Callable[[Class], bool], str] = {
    is_CDE: "Class isn't a valid CDE"
}

def CDE_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the CDE requirement
    """
    return basic_check( roster, logger, "CDE", uchecks_to_run )[:2]
