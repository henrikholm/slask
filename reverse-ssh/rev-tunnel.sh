#!/bin/bash

#set -o errexit
#set -o pipefail

set -o nounset


local_port="22"
remote_host="HOSTNAME"
remote_binding_port="11012"

ssh_command="autossh -M 0 -f -N -T foxtrot-tunnel"
pid=$(pgrep -f "autossh -M 0    -N -T foxtrot-tunnel")


#
#	Helper function to print a good tip!
#
function print_config(){

	echo "#--------------------------------------------------------"
	echo "#--- At home, place this in your '~/.ssh/config' file ---"
	echo "#--------------------------------------------------------"
	echo "Host $remote_host"
	echo "HostName $remote_host.example.com"
	echo "Port 22"
	echo "User $USER"
	echo "IdentityFile /home/$USER/.ssh/<RSA-FILE>"
	echo ""
	echo "Host work"
	echo "User WORK-USER"
	echo "ProxyCommand ssh $remote_host nc -w 120 localhost $remote_binding_port"
	echo "#--------------------------------------------------------"

}

#
#	If invoked with '-h' print usage
#	including short '.ssh/config' example
[[ $# == 1 && ( $1 == "--help" || $1 == "-h" ) ]] && {
		echo "Usage: $0 [-q | --quit]"
		print_config
		exit
}

#
#	If 'quit' and if we have the pid, then exit tunnel
#
[[ $# == 1 && ( $1 == "--quit" || $1 == "-q" ) ]] && {
	if [ "$pid" != "" ] ; then
		echo "Quitting tunnel ... (pid: $pid)"
		kill "$pid"
	else
		echo "Tunnel not running"
	fi
}

#
#	If no arguments and no pid, then start a tunnel
#
[[ $# == 0 ]] && {
	if [ "$pid" = "" ] ; then
		echo "No tunnel, starting one"
		$ssh_command
		[ "$?" -ne "0" ] && {
			echo ""
			echo "Make sure '$remote_host' is accessible as 'ssh $remote_host', preferably in '.ssh/config'"
			echo ""
		}
	else
		echo "Tunnel already running"
	fi
}


