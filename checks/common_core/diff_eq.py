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
from checks.utils.uchecks import is_name

# Describe the uchecks to run, and the corresponding error messages

uchecks_to_run = {
    is_name( "MATH 2930" ): "Class isn't MATH 2930"
}

def diff_eq_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the DIFF. EQ. requirement with MATH 2930
    """
    return basic_check( roster, logger, "DIFF. EQ.", uchecks_to_run, full_creds = True )[:2]
