# standard library
import os
import csv
import argparse

from collections import defaultdict
from datetime import datetime, timedelta

# external libraries
import pandas
from jinja2 import Environment, FileSystemLoader

# internal libs
from config import *
from mailer import Mailer
from datalib.module_list import *

# Templating stuff
TEMPLATE_ENVIRONMENT = Environment(autoescape=True, loader=FileSystemLoader(TEMPLATE_PATH), trim_blocks=False)
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def read_module_leaders():
    """
    Read in a .csv of module leaders and return two lookup dictionaries

    CSV file should be in a 2-column format where each row contains
    a module code and the module leader
    """
    MODULE_LEADER_COL = 'module leader'
    MODULE_CODE_COL = 'module'

    # lookups for data
    leader2modules = defaultdict(list)
    module2leader = defaultdict(str)

    # file with data
    leader2module_file = os.path.join(INPUT_DIR, MODULE_TO_MODULE_LEADER_FILE)
    with open(leader2module_file, 'r') as input_file:
        reader = csv.DictReader(input_file)
        # loop through and populate lookups
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

    # lookups for data
    leader2email = defaultdict(str)

    # file with data
    leader2email_file = os.path.join(INPUT_DIR, MODULE_LEADER_TO_EMAIL_FILE)
    with open(leader2email_file, 'r') as input_file:
        reader = csv.DictReader(input_file)
        # loop through and populate lookup
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

    # get the necessary lookups
    leader2modules, module2leader = read_module_leaders()
    leader2email = read_module_leaders_emails()
    start, end = calculate_start_and_end_of_week()
    assessment_data = read_assessment_sheet()

    # lists of tasks
    modules_out = []
    modules_in = []
    modules_feedback = []

    # loop through assessments and extract tasks for this week
    for i, row in assessment_data.iterrows():

        # convert pandas TimeDate to python datetime.date objects
        out_date = row['Out'].to_pydatetime().date()
        in_date = row['In'].to_pydatetime().date()
        feedback_date = row['Feedback'].to_pydatetime().date()

        # if task is within this week, add it to the correct week
        if out_date >= start and out_date <= end:
            modules_out.append(row)
        if in_date >= start and in_date <= end:
            modules_in.append(row)
        if feedback_date >= start and feedback_date <= end:
            modules_feedback,append(row)

    # collect the set of module leaders with actions this week
    module_leaders = set()

    for row in modules_in:
        module_leader = module2leader[row['Module']]
        module_leaders.add(module_leader)
    for row in modules_out:
        module_leader = module2leader[row['Module']]
        module_leaders.add(module_leader)
    for row in modules_feedback:
        module_leader = module2leader[row['Module']]
        module_leaders.add(module_leader)

    # build a context for each module leader including basic data
    module_leader_contexts = defaultdict(dict)
    for module_leader in module_leaders:
        module_leader_contexts[module_leader]['module_leader'] = module_leader
        module_leader_contexts[module_leader]['tasks'] = []
        module_leader_contexts[module_leader]['reply_to'] = SEND_FROM

    # add each task for the module leader to the context
    for row in modules_in:
        module_leader = module2leader[row['Module']]
        r_dict = row.to_dict()
        r_dict['in'] = True
        module_leader_contexts[module_leader]['tasks'].append(r_dict)
    for row in modules_out:
        module_leader = module2leader[row['Module']]
        r_dict = row.to_dict()
        r_dict['out'] = True
        module_leader_contexts[module_leader]['tasks'].append(r_dict)
    for row in modules_feedback:
        module_leader = module2leader[row['Module']]
        r_dict = row.to_dict()
        r_dict['feedback'] = True
        module_leader_contexts[module_leader]['tasks'].append(r_dict)

    # initialise the mailer object
    mailer = Mailer(SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT)

    # build and send email to each module leader
    for module_leader, context in module_leader_contexts.items():
        #module_leader_email = leader2email[module_leader]
        module_leader_email = ['chorleymj@cardiff.ac.uk']

        html = render_template('email_template.html', context)
        text = render_template('email_template.txt', context)

        if not dev_mode:
            # not in dev mode so we can send emails
            mailer.send(SEND_FROM, module_leader_email, "Assessment tasks due this week - %s" % module_leader, text_body=text, html_body=html)
        else:
            # in dev mode, write the emails out instead
            mailer.mock(SEND_FROM, module_leader_email, "Assessment tasks due this week - %s" % module_leader, text_body=text, html_body=html)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Reminding module leaders of their assessment tasks")
    parser.add_argument('-d', '--dev', help='Development mode, do not email module leaders, write emails to file instead', action='store_true')
    args = parser.parse_args()

    main(args.dev)
