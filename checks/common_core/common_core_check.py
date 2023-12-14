"""
#=====================================================================
# common_core_checks.py
#=====================================================================
# A wrapper around all Engineering Common Core Checks

# Author: Aidan McNay
# Date: December 13th, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster

from checks.common_core.math_1910 import math_1910_check

CHECKS_TO_RUN = [
    math_1910_check
]

def common_core_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Runs all of the checks on the Common Core requirements
    """
    errors = 0
    warnings = 0

    for check in CHECKS_TO_RUN:
        result = check( roster, logger )

        errors   += result[0]
        warnings += result[1]

    return errors, warnings
