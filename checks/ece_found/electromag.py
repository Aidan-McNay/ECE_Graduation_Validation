"""
#=====================================================================
# electromag.py
#=====================================================================
# A check to see that the ELECTROMAG. requirement is satisfied

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
    is_name( "ECE 3030" ): "Class isn't ECE 3030"
}

def electromag_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the ELECTROMAG. requirement with ECE 3030
    """
    return basic_check( roster, logger, "ELECTROMAG.", uchecks_to_run, full_creds = True )[:2]
