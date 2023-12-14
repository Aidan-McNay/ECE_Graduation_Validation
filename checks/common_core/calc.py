"""
#=====================================================================
# calc.py
#=====================================================================
# A check to see that the CALC. requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def calc_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the CALC. requirement with MATH 1910
    """
    return basic_check( roster, logger, "CALC.", ["MATH 1910"] )
