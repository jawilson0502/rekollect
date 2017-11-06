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
                # TODO: Find a way to get protocol
                # TODO: Fix bug that will break this with ipv6
                conn = {}
                conn['local_ip'], conn['local_port'] = result[1].split(':')
                conn['remote_ip'], conn['remote_port'] = result[2].split(':')
                # pid comes back as a pid object, str makes it more useable
                conn['pid'] = str(result[3])
                conns.append(conn)
        elif 'win7' in imageinfo[win_build]:
            results = sess.plugins.netscan()
            for result in results:
                # Each result is a tuple of offset, protocol, local_addr,
                # remote_addr, state, pid, owner, created
                conn = {}
                conn['protocol'] = result[1]
                if 'v6' in conn['protocol']:
                    # Break up ipv6 address into ip and port
                    ipv6_addr = result[2].split(':')
                    local_port = ipv6_addr[-1]
                    local_ip = ':'.join(ipv6_addr[:-1])
                    conn['local_ip'] = local_ip
                    conn['local_port'] = local_port

                    ipv6_addr = result[3].split(':')
                    remote_port = ipv6_addr[-1]
                    remote_ip = ':'.join(ipv6_addr[:-1])
                    conn['remote_ip'] = remote_ip
                    conn['remote_port'] = remote_port
                else:
                    # Assuming not ipv6, then ipv4
                    conn['local_ip'], conn['local_port'] = result[2].split(':')
                    conn['remote_ip'], conn['remote_port'] = result[3].split(':')
                conn['state'] = result[4]
                # pid comes back as a pid object, str makes it more useable
                conn['pid'] = str(result[5])
                # create_time comes back as a createtime objecct, str makes
                # it more useable
                conn['create_time'] = str(result[7])
                conns.append(conn)

        else:
            return
    return conns

def get_filescan(filename):
    '''Gets all the filenames of files open in memory

    Returns a dictionary of results'''

    sess = create_session(filename)

    files = sess.plugins.filescan()
    results = []
    for result in files:
        # Each result is a dictionary.
        item = {}
        item['access'] = result['access']
        item['offset'] = result['offset']
        item['pid'] = str(result['Owner'].pid)
        item['path'] = result['path']
        results.append(item)

    return results

def get_shimcache(filename):
    '''Gets the shimecache registry value

    returns a dictionary of results'''

    sess = create_session(filename)
    shimcache = sess.plugins.shimcachemem()
    results = []

    for result in shimcache:
        # Each result is a dictionary
        item = {}
        item['path'] = str(result['Path'])
        item['last_mod'] = str(result['last_mod'])
        item['last_update'] = str(result['last_update'])
        results.append(item)

    return results
