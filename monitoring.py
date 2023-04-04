import os, shutil, datetime, time
from turtle import left
from configfile import configfile 
import paramiko
from helpers import bcolors
from helpers import output
from environmnt import environmnt

class monitoring:
    def currentStatus():
        print(output.prompt_environment_table_header)
        print(output.prompt_environment_table_border)
        for section in configfile.sectionsNames():
            print(bcolors.INFO + bcolors.IND + 'sipp   : ' + bcolors.RESET + f"{configfile.sectionGetElement(section, 'sipp_host'):<15}", end = '  ')
            systemInfo = environmnt.statusInfo_sipp(section)
            if systemInfo[0] == 'established':
                print(f"{systemInfo[0]:<11}", f'{systemInfo[1][0]:<7}', f'({systemInfo[1][1]:<1} tasks)', sep = '  ')#, end = '  ')
            else:
                print(systemInfo[0])
            
            print(bcolors.INFO + bcolors.IND + 'aeonix : ' + bcolors.RESET + f"{configfile.sectionGetElement(section, 'aeonix_host'):<15}", end = '  ')
            systemInfo = environmnt.statusInfo_anx(section)
            if systemInfo[0] == 'established':
                print(f"{systemInfo[0]:<11}", f'{systemInfo[1][0]:<7}', f'({systemInfo[1][1]:<1} services)' + '  ' + f'{systemInfo[2]:<8}', sep = '  ')#, end = '  ')
            else:
                print(systemInfo[0])
            
            print(output.prompt_environment_table_border)        

            # return('running' if running == 6 and stopped == 0 else 'stopped' if running == 0 and stopped == 6 else 'error', running)   