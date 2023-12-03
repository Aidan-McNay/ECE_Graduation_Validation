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

import pandas as pd

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
        self.y = y
        self.x = x

    def up( self ):
        return Coordinates( self.y - 1, self.x )
    
    def down( self ):
        return Coordinates( self.y + 1, self.x )
    
    def left( self ):
        return Coordinates( self.y, self.x - 1 )
    
    def right( self ):
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

     - reqs: List of Requirement objects listed in the checklist
             (list of Requirements)
    """

    def __init__( self, file_path ):
        """
        Initializes the Checklist data, based off of the given file path
        """

        if( file_path.endswith( ".xlsx" ) ):
            dataframe = pd.read_excel( file_path )

        elif( file_path.endswith( ".csv" ) ):
            dataframe = pd.read_csv( file_path )

        else:
            assert False, "Error: Not a supported checklist file type. Please use a .xlsx or .csv file."

        self._data = ( dataframe.to_numpy() ).tolist()

    def find_cell( self, val, case_insensitive = True ):
        """
        Returns a list of Coordinates of cells with val (str) as a substring
        (returns a list of Coordinates)
        """

        result = []

        for row_idx, row in enumerate( self._data ):
            for column_idx, data_value in enumerate( row ):
                if ( ( val in str( data_value ) ) or ( case_insensitive and ( val.lower() in str( data_value ).lower() ) ) ):
                    result.append( Coordinates( row_idx, column_idx ) )

        return result
    
    def get_cell( self, coord ):
        """
        Returns the value of the cell at the given coordinates
        """

        return self._data[ coord.y ][ coord.x ]
    
    #---------------------------------------------------------------------
    # Dynamic Properties - Student Attributes
    #---------------------------------------------------------------------

    def get_student_attr( self, val, case_insensitive = True ):
        val_label = self.find_cell( val, case_insensitive )
        assert len( val_label ) == 1, f"Error: Multiple {val} found"

        coordinates = val_label[ 0 ]
        return self.get_cell( coordinates.right() )

    @property
    def first_name( self ):
        return self.get_student_attr( "First Name:" )
    
    @property
    def last_name( self ):
        return self.get_student_attr( "Last Name:" )
    
    @property
    def netid( self ):
        return self.get_student_attr( "NetID:" )
    
    @property
    def cuid( self ):
        return self.get_student_attr( "CUID:" )
    
    @property
    def advisor( self ):
        return self.get_student_attr( "Advisor:", False )
        
