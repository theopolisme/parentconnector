# -*- coding: utf-8 -*-

"""
parentconnector.py
========

Programmatic access to ParentConnect data

usage: parentconnector.py [-h] base_url username password

positional arguments:
  base_url    base url of the ParentConnect instance, including protocol and
              trailing slash
  username    username (typically email address) of the user to log in as
  password    password of the user to log in as

Copyright (C) 2014 Theo Patt <theo@theopatt.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

PATHS = {
    'login': 'Login.asp',
    'home': 'HomePage.asp?loadState=2',
    'assignments': 'AssignmentsGeneral.asp?StudentIndex={student_index}'
}

DURATION = 'THISSCHOOLYEAR'
DURATION_STRING = 'Assignments for this school year'

class ParentConnector(object):
    def __init__(self, base_url, username, password, phantomjs_path=None):
        self.base_url = base_url
        self.username = username
        self.password = password

        self.is_logged_in = False
        self.is_destroyed = False
        self.current_path = ''
        self.students = []

        # Create the driver
        self.driver = webdriver.PhantomJS(phantomjs_path)
        self.driver.set_window_size(1120, 550)

    def navigate_to(self, short_name, force=False, **kwargs):
        path = PATHS[short_name].format(**kwargs)

        if force or path != self.current_path:
            self.driver.get(self.base_url + path)
            self.current_path = path

    def login(self):
        if self.is_logged_in:
            return True

        self.navigate_to('login')
        username = self.driver.find_element_by_name('UserID')
        username.send_keys(self.username)
        password = self.driver.find_element_by_name('UserPwd')
        password.send_keys(self.password)
        password.submit()

        # Wait for homepage to load, indicating that we are indeed logged in
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'clHomePageStuLbl'))
            )
            self.current_path = PATHS['home'] # Since we were redirected
            self.is_logged_in = True
        except:
            self.is_logged_in = False

        return self.is_logged_in

    def get_students(self):
        self.login()

        if self.students:
            return self.students

        self.navigate_to('home')
        students = []
        for link in self.driver.find_elements_by_css_selector('.clHomePageStuLbl a'):
            students.append({
                'name': link.text,
                'index': link.get_attribute('href').split('=')[1]
            })

        self.students = students
        return students

    def get_assignments(self, student_index=False):
        self.login()

        def get_student_assignments(index):
            self.navigate_to('assignments', student_index=index)
            option = self.driver.find_element_by_css_selector('select option[value="' + DURATION + '"]')
            option.click()
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, 'clIGPTaskTimeLine'),
                    DURATION_STRING # FIXME: Make work for multiple durations
                )
            )

            soup = BeautifulSoup(self.driver.page_source)
            grade_rows = soup.select('.clIGPTaskGenTbl tr')
            grade_rows = grade_rows[1:] # Remove header row

            def get_text_if_not_empty(el):
                text = el.get_text(strip=True)
                return text if text != '-' else None

            data = []
            for row in grade_rows:
                children = map(get_text_if_not_empty, row.find_all('td'))
                data.append({
                    'course': children[0],
                    'period': children[1],
                    'assignment': children[2],
                    'type': children[3],
                    'score': children[4],
                    'due': children[5],
                    'remark': children[6],
                    'teacher': children[7]
                })

            return data

        if student_index:
            return get_student_assignments(student_index)

        output = {}
        for student in self.get_students():
            output[student['name']] = get_student_assignments(student['index'])
        return output

    def destroy(self):
        self.driver.quit()
        self.is_destroyed = True

if __name__ == '__main__':
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument('base_url', help='base url of the ParentConnect instance, including protocol and trailing slash')
    parser.add_argument('username', help='username (typically email address) of the user to log in as')
    parser.add_argument('password', help='password of the user to log in as')
    args = parser.parse_args()

    start_time = time.time()

    connector = ParentConnector(args.base_url, args.username, args.password)
    print connector.get_assignments()

    print 'Time elapsed: {}s'.format(time.time() - start_time)
