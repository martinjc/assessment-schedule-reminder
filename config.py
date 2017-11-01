import os

# _credentials.py should contain a valid username and password
# for accessing the email server (SMTP_SERVER) given below. It's
# in the .gitignore so it won't get added to the Git repo during
# development
from _credentials import uname, pwd

# Address to send emails from
SEND_FROM = "COMSC-AF@cardiff.ac.uk"

# directory containing necessary csv files for input
INPUT_DIR = os.path.join(os.getcwd(), 'input')

# names of input csv files
# this file should be a mapping of module codes to module leaders
MODULE_TO_MODULE_LEADER_FILE = 'module_list.csv'
# this file should be a mapping of module leaders to email addresses
MODULE_LEADER_TO_EMAIL_FILE = 'mllist2email.csv'
# this file should be a list of assessments with their module codes, titles,
# percentages, date handed out, date handed in and feedback date
ASSESSMENT_DETAILS_FILE = 'assessment.xlsx'

# details for the email server
SMTP_SERVER = "outlook.office365.com"
SMTP_PORT = 587
SMTP_USERNAME = uname
SMTP_PASSWORD = pwd

# where are the templates for emails to send?
TEMPLATE_PATH = os.path.join(os.getcwd(), 'templates')
