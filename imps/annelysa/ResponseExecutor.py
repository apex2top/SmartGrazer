import os
from sys import platform
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ResponseExecutor(object):
    _driver = None

    def __init__(self, driver):
        if driver == 'Firefox':
            self._driver = webdriver.Firefox(executable_path=r'webdriver/'+self._getOS()+'/geckodriver')
        else:
            self._driver = webdriver.Chrome(executable_path=r'webdriver/'+self._getOS()+'/chromedriver')

    def _getOS(self):
        if platform == "linux" or platform == "linux2":
            return "linux"
        elif platform == "win32":
            return "windows"

    def execute(self, file):
        htmlfile = "file://" + os.getcwd() + "/" + file

        self._driver.get(htmlfile)

        try:
            WebDriverWait(self._driver, 1).until(EC.alert_is_present(),
                                                 'Timed out waiting for PA creation ' +
                                                 'confirmation popup to appear.')

            self._driver.switch_to.alert.accept()
            return True
        except TimeoutException:
            return False
