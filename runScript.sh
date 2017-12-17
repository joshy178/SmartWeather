#!/bin/sh

COMMAND=/home/pi/SmartWeather/SmartWeather.py
LOGFILE=restart.txt

writelog() {
  now=`date`
  echo "$now $*" >> $LOGFILE
  echo "The SmartWeather Raspberry Pi script crashed at $now and has now restarted." | mail -s "SmartWeather Crash" joshieserva@gmail.com
}

writelog "Starting"
while true ; do
  $COMMAND
  writelog "Exited with status $?"
  writelog "Restarting"
done
