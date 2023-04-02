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

    # TODO add type hint for visited
    def get_prereqs(self, visited: set = set()) -> list[set[_Course]]:  # can't have set in set
        # if course is CSC265, prereqs are CSC240 or CSC236 (excluding coreqs)
        # CSC240 prereqs are none
        # CSC236 prereqs are (CSC148 and CSC165) OR CSC(csc111)
        # so this methods returns {{CSC240}, {CSC236, CSC148, CSC165}, {CSC236, CSC111}}
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

    def get_prereqs_left(self, completed: set[_Course]) -> list[set[_Course]]:
        prereqs_list = self.get_prereqs()
        for prereq_set in prereqs_list:
            for completed_course in completed:
                if completed_course in prereq_set:
                    prereq_set.remove(completed_course)
        return prereqs_list

    def __repr__(self) -> str:
        return self.course_code


def get_union(greater_set: list[set], smaller_set: list[set]):
    total_paths = []
    for path in greater_set:
        for path1 in smaller_set:
            joined_path = path.union(path1)
            total_paths.append(joined_path)
    return total_paths
