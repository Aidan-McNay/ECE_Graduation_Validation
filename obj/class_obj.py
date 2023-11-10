#=====================================================================
# class_obj.py
#=====================================================================
# An object representation of a Cornell class
#
# Author: Aidan McNay
# Date: October 2nd, 2023

import ui, api
import exceptions as excp

class Class:
    """
    Python representation of a Cornell class
    
    Attributes: (* designates derived properties, read-only)
                (_ designates only for internal use)

     - primary_name: The primary name of the class (str)
         ex. "ECE 2720"

     * department: The department of the class (str)
         ex. "ECE"

     * course_number: The course number of the course (str)
         ex. "2720"

     - title: The title of the class (short version) (str)

     - titleLong: The title of the class (long version) (str)

     - all_names: All names that the class goes by (set of str)

     * all_departments: Other departments that the class is listed in
       (set of str)

     * other_names: All names that the class goes by (set of str)

     * other_departments: Other departments that the class is listed in
       (set of str)

     - catalogDistr: Distribution categories of the class
       (if they exist) (list of str or None)
         ex. ["SBA-AS", "SSC-AS"]

     - acadGroup: The course's academic group (str)
         ex. "EN" (for Engineering)

     - acadCareer: The course's nominal program affiliation (str)
         ex. "UG" (for undergraduate)

     - credits: The number of credits you can take the class for (int)
       - Will prompt for input if number is variable

     - is_FWS: Whether the class is a FWS or not (bool)

     - term_taken: Term that the class was taken in

     - term_sourced: The term from which information was sourced (if
                     possible, the same as term_taken)

     - _enrl_idx: The index of the enrolled section (if only 1, set to 0)
    """

    def __init__( self, course_name, term = None ):
        """
        Sources the initial information for the class

        Args:
         - course_name: The name of the course (str)

         - term: The term the course was taken (will
                 prompt if not specified)
        """

        course_name = ui.parser.parse_class_name( course_name )

        if( term == None ):
            term = ui.user.prompt_term( course_name )
        else:
            term = ui.parser.parse_class_term( term )

        self.primary_name = course_name
        self.term_taken   = term

        # Grab the data for the course
        try:
          json_object = api.class_api.get_class( course_name, term )
          self.term_sourced = term

        except excp.api_exceptions.TermNotFoundError as e:
          if api.class_api.in_future( term ): # Find the next best term
            json_object, self.term_sourced = api.class_api.most_recent_term( course_name, term )
          else: # Not in the future, we just don't have info on it
            raise e
          
        self.set__enrl_idx   ( json_object )

        self.set_all_names   ( json_object )
        self.set_title       ( json_object )
        self.set_titleLong   ( json_object )
        self.set_catalogDistr( json_object )
        self.set_acadGroup   ( json_object )
        self.set_acadCareer  ( json_object )
        self.set_credits     ( json_object )
        self.set_is_FWS      ( json_object )

    #---------------------------------------------------------------------
    # Attribute setters
    #---------------------------------------------------------------------

    def set__enrl_idx( self, json_obj ):
        if ( len( json_obj[ "enrollGroups" ] ) == 1 ):
            self._enrl_idx = 0
            return
        # Otherwise, we need to prompt the user to choose
        prompt_msg = f"Looks like {self.course_name} has multiple sections - which one did you take?"
        options = [ x["classSections"][0]["section"] for x in json_obj[ "enrollGroups" ] ] # Use first section to identify enroll group
        sel_option = ui.user.prompt_usr_list( prompt_msg, options, 0 )
        self._enrl_idx = options.index( sel_option )

    def set_all_names( self, json_obj ):
        all_names = { self.primary_name }
        for crosslist in json_obj[ "enrollGroups" ][ self._enrl_idx ][ "simpleCombinations" ]:
            other_name = f"{crosslist[ 'subject' ]} {crosslist[ 'catalogNbr' ]}"
            all_names.add( other_name )
        self.all_names = all_names

    def set_title( self, json_obj ):
        self.title = json_obj[ "titleShort" ]

    def set_titleLong( self, json_obj ):
        self.titleLong = json_obj[ "titleLong" ]

    def set_catalogDistr( self, json_obj ):
        distr_string = json_obj[ "catalogDistr" ]
        distr_string = distr_string.strip( "()" ) # Strip off parenthesis
        self.catalogDistr = distr_string.split( ", " )

    def set_acadGroup( self, json_obj ):
        self.acadGroup = json_obj[ "acadGroup" ]

    def set_acadCareer( self, json_obj ):
        self.acadGroup = json_obj[ "acadCareer" ]

    def set_is_FWS( self, json_obj ):
        if( "FWS: " in json_obj[ "titleLong" ] ):
            self.is_FWS = True
            return
        
        if( ( "ENGL 2880" in self.all_names ) or ( "ENGL 2890" in self.all_names ) ):
            self.is_FWS = True # Counts for FWS credit
            return
        
        self.is_FWS = False

    def set_credits( self, json_obj ):
        max_cred = json_obj[ "enrollGroups" ][ self._enrl_idx ][ "unitsMaximum" ]
        min_cred = json_obj[ "enrollGroups" ][ self._enrl_idx ][ "unitsMinimum" ]
        if( max_cred == min_cred ):
            self.credits = max_cred
            return
        # If we got here, variable number of credits - prompt user
        prompt_msg = f"Looks like {self.course_name} has variable numbers of credits - how many did you take?"
        options = [ str( i ) for i in range( min_cred, max_cred + 1 ) ]
        self.credits = int( ui.user.prompt_usr_list( prompt_msg, options, 0 ) )
    
    #---------------------------------------------------------------------
    # Dynamic Properties
    #---------------------------------------------------------------------

    @property
    def department( self ):
        return ui.parser.get_dept_from_name( self.primary_name )
    
    @property
    def course_number( self ):
        return ui.parser.get_nbr_from_name( self.primary_name )
    
    @property
    def all_departments( self ):
        return { ui.parser.get_dept_from_name( i ) for i in self.all_names }
    
    @property
    def other_names( self ):
        cpy_to_return = self.all_names.copy()
        cpy_to_return.remove( self.primary_name )
        return cpy_to_return
    
    @property
    def other_departments( self ):
        return { ui.parser.get_dept_from_name( i ) for i in self.other_names }
    
    #---------------------------------------------------------------------
    # Member Functions
    #---------------------------------------------------------------------

    #---------------------------------------------------------------------
    # Overloaded Operators
    #---------------------------------------------------------------------

    def __str__( self ):
        str_repr  = self.primary_name + ": " + self.title
        str_repr += f" ({self.term_taken})"
        
        return str_repr

    def __eq__( self, other ):
        if not isinstance( other, Class ):
            return False
        return ( ( self.all_names == other.all_names ) and ( self.term_taken == other.term_taken ) )
    
    def __ne__( self, other ):
        return not ( self == other )
    
    def __len__( self ): # We'll use this for the number of credits
        return self.credits
       
