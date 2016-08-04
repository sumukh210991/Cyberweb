#! /bin/bash

export LD_LIBRARY_PATH=/usr/local/globus4.2.1/lib:$LD_LIBRARY_PATH


echo "Clearing old session data."
rm -rf data/session/*
if [ ! -n "$1" ]; then 
	echo "Starting up production Pylons server on port" $port
	paster serve -v production.ini http_port=5011  http_host=`hostname -f`
else
	paster serve -v --reload development.ini http_port=$1  http_host=`hostname -f`
fi
