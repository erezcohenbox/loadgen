import os, shutil, datetime, time
from turtle import left
from configfile import configfile 
import paramiko
from helpers import bcolors
from helpers import output
from helpers import logger
import socket
import threading

class environmnt:
    def __init__(self, server, component, operation = 'comm'):
        self.server = server
        self.component = component
        self.operation = operation
        self.host = configfile.sectionGetCredentials(server, component)[0]
        self.user = configfile.sectionGetCredentials(server, component)[1]
        self.password = configfile.sectionGetCredentials(server, component)[2]
        
        self.anx_remote_path              = '/home/aeonixadmin/aeonix/'
        self.anx_remote_path_logs_server  = '/home/aeonixadmin/aeonix/logs/server/'
        self.anx_remote_path_logs_web     = '/home/aeonixadmin/aeonix/logs/web/'
        self.anx_remote_path_logs_MP      = '/home/aeonixadmin/aeonixMP/logs/'
        self.anx_remote_path_logs_WD      = '/home/aeonixadmin/aeonixWD/logs/'
        self.anx_remote_path_logs_agent   = '/home/aeonixadmin/agent/logs/'
        self.anx_remote_path_logs_agentWD = '/home/aeonixadmin/agentWD/logs/'
        self.anx_remote_path_logs_cdr     = '/home/aeonixadmin/cdr/'

        self.anx_remote_path_simulator       = 'simulator/'
        self.anx_remote_path_simulator_logs  = self.anx_remote_path_simulator + 'logs/' 
        self.anx_remote_path_simulator_packs = self.anx_remote_path_simulator + 'packs/' 
        
        self.sipp_remote_path                = 'simulator/'
        self.sipp_remote_path_logs           = self.sipp_remote_path + 'logs/'
        self.sipp_remote_path_packs          = self.sipp_remote_path + 'packs/'
        
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
                    ssh_command = 'cd ' +  self.anx_remote_path_logs_server + \
                    '; find ' + self.anx_remote_path_logs_server + ' -type f -name \'stdout*\' | wc -l ' + \
                    '; find ' + self.anx_remote_path_logs_server + ' -type f -name \'sysHealth*\' | wc -l '
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = sum(list(map(int,''.join(outlines).split())))
                    if response == 0: return('nothing to collect')
                    else:
                        log_command = logger.log_environment_collect 
                        ssh_command = 'cd ' +  self.anx_remote_path_simulator_logs + \
                        '; find ' + self.anx_remote_path_logs_server + ' -type f -name \'stdout*\' -exec cp \'{}\' . \;' + \
                        '; find ' + self.anx_remote_path_logs_server + ' -type f -name \'sysHealth*\' -exec cp \'{}\' . \;' + \
                        '; zip -rpq ../packs/anx_`hostname`_`hostname -I | cut -f1 -d\' \'`' + self.timestamp_zip + '_logs.zip * ;'
                    #else: return
                #case 'collect':
                #    log_command = logger.log_environment_collect 
                #    ssh_command = 'cd ' +  self.anx_remote_path_simulator_logs + \
                #    '; find ' + self.anx_remote_path_logs_server + ' -type f -name \'stdout*\' -exec cp \'{}\' . \;' + \
                #    '; find ' + self.anx_remote_path_logs_server + ' -type f -name \'sysHealth*\' -exec cp \'{}\' . \;'
                #case 'pack':
                #    log_command = logger.log_environment_pack
                #    ssh_command = 'cd ' +  self.anx_remote_path_simulator_logs + \
                #    '; zip -rpq ../packs/anx_`hostname`_`hostname -I | cut -f1 -d\' \'`' + self.timestamp_zip + '_logs.zip * ;'# &>/dev/null'# &'
                case 'download':
                    log_command = logger.log_environment_download
                    self.sftp.chdir(self.anx_remote_path_simulator_packs)
                    while True:
                        file_list = self.sftp.listdir()
                        if not file_list: return('nothing to download')
                        zipfile = any(('zip' in item) for item in file_list)
                        if zipfile == True: break
                    os.makedirs(self.local_path + '/aeonix/downloads/', exist_ok = True)
                    for item in file_list:
                        if 'zip' in item:
                            self.sftp.get(item, self.local_path + '/aeonix/downloads/' + item)
                    return
                case 'upload':
                    try:
                        self.sftp.chdir(self.anx_remote_path_simulator)
                        ssh_command = 'cd ' + self.anx_remote_path_simulator + '; chmod +x *.sh ;'
                        stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    except IOError:
                        self.sftp.mkdir(self.anx_remote_path_simulator)
                        self.sftp.mkdir(self.anx_remote_path_simulator_logs)
                        self.sftp.mkdir(self.anx_remote_path_simulator_packs)
                        self.sftp.chdir(self.anx_remote_path_simulator)
                    files = [f for f in os.listdir(self.local_path + '/aeonix/') if os.path.isfile(os.path.join(self.local_path + '/aeonix/',f))]
                    for filename in files:
                        self.sftp.put(self.local_path + '/aeonix/' + filename, filename)
                    ssh_command = 'cd ' + self.anx_remote_path_simulator + '; chmod +x *.sh ;'
                    log_command = logger.log_environment_upload
                case 'cleanLogs':
                    log_command = logger.log_environment_clean
                    ssh_command = 'cd ' +  self.anx_remote_path_simulator_logs + '; rm -rf * ;'
                case 'cleanPacks':
                    log_command = logger.log_environment_cleanPacks
                    ssh_command = 'cd ' +  self.anx_remote_path_simulator_packs + '; rm -rf * ;'
                case 'erase':
                    log_command = logger.log_environment_erase_aeonix
                    ssh_command = 'cd ' +  self.anx_remote_path_logs_server + \
                    '; find . -type f -name \'stdout*\' -exec sudo rm \'{}\' \;' + \
                    '; find . -type f -name \'sysHealth*\' -exec sudo rm \'{}\' \;'
                case 'eraseAll':
                    log_command = logger.log_environment_erase_aeonix
                    ssh_command = 'cd ' +  self.anx_remote_path_logs_server + \
                    '; sudo rm -rf *.log *.zip Sun/ Mon/ Tue/ Wed/ Thu/ Fri/ Sat/ ;' 
                case 'reboot':
                    log_command = logger.log_environment_reboot
                    ssh_command ="sudo reboot &"
                case 'stop':
                    log_command = logger.log_environment_stop
                    ssh_command ="sudo service aeonix stop &"
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    #print(response)
                    return
                case 'start':
                    log_command = logger.log_environment_start
                    ssh_command ="sudo service aeonix start &"
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = ''.join(outlines)
                    return
                case 'restart':
                    log_command = logger.log_environment_restart
                    ssh_command ="sudo service aeonix restart &"
                case _:
                    return('not found')
            stdin,stdout,stderr = self.client.exec_command(log_command)
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
        else:
            return('unreachable')

    # sipp specific operations ################################
    
    def sippWalker(self):
        if self.comm == 'established':
            match self.operation:
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
                case 'jobs':
                    ssh_command = 'pgrep sipp'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    outlines = stdout.readlines()
                    response = len(outlines)
                    return('running' if response != 0 else 'stopped',response)            
                case 'collect':
                    log_command = logger.log_environment_collect
                    ssh_command = 'cd ' +  self.sipp_remote_path_logs + '; cp ../*.* . \;'
                case 'pack':
                    log_command = logger.log_environment_pack
                    ssh_command = 'cd ' +  self.sipp_remote_path_logs + \
                    ';zip -rpq ../packs/sipp_`hostname`_`hostname -I | cut -f1 -d\' \'`' + self.timestamp_zip + '_logs.zip * \;'
                case 'download':
                    log_command = logger.log_environment_download
                    self.sftp.chdir(self.sipp_remote_path_packs)
                    while True:
                        file_list = self.sftp.listdir()
                        zipfile = any(('zip' in item) for item in file_list)
                        if zipfile == True: break
                    for item in file_list:
                        if 'zip' in item:
                            self.sftp.get(item, self.local_path + '/sipp/downloads/' + item)
                    return
                case 'upload':
                    try:
                        self.sftp.chdir(self.sipp_remote_path)
                        ssh_command = 'cd ' + self.sipp_remote_path + '; chmod +x *.sh \;' #anxd
                        stdin,stdout,stderr = self.client.exec_command(ssh_command)
                    except IOError:
                        self.sftp.mkdir(self.sipp_remote_path)
                        self.sftp.mkdir(self.sipp_remote_path_logs)
                        self.sftp.mkdir(self.sipp_remote_path_packs)
                        self.sftp.chdir(self.sipp_remote_path)
                    files = [f for f in os.listdir(self.local_path + '/sipp/') if os.path.isfile(os.path.join(self.local_path + '/sipp/',f))]
                    # print('uploading from: ' + self.local_path + '/sipp/' + ' to: sipp ' + self.host + ' ../' + self.sipp_remote_path)
                    for filename in files:
                        self.sftp.put(self.local_path + '/sipp/' + filename, filename)
                    ssh_command = 'cd ' + self.sipp_remote_path + '; chmod +x *.sh ; rm -rf *.zip \;'
                    log_command = logger.log_environment_upload
                case 'cleanLogs':
                    log_command = logger.log_environment_clean
                    ssh_command = 'cd ' +  self.sipp_remote_path_logs + '; rm -rf * \;'
                case 'cleanPacks':
                    log_command = logger.log_environment_cleanPacks
                    ssh_command = 'cd ' +  self.sipp_remote_path_packs + '; rm -rf * \;'
                case 'erase':
                    log_command = logger.log_environment_erase_sipp
                    ssh_command = 'cd ' +  self.sipp_remote_path + '; rm -rf *_.* ; rm -rf *_calldebug.log ; rm -rf *_errors.* ;' + \
                    '; rm -rf *_error_codes.csv ; rm -rf *_messages.log ; rm -rf *_screen.log; rm -rf *_shortmessages.log \;'
                case 'terminate':
                    log_command = logger.log_environment_terminate
                    ssh_command = 'killall sipp &'
                case _:
                    return('not found')
            stdin,stdout,stderr = self.client.exec_command(log_command)
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
        else:
            return('unreachable')

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

    def anxFuncCall(operation):
        print(output.prompt_environmnt_handler_aeonix + operation  + output.prompt_environmnt_handler_2)
        for section in configfile.sectionsNames():
            results = environmnt(section, 'aeonix', operation).anxWalker()
            if results == None:
                print(output.prompt_indent_pass_1 + section + ' (' + configfile.sectionGetElement(section, 'aeonix_host')+') ')
            elif results == 'unreachable':
                print(output.prompt_indent_fail_1 + section + ' (' + configfile.sectionGetElement(section, 'aeonix_host')+') - ' + results)
            else:
                print(output.prompt_indent_attn_1 + section + ' (' + configfile.sectionGetElement(section, 'aeonix_host')+') - ' + results) 

    def sippFuncCall(operation):
        print(output.prompt_environmnt_handler_sipp + operation  + output.prompt_environmnt_handler_2)
        for section in configfile.sectionsNames():
            results = environmnt(section, 'sipp', operation).sippWalker()
            if results == None:
                print(output.prompt_indent_pass_1 + section + ' (' + configfile.sectionGetElement(section, 'sipp_host')+') ')
            else:
                print(output.prompt_indent_fail_1 + section + ' (' + configfile.sectionGetElement(section, 'sipp_host')+') - ' + results)

    '''def sippFuncCall(operation):   *** WITH THREADS ***
        thread_instance = []
        for section in configfile.sectionsNames():
            print(section)
            trd = threading.Thread(target=environmnt(section, 'sipp', operation).sippWalker())
            trd.start()
            thread_instance.append(trd)
        for thread in thread_instance:
            thread.join()'''

   

    '''def distributeFiles():
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
                continue'''

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