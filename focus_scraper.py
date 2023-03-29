import csv
import random
import requests
from bs4 import BeautifulSoup
import re
from scraper import get_valid_links

class FocusScraper:
    def __init__(self) -> None:
        r = requests.get('https://artsci.calendar.utoronto.ca/print/view/pdf/search_programs/print_page/debug?combine=&type=4&field_subject_area_prog_search_value=All')
        self.soup = BeautifulSoup(r.text, 'html.parser')
    
    def get_focus_soups(self) -> list[BeautifulSoup]:
        """
        Returns a list of beautiful soup objects for each focus in the academic calender.
        Assumes that each focus is in an HTML div of class "views-row"
        """
        focuses = self.soup.find_all("div", class_="views-row")
        focus_soups = [BeautifulSoup(str(focus), 'html.parser') for focus in focuses]
        return focus_soups
    
    def get_focus_names(self) -> list[str]:
        """
        Returns a tuple of two lists: a list of course codes and a list of course names.
        Assumes that the title of each course can be found in an h3 tag in each course soup.
        """
        focus_soups = self.get_focus_soups()
        focus_titles = [str(soup.find('h2')).strip()[4:-5] for soup in focus_soups]
        return focus_titles
    
    def get_completion_soups(self) -> list[BeautifulSoup]:
        """
        Returns a list of beautiful soup objects for the completion requirements of each focus.
        Assumes that each focus' completion data is stored in a span titled "views-field views-field-field-completion-requirements".
        """
        focus_soups = self.get_focus_soups()
        completion_soups = []
        for soup in focus_soups:
            completion_data_html = soup.find("div" , class_ = "views-field views-field-field-completion-requirements")
            completion_soup = BeautifulSoup(str(completion_data_html), "html.parser")
            completion_soups.append(completion_soup)
        return completion_soups

    def get_cmb(self):
        focus_titles = self.get_focus_names()
        focus_completion_soups = self.get_completion_soups()
        cmb_data = []
        titles = []
        for i, soup in enumerate(focus_completion_soups):
            if ('Cell &amp; Molecular Biology') in focus_titles[i]:
                data = cmb_focus(soup)
                cmb_data.append(data)
                titles.append(focus_titles[i])
        return cmb_data, titles
    
    def get_ssv_file(self):
        reqrs, titles = scraper.get_cmb()
        with open('focus-data.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Title', 'requirements'])
            for i in range(len(titles)):
                writer.writerow([titles[i], reqrs[i]])


def analyse_requirememts(soup: BeautifulSoup) -> str:
    lis = soup.find("ol")
    if not lis:
        return "Cell & Molecular Biology Major"
    else:
        list_soup = BeautifulSoup(str(lis), 'html.parser')
        li_items = list_soup.findAll('li')
        f_credits = 0.0
        for li in li_items:
            f_credits += credits_specified(str(li))
        return f_credits


def cmb_focus(soup: BeautifulSoup):
    reqrs = str(soup.find_all('p')[1])
    split_reqrs = reqrs.split('<br/>')
    course_credit_data = []
    for req in split_reqrs:
        data = find_course_and_credits_cmb(req)
        if data:
            course_credit_data.append(data)
    return course_credit_data


def find_course_and_credits_cmb(req: str):
    credits = re.findall('\d\.\d', req)
    if credits:
        credits = float(credits[0])
        split_req = req.split(',')
        courses = []
        for course_set in split_req:
            course_soup = BeautifulSoup(course_set, 'html.parser')
            course = random.choice(list(get_valid_links(course_soup)))
            courses.append(course)
        return credits, courses


def credits_specified(li: str):
    credits = re.findall('\d\.\d', li)
    if credits:
        return float(credits[0])
    else:
        sections = li.split(',')
        credits = 0
        for section in sections:
            if 'H1' in section:
                credits += 0.5
            elif 'Y1' in section:
                credits += 1.0
        return credits

if __name__ == '__main__':
    scraper = FocusScraper()
    scraper.get_ssv_file()