import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import datetime


def read_test_data(path):
    """Read testcase datasheet. Format: *.csv"""

    data = pd.read_csv(path, dtype=str)
    return data


def update_test_result(path, test_status, row_num):
    """Update test result of testcase. Include: test_status: pass or fail and execution_completion: time"""

    df = pd.read_csv(path, dtype=str)

    # df["test_status"] = pd.Series(dtype=str)
    # df["execution_completion"] = pd.Series(dtype=str)
    df["test_status"].values[row_num] = test_status
    df["execution_completion"].values[row_num] = str(datetime.datetime.now())

    df.to_csv(path, index=False)
