"""
#=====================================================================
# phys_ed.py
#=====================================================================
# A check to see that the PHYS. ED. requirements are satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from checks.utils.uchecks import is_dept

# Describe the uchecks to run, and the corresponding error messages

uchecks_to_run = {
    is_dept( "PE" ): "Class isn't a PE"
}

def phys_ed_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the PHYS. ED. requirement with any two PE classes
    """
    return basic_check( roster, logger, "PHYS. ED.", uchecks_to_run, req_num_expected = 2,
                        full_creds = True )[:2]
