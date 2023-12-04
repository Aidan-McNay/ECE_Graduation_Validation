#=====================================================================
# grade_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's grades
#
# Author: Aidan McNay
# Date: December 3rd, 2023

from ui.logger import printl as printl

def grade_check( roster, grades, log_path, verbose = False ):
    """
    Validates all of the grades reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    log    = [ f"Grade Check for {netid}:" ]
    errors = 0

    with open( log_path, 'w') as file:
        file.write( f"Grade Check for {netid}:" )

        for entry in roster.entries:
            # Only consider requirements, not checkoffs
            if( not entry.req.startswith( "REQ-" ) ):
                continue

            term           = entry.term
            course         = entry.course_used
            proposed_grade = entry.grade

            try:
                real_grade = grades.get_grade( netid, term, course )
            except:
                real_grade = "No Entry"

            if( real_grade != proposed_grade ): #The student lied :(
                message = f" - [ERROR] Proposed grade for {course} ({proposed_grade}) doesn't match our records ({real_grade})"
                errors += 1
            else:
                message = f" - Grade match for {course}"
         
            printl( message, file, verbose )

        if( errors == 0 ):
            printl( " - [SUCCESS] All grades match", file, verbose )

    return errors
