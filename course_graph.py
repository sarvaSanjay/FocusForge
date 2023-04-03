"""Module Description
===============================
This Python module implements our Graph

Copyright and Usage Information
===============================
This file is provided under the Mozilla Public License 2.0
This file is Copyright (c) 2023 Raahil Vora, Sarva Sanjay, and Ansh Prasad."""
from __future__ import annotations
import ast
import csv
from course import _Course


class Graph:
    """
    Creates a Graph of all courses depicting the pre-requisite relations between all courses.

    Instance Attributes
    - courses:
        A dictionary of all courses in the University of Toronto where the hey corresponds to the six letter unique
        course code and the value is a _Course object.
    - prereqs:
        A set of all pre-requisite relations in the University of Toronto academic calendar. Each pre-requiste relation
        is represented as a tuple whose first value is the parent course and the second value is the child course which
        is the pre-requisite of the first course.

    Representation Invariants:
        - all([prer[0].course_code in self.courses and prer[1].course_code in self.courses for prer in self.prereqs])
        - all([prereq[1] in prereq[0].prereqs for prereq in self.prereqs])
    """
    courses: dict[str, _Course]
    prereqs: set[tuple[_Course, _Course]]

    def __init__(self, input_file: str = 'course-data.csv') -> None:
        self.courses = {}
        self.prereqs = set()
        self.generate_graph_from_csv(input_file=input_file)

    def generate_graph_from_csv(self, input_file: str = 'course-data.csv') -> None:
        """
        Generates the courses and pre-requisite relations from the input_file.
        Preconditions:
        - input_file is a valid csv file that contains course codes, names and prereqs.
        """
        with open(input_file, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f=f, delimiter=';')
            for row in reader:
                course = _Course(row['code'], row['name'], [])
                self.courses[row['code']] = course
        with open(input_file, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f=f, delimiter=';')
            for row in reader:
                pre_requisites = ast.literal_eval(row['pre-requisites'])
                for prereq_code_set in pre_requisites:
                    prereq_code_set = set(prereq_code_set)
                    prereq_set = {self.courses[code] for code in prereq_code_set if code in self.courses}
                    self.courses[row['code']].prereqs.append(prereq_set)
                    for pre_req in prereq_set:
                        self.prereqs.add((self.courses[row['code']], pre_req))


def get_schedule(path: set[_Course], completed: set[_Course] = None) -> list[set[_Course]]:
    """
    Generates a schedule to complete a particular path of courses. The function works by recursively finding the set of
    courses which can be met only using the completed courses.
    Preconditions:
    - [course in path for course in completed]
    """
    if completed is None:
        completed = set()
    completed = {course for course in completed if course in path}
    if completed == path:
        return []
    next_courses = set()
    for course in path:
        if (not course.path_has_prerequisite(path, completed)) and (course not in completed):
            next_courses.add(course)
    return [next_courses] + get_schedule(path, completed.union(next_courses))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'disable': ['forbidden-IO-function'],
        'extra-imports': ['ast', 'csv', 'course'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
