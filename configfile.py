import os
import ipaddress #, datetime
from configobj import ConfigObj
from helpers import bcolors



configFileName = 'configfile.ini'

try:
    configFileObject = ConfigObj(configFileName,raise_errors=True)
except:
    file = open(configFileName,"w")
    file.close()
    configFileObject = ConfigObj(configFileName,raise_errors=True)

class configfile:

    def initialize():
        with open(configFileName, 'w') as configfile:
            pass
        return

    def sectionsCount():
        return(len(configFileObject.sections))
        #5

    def sectionsNames():
        return(configFileObject.sections)
        #['1.1.1.1', '10.10.10.10', '100.100.100.100', '5.5.5.5', '6.6.6.6']

    def sectionsNamesDisplay():
        return(' | '.join(configFileObject.sections))
        #1.1.1.1 | 10.10.10.10 | 100.100.100.100 | 5.5.5.5 | 6.6.6.6

    def checkOptions():
        configFileOptions = ''
        try:
            with open(configFileName) as configFile:
                filesize = os.path.getsize(configFileName)
                if filesize > 0:
                    configFileOptions = ['add','remove','overview']
                else:
                    configFileOptions = ['add']
        except FileNotFoundError:
            configFileOptions = ['initialize']
        return(configFileOptions)

#------------------------------------------------------------------------------------------

    def sectionDelete():
        if 'remove' in configfile.checkOptions():
            sections = configfile.sectionsNames()
            print(bcolors.INFO + bcolors.IND + str(configfile.sectionsCount()) + ' sever(s) in the list:' + bcolors.RESET)
            i = 0
            for element in sections:
                i += 1
                print(bcolors.IND + str(i) + ': ' + str(element), end="")
            print() 
            try:
                choice = input(bcolors.PROMPT + bcolors.IND + 'Choose sever to delete [1-'+ str(i) + ']: ' + bcolors.RESET)
                if int(choice) < 1 or int(choice) > i:
                    return(False)
                selection = sections[int(choice) - 1]
                return(selection)
            except (ValueError, IndexError):
                return(False)    


    def sectionRemove(aeonix_host):
        if 'remove' in configfile.checkOptions():
            try:
                configFileObject.sections.remove(aeonix_host)
                configFileObject.write()
                return (True)
            except ValueError:
                return (False)
        else:
            return(False)

    #------------------------------------------------------------------------------------------

    def sectionAdd():
        if 'add' in configfile.checkOptions():
            print(bcolors.INFO + bcolors.IND + 'adding new server section:' + bcolors.RESET)
            elementKeys = ['aeonix host', 'aeonix user', 'aeonix password', 'aeonix web user',
                            'aeonix web password', 'sipp host', 'sipp user', 'sipp password']
            elementKeysInput = []

            for iter in range(8):
                elementKeysInput.append(input(bcolors.IND + f'{elementKeys[iter]} = '))
                
                if 'host' in elementKeys[iter]:
                    try:
                        ipaddress.ip_address(elementKeysInput[iter]) 
                    except:
                        return (False)
                else:
                    if " " in elementKeysInput[iter] or elementKeysInput[iter] == "":
                        return (False)
            return(elementKeysInput)
        else:
            return(False)

    def sectionAppend(elementKeysInput):
        configFileObject[elementKeysInput[0]] = {}
        configFileObject[elementKeysInput[0]]['aeonix_host'] = elementKeysInput[0]
        configFileObject[elementKeysInput[0]]['aeonix_user'] = elementKeysInput[1]
        configFileObject[elementKeysInput[0]]['aeonix_password'] = elementKeysInput[2]
        configFileObject[elementKeysInput[0]]['aeonix_web_user'] = elementKeysInput[3]
        configFileObject[elementKeysInput[0]]['aeonix_web_password'] = elementKeysInput[4]
        configFileObject[elementKeysInput[0]]['sipp_host'] = elementKeysInput[5]
        configFileObject[elementKeysInput[0]]['sipp_user'] = elementKeysInput[6]
        configFileObject[elementKeysInput[0]]['sipp_password'] = elementKeysInput[7]
        configFileObject.write()
        return

#------------------------------------------------------------------------------------------

    def sectionsOverview():
        if configfile.sectionsCount() >= 1:
            print(bcolors.INFO + bcolors.IND + str(configfile.sectionsCount()) + ' sever(s) in the list:' + bcolors.RESET)
            file = open(configFileName,"r")
            fileLines = file.readlines()
            count = 0
            for line in fileLines:
                count += 1
                if line[0] =='[':
                    print()
                print(bcolors.IND + format(line.strip()))
            file.close()
        else:
            print(bcolors.FAIL + bcolors.IND + 'configuration file is empty' + bcolors.RESET)
            return

#------------------------------------------------------------------------------------------

    def sectionGetElements(aeonix_host):
        serverdict = {}
        serverdict.clear
        SECTION = aeonix_host
        try:
            aeonix_host = configFileObject[SECTION]['aeonix_host']
        except KeyError:
            return(False)
        aeonix_user = configFileObject[SECTION]['aeonix_user']
        aeonix_password = configFileObject[SECTION]['aeonix_password']
        aeonix_web_user = configFileObject[SECTION]['aeonix_web_user']
        aeonix_web_password = configFileObject[SECTION]['aeonix_web_password']
        sipp_host = configFileObject[SECTION]['sipp_host']
        sipp_user = configFileObject[SECTION]['sipp_user']
        sipp_password = configFileObject[SECTION]['sipp_password']
        serverdict = {'section':SECTION, 'aeonix_host': aeonix_host, 'aeonix_user': aeonix_user, 
                        'aeonix_password':aeonix_password, 'aeonix_web_user': aeonix_web_user,
                        'aeonix_web_password': aeonix_web_password, 'sipp_host':sipp_host, 
                        'sipp_user': sipp_user, 'sipp_password': sipp_password}
        return(serverdict)

    def sectionGetElement(aeonix_host, elementName):
        try:
            elementValue = configfile.sectionGetElements(aeonix_host)[elementName]
        except TypeError:
            return(False)
        return(elementValue)

    def sectionGetCredentials(aeonix_host, scope):
        try:
            if scope == 'aeonix':
                host = configfile.sectionGetElements(aeonix_host)['aeonix_host']
                user = configfile.sectionGetElements(aeonix_host)['aeonix_user']
                password = configfile.sectionGetElements(aeonix_host)['aeonix_password']
            elif scope == 'aeonix_web':
                host = configfile.sectionGetElements(aeonix_host)['aeonix_host']
                user = configfile.sectionGetElements(aeonix_host)['aeonix_web_user']
                password = configfile.sectionGetElements(aeonix_host)['aeonix_web_password']
            elif scope == 'sipp':
                host = configfile.sectionGetElements(aeonix_host)['sipp_host']
                user = configfile.sectionGetElements(aeonix_host)['sipp_user']
                password = configfile.sectionGetElements(aeonix_host)['sipp_password']
        except:
            return(False)    
        return(host, user, password)

#------------------------------------------------------------------------------------------