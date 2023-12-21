"""
#=====================================================================
# ece_upper_check.py
#=====================================================================
# A wrapper around all ECE Upper-Level Elective Checks

# Author: Aidan McNay
# Date: December 21st, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster

from checks.ece_upper.junior_level import junior_level_check
from checks.ece_upper.senior_level import senior_level_check
from checks.ece_upper.CDE          import CDE_check

CHECKS_TO_RUN = [
    junior_level_check,
    senior_level_check,
    CDE_check
]

req_types = [
    "3000+",
    "4000+",
    "CDE"
]

def ece_upper_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Runs all of the checks on the ECE Upper-Level Elective requirements
    """
    errors = 0
    warnings = 0

    # Check that the classes sum to 21 credits

    ece_upper_req_list = []
    for req_type in req_types:
        ece_upper_req_list += roster.get_req( req_type )

    cred_taken = sum( x.cred_applied for x in ece_upper_req_list )
    if cred_taken < 21:
        logger.error( "ECE Upper-Level Electives sum to %d (<21) credits", cred_taken )
        errors += 1
        for entry in ece_upper_req_list:
            entry.error( "req" )

    # Run the checks on each type of requirement

    for check in CHECKS_TO_RUN:
        result = check( roster, logger )

        errors   += result[0]
        warnings += result[1]

    return errors, warnings
