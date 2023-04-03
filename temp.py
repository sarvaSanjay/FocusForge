import requests

from focus import setup_minimal_focii, complete_minimal_focus, rank_path
from pprint import pprint
from course_graph import Graph, get_schedule

# Web and Internet Technologies
#
g = Graph()
print(g.courses['CSC457H1'].prereqs)
focus = setup_minimal_focii('focus-data.csv')[15]
complete_minimal_focus(g, focus, 'focus-data.csv')
print(len(focus.course_reqs))
completed = {g.courses['MGT100H1']}
paths = focus.get_paths(completed=completed)
print(len(paths))
i = 0
j = 0
for path in paths:
    print(rank_path(path, completed=completed), get_schedule(path))
    i += 1
    if i == 10:
        break
#print(len([focus.course_reqs[i] == focus.course_reqs[j] and i != j for i in range(len(focus.course_reqs)) for j in range(i, len(focus.course_reqs)) if focus.course_reqs[i] == focus.course_reqs[j] and i != j]))
