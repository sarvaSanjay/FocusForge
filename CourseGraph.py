from __future__ import annotations
import ast
import csv

import re
from main_question_mark import _Course

class Graph:
    courses: dict[str, _Course]
    edges: set[tuple[_Course, _Course]]

    def __init__(self) -> None:
        self.courses = {}
        self.edges = set()
        with open('course-data.csv', 'r') as f:
            reader = csv.DictReader(f=f, delimiter=';')
            for row in reader:
                course = _Course(row['code'], row['name'], [{}])
                self.courses[row['code']] = course
        with open('course-data.csv', 'r') as f:
            reader = csv.DictReader(f=f, delimiter=';')
            for row in reader:
                pre_requisites = list(row['pre-requisites'])
                pre_requisites = ast.literal_eval(row['pre-requisites'])
                for prereq_code_set in pre_requisites:
                    prereq_code_set = set(prereq_code_set)
                    prereq_set = {self.courses[code] for code in prereq_code_set if code in self.courses}
                    self.courses[row['code']].prereqs.append(prereq_set)
                    for pre_req in prereq_set:
                        self.edges.add((self.courses[row['code']], pre_req))


if __name__ == '__main__':
    graph = Graph()
    print('hi')
    print(len(graph.edges))