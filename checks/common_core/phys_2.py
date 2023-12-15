"""
#=====================================================================
# phys_2.py
#=====================================================================
# A check to see that the PHYS. 2 requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def phys_2_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the PHYS. 2 requirement with PHYS 2213 or PHYS 2217
    """
    return basic_check( roster, logger, "PHYS. 2", ["PHYS 2213", "PHYS 2217"] )[:2]
