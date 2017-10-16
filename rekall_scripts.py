'''Functions to wrap rekall and return python dictionaries of data'''
import yaml

from rekall import plugins
from rekall import session


with open("config.yaml", 'r') as f:
    CONFIG = yaml.load(f)['rekall']

def create_session(filename):
    '''Create the Rekall session necessary to run plugins

    Returns the session created'''
    s = session.Session(
        filename=filename,
        profile_path=[CONFIG['profile_path']],
        autodetect=["rsds"]
    )
    return s


def get_imageinfo(filename):
    '''Gets the basic image info provided by Rekall

    Returns a dict of image information'''
    sess = create_session(filename)

    # Returns as a rekall object
    info = sess.plugins.imageinfo()

    #Convert rekall object to python dict
    info_dict = {}
    for line in info:
        if isinstance(line, tuple):
            info_dict[line[0]] = str(line[1])
        elif isinstance(line, dict):
            info_dict[line['key']] = str(line['value'])

    return info_dict


def get_processlist(filename):
    '''Gets the basic processlist provided by Rekall

    Returns a dict of all the process from processlist'''
    sess = create_session(filename)
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

def get_networkconns(filename):
    '''Gets the network connections after determining what OS this is from

    Returns a dict containing network connections'''
    sess = create_session(filename)
    imageinfo = get_imageinfo(filename)

    # Determine what platform
    win_build = 'NT Build'
    conns = []
    if win_build in imageinfo:
        if 'xp' in imageinfo[win_build]:
            results = sess.plugins.connscan()
            for result in results:
                # Each result is a tuple of netobject, src ip:port,
                # dest ip:port, pid, in that order
                conn = {}
                conn['local_ip'], conn['local_port'] = result[1].split(':')
                conn['remote_ip'], conn['remote_port'] = result[2].split(':')
                # pid comes back as a pid object, str makes it more useable
                conn['pid'] = str(result[3])
                conns.append(conn)
        elif 'win7' in imageinfo[win_build]:
            pass
        else:
            return
    return conns
