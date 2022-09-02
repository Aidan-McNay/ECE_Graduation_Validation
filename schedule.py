#####################################
# schedule.py
# Author: Aidan McNay
#####################################
# Implements the "Class" and
# "Schedule" classes

import json, requests, copy


def get_rosters():
  """
  Get the current rosters that the Cornell class API has data for
  Returns a list of the roster codes. If unable to get, returns
  -1
  """
  url = "https://classes.cornell.edu/api/2.0/config/rosters.json"
  try:
    list_of_rosters = []
    json_data = requests.get(url).text
    json_object = json.loads(json_data)
    rosters = (json_object["data"])["rosters"]
    for roster in rosters:
      list_of_rosters.append(roster["slug"])
    return list_of_rosters
  except:
    return -1


def parse_name(ugly_name):
    """
    Parses non-optimal user input into a usable class name for making
    API requests.

    Ex. " ecE2720" -> "ECE 2720"
    """
    less_ugly_name = ugly_name.strip()

    letters = [x for x in less_ugly_name if x.isalpha()]
    digits = [x for x in less_ugly_name if x.isdigit()]

    return ("".join(letters)).upper()+" "+"".join(digits)

def parse_term(ugly_term):
    """
    Parses non-optimal user input into a usable term ID

    Ex. " fA '2 2" -> "FA22"
    """
    less_ugly_term = ugly_term.strip()

    letters = [x for x in less_ugly_term if x.isalpha()]
    digits = [x for x in less_ugly_term if x.isdigit()]

    return ("".join(letters)).upper()+"".join(digits)

def term_index(term):
  """
  Returns a value for each term such that chronologically later
  terms will have higher values than terms that come before
  """

  term_season = "".join([x for x in term if x.isalpha()])
  term_year = int("".join([x for x in term if x.isdigit()]))

  seasons = {
    "WI": 0,
    "SP": 0.25,
    "SU": 0.5,
    "FA": 0.75
  }

  assert (term_season in list(seasons.keys())), (term+" is not a valid term")

  return (term_year + seasons[term_season])

class Class: #Lol
    """
    Python representation of a Cornell class
    
    Attributes:
     - primary_name: The primary name of the class (str)
         ex. "ECE 2720"
     - department: The department of the class (str)
         ex. "ECE"
     - course_number: The course number of the course (str)
         ex. "2720"
     - other_names: Other names that the class goes by (list of str)
     - other_departments: Other departments that the class is listed in
       (list of str)
     - catalogDistr: Distribution categories of the class
       (if they exist) (list of str or None)
         ex. ["SBA-AS", "SSC-AS"]
     - acadGroup: The course's academic group
         ex. "EN" (for Engineering)
     - credits: The number of credits you can take the class for (int)
       - Will prompt for input if number is variable
     - is_FWS: Whether the class is a FWS or not (bool)
     - source_term: Term that the class data was sourced from
     - section: The section of the course selected. If there is
       only one section, this is set to None
    """

    def __init__(self, course_name, term = "NULL"):
      """
      Finds the class with the given name in the database, and creates an instance of it.
      Unfortunately, we can't get a global definition of the class. To get around this,
      we query for the class in all rosters (working backwards in time) until we get a match,
      and take this to be the most up-to-date (and accurate) class
      """
      pretty_name = parse_name(course_name)
      self.primary_name = pretty_name
      self.department = pretty_name[:pretty_name.index(" ")]
      self.course_number = pretty_name[pretty_name.index(" ")+1:]
      self.other_names = []
      self.other_departments = []

      # Alright here's where it gets ugly - loop over all rosters, checking if the class is in them
      list_of_rosters = get_rosters() 
      list_of_rosters.reverse() # Iterate from most recent all the way back
      if(list_of_rosters==-1):
        assert False, "Uh oh - was unable to connect to the API"

      user_term = parse_term(term)
      if user_term in list_of_rosters:
        # Just use the correct term
        list_of_rosters = [user_term]
      
      roster_index = 0
      found_class = False
      while not found_class:
        # Check to see if we've gone over
        if(roster_index >= len(list_of_rosters)):
          error_message = "Sorry - can't find any record of a class named "+self.primary_name
          if (term!="NULL"):
            error_message = error_message + " in term "+user_term
          assert False, error_message
        roster_id = list_of_rosters[roster_index]
        roster_index += 1

        url = "https://classes.cornell.edu/api/2.0/search/classes.json?roster="+roster_id+"&subject="+self.department+"&q="+self.course_number
        json_data = requests.get(url).text
        json_object = json.loads(json_data)
        
        # This searches for the class that semester
        # - If found, the "status" attribute is "success"
        # - If not found, the "status" attribute is "error"

        if(json_object["status"]=="success"):
          # We searched for classes, and could have multiple results, 
          # so we should still verify that we have the correct class
          classes = (json_object["data"])["classes"]
          for cornell_class in classes:
            if(cornell_class["subject"]==self.department and cornell_class["catalogNbr"]==self.course_number):
              # We found the class!
              found_class = True
              self.source_term = roster_id

              # Handle multiple classes listed under this
              if (len(cornell_class["enrollGroups"])>1):
                valid_input = False
                while not valid_input:
                  print("Which section did you enroll in for "+self.primary_name+" in "+user_term+"?")
                  index = 0
                  sections = {}
                  for section in cornell_class["enrollGroups"]:
                    # Stores section number as key for the section's index
                    sections[((section["classSections"])[0])["section"]] = index
                  print("Options are "+", ".join(list(sections.keys())))
                  user_input = input()
                  if user_input in list(sections.keys()):
                    section_index = sections[user_input]
                    valid_input = True
                    self.section = user_input
                  else:
                    print("Whoops - invalid section, try again")
              else:
                section_index = 0
                self.section = None


              # Get other names of the class
              other_names = ((cornell_class["enrollGroups"])[section_index])["simpleCombinations"]
              for other_name in other_names:
                # Form the name, then append
                name = other_name["subject"]+" "+other_name["catalogNbr"]
                self.other_names.append(name)
                self.other_departments.append(other_name["subject"])
              
              self.acadGroup = cornell_class["acadGroup"]
              min_credits = ((cornell_class["enrollGroups"])[section_index])["unitsMinimum"]
              max_credits = ((cornell_class["enrollGroups"])[section_index])["unitsMaximum"]
              if min_credits==max_credits:
                self.credits = min_credits
              else:
                credits_determined = False
                while not credits_determined:
                  reported_credits = int(input("How many credits did you take "+self.primary_name+" for? (Between "+str(min_credits)+" and "+str(max_credits)+")\n"))
                  if (reported_credits>=min_credits and reported_credits<=max_credits):
                    self.credits = reported_credits
                    credits_determined = True
                  else:
                    print("Please choose a valid number of credits")
              
              # Get distributions
              distribution_string = cornell_class["catalogDistr"]
              if(distribution_string==""):
                # No listed distributions
                self.catalogDistr = None
              else:
                self.catalogDistr = (distribution_string.strip("()")).split(", ")

              # See if it's a FWS or not
              if( ((cornell_class["enrollGroups"])[section_index])["sessionCode"]=="FWS" ):
                self.is_FWS = True
              else:
                self.is_FWS = False

              
              
              break # Don't need to search the other classes for the correct class
    def __str__(self):
      """
      Gives the class in a user-friendly string
      Useful for printing/debugging
      """
      class_string = ""
      class_string += "***********************\n"
      class_string += ("Class Name: "+self.primary_name+"\n")
      if(self.section!=None):
        class_string += "Section "+self.section+"\n"
      for other_name in self.other_names:
        class_string += (" - "+other_name+"\n")
      class_string += (str(self.credits)+" credit(s)\n")
      if (self.is_FWS):
        class_string += "Is a FWS\n"
      if(self.catalogDistr==None):
        pass
      else:
        class_string += "Distributions: "
        for distribution in self.catalogDistr:
          class_string += distribution
          if distribution != self.catalogDistr[-1]: # Not the last element
            class_string += ", "
        class_string += "\n"
      class_string += ("Academic Group: "+self.acadGroup+"\n")
      class_string += "***********************"
      return class_string

    def __eq__(self, other_class):
      """
      Determines if the given classes are the same, 
      and returns the appropriate bool
      """
      name_to_compare = parse_name(other_class.primary_name)
      return( (self.primary_name==name_to_compare) or (name_to_compare in self.other_names))

    # Here, we define the comparison operators to check the course number
    def __lt__(self, class_level):
      return (int(self.course_number) < class_level)

    def __le__(self, class_level):
      return (int(self.course_number) <= class_level)

    def __gt__(self, class_level):
      return (int(self.course_number) > class_level)

    def __ge__(self, class_level):
      return (int(self.course_number) >= class_level)

    def same_name(self, other_name):
      """
      Determines if the given class name can describe the class
      (i.e. it's either the class' primary name or one of its
      other names), and returns the appropriate bool
      """
      name_to_compare = parse_name(other_name)
      return( (self.primary_name==name_to_compare) or (name_to_compare in self.other_names))

class Schedule:
    """
    This class is meant to represent an entire student schedule.
    It contains one attribute; a dictionary mapping terms to lists
    of classes (the upside for organizing by term being that
    visualization of the schedule is easier, as well as for possible
    future checks on credit limits and prerequisites)

    Attributes:
     - schedDict: a dictionary where terms that classes were taken
       correspond to keys, with the value being a list of Class
       objects that were taken during that term
    """
    def __init__(self, text_schedule_path):
      """
      Initializes the Schedule object from a text file of Classes
      Each Class should be on a separate line, and be formatted
      like so: <class_name>(<year>)
       - <class_name> is the name of the class
       - <year> is the year you have/plan on taking the class
     Note that the code shouldn't rely on knowing what year you will
     take a class, so if only <class_name> is given, it will be categorized
     under "NAY" for "No Assigned Year"
     """
      self.schedDict = {}
     
      f = open(text_schedule_path, "r")
      # Don't use blank lines, eliminate \newline
      lines = [line for line in f.readlines() if line.strip()]
      f.close()
      for class_bit in lines:
        self.add_class(class_bit)

    def add_class(self, class_bit):
      """
      Adds a class to the schedule.

      class_bit is either of the form <class_name>(<year>)
      of simply <class_name>

      ex. "ece2720", "Math 1920( fA '22)"
      """

      if "(" in class_bit:
        # Term was given
        class_name = class_bit[:class_bit.index("(")]
        termID = class_bit[class_bit.index("(")+1:class_bit.index(")")]
      else:
        # Term wasn't given
        class_name = class_bit
        termID = "NAY"
      
      # Account for wacky inputs
      class_name = parse_name(class_name) # Reduntant, but nice for print statements
      termID = parse_term(termID)

      print("Adding "+class_name+" to schedule...")
      class_to_add = Class(class_name)
      if termID in self.schedDict:
        (self.schedDict[termID]).append(class_to_add)
      else:
        self.schedDict[termID] = [class_to_add]

    def get_classes(self, user_term):
      """
      Returns a list of the classes corresponding to the given term.
      If the argument "ALL" is given, will return a list of 
      all classes stored in the schedule with no term information
      """
      term = parse_term(user_term)
      assert (term=="ALL" or term in list(self.schedDict.keys())), (term+" is not a valid term")
      if term!="ALL":
        return copy.deepcopy(self.schedDict[term])
      else:
        list_of_classes = []
        for key in self.schedDict:
          list_of_classes += self.schedDict[key]
        return copy.deepcopy(list_of_classes)

    def __str__(self):
      """
      Defines a string representation for the Schedule, for ease of printing
      """

      list_of_terms = list(self.schedDict.keys())
      # We need to organize this in chronological order
      sorted_terms = sorted(list_of_terms, key = term_index)

      string_to_return = ""
      
      string_to_return += "###############################\n"
      for term in sorted_terms:
        string_to_return += (term+":\n")
        for cornell_class in self.schedDict[term]:
          string_to_return += (" - "+cornell_class.primary_name+"\n")
      string_to_return += "###############################"
      return string_to_return

    def credit_limit(self):
      """
      A preliminary validation for a Schedule. Currently, it
      checks each semester to see if you're over the credit limit
      on any of them (which, at time of writing, is 20). It won't
      throw errors if there are violations (especially given the recent
      changes), but will notify the user
      """
      list_of_terms = list(self.schedDict.keys())
      sorted_terms = sorted(list_of_terms, key = term_index)
      for term in sorted_terms:
        cornell_classes = self.schedDict[term]
        total_credits = 0
        for cornell_class in cornell_classes:
          total_credits += cornell_class.credits
        print(term+": "+str(total_credits)+" credits")
        if total_credits > 20:
          print("  WARNING: This is over the current credit limit of 20 credits")
          print("  Make sure this is approved by your advisor beforehand")

