#!/bin/bash

set -o nounset

activity_command="/bin/bash $0 --run"
pid=$(pgrep -o -f -x "$activity_command")
logfile="/home/holm/activity.log"

NAME="Activity logger"
TAG="ACTIVITYLOGGER"

FACILITY="local2"
infolog="logger -s -p $FACILITY.info -t $TAG "
errorlog="logger -s -p $FACILITY.error -t $TAG "


function closedown {
	# Kill based on parent process, then exit gracefully
	$infolog "Stopping (pid: $pid)"
	pkill -P "$pid"
	#exit 0
}


#
#	If 'quit' and if we have the pid, then exit tunnel
#
[[ $# == 1 && ( $1 == "--quit" || $1 == "-q" ) ]] && {
	if [ "$pid" != "" ] ; then
		closedown
	else
		$infolog "Not running"
	fi
}

[[ $# == 1 && ( $1 == "--run" ) ]] && {

	$infolog "Inside internal method."

	#trap "closedown" SIGINT SIGTERM

	$infolog "After trap inside"
	DBSPID="$(pgrep gnome-session)"
	export DBUS_SESSION_BUS_ADDRESS="$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$DBSPID/environ|cut -d= -f2-)"
	DISPLAY=":0"

	$infolog "DBUS Session set to: $DBUS_SESSION_BUS_ADDRESS"

	#dbus-monitor --session "type='signal',interface='org.gnome.SessionManager.Presence',member='StatusChanged'" | while read line ; do

	#dbus-monitor --session "type='signal',interface='com.canonical.Unity.Session',member='Locked'" | while read line ; do
	dbus-monitor --session "type='signal',interface='com.canonical.Unity.Session'" | while read line ; do
	$infolog "Before dbus check line: $line"
	#if [ x"$(echo "$line" | grep 'boolean true')" != x ] ; then
	if [ x"$(echo "$line" | grep 'Locked')" != x ] ; then
		# runs once when screensaver comes on...
		delay=$(dconf read /org/gnome/desktop/session/idle-delay | cut -d" " -f2)
		actts=$(date --date="$delay seconds ago")
		echo "$(date) - Activity STOPPED" >> "$logfile"
	fi
	#if [ x"$(echo "$line" | grep 'boolean false')" != x ] ; then
	if [ x"$(echo "$line" | grep 'Unlocked')" != x ] ; then
		# runs once when screensaver goes off...
		echo "$(date) - Activity STARTED" >> "$logfile"
	fi
	done
	$infolog "After dbus command: $?"
}


#
#	If no arguments and no pid, then start a tunnel
#
[[ $# == 0 ]] && {
	if [ "$pid" = "" ] ; then
		$infolog "Not running, starting ..."
		$activity_command &
		[ "$?" -ne "0" ] && {
			$errorlog "Could not start, check for errors ..."
		}
	else
		$infolog "Already running"
	fi
}


