#!/bin/bash

if [ -z "$1" ] ; then
	echo "Usage: $0 SOCKET - Where SOCKET is the full path to a socket"
	exit 1
fi

logger -u $1 -p local6.info -t test.sh "Testing the STREAM socket!"
