from __future__ import annotations
from course import _Course
import csv
import math

class Focus():
    name: str
    course_reqs = list[set[_Course]]  # top  level prereqs
    credits_req = float
    # REDO: That long string of characters is not there for 2 focii so let it be
    program_code = str  # the long string of alphabets that nobody really cares about. like ASFOC1689F

    def __init__(self, name: str, courses_reqs: list[set[_Course]], credits_req: float, program_code: str):
        self.name = name
        self.course_reqs = courses_reqs
        self.credits_req = credits_req
        self.program_code = program_code

    def credits_left(self, completed: set[_Course]) -> float:
        """Returns the number of credits left to complete a focus"""
        total_prereqs = [set()]
        for path in self.course_reqs:
            temp_list = [set()]
            for course in path:
                temp_list = cartesian_product(temp_list, course.get_prereqs())
                temp_list = cartesian_product(temp_list, [{course}])
            total_prereqs = cartesian_product(temp_list, total_prereqs)
        min = math.inf
        for path in total_prereqs:
            if sum(course.credits for course in path if course not in completed) < min:
                min = round(sum(course.credits for course in path), 1)  # avoid weird floating point bugs
        return min


def cartesian_product(lst1: list[set], lst2: list[set]) -> list[set]:
    """Returns a cartesian product"""
    return [set1.union(set2) for set1 in lst1 for set2 in lst2]


def setup_focus(course_file: str, focus_file: str) -> Focus:
    courses_dict = {}
    with open(course_file) as courses_csv:
        reader = csv.reader(courses_csv, delimiter=';')
        next(reader)
        for row in reader:
            courses_dict[row[0]] = _Course(row[0], row[1], [set()])
    with open(course_file) as courses_csv:  # prereqs need to be done separately
        reader = csv.reader(courses_csv, delimiter=';')
        next(reader)
        for row in reader: #gtg now, will touch later
            pass