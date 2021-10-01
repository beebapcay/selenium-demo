import time
import unittest
from time import sleep

import pandas as pd

from EnvSetup import *
from DataManipulation import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pathlib import Path
import mysql.connector
import os


def perform_login(driver, username, password):
    """Perform login account in authentication page"""

    actions = ActionChains(driver)

    username_input = driver.find_element(By.ID, "txtUsername")
    # username_input.send_keys(username)
    actions.send_keys_to_element(username_input, username)

    password_input = driver.find_element(By.ID, "txtPassword")
    # password_input.send_keys(password)
    actions.send_keys_to_element(password_input, password)

    login_btn = driver.find_element(By.ID, "btnLogin")
    # login_btn.click()
    actions.click(login_btn)

    actions.perform()
    time.sleep(1)


def navigate_add_employee_page(driver):
    """Perform choose feature add employee in pim menu"""

    pim_menu_btn = driver.find_element(By.ID, "menu_pim_viewPimModule")
    pim_menu_btn.click()

    add_btn = driver.find_element(By.ID, "btnAdd")
    add_btn.click()
    time.sleep(1)


def navigate_add_user_page(driver):
    """Perform choose feature add user in admin menu"""

    admin_menu_btn = driver.find_element(By.ID, "menu_admin_viewAdminModule")
    admin_menu_btn.click()

    add_btn = driver.find_element(By.ID, "btnAdd")
    add_btn.click()
    time.sleep(1)


def perform_add_employee(driver, firstname, middlename, lastname, employee_id, photofile_name):
    """Perform input info for new employee"""

    if firstname:
        firstname_input = driver.find_element(By.ID, "firstName")
        firstname_input.send_keys(firstname)

    if middlename:
        middlename_input = driver.find_element(By.ID, "middleName")
        middlename_input.send_keys(middlename)

    if lastname:
        lastname_input = driver.find_element(By.ID, "lastName")
        lastname_input.send_keys(lastname)

    if employee_id:
        id_input = driver.find_element(By.ID, "employeeId")
        id_input.clear()
        id_input.send_keys(employee_id)

    if photofile_name:
        photograph_file = driver.find_element(By.ID, "photofile")
        photograph_file.send_keys(str(Path("../data/attach/" + str(photofile_name)).resolve()))

    save_btn = driver.find_element(By.ID, "btnSave")
    save_btn.click()
    time.sleep(1)


def perform_add_user(driver, role, username, password, name):
    """Perform input info for new user"""

    role_select = Select(driver.find_element(By.ID, "systemUser_userType"))
    role_select.select_by_visible_text(role)

    emp_name = driver.find_element(By.ID, "systemUser_employeeName_empName");
    emp_name.send_keys(name)
    time.sleep(1)

    username_input = driver.find_element(By.ID, "systemUser_userName")
    username_input.send_keys(username)
    time.sleep(1)

    password_input = driver.find_element(By.ID, "systemUser_password")
    password_input.send_keys(password)
    time.sleep(1)

    repassword_input = driver.find_element(By.ID, "systemUser_confirmPassword")
    repassword_input.send_keys(password)
    time.sleep(1)

    save_btn = driver.find_element(By.ID, "btnSave")
    save_btn.click()
    time.sleep(2.5)


class AutoScript(EnvSetup):
    def test_script(self):
        """Functional automation testing for adding a new user"""

        # read data
        testdata_path = "../data/add_user_data.csv"
        testdata_df = read_test_data(testdata_path)
        testdata_df = testdata_df.fillna("")
        admin_user = "Admin"
        admin_pwd = "Beebapcay2000+"

        # url navigation
        base_url = "http://localhost/orangehrm-4.5"

        # navigate orangehrm root
        self.driver.get(base_url)

        # perform login
        perform_login(self.driver, admin_user, admin_pwd)

        for index, row in testdata_df.iterrows():

            first_name = row["first_name"]
            middle_name = row["middle_name"]
            last_name = row["last_name"]
            employee_id = row["id"]
            photofile = row["photofile"]

            role = row["role"]
            username = row["username"]
            password = row["password"]

            # navigate to add employee in menu pim
            navigate_add_employee_page(self.driver)

            # perform input data for adding employee
            perform_add_employee(self.driver, first_name, middle_name, last_name, employee_id, photofile)

            # navigate to add user in menu admin
            navigate_add_user_page(self.driver)

            # perform input data for adding user
            perform_add_user(self.driver, role, username, password, first_name + " " + middle_name + " " + last_name)


if __name__ == "__main__":
    unittest.main()
