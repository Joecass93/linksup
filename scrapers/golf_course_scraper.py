import pandas as pd
import requests
from bs4 import BeautifulSoup
import googlemaps
from datetime import datetime
import re

class Main():

    def __init__(self):

        self.url = "http://www.golfnationwide.com"
        self.courses = {}
        print "getting all state urls..."
        self._get_states()
        for link in self.links:
            state = (link.split('State/', 1)[1]).split('-', 1)[0]
            print ""
            print "getting all courses in {}".format(state)
            self._get_courses_by_state(link)

        self._build_df()
        self.df.to_csv('courses.csv')

    def _get_states(self):
        page = requests.get(self.url, timeout=5)
        soup = BeautifulSoup(page.content, "html.parser")

        links = soup.find_all('a', {'href': re.compile('/Golf-Courses-By-State')})
        links = [ str(link).split('href="', 1)[1] for link in links ]
        links = [ link.split('" ', 1)[0] for link in links ]
        links = [ '{}{}'.format(self.url, link) for link in links ]
        self.links = links

    def _get_courses_by_state(self, link):
        page = requests.get(link, timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')

        links = soup.find_all('a', {'href': re.compile('/Golf-Courses-By-State')})
        links = [ str(link).split('href="', 1)[1] for link in links ]
        links = [ link.split('" ', 1)[0] for link in links ]
        links = [ '{}{}'.format(self.url, link) for link in links ]

        for link in links:
            self._store_courses(link)

    def _store_courses(self, url):
        page = requests.get(url, timeout=5)
        page_content = BeautifulSoup(page.content, "html.parser")

        try:
            course = page_content.find_all('span', id='ctl00_MainContentPlaceholder_CourseNameLabel')[0]
            course = course.get_text()
        except Exception as e:
            course = "missing"
        try:
            link = page_content.find_all("a", id='ctl00_MainContentPlaceholder_WebAddressLink')[0]
            link = (str(link).split('href="', 1)[1]).split('" ', 1)[0]
        except Exception as e:
            link = "missing"

        self.courses[str(course)] = link

    def _build_df(self):
        self.df = pd.DataFrame()
        for course, url in self.courses.iteritems():
            temp = pd.DataFrame({'course':[course], 'url':[url]})
            self.df = self.df.append(temp)

if __name__ == "__main__":
    Main()
