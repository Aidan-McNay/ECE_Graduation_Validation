"""
#=====================================================================
# multi.py
#=====================================================================
# A check to see that the MULTI. requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def multi_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the MULTI. requirement with MATH 1920
    """
    return basic_check( roster, logger, "MULTI.", ["MATH 1920"] )[:2]
