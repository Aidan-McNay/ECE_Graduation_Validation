"""
#=====================================================================
# phys_3.py
#=====================================================================
# A check to see that the PHYS. 3 requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def phys_3_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the PHYS. 3 requirement with PHYS 2214 or PHYS 2218
    """
    return basic_check( roster, logger, "PHYS. 3", ["PHYS 2214", "PHYS 2218"] )[:2]
