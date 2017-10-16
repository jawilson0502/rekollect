import json
import yaml

from rekall import session
from rekall import plugins


with open("config.yaml", 'r') as f:
    config = yaml.load(f)['rekall']

def create_session(filename):
    s = session.Session(
        filename=filename,
        profile_path = [config['profile_path']],
        autodetect = ["rsds"]
    )
    return s


def get_imageinfo(sess):
    '''Gets the basic image info provided by Rekall
    Returns a dict of image information'''

    # Returns as a rekall object
    info = sess.plugins.imageinfo()

    #Convert rekall object to python dict
    info_dict = {} 
    for line in info:
        if type(line) == tuple:
            info_dict[line[0]] = str(line[1])
        elif type(line) == dict: 
            info_dict[line['key']] = str(line['value'])

    return info_dict


def get_processlist(sess):
    '''Gets the basic processlist provided by Rekall
    Returns a dict of all the process from processlist'''
    
    # ps is a rekall object
    ps = sess.plugins.pslist()

    pslist = []
    for proc in ps:
        # Returns an dict
        for line in proc:
            # Iterate through the keys and ensure values are strings
            if line == '_EPROCESS':
                # Eprocess is a whole data struct, which also contains the pid
                # Currently I only want to use the pid and name for pslist
                # TODO: Handle _EPROCESS better
                pid = str(proc[line].pid)
                proc_name = str(proc[line].name)

            proc[line] = str(proc[line])

        # Insert the name and pid as keys in the proc info
        proc['pid'] = pid
        proc['name'] = proc_name
        proc.pop('_EPROCESS')
        pslist.append(proc)

    return pslist
