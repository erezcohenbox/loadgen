#!/bin/sh

case $1 in
	collect)
		find ../aeonix/logs/server/ -type f -name 'stdout*' -exec cp '{}' ../simulator/logs/ \;
		find ../aeonix/logs/server/ -type f -name 'sysHealth*' -exec cp '{}' ../simulator/logs/ \;
	;;
	pack)
		cd logs/
		zip -r "../packs/anx_`hostname`_`hostname -I | cut -f1 -d' '`_`date +%Y-%m-%d-%H_%M_%S`_logs.zip" * 1> /dev/null
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
		find ../aeonix/logs/server/ -type f -name 'stdout*' -exec rm '{}' \;
		find ../aeonix/logs/server/ -type f -name 'sysHealth*' -exec rm '{}' \;
esac