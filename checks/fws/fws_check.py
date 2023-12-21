"""
#=====================================================================
# fws_check.py
#=====================================================================
# A check for all FWS Requirements

# Author: Aidan McNay
# Date: December 13th, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster
from checks.utils.basic_check import basic_check
from checks.utils.uchecks import is_FWS

uchecks_to_run = {
    is_FWS(): "Class isn't an FWS"
}

def fws_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Verifies that all of our FWS requrements are satisfied by FWS classes

    this can be done by running a basic_check on the FWS requirement, specifying
    the appropriate ucheck to verify that they're FWS classes
    """
    return basic_check( roster, logger, "FWS", uchecks_to_run, req_num_expected = 2 )[:2]
