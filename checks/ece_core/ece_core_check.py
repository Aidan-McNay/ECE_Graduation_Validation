"""
#=====================================================================
# ece_core_checks.py
#=====================================================================
# A wrapper around all ECE Core Checks

# Author: Aidan McNay
# Date: December 21st, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster

from checks.ece_core.circuits     import circuits_check
from checks.ece_core.data_science import data_science_check

CHECKS_TO_RUN = [
    circuits_check,
    data_science_check
]

def ece_core_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Runs all of the checks on the ECE Core requirements
    """
    errors = 0
    warnings = 0

    for check in CHECKS_TO_RUN:
        result = check( roster, logger )

        errors   += result[0]
        warnings += result[1]

    return errors, warnings
