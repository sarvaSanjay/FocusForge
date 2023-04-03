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

    def __init__(self, code: str, name: str, prereqs: list[set[_Course]]):
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
        """
        # if course is CSC265, prereqs are CSC240 or CSC236 (excluding coreqs)
        # CSC240 prereqs are none
        # CSC236 prereqs are (CSC148 and CSC165) OR CSC(csc111)
        # so this methods returns {{CSC240}, {CSC236, CSC148, CSC165}, {CSC236, CSC111}}
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
