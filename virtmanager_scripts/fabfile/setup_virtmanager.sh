#!/bin/bash

text="# Replace old eth0 config with br0
auto br0
# Use old eth0 config for br0, plus bridge stuff
iface br0 inet dhcp
   bridge_ports    eth0
   bridge_stp      off
   bridge_maxwait  0
   bridge_fd       0"

if [[ ! -f interfaces ]]; then
    echo "interfaces file not found!"
    echo "Creating it"
    echo "$text" > interfaces
else
    echo "File already exists ; not creating it"
fi

fab -f setup_virtmanager.py copy_virt_manager_script
fab -f setup_virtmanager.py run_virtmanager_manager_script
fab -f setup_virtmanager.py setup_bridge_interface
fab -f setup_virtmanager.py copy_image
fab -f setup_virtmanager.py make_copy_of_image:4
fab -f setup_virtmanager.py reboot_server

