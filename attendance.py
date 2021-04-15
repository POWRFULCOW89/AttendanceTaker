import os, sys, json
import selenium as se
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Helper functions
def pplink(ls): # "Pretty print link" Displays the text properties of a list. Debug
    print(list(map(lambda x: x.text, ls)))

class CredentialsError(Exception):
    def __init__(self, msg="Credentials are invalid."):
        self.msg = msg
        super().__init__(self.msg)

class MoodleError(Exception):
    def __init__(self, msg="Moodle is currently down or the URL is not valid."):
        self.msg = msg
        super().__init__(self.msg)

class TimeoutError(Exception):
    def __init__(self, msg="Webdriver timed out. Is the server up?"):
        self.msg = msg
        super().__init__(self.msg)

class AttendanceError(Exception):
    def __init__(self, msg="The attendance page does not exist or attendance is not being taken."):
        self.msg = msg
        super().__init__(self.msg)

# There should be only one instance of a webdriver
class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# The actual singleton 
class AttendanceTaker(metaclass=Singleton):
    def __init__(self, base_url, logs=True):
        self.browser = webdriver.PhantomJS()
        self.base_url = base_url
        self.credentials = {}
        self.logs = logs

    def currentPage(self):
        return "Current page: " + self.browser.title + " at: " + self.browser.current_url
    
    def logPage(self):
        if self.logs:
            return "Current page: {0} at: {1}".format(self.browser.title, self.browser.current_url)

    def isURLValid(self):
        if self.currentPage() == "Error":
            raise MoodleError

    def loadCredentials(self, file):
        with open(file) as json_file:
            self.credentials = json.load(json_file)

    def login(self):
        starterURL = "{0}/login/index.php".format(self.base_url)
        try:
            # Getting there
            self.browser.get(starterURL)

            # and assuring it
            self.isURLValid()
            print(self.logPage())

            # Inputting credentials
            username = self.browser.find_element_by_id("username")
            username.send_keys(self.credentials["username"])
            password = self.browser.find_element_by_id("password")
            password.send_keys(self.credentials["password"])

            # Submitting credentials
            self.browser.find_element_by_id("loginbtn").submit()

        except NoSuchElementException:
            raise MoodleError

        except TimeoutException:
            raise TimeoutError

        if starterURL == self.browser.current_url:
            raise CredentialsError

        self.isURLValid()

    def navigateToCourseById(self, courseId):
        # Locate course. 
        self.browser.get("{0}/course/view.php?id={1}".format(self.base_url, courseId))
        self.isURLValid()
        self.logPage()

    def navigateToAttendanceById(self, attendanceListId): # Currently unused.
        # Locate attendance list. 
        self.browser.get("{0}/mod/attendance/view.php?id={1}".format(self.base_url, attendanceListId))
        self.isURLValid()
        self.logPage()

    def takeAttendance(self): # Assuming the webdriver is currently on a course page.
        try:
            # Grab all links that lead to attendance lists.
            attendanceLinks = self.browser.find_elements_by_class_name("aalink")

            if len(attendanceLinks) == 0:
                raise AttendanceError

            for link in attendanceLinks[:]:
                href = link.get_attribute("href")
                if "attendance" not in href:
                    attendanceLinks.remove(link)

            # Submit attendance     (CURRENTLY UNTESTED)
            for link in attendanceLinks:
                try:
                    # Navigating to the attendance page
                    self.browser.get(link.get_attribute("href"))

                    self.isURLValid()

                    print(self.logPage())

                    # Click the link leading to checkout
                    self.browser.find_elements_by_xpath("//*[contains(@href, 'attendance/attendance')]")[0].click()

                    # Click the first radio input
                    self.browser.find_elements_by_class_name("form-check-input")[0].click()

                    # # Clicking ok. We don't need a ref.
                    self.browser.find_element_by_name("submitbutton").click()

                    print("Attendance taken at: " + self.browser.current_url)
                except:
                    # print("Error: No current attendance at: " + self.browser.current_url)
                    pass

        except NoSuchElementException: #TODO: Remove double warning
            raise 

    def logout(self):
        try:
            # Click the user panel.
            self.browser.find_element_by_id("action-menu-toggle-1").click()
            # Click the logout button. Can't click if the panel was hidden. TODO: Is there an URL for logging out?
            self.browser.find_element_by_xpath("//a[@data-title='logout,moodle']").click()
            print(self.logPage())

        except NoSuchElementException:
            raise MoodleError

    def exit(self):
        self.browser.quit()
        