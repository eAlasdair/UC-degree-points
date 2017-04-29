"""
Program to show progress towards a BSc
and maybe the others eventually
"""

GREETING_INITIAL = """
Hello! This program will help you find out how you are progressing towards a
degree in your chosen field at UC. You will need to find out and enter the
number of points you have achieved in your chosen field and specialisation,
per level you have studied. Will currently only check point requirements,
not course requirements.
Please answer the questions that follow.
"""
GREETING_POINTS_REQUIRED = """
For a {0} degree, majoring in {1} you need:
"""
GREETING_POINTS_ACHIEVED = """
You have achieved:
"""

TEMPLATE_POINTS_ACHIEVED = "{0} points {1}"
EXTENDED_TEMPLATE_POINTS_ACHIEVED = TEMPLATE_POINTS_ACHIEVED + " {2}%"

QUESTION_DEGREE_CHOICE = "What is your degree choice? "
QUESTION_DOUBLE_MAJOR = "Are you doing a double major? "
QUESTION_MAJOR_CHOICE = "What is your major? "

QUESTION_HIGHEST_LEVEL = "What X is the level of the highest X-hundred level course you have finished? "
QUESTION_MAJOR_POINTS = "How many {1} points did you get at {0} level? "
QUESTION_DEGREE_POINTS = "How many {2} but not {1} points did you get at {0} level? "
QUESTION_OTHER_POINTS = "How many other points did you get at {0} level? "

ERROR_UNKNOWN_DEGREE = "Error: Degree not found. Please choose from:"
ERROR_UNKNOWN_MAJOR = "Error: Major not found. Please choose from:"
ERROR_DIFFERENT_MAJOR = "Please choose a different second major."
ERROR_NOT_YES_OR_NO = "Error: Please answer yes or no."
ERROR_NOT_HUNDRED_LEVEL = "Error: Please give a multiple of 100. Choose from:"
ERROR_NOT_A_NUMBER = "Error: Please give a positive integer."

ACCEPTED_DEGREES = [
    "Science"
]
ACCEPTED_SCIENCE_MAJORS = [
    "Astronomy",
    "Biochemistry",
    "Biological Sciences",
    "Chemistry",
    "Computer Science",
    "Economics",
    "Finance",
    "Financial Engineering",
    "Geography",
    "Geology",
    "Linguistics",
    "Mathematics",
    "Philosophy",
    "Physics",
    "Psychology",
    "Statistics",
]

#SCIENCE TEXT
SCIENCE_NON_SCI_POINT_LIMIT = 105

ABOVE_100_LEVEL = "above 100 level."
OVERALL_IN_SCIENCE = "overall in science courses."
IN_MAJOR_AT_300_LEVEL_AND_ABOVE = "in {0} at 300 level and above."
OVERALL_AT_300_LEVEL_AND_ABOVE = "overall at 300 level and above."
OVERALL = "overall."
MAX_NON_SCI_PTS_COUNTED = "maximum in non-science courses are counted."
NON_SCI_PTS = "from non-science courses at all levels,"
OTHER_HAVE_BEEN_COUNTED = "of these have been counted."
SCIENCE_POINTS_REQUIRED = [
    (225, ABOVE_100_LEVEL),
    (255, OVERALL_IN_SCIENCE),
    (60, IN_MAJOR_AT_300_LEVEL_AND_ABOVE),
    (90, OVERALL_AT_300_LEVEL_AND_ABOVE),
    (360, OVERALL),
    (SCIENCE_NON_SCI_POINT_LIMIT, MAX_NON_SCI_PTS_COUNTED)
    ]

YES_OR_NO = ["yes", "no"]

X_HUNDRED_LEVELS = ["0", "1", "2", "3", "4", "5"]

def ask_degree():
    """Asks for the user's degree choice and returns a string"""
    user_degree = input(QUESTION_DEGREE_CHOICE).strip().title()
    while user_degree not in ACCEPTED_DEGREES:
        print(ERROR_UNKNOWN_DEGREE)
        for degree in ACCEPTED_DEGREES:
            print(degree)
        user_degree = input(QUESTION_DEGREE_CHOICE).strip().title()
    return(user_degree)

def askif_double_major():
    """Asks whether the user is doing a double major and returns a string"""
    is_double_major = input(QUESTION_DOUBLE_MAJOR).strip().lower()
    while is_double_major not in YES_OR_NO:
        print(ERROR_NOT_YES_OR_NO)
        is_double_major = input(QUESTION_DOUBLE_MAJOR).strip().lower()
    return(is_double_major)

def ask_major(accepted_majors):
    """Asks for the user's major choice and returns a string"""
    user_major = input(QUESTION_MAJOR_CHOICE).strip().title()
    while user_major not in accepted_majors:
        print(ERROR_UNKNOWN_MAJOR)
        for major in accepted_majors:
            print(major)
        user_major = input(QUESTION_MAJOR_CHOICE).strip().title()
    return(user_major)

def initial_questions_main():
    """
    Asks the initial questions about degree and major, returns a list of strings
    [Degree choice, 1st maj choice, (2nd maj choice or 'not double' if none)]
    """
    user_degree = ask_degree()
    if user_degree == "Science":
        accepted_majors = ACCEPTED_SCIENCE_MAJORS
    #NEEDS TO BE EXTENDED FOR FURTHER DEGREES - KINDA CLUNKY
    double_major = askif_double_major()
    if double_major == "no":
        user_major = ask_major(accepted_majors)
        return[user_degree, user_major, "not double"]
    else:
        print("First major:")
        user_major_1 = ask_major(accepted_majors)
        print("Second major:")
        user_major_2 = ask_major(accepted_majors)
        while user_major_2 == user_major_1:
            print(ERROR_DIFFERENT_MAJOR)
            user_major_2 = ask_major(accepted_majors)
        return[user_degree, user_major_1, user_major_2]
    
def ask_hundred_levels():
    """Asks for the max level course that has been completed, returns an int"""
    max_hundred_level = input(QUESTION_HIGHEST_LEVEL).strip()
    while max_hundred_level not in X_HUNDRED_LEVELS:
        print(ERROR_NOT_HUNDRED_LEVEL)
        for level in X_HUNDRED_LEVELS:
            print(level)
        max_hundred_level = input(QUESTION_HIGHEST_LEVEL).strip()
    return(int(max_hundred_level))

def ask_points_per_hundred_level(hundred_level, user_major, user_degree):
    """
    Asks for the number of points achieved per hundred level,
    returns a list of lists of positive integers:
    [Major points per year, Degree points per year, Other points per year]
    """
    list_major_points = []
    list_degree_points = []
    list_other_points = []
    for i in range(1, hundred_level + 1):
        level = i * 100
        major_points = input(QUESTION_MAJOR_POINTS.format(level, user_major))
        while not major_points.isnumeric():
            print(ERROR_NOT_A_NUMBER)
            major_points = input(QUESTION_MAJOR_POINTS.format(level, user_major))
        major_points = int(major_points)
        list_major_points.append(abs(major_points))
        
        degree_points = input(QUESTION_DEGREE_POINTS.format(level, user_major, user_degree))
        while not degree_points.isnumeric():
            print(ERROR_NOT_A_NUMBER)
            degree_points = input(QUESTION_DEGREE_POINTS.format(level, user_major, user_degree))
        degree_points = int(degree_points)
        list_degree_points.append(abs(degree_points))
        
        other_points = input(QUESTION_OTHER_POINTS.format(level))
        while not other_points.isnumeric():
            print(ERROR_NOT_A_NUMBER)
            other_points = input(QUESTION_OTHER_POINTS.format(level))
        other_points = int(other_points)
        list_other_points.append(abs(other_points))
    
    points_summary = [list_major_points, list_degree_points, list_other_points]
    return(points_summary)

def calculate_points_achieved_science(points_summary, hundred_level):
    """
    Calculates the information needed to determine progress, returns lists
    remember points_summary comes in form [major_points, degree_points, other]
    """
    total_points = 0
    total_100_level = 0
    total_200_level = 0
    total_300_level = 0
    total_400_level = 0
    total_500_level = 0
    
    if hundred_level > 0:
        total_100_level = points_summary[0][0] + points_summary[1][0] + points_summary[2][0]
    if hundred_level > 1:
        total_200_level = points_summary[0][1] + points_summary[1][1] + points_summary[2][1]
    if hundred_level > 2:
        total_300_level = points_summary[0][2] + points_summary[1][2] + points_summary[2][2]
    if hundred_level > 3:
        total_400_level = points_summary[0][3] + points_summary[1][3] + points_summary[2][3]
    if hundred_level > 4:
        total_500_level = points_summary[0][4] + points_summary[1][4] + points_summary[2][4]
    
    total_for_major_all_levels = 0
    total_for_degree_all_levels = 0
    total_for_other_all_levels = 0
    
    total_degree_above_100_level = 0
    total_major_above_100_level = 0
    total_other_above_100_level = 0
    
    total_for_major_300_level = 0
    total_for_degree_300_level = 0
    total_for_other_300_level = 0
    
    for i in range(hundred_level):
        total_points += sum(points_summary[i])
        total_for_degree_all_levels += (points_summary[0][i] + points_summary[1][i])
        total_for_major_all_levels += points_summary[0][i]
        total_for_other_all_levels += points_summary[2][i]
        if i > 0:
            total_degree_above_100_level += (points_summary[0][i] + points_summary[1][i])
            total_major_above_100_level += points_summary[0][i]
            total_other_above_100_level += points_summary[2][i]
        if i >= 2:
            total_for_degree_300_level += (points_summary[0][i] + points_summary[1][i])
            total_for_major_300_level += points_summary[0][i]
            total_for_other_300_level += points_summary[2][i]
      
    if total_for_other_all_levels <= SCIENCE_NON_SCI_POINT_LIMIT:
        total_for_degree_all_levels += total_for_other_all_levels
    else:
        total_for_degree_all_levels += SCIENCE_NON_SCI_POINT_LIMIT
    
    if total_other_above_100_level <= SCIENCE_NON_SCI_POINT_LIMIT:
        total_degree_above_100_level += total_other_above_100_level
    else:
        total_degree_above_100_level += SCIENCE_NON_SCI_POINT_LIMIT
    
    if total_for_other_300_level <= SCIENCE_NON_SCI_POINT_LIMIT:
        total_for_degree_300_level += total_for_other_300_level
    else:
        total_for_degree_300_level += SCIENCE_NON_SCI_POINT_LIMIT
    
    points_per_level = [
        total_100_level,
        total_200_level,
        total_300_level,
        total_400_level,
        total_500_level
        ]
    
    total_points_all_levels = [
        total_for_degree_all_levels,
        total_for_major_all_levels,
        total_for_other_all_levels
        ]
    
    total_points_above_100_level = [
        total_degree_above_100_level,
        total_major_above_100_level,
        total_other_above_100_level
        ]
    
    total_points_300_level = [
        total_for_degree_300_level,
        total_for_major_300_level,
        total_for_other_300_level
        ]
    
    science_point_summary = [
        points_per_level,
        total_points_all_levels,
        total_points_above_100_level,
        total_points_300_level
        ]
    
    return(science_point_summary)

def format_science_point_summary(science_point_summary):
    """Formats the point summary for display, returns list of pairs    
    note that input is in the form [
    [points per level (100 - 500)],
    [overall points (degree, major, other)],
    [points above 100 level (degree, major, other)],
    [points at 300+ level (degree, major, other)]
    ]"""
    #DO IN PARALLEL WITH SCIENCE_POINTS_REQUIRED
    formatted_science_point_summary = []
    formatted_pts_above_100_level = [
        science_point_summary[2][0],
        ABOVE_100_LEVEL]
    formatted_science_point_summary.append(formatted_pts_above_100_level)
    formatted_sci_pts_overall = [
        (science_point_summary[1][0] - science_point_summary[1][2]),
        OVERALL_IN_SCIENCE]
    formatted_science_point_summary.append(formatted_sci_pts_overall)
    formatted_pts_in_major_300_level = [
        science_point_summary[3][1],
        IN_MAJOR_AT_300_LEVEL_AND_ABOVE]
    formatted_science_point_summary.append(formatted_pts_in_major_300_level)
    formatted_pts_overall_300_level = [
        science_point_summary[3][0],
        OVERALL_AT_300_LEVEL_AND_ABOVE]
    formatted_science_point_summary.append(formatted_pts_overall_300_level)
    formatted_pts_overall = [
        science_point_summary[1][0],
        OVERALL]
    formatted_science_point_summary.append(formatted_pts_overall)
    formatted_other_pts_overall = [
        science_point_summary[1][2],
        NON_SCI_PTS]
    formatted_science_point_summary.append(formatted_other_pts_overall)
    if science_point_summary[1][2] > SCIENCE_NON_SCI_POINT_LIMIT:
        formatted_other_pts_counted = [SCIENCE_NON_SCI_POINT_LIMIT, OTHER_HAVE_BEEN_COUNTED]
    else:
        formatted_other_pts_counted = [science_point_summary[1][2], OTHER_HAVE_BEEN_COUNTED]
    formatted_science_point_summary.append(formatted_other_pts_counted)
    return(formatted_science_point_summary)

def print_progress_science(user_degree, user_major, formatted_science_point_summary):
    """Tells the user what they need and prints what they have"""
    print(GREETING_POINTS_REQUIRED.format(user_degree, user_major))
    list_numbers = []
    for pair in SCIENCE_POINTS_REQUIRED:
        list_numbers.append(pair[0])
        print(TEMPLATE_POINTS_ACHIEVED.format(pair[0], pair[1].format(user_major)))
    print(GREETING_POINTS_ACHIEVED)
    
    i = 0
    for i in range(len(formatted_science_point_summary)):
        pair = formatted_science_point_summary[i]
        if i < (len(SCIENCE_POINTS_REQUIRED) - 1):
            divisor = list_numbers[i]
            percentile = int(pair[0] / divisor * 100)
            if percentile > 100:
                percentile = 100
            print(EXTENDED_TEMPLATE_POINTS_ACHIEVED.format(pair[0], pair[1].format(user_major), percentile))
        else:
            print(TEMPLATE_POINTS_ACHIEVED.format(pair[0], pair[1].format(user_major)))

def secondary_questions_main(user_degree, user_major):
    """
    Asks further questions about year of study and points aquired
    then chooses how to proceed and prints standings
    """
    max_hundred_level = ask_hundred_levels()
    points_summary = ask_points_per_hundred_level(max_hundred_level, user_major, user_degree)
    if user_degree == "Science":
        science_point_summary = calculate_points_achieved_science(points_summary, max_hundred_level)
        formatted_science_point_summary = format_science_point_summary(science_point_summary)
        print_progress_science(user_degree, user_major, formatted_science_point_summary)
    #EXTEND FOR FURTHER MAJORS
    #CURRENTLY NEW FUNCTIONS NEED TO BE MADE FOR EACH

def main():
    """Runs everything with some boolean logic"""
    print(GREETING_INITIAL)
    
    print("Part 1:")
    degree_and_majors = initial_questions_main()
    user_degree = degree_and_majors[0]
    if degree_and_majors[2] == "not double":
        user_major = degree_and_majors[1]
        print("""
        Continuing for the degree: {0},
        majoring in {1}
        """.format(user_degree, user_major))
        print("Part 2:")
        secondary_questions_main(user_degree, user_major)        
    else:
        user_major_1 = degree_and_majors[1]
        user_major_2 = degree_and_majors[2]
        print("""
        Continuing for the degree: {0},
        majoring in {1} and {2}.
        """.format(user_degree, user_major_1, user_major_2))
        
        print("This functionality is incomplete! Will be improved in future")
        print("""
        Part 2:
        For your first major, {}:
        """.format(user_major_1))
        secondary_questions_main(user_degree, user_major_1)
        print("""
        For your second major, {}:
        """.format(user_major_2))
        secondary_questions_main(user_degree, user_major_2)
    
    
main()