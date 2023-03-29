from __future__ import annotations
import math  # maybe we can work on a simplar solution later? Maybe not?
import csv


class _Course():
    course_code: str
    name: str
    prereqs: list[set[_Course]]
    credits: float

    def __init__(self, code: str, name: str, prereqs: list[set[_Course]]):
        self.course_code = code
        self.name = name
        self.prereqs = prereqs
        if self.course_code[6] == 'Y':  # Better solution. PSY129H1 would get assigned 1 with suggested solution
            self.credits = 1.0
        else:
            self.credits = 0.5

    def get_prereqs(self) -> list[set[_Course]]:  # can't have set in set
        # if course is CSC265, prereqs are CSC240 or CSC236 (excluding coreqs)
        # CSC240 prereqs are none
        # CSC236 prereqs are (CSC148 and CSC165) OR CSC(csc111)
        # so this methods returns {{CSC240}, {CSC236, CSC148, CSC165}, {CSC236, CSC111}}
        return  # nooooooo, it's too hard


class Focus():
    name: str
    course_reqs = list[set[_Course]]  # top  level prereqs
    credits_req = float
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

























































# oshiete oshiete yo sono shikumi wo
# boku no naka ni dare ga iru no kowareta kowareta yo kono sekai de
# kimi ga warau nani mo miezu ni
