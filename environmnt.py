import os, shutil, datetime, time
from turtle import left
from configfile import configfile 
import paramiko
from helpers import bcolors
from helpers import output
from helpers import logger
import socket

class environmnt:
    def __init__(self, server, component, operation = 'comm'):
        self.server = server
        self.component = component
        self.operation = operation
        self.host = configfile.sectionGetCredentials(server, component)[0]
        self.user = configfile.sectionGetCredentials(server, component)[1]
        self.password = configfile.sectionGetCredentials(server, component)[2]
        self.anx_remote_path = '/home/aeonixadmin/aeonix/'
        self.anx_remote_path_logs_server = '/home/aeonixadmin/aeonix/logs/server/'
        #self.anx_remote_path_simulator = '/home/aeonixadmin/simulator/'
        self.anx_remote_path_simulator = 'simulator/'
        self.anx_remote_path_simulator_logs = self.anx_remote_path_simulator + 'logs/' 
        self.anx_remote_path_simulator_packs = self.anx_remote_path_simulator + 'packs/' 
        self.sipp_remote_path = 'simulator/'
        self.sipp_remote_path_logs = self.sipp_remote_path + 'logs/'
        self.sipp_remote_path_packs = self.sipp_remote_path + 'packs/'
        self.local_path =  'scripts/' + str(environmnt.tempFileInfo()[1]) + '_users' + '_' + environmnt.tempFileInfo()[3] + '/server_'+ server
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_zip = datetime.datetime.now().strftime("_%Y-%m-%d_%H_%M_%S")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((self.host,22))
        self.comm = ('established' if result == 0 else 'unreachable')
        sock.close()
       
        if self.comm == 'established':
            self.client = paramiko.client.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.transport = paramiko.Transport(self.host, 22)
            self.transport.connect(username=self.user,password=self.password)
            self.client.connect(hostname = self.host, username=self.user,password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)


    def anxWalker(self):
        if self.comm == 'established':
            match self.operation:
                case 'status':
                    ssh_command ='sudo service aeonix status'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    running = response.count('running')
                    stopped = response.count('stopped')
                    dead = response.count('dead')
                    return('running' if running == 6 and stopped == 0 else 'stopped' if running == 0 and stopped == 6 else 'error', running)            
                case 'version':
                    ssh_command ="sudo sed -n '4p' /home/aeonixadmin/aeonix/MANIFEST.MF |tr -c -d 0-9."
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(response if response !='' else 'unknown')
                case 'collect':
                    ssh_command = logger.log_environment_collect
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.anx_remote_path_simulator + '; ./remote.sh collect'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                case 'pack':
                    ssh_command = logger.log_environment_pack
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.anx_remote_path_simulator + '; ./remote.sh pack'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                case 'download':
                    ssh_command = logger.log_environment_download
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    self.sftp.chdir(self.anx_remote_path_simulator_packs)
                    file_list = self.sftp.listdir()
                    for item in file_list:
                        if 'zip' in item:
                            self.sftp.get(item, self.local_path + '/aeonix/downloads/' + item)
                case 'upload':
                    try:
                        #print('trying...' + self.server + self.remote_path)
                        self.sftp.chdir(self.anx_remote_path_simulator)
                        ssh_command = 'cd ' + self.anx_remote_path_simulator + '; chmod +x *.sh' #anxd
                        stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    except IOError:
                        self.sftp.mkdir(self.anx_remote_path_simulator)
                        self.sftp.mkdir(self.anx_remote_path_simulator_logs)
                        self.sftp.mkdir(self.anx_remote_path_simulator_packs)
                        self.sftp.chdir(self.anx_remote_path_simulator)
                    files = [f for f in os.listdir(self.local_path + '/aeonix/') if os.path.isfile(os.path.join(self.local_path + '/aeonix/',f))]
                    print('uploading from: ' + self.local_path + '/aeonix/' + ' to: aeonix ' + self.host + ' ' + self.anx_remote_path_simulator)
                    for filename in files:
                        self.sftp.put(self.local_path + '/aeonix/' + filename, filename)
                    ssh_command = 'cd ' + self.anx_remote_path_simulator + '; chmod +x *.sh ; rm -rf *.zip'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = logger.log_environment_upload
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    #return None
                case 'clean':
                    ssh_command = logger.log_environment_clean
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.anx_remote_path_simulator + '; ./remote.sh clean'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    return None
                case 'cleanZip':
                    ssh_command = logger.log_environment_cleanZip
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.anx_remote_path_simulator + '; ./remote.sh cleanZip'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    return None
                case 'erase':
                    ssh_command = logger.log_environment_erase_aeonix
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.anx_remote_path_simulator + '; ./remote.sh erase'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    return None
                case 'reboot':
                    ssh_command = logger.log_environment_reboot
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command ="sudo reboot"
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(True)
                case 'stop':
                    ssh_command = logger.log_environment_stop
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command ="sudo service aeonix stop"
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(True)
                case 'start':
                    ssh_command = logger.log_environment_start
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command ="sudo service aeonix start"
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(True)
                case 'restart':
                    ssh_command = logger.log_environment_restart
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command ="sudo service aeonix restart"
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(True)
                case 'comm':
                    return(self.comm)
                case 'hostname':
                    ssh_command = 'hostname'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(response)
                case 'ipaddress':
                    ssh_command = 'hostname -i | cut -f1 -d' ''
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(response)
                case _:
                    return('not found')
        else:
            return

    # sipp specific operations ################################
    
    def sippWalker(self):
        if self.comm == 'established':
            match self.operation:
                case 'jobs':
                    ssh_command = 'pgrep sipp'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = len(outlines)
                    return('running' if response != 0 else 'stopped',response)            
                case 'terminate':
                    ssh_command = logger.log_environment_terminate
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'killall sipp'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    return None
                case 'collect':
                    ssh_command = logger.log_environment_collect
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.sipp_remote_path + '; ./remote.sh collect'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                case 'pack':
                    ssh_command = logger.log_environment_pack
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.sipp_remote_path + '; ./remote.sh pack'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                case 'download':
                    ssh_command = logger.log_environment_download
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    self.sftp.chdir(self.sipp_remote_path_packs)
                    file_list = self.sftp.listdir()
                    print(file_list)
                    for item in file_list:
                        if 'zip' in item:
                            print(item)
                            self.sftp.get(item, self.local_path + '/sipp/downloads/' + item)
                case 'upload':
                    try:
                        self.sftp.chdir(self.sipp_remote_path)
                        ssh_command = 'cd ' + self.sipp_remote_path + '; chmod +x *.sh' #anxd
                        stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    except IOError:
                        self.sftp.mkdir(self.sipp_remote_path)
                        self.sftp.mkdir(self.sipp_remote_path_logs)
                        self.sftp.mkdir(self.sipp_remote_path_packs)
                        self.sftp.chdir(self.sipp_remote_path)
                    files = [f for f in os.listdir(self.local_path + '/sipp/') if os.path.isfile(os.path.join(self.local_path + '/sipp/',f))]
                    print('uploading from: ' + self.local_path + '/sipp/' + ' to: sipp ' + self.host + ' ../' + self.sipp_remote_path)
                    for filename in files:
                        self.sftp.put(self.local_path + '/sipp/' + filename, filename)
                    ssh_command = 'cd ' + self.sipp_remote_path + '; chmod +x *.sh ; rm -rf *.zip'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = logger.log_environment_upload
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    #return None
                case 'clean':
                    ssh_command = logger.log_environment_clean
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.sipp_remote_path + '; ./remote.sh clean'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    return None
                case 'cleanZip':
                    ssh_command = logger.log_environment_cleanZip
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.sipp_remote_path + '; ./remote.sh cleanZip'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    return None
                case 'erase':
                    ssh_command = logger.log_environment_erase_sipp
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    ssh_command = 'cd ' +  self.sipp_remote_path + '; ./remote.sh erase'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    return None
                case 'comm':
                    return(self.comm)
                case 'hostname':
                    ssh_command = 'hostname'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(response)
                case 'ipaddress':
                    ssh_command = 'hostname -i | cut -f1 -d' ''
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return(response)
                case _:
                    return('not found')
        else:
            return

    def localWalker(self):
            match self.operation:
                case 'clean':
                    print()

    def statusInfo_anx(section):
        comm = status = version = ''
        comm = environmnt(section, 'aeonix').comm
        if comm != 'established':
            pass
        else:
            status = environmnt(section, 'aeonix', 'status').anxWalker()
            version = environmnt(section, 'aeonix', 'version').anxWalker()
        return(comm, status, version)

    def statusInfo_sipp(section):
        comm = status = ''
        comm = environmnt(section, 'sipp').comm
        if comm != 'established':
            pass
        else:
            status = environmnt(section, 'sipp' ,'jobs').sippWalker()
        return(comm, status)

    def sippFuncCall(operation):
        for section in configfile.sectionsNames():
            print(section)
            results = environmnt(section, 'sipp', operation).sippWalker()
            print(results)       

    def anxFuncCall(operation):
        for section in configfile.sectionsNames():
            print(section)
            results = environmnt(section, 'aeonix', operation).anxWalker()
            print(results)        

    def distributeFiles():
        for section in configfile.sectionsNames():
            print(section)
            try:
                status_sipp = environmnt.statusInfo_sipp(section)
                if status_sipp[0] == 'established' and status_sipp[1][0] == 'stopped':
                    upload = environmnt(section, 'sipp', 'upload').sippWalker()
                #print(status_sipp)
                #print(upload)
                status_anx = environmnt.statusInfo_anx(section)
                if status_anx[0] == 'established': 
                    upload = environmnt(section, 'aeonix', 'upload').anxWalker()
                #print(status_anx)
                #print(upload)
            except:
                print('FAIL')
                continue

    def tempFileInfo():
        try:
            with open("temp", "r") as tempfile:
                tempFileValues = tempfile.read().split(',')
                tempfile.close()
            servers      = tempFileValues[0] # amount of servers
            usersValue   = tempFileValues[1] # total number of users
            startatValue = tempFileValues[2] # first user start at
            methodValue  = tempFileValues[3] # method
            return(servers, usersValue, startatValue, methodValue)
        except:
            return('error')