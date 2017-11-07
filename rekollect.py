'''Functions to wrap rekall and return python dictionaries of data'''
import yaml

from rekall import plugins
from rekall import session



class Rekollect(object):
    ''' Contains info and functions from a single memory image'''
    # pylint: disable=too-many-instance-attributes

    def __init__(self, filename):
        self.set_config()
        self.filename = filename
        self.create_session()
        self.get_imageinfo()
        self.get_processlist()
        self.get_networkconns()
        self.get_filescan()
        self.get_shimcache()

    def set_config(self):
        '''Sets the config needed for Rekall'''
        with open("config.yaml", 'r') as config_file:
            self.config = yaml.load(config_file)['rekall']

    def create_session(self):
        '''Create the Rekall session necessary to run plugins

        Sets the session created in self'''
        self.session = session.Session(
            filename=self.filename,
            profile_path=[self.config['profile_path']],
            autodetect=["rsds"]
        )


    def get_imageinfo(self):
        '''Gets the basic image info provided by Rekall

        Sets self.imageinfo with dict of image information'''

        # Returns as a rekall object
        info = self.session.plugins.imageinfo()

        #Convert rekall object to python dict
        self.imageinfo = {}
        for line in info:
            if isinstance(line, tuple):
                self.imageinfo[line[0]] = str(line[1])
            elif isinstance(line, dict):
                self.imageinfo[line['key']] = str(line['value'])


    def get_processlist(self):
        '''Gets the basic processlist provided by Rekall

        Sets self.pslist with a dict of all the process from processlist'''
        # ps is a rekall object
        ps = self.session.plugins.pslist()

        self.pslist = []
        for proc in ps:
            # Returns an dict
            for line in proc:
                # Iterate through the keys and ensure values are strings
                if line == '_EPROCESS':
                    # Eprocess is a whole data struct, & contains the pid
                    # Currently I only want to use the pid and name for pslist
                    # TODO: Handle _EPROCESS better
                    pid = str(proc[line].pid)
                    proc_name = str(proc[line].name)

                proc[line] = str(proc[line])

            # Insert the name and pid as keys in the proc info
            proc['pid'] = pid
            proc['name'] = proc_name
            proc.pop('_EPROCESS')
            self.pslist.append(proc)


    def get_networkconns(self):
        '''Gets the network connections after determining what OS this is from

        Sets self.networkconns a dict containing network connections'''

        # Determine what platform
        self.networkconns = []
        win_build = 'NT Build'
        if win_build in self.imageinfo:
            if 'xp' in self.imageinfo[win_build]:
                results = self.session.plugins.connscan()
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
                    self.networkconns.append(conn)
            elif 'win7' in self.imageinfo[win_build]:
                results = self.session.plugins.netscan()
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
                    self.networkconns.append(conn)

            else:
                return


    def get_filescan(self):
        '''Gets all the filenames of files open in memory

        Sets self.filescan with a list of open files'''


        results = self.session.plugins.filescan()
        self.filescan = []
        for result in results:
            # Each result is a dictionary.
            item = {}
            item['access'] = result['access']
            item['offset'] = result['offset']
            item['pid'] = str(result['Owner'].pid)
            item['path'] = result['path']
            self.filescan.append(item)


    def get_shimcache(self):
        '''Gets the shimecache registry value

        Sets self.shimcache with recently used exes'''
        results = self.session.plugins.shimcachemem()
        self.shimcache = []

        for result in results:
            # Each result is a dictionary
            item = {}
            item['path'] = str(result['Path'])
            item['last_mod'] = str(result['last_mod'])
            item['last_update'] = str(result['last_update'])
            self.shimcache.append(item)
