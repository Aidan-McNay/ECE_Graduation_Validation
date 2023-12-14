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

from checks.common_core.calc       import calc_check
from checks.common_core.multi      import multi_check
from checks.common_core.diff_eq    import diff_eq_check
from checks.common_core.lin_alg    import lin_alg_check
from checks.common_core.intro_prog import intro_prog_check
from checks.common_core.phys_1     import phys_1_check

CHECKS_TO_RUN = [
    calc_check,
    multi_check,
    diff_eq_check,
    lin_alg_check,
    intro_prog_check,
    phys_1_check
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
