"""
#=====================================================================
# common_core_check.py
#=====================================================================
# A wrapper around all Engineering Common Core Checks

# Author: Aidan McNay
# Date: December 13th, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster

from checks.common_core.calc          import calc_check
from checks.common_core.multi         import multi_check
from checks.common_core.diff_eq       import diff_eq_check
from checks.common_core.lin_alg       import lin_alg_check
from checks.common_core.intro_prog    import intro_prog_check
from checks.common_core.gen_chem      import gen_chem_check
from checks.common_core.phys_1        import phys_1_check
from checks.common_core.phys_2        import phys_2_check
from checks.common_core.phys_3        import phys_3_check
from checks.common_core.dig_logic     import dig_logic_check
from checks.common_core.phys_ed       import phys_ed_check
from checks.common_core.engr_dist     import engr_dist_check
from checks.common_core.engr_interest import engr_interest_check

CHECKS_TO_RUN = [
    calc_check,
    multi_check,
    diff_eq_check,
    lin_alg_check,
    intro_prog_check,
    gen_chem_check,
    phys_1_check,
    phys_2_check,
    phys_3_check,
    dig_logic_check,
    phys_ed_check,
    engr_dist_check,
    engr_interest_check
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
