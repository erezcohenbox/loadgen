#!/bin/sh

case $1 in
	collect)
		cp *_.* logs/ 2>/dev/null
		cp *_calldebug.log logs/ 2>/dev/null
		cp *_errors.* logs/ 2>/dev/null
		cp *_error_codes.csv logs/ 2>/dev/null
		cp *_messages.log logs/ 2>/dev/null
		cp *_screen.log logs/ 2>/dev/null
		cp *_shortmessages.log logs/ 2>/dev/null
	;;
	pack)
		cd logs/
		zip -r "../packs/sim_`hostname`_`hostname -I | cut -f1 -d' '`_`date +%Y-%m-%d-%H_%M_%S`_logs.zip" * 1> /dev/null
	;;
	clean)
		cd logs/	
		\rm -rf *
	;;
	cleanZip)
		cd packs/	
		\rm -rf *
	;;	
	erase)
		rm -rf *_.*
		rm -rf *_calldebug.log
		rm -rf *_errors.*
		rm -rf *_error_codes.csv
		rm -rf *_messages.log
		rm -rf *_screen.log
		rm -rf *_shortmessages.log
esac