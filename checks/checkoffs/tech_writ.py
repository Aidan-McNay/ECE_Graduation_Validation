"""
#=====================================================================
# tech_writ.py
#=====================================================================
# A check to see that the TECH. WRITING checkoff is satisfied

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple, List

from obj.class_obj import Class
from obj.roster_obj import Roster
from checks.utils.uchecks import UcheckType
from checks.checkoffs.validate_checkoff import validate_checkoff

valid_classes = {
    "ECE 4920",
    "COMM 3030",
    "COMM 3020"
}

def is_tech_writ( class_obj: Class ) -> bool:
    """
    A ucheck to determine whether a checkoff is an advanced programming course
    """
    if "ENGRC" in class_obj.all_departments:
        return True

    return any( name in class_obj.all_names for name in valid_classes )

uchecks_to_run: List[UcheckType] = [ is_tech_writ ]

def tech_writ_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the ADV. PROGRAMMING checkoff with
    an advanced programming class
    """
    return validate_checkoff( roster, logger, "TECH. WRITING", uchecks_to_run )
