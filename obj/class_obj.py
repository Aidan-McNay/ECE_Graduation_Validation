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

     - primary_name: The primary name of the class (str)
         ex. "ECE 2720"

     * department: The department of the class (str)
         ex. "ECE"

     * course_number: The course number of the course (str)
         ex. "2720"

     - all_names: All names that the class goes by (list of str)

     * all_departments: Other departments that the class is listed in
       (list of str)

     * other_names: All names that the class goes by (list of str)

     * other_departments: Other departments that the class is listed in
       (list of str)

     - catalogDistr: Distribution categories of the class
       (if they exist) (list of str or None)
         ex. ["SBA-AS", "SSC-AS"]

     - acadGroup: The course's academic group (str)
         ex. "EN" (for Engineering)

     - credits: The number of credits you can take the class for (int)
       - Will prompt for input if number is variable

     - is_FWS: Whether the class is a FWS or not (bool)

     - term_taken: Term that the class was taken in

     - term_sourced: The term from which information was sourced (if
                     possible, the same as term_taken)

     - section: The section of the course selected. If there is
       only one section, this is set to None
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
            term = ui.parser.parse_term_name( term )

        self.primary_name = course_name
        self.term_taken   = term

        # Grab the data for the course
        try:
          json_object = api.class_api.get_class( course_name, term )

        except api.api_exceptions.TermNotFoundError as e:
          if api.class_api.is_future( term ): # Find the next best term
            json_object = api.class_api.most_recent_term( course_name, term )
          else: # Not in the future, we just don't have info on it
            raise e
        