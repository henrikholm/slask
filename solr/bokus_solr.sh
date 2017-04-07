#!/bin/bash

SOLR="./bin/solr"
POST="./bin/post"
LABEL="bokus"
PORT="8983"

URL="http://localhost:$PORT/solr/admin/cores?action=STATUS"
CORE_XML="<str name=\"name\">$LABEL</str>"

run() {
	$SOLR start
	r=$(curl -s $URL | grep "$CORE_XML")
	if [ -z "$r" ] ; then
		$SOLR create -c $LABEL
		$POST -c $LABEL example/exampledocs/bokus.csv
	fi
}

shutdown() {
	$SOLR stop -all
}

clean() {
	$SOLR delete -c $LABEL
}

r=$($SOLR status | grep "No Solr nodes are running")
if [ -z "$r" ] ; then
	clean
	shutdown
else
	run
fi
