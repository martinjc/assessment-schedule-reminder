import os
import csv

from collections import defaultdict

from datalib.module_list import *

REPORT_TO = ["PhillipsHR@cardiff.ac.uk"]

INPUT_DIR = os.path.join(os.getcwd(), 'input')

def read_module_leaders():
    """
    Read in a .csv of module leaders and return two lookup dictionaries

    CSV file should be in a 2-column format where each row contains a module code and the module leader
    """

    MODULE_LEADER_COL = 'module leader'
    MODULE_CODE_COL = 'module'

    leader2modules = defaultdict(list)
    module2leader = defaultdict(str)

    leader2module_file = os.path.join(INPUT_DIR, 'module_list.csv')
    with open(leader2module_file, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            leader2modules[row[MODULE_LEADER_COL]].append(row[MODULE_CODE_COL])
            module2leader[row[MODULE_CODE_COL]] = row[MODULE_LEADER_COL]

    return leader2modules, module2leader

def main():

    leader2modules, module2leader = read_module_leaders()
    print(leader2modules)
    print(module2leader)


if __name__ == '__main__':
    main()
