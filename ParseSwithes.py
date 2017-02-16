#!/usr/bin/python2
from sys import argv
import subprocess
import string


# Converts text into list of ditctionaries (each dictionary is switch{port: nodename/address/switch}
def peel(unpeeled_list):
    peeled_list = []
    peeled_dict = {}
    for line in unpeeled_list:
        if line != '':
            if line[0] == '[':
                peeled_dict[int(line[1:line.find(']')])] = line.split()[3].lower().replace('"', '')
            else:
                if line[0] == 'S' and len(peeled_dict.items()) != 0:
                    peeled_list.append(peeled_dict)
                    peeled_dict = {}
    return peeled_list


# Converts node! to node!!!
def get_nodename(node):
    nodename = node
    while len(nodename) < 7:
        nodename = nodename[:4] + '0' + nodename[4::]
    return nodename


# Uses list of peeled dictionaries to find missing ports in switches and tries to guess the nodename
def find_missing_ports(peeled_dict, user_key):
    missing_ports = []
    for switch in peeled_dict:
        previous_key = 0
        current_key = 0
        keys = switch.keys()
        if not user_key in keys:
            for key in keys:
                if switch[key].find('node') != -1:
                    if key < user_key:
                        previous_key = key
                    else:
                        current_key = key
                        break

            if previous_key != 0 and current_key != 0:
                delta1 = user_key - previous_key
                delta2 = current_key - user_key
                if delta1 < delta2:
                    missing_ports.append('node' + str(int(switch[previous_key][4::]) + delta1))
                else:
                    missing_ports.append('node' + str(int(switch[current_key][4::]) - delta2))
            elif previous_key != 0:
                nodename = 'node' + str(int(switch[previous_key][4::]) + user_key - previous_key)
                missing_ports.append(get_nodename(nodename))
            elif current_key != 0:
                nodename = 'node' + str(int(switch[current_key][4::]) - current_key + user_key)
                missing_ports.append(get_nodename(nodename))
    return missing_ports


'''Formatting section. Can be used for nodelist output'''


def get_nodenumber(node, delta):
    nodenumber = int(node[4::]) + delta
    if nodenumber < 10:
        nodenumber = '00' + str(nodenumber)
    elif nodenumber < 100:
        nodenumber = '0' + str(nodenumber)
    return str(nodenumber)


def nodelist(nodes):
    if not nodes:
        return 'None'
    ndlist = 'node['
    for node in nodes:
        ndlist += get_nodenumber(node, 0)
        ndlist += ','
    ndlist = ndlist[:-1:]
    ndlist += ']'
    return ndlist


def get_swithes():
    ibhosts = subprocess.Popen('ibnetdiscover', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ibnetdiscover_log, err = ibhosts.communicate()
    ibnetdiscover_log = string.split(ibnetdiscover_log, '\n')
    return ibnetdiscover_log

if int(argv[1]):
    print(nodelist(find_missing_ports(peel(get_swithes()), int(argv[1]))))
else:
    print('Usage: swparse <port_number>')
