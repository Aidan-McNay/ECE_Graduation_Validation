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

import pandas as pd
from dateutil import parser
from obj.roster_entry_obj import RosterEntry
from ui.parser import parse_class_name as pclass
from ui.parser import parse_class_term as pterm

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

    def __init__( self, y, x ):
        """Initializes the values"""
        self.y = y
        self.x = x

    def up( self ):
        """Returns the coordinates of the cell above"""
        return Coordinates( self.y - 1, self.x )

    def down( self ):
        """Returns the coordinates of the cell below"""
        return Coordinates( self.y + 1, self.x )

    def left( self ):
        """Returns the coordinates of the cell to the left"""
        return Coordinates( self.y, self.x - 1 )

    def right( self ):
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

     - exp_grad_term: The student's expected graduation term (str)

     - agreement_initials: Initials of student agreeing to 
                           validity (str)

     - agreement_date: Date of initials for agreement (datetime.datetime)

    Note that any subsequent parsers for different formats should additionally
    support these properties for access by other code, to ensure compatibility
    """

    def __init__( self, file_path ):
        """
        Initializes the Checklist data, based off of the given file path
        """

        if file_path.endswith( ".xlsx" ):
            dataframe = pd.read_excel( file_path )

        elif file_path.endswith( ".csv" ):
            dataframe = pd.read_csv( file_path )

        else:
            assert False, ( "Error: Not a supported checklist file type. " + \
                            "Please use a .xlsx or .csv file." )

        self._data = ( dataframe.to_numpy() ).tolist()

    def find_cell( self, val, case_insensitive = True ):
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

    def get_cell( self, coord ):
        """
        Returns the value of the cell (str) at the given coordinates
        """

        return str( self._data[ coord.y ][ coord.x ] )

    #---------------------------------------------------------------------
    # Dynamic Properties - Student Attributes
    #---------------------------------------------------------------------

    def get_student_attr( self, val, case_insensitive = True ):
        """Gets an attribute next to the given label (val)"""

        val_label = self.find_cell( val, case_insensitive )
        assert len( val_label ) == 1, f"Error: Multiple {val} found"

        coordinates = val_label[ 0 ]
        return self.get_cell( coordinates.right() )

    @property
    def first_name( self ):
        """Gets the first name of the student"""

        return self.get_student_attr( "First Name:" )

    @property
    def last_name( self ):
        """Gets the last name of the student"""

        return self.get_student_attr( "Last Name:" )

    @property
    def netid( self ):
        """Gets the NetID of the student"""

        return self.get_student_attr( "NetID:" )

    @property
    def cuid( self ):
        """Gets the CUID of the student"""

        return self.get_student_attr( "CUID:" )

    @property
    def advisor( self ):
        """Gets the advisor of the student"""

        return self.get_student_attr( "Advisor:" )

    # The remaining properties aren't directly next to the label, so
    # we must treat them separately

    @property
    def agreement_initials( self ):
        """Gets the agreement initials of the student"""

        initials_label = self.find_cell( "Student Initials" )
        assert len( initials_label ) == 1, "Error: Multiple Student Initials found"

        coordinates = initials_label[ 0 ]
        # The initials two cells to the right
        return self.get_cell( coordinates.right().right() )

    @property
    def agreement_date( self ):
        """Gets the agreement date of the student"""

        initials_label = self.find_cell( "Student Initials" )
        assert len( initials_label ) == 1, "Error: Multiple Student Initials found"

        coordinates = initials_label[ 0 ]
        # The date is four cells to the right
        return parser.parse( self.get_cell( coordinates.right().right().right().right() ) )

    @property
    def exp_grad_term( self ):
        """Gets the expected graduation date of the student"""

        term_label = self.find_cell( "Expected Graduation Term" )
        assert len( term_label ) == 1, "Error: Multiple Expected Graduation Term found"

        coordinates = term_label[ 0 ]
        # The date is three cells to the right
        return self.get_cell( coordinates.right().right().right() )

    #---------------------------------------------------------------------
    # Dynamic Properties - Roster Entries
    #---------------------------------------------------------------------

    @property
    def entries( self ):
        """Gets the entries in the checklist"""

        roster_entries = []

        # Get requirements
        entry_coords = self.find_cell( "REQ-" )

        for coord in entry_coords:
            req    = self.get_cell( coord )
            course = self.get_cell( coord.right() )
            cred   = self.get_cell( coord.right().right() )
            term   = self.get_cell( coord.right().right().right() )
            grade  = self.get_cell( coord.right().right().right().right() )

            course = pclass( course )
            term   = pterm( term )
            cred   = int( cred )

            if req.lower() == "REQ-LS".lower():
                cat = self.get_cell( coord.right().right().right().right().right() )
            else:
                cat = None

            roster_entries.append( RosterEntry( req, course, cred, term, grade, cat ) )

        # Get checkoffs
        roster_entries.append( RosterEntry( "CKOFF-ADVPROG",
                                            self.get_student_attr( "Adv. Programming" ) ) )

        roster_entries.append( RosterEntry( "CKOFF-TECHWRIT",
                                            self.get_student_attr( "Tech. Writing"    ) ) )

        return roster_entries

    #---------------------------------------------------------------------
    # Overloaded Operators
    #---------------------------------------------------------------------

    def __str__( self ):
        """String representation (for debugging)"""

        str_repr = ""
        str_repr += f"Checklist for {self.first_name} {self.last_name} ({self.netid})\n"

        for entry in self.entries:
            str_repr +=  ( " - " + str( entry ) + "\n" )

        return str_repr[:-1]
