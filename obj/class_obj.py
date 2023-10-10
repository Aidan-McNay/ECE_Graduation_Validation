#=====================================================================
# class_obj.py
#=====================================================================
# An object representation of a Cornell class
#
# Author: Aidan McNay
# Date: October 2nd, 2023

import ui, api

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

        except api.api_exceptions.TermNotFoundError as e:
          if api.class_api.in_future( term ): # Find the next best term
            json_object, self.term_sourced = api.class_api.most_recent_term( course_name, term )
          else: # Not in the future, we just don't have info on it
            raise e
          
        self.set__enrl_idx   ( json_object )

        self.set_all_names   ( json_object )
        self.set_catalogDistr( json_object )
        self.set_acadGroup   ( json_object )
        self.set_acadCareer  ( json_object )
        self.set_credits     ( json_object )
        # self.set_is_FWS      ( json_object )

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

    def set_catalogDistr( self, json_obj ):
        distr_string = json_obj[ "catalogDistr" ]
        distr_string = distr_string.strip( "()" ) # Strip off parenthesis
        self.catalogDistr = distr_string.split( ", " )

    def set_acadGroup( self, json_obj ):
        self.acadGroup = json_obj[ "acadGroup" ]

    def set_acadCareer( self, json_obj ):
        self.acadGroup = json_obj[ "acadCareer" ]

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
       
