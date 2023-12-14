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

def intro_prog_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the INTRO. PROG. requirement with either
    CS 1110 or CS 1112
    """
    return basic_check( roster, logger, "INTRO. PROG.", ["CS 1110", "CS 1112"] )[:2]
