import os

from _credentials import uname, pwd

REPORT_TO = ["martin.chorley@gmail.com"]
INPUT_DIR = os.path.join(os.getcwd(), 'input')

MODULE_TO_MODULE_LEADER_FILE = 'module_list.csv'
MODULE_LEADER_TO_EMAIL_FILE = 'mllist2email.csv'
ASSESSMENT_DETAILS_FILE = 'assessment.xlsx'

SMTP_SERVER = "outlook.office365.com"
SMTP_PORT = 587
SMTP_USERNAME = uname
SMTP_PASSWORD = pwd
