"""
#=====================================================================
# engr_dist.py
#=====================================================================
# A check to see that the ENGR. DIST. requirement is satisfied

# Author: Aidan McNay
# Date: December 16th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from checks.utils.uchecks import is_dept

# Describe the uchecks to run, and the corresponding error messages

uchecks_to_run = {
    is_dept( "ENGRD" ): "Class isn't an ENGRD"
}

def engr_dist_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the ENGR. DIST. requirement with an ENGRD class
    """
    return basic_check( roster, logger, "ENGR. DIST.", uchecks_to_run, full_creds = True )[:2]
