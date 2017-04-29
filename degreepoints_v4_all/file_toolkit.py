"""
file_toolkit:

Complement module for prog_degreepoints_v3 and higher versions
Contains extra functions for file processing

Alasdair Smith
Created September 2016
"""

def ask_a_question(question, potential_answers, error_message="Invalid answer",
                   list_answers=True):
    """Asks the specified question repeatedly until an answer is given that is
    in potential_answers.
    Will print error_message for each failed attempt to answer.
    If list_answers is true then for each failed attempt the potential answers
    to the question are given (default = True).
    If potential_answers include strings, they must be in .title() format.
    Returns the answer as a string in .title() format.
    """
    answer = input(question).strip().title()
    answers_as_string = []
    for i in range(len(potential_answers)):
        answers_as_string.append(str(potential_answers[i]))
    while answer not in answers_as_string:
        print(error_message)
        if list_answers:
            for item in potential_answers:
                print(item)
        answer = input(question).strip().title()
    return answer


def open_txt(string):
    """Opens file (string.txt) where 'string' is the filename.
    Returns a list of strings. Returns an empty list if the file is not found"""
    filename = string + ".txt"
    try:
        infile = open(filename)
        lines = infile.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip("\n")
        infile.close()
        return lines
    except FileNotFoundError:
        return []


def string_to_filename(string):
    """Takes a string and returns a new one in lowercase with whitespace
    replaced by underscores.
    NOTE: Will remove whitespace either side of the string rather than replace
    """
    string = string.lower().strip()
    filename = string.replace(" ", "_")
    return filename


def open_string_txt(string, prefix="", suffix=""):
    """Combines string_to_filename with open_txt to open files
    Can include prefix and/or suffix (NOTE: still pre .txt) if required
    Remember: include the underscore before/after the suffix/prefix if required
    """
    filename = prefix + string_to_filename(string) + suffix
    file_lines = open_txt(filename)
    return file_lines