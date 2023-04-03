import requests

from focus import setup_minimal_focii, complete_minimal_focus, rank_path
from pprint import pprint
from course_graph import Graph, get_schedule

# Web and Internet Technologies
#
g = Graph()
print(g.courses['STA237H1'].prereqs)
focus = setup_minimal_focii('focus-data.csv')[8]
complete_minimal_focus(g, focus, 'focus-data.csv')
print(focus.course_reqs)
completed = set()
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

url_part_1 = 'https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/'
url_part_2 = 'debug?course_keyword=&field_section_value=All&field_prerequisite_value=&'
url_part_3 = 'field_breadth_requirements_value=All&field_distribution_requirements_value=All'
r = requests.get(url_part_1 + url_part_2 + url_part_3)
