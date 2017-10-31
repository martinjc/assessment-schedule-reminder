import os
import csv
import pandas
import argparse

from collections import defaultdict
from datetime import datetime, timedelta

from config import *
from datalib.module_list import *


def read_module_leaders():
    """
    Read in a .csv of module leaders and return two lookup dictionaries

    CSV file should be in a 2-column format where each row contains
    a module code and the module leader
    """
    MODULE_LEADER_COL = 'module leader'
    MODULE_CODE_COL = 'module'

    leader2modules = defaultdict(list)
    module2leader = defaultdict(str)

    leader2module_file = os.path.join(INPUT_DIR, MODULE_TO_MODULE_LEADER_FILE)
    with open(leader2module_file, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            leader2modules[row[MODULE_LEADER_COL]].append(row[MODULE_CODE_COL])
            module2leader[row[MODULE_CODE_COL]] = row[MODULE_LEADER_COL]

    return leader2modules, module2leader



def read_module_leaders_emails():
    """
    Read in a .csv of module leaders to emails and return a lookup dictionary

    CSV file should be in a 2-column format where each row contains a
    module leader and their email address
    """
    MODULE_LEADER_COL = 'module leader'
    EMAIL_COL = 'email'

    leader2email = defaultdict(str)

    leader2email_file = os.path.join(INPUT_DIR, MODULE_LEADER_TO_EMAIL_FILE)
    with open(leader2email_file, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            leader2email[row[MODULE_LEADER_COL]] = row[EMAIL_COL]

    return leader2email



def calculate_start_and_end_of_week():
    """
    Get today's date and work out the start and the end of the week
    """
    dt = datetime.today()
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return start.date(), end.date()


def read_assessment_sheet():
    """
    Read in the details of assessments.

    This expects an xlsx file (for ease of use), with set columns:
    [Module,Coursework,Percentage,Out,In,Feedback]
    """
    assessment_data_file = os.path.join(INPUT_DIR, ASSESSMENT_DETAILS_FILE)
    assessment_data = pandas.read_excel(assessment_data_file)
    return assessment_data



def main(dev_mode=False):

    leader2modules, module2leader = read_module_leaders()
    print(leader2modules, module2leader)
    leader2email = read_module_leaders_emails()
    print(leader2email)
    start, end = calculate_start_and_end_of_week()
    print(start, end)
    assessment_data = read_assessment_sheet()
    print(assessment_data)






if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Reminding module leaders of their assessment commitments")
    parser.add_argument('-d', '--dev', help='Development mode, do not email module leaders, use dev email address instead', action='store_true')
    args = parser.parse_args()

    main(args.dev)
