import time
import unittest
from time import sleep

import pandas as pd

from EnvSetup import *
from DataManipulation import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import mysql.connector
import os


def delete_db_exist_id(_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="orangehrm_mysql"
    )
    cursor = db.cursor()
    delete_id_query = "delete from hs_hr_employee where employee_id = %s"
    cursor.execute(delete_id_query, (_id,))
    db.commit()

    cursor.close()
    db.close()


def is_exists_id(_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="orangehrm_mysql"
    )
    cursor = db.cursor()
    id_query = "select * from hs_hr_employee where employee_id = %s"
    cursor.execute(id_query, (_id,))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    if result is None:
        return False
    return True


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


def perform_add_employee(driver, firstname, middlename, lastname, employee_id, photofile_name):
    """Perform input info for new employee"""

    if firstname:
        firstname_input = driver.find_element(By.ID, "firstName")
        firstname_input.send_keys(firstname)
        time.sleep(1)

    if middlename:
        middlename_input = driver.find_element(By.ID, "middleName")
        middlename_input.send_keys(middlename)
        time.sleep(1)

    if lastname:
        lastname_input = driver.find_element(By.ID, "lastName")
        lastname_input.send_keys(lastname)
        time.sleep(1)

    if employee_id:
        id_input = driver.find_element(By.ID, "employeeId")
        id_input.clear()
        id_input.send_keys(employee_id)
        time.sleep(1)

    if photofile_name:
        photograph_file = driver.find_element(By.ID, "photofile")
        photograph_file.send_keys(str(Path("../data/attach/" + str(photofile_name)).resolve()))
        time.sleep(1)

    save_btn = driver.find_element(By.ID, "btnSave")
    save_btn.click()
    time.sleep(1)


def check_valid_add_employee_form(driver, firstname, middlename, lastname, employee_id, photofile_name):
    """Check form add employee is valid"""

    if not firstname:
        valid_err = driver.find_element(By.CSS_SELECTOR, "#firstName + .validation-error")
        assert valid_err.text == "Required"  # checkpoint for require field

    if not lastname:
        valid_err = driver.find_element(By.CSS_SELECTOR, "#lastName + .validation-error")
        assert valid_err.text == "Required"  # checkpoint for require field

    if not employee_id:
        valid_err = "Failed To Save: Employee Id Exists"
        assert valid_err not in driver.page_source  # checkpoint for exist id

    if photofile_name:
        if os.path.splitext(photofile_name)[1] not in [".png", ".jpg", ".gif"]:
            valid_err = "Failed to Save: File Type Not Allowed"
            assert valid_err not in driver.page_source  # checkpoint for file in .png, .jpg, .gif

        path = Path("../data/attach/" + str(photofile_name))
        if path.stat().st_size > 1_000_000:
            valid_err = "Failed To Save: File Size Exceeded"
            assert valid_err not in driver.page_source  # checkpoint for file size > 1MB


def check_valid_result_info(driver, firstname, middlename, lastname, employee_id, photofile_name):
    firstname_result = driver.find_element(By.ID, "personal_txtEmpFirstName")
    assert firstname_result.getAttribute("value") == firstname

    middlename_result = driver.find_element(By.ID, "personal_txtEmpMiddleName")
    assert middlename_result.getAttribute("value") == middlename

    lastname_result = driver.find_element(By.ID, "personal_txtEmpLastName")
    assert lastname_result.getAttribute("value") == lastname

    id_result = driver.find_element(By.ID, "personal_txtEmployeeId")
    assert id_result.getAttribute("value") == employee_id


def is_accept_photofile(photofile):
    path = Path("../data/attach/" + str(photofile))
    if os.path.splitext(photofile)[1] not in [".jpg", ".png", ".gif"]:
        return False
    if path.stat().st_size > 1_000_000:
        return False
    return True


class TestScript(EnvSetup):
    def test_script(self):
        """Functional automation testing for adding a new employee"""

        # read testdata
        testdata_path = "../data/testdata.csv"
        testdata_df = read_test_data(testdata_path)
        testdata_df = testdata_df.fillna("")
        admin_user = "admin"
        admin_pwd = "Beebapcay2000+"

        # clear exist id
        id_set = set(testdata_df["id"])
        id_set.discard("0001")
        for _id in id_set:
            delete_db_exist_id(_id)

        # url navigation
        base_url = "http://localhost/orangehrm-4.5"
        login_url = base_url + "/symfony/web/index.php/auth/login"
        dashboard_url = base_url + "/symfony/web/index.php/dashboard"
        add_employee_url = base_url + "/symfony/web/index.php/pim/addEmployee"

        try:
            # navigate orangehrm root
            self.driver.get(base_url)
            assert self.driver.current_url == login_url  # checkpoint navigate to authentication page

            # perform login
            perform_login(self.driver, admin_user, admin_pwd)
            assert self.driver.current_url == dashboard_url  # checkpoint navigate to dashboard page

            for index, row in testdata_df.iterrows():
                try:
                    first_name = row["first_name"]
                    middle_name = row["middle_name"]
                    last_name = row["last_name"]
                    employee_id = row["id"]
                    photofile = row["photofile"]

                    # navigate to add employee in menu pim
                    navigate_add_employee_page(self.driver)
                    assert self.driver.current_url == add_employee_url  # checkpoint navigate to pim add employee page

                    # perform input testdata for adding employee
                    perform_add_employee(self.driver, first_name, middle_name, last_name, employee_id, photofile)
                    time.sleep(1)

                    err = True
                    if first_name and last_name and not is_exists_id(employee_id) and is_accept_photofile(photofile):
                        err = False

                    # check valid form
                    if err:
                        check_valid_add_employee_form(self.driver, first_name, middle_name, last_name, employee_id,
                                                      photofile)

                    # check valid result
                    else:
                        check_valid_result_info(self.driver, first_name, middle_name, last_name, employee_id, photofile)

                    update_test_result(testdata_path, "pass", index)
                    print(".", end=" ")

                except AssertionError:
                    update_test_result(testdata_path, "fail", index)
                    print("x", end=" ")

        except AssertionError:
            print("FAILED LOGIN")


if __name__ == "__main__":
    unittest.main()
