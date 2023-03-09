import requests
from bs4 import BeautifulSoup

r = requests.get('https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug?course_keyword=&field_section_value=All&field_prerequisite_value=&field_breadth_requirements_value=All&field_distribution_requirements_value=All')
soup = BeautifulSoup(r.text, 'html.parser')
courses = soup.find_all("div", class_="no-break views-row")
course = courses[0]
course_soups = [BeautifulSoup(str(course), 'html.parser') for course in courses]
course_names = [str(soup.find('h3')).strip()[4:-5] for soup in course_soups]
course_code = [course.split('-')[0].strip() for course in course_names]
with open('course_code.txt', 'w') as f:
    for code in course_code:
        f.write(code + '\n')
print(course_code)