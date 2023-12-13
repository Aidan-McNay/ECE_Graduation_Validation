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
 - `course`
 - `cred` (Credits)
 - `term`
 - `grade`
 - `cat` (when applicable)

### `CheckoffEntrys`

 - `req`
 - `course`