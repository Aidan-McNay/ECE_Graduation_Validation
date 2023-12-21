"""
#=====================================================================
# embedded_sys.py
#=====================================================================
# A check to see that the EMBEDDED SYS. requirement is satisfied

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
    is_name( "ECE 3140" ): "Class isn't ECE 3140"
}

def embedded_sys_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the EMBEDDED SYS. requirement with ECE 3140
    """
    return basic_check( roster, logger, "EMBEDDED SYS.", uchecks_to_run, full_creds = True )[:2]
