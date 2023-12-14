# `obj`

This is a folder for (most of) the object representations used in the graduation validation code

## Files

This folder includes:
 - `checklist_obj.py`: A wrapper around a checklist, close to the physical spreadsheet
 - `class_obj.py`: A representation of a Cornell class; the data is sourced using the API
 - `class_record_obj.py`: A record of a class someone took, determined from their Grades
 - `class_records_obj.py`: A collection of ClassRecords
 - `coordinates_obj.py`: A coordinate used by Checklists for interacting with spreadsheets
 - `grades_obj.py`: A representation of grades for any number of users
 - `roster_entry_obj.py`: An entry in a student's Roster, such as a requirement (`ReqEntry`) or a checkoff (`CheckoffEntry`)
 - `roster_obj.py`: A student's Roster (similar to a checklist, but more abstract and less connected to the physical layout)

## Validity

In addition to the object representations, `roster_entry_obj.py` defines different validity levels for roster entry components:

 - `UNCHECKED`: The component has not been checked
 - `VALID`: The component is considered valid
 - `WARNING`: The component has a warning
 - `ERROR`: The component has an error

These different validity levels have different semantics when applying to different components:

### `ReqEntrys`

 - `req`
    - `VALID`: The requirement is satisfied by the given course
    - `WARNING`: The requirement isn't satisfied by the overall course collection (ex. fewer than 3 OTE's supplied), **_OR_** the requirement couldn't be fully validated due to other missing information
    - `ERROR`: The requirement isn't satisfied by the given course
 - `course`
    - `VALID`: A course was supplied
    - `ERROR`: No course was supplied
 - `cred` (Credits)
    - `VALID`: The course was taken for the given number of credits
    - `WARNING`: The course (across this and any other listings) was taken for more credits than reported
    - `ERROR`: The course (across this and any other listings) was taken for fewer credits than reported, or wasn't taken (no record)
 - `term`
    - `VALID`: The course was offered during the given term
    - `WARNING`: The course may or may not be offered in the given (future) term
    - `ERROR`: The course was not offered during the given term
 - `grade`
    - `VALID`: The reported grade matches our records
    - `WARNING`: No grade was reported
    - `ERROR`: The reported grade either doesn't match our records, or our records don't have an entry for the given class
 - `cat` (when applicable)
    - `VALID`: The category is a valid LS category **_AND_** matches the category of the class
    - `WARNING`: The category is a valid LS category, but we couldn't verify it against the class (offered in the future)
    - `ERROR`: The category isn't a valid LS category **_OR_** is doesn't match the category of the class

### `CheckoffEntrys`

 - `req`
    - `VALID`: The requirement is satisfied by the given course
    - `WARNING`: No course supplied
    - `ERROR`: The requirement isn't satisfied by the given course
 - `course`
    - `VALID`: The class was found in the requirement entries
    - `WARNING`: No course supplied
    - `ERROR`: The class wasn't found in the requirement entries

Running the code with the `-g` flag and supplying grades will validate `cred` and `term` components, whereas running with the
`-s` flag will validate `req`, `course`, `term`, and `cat` components