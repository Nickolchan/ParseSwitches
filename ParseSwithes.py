import argparse


def peel(unpeeled_list):
    peeled_list = []
    peeled_dict = {}
    for line in unpeeled_list:
        if line != '':
            if line[0] == '[':  # and (line.find('node') != -1 or line.find('NODE') != -1):
                peeled_dict[int(line[1:line.find(']')])] = line.split()[3].lower().replace('"', '')
            else:
                if line[0] == 'S' and len(peeled_dict.items()) != 0:
                    peeled_list.append(peeled_dict)
                    peeled_dict = {}
    return peeled_list


def get_nodename(node):
    nodename = node
    if type(node) == int:
        nodename = 'node' + str(nodename)
    while len(nodename) < 7:
        nodename = nodename[:4] + '0' + nodename[4::]
    return nodename


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


# parsep = argparse.ArgumentParser(description='find missing ibports')
# parsep.add_argument(type = int)
# parsep.add_argument('-l', help='long output format')
# args = parsep.parse_args()
ibnetdiscover_log = open("ibnetdiscover.log", 'r')
switches = ibnetdiscover_log.readlines()
print(find_missing_ports(peel(switches), 29))
