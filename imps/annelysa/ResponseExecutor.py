import logging
import os
from sys import platform
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.remote_connection import LOGGER

class ResponseExecutor(object):
    """ This class is responsible for opening the website-responses in the browser to check wether there is an alert or not.


        :param driver: The Name of the webdriver
        :type input: str.
    """
    _driver = None

    def __init__(self, driver):
        LOGGER.setLevel(logging.WARNING)
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
        """ This method opens the given file with the configured webdriver.


            :param file: The file to open
            :type input: str.

            :returns: boolean: Wether an alert box was found or not.
        """
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
        self._driver.close()