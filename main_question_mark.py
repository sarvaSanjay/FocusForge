from __future__ import annotations
class _Course():
    course_code: str
    name: str
    # ERROR: At least read the proposal. The prereqs are list of sets of courses because some prereqs have multiple options. Like MAT137/ MAT157 but not both.
    prereqs: set[_Course]
    credits: float

    def __init__(self, code: str, name: str, prereqs: set[_Course]):
        self.course_code = code
        self.name = name
        self.prereqs = prereqs
        # ERROR: Do 'Y1' instead of 'Y' cos course codes like PSY270H1 exist.
        if 'Y' in self.course_code:
            self.credits = 1.0
        else:
            self.credits = 0.5

    def get_prereqs(self) -> set[set[_Course]]:
        # if course is CSC265, prereqs are CSC240 or CSC236 (excluding coreqs)
        # CSC240 prereqs are none
        # CSC236 prereqs are (CSC148 and CSC165) OR CSC(csc111)
        # so this methods returns {{CSC240}, {CSC236, CSC148, CSC165}, {CSC236, CSC111}}
        return # nooooooo, it's too hard


class Focus():
    name: str
    # ERROR: You cannot do set of set. Sets are unhashable. We need to work on this.
    course_reqs = set[set[_Course]] #top  level prereqs
    credits_req = float
    program_code = str

    def __init__(self, name: str, courses_reqs: set[set[_Course]], credits_req: float, program_code: str):
        self.name = name
        self.course_reqs = courses_reqs
        self.credits_req = credits_req
        # QUESTION: What exactly do you mean by program_code?
        self.program_code = program_code

    def credits_left(self, completed: set[_Course]) -> float:
        total_preqreqs = []
        for path in self.course_reqs:
            temp_set = set()
            for course in path:
                temp_set.add(course)
            total_prereqs.append(path.


