import typing
class _Course():
    course_code: str
    name: str
    prereqs: set[_Course]

    def __init__(self, code: str, name: str, prereqs: set[_Course]):
        self.course_code = code
        self.name = name
        self.prereqs = prereqs

    def get_prereqs(self):
        # nooooooo, it's too hard


class Program():
    name: str
    course_reqs = set[set[_Course]]
    credits_req = float
    program_code = str

    def __init__(self, name, courses_reqs, credits_req, program_code):
        self.name = name
        self.course_reqs = courses_reqs
        self.credits_req = credits_req
        self.program_code = program_code
class Focus(Program):
    def
