"""
#=====================================================================
# checkoffs_check.py
#=====================================================================
# A wrapper around all Checkoffs checks

# Author: Aidan McNay
# Date: December 21st, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster

from checks.checkoffs.adv_prog  import adv_prog_check
from checks.checkoffs.tech_writ import tech_writ_check

CHECKS_TO_RUN = [
    adv_prog_check,
    tech_writ_check
]

def checkoffs_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
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
