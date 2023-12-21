"""
#=====================================================================
# dig_logic.py
#=====================================================================
# A check to see that the DIG. LOGIC requirement is satisfied

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
    is_name( "ECE 2300" ): "Class isn't ECE 2300"
}

def dig_logic_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the DIG. LOGIC requirement with ECE 2300
    """
    return basic_check( roster, logger, "DIG. LOGIC", uchecks_to_run, full_creds = True )[:2]
