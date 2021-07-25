import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import datetime


class EnvSetup(unittest.TestCase):
    def setUp(self):
        print("Environment Setup")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        print("TestScript Run Started: " + str(datetime.datetime.now()))
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()

    def tearDown(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()
            print("Environment Destroyed")
            print("TestScript Run Completed:" + str(datetime.datetime.now()))
