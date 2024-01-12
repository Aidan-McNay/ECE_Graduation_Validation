"""
#=====================================================================
# class_exceptions.py
#=====================================================================
# Exceptions that our Class object may need to throw
#
# Author: Aidan McNay
# Date: January 12th, 2024
"""

from typing import List

class SectionNotFoundError( Exception ):
    """
    Indicates that we didn't find the recorded section in our API data

    Attributes:
     - course_name: Name of the course (str)
     - term: Term of the course (str)
     - section_reported: Section that our data indicate (str)
     - sections_found: The sections in th API data (List of str)
    """

    def __init__( self, course_name: str, term: str,
                  section_reported: str, sections_found: List[str] ):
        self.course_name      = course_name
        self.term             = term
        self.section_reported = section_reported
        self.sections_found   = sections_found

        self.err_msg =  f"No record of section {section_reported} for {course_name} in {term}\n"
        self.err_msg += f" - Sections found: {', '.join( sections_found )}"
        super().__init__( self.err_msg )
