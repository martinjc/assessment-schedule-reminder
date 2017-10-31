import os
import csv
import pandas
import argparse

from collections import defaultdict
from datetime import datetime, timedelta

from config import *
from mailer import Mailer
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

    modules_out = []
    modules_in = []
    modules_feedback = []

    for i, row in assessment_data.iterrows():
        #print(i, row)
        out_date = row['Out'].to_pydatetime().date()
        in_date = row['In'].to_pydatetime().date()
        feedback_date = row['Feedback'].to_pydatetime().date()

        if out_date >= start and out_date <= end:
            modules_out.append(row)
        if in_date >= start and in_date <= end:
            modules_in.append(row)
        if feedback_date >= start and feedback_date <= end:
            modules_feedback,append(row)

    module_leader_phrases = defaultdict(list)

    print(modules_in)
    print(modules_out)
    print(modules_feedback)

    mailer = Mailer(SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT)

    for row in modules_in:
        module_leader = module2leader[row['Module']]
        phrase = 'Assessment "%s (%s)" for module %s is due to be handed in' % (row['Coursework'], row['Percentage'], row['Module'])
        module_leader_phrases[module_leader].append(phrase)
    for row in modules_out:
        module_leader = module2leader[row['Module']]
        phrase = 'Assessment "%s (%s)" for module %s is due to be handed out' % (row['Coursework'], row['Percentage'], row['Module'])
        module_leader_phrases[module_leader].append(phrase)
    for row in modules_feedback:
        module_leader = module2leader[row['Module']]
        phrase = 'Feedback for Assessment "%s (%s)" for module %s is due to be handed back to students.' % (row['Coursework'], row['Percentage'], row['Module'])
        module_leader_phrases[module_leader].append(phrase)

    for module_leader, phrases in module_leader_phrases.items():
        opening = "Dear %s,\n\nAccording to the assessment timetable you agreed to at the start of the year, you have the following assessment tasks taking place this week:\n" % (module_leader)
        middle = "\n".join(phrases)
        closing = "\nPlease check this is as you expect. If anything has changed and you have not already discussed this with Helen Phillips, please make sure to contact her immediately.\nIf you are due to be returning feedback this week and will not make this deadline you must inform both Helen Phillips and Andrew Jones as soon as possible."
        full_message = "%s\n%s\n%s" % (opening, middle, closing)
        print(full_message)
        mailer.send(SMTP_USERNAME, REPORT_TO, "test - %s" % module_leader, full_message)





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Reminding module leaders of their assessment commitments")
    parser.add_argument('-d', '--dev', help='Development mode, do not email module leaders, use dev email address instead', action='store_true')
    args = parser.parse_args()

    main(args.dev)
