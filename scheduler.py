import copy

from course import _Course
from focus import *  # also imports course
# from CourseGraph import Graph

def schedule(in_path: set[_Course], completed_courses: set[_Course], current_semester: str) -> dict[str, set[_Course]]:
    """Returns one of the faster way to complete a focus
    Preconditions:
    current_semester is in ('Fall' + 'Winter') 20([0-9])^2"""
    path = copy.deepcopy(in_path)
    for course in completed_courses: # avoid iteration bugs
        if course in path:
            path.remove(course)
    max_level = 0

