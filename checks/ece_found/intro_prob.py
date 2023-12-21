"""
#=====================================================================
# intro_prob.py
#=====================================================================
# A check to see that the INTRO. PROB. requirement is satisfied

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
    is_name( "ECE 3100" ): "Class isn't ECE 3100"
}

def intro_prob_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the INTRO. PROB. requirement with ECE 3100
    """
    return basic_check( roster, logger, "INTRO. PROB.", uchecks_to_run, full_creds = True )[:2]
