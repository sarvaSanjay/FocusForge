import csv
import requests
from bs4 import BeautifulSoup
import re


class Scraper:
    """
    Creates a scraper object that scrapes data from the Arts and Science Calendar.
    """

    def __init__(self) -> None:
        url_part_1 = 'https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/'
        url_part_2 = 'debug?course_keyword=&field_section_value=All&field_prerequisite_value=&'
        url_part_3 = 'field_breadth_requirements_value=All&field_distribution_requirements_value=All'
        r = requests.get(url_part_1 + url_part_2 + url_part_3)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def get_course_soups(self) -> list[BeautifulSoup]:
        """
        Returns a list of beautiful soup objects for each course in the academic calendar.
        Preconditions:
        - Assumes that each course is in an HTML div of class "no-break views-row"
        """
        courses = self.soup.find_all("div", class_="no-break views-row")
        course_soups = [BeautifulSoup(str(course), 'html.parser') for course in courses]
        return course_soups

    def get_course_codes_and_names(self) -> tuple[list[str], list[str]]:
        """
        Returns a tuple of two lists: a list of course codes and a list of course names.
        Assumes that the title of each course can be found in an h3 tag in each course soup.
        """
        course_soups = self.get_course_soups()
        course_titles = [str(soup.find('h3')).strip()[4:-5] for soup in course_soups]
        course_codes = [course.split('-')[0].strip() for course in course_titles]
        course_names = [course.split('-')[1].strip() for course in course_titles]
        return course_codes, course_names

    def get_prereq_soups(self) -> list[BeautifulSoup]:
        """
        Returns a list of beautiful soup objects for the pre-requisites of each course.
        Assumes that each course's prerequisite data is stored in a span titled
        "views-field views-field-field-prerequisite".
        If a course's pre-requisite info is not present, its soup object is a BeautifulSoup object of empty string.
        """
        course_soups = self.get_course_soups()
        prereq_soups = []
        for soup in course_soups:
            prereq_data_html = soup.find("span", class_="views-field views-field-field-prerequisite")
            if prereq_data_html:
                prereq_soup = BeautifulSoup(str(prereq_data_html), "html.parser")
            else:
                prereq_soup = BeautifulSoup('', 'html.parser')
            prereq_soups.append(prereq_soup)
        return prereq_soups

    def get_pre_reqs(self) -> list[list[set[str]]]:
        """
        Returns a list of pre-requisite courses for each course in the academic calender.
        Assumes that each course pre-requisite is in a link tag and is a course-code of 8 characters.
        This implementation does not account for any co-requisites and more complex requirements like 4.0 credits should
        be completed.
        """
        prereq_soups = self.get_prereq_soups()
        pre_reqs = []
        for prereq_soup in prereq_soups:
            prereq_html = str(prereq_soup.find("span", class_="field-content"))
            split_courses = prereq_html.split(';')
            pre_req_list = []
            for courses in split_courses:
                soup = BeautifulSoup(courses, "html.parser")
                course_names = get_valid_links(soup)
                if len(course_names) != 0:
                    pre_req_list.append(course_names)
            pre_reqs.append(pre_req_list)
        return pre_reqs

    def get_csv_file(self) -> None:
        """
        Creates a csv file with course data.
        """
        codes, names = self.get_course_codes_and_names()
        pre_requisites = self.get_pre_reqs()
        with open('course-data.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['code', 'name', 'pre-requisites'])
            for i in range(len(codes)):
                writer.writerow([codes[i], names[i], pre_requisites[i]])


def get_valid_links(soup: BeautifulSoup) -> set[str]:
    """
    Helper function that returns a list of valid links in the pre-requisite soup.
    A valid link is that which has exactly 8 characters.
    """
    links = soup.find_all('a')
    valid_links = set()
    for link in links:
        name = re.findall('>(.+)<', str(link))[0]
        if len(name) == 8:
            valid_links.add(name)
    return valid_links


if __name__ == '__main__':
    scraper = Scraper()
    scraper.get_csv_file()
