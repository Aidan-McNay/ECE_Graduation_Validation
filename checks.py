#####################################
# checks.py
# Author: Aidan McNay
#####################################
# Contains the checks to run on 
# a Schedule to validate it
#
# All check functions should only take
# a ScheduleChecker object as an argument,
# and should return the number of errors
# found during the check

def has_ececore(schedule_checker):
    """
    Checks the schedule to make sure it has ECE 2100,
    ECE2300, and either ECE 2200 or ECE 2720
    """
    found_ece2100 = False
    found_ece2300 = False
    found_ece2200_ece2720 = False
    for cornell_class in schedule_checker.class_list:
        if(not found_ece2100):
            if(cornell_class=="ECE 2100"):
                print("Found ECE 2100!")
                found_ece2100 = True
                schedule_check.class_list.remove(cornell_class)
        if(not found_ece2300):
            if(cornell_class=="ECE 2300"):
                print("Found ECE 2300!")
                found_ece2300 = True
                schedule_check.class_list.remove(cornell_class)
        if(not found_ece2200_ece2720):
            if(cornell_class=="ECE 2200"):
                print("Found ECE 2200!")
                found_ece2200_ece2720 = True
                schedule_check.class_list.remove(cornell_class)
            if(cornell_class=="ECE 2720"):
                print("Found ECE 2720!")
                found_ece2200_ece2720 = True
                schedule_check.class_list.remove(cornell_class)
        if(found_ece2100 and found_ece2300 and found_ece2200_ece2720):
            break # Early exit if we found all three
    # Calculate errors
    num_errors = 0
    if(not found_ece2100):
        print("ERROR: Didn't find ECE 2100")
        num_errors += 1
    if(not found_ece2300):
        print("ERROR: Didn't find ECE 2300")
        num_errors += 1
    if(not found_ece2200_ece2720):
        print("ERROR: Didn't find ECE 2200 or ECE 2720")
        num_errors += 1
    return num_errors

