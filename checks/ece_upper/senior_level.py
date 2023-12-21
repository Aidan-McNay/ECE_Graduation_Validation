"""
#=====================================================================
# senior_level.py
#=====================================================================
# A check to verify both 4000+ ECE Upper-Level Requirements

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from checks.utils.uchecks import is_dept, is_level
from checks.ece_upper.tech_courses import is_technical

# Describe the uchecks to run, and the corresponding error messages

uchecks_to_run = {
    is_dept( "ECE" ): "Class isn't an ECE course",
    is_level( 4000 ): "Class isn't a 4000+ level class",
    is_technical()  : "Class isn't a technical ECE course"
}

def senior_level_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the 4000+ requirement with 2 4000+ ECE technical classes
    """
    return basic_check( roster, logger, "4000+", uchecks_to_run, req_num_expected = 2 )[:2]
