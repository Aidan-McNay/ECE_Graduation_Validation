"""
#=====================================================================
# gen_chem.py
#=====================================================================
# A check to see that the GEN. CHEM. requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check

def gen_chem_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the GEN. CHEM. requirement with CHEM 2090
    """
    return basic_check( roster, logger, "GEN. CHEM.", ["CHEM 2090"] )[:2]
