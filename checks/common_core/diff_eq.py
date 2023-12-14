"""
#=====================================================================
# diff_eq.py
#=====================================================================
# A check to see that the DIFF. EQ. requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def diff_eq_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the DIFF. EQ. requirement with MATH 2930
    """
    return basic_check( roster, logger, "DIFF. EQ.", ["MATH 2930"] )
