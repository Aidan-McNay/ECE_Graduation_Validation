"""
#=====================================================================
# ece_found_check.py
#=====================================================================
# A wrapper around all ECE Foundation Checks

# Author: Aidan McNay
# Date: December 21st, 2023
"""
from logging import Logger
from typing import Tuple

from obj.roster_obj import Roster

from checks.ece_found.electromag       import electromag_check
from checks.ece_found.intro_prob       import intro_prob_check
from checks.ece_found.embedded_sys     import embedded_sys_check
from checks.ece_found.microelectronics import microelectronics_check
from checks.ece_found.sig_and_sys      import sig_and_sys_check

req_check_mapping = {
    "ELECTROMAG."     : electromag_check,
    "INTRO. PROB."    : intro_prob_check,
    "EMBEDDED SYS."   : embedded_sys_check,
    "MICROELECTRONICS": microelectronics_check,
    "SIG. & SYS."     : sig_and_sys_check
}

def ece_found_check( roster: Roster, logger: Logger ) -> Tuple[int, int]:
    """
    Runs all of the checks on the ECE Foundation requirements
    """

    # pylint: disable=too-many-branches

    errors = 0
    warnings = 0

    # Form the possible requirements

    ece_found_req_list = []
    for req_type in req_check_mapping:
        ece_found_req_list += roster.get_req( req_type )

    # Delete all the blank entries

    for entry in ece_found_req_list:
        if entry.course_used == "":
            ece_found_req_list.remove( entry )

    # Make sure that we have 3 entries

    if len( ece_found_req_list ) != 3:
        logger.error( " - Expected 3 Foundation entries, but got %d", len( ece_found_req_list ) )
        logger.error( " - Extra Foundation courses should be listed as EXTRA-C courses" )
        errors += 1
        for entry in ece_found_req_list:
            entry.error( "req" )

    # Make sure no multiple entries

    found_reqs = set()
    for entry in ece_found_req_list:
        if entry.req in found_reqs:
            logger.error( "Found multiple instances of the %s requirement", entry.req )
            entry.error( "req" )
        else:
            found_reqs.add( entry.req )

    logger.info( "Foundation Requirements found: " + ", ".join( found_reqs ) )

    # Make sure we have instances of the required foundation classes

    if ( "ELECTROMAG." not in found_reqs ) and ( "MICROELECTRONICS" not in found_reqs ):
        logger.error( "Foundations don't include either Electromagnetism (ECE 3030) " +
                      "or Microelectronics (ECE 3150)" )
        errors += 1
        for entry in ece_found_req_list:
            entry.error( "req" )

    if ( "INTRO. PROB." not in found_reqs ) and ( "SIG. & SYS." not in found_reqs ):
        logger.error( "Foundations don't include either Probability (ECE 3100) " +
                      "or Signals & Systems (ECE 3250)" )
        errors += 1
        for entry in ece_found_req_list:
            entry.error( "req" )

    # Finally, check that each requirement present is satisfied

    for req in found_reqs:
        check_to_run = req_check_mapping[ req ]
        result = check_to_run( roster, logger )
        errors   += result[0]
        warnings += result[1]

    return errors, warnings

    # pylint: enable=too-many-branches
