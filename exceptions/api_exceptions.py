"""
#=====================================================================
# api_exceptions.py
#=====================================================================
# Exceptions that our API functions may need to throw
#
# Author: Aidan McNay
# Date: October 2nd, 2023
"""

class TermNotFoundError( Exception ):
    """
    Indicates that the requested term wasn't found by the API

    Attributes:
     - term: Term that wasn't found (str)
    """

    def __init__( self, term ):
        self.term = term

        err_msg = f"Information for {term} wasn't found by the API"
        super().__init__( err_msg )

class DeptNotFoundError( Exception ):
    """
    Indicates that the requested department wasn't found by the API

    Attributes:
     - dept: Department that wasn't found (str)
     - term: Term that the given department wasn't found in
    """

    def __init__( self, dept, term ):
        self.dept = dept
        self.term = term

        err_msg = f"Information on the {dept} department wasn't found by the API for {term}"
        super().__init__( err_msg )

class ClassNotFoundError( Exception ):
    """
    Indicates that the requested class wasn't found by the API

    Attributes:
     - course_name: Name of the course not found (str)
     - term: Term that the course wasn't found in (str)
    """

    def __init__( self, course_name, term ):
        self.course_name = course_name
        self.term        = term

        err_msg = f"The class {course_name} wasn't offered in {term}"
        super().__init__( err_msg )

class NoClassInfoError( Exception ):
    """
    Indicates that the requested class had a term specified in the future, but
    no previous offerings were found

    Attributes:
     - course_name: Name of the course not found (str)
     - term: The future term that was specified (str)
    """

    def __init__( self, course_name, term ):
        self.course_name = course_name
        self.term        = term

        err_msg = f"Intending to take {course_name} in {term}, but no previous iterations found"
        super().__init__( err_msg )
