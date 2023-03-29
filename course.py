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


