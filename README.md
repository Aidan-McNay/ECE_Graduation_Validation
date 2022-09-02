# ECE_Graduation_Validation
This code validates a course schedule and ensures it follows Cornell ECE's requirements for graduation

## Components

* **validate_schedule.py**: This is the main script that takes in all of the information, data structures, and check functions, and runs them all on your schedule
* **schedule.py**: Helper implementations for the Class and Schedule classes
* **checks.py**: This is where all of the functions are that check a schedule to see whether it meets the ECE Department's requirements
* **my_classes.txt**: This is a user's defined class schedule from all of there semesters _(Users should edit this by adding/removing classes)_
  * Entries should be of the format <class_name>(<class_term>) or simply <class_name>
  * Ex. "ECE2720", "MATH1920(SP20)"
  * Formatting is fairly forgiving

To run, simply go into the directory and type `python validate_schedule.py`. This code runs on ECELinux, so all ECE students should be able to run it there without having to install any dependencies.
