"""
#=====================================================================
# adv_prog.py
#=====================================================================
# A check to see that the ADV. PROGRAMMING checkoff is satisfied

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple, List

from obj.class_obj import Class
from obj.roster_obj import Roster
from checks.checkoffs.validate_checkoff import validate_checkoff
from checks.utils.uchecks import UcheckType

valid_classes = {
    "ECE 2400",
    "CS 2110",
    "ENGRD 3200",
    "AEP 4380",
    "ECE 4740",
    "ECE 4750",
    "ECE 4760"
}

def is_adv_prog( class_obj: Class ) -> bool:
    """
    A ucheck to determine whether a checkoff is an advanced programming course
    """
    return any( name in class_obj.all_names for name in valid_classes )

uchecks_to_run: List[UcheckType] = [ is_adv_prog ]

def adv_prog_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the ADV. PROGRAMMING checkoff with
    an advanced programming class
    """
    return validate_checkoff( roster, logger, "ADV. PROGRAMMING", uchecks_to_run )
