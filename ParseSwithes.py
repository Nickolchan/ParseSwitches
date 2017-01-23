
ibnetdiscover_log = open("ibnetdiscover.log", 'r')
switches = ibnetdiscover_log.readlines()


def peel(unpeeled_list):
    peeled_list = []
    peeled_dict = {}
    for line in unpeeled_list:
        if line != '':
            if line[0] == '[' and (line.find('node') != -1 or line.find('NODE') != -1):
                short = int(line[1:line.find(']')])
                long = line.split()[3].lower().replace('"','')
                peeled_dict[short] = long
            else:
                if line[0] == 'S' and len(peeled_dict.items()) != 0:
                    peeled_list.append(peeled_dict)
                    peeled_dict = {}
    return peeled_list


def get_nodenumber(node, delta):
    nodenumber = int(node[4::]) + delta
    if nodenumber < 10:
        nodenumber = '00' + str(nodenumber)
    elif nodenumber < 100:
        nodenumber = '0' + str(nodenumber)
    return str (nodenumber)


def find_missing_ports(peeled_dict, user_key):
    missing_ports = []
    for switch in peeled_dict:
        below_key = 0
        above_key = 37
        for key in switch.keys():
           if key < user_key:
               below_key = max(below_key, key)
           elif key > user_key:
                above_key = min(key, above_key)
        if below_key != 0:
            below_node = 'node' + get_nodenumber(switch[below_key], user_key-below_key)
        if above_key != 37:
            above_node = 'node' + get_nodenumber(switch[above_key], user_key-above_key)
        if below_node and above_node:
            if user_key-below_key < above_key-user_key:
                missing_ports.append(below_node)
            else:
                missing_ports.append(above_node)
        elif below_node:
            missing_ports.append(below_node)
        elif above_node:
            missing_ports.append(above_node)
    missing_ports.sort()
    for i in range(1,len(missing_ports)-1):
        if missing_ports[i] == missing_ports[i-1]:
            missing_ports.pop(i-1)
    return missing_ports

def get_nodelist(nodes):
    nodelist = 'node['
    for node in nodes:
        nodelist += get_nodenumber(node, 0)
        nodelist += ','
    nodelist = nodelist[:-1:]
    nodelist += ']'
    return nodelist





a = peel(switches)
#print (a[1])
b = find_missing_ports(a, 12)
b.sort()
print (get_nodelist(b))
