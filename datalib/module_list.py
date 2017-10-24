import csv

from datalib.handbooks import *

def write_module_leader_list(school, f):

    modules = get_module_list(school)

    with open(f, 'w') as output_file:
        fields = ['module leader', 'module']
        writer = csv.DictWriter(output_file, fields)
        writer.writeheader()
        for module in modules:
            module_leader = module['moduleLeader']
            module_leader_str = "%s %s %s" % (module_leader['title'], module_leader['firstName'], module_leader['surname'])
            module_data = {'module leader': module_leader_str, 'module': module['moduleCode']}
            writer.writerow(module_data)
