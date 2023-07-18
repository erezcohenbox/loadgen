import os, sys
from configfile import configfile
from prepare import *
from helpers import *
from prepare import prepare
from configfile import configfile
from monitoring import monitoring
def main():
    main_menu()

def main_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + """
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+
    |A|e|o|n|i|x| |L|o|a|d| |G|e|n|
    +-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+    
    Aeonix Load Gen - main menu
    0 -- dashboard view
    1 -- set the configuration file
    2 -- aeonix environmnt settings
    3 -- prepare for simulation
    4 -- activate and control simulation           X
    5 -- monitoring current simulation activties
    6 -- collect information and analyze
    7 -- maintenance operations
    8 -- quit""" + bcolors.PROMPT + """
    Enter your choice [1-8]: """ + bcolors.RESET 
    choice = input(prompt )
    if choice in ["0"]:
        main_menu()
    elif choice in ["1"]:
        configfile_menu()
    elif choice in ["2"]:
        if not 'remove' in configfile.checkOptions():
            print(output.prompt_configfile_unavailable_option_2)
            main_menu()
        environment_menu()
    elif choice in ["3"]:
        prepare_menu()
    elif choice in ["4"]:
        main_menu()
    elif choice in ["5"]:
        monitoring_menu()
    elif choice in ["6"]:
        analyzing_menu()
        #main_menu()
    elif choice in ["7"]:
        main_menu()
    elif choice in ["8"]:
        print(output.prompt_main_goodbye)
        sys.exit()  # Leave the program
    else:
        main_menu()


def configfile_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + """
    Aeonix Load Gen - configuration file menu
    1 -- add a new server
    2 -- delete a server
    3 -- overview of the configuraion file 
    4 -- initialize the configuration file
    5 -- go back\n""" + bcolors.IND + bcolors.INFO + f"""you can use the {', '.join(configfile.checkOptions())} option(s) only""" + bcolors.PROMPT + """
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
            print(output.prompt_configfile_unavailable_option_1)
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
            print(output.prompt_configfile_unavailable_option_1)
        configfile_menu()
    elif choice in ["3"]:
        if 'overview' in configfile.checkOptions():
            configfile.sectionsOverview()
        else:
            print(output.prompt_configfile_unavailable_option_1)
        configfile_menu()
    elif choice in ["4"]:
        if 'initalize' in configfile.checkOptions():
            configfile.initialize()
        else:
            print(output.prompt_configfile_unavailable_option_1)
        configfile_menu()
    elif choice in ["5"]:
        main_menu()
    else:
        configfile_menu()


def environment_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - aeonix environmnt menu
    1 -- upgrade aeonix servers                   X
    2 -- patch aeonix servers (captcha, more...)  X
    3 -- set aeonix server(s) log level           X
    4 -- restart aeonix server(s)
    5 -- stop aeonix server(s)
    6 -- reboot aeonix server(s)
    7 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-6]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        environment_menu()
    elif choice in ["2"]:
        environment_menu()
    elif choice in ["3"]:
        environment_menu()
    elif choice in ["4"]:
        environmnt.anxFuncCall('restart')
        environment_menu()
    elif choice in ["5"]:
        environmnt.anxFuncCall('stop')
        environment_menu()
    elif choice in ["6"]:
        environmnt.anxFuncCall('reboot')
        environment_menu()
    elif choice in ["7"]:
        main_menu()
    else:
        environment_menu()


def prepare_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - prepare for simulation
    1 -- set simulation scope and create files
    2 -- distribute simulation files
    3 -- apply simulation patches                  X
    4 -- terminate sipp simulator(s) activities
    5 -- clean all local collected activity logs
    6 -- clean remote collected aeonix activity logs
    7 -- clean remote collected sipp activity logs
    8 -- reset the environmnt (clean all logs and restart aeonix servers)
    9 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-9]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        prepare.setSimulScope()
        prepare_menu()
    elif choice in ["2"]:
        environmnt.anxFuncCall('upload')
        environmnt.sippFuncCall('upload')
        #environmnt.distributeFiles()
        prepare_menu()
    elif choice in ["3"]:
        prepare_menu()
    elif choice in ["4"]:
        environmnt.sippFuncCall('terminate')
        prepare_menu()
    elif choice in ["5"]:
        prepare.cleanLocalActivity()
        prepare_menu()
    elif choice in ["6"]:
        environmnt.anxFuncCall('cleanLogs')
        environmnt.anxFuncCall('cleanPacks')
        prepare_menu()
    elif choice in ["7"]:
        environmnt.sippFuncCall('cleanLogs')
        environmnt.sippFuncCall('cleanPacks')
        environmnt.sippFuncCall('erase')
        prepare_menu()
    elif choice in ["8"]:
        #prepare.cleanLocalActivity()
        environmnt.anxFuncCall('stop')
        environmnt.anxFuncCall('cleanLogs')
        environmnt.anxFuncCall('cleanPacks')
        environmnt.anxFuncCall('eraseAll')
        environmnt.sippFuncCall('cleanLogs')
        environmnt.sippFuncCall('cleanPacks')
        environmnt.sippFuncCall('erase')
        environmnt.anxFuncCall('start')        
        prepare_menu()
    elif choice in ["9"]:
        main_menu()
    else:
        prepare_menu()


def activate_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - activate and control load activities
    1 -- activate/control endpoints registration        X
    2 -- activate/control endpoints auto answer         X
    3 -- activate/control endpoints call initiation     X
    4 -- auto start all endpoints activities            X
    5 -- block/unblock aeonix server(s) network trafic  X
    6 -- gracefuly stop all endpoints activities        X
    7 -- terminate all simulator(s) activities          X
    8 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-8]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        activate_menu()
    elif choice in ["2"]:
        activate_menu()
    elif choice in ["3"]:
        activate_menu()
    elif choice in ["4"]:
        activate_menu()
    elif choice in ["5"]:
        activate_menu()
    elif choice in ["6"]:
        activate_menu()
    elif choice in ["7"]:
        main_menu()
    elif choice in ["8"]:
        main_menu()
    else:
        activate_menu()

def monitoring_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - monitoring current activity
    1 -- check the environment status                 
    2 -- check sipp simulatior(s) activity            X
    3 -- check aeonix server(s) activity and health   X
    4 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-4]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        monitoring.currentStatus()
        monitoring_menu()
    elif choice in ["2"]:
        monitoring_menu()
    elif choice in ["3"]:
        monitoring_menu()
    elif choice in ["4"]:
        main_menu()
    else:
        monitoring_menu()

def analyzing_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - collect information and analyze
    1 -- collect sipp simulation logs
    2 -- collect aeonix activity logs
    3 -- analyze sipp simulation activity          X (erase All Aeonix logs)
    4 -- analyze aeonix simulation activity        X
    5 -- analyze aeonix jvm activity               X
    6 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-6]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        environmnt.sippFuncCall('collect')
        environmnt.sippFuncCall('pack')
        environmnt.sippFuncCall('download')
        analyzing_menu()
    elif choice in ["2"]:
        environmnt.anxFuncCall('collect')
        environmnt.anxFuncCall('download')
        analyzing_menu()
    elif choice in ["3"]:
        analyzing_menu()
    elif choice in ["4"]:
        analyzing_menu()
    elif choice in ["5"]:
        analyzing_menu()
    elif choice in ["6"]:
        main_menu()
    else:
        analyzing_menu()

def maintenance_menu():
    print(bcolors.RESET)
    prompt = bcolors.MENU + f"""
    Aeonix Load Gen - maintenance operations
    1 -- reset the environment                     X
    2 -- delete all local logs                     X
    3 -- create a snapshot                         X
    4 -- revert to snapshot                        X
    5 -- alarm configuration                       X
    6 -- go back""" + bcolors.PROMPT + """
    Enter your choice [1-6]: """ + bcolors.RESET 
    choice = input(prompt)
    if choice in ["1"]:
        maintenance_menu()
    elif choice in ["2"]:
        maintenance_menu()
    elif choice in ["3"]:
        maintenance_menu()
    elif choice in ["4"]:
        maintenance_menu()
    elif choice in ["5"]:
        maintenance_menu()
    elif choice in ["6"]:
        main_menu()
    else:
        maintenance_menu()

# maintenance

main()
