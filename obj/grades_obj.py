"""
#=====================================================================
# grades_obj.py
#=====================================================================
# An object representation of a student's grades
#
# Author: Aidan McNay
# Date: November 10th, 2023
"""

import csv
from typing import Optional, List, Dict, Union, cast

import exceptions as excp

#---------------------------------------------------------------------
# Grade Mapping
#---------------------------------------------------------------------

GRADE_MAPPING: Dict[str, float] = {
    "A+": 4.3,
    "A" : 4,
    "A-": 3.7,
    "B+": 3.3,
    "B" : 3,
    "B-": 2.7,
    "C+": 2.3,
    "C" : 2,
    "C-": 1.7,
    "D+": 1.3,
    "D" : 1,
    "D-": 0.7,
    "F" : 0
}

def grd_to_val( grd_str: str ) -> float:
    """Maps grades to values"""
    return GRADE_MAPPING[ grd_str ]

#---------------------------------------------------------------------
# Term Mapping
#---------------------------------------------------------------------

TERM_MAPPING: Dict[str, str] = {
    "spring" : "SP",
    "summer" : "SU",
    "fall"   : "FA",
    "winter" : "WI"
}

def term_str_convert( term_str: str ) -> str:
    """
    Converts a verbose term string to the simplified version
    Ex. 'Spring 2023' => 'SP23'
    """

    term_str = term_str.strip()

    letters = "".join( [ x for x in term_str if x.isalpha() ] )
    digits  = "".join( [ x for x in term_str if x.isdigit() ] )

    season = TERM_MAPPING[ letters.lower() ]
    year   = digits[-2:] # Last two

    return season + year

#---------------------------------------------------------------------
# Grades Object
#---------------------------------------------------------------------

class Grades:
    """
    Python representation of a student's grades

    Attributes:
     - _fields (list of str): A list corresponding to 
         the titles/headers of the columns in the CSV, if any

     - _grades (dict): A dictionary or the following format:

       {
          <student>: {
             <term>: {
                <class>: {
                    "num_credits": X,
                    "grade": X
                }
             }
          }
       }

        - student: The student's NetID (str)
        - term: The term name (ex. 'FA23') (str)
        - class: The class name (ex. 'ECE 2720') (str)
        - num_credits: The number of credits taken (int)
        - grade: The grade received (str)

    This main attritube is not meant to be accessed from the
    outside; rather, several member functions are provided to
    act as an interface
    """

    #---------------------------------------------------------------------
    # Initialization Functions
    #---------------------------------------------------------------------
    # These are only meant to be called on initialization, NOT from
    # outside the object

    def __init__( self, src_file: Optional[str] = None ):
        self._grades: Dict[str,Dict[str,Dict[str,Dict[str,Union[ str, int ]]]]] = {}

        if src_file is not None: # Load data
            with open( src_file, "r", encoding = "utf-8" ) as data:
                contents = csv.reader( data )

                self.set_fields( next( contents ) ) # First line

                for line in contents:
                    self.add_grade( line )

    def set_fields( self, line: List[str] ) -> None:
        """Sets the fields, for later slicing into the CSV"""

        self._fields = line

    def get_field( self, line: List[str], field: str ) -> str:
        """Returns the item from the column specified by the given field"""

        index = self._fields.index( field )
        return line[ index ]

    def add_grade( self, line: List[str] ) -> None:
        """Adds the grade from the given line"""

        netid      = self.get_field( line, "Netid"                )
        term_str   = self.get_field( line, "Academic Term Ldescr" )
        class_subj = self.get_field( line, "Subject"              )
        class_num  = self.get_field( line, "Catalog Nbr"          )
        cred       = self.get_field( line, "Unt Taken"            )
        grade_str  = self.get_field( line, "Official Grade"       )

        term  = term_str_convert( term_str )
        class_str = f"{class_subj} {class_num}"
        num_cred = int( cred )

        if not netid in self._grades:
            self._grades[ netid ] = {}

        if not term in self._grades[ netid ]:
            self._grades[ netid ][ term ] = {}

        self._grades[ netid ][ term ][ class_str ] = {
            "num_credits" : num_cred,
            "grade"       : grade_str
        }

    def add_grade_manual( self, netid: str, term: str, class_str: str,
                          num_cred: int, grade: str ) -> None:
        """
        Adds the grade data manually, using all the necessary values

        Used when copying data
        """

        if not netid in self._grades:
            self._grades[ netid ] = {}

        if not term in self._grades[ netid ]:
            self._grades[ netid ][ term ] = {}

        self._grades[ netid ][ term ][ class_str ] = {
            "num_credits" : num_cred,
            "grade"       : grade
        }

    #---------------------------------------------------------------------
    # Access Functions
    #---------------------------------------------------------------------
    # These are meant to be used to access the stored data, and should be
    # used from other modules

    def get_data( self, netid: str, term: str, class_str: str ) -> Dict[ str, Union[ str, int ] ]:
        """
        Returns data from when the student took the class

        Arguments:
         - netid:     (str)
         - term:      (str) Ex. 'SP23'
         - class_str: (str) Ex. 'ECE 2720'

        Returns a dictionary with the attributes "num_credits" (int) 
        and "grade" (str)
        """

        if not netid in self._grades:
            raise excp.grade_exceptions.StudentNotFoundError( netid )

        if not term in self._grades[ netid ]:
            raise excp.grade_exceptions.TermNotFoundError( netid, term )

        if not class_str in self._grades[ netid ][ term ]:
            raise excp.grade_exceptions.ClassNotFoundError( netid, term, class_str )

        return self._grades[ netid ][ term ][ class_str ]

    def get_credits( self, netid: str, term: str, class_str: str ) -> int:
        """Returns the number of credits a student took a class for"""

        # Indicate that we return an int for type safety
        return cast( int, self.get_data( netid, term, class_str )[ "num_credits" ] )

    def get_grade( self, netid: str, term: str, class_str: str ) -> str:
        """Returns the grade a student got in a class"""

        # Indicate that we return an str for type safety
        return cast( str, self.get_data( netid, term, class_str )[ "grade" ] )

    def when_taken( self, netid: str, class_str: str ) -> List[str]:
        """
        Determines when a student took a class (returning multiple terms
        if taken multiple times)

        Returns a list of term strings (ex. 'FA23') of when the student
        took the class
        """

        if not netid in self._grades:
            raise excp.grade_exceptions.StudentNotFoundError( netid )

        terms_taken = []

        for term in self._grades[ netid ]:
            if class_str in self._grades[ netid ][ term ].keys():
                terms_taken.append( term )

        return terms_taken

    #---------------------------------------------------------------------
    # Operator Overloading
    #---------------------------------------------------------------------

    def __add__( self, other: 'Grades' ) -> 'Grades':
        # Returns a new Grades object with all of the grades from the
        # two sources

        new_grades = Grades()
        for old_grades in [ self, other ]:
            for netid in old_grades._grades.keys():
                for term in old_grades._grades[ netid ].keys():
                    for class_str in old_grades._grades[ netid ][ term ].keys():
                        data = old_grades.get_data( netid, term, class_str )
                        # Indicate types for type safety
                        num_cred = cast( int, data[ "num_credits" ] )
                        grade    = cast( str, data[ "grade" ]       )

                        new_grades.add_grade_manual( netid,     \
                                                     term,      \
                                                     class_str, \
                                                     num_cred,  \
                                                     grade )

        return new_grades

    def __str__( self ) -> str:
        # Returns a string representation of the Grades, for debugging
        str_repr = ""

        for netid, terms in self._grades.items():
            str_repr += f"{netid}:\n"
            for term, classes in terms.items():
                for class_str in classes:
                    grade = self.get_grade( netid, term, class_str )

                    str_repr += f" - {class_str} ({term}): {grade}\n"

        return str_repr[:-1] # Exclude last newline
