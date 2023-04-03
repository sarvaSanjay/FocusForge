"""Module Description
===============================
This Python module implements our focus class

Copyright and Usage Information
===============================
This file is provided under the Mozilla Public License 2.0
This file is Copyright (c) 2023 Raahil Vora, Sarva Sanjay, and Ansh Prasad."""
from __future__ import annotations
import csv
import math
import ast
from course import _Course, get_union
from course_graph import Graph


class Focus:
    """
    Represents a single focus at University of Toronto.

    Instance Attributes
    - name:
        Name of the focus.
    - course_reqs:
        Top-level courses required in order to complete a focus at University of Toronto.
        It is a list of set of Courses where every set of courses represents a valid way to complete the focus.
    - credits_req:
        The total number of credits required to complete a focus.

    Representation Invariants:
    - self.name != ''
    - self.credits_req > 0.0
    - every course in self.course_reqs is a valid course
    """
    name: str
    course_reqs: list[set[_Course]]  # top  level prereqs
    credits_req: float

    def __init__(self, name: str, courses_reqs: list[set[_Course]], credits_req: float) -> None:
        self.name = name
        self.course_reqs = courses_reqs
        self.credits_req = credits_req

    def get_paths(self, completed: set = None) -> list[set[_Course]]:
        """
        Get all possible course paths by which you can complete a particular focus ranked by minimum credits required to
        complete them.
        """
        if completed is None:
            completed = set()
        if len(self.course_reqs) > 50:
            self.course_reqs.sort(key=lambda x: (rank_path(x, completed), len(x)))
            self.course_reqs = self.course_reqs[:50]
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

    def __repr__(self) -> str:
        return f'Name: {self.name}\t Credits: {self.credits_req}\t Pre_reqs: {self.course_reqs}'


def cartesian_product(lst1: list[set], lst2: list[set], max_size: int = math.inf) -> list[set]:
    """Returns a cartesian product"""
    return [set1.union(set2) for set1 in lst1 for set2 in lst2 if len(set1) + len(set2) < max_size]


def setup_minimal_focus(focus_string: list[str]) -> Focus:
    """
    Sets up focus with only name and credits required
    i.e., does not calculate valid course requirements for a focus
    """
    lst = ast.literal_eval(focus_string[1])
    credits_required_so_far = sum(req[0] for req in lst)
    return Focus(focus_string[0], [set()], credits_required_so_far)


def setup_minimal_focii(focus_file: str) -> list[Focus]:
    """
    Returns a list of focii with only names and credits required initialised.
    """
    list_of_focii = []
    with open(focus_file) as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            list_of_focii.append(setup_minimal_focus(row))
        return list_of_focii


# RECO: convert this into a method
def complete_minimal_focus(course_graph: Graph, in_focus: Focus, focus_file: str) -> None:
    """
    Mutates in_focus so that it contains its required courses. The function calculates all possible ways to complete a
    focus.
    Preconditions:
    focus_file contains the corresponding in_focus
    """
    focus_string = ''
    # Reads the file to find the initial course requirements
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
            elif course in course_graph.courses:
                powerset_so_far.extend(
                    cartesian_product(powerset_so_far, [{course_graph.courses[course]}], 2 * req[0] + 1))
        # for paths which have tuples of courses, we create multiple paths for each course in the tuple
        total_paths = []
        for path in powerset_so_far:
            total_paths.extend(multiply_paths(path))
        # block cuts down powerset to those meeting credits required
        valid_paths = []
        for path in total_paths:
            sum_credits = sum(subject.credits for subject in path)
            contains_y = any('Y' in subject.course_code[6] for subject in path)
            if sum_credits == req[0] or (sum_credits == req[0] + 0.5 and contains_y):
                valid_paths.append(path)
        list_reqs.append(valid_paths)
    # takes cartesian product of every requirement
    final_valid_paths = list_reqs[0]
    for i in range(1, len(list_reqs)):
        final_valid_paths = cartesian_product(final_valid_paths, list_reqs[i])
    in_focus.course_reqs = final_valid_paths


def multiply_paths(path: set) -> list[set[_Course]]:
    """
    A helper function that creates a list of set of courses if there is a tuple of courses in the path.
    """
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


def rank_path(path: set[_Course], completed: set = None) -> float:
    """
    Calculates the number of further credits required to finish a set of courses given the current number of completed
    courses.
    """
    if completed is None:
        completed = set()
    credits_so_far = 0.0
    for course in path:
        if course not in completed:
            credits_so_far += course.credits
    return credits_so_far


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'disable': ['forbidden-IO-function', 'too-many-locals'],
        'extra-imports': ['course', 'math', 'ast', 'csv', 'course_graph'],  # the names (strs) of imported modules
        'max-line-length': 120
    })
