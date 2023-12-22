# `exceptions`

This is a folder for all exceptions that may be thrown across all functionality

## Files

This folder includes:
 - `api_exceptions.py`: Exceptions that may be thrown by our API functions, namely when interfacing with individual classes (in `api/class_api.py`)
 - `checklist_exceptions.py`: Exceptions that may be thrown by our Checklist object (in `obj/checklist_obj.py`)
 - `class_records_exceptions.py`: Exceptions that may be thrown by our Class Records, either an individual (in `obj/class_record_obj.py`) or a collection (in `obj/class_records_obj.py`)
 - `grade_exceptions.py`: Exceptions that may be thrown by our Grades object (in `obj/grades_obj.py`)
 - `ui_exceptions.py`: Exceptions that may be thrown by our UI functions, namely when parsing input (in `ui/parser.py`)

## Exceptions

A variety of exceptions may be thrown, with the emphasis being on handling unexpected scenarios as close to the user source as possible. These exceptions include:

 - `api_exceptions.py`:
    - `TermNotFoundError`: Indicates that the API doesn't have information on the given term
    - `DeptNotFoundError`: Indicates that the API doesn't have information on the given department for the specific term
    - `ClassNotFoundError`: Indicates that the API couldn't find the given class for the specific department and term
    - `NoClassInfoError`: Indicates that the API couldn't find the given class in any term _(this involves searching all terms, and is avoided in the current script due to the time penalty, but left in the source code for completion)_
 - `checklist_exceptions.py`:
    - `UnsupportedFileTypeError`: Indicates that an unsupported file type was provided (currently, only Excel spreadsheets with the `.xlsx` file extension are supported)
    - `MultipleAttributeError`: Indicates that a given attribute (such as a name or NetID) was found multiple times on the checklist
 - `class_records_exceptions.py`:
    - `RecordNotFoundError`: Indicates that we didn't find a record of the student taking a class in a given term
    - `InsufficientCreditsError`: Indicates that the student listed more credits for a class than they took it for
 - `grade_exceptions.py`:
    - `StudentNotFoundError`: Indicates that we don't have grade records for the given student
    - `TermNotFoundError`: Indicates that we don't have grade records in the given term for the specific student
    - `ClassNotFoundError`: Indicates that we don't have grade records for the given class for the specific student and term
 - `ui_exceptions.py`:
    - `InvalidClassNameError`: Indicates that the user supplied an invalid class name (not a recognized format)
    - `InvalidTermError`: Indicates that the user supplied an invalid term (not a recognized format)
    - `InvalidGradeError`: Indicates that the user supplied an invalid grade (not a recognized format)