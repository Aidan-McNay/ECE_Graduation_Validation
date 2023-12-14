"""
#=====================================================================
# credits_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's credits
# taken
#
# Author: Aidan McNay
# Date: December 3rd, 2023
"""

from logging import Logger
from typing import Tuple

from exceptions.class_records_exceptions import RecordNotFoundError
from exceptions.class_records_exceptions import InsufficientCreditsError

from obj.roster_obj import Roster
from obj.grades_obj import Grades
from obj.class_records_obj import ClassRecords
from ui.logger import SUCCESS

def credits_check( roster: Roster, grades: Grades, logger: Logger ) -> Tuple[int, int]:
    """
    Validates all of the credits reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    errors = 0
    warnings = 0

    logger.info( "Credits Check for %s:", netid )

    records = ClassRecords( netid, grades )

    for entry in roster.req_entries:

        term             = entry.term
        course           = entry.course_used
        proposed_credits = entry.cred_applied

        if ( term == "" ) or ( course == "" ):
            logger.warning( " - Not enough information provided for %s to locate credit record",
                            entry.req )
            warnings += 1
            # Grade check will already warn the appropriate term/course entries
            entry.warn( "cred" )
            continue

        if proposed_credits == -1:
            logger.warning( " - No credits supplied for %s", course )
            warnings += 1
            entry.warn( "cred" )
            continue

        try:
            records.use_cred( course, term, proposed_credits )
            logger.info( " - Credits match for %s", course )
            entry.valid( "cred" )

        except ( RecordNotFoundError, InsufficientCreditsError ) as e:
            logger.error( e.err_msg )
            entry.error( "cred" )
            errors += 1

    if errors == 0:
        logger.log( SUCCESS, "All credits match" )

    return errors, warnings
