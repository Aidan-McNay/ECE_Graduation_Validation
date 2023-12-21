"""
#=====================================================================
# circuits.py
#=====================================================================
# A check to see that the CIRCUITS requirement is satisfied

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from checks.utils.uchecks import is_name

# Describe the uchecks to run, and the corresponding error messages

uchecks_to_run = {
    is_name( "ECE 2100" ): "Class isn't ECE 2100"
}

def circuits_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the CIRCUITS requirement with ECE 2100
    """
    return basic_check( roster, logger, "CIRCUITS", uchecks_to_run, full_creds = True )[:2]
