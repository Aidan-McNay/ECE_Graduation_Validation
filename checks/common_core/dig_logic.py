"""
#=====================================================================
# dig_logic.py
#=====================================================================
# A check to see that the DIG. LOGIC requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def dig_logic_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the DIG. LOGIC requirement with ECE 2300
    """
    return basic_check( roster, logger, "DIG. LOGIC", ["ECE 2300"] )[:2]
