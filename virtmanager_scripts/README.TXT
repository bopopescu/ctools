Bringing up virtual testbed – automated way

1.Install Virt manager – copy InstallVirtManager.sh from cs-shared and run it on the server
2.Setup bridge interfaces 
3.Copy std ubuntu disk image from cs-shared to the server
4.Make as many copy  of the image as we wish to create vm
5.Reboot server

+++ For the above steps , wrote a script setup_virtmanager.sh 

6.Create vms to install contrail packages

+++ fab -f setup_virtmanager.py create_vm:hosts="nodei15",compute12,/root/tmp/c12image.img,32768,vcpus="4"
+++ fab -f setup_virtmanager.py create_vm:hosts="nodei13",compute2,/root/tmp/c2image.img,32768,mac="52:54:00:6c:71:1c",vcpus="4"
 
7.Change hostname fo the vms .Update cobbler so that vms could be accessed with hostnames

+++fab -f setup_virtmanager.py change_host_name_of_vm:hosts="10.204.217.91",sandipd-c1
Host               new_name


8.Keep snapshot of these vms for future use

+++Need to do manually. Just copy ,for example c12image.img, somewhere

9.Update test bed with the vms as the contrail nodes to install packages

+++Need to do manually

10.fab install_packages,fab install_contrail;fab setup_all

+++Need to manually

11.Do testing
12.Delete vms

+++fab -f setup_virtmanager.py delete_vm:hosts="nodei14" >>> all vms launched on nodei14 will be deleted

13.Create them again from snapshot with the same mac

+++fab -f setup_virtmanager.py create_vm:hosts="nodei15",compute11,/root/tmp/c11image.img,32768,mac="52:54:00:29:5c:e9",vcpus="4"

These fab functions are saved at nodeb11:/home/sandipd/practice/fabfile . 

This fab functions may come handy when we launch large number of vms/delete large number of vms. Creating / deleting a number of vms from ui is a pain.

Regards
Sandip
