"""Module Description
===============================
This Python module implements our Course class

Copyright and Usage Information
===============================
This file is provided under the Mozilla Public License 2.0
This file is Copyright (c) 2023 Raahil Vora, Sarva Sanjay, and Ansh Prasad."""
from __future__ import annotations


class _Course:
    """
    Class to represent a single course at University of Toronto.
    Instance Attributes
    - course_code:
        A unique 8-digit code that is used to identify a course.
    - name:
        Name of the course.
    - prereqs:
        Courses that need to be taken in order to take this particular course. It is represented as a list of set of
        courses where each course in the set of courses represents one possible way in which a prerequisite condition
        can be met.
    - credits:
        Number of credits that a course is worth. It can either be 0.5 or 1.0.

    Representation Invariants
    - len(self.course_code) == 8
    - len(self.name) != 0
    - self.credits == 0.5 or self.credits == 1.0
    - Every course in self.prereqs is a valid course at University of Toronto St. George campus.
    """
    course_code: str
    name: str
    prereqs: list[set[_Course]]
    credits: float

    def __init__(self, code: str, name: str, prereqs: list[set[_Course]]) -> None:
        self.course_code = code
        self.name = name
        self.prereqs = prereqs
        if self.course_code[6] == 'Y':
            self.credits = 1.0
        else:
            self.credits = 0.5

    def get_prereqs(self, visited: set = None) -> list[set[_Course]]:
        """
        Recursive function that returns a list of set of courses where each set of courses is a way in which the
        pre-requisites for a particular course can be met.
        Doctests:
        >>> csc110 = _Course('CSC110Y1', 'Foundations of Computer Science I', [])
        >>> csc111 = _Course('CSC111H1', 'Foundations of Computer Science II', [{csc110}])
        >>> prereqs = csc111.get_prereqs()
        >>> real_prereqs = [{csc110, csc111}]
        >>> all(prereq in real_prereqs for prereq in prereqs) and all(prereq in prereqs for prereq in real_prereqs)
        True
        >>> csc108 = _Course('CSC108H1', 'Introduction to Computer Programming', [])
        >>> csc148 = _Course('CSC148H1', 'Introduction to Computer Science', [{csc108}])
        >>> csc165 = _Course('CSC165H1', 'Mathematical Expression and Reasoning for Computer Science', [])
        >>> csc236 = _Course('CSC236H1', 'Introduction to the Theory of Computation', [{csc148, csc165, csc111}])
        >>> csc240 = _Course('CSC240H1', 'Enriched Introduction to the Theory of Computation', [])
        >>> csc265 = _Course('CSC265H1', 'Enriched Data Structures and Analysis', [{csc240, csc236}])
        >>> prereqs = csc265.get_prereqs()
        >>> real_prereqs = [{csc240, csc265}, {csc111, csc110, csc236, csc265}, {csc148, csc108, csc236,csc265},{csc165, csc236, csc265}]
        >>> all(prereq in real_prereqs for prereq in prereqs) and all(prereq in prereqs for prereq in real_prereqs)
        True
        """
        if visited is None:
            visited = set()
        visited = visited.union({self})
        if len(self.prereqs) == 0:
            return [{self}]
        paths = [set()]
        for pre_req_set in self.prereqs:
            sub_paths = []
            for pre_req in pre_req_set:
                pre_req_paths = []
                if pre_req not in visited:
                    pre_req_paths = pre_req.get_prereqs(visited)
                sub_paths.extend(pre_req_paths)
            paths = get_union(paths, sub_paths)
        for path in paths:
            path.add(self)
        return paths

    def prereqs_to_set(self) -> set[_Course]:
        """
        Gives a set of all possible pre-requisites to a course.
        """
        prereq_set = set()
        for prereq in self.prereqs:
            for req in prereq:
                prereq_set.add(req)
        return prereq_set

    def path_has_prerequisite(self, path: set[_Course], completed: set[_Course]) -> bool:
        """
        Returns whether there exists a course in the path of courses which is a pre-requisite to
        """
        for course in path:
            if course in self.prereqs_to_set() and course not in completed:
                return True
        return False

    def __repr__(self) -> str:
        return self.course_code


def get_union(greater_set: list[set], smaller_set: list[set]) -> list[set]:
    """
    Helper function that returns a list of sets where each set is a union of every set in greater_set with a set in
    smaller_set.
    """
    total_paths = []
    for path in greater_set:
        for path1 in smaller_set:
            joined_path = path.union(path1)
            total_paths.append(joined_path)
    return total_paths


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
