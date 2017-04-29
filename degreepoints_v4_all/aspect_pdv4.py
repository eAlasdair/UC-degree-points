"""
This module defines the Aspect class and Requirement & Progress subclasses
for degreepoints.v4

The Requirement subclass holds the definition of a particular requirement for a degree
The Progress subclass holds the user's progress towards that requirement

Author: Alasdair Smith
Started: 17 October 2016 (Within calculations_pdv4.py)
Status: Incomplete
"""

class Aspect:
    """
    Defines the Aspect class for degreepoints.v4
    
    An object of this class holds either:
        One requirement for a particular major and degree       (Requirement subclass)
        The user's progress towards that particular requirement (Progress subclass)
    
    For example:
    For one of the requirements for a Computer Science major for a B.Sc:
        60 points in Computer Science at 300 level.
    The progress may be:
        15 points in Computer Science at 300 level.
    
    Attributes:
    self.majors ([] if any major) == A set of major(s) for which the requirement holds
    self.degree == The degree for which the requirement holds
                (Default=None {use if any degree AND if majors is not []})
    self.levels (default=[1 to 5]) == A set of hundred level(s) at which the points can be achieved
    self.points == The number of points required for that requirement
        or the number of points achieved for that requirement
    self.max_non_degree (default=None) == The max number of non-degree points that count
        or the number of non-degree points that were credited
    
    Methods:
    __init__(self, points, degree, majors, levels, max_non_degree)
    __repr__(self)
    __eq__(self, other)
    """
    
    def __init__(self, points, degree=None, majors=[],
                 levels=[1, 2, 3, 4, 5], max_non_degree=None):
        """Initialises the Aspect object"""
        self.points = points
        self.degree = degree
        self.majors = majors
        self.levels = levels
        self.max_non_degree = max_non_degree
    
    
    def __repr__(self):
        """Defines how the aspect is to be displayed"""
        if len(self.majors) == 1:
            template = "{0} {1} points"
        elif self.degree is not None:
            template = "{0} {2} points"
        else:
            template = "{0} points overall"
        if len(self.levels) != [1, 2, 3, 4, 5]:
            template += " at {3} hundred level"
        return template.format(self.points_required, self.majors[0], self.degree, self.levels)
    
    
    def __eq__(self, other):
        """Defines equality between two Aspect objects
        They are equal if they have the same degree, major and levels. Points isn't checked
        other corresponds to the progress-type aspect"""
        is_same_degree = self.degree == None or self.degree == other.degree
        is_same_majors = is_list_in_list(other.majors, self.majors)
        is_same_levels = is_list_in_list(other.levels, self.levels)
        return is_same_degree and is_same_majors and is_same_levels
    
    
    def towards_completion(self, *progresses):
        """"Returns a percentage of the number of points achieved in each progress aspect
        out of the number of points required in self"""
        complete_progress = 0
        for progress in progresses:
            if self.__eq__(progress):
                complete_progress += progress.points / self.points * 100
            elif is_list_in_list(progress.levels, self.levels):
                max_points = max(progress.points, self.max_non_degree)
                complete_progress += max_points / self.points * 100
        
        return complete_progress


def is_list_in_list(list_1, list_2):
    """Returns true if all items in list_1 are in list_2, false otherwise"""
    for item in list_1:
        if item not in list_2:
            return False
    return True
    
#class Requirement(Aspect):
    #"""
    #Defines the Requirement subclass for degreepoints.v4
    #"""
    #def __init__(self, points, degree=None, majors=[],
                     #levels=[1, 2, 3, 4, 5], max_non_degree=None):
            #"""Initialises the Requirement object"""


#class Progress(Aspect):
    #"""
    #Defines the Progress subclass for degreepoints.v4
    #"""
    #def __init__(self, points, degree=None, majors=[],
                     #levels=[1, 2, 3, 4, 5], max_non_degree=None):
            #"""Initialises the Progress object"""  