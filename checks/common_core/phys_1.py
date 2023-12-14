"""
#=====================================================================
# phys_1.py
#=====================================================================
# A check to see that the PHYS. 1 requirement is satisfied (as well as
# EXP. PHYS., if necessary)

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from ui.parser import term_is_later

def exp_phys_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the EXP. PHYS. requirement with PHYS 1110
    """
    return basic_check( roster, logger, "EXP. PHYS.", ["PHYS 1110"] )[:2]

def phys_1_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfied the PHYS. 1 requirement, as well as the
    PHYS 1110 requirement if needed.
    """

    errors, warnings, entry = basic_check( roster, logger, "PHYS. 1", ["PHYS 1112", "PHYS 1116"] )

    if ( entry.course_used == "PHYS 1112" ) and term_is_later( entry.term, "SU23" ):
        # If so, they also need to take PHYS 1110
        phys_1110_result = exp_phys_check( roster, logger )
        errors   += phys_1110_result[0]
        warnings += phys_1110_result[1]

    return errors, warnings
