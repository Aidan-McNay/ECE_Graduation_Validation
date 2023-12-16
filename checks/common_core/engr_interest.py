"""
#=====================================================================
# engr_dist.py
#=====================================================================
# A check to see that the ENGR. INTEREST requirement is satisfied

# Author: Aidan McNay
# Date: December 16th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def engr_interest_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the ENGR. INTEREST requirement with an ENGRI class
    """
    return basic_check( roster, logger, "ENGR. INTEREST", ["ENGRI"] )[:2]
