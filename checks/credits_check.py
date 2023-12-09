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

from exceptions.class_records_exceptions import RecordNotFoundError
from exceptions.class_records_exceptions import InsufficientCreditsError

from obj.roster_obj import Roster
from obj.grades_obj import Grades
from obj.class_records_obj import ClassRecords
from ui.logger import SUCCESS

def credits_check( roster: Roster, grades: Grades, logger: Logger ) -> int:
    """
    Validates all of the credits reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    errors = 0

    logger.info( "Credits Check for %s:", netid )

    records = ClassRecords( netid, grades )

    for entry in roster.req_entries:

        term             = entry.term
        course           = entry.course_used
        proposed_credits = entry.cred_applied

        try:
            records.use_cred( course, term, proposed_credits )
            logger.info( " - Credits match for %s", course )

        except ( RecordNotFoundError, InsufficientCreditsError ) as e:
            logger.error( e.err_msg )
            roster.error( entry )
            errors += 1

    if errors == 0:
        logger.log( SUCCESS, "All credits match" )

    return errors
