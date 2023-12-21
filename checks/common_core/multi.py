"""
#=====================================================================
# multi.py
#=====================================================================
# A check to see that the MULTI. requirement is satisfied

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
    is_name( "MATH 1920" ): "Class isn't MATH 1920"
}

def multi_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the MULTI. requirement with MATH 1920
    """
    return basic_check( roster, logger, "MULTI.", uchecks_to_run, full_creds = True )[:2]
