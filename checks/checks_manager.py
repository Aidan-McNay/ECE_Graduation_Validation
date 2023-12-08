"""
#=====================================================================
# checks_manager.py
#=====================================================================
# A wrapper around checks to run on checklists
#
# Author: Aidan McNay
# Date: December 8th, 2023
"""

from logging import Logger
import os
from typing import Dict, List, Callable

from obj.roster_obj import Roster
from ui.logger import gen_v_file_logger, SUCCESS

#---------------------------------------------------------------------
# ChecksManager Object
#---------------------------------------------------------------------

class ChecksManager:
    """
    A Python wrapper around all of the checks that we need to run on a
    checklist

    For the purposes of this manager, a "check" is defined as any
    function of the following signature:

        check( roster: Roster, logger: logging.Logger ) -> int

    The check should take in a Roster and logger, and return the
    number of errors that the check generated

    Attributes:

     - checks: The checks that are being managed
               (dictionary mapping str (name of check) to a 
                "check", as defined above)

     - results: The results of running the checks
                (dictionary mapping str (netid) to a dict mapping
                 str (name of check) to an int (number of errors) )

                {
                  netid1: {
                    check1: 2,
                    check2: 0,
                    check3: 1,
                    ...
                  },
                  netid2: {
                    ...
                  },
                  ...
                }
    """

    def __init__( self ) -> None:
        self.checks:  Dict[str, Callable[[Roster, Logger], int]] = {}
        self.results: Dict[str, Dict[str,int]] = {}

    def add_check( self, check_name: str, check_func: Callable[[Roster, Logger], int] ) -> None:
        """Adds a check to the set of checks to run"""
        self.checks[ check_name ] = check_func

    def run_checks( self, rosters: List[ Roster ], log_dir: str, logger: Logger ) -> None:
        """
        Runs the checks on the specified list of Roster, logging the output
        in the specified directory (as well as general info with the provided
        Logger)
        """

        for check_name, check_func in self.checks.items():
            result_dir = os.path.join( log_dir, check_name )
            os.makedirs( result_dir, exist_ok = True )

            logger.info( "Running %s...", check_name )

            for roster in rosters:
                netid = roster.netid
                log_file = os.path.join( result_dir, f"{netid}.log" )
                check_logger = gen_v_file_logger( log_file )

                if netid not in self.results:
                    self.results[ netid ] = {}

                self.results[ netid ][ check_name ] = check_func( roster, check_logger )

    def summary( self, logger: Logger ) -> None:
        """Logs a summary of all checks run"""

        if len( self.results ) > 0:

            logger.info( "Summary:" )

            total_errors = 0

            for netid, error_logs in self.results.items():
                netid_errors = sum( error_logs.values() )
                total_errors += netid_errors
                logger.info( " - %s: %d errors", netid, netid_errors )

                for check_name, check_errors in error_logs.items():
                    logger.info( "    - %s: %d errors", check_name, check_errors )

            if total_errors > 0:
                logger.error( "Overall: %d errors", total_errors )
            else:
                logger.log( SUCCESS, "All checks passed!" )
