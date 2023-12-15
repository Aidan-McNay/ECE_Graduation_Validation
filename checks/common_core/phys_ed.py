"""
#=====================================================================
# phys_ed.py
#=====================================================================
# A check to see that the PHYS. ED. requirements are satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def phys_ed_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the PHYS. ED. requirement with any two PE classes
    """
    return basic_check( roster, logger, "PHYS. ED.", ["PE"], req_num_expected = 2 )[:2]
