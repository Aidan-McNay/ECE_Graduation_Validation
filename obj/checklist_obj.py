"""
#=====================================================================
# checklist_obj.py
#=====================================================================
# An object representation of an ECE Graduation Checklist
#
# Note this is meant to be a representation close to the physical
# spreadsheet, only to be converted into a Roster for later processing
#
# Author: Aidan McNay
# Date: December 2nd, 2023
"""

from typing import List
import datetime

import pandas as pd
from dateutil import parser

from obj.roster_entry_obj import RosterEntry, ReqEntry, CheckoffEntry
from ui.parser import parse_class_name as pclass, \
                      parse_class_term as pterm,  \
                      parse_grade      as pgrade
import exceptions as excp

#---------------------------------------------------------------------
# Coordinates Object
#---------------------------------------------------------------------
# Thin wrapper around 2D indeces, for improved readability (internal)

class Coordinates:
    """
    Attributes:

     - y: Row coordinate ( int )
     - x: Column coordinate ( int )

     0    1    2    3     
       ------------------> x
     1 |
       |
     2 |
       |
     3 |
       |
       v
       y
    """

    def __init__( self, y: int, x: int ):
        """Initializes the values"""
        self.y = y
        self.x = x

    def up( self ) -> 'Coordinates':
        """Returns the coordinates of the cell above"""
        return Coordinates( self.y - 1, self.x )

    def down( self ) -> 'Coordinates':
        """Returns the coordinates of the cell below"""
        return Coordinates( self.y + 1, self.x )

    def left( self ) -> 'Coordinates':
        """Returns the coordinates of the cell to the left"""
        return Coordinates( self.y, self.x - 1 )

    def right( self ) -> 'Coordinates':
        """Returns the coordinates of the cell to the right"""
        return Coordinates( self.y, self.x + 1 )

#---------------------------------------------------------------------
# Checklist Object
#---------------------------------------------------------------------
# Representation of a student's checklist

class Checklist:
    """
    Python representation of a student's checklist

    All of the data is simply kept as a 2D array of cells, taken from
    the spreadsheet. However, derived properties are also supported
    to make it easier for external code to access the data

    Attributes:

     - filepath: The filepath that the data was sourced from (str)

     - _data: The 2D array taken from the checklist spreadsheet
              (list of lists of str)

    Properties (dynamically derived):

     - first_name: First name of the student (str)

     - last_name: Last name of the student (str)

     - netid: NetID of the student (str)

     - cuid: CUID of the student (str)

     - advisor: Student's advisor (str)

     - entries: List of RosterEntry objects listed in the checklist
                for the satisfied requirements and checkoffs
                (list of RosterEntrys)

     - req_entries: List of ReqEntry objects listed in the checklist
                    for the satisfied requirements (list of ReqEntrys)

     - checkoff_entries: List of ReqEntry objects listed in the checklist
                         for the satisfied checkoffs (list of CheckoffEntrys)

     - exp_grad_term: The student's expected graduation term (str)

     - agreement_initials: Initials of student agreeing to 
                           validity (str)

     - agreement_date: Date of initials for agreement (datetime.datetime)

    Note that any subsequent parsers for different formats should additionally
    support these properties for access by other code, to ensure compatibility
    """

    def __init__( self, file_path: str ):
        """
        Initializes the Checklist data, based off of the given file path
        """
        self.filepath = file_path

        if file_path.endswith( ".xlsx" ):
            dataframe = pd.read_excel( file_path )

        elif file_path.endswith( ".csv" ):
            dataframe = pd.read_csv( file_path )

        else:
            raise excp.checklist_exceptions.UnsupportedFileTypeError( file_path )

        self._data = ( dataframe.to_numpy() ).tolist()

    def find_cell( self, val: str, case_insensitive: bool = True ) -> List[Coordinates]:
        """
        Returns a list of Coordinates of cells with val (str) as a substring
        (returns a list of Coordinates)
        """

        result = []

        for row_idx, row in enumerate( self._data ):
            for column_idx, data_value in enumerate( row ):
                if (                        ( val         in str( data_value )           ) or
                     ( case_insensitive and ( val.lower() in str( data_value ).lower() ) ) ):

                    result.append( Coordinates( row_idx, column_idx ) )

        return result

    def get_cell( self, coord: Coordinates ) -> str:
        """
        Returns the value of the cell (str) at the given coordinates
        """

        return str( self._data[ coord.y ][ coord.x ] )

    #---------------------------------------------------------------------
    # Dynamic Properties - Student Attributes
    #---------------------------------------------------------------------

    def get_student_attr( self, val: str, num_right: int, case_insensitive: bool = True ) -> str:
        """Gets an attribute next to the given label (val) a given number of spaces away"""

        val_label = self.find_cell( val, case_insensitive )
        if len( val_label ) != 1:
            raise excp.checklist_exceptions.MultipleAttributeError( val, len( val_label ) )

        coordinates = val_label[ 0 ]
        for _ in range( num_right ):
            coordinates = coordinates.right()

        return self.get_cell( coordinates )

    @property
    def first_name( self ) -> str:
        """Gets the first name of the student"""

        return self.get_student_attr( "First Name:", 1 )

    @property
    def last_name( self ) -> str:
        """Gets the last name of the student"""

        return self.get_student_attr( "Last Name:", 1 )

    @property
    def netid( self ) -> str:
        """Gets the NetID of the student"""

        return self.get_student_attr( "NetID:", 1 )

    @property
    def cuid( self ) -> str:
        """Gets the CUID of the student"""

        return self.get_student_attr( "CUID:", 1 )

    @property
    def advisor( self ) -> str:
        """Gets the advisor of the student"""

        return self.get_student_attr( "Advisor:", 1 )

    @property
    def agreement_initials( self ) -> str:
        """Gets the agreement initials of the student"""

        return self.get_student_attr( "Student Initials", 2 )

    @property
    def agreement_date( self ) -> datetime.datetime:
        """Gets the agreement date of the student"""

        return parser.parse( self.get_student_attr( "Student Initials", 4 ) )

    @property
    def exp_grad_term( self ) -> str:
        """Gets the expected graduation date of the student"""

        return self.get_student_attr( "Expected Graduation Term", 3 )

    #---------------------------------------------------------------------
    # Dynamic Properties - Roster Entries
    #---------------------------------------------------------------------

    @property
    def req_entries( self ) -> List[ReqEntry]:
        """Gets the requirement entries in the checklist"""

        req_entries: List[ReqEntry] = []

        # Get requirements
        entry_coords = self.find_cell( "REQ-" )

        for coord in entry_coords:
            req    = self.get_cell( coord )
            course = self.get_cell( coord.right() )
            cred   = self.get_cell( coord.right().right() )
            term   = self.get_cell( coord.right().right().right() )
            grade  = self.get_cell( coord.right().right().right().right() )

            # Parsing of user formatting
            req      = req.upper()
            course   = pclass( course )
            cred_num = int( cred )
            term     = pterm( term )
            grade    = pgrade( grade )

            if req.lower() == "REQ-LS".lower():
                cat = self.get_cell( coord.right().right().right().right().right() )
            else:
                cat = None

            req_entries.append( ReqEntry( req, course, cred_num, term, grade, cat ) )

        return req_entries

    @property
    def checkoff_entries( self ) -> List[CheckoffEntry]:
        """Gets the checkoff entries in the checklist"""

        checkoff_entries: List[CheckoffEntry] = []

        # Get checkoffs
        checkoff_entries.append( CheckoffEntry( "CKOFF-ADVPROG",
                                                self.get_student_attr( "Adv. Programming", 1 ) ) )

        checkoff_entries.append( CheckoffEntry( "CKOFF-TECHWRIT",
                                                self.get_student_attr( "Tech. Writing"   , 1 ) ) )

        return checkoff_entries

    @property
    def entries( self ) -> List[RosterEntry]:
        """Gets all entries in the checklist"""
        roster_entries: List[RosterEntry] = []

        roster_entries += self.req_entries
        roster_entries += self.checkoff_entries

        return roster_entries

    #---------------------------------------------------------------------
    # Overloaded Operators
    #---------------------------------------------------------------------

    def __str__( self ) -> str:
        """String representation (for debugging)"""

        str_repr = ""
        str_repr += f"Checklist for {self.first_name} {self.last_name} ({self.netid})\n"

        for entry in self.entries:
            str_repr +=  ( " - " + str( entry ) + "\n" )

        return str_repr[:-1]
