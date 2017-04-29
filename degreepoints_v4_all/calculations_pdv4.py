"""
Module that defines the Data classe for degreepoints.v4
Includes helper functions for file handling

This class manages all calculations in degreepoints.v4

Author: Alasdair Smith
Started: 15 October 2016
Status: Incomplete
"""

from main_gui_pdv4 import UniCourse #For test cases only
from file_toolkit import open_string_txt
from aspect_pdv4 import *


class Data:
    """
    Defines the Data class for degreepoints.v4
    
    Tell the nice reader of this docstring what this all does Mr Smith!
    """
    
    def __init__(self, gui_results):
        """Initialises components of the gui_results object that are needed for
        calculations into this class, then calls the main calculations method"""
        self.degree = gui_results.degree_chosen
        self.is_double_major = gui_results.is_double_major
        self.major = gui_results.major
        self.major2 = gui_results.major2
        self.user_courses = gui_results.user_courses_dict
        self.all_courses_dict = gui_results.all_courses_dict
        
        self.calculations()
    
    
    def check_prerequisites(self):
        """Checks the prerequisite set against the courses the user has entered
        Assigns a set of prerequisite courses the user has not completed"""
        self.courses_not_completed = self.prerequisite_set - set(self.user_courses.keys())
    
    
    def calculations(self):
        """Runs all the calculation methods as required"""
        self.prerequisite_set = get_prerequisites(self.major, self.major2)
        self.check_prerequisites()
        self.get_requirements_for_majors()
    
    
    def get_requirements_for_majors(self):
        """Creates a dictionary with each major as its keys and Requirement
        objects for each value"""
        self.requirements_dict = {}
        self.major1_requirements = open_requirements(self.degree, self.major2)
        major1_requirement_set = interpret_point_requirements(self.major1_requirements)
        self.requirements_dict[self.major] = major1_requirement_set
        if self.major2 is not None:
            self.major2_requirements = open_requirements(self.degree, self.major2)
            major2_requirement_set = interpret_point_requirements(self.major2_requirements)
            self.requirements_dict[self.major2] = major2_requirement_set
        else:
            self.requirements_dict[self.major2] = set()
        
        
        #all_requirements = self.major1_requirements | self.major2_requirements
        #self.requirements_dict = interpret_point_requirements(all_requirements)


def interpret_point_requirements(requirements):
    """Takes a set of requirements as strings and creates Requirement objects
    Returns a set of Requirement objects"""
    requirements_for_major_set = set()
    for string in sorted(requirements):
        requirement_object = interpret_requirement(string)
        requirements_for_major_set.add(requirement_object)
    return requirements_for_major_set


def interpret_requirement(string):
    """Disassembles a string and creates a Requirement object
    The string (separated by spaces) is made up of:
    - The number of points required (3 digits) and the word 'points'
    - 'in', 'at', 'max' or 'overall'
    - [major], [{a degree}], [non-{a degree}]
    - Hundred levels (3 digits) seperated by 'and'. Followed by 'level'
    """
    string_list = split(string, sep=' ')
    
    requirement = Requirement(points, degree, majors, levels, max_non_degree)
    return requirement


def open_requirements(degree, major):
    """Opens the requirements file for a major in the degree chosen
    returns a set of requirements"""
    return set()


def get_prerequisites(major1, major2):
    """Opens the prerequisite courses for a degree with the chosen majors
    Returns a set of UniCourse objects"""
    file_prefix = "prereq_"
    file1 = major1.lower()
    major1_prereq_lines = open_string_txt(file1, prefix=file_prefix)
    if major2 is not None:
        file2 = major2.lower()
        major2_prereq_lines = open_string_txt(file2, prefix=file_prefix)
    else:
        major2_prereq_lines = []
    #In file, courses are defined from line 3, hence the index:
    prerequisite_courses = set(major1_prereq_lines[2:]) | set(major2_prereq_lines[2:])
    return prerequisite_courses











class Test_gui_results:
    """Class to provide figures that test the Data class and its methods"""
    def __init__(self, test_num):
        """Initialises some test data, depending on test number"""
        if test_num == 1:
            self.degree_chosen = "Science"
            self.is_double_major = True
            self.major = "Computer Science"
            self.major2 = "Mathematics"
            self.user_courses_dict = {
                "COSC121": UniCourse("COSC121", "Introduction to Computer Science"),
                "MATH120": UniCourse("MATH120", "Discrete Mathematics")
                }
        self.all_courses_dict = {
            "COSC121": UniCourse("COSC121", "Introduction to Computer Science"),
            "MATH120": UniCourse("MATH120", "Discrete Mathematics"),
            "MATH101": UniCourse("MATH101", "Methods of Mathematics")
            }


def main():
    """To test"""
    if __name__ == "__main__":
        gui = Test_gui_results(1)
        data = Data(gui)
        print("Courses not completed:")
        print(data.courses_not_completed)
        print("Requirements:")
        print(data.requirements_dict)


main()