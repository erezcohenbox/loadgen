import os, shutil, datetime, time
#import environmnt
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#timestamp_zip = datetime.datetime.now().strftime("_%Y-%m-%d_%H_%M_%S") 

class bcolors:
    #PROMPT   =   '\033[90m'    #GRAY
    PROMPT   =   '\033[93m'     #YELLOW
    FAIL     =   '\033[91m'     #RED
    PASS     =   '\033[92m'     #GREEN
    WARNING  =   '\033[93m'     #YELLOW
    WARNINGX =   '\033[95m'     #PURPLE/PINK
    INFO     =   '\033[96m'     #LIGHT BLUE
    MENU     =   '\033[97m'     #WHITE
    RESET    =   '\033[0m'      #RESET
    CLS      =   '\033[2J'      #CLS
    IND      =   '    '         #INDENTATION

class output:
    prompt_main_goodbye    = bcolors.WARNING + bcolors.IND + "> goodbye...\n" + bcolors.RESET

    prompt_configfile_fail = bcolors.FAIL + bcolors.IND + 'invalid entry -or- user aborted' + bcolors.RESET
    prompt_configfile_pass = bcolors.PASS + bcolors.IND + 'successfully updated' + bcolors.RESET
    prompt_configfile_unavailable_option_1 = bcolors.FAIL + bcolors.IND + 'option is unavailable' + bcolors.RESET
    prompt_configfile_unavailable_option_2 = bcolors.FAIL + bcolors.IND + 'option is unavailable, please set the configuration file first' + bcolors.RESET

    prompt_prepare_simulation_scope             = bcolors.INFO + bcolors.IND + 'the following data was collected : ' + bcolors.RESET
    prompt_prepare_simulation_scope_servers     = bcolors.INFO + bcolors.IND + '- load test configuration contains : ' + bcolors.RESET
    prompt_prepare_simulation_scope_users       = bcolors.INFO + bcolors.IND + '- total capacity load amount of    : ' + bcolors.RESET
    prompt_prepare_simulation_scope_startat     = bcolors.INFO + bcolors.IND + '- scope of imported uesrs          : ' + bcolors.RESET
    prompt_prepare_simulation_scope_method      = bcolors.INFO + bcolors.IND + '- prefered load run method         : ' + bcolors.RESET
    prompt_prepare_scripts_import_ANX_users_1   = bcolors.INFO + bcolors.IND + 'creating: Aeonix ' + bcolors.RESET + 'import_ANX_'
    prompt_prepare_scripts_import_ANX_users_2   = '_users.csv' + bcolors.INFO + ' file having the following fields/order:' + bcolors.RESET
    prompt_prepare_scripts_import_ANX_users_3   = bcolors.INFO + bcolors.IND + '\'User ID\', \'Internal aliases\', \'Description\', \'Phone name\', \'Phone type\', \'Phone Domain\'' + bcolors.RESET
    prompt_prepare_scripts_import_ACC_agents_1  = bcolors.INFO + bcolors.IND + 'creating: ACC ' + bcolors.RESET + 'ala.ini' + bcolors.INFO + ' file' + bcolors.RESET
    prompt_prepare_scripts_import_ACC_agents_2  = bcolors.INFO + bcolors.IND + 'creating: ACC ' + bcolors.RESET + 'import_ACC_600_agents.sql' + bcolors.INFO + ' file' + bcolors.RESET
    prompt_prepare_scripts_handling             = bcolors.INFO + bcolors.IND + 'handling scripts files of simulator server environment: ' + bcolors.RESET
    prompt_prepare_scripts_1_templates          = bcolors.INFO + bcolors.IND + '- copy all templates files to local /scripts directory..' + bcolors.RESET
    prompt_prepare_scripts_2_parsing            = bcolors.INFO + bcolors.IND + '- parsing executable \'*.sh\' scripts' + bcolors.RESET
    prompt_prepare_scripts_3_sequential         = bcolors.INFO + bcolors.IND + '- creating sequential \'*.csv\' files' + bcolors.RESET
    prompt_prepare_scripts_4_loadinfo           = bcolors.INFO + bcolors.IND + '- creating \'load.info\' file' + bcolors.RESET
    prompt_prepare_scripts_5_disconnect         = bcolors.INFO + bcolors.IND + '- setting \'cluster_disconnect.sh\' file' + bcolors.RESET
    prompt_prepare_scripts_done                 = bcolors.PASS + bcolors.IND + 'completed. all scripts were properly created' + bcolors.RESET
    
    prompt_prepare_deleting_old_activity_logs   = bcolors.INFO + bcolors.IND + 'deleting old activity logs for server_' + bcolors.RESET
    
    prompt_environment_table_header             = bcolors.INFO + bcolors.IND + '         ip address       network      status                 version' + bcolors.RESET
    prompt_environment_table_border             = bcolors.INFO + bcolors.IND + '---------------------------------------------------------------------' + bcolors.RESET

class logger():
    log_environment_upload          = 'echo ' + timestamp + ' created and uploaded files \r >> simulator/load.info'
    log_environment_collect         = 'echo ' + timestamp + ' collect log files into ../logs directory \r >> simulator/load.info'
    log_environment_pack            = 'echo ' + timestamp + ' zip all log files from ../logs directory to ../packs directory \r >> simulator/load.info'
    log_environment_download        = 'echo ' + timestamp + ' download all zip files from ../packs directory \r >> simulator/load.info'
    log_environment_clean           = 'echo ' + timestamp + ' clean up the collected log files from ../logs directory \r >> simulator/load.info'
    log_environment_cleanZip        = 'echo ' + timestamp + ' clean up the collected zip files from ../packs directory \r >> simulator/load.info'
    log_environment_erase_aeonix    = 'echo ' + timestamp + ' clean up current aeonix server log files \r >> simulator/load.info'
    log_environment_erase_sipp      = 'echo ' + timestamp + ' clean up current sipp log files \r >> simulator/load.info'
    log_environment_reboot          = 'echo ' + timestamp + ' about to initiate a reboot to the machine! \r >> simulator/load.info'
    log_environment_stop            = 'echo ' + timestamp + ' about to stop the aeonix services \r >> simulator/load.info'
    log_environment_start           = 'echo ' + timestamp + ' about to start the aeonix services \r >> simulator/load.info'
    log_environment_restart         = 'echo ' + timestamp + ' about to restart the aeonix services \r >> simulator/load.info'
    log_environment_terminate       = 'echo ' + timestamp + ' terminate all running sipp jobs \r >> simulator/load.info'