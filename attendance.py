import os, sys, json
import selenium as se
from selenium import webdriver

# Helper functions
def pplink(ls): # "Pretty print link" Displays the text properties of a list. Debug
    print(list(map(lambda x: x.text, ls)))


# There should be only one instance of a webdriver
class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# The actual singleton 
class AttendanceTaker(metaclass=Singleton):
    def __init__(self, base_url):
        self.browser = webdriver.PhantomJS()
        self.base_url = base_url
        self.credentials = {}

    def currentPage(self):
        return self.browser.title

    def loadCredentials(self, file):
        with open(file) as json_file:
            self.credentials = json.load(json_file)

    def login(self):
        # Getting there
        self.browser.get("{0}/login/index.php".format(self.base_url))

        # Inputting credentials
        username = self.browser.find_element_by_id("username")
        username.send_keys(self.credentials["username"])
        password = self.browser.find_element_by_id("password")
        password.send_keys(self.credentials["password"])

        # Submitting credentials
        self.browser.find_element_by_id("loginbtn").submit()

    def navigateToCourseById(self, courseId):
        # Locate course. 
        self.browser.get("{0}/course/view.php?id={1}".format(self.base_url, courseId))

    def navigateToAttendanceById(self, attendanceListId):
        # Locate attendance list. 
        self.browser.get("{0}/mod/attendance/view.php?id={1}".format(self.base_url, attendanceListId))

    def takeAttendance(self): # Assuming the webdriver is currently on a course page.
        # Grab all links that lead to attendance lists.
        attendanceLinks = self.browser.find_elements_by_class_name("aalink")
        for link in attendanceLinks[:]:
            href = link.get_attribute("href")
            if "attendance" not in href:
                attendanceLinks.remove(link)

        # Submit attendance     (CURRENTLY UNTESTED)
        for link in attendanceLinks:
            # Navigating to the attendance page
            self.browser.get(link.get_attribute("href"))
            # Getting all possible links                 
            attendanceBtns = self.browser.find_elements_by_class_name("form-check-input")
            for btn in attendanceBtns:
                btn.click()     # Might lead to unstable behavior

            # Clicking ok. We don't need a ref.
            self.browser.find_element_by_name("submitbutton").click()

    def logout(self):
        # Click the user panel.
        self.browser.find_element_by_id("action-menu-toggle-1").click()
        # Click the logout button. Can't click if hidden.
        self.browser.find_element_by_xpath("//a[@data-title='logout,moodle']").click()

    def exit(self):
        self.browser.quit()