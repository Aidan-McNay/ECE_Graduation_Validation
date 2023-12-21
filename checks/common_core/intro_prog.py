"""
#=====================================================================
# intro_prog.py
#=====================================================================
# A check to see that the INTRO. PROG. requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from checks.utils.uchecks import is_names

# Describe the uchecks to run, and the corresponding error messages

uchecks_to_run = {
    is_names( ["CS 1110", "CS 1112"] ): "Class isn't CS 1110 or CS 1112"
}

def intro_prog_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the INTRO. PROG. requirement with either
    CS 1110 or CS 1112
    """
    return basic_check( roster, logger, "INTRO. PROG.", uchecks_to_run, full_creds = True )[:2]
