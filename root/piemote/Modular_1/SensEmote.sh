## SensEmote changes the colour of Lifx lights based on ambient facial emotions
## Copyright (C) 2017  Pratik Gupta pratikvgupta@gmail.com
##
## This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
/piemote/Modular_1/bcast.sh
r=`/sbin/iwgetid wlan0 | wc -l`
while [ $r -eq 0 ];
do
	sleep 5s
	r=`/sbin/iwgetid wlan0 | wc -l`
	echo "Waiting for Wifi Network"
done
#sleep 30
trap "echo Exitting SensEmote. Keep it light!; exit;" SIGINT SIGTERM
while true
do
	python /piemote/Modular_1/PiEmote.py 2>/piemote/error.log
	sleep 3
done
