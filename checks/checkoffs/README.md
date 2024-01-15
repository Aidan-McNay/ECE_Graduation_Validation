# `checkoffs`

This is a folder for making sure that a student has taken classes satisfying the ECE checkoffs

## Files

This folder includes:
 - `adv_prog.py`: A check for verifying the `ADV. PROGRAMMING` (Advanced Programming) checkoff
 - `checkoffs_check.py`: A wrapper around all Checkoff checks, to be used by a `ChecksManager`
 - `course_in_reqs.py`: Utility functions for verifying whether a class used for a checkoff was present elsewhere in the checklist (and to get the relevant ReqEntry)
 - `tech_writ.py`: A check for verifying the `TECH. WRITING` (Technical Writing) checkoff
 - `validate_checkoff.py`: A utility function used to verify a generic checkoff with uchecks (modeled after `checks/utils/basic_check.py`)