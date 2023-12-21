"""
#=====================================================================
# tech_courses.py
#=====================================================================
# A ucheck to determine whether an ECE course is "technical"

# Author: Aidan McNay
# Date: December 21st, 2023
"""

from checks.utils.uchecks import UcheckType

nontech_courses = [
    "ECE 3600",
    "ECE 4999",
    "ECE 5830",
    "ECE 5870",
    "ECE 5880"
]

def is_technical() -> UcheckType:
    """
    Returns a lambda checking whether the given Class object is a technical
    ECE class
    """

    return lambda x : ( "ECE" in x.all_departments ) and \
                      not any( name in x.all_names for name in nontech_courses )
