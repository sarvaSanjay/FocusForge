from __future__ import annotations
import ast
import csv

# from focus import _Course why is this here?
from course import _Course

class Graph:
    courses: dict[str, _Course]
    prereqs: set[tuple[_Course, _Course]]

# can we make it so that the file names aren't hard coded
    def __init__(self, input_file: str = 'course-data.csv') -> None:
        self.courses = {}
        self.prereqs = set()
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f=f, delimiter=';')
            for row in reader:
                course = _Course(row['code'], row['name'], [])
                self.courses[row['code']] = course
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f=f, delimiter=';')
            for row in reader:
                pre_requisites = ast.literal_eval(row['pre-requisites'])
                for prereq_code_set in pre_requisites:
                    prereq_code_set = set(prereq_code_set)
                    prereq_set = {self.courses[code] for code in prereq_code_set if code in self.courses}
                    self.courses[row['code']].prereqs.append(prereq_set)
                    for pre_req in prereq_set:
                        self.prereqs.add((self.courses[row['code']], pre_req))


if __name__ == '__main__':
    graph = Graph()
    paths = graph.courses['CSC469H1'].get_prereqs()
    for path in paths:
        print({course.course_code for course in path})

    print(graph.courses['CSC469H1'].prereqs)
