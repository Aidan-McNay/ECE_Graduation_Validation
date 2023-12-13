"""
#=====================================================================
# math_1910.py
#=====================================================================
# A check to see that the MATH 1910 requirement is satisfied

# Author: Aidan McNay
# Date: December 13th, 2023
"""

from logging import Logger

from obj.roster_obj import Roster
from obj.class_obj import Class

def math_1910_check( roster: Roster, logger: Logger ) -> int:
    errors = 0

    entry_list = roster.get_req( "CALC." )
    if len( entry_list ) != 1:
        logger.error( "Expected 1 entry for the CALC. requirement, found %d", len( entry_list ) )
        for entry in entry_list:
            entry.warn( "req" )
        errors += 1
    
    for entry in entry_list: # Should be just one