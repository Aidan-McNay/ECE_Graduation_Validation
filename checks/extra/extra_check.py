"""
#=====================================================================
# extra_check.py
#=====================================================================
# A check for all extra classes

# Author: Aidan McNay
# Date: December 21st, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def extra_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Runs all of the checks on the extra classes

    Since they don't have to satisfy any requirements, we just run a basic_check with no
    uchecks, to verify that classes were supplied that were actually offered
    """
    return basic_check( roster, logger, "EXTRA-C", {}, req_num_expected = -1 )[:2]
