import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug?course_keyword=&field_section_value=All&field_prerequisite_value=&field_breadth_requirements_value=All&field_distribution_requirements_value=All')
soup = BeautifulSoup(r.text, 'html.parser')
courses = soup.find_all("div", class_="no-break views-row")
course = courses[0]
course_soups = [BeautifulSoup(str(course), 'html.parser') for course in courses]
course_titles = [str(soup.find('h3')).strip()[4:-5] for soup in course_soups]
course_code = [course.split('-')[0].strip() for course in course_titles]
course_names = [course.split('-')[1].strip() for course in course_titles]

pre_reqs = []
for soup in course_soups:
    prereq_data_html = soup.find("span" , class_ = "views-field views-field-field-prerequisite")
    if prereq_data_html:
        prereq_soup = BeautifulSoup(str(prereq_data_html), "html.parser")
    else:
        prereq_soup = BeautifulSoup('', 'html.parser')
    prereq_html = str(prereq_soup.find("span", class_ = "field-content"))
    split_courses = prereq_html.split(';')
    pre_req_list = []
    for courses in split_courses:
        soup = BeautifulSoup(courses, "html.parser")
        links = soup.find_all('a')
        pre_names = []
        for link in links:
            pre_names.append(re.findall('>(.+)<', str(link))[0])
        pre_req_list.append(pre_names)

    pre_reqs.append(pre_req_list)

# for pre_req in pre_reqs[0:500]:
#     print(pre_req)
with open('course_preeqs.txt', 'w') as f:
    for pre_req in pre_reqs:
        f.write(str(pre_req) + '\n')
print(course_names[:100])
print(len(pre_reqs) == len(course_names))