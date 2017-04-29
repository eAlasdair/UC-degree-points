"""
Module that defines the UniCourse class and the MainGui class for degreepoints.v4
includes helper functions to open files

Author: Alasdair Smith
Started: 11 October 2016
Completed: 16 October 2016
Status: Functional, aesthetic details need work

Will add predictive writing to course combobox once I figure out how to do so
"""

from tkinter import *
from tkinter.ttk import *
from file_toolkit import open_string_txt

class UniCourse:
    """Defines the university course object
    Data attributes:
        course_id (eg: MATH120) of type 'str'
        course_title (eg: 'Discrete Mathematics') of type 'str'
        points_worth (default 15) of type 'int'
    Methods:
    __init__()
    __repr__()
    """
    def __init__(self, course_id, course_title, points_worth=15):
        """Sets up the UniCourse object"""
        self.course_id = course_id
        self.course_title = course_title
        self.points = int(points_worth)
    
    def __repr__(self):
        """Defines how the course object is to be displayed:
        [course code]: [course title]"""
        return "{0:<7}: {1:<38}{2:>5}".format(self.course_id, self.course_title, self.points)


class MainGui:
    """Defines the main GUI class for degreepoints.v4
    
    Creates a GUI with multiple combobox and button questions used to build a
    map of the user's degree, majors and all courses they have completed.
    Upon finishing the form, the user presses the SUBMIT ALL button, which closes
    the GUI so that the program can continue.
    """
    def __init__(self, window, start_message, accepted_degrees):
        """Sets up the main gui by calling setup_subgui_1, which in turn calls the
        others as the user completes the form.
        Before this, initialises all display labels to avoid
        repeated user input creating overlap"""
        self.window = window
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame5 = Frame(self.window)
        
        self.start_message = start_message
        self.accepted_degrees = accepted_degrees
        
        self.main_label = Label(self.frame1, text=self.start_message)
        self.degree_chosen_label = Label(self.frame2)
        self.error_majors_label = Label(self.frame3)
        self.majors_chosen_label = Label(self.frame3)
        self.enter_all_courses_label = Label(self.frame4)
        self.error_courses_label = Label(self.frame4)
        self.user_courses_label = Label(self.frame4)
        
        self.major_combobox = Combobox(self.frame3)
        self.first_major_combobox = Combobox(self.frame3)
        self.second_major_combobox = Combobox(self.frame3)
        
        self.user_courses_dict = {}
        self.courses_entered = []
        self.submit_button_pushed = False
        
        self.setup_subgui_1()
    
    
    def setup_subgui_1(self):
        """Sets up SubGUI 1 in frame1 with the introduction and choose a degree features"""
        self.main_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0))
        self.degree_chosen = None
        self.degree_combobox = Combobox(self.frame1, values=sorted(self.accepted_degrees.keys()))
        self.degree_combobox.set("Choose a degree")
        self.degree_combobox.grid(row=1, column=0)
        self.degree_submit = Button(self.frame1, text="Submit", command=self.submit_degree)
        self.degree_submit.grid(row=1, column=1)   
        self.frame1.grid(row=0, column=0)
    
    
    def setup_subgui_2(self):
        """Sets up SubGUI 2 in frame2 with display of the chosen degree and buttons to
        decide between a single and double major"""
        degree_template = "Continuing for the degree: {}"
        self.degree_chosen_label['text'] = degree_template.format(self.degree_chosen)
        self.degree_chosen_label.grid(row=0, column=0, columnspan=2, pady=10)
        single_major_button = Button(self.frame2, text="Single Major",
                                     command=lambda: self.setup_subgui_3(False))
        single_major_button.grid(row=1, column=0)
        double_major_button = Button(self.frame2, text="Double Major",
                                     command=lambda: self.setup_subgui_3(True))
        double_major_button.grid(row=1, column=1)
        self.frame2.grid(row=1, column=0)        
    
    
    def setup_subgui_3(self, is_double_major):
        """Sets up SubGUI 3 in frame3 with; either one or two choose a major comboboxes
        depending on is_double_major; and a submit button"""
        self.majors_chosen_label.grid_forget()
        self.frame5.grid_forget()
        self.is_double_major = is_double_major
        if self.is_double_major:
            self.major_combobox.grid_forget()
            self.first_major_combobox['values'] = self.possible_majors
            self.first_major_combobox.set("First Major")
            self.first_major_combobox.grid(row=0, column=0, pady=10)
            self.second_major_combobox['values'] = self.possible_majors
            self.second_major_combobox.set("Second Major")
            self.second_major_combobox.grid(row=0, column=1, pady=10)            
            submit_majors_button = Button(self.frame3, text='Go', command=self.submit_majors)
        else:
            self.first_major_combobox.grid_forget()
            self.second_major_combobox.grid_forget()
            self.major_combobox['values'] = self.possible_majors
            self.major_combobox.set("Choose a major")
            self.major_combobox.grid(row=0, column=0, columnspan=2, pady=10)
            submit_majors_button = Button(self.frame3, text='Go', command=self.submit_major)
        submit_majors_button.grid(row=0, column=2)
        self.frame3.grid(row=2, column=0)
    
    
    def setup_subgui_4(self):
        """Sets up SubGUI 4 in frame 4 with; 'majoring in' info label, GUI
        to enter a completed course (or remove most recent) and another info
        label displaying all courses chosen"""
        self.setup_majors_label()
        self.all_course_objects = open_uni_courses()
        self.all_courses_dict = {}
        for course in list(self.all_course_objects):
            self.all_courses_dict[course.course_id] = course
        message = "Enter the course codes for all courses you have completed (EG: COSC121):"
        self.enter_all_courses_label['text'] = message
        self.enter_all_courses_label.grid(row=0, column=0, columnspan=3)
        self.course_combobox = Combobox(self.frame4, values=sorted(self.all_courses_dict.keys()))
        self.course_combobox.set("Type or select a course")
        self.course_combobox.grid(row=1, column=0)
        self.add_button = Button(self.frame4, text="Add", command=self.add_course)
        self.add_button.grid(row=1, column=1)
        self.remove_last_button = Button(self.frame4, text="Remove Last", command=self.remove_last)
        self.remove_last_button.grid(row=1, column=2)
        self.frame4.grid(row=3, column=0)
        self.user_courses_label.grid(row=5, column=0, columnspan=3)
    
    
    def setup_subgui_5(self):
        """Sets up SubGUI 5 with a single 'SUBMIT ALL' button that submits all info"""
        final_submit_button = Button(self.frame5, text="SUBMIT ALL", command=self.submit_all)
        final_submit_button.grid(row=0, column=0, pady = 10, ipadx = 100)
        self.frame5.grid(row=4, column=0)
    
    
    def setup_majors_label(self):
        """Sets up the majors_chosen_label in grid3 with; 'majoring in' info panel"""
        majors_template = "Majoring in {0}"
        if self.is_double_major:
            majors_template += " and {1}"
        self.majors_chosen_label['text'] = majors_template.format(self.major, self.major2)
        self.majors_chosen_label.grid(row=3, column=0, columnspan=3)
    
    
    def add_course(self):
        """Gets the answer in the text entry, checks if it's a valid course
        then if valid, adds it to the list of courses"""
        potential_course = self.course_combobox.get()
        if potential_course in self.all_courses_dict:
            self.error_courses_label.grid_forget()
            self.user_courses_dict[potential_course] = self.all_courses_dict[potential_course]
            self.user_courses_label['text'] = self.set_label()
            self.course_combobox.set("Type or select a course")
            self.courses_entered.append(potential_course)
        else:
            self.error_courses_label['text'] = "COURSE NOT FOUND"
            self.error_courses_label.grid(row=4, column=0)
    
    
    def set_label(self):
        """Takers self.user_courses_dict and adds its values to
        self.user_courses_label in grid4 with correct formatting"""
        all_text = "{0:<15}{1:<30}{2:>5}\n".format("Course Code", "Title", "Points")
        for item in sorted(self.user_courses_dict.keys()):
            all_text += "\n{}".format(self.user_courses_dict[item])
        self.user_courses_label['text'] = all_text
    
    
    def remove_last(self):
        """Remove the most recently added item from the list of courses"""
        if len(self.courses_entered) > 0:
            most_recent = self.courses_entered.pop()
            self.user_courses_dict.pop(most_recent)
            self.error_courses_label['text'] = "{} was removed from the list.".format(most_recent)
            self.error_courses_label.grid(row=4, column=0)            
        self.user_courses_label['text'] = self.set_label()
    
    
    def submit_all(self):
        """Shuts the MainGui window, allowing the rest of degreepoints.v4 to
        proceed"""
        self.submit_button_pushed = True
        self.window.destroy()
    
    
    def submit_majors(self):
        """Gets the items in first_major_combobox and second_major_combobox,
        checks if valid and different majors, and if so,
        continues by opening SubGUIs 4 and 5"""
        self.frame4.grid_forget()
        self.frame5.grid_forget()
        chosen_major1 = self.first_major_combobox.get()
        chosen_major2 = self.second_major_combobox.get()
        major1_is_valid = chosen_major1 in self.possible_majors
        major2_is_valid = chosen_major2 in self.possible_majors
        if chosen_major1 == chosen_major2:
            self.error_majors_label['text'] = "Please choose different majors"
            self.error_majors_label.grid(row=1, column=0, columnspan=3)
        elif major1_is_valid and major2_is_valid:
            self.major = chosen_major1
            self.major2 = chosen_major2
            self.error_majors_label.grid_forget()
            self.setup_subgui_4()
            self.setup_subgui_5()
        else:
            self.error_majors_label['text'] = ("Please choose majors from the dropdown boxes")
            self.error_majors_label.grid(row=1, column=0, columnspan=3)
    
    
    def submit_major(self):
        """Gets the item in major_combobox, check is a valid major, and if so,
        continues by opening SubGUIs 4 and 5"""
        self.frame4.grid_forget()
        self.frame5.grid_forget()
        chosen_major = self.major_combobox.get()
        if chosen_major in self.possible_majors and chosen_major is not None:            
            self.major = chosen_major
            self.major2 = None
            self.error_majors_label.grid_forget()
            self.setup_subgui_4()
            self.setup_subgui_5()
        else:
            self.error_majors_label['text'] = ("Please choose a major from the dropdown box")
            self.error_majors_label.grid(row=1, column=0, columnspan=3)            
    
    
    def submit_degree(self):
        """If the chosen item is different to the previous, resets all subsequent
        SubGUIs to avoid confusion and then sets up SubGUI 2"""
        degree_chosen = self.degree_combobox.get()
        if degree_chosen in self.accepted_degrees and degree_chosen != self.degree_chosen:
            self.frame2.grid_forget()
            self.frame3.grid_forget()
            self.frame4.grid_forget()
            self.frame5.grid_forget()
            self.degree_chosen = degree_chosen
            self.possible_majors = open_majors(self.degree_chosen)
            self.possible_majors.sort()            
            self.setup_subgui_2()


def open_majors(degree):
    """Opens the file containing possible majors for the degree of choice.
    Returns a list of majors, an empty list if file not found"""
    file_suffix = "_majors"
    file_list = open_string_txt(degree, suffix=file_suffix)
    if file_list != []:
        potential_majors = file_list[2:] #in file, majors are defined from line 3
        return potential_majors
    else:
        return file_list


def open_uni_courses():
    """Opens the university courses file
    Returns a set containing all of the courses as the UniCourse objects"""
    file = "uc_all_courses"
    file_list = open_string_txt(file)
    course_set = set()
    for course in file_list[2:]: #in file, courses are defined from line 3
        if len(course.split(',')) > 2:
            course_id, course_title, points = course.split(',')
            uni_course = UniCourse(course_id, course_title, points)
        else:
            course_id, course_title = course.split(',')
            uni_course = UniCourse(course_id, course_title)
        course_set.add(uni_course)
    return course_set