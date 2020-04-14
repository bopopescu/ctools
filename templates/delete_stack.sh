#!/bin/bash
source /etc/contrail/openstackrc
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"
    if [[ $line == "test_server"* ]]; then
	heat stack-delete -y $line
        sleep 40
	heat stack-list | grep $line
        if [ $? -eq 0 ]; then 
            sleep 20
	fi
    fi
done < "$1"
while IFS='' read -r line || [[ -n "$line" ]]; do
    if [[ $line == "test_network"* ]]; then
        heat stack-delete -y $line
        sleep 20
    fi    
done < "$1"
