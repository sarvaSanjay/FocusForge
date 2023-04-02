from __future__ import annotations

import operator

from course import _Course, get_union
from CourseGraph import Graph
import csv
import math
import ast

class Focus():
    name: str
    course_reqs = list[set[_Course]]  # top  level prereqs
    credits_req = float
    # REDO: That long string of characters is not there for 2 focii so let it be
    # program_code = str  # the long string of alphabets that nobody really cares about. like ASFOC1689F

    def __init__(self, name: str, courses_reqs: list[set[_Course]], credits_req: float):
        self.name = name
        self.course_reqs = courses_reqs
        self.credits_req = credits_req
        # self.program_code = program_code

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

    def get_paths(self, completed=None) -> list[set[_Course]]:
        """
        Get all possible paths by which you can complete a particular focus
        """
        if completed is None:
            completed = set()
        total_paths = []
        for reqs in self.course_reqs:
            paths = [set()]
            for course in reqs:
                sub_paths = course.get_prereqs()
                sub_paths.sort(key=lambda x: (rank_path(x, completed), len(x)))
                paths = get_union(paths, sub_paths[:5])
            total_paths.extend(paths)
        total_paths.sort(key=lambda x: (rank_path(x, completed), len(x)))
        return total_paths

    def __repr__(self):
        return f'Name: {self.name}\t Credits: {self.credits_req}\t Pre_reqs: {self.course_reqs}'


def cartesian_product(lst1: list[set], lst2: list[set], max_size: int =math.inf) -> list[set]:
    """Returns a cartesian product"""
    return [set1.union(set2) for set1 in lst1 for set2 in lst2 if len(set1) + len(set2) < max_size]


def setup_minimal_focus(focus_string: list[str]) -> Focus:
    """Sets up focus with only name and credits required
    i.e., does not calculate valid course requirements for a focus"""
    lst = ast.literal_eval(focus_string[1])
    credits_required_so_far = sum(req[0] for req in lst)
    return Focus(focus_string[0], [set()], credits_required_so_far)


def setup_minimal_focii(focus_file: str) -> list[Focus]:
    list_of_focii = []
    with open(focus_file) as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            list_of_focii.append(setup_minimal_focus(row))
        return list_of_focii


#RECO: instead of taking the focus string as a parameter read the file to find the valid focus string. Also convert this into a method
def complete_minimal_focus(course_graph: Graph, in_focus: Focus, focus_file: str):
    """Mutates in_focus so that it contains its required courses"""
    with open(focus_file) as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            if row[0] == in_focus.name:
                focus_string = row[1]
                break

    list_reqs = []
    lst = ast.literal_eval(focus_string)
    for req in lst:
        # block calculates the powerset for each collection of requirements
        powerset_so_far = [set()]
        for course in req[1]:
            if isinstance(course, set):
                course_list = tuple(course_graph.courses[c] for c in course if c in course_graph.courses)
                powerset_so_far.extend(
                    cartesian_product(powerset_so_far, [{course_list}], 2 * req[0] + 1))
            elif course in course_graph.courses:  # TODO some courses no longer exist in timetable
                powerset_so_far.extend(
                    cartesian_product(powerset_so_far, [{course_graph.courses[course]}], 2 * req[0] + 1))

        total_paths = []
        for path in powerset_so_far:
            total_paths.extend(multiply_paths(path))

        valid_paths = []  # block cuts down powerset to those meeting credits required
        for path in total_paths:
            if sum(course.credits for course in path) == req[0] or (
                    sum(course.credits for course in path) == req[0] + 0.5 and any(
                'Y' in course.course_code[6] for course in path)):
                valid_paths.append(path)
        list_reqs.append(valid_paths)

    final_valid_paths = list_reqs[0]
    for i in range(1, len(list_reqs)):
        final_valid_paths = cartesian_product(final_valid_paths, list_reqs[i])
    in_focus.course_reqs = final_valid_paths


def multiply_paths(path):
    optioned_courses = []
    regular_courses = set()
    for choice in path:
        if isinstance(choice, _Course):
            regular_courses.add(choice)
        if isinstance(choice, tuple):
            courses = []
            for course in choice:
                courses.append({course})
            optioned_courses.append(courses)
    total_paths = [regular_courses]
    while len(optioned_courses) != 0:
        total_paths = get_union(total_paths, optioned_courses[0])
        optioned_courses.pop(0)
    return total_paths


def rank_path(path: set[_Course], completed=None) -> float:
    if completed is None:
        completed = set()
    credits = 0.0
    for course in path:
        if course not in completed:
            credits += course.credits
    return credits
