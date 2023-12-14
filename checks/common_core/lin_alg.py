"""
#=====================================================================
# lin_alg.py
#=====================================================================
# A check to see that the LIN. ALG. requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def lin_alg_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the LIN. ALG. requirement with MATH 2940
    """
    return basic_check( roster, logger, "LIN. ALG.", ["MATH 2940"] )
