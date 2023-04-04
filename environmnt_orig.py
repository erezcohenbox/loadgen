import os, shutil, datetime, time
from turtle import left
from configfile import configfile 
import paramiko
from helpers import bcolors
from helpers import output


class environmnt:
    def __init__(self, server, component, operation = 'comm'):
        self.server = server
        self.component = component
        self.operation = operation
        self.host = configfile.sectionGetCredentials(server, component)[0]
        self.user = configfile.sectionGetCredentials(server, component)[1]
        self.password = configfile.sectionGetCredentials(server, component)[2]
        self.remote_path = 'simulator/'
        self.local_path =  'scripts/' + str(environmnt.tempFileInfo()[1]) + '_users' + '_' + environmnt.tempFileInfo()[3] + '/server_'+ server
        
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_zip = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

        self.client = paramiko.client.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.transport = paramiko.Transport(self.host, 22)
            self.transport.connect(username=self.user,password=self.password)
            self.client.connect(hostname = self.host, username=self.user,password=self.password, timeout=3)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.comm = 'established'
        except:
            self.comm = 'unreachable'


    def check(self):

        # aeonix specific operations ##############################

        if self.operation in ['status']:
            ssh_command ='sudo service aeonix status'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            running = response.count('running')
            stopped = response.count('stopped')
            return('running' if running == 6 and stopped == 0 else 'stopped' if running == 0 and stopped == 6 else 'error', running)            

        elif self.operation in ['version']:
            ssh_command ="sudo sed -n '4p' /home/aeonixadmin/aeonix/MANIFEST.MF |tr -c -d 0-9."
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(response if response !='' else 'unknown')

        elif self.operation in ['reboot']:
            ssh_command ="sudo reboot"
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(True)

        elif self.operation in ['stop']:
            ssh_command ="sudo service stop"
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(True)

        elif self.operation in ['start']:
            ssh_command ="sudo service start"
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(True)

        elif self.operation in ['restart']:
            ssh_command ="sudo service restart"
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(True)

        # sipp specific operations ################################

        elif self.operation in ['jobs']:
            ssh_command = 'pgrep sipp'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = len(outlines)
            return('running' if response != 0 else 'stopped',response)            

        elif self.operation in ['terminate']:
            ssh_command = 'killall sipp'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            ssh_command = 'cd ' + self.remote_path
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            ssh_command = 'echo ' + self.timestamp + ' terminate all running sipp jobs' + '\r >> ' + self.remote_path + 'load.info'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            return None

        elif self.operation in ['pack']:
            ssh_command = 'cd ' + self.remote_path + '; zip -r ../sim_`hostname`_' + self.timestamp_zip + '_logs.zip * &>/dev/null &'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            ssh_command = 'echo ' + self.timestamp + ' pack log files to zip' + '\r >> ' + self.remote_path + 'load.info'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)

        elif self.operation in ['download']:
            ssh_command = 'cd ~'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            file_list = self.sftp.listdir()
            for item in file_list:
                if 'zip' in item:
                    print(item)
                    self.sftp.get(item, self.local_path + '/download/' + item)
                    ssh_command = 'echo ' + self.timestamp + ' download file: ' + item + '\r >> ' + self.remote_path + 'load.info'
                    stdin,stdout,stderr = self.client.exec_command(ssh_command)

        elif self.operation in ['upload']:
            try:
                #print('trying...' + self.server + self.remote_path)
                self.sftp.chdir(self.remote_path)
                #ssh_command = 'chmod +x *.sh'
                ssh_command = 'cd ' + self.remote_path + '; chmod +x *.sh' #anxd
                stdin,stdout,stderr = self.client.exec_command(ssh_command)
            except IOError:
                self.sftp.mkdir(self.remote_path)
                self.sftp.chdir(self.remote_path)
            
            files = os.listdir(self.local_path + '/sipp/') 
            print('uploading from: ' + self.local_path + '/sipp/' + ' to: sipp ' + self.host + ' ../' + self.remote_path)
            #print(files)
            #print()
            for filename in files:
                self.sftp.put(self.local_path + '/sipp/' + filename, filename)
            ssh_command = 'cd ' + self.remote_path + '; chmod +x *.sh ; rm -rf *.zip'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            ssh_command = 'echo ' + self.timestamp + ' created and uploaded' + '\r >> ' + self.remote_path + 'load.info'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            #return None

        elif self.operation in ['clean']:
            ssh_command = 'cd ' + self.remote_path + '; chmod +x *.sh ; ./clean_logs.sh &>/dev/null &'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            ssh_command = 'echo ' + self.timestamp + ' clean up the log files ' + '\r >> ' + self.remote_path + 'load.info'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            return None

        elif self.operation in ['clean_zip']:
            ssh_command = 'cd ~' + '; rm -rf *.zip'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            #ssh_command = 'cd ' + remote_path + 'echo ' + timestamp + ' clean up the zip log files ' + '\r >> ' + remote_path + 'load.info'
            ssh_command = 'echo ' + self.timestamp + ' clean up the zip log files ' + '\r >> ' + self.remote_path + 'load.info'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            return None

        # common operations #######################################

        elif self.operation in ['comm']:
            return(self.comm)

        elif self.operation in ['hostname']:
            ssh_command = 'hostname'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(response)

        elif self.opration in ['ipaddress']:
            ssh_command = 'hostname -I'
            stdin,stdout,stderr = self.client.exec_command(ssh_command)
            outlines = stdout.readlines()
            response = ''.join(outlines)
            return(response)

    
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

    
    def statusInfo_anx(section):
        comm = status = version = ''
        comm = environmnt(section, 'aeonix').comm
        if comm != 'established':
            pass
        else:
            status = environmnt(section, 'aeonix', 'status').check()
            version = environmnt(section, 'aeonix', 'version').check()
        return(comm, status, version)

    def statusInfo_sipp(section):
        comm = status = ''
        comm = environmnt(section, 'sipp').comm
        if comm != 'established':
            pass
        else:
            status = environmnt(section, 'sipp', 'jobs').check()
        return(comm, status)
        
