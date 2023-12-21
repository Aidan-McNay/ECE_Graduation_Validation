"""
#=====================================================================
# uchecks.py
#=====================================================================
# A collection of microchecks (uchecks), to be used by larger checks
#
# Each microcheck function returns a lambda that takes in a Class
# object, and returns a bool indicating whether the ucheck was passed
#
# Author: Aidan McNay
# Date: December 21st, 2023
"""

from typing import Callable, List

from obj.class_obj import Class

UcheckType = Callable[ [Class], bool ]

#---------------------------------------------------------------------
# is_dept
#---------------------------------------------------------------------

def is_dept( dept: str ) -> UcheckType:
    """
    Returns a lambda checking whether the given Class object is in
    the given department
    """

    return lambda x : dept in x.all_departments

#---------------------------------------------------------------------
# is_level
#---------------------------------------------------------------------

def is_level( level: int ) -> UcheckType:
    """
    Returns a lambda checking whether the given Class object is at
    or above the given level
    """

    return lambda x : int( x.course_number ) >= level

#---------------------------------------------------------------------
# is_name
#---------------------------------------------------------------------

def is_name( class_name: str ) -> UcheckType:
    """
    Returns a lambda checking whether the given Class object has the
    intended name
    """

    return lambda x : class_name in x.all_names

#---------------------------------------------------------------------
# is_names
#---------------------------------------------------------------------

def is_names( class_names: List[str] ) -> UcheckType:
    """
    Returns a lambda checking whether the given Class object has any
    of the possible names
    """

    return lambda x : any( name in x.all_names for name in class_names )
