"""
#=====================================================================
# data_science.py
#=====================================================================
# A check to see that the DATA SCIENCE requirement is satisfied

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from checks.utils.uchecks import is_names

# Describe the uchecks to run, and the corresponding error messages

uchecks_to_run = {
    is_names( ["ECE 2200", "ECE 2720"] ): "Class isn't ECE 2200 or ECE 2720"
}

def data_science_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Checks that the student satisfies the DATA SCIENCE requirement with ECE 2200 or ECE 2720
    """
    return basic_check( roster, logger, "DATA SCIENCE", uchecks_to_run, full_creds = True )[:2]
