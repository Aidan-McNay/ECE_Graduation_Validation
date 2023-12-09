"""
#=====================================================================
# coordinates_obj.py
#=====================================================================
# An object representation of 2D Coordinates (for indexing 
# spreadsheets)
#
# Author: Aidan McNay
# Date: December 8th, 2023
"""

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

    def __eq__( self, other: object ) -> bool:
        """Returns whether the coordinates are equal"""
        if not isinstance(other, Coordinates):
            return NotImplemented
        return ( ( self.x == other.x ) and ( self.y == other.y ) )

    def __str__( self ) -> str:
        return f"({self.x}, {self.y})"

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
