"""
Version 4 of a program to calculate and display statistics about how a student
is progressing towards a degree in his/her chosen field and specialisation at UC.

Improvements:
More functionality, file processing for prerequisites, classes, modules,
dictionaries, all wrapped up in a GUI and will hopefully be finished this time.

Author: Alasdair Smith
Started: 11 October 2016
Status: Incomplete
"""

from tkinter import *
from tkinter.ttk import *
#from file_toolkit import open_string_txt
from main_gui_pdv4 import MainGui
from calculations_pdv4 import Data

ACCEPTED_DEGREES = {
    "Science": "B.Sc",
    "Commerce": "B.Com",
    "Arts": "B.A"
    }

START_MESSAGE = """Hello!
This program will help you find out how you are progressing towards a
degree in your chosen field at UC. You can change your answers at any
time, and this form will revert to where you changed your answer.

Please choose a degree:
"""








def main():
    """Piddly little bit of code that runs everything"""
    window = Tk()
    main_gui = MainGui(window, START_MESSAGE, ACCEPTED_DEGREES)
    window.mainloop()
    
    if main_gui.submit_button_pushed:
        main_data = Data(main_gui)
        
        #second_window = Tk()
        #results_gui = ResultsGui(second_window, main_data)
        #second_window.mainloop()
    
    print(main_gui.user_courses_dict)
    print("THANKS")


main()