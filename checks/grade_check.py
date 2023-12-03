#=====================================================================
# grade_check.py
#=====================================================================
# Checking whether a checklist is consistent with a student's grades
#
# Author: Aidan McNay
# Date: December 3rd, 2023

def grade_check( roster, grades, log_path, verbose = False ):
    """
    Validates all of the grades reported in a Roster, verifying
    against the given Grades. The results are outputted to the given
    log_path, and the function returns the number of mismatches
    (0 if no mismatches)
    """

    netid  = roster.netid
    log    = [ f"Grade Check for {netid}:\n" ]
    errors = 0

    for entry in roster.entries:
        term           = entry.term
        course         = entry.course_used
        proposed_grade = entry.grade

        try:
            real_grade = grades.get_grade( netid, term, course )
        except:
            real_grade = "No Entry"

        if( real_grade != proposed_grade ): #The student lied :(
            message = f" - [ERROR] Proposed grade for {course} ({proposed_grade}) doesn't match our records ({real_grade})\n"
            errors += 1
        else:
            message = f" - Grade match for {course}\n"
         
        log.append( message )
        if( verbose ):
            print( message )

    if( errors == 0 ):
        message = " - [SUCCESS] All grades match"
        log.append( message )
        if( verbose ):
            print( message )

    with open( log_path, 'w') as file:
        file.writelines( log )

    return errors
