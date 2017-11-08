import logging
import os
from sys import platform
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ResponseExecutor(object):
    """ This class is responsible for opening the website-responses in the browser to check wether there is an alert or not.


        :param driver: The Name of the webdriver
        :type input: str.
    """
    _driver = None
    _driverName = ''

    def __init__(self, driver):
        self._driverName = driver

    def _getOS(self):
        if platform == "linux" or platform == "linux2":
            return "linux"
        elif platform == "win32":
            return "windows"

    def _getDriver(self):
        if self._driverName == 'Firefox':
            self._driver = webdriver.Firefox(executable_path=r'webdriver/'+self._getOS()+'/geckodriver')
        elif self._driverName == 'Chrome':
            self._driver = webdriver.Chrome(executable_path=r'webdriver/'+self._getOS()+'/chromedriver')


    def execute(self, file):
        """ This method opens the given file with the configured webdriver.


            :param file: The file to open
            :type input: str.

            :returns: boolean: Wether an alert box was found or not.
        """
        if not self._driver:
            self._getDriver()

        htmlfile = "file://" + os.getcwd() + "/" + file

        if os.path.isfile(os.getcwd() + "/" + file):
            self._driver.get(htmlfile)

            try:
                WebDriverWait(self._driver, 1).until(EC.alert_is_present(),
                                                     'Timed out waiting for PA creation ' +
                                                     'confirmation popup to appear.')

                self._driver.switch_to.alert.accept()
                return True
            except TimeoutException:
                return False
        else:
            logging.getLogger("SmartGrazer").warning("Response file: " + os.getcwd() + "/" + file + " was not found! Skipping by returning False.")
            return False

    def close(self):
        if self._driver:
            self._driver.close()