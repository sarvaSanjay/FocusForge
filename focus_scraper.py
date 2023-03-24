import csv
import requests
from bs4 import BeautifulSoup
import re

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
            completion_data_html = soup.find("span" , class_ = "views-field views-field-field-completion-requirements")
            completion_soup = BeautifulSoup(str(completion_data_html), "html.parser")
            completion_soups.append(completion_soup)
        return completion_soups


if __name__ == '__main__':
    scraper = FocusScraper()
    reqrs = scraper.get_completion_soups()
    print(len(reqrs))