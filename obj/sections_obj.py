"""
#=====================================================================
# sections_obj.py
#=====================================================================
# An object representation of the section a student enrolled in for
# different classes
#
# Author: Aidan McNay
# Date: January 11th, 2024
"""

import csv
from typing import Optional, List, Dict, Tuple

from obj.class_obj import Class
import ui.parser

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

class Sections:
    """
    Python representation of a student's section enrollment

    Attributes:
     - _fields (list of str): A list corresponding to 
         the titles/headers of the columns in the CSV, if any
         Note: this attribute is not meant to be relied on beyond
         initialization, and its presence should not be assumed

     - _sections (dict): A dictionary or the following format:

       {
          <student>: {
             <term>: {
                <class>: <section>
             }
          }
       }

        - student: The student's NetID (str)
        - term: The term name (ex. 'FA23') (str)
        - class: The class name (ex. 'ECE 2720') (str)
        - section: The section the student enrolled in (str)

     - _aliases: A dictionary converting class strings and the
                 corresponding term to the class name alias in
                 _grades, if any (dict converting (term, class) to str)

    This main attritube is not meant to be accessed from the
    outside; rather, several member functions are provided to
    act as an interface.
    """

    #---------------------------------------------------------------------
    # Initialization Functions
    #---------------------------------------------------------------------
    # These are only meant to be called on initialization, NOT from
    # outside the object

    def __init__( self, src_file: Optional[str] = None ):
        self._sections: Dict[str,Dict[str,Dict[str,str]]] = {}
        self._aliases: Dict[ Tuple[ str, str ], str ] = {}

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
        section    = self.get_field( line, "Class Section"        )

        term  = term_str_convert( term_str )
        class_str = f"{class_subj} {class_num}"

        # Run through the parser, just to make sure :)
        class_str = ui.parser.parse_class_name( class_str )
        term      = ui.parser.parse_class_term( term      )

        if not netid in self._sections:
            self._sections[ netid ] = {}

        if not term in self._sections[ netid ]:
            self._sections[ netid ][ term ] = {}

        self._sections[ netid ][ term ][ class_str ] = section

    def add_section_manual( self, netid: str, term: str, class_str: str,
                          section: str ) -> None:
        """
        Adds the grade data manually, using all the necessary values

        Used when copying data
        """

        if not netid in self._sections:
            self._sections[ netid ] = {}

        if not term in self._sections[ netid ]:
            self._sections[ netid ][ term ] = {}

        self._sections[ netid ][ term ][ class_str ] = section

    def populate_aliases( self ) -> None:
        """Populates class alias data based on API data"""

        for _, terms in self._sections.items():
            for term, classes in terms.items():
                for class_str in classes:
                    class_obj = Class( class_str, term )

                    for name in class_obj.all_names:
                        self._aliases[ ( term, name ) ] = class_str

    #---------------------------------------------------------------------
    # Access Functions
    #---------------------------------------------------------------------
    # These are meant to be used to access the stored data, and should be
    # used from other modules

    def get_alias( self, term: str, class_str: str ) -> str:
        """Gets the alias of a class in a given term, if it exists"""
        if ( term, class_str ) in self._aliases:
            return self._aliases[ ( term, class_str ) ]

        # Alias isn't present
        return class_str

    def get_section( self, netid: str, term: str, class_str: str ) -> str:
        """
        Returns the section a student enrolled in a class for (str)

        Arguments:
         - netid:     (str)
         - term:      (str) Ex. 'SP23'
         - class_str: (str) Ex. 'ECE 2720'

        If the student didn't enroll for the given class or in the given
        term, simply return an empty string
        """

        class_str = self.get_alias( term, class_str )

        if not netid in self._sections:
            return ""

        if not term in self._sections[ netid ]:
            return ""

        if not class_str in self._sections[ netid ][ term ]:
            return ""

        return self._sections[ netid ][ term ][ class_str ]

    #---------------------------------------------------------------------
    # Operator Overloading
    #---------------------------------------------------------------------

    def __add__( self, other: 'Sections' ) -> 'Sections':
        # Returns a new Sections object with all of the grades from the
        # two sources

        new_sections = Sections()
        for old_sections in [ self, other ]:
            for netid in old_sections._sections:
                for term in old_sections._sections[ netid ]:
                    for class_str in old_sections._sections[ netid ][ term ]:
                        section = old_sections._sections[ netid ][ term ][ class_str ]

                        new_sections.add_section_manual( netid,     \
                                                       term,      \
                                                       class_str, \
                                                       section )

        return new_sections

    def __str__( self ) -> str:
        # Returns a string representation of the Sections, for debugging
        str_repr = ""

        for netid, terms in self._sections.items():
            str_repr += f"{netid}:\n"
            for term, classes in terms.items():
                for class_str in classes:
                    section = self.get_section( netid, term, class_str )

                    str_repr += f" - {class_str} ({term}): {section}\n"

        return str_repr[:-1] # Exclude last newline

#---------------------------------------------------------------------
# Global Accessors
#---------------------------------------------------------------------

_SECTIONS = Sections()

def add_section_data( file_path: str ) -> None:
    """Adds Sections data from the given grade CSV"""
    global _SECTIONS
    _SECTIONS = _SECTIONS + Sections( file_path )

def get_section( netid: str, term: str, class_str: str ) -> str:
    """Gets the section for the given class instance from the global data"""
    return _SECTIONS.get_section( netid, term, class_str )
