#=====================================================================
# credits_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's credits
# taken
#
# Author: Aidan McNay
# Date: December 3rd, 2023

from ui.logger import printl as printl

def credits_check( roster, grades, log_path, verbose = False ):
    """
    Validates all of the credits reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    errors = 0

    with open( log_path, 'w') as file:
        file.write( f"Credits Check for {netid}:" )

        for entry in roster.entries:
            # Only consider requirements, not checkoffs
            if( not entry.req.startswith( "REQ-" ) ):
                continue

            term             = entry.term
            course           = entry.course_used
            proposed_credits = entry.cred_applied

            try:
                real_credits = grades.get_credits( netid, term, course )
            except:
                real_credits = "No Entry"

            if( real_credits != proposed_credits ): #The student lied :(
                message = f" - [ERROR] Proposed credits for {course} ({proposed_credits}) doesn't match our records ({real_credits})"
                errors += 1
            else:
                message = f" - Credits match for {course}"
         
            printl( message, file, verbose )

        if( errors == 0 ):
            printl( " - [SUCCESS] All credits match", file, verbose )

    return errors
