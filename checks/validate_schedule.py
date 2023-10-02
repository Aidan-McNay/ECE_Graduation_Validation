#####################################
# validate_schedule.py
# Author: Aidan McNay
#####################################
# Runs a list of checks on a Schedule
# to validate it for graduation

import schedule
from checks import *

class ScheduleChecker:
    """
    This class is an object whos jobs it to
    validate a schedule. It has three attributes:
     - schedule: The Schedule object that it's checking
     - class_list: A list of classes containted in the Schedule
         Note that this may not be a comprehensive list of all classes
         in the schedule at any given time. It is initialized as all of
         the classes in the schedule, but it is intended that check
         functions may remove classes from this list to indicate that
         they have been used to satisfy a requirement, and cannot be used
         further
     - checks: A list of functions that are contained in checks.py
        - check functions should only take a ScheduleChecker object as an 
          argument
        - the output of check functions should be an int that corresponds to
          the number of ERRORS (not warnings) that were found during the check.
          This should always be a positive number
    """

    def __init__(self, text_schedule_path, list_of_checks):
        self.schedule = schedule.Schedule(text_schedule_path)
        self.class_list = self.schedule.get_classes("ALL")
        self.checks = list_of_checks

    def validate(self):
        """
        Validates the given schedule with the checks provided
        """

        print("\n############################")
        print("VALIDATING SCHEDULE")
        print("############################\n")
        # Initial credits check
        print("Checking credits:")
        self.schedule.credit_limit()
        print("")

        # Run the checks
        num_errors = 0
        for check in self.checks:
            print("Running "+check.__name__+"...")
            num_errors += abs(check(self))
            print("")
        if num_errors==0:
            print("Congratulations! It looks like your class list satisfies all of our requirements!")
        else:
            print("Whoops - looks like you had "+str(num_errors)+" errors, please review these!")


#################################################

if __name__ == '__main__':

    list_of_checks = [
        has_commoncore,
        has_ececore,
        has_secondengrd,
        has_ecefoundations
    ]

    #USER: Change this if your text file is contained somewhere else
    schedule_path = "my_classes.txt"

    schedule_checker = ScheduleChecker(schedule_path, list_of_checks)
    schedule_checker.validate()