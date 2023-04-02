from focus import setup_minimal_focii, complete_minimal_focus, rank_path
from pprint import pprint
from CourseGraph import Graph, get_schedule

# Web and Internet Technologies
#
g = Graph()
focus = setup_minimal_focii('focus-data.csv')[8]
complete_minimal_focus(g, focus, 'focus-data.csv')
print(focus.course_reqs)
completed = {g.courses['CSC110Y1'], g.courses['CSC111H1'], g.courses['MAT137Y1']}
paths = focus.get_paths(completed=completed)
print(len(paths))
i = 0
j = 0
for path in paths:
    print(rank_path(path, completed=completed), get_schedule(path))
    i += 1
    if i == 10:
        break
print(len([focus.course_reqs[i] == focus.course_reqs[j] and i != j for i in range(len(focus.course_reqs)) for j in range(i, len(focus.course_reqs)) if focus.course_reqs[i] == focus.course_reqs[j] and i != j]))
