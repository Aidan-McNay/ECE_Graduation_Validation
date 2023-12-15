# `checks`

This is a folder for the checks that are run on a student's Roster, to determine its validity

## Files

This folder includes:
 - `checks_manager.py`: A wrapper around many "check" functions, responsible for managing and calling them when needed
 - `common_core/`: Checks pertaining to the Engineering Common Core classes (run when the `-s` flag is supplied)
 - `credits_check.py`: A check to make sure that the credits reported for classes align with our records (run when the `-g` flag is supplied)
 - `grade_check.py`: A check to make sure that the grades reported for classes align with our records (run when the `-g` flag is supplied)
 - `utils/`: Utility functions useful across a variety of checks

## "Check" Functions

To obtain high code reusability and readability, all functions performing checks on a student's Roster must conform to the same function signature.
An example is given below for a check function named `check_func`

```
check_func( roster: obj.roster_obj.Roster, logger: logging.Logger ) -> Tuple[int, int]
```

The check must take in a student's Roster, as well as a Logger for logging the results. The check must return
a tuple of two ints; the first is the number of errors generated, and the second is the number of warnings. This
common interface allows checks to easily be managed by our ChecksManager.