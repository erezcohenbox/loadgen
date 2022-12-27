import os, sys
from configfile import configfile
from prepare import *
from helpers import *
from prepare import prepare
from configfile import configfile
def main():
    main_menu()

def main_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + """
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+
    |A|e|o|n|i|x| |L|o|a|d| |G|e|n|
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+    
    Aeonix Load Gen - main menu
    1 -- set the configuration file
    2 -- system environmnt status and settings
    3 -- prepare for simulation
    4 -- prepare aeonix for load running
    5 -- run load tests
    6 -- quit""" + bcolors.PROMPT + """
    Enter your choice [1-5]: """ + bcolors.RESET 
    choice = input(prompt )
    if choice in ["1"]:
        configfile_menu()
    elif choice in ["2"]:
        environment_menu()
    elif choice in ["3"]:
        prepare_menu()
    elif choice in ["4"]:
        main_menu()
    elif choice in ["5"]:
        main_menu()
    elif choice in ["6"]:
        print(output.prompt_main_goodbye)
        sys.exit()  # Leave the program
    else:
        main_menu()


def configfile_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - configuration file menu
    1 -- add a new server
    2 -- delete a server
    3 -- overview the configuraion file 
    4 -- initialize the configuration file
    5 -- go back
    you can use the {', '.join(configfile.checkOptions())} option(s) only""" + bcolors.PROMPT + """
    Enter your choice [1-5]: """ + bcolors.RESET
    choice = input(prompt)
    if choice in ["1"]:
        if 'add' in configfile.checkOptions():
            check = configfile.sectionAdd()
            if check == False:
                print(output.prompt_configfile_fail)
            else:
                configfile.sectionAppend(check)
                print(output.prompt_configfile_pass)
        else:
            print(output.prompt_configfile_unavailable_option)
        configfile_menu()
    elif choice in ["2"]:
        if 'remove' in configfile.checkOptions():
            check = configfile.sectionDelete()
            if check == False:
                print(output.prompt_configfile_fail)
            else:
                configfile.sectionRemove(check)
                print(output.prompt_configfile_pass)
        else:
            print(output.prompt_configfile_unavailable_option)
        configfile_menu()
    elif choice in ["3"]:
        if 'overview' in configfile.checkOptions():
            configfile.sectionsOverview()
        else:
            print(output.prompt_configfile_unavailable_option)
        configfile_menu()
    elif choice in ["4"]:
        if 'initalize' in configfile.checkOptions():
            configfile.initialize()
        else:
            print(output.prompt_configfile_unavailable_option)
        configfile_menu()
    elif choice in ["5"]:
        main_menu()
    else:
        configfile_menu()


def environment_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - system environmnt menu
    1 -- check environment status
    2 -- upgrade servers
    3 -- patch servers
    4 -- restart aeonix server(s)
    5 -- stop aeonix server(s)
    6 -- reboot aeonix server(s)
    7 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-6]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        print(output.prompt_environment_table_header)
        print(output.prompt_environment_table_border)
        for section in configfile.sectionsNames():
            print(bcolors.INFO + bcolors.IND + 'aeonix : ' + bcolors.RESET + f"{configfile.sectionGetElement(section, 'aeonix_host'):<15}", end = '  ')
            systemInfo = environmnt.statusInfo_anx(section)
            print(f"{systemInfo[0]:<11}", f'{systemInfo[1]:<7}' + '  ' + f'{systemInfo[2]:<8}', sep = '  ')#, end = '  ')
            print(bcolors.INFO + bcolors.IND + 'sipp   : ' + bcolors.RESET + f"{configfile.sectionGetElement(section, 'sipp_host'):<15}", end = '  ')
            systemInfo = environmnt.statusInfo_sipp(section)
            print(f"{systemInfo[0]:<11}", f'{systemInfo[1]:<7}', sep = '  ')#, end = '  ')
            print(output.prompt_environment_table_border)
        environment_menu()
    elif choice in ["2"]:
        environment_menu()
    elif choice in ["3"]:
        environment_menu()
    elif choice in ["4"]:
        environment_menu()
    elif choice in ["5"]:
        environment_menu()
    elif choice in ["6"]:
        environment_menu()
    elif choice in ["7"]:
        main_menu()
    else:
        environment_menu()


def prepare_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - prepare sipp for simulation
    1 -- set simulation scope and create files
    2 -- upload all the simulation files
    3 -- apply simulation patches (captcha, etc..)
    4 -- restart servers
    5 -- stop servers
    6 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-6]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        usersValue = prepare.getUsersValue()
        startatValue = prepare.getStartatValue()
        methodValue = prepare.getMethodValue()
        print()
        print(output.prompt_prepare_simulation_scope)
        print(output.prompt_prepare_simulation_scope_servers + str(configfile.sectionsCount()) + 
                    ' server(s)')
        print(output.prompt_prepare_simulation_scope_users + str(usersValue) + ' users')
        print(output.prompt_prepare_simulation_scope_startat + 'from user ' + str(startatValue) + 
                    ' to user ' + str(startatValue + usersValue - 1))
        print(output.prompt_prepare_simulation_scope_method + methodValue)
        
        prepare.createSimFiles(usersValue, startatValue, methodValue)
        print(output.prompt_prepare_scripts_done)
        prepare_menu()

    elif choice in ["2"]:
        prepare.uploadSimFiles()
        prepare_menu()
    elif choice in ["3"]:
        prepare_menu()
    elif choice in ["4"]:
        prepare_menu()
    elif choice in ["5"]:
        prepare_menu()
    elif choice in ["6"]:
        main_menu()
    else:
        environment_menu()

main()
