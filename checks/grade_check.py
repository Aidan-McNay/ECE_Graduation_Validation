#=====================================================================
# grade_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's grades
#
# Author: Aidan McNay
# Date: December 3rd, 2023

def grade_check( roster, grades, log_path ):
    """
    Validates all of the grades reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    log    = []
    errors = 0

    for entry in roster.entries:
        term           = entry.term
        course         = entry.course_used
        proposed_grade = entry.grade

        real_grade     = grades.get_grade( netid, term, course )

        if( real_grade != proposed grade ): #The student lied :(
            log.append( f"ERROR: Proposed grade for {course} ({proposed_grade}) doesn't match our records ({real_grade})\n" )
            errors += 1
        else:
            log.append( f"SUCCESS: Grade match for {course}\n" )

    with open( log_path, 'w') as file:
        file.writelines( log )

    return errors
