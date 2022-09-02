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

###################
# has_commoncore
# Checks whether the schedule has the
# common Core Engineering classes, 
# although those specific to ECE
###################

def has_commoncore(schedule_checker):
    # First, we'll just take out 
    # - MATH 1910
    # - MATH 1920
    # - MATH 2930
    # - MATH 2940
    # - CHEM 2090
    found_math1910 = False
    found_math1920 = False
    found_math2930 = False
    found_math2940 = False
    found_chem2090 = False
    classes_to_remove = []
    num_errors = 0
    for cornell_class in schedule_checker.class_list:
        if(cornell_class.same_name("MATH 1910")):
            if(not found_math1910):
                print("Found MATH 1910!")
                found_math1910 = True
                classes_to_remove.append(cornell_class)
        elif(cornell_class.same_name("MATH 1920")):
            if(not found_math1920):
                print("Found MATH 1920!")
                found_math1920 = True
                classes_to_remove.append(cornell_class)
        elif(cornell_class.same_name("MATH 2930")):
            if(not found_math2930):
                print("Found MATH 2930!")
                found_math2930 = True
                classes_to_remove.append(cornell_class)
        elif(cornell_class.same_name("MATH 2940")):
            if(not found_math2940):
                print("Found MATH 2940!")
                found_math2940 = True
                classes_to_remove.append(cornell_class)
        elif(cornell_class.same_name("CHEM 2090")):
            if(not found_chem2090):
                print("Found CHEM 2090!")
                found_chem2090 = True
                classes_to_remove.append(cornell_class)
    if(not found_math1910):
        print("ERROR: Didn't find MATH 1910")
        num_errors += 1
    if(not found_math1920):
        print("ERROR: Didn't find MATH 1920")
        num_errors += 1
    if(not found_math2930):
        print("ERROR: Didn't find MATH 2930")
        num_errors += 1
    if(not found_math2940):
        print("ERROR: Didn't find MATH 2940")
        num_errors += 1
    if(not found_chem2090):
        print("ERROR: Didn't find CHEM 2090")
        num_errors += 1
    for cornell_class in classes_to_remove:
        schedule_checker.class_list.remove(class_to_remove)

    # Now we look for the FWS's
    num_fws_found = 0
    classes_to_remove = []
    for cornell_class in schedule_checker.class_list:
        if (cornell_class.is_FWS):
            print("Found "+cornell_class.primary_name+" as a FWS")
            if(num_fws_found < 2):
                classes_to_remove.append(cornell_class)
                num_fws_found += 1
        if(num_fws_found >= 2):
            break # Found two FWS's
    if(num_fws_found < 2):
        print("ERROR: Fewer than 2 FWS's")
        num_errors += 1
    
    for cornell_class in classes_to_remove:
        schedule_checker.class_list.remove(class_to_remove)
    
    return num_errors



###################
# has_ececore
# Checks whether the schedule has Core ECE classes
###################

def has_ececore(schedule_checker):
    found_ece2100 = False
    found_ece2300 = False
    found_ece2200_ece2720 = False
    classes_to_remove = []
    for cornell_class in schedule_checker.class_list:
        if(not found_ece2100):
            if(cornell_class.same_name("ECE 2100")):
                print("Found ECE 2100!")
                found_ece2100 = True
                classes_to_remove.append(cornell_class)
        if(not found_ece2300):
            if(cornell_class.same_name("ECE 2300")):
                print("Found ECE 2300!")
                found_ece2300 = True
                classes_to_remove.append(cornell_class)
        if(not found_ece2200_ece2720):
            if(cornell_class.same_name("ECE 2200")):
                print("Found ECE 2200!")
                found_ece2200_ece2720 = True
                classes_to_remove.append(cornell_class)
            if(cornell_class.same_name("ECE 2720")):
                print("Found ECE 2720!")
                found_ece2200_ece2720 = True
                classes_to_remove.append(cornell_class)
    
    for class_to_remove in classes_to_remove:
        schedule_checker.class_list.remove(class_to_remove)

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

###################
# has_ecefoundational
# Checks whether the schedule has Core ECE classes
###################

def has_ecefoundations(schedule_checker):
    physicalclass = None
    mathclass = None
    foundational_removed = 0
    num_errors = 0
    for cornell_class in schedule_checker.class_list:
        if(cornell_class.same_name("ECE 3030")):
            physicalclass = cornell_class
        elif(cornell_class.same_name("ECE 3100")):
            mathclass = cornell_class
        elif(cornell_class.same_name("ECE 3150")):
            physicalclass = cornell_class
        elif(cornell_class.same_name("ECE 3250")):
            mathclass = cornell_class

    if (physicalclass):
        print("Contains "+physicalclass.primary_name+", using as the physical foundational class")
        schedule_checker.class_list.remove(physicalclass)
        foundational_removed += 1
    else:
        print("ERROR: Doesn't contain ECE 3030 or ECE 3150")
        num_errors += 1

    if (mathclass):
        print("Contains "+mathclass.primary_name+", using as the math foundational class")
        schedule_checker.class_list.remove(mathclass)
        foundational_removed += 1
    else:
        print("ERROR: Doesn't contain ECE 3100 or ECE 3250")
        num_errors += 1

    # Remove final foundational class
    classes_to_remove = []
    for cornell_class in schedule_checker.class_list:
        if(cornell_class.same_name("ECE 3030") and not (physicalclass.same_name("ECE 3030"))):
            print("Using ECE 3030 as a foundational class")
            if (foundational_count < 3):
                # Only remove classes until we get to three removed
                classes_to_remove.append(cornell_class)
                foundational_removed += 1
        elif(cornell_class.same_name("ECE 3100") and not (mathclass.same_name("ECE 3100"))):
            print("Using ECE 3100 as a foundational class")
            if (foundational_count < 3):
                # Only remove classes until we get to three removed
                classes_to_remove.append(cornell_class)
                foundational_removed += 1
        elif(cornell_class.same_name("ECE 3140")):
            print("Using ECE 3140 as a foundational class")
            if (foundational_removed < 3):
                # Only remove classes until we get to three removed
                classes_to_remove.append(cornell_class)
                foundational_removed += 1
        elif(cornell_class.same_name("ECE 3150") and (physicalclass.same_name("ECE 3150"))):
            print("Using ECE 3150 as a foundational class")
            if (foundational_count < 3):
                # Only remove classes until we get to three removed
                classes_to_remove.append(cornell_class)
                foundational_removed += 1
        elif(cornell_class.same_name("ECE 3250") and not (mathclass.same_name("ECE 3250"))):
            print("Using ECE 3250 as a foundational class")
            if (foundational_count < 3):
                # Only remove classes until we get to three removed
                classes_to_remove.append(cornell_class)
                foundational_removed += 1
        if(foundational_removed==3):
            break # Don't need to search further

    for class_to_remove in classes_to_remove:
        schedule_checker.class_list.remove(class_to_remove)

    if(foundational_removed < 3):
        print("ERROR: Fewer than 3 foundational classes")
        num_errors += 1
    return num_errors