"""
Author : Soumil Kulkarni
Script Name: sanity_summary_tool.py
Description: The inputs to this script are the exact Branch Name and the exact Build Number. The script will fetch the results of all the sanity results of that build and 
              displays them as a summary in the terminal or can create a html file which when opened from the browser have hyperlinks to the entire report. 

Usage : 
		python sanity_summary_tool.py --branch <branch name > --build <build number> --output_format <print/html> --dest_file_name <name for the destiantion html file (optional)>
		-> if the output format is 'html', mentioning of the '--dest_file_name' parameter is optional 
		-> if '--dest_file_name' parameter is not given when '--output_format=html', the dest file name by default is 'result_summary.html'
		-> if the output format is 'print', mentioning of the '--dest_file_name' parameter is not required. 

		eg : python sanity_summary_tool.py --branch all --build latest --output_format html --dest_file_name test_sanity_10.html
"""
import time
import sys 
from bs4 import BeautifulSoup
import ConfigParser
import paramiko
import os
import re
import subprocess
import urllib 
from optparse import OptionParser
import json


def check_if_object_downloaded(file=''):
	temp = False
	while(temp == False):
		time.sleep(5)
		a_tmp = subprocess.Popen('ls | grep %s' %file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate() 
		if a_tmp[0] != '':
			temp = True
		else:
			print "Waiting for some more time for the file to get downloaded : %s" % file
	
def check_if_object_deleted(file=''):
	temp = False
	while (temp == False):
		time.sleep(5)
		a_tmp = subprocess.Popen('ls | grep %s' %file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
		if a_tmp[0] == '':
			temp = True
		else:
			print "Waiting for some more time for the file to get deleted : %s" % file

def get_summary_from_html_file(html_file_link):
	os.system('wget -q %s -O junit-noframes.html' %html_file_link)
	time.sleep(10)
	check_if_object_downloaded(file='junit-noframes.html')
	file = open('junit-noframes.html', 'r')
	soup = BeautifulSoup(file)
	#print soup	
	th_tags = soup.findAll('th')
	td_tags = soup.findAll('td')
	final_th_tags = []
	final_td_tags = []
	final_td_tags_1 = []
	return_dict = {}
	for i in range(6):
		a = str(th_tags[i]).replace('<th>', '')
		b = str(a).replace('</th>', '')
		final_th_tags.append(b)
	return_dict["labels"] = final_th_tags
	final_td_tags = [td_tags[2], td_tags[3], td_tags[4], td_tags[5], td_tags[6], td_tags[7]]
	for i in final_td_tags:
		a = str(i).replace('<td>', '')
		b = str(a).replace('</td>', '')
		final_td_tags_1.append(b)
	return_dict["values"] = final_td_tags_1
	file.close()
	os.system('rm -f /root/sanity_dashboard_data/process_results/junit-noframes.html')
	check_if_object_deleted(file='junit-noframes.html')
	return return_dict



def get_data_from_ini_file(file_1):
	config = ConfigParser.ConfigParser()
	return_dict = {}
	#config_file = open('report_details_jenkins-centos71_kilo_Multi_Node_Sanity-358_2017_03_22_22_10_40.ini', 'r')
	config_file = open(file_1, 'r')
	config.readfp(config_file)
	build = config.get('Test', 'build')
	distro = config.get('Test', 'distro_sku')
	report = config.get('Test', 'report')
	topology = config.get('Test', 'topology')
	topo_summary = topology
	a_temp = topo_summary.split(':')
	#print a_temp
	temp_list = ['Config Nodes', 'Control Nodes', 'Compute Nodes', 'Openstack Node', 'WebUI Node', 'Analytics Nodes', 'Physical Devices']
	b_temp = []
	for del_string in temp_list:
		for rep_string in a_temp:
			if del_string in rep_string:
				a = rep_string.replace(del_string, '')
				b_temp.append(a)
	#print b_temp
	c_temp = []
	for j in b_temp:
		a = j.replace(' ', '')
		c_temp.append(a)
	#print c_temp
	d_temp = []
	for j in c_temp:
		a = j.replace("[u'", '')
		d_temp.append(a)
	#print d_temp
	e_temp = []
	for j in d_temp:
		a = j.replace("'", '')
		e_temp.append(a)
	#print e_temp
	f_temp = []
	for j in e_temp:
		a = j.replace("]", '')
		f_temp.append(a)
	del f_temp[0]
	#print f_temp
	first_element = f_temp[0]
	itr = 0
	for j in f_temp:
		if j != first_element:
			itr = 1
	if itr == 0:
		#print "Topology Summary: SINGLE NODE CLUSTER"
		return_dict['topo_summary'] = 'SINGLE-NODE CLUSTER'
	else:
		#print "Topology Summary: MULTI-NODE CLUSTER"
		return_dict['topo_summary'] = 'MULTI-NODE CLUSTER'
	#print distro
	#print build
	#print report

	return_dict["build"] = build
	return_dict["distro"] = distro
	return_dict["report"] = report
	return_dict["topology"] = topology
	return return_dict

def print_summary():
	value_dict = get_summary()
	label_list = value_dict["labels"]
	value_list = value_dict["values"]
	ini_dict = get_data_from_ini_file()
	print "\nDistro : %s" %ini_dict["distro"]
	print "-----------------------------------------"
	print "Build : %s" % ini_dict["build"]
	print "-----------------------------------------"
	print "Total Tests : %s" %value_list[0]
	print "-----------------------------------------"
	print "Failures : %s" %value_list[1]
	print "-----------------------------------------"
	print "Errors : %s" %value_list[2]
	print "-----------------------------------------"
	print "Skipped : %s" %value_list[3]
	print "-----------------------------------------"
	print "Success Rate (Percent): %s " %value_list[4]
	print "-----------------------------------------"
	print "Time Taken : %s" %value_list[5]
	print "-----------------------------------------"
	rep_path = str(ini_dict["report"]).replace('http://10.204.216.50/', 'http://mayamruga.englab.juniper.net/')
	print "Path to the html file (Paste this link on the browser): %s\n" % rep_path


# Function for getting the exact path to download the ini files.
def get_exact_path(branch='', build='', openstack_version=''):
	host = host = '10.204.216.50'
	username = 'bhushana'
	password = 'c0ntrail!23'
	ini_list = []
	err_list = []
	path = "/var/www/html/sanity/cb-sanity/"
	if branch == 'R3.2':
		if openstack_version == 'kilo':
			path = path + 'CB-R3.2-ubuntu14-kilo/daily/R3.2/'
		elif openstack_version == 'liberty':
			path = path + 'CB-R3.2-ubuntu14-liberty/daily/R3.2/'
		elif openstack_version == 'mitaka':
			path = path + 'CB-R3.2-ubuntu14-mitaka/daily/R3.2/'
	elif branch == 'R4.0':
		if openstack_version == 'mitaka':
			path = path + 'CB-R4.0-ubuntu14-mitaka/daily/R4.0/'
			#print path
		elif openstack_version == 'newton':
			path = path + 'CB-R4.0-ubuntu16-newton/daily/R4.0/'
	elif branch == 'mainline':
		if openstack_version == 'mitaka':
			path = path + 'CB-mainline-ubuntu14-mitaka/daily/mainline/'
		elif openstack_version == 'newton':
			path = path + 'CB-mainline-ubuntu16-newton/daily/mainline/'

	client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username = username, password = password)
	stdin, stdout, stderr = client.exec_command('ls %s | grep %s' %(path, build))
	a = stdout.readlines()
	for i in a:
		b = i.replace('\n', '')
		#print b
		ini_list.append(b)
	client.close()
	if len(ini_list) == 1:
		path = path + ini_list[0]
		#print path 
		return path 
		



def get_all_ini_files(branch='', build='', openstack_version=''):
	host = '10.204.216.50'
	username = 'bhushana'
	password = 'c0ntrail!23'
	ini_list = []
	final_ini_list  = []
	error_list = []
	path = get_exact_path(branch=branch, build=build, openstack_version=openstack_version)
	#print path
	if path == None:
		print "Branch name or Build Number is wrong, please check ..."
	else:
		if branch == 'R3.2':
			if openstack_version == 'mitaka':
				client = paramiko.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				client.connect(host, username = username, password = password)
				#stdin, stdout, stderr = client.exec_command('ls %s | grep .ini | grep jenkins-ubuntu-14-04_mitaka_Multi_Node_Sanity' %path)
				stdin, stdout, stderr = client.exec_command('ls %s | grep .ini' %path)
				ini_list =stdout.readlines()
				error_list = stderr.readlines()
				client.close()
			elif openstack_version == 'kilo':
				client = paramiko.SSHClient()
                		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                		client.connect(host, username = username, password = password)
				#stdin, stdout, stderr = client.exec_command('ls %s | grep .ini | grep jenkins-ubuntu-14-04_kilo_Multi_Node_Sanity' %path)
                		stdin, stdout, stderr = client.exec_command('ls %s | grep .ini' %path)
				ini_list.extend(stdout.readlines())
                		error_list.extend(stderr.readlines())
                		client.close()
			elif openstack_version == 'liberty':
				client = paramiko.SSHClient()
                        	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        	client.connect(host, username = username, password = password)
                        	#stdin, stdout, stderr = client.exec_command('ls %s | grep .ini | grep jenkins-ubuntu-14-04_liberty_Multi_Node_Sanity' %path)
                        	stdin, stdout, stderr = client.exec_command('ls %s | grep .ini' %path)
				ini_list.extend(stdout.readlines())
                        	error_list.extend(stderr.readlines())
                        	client.close()
		
			print ini_list
			for i in ini_list:
				a = str(i).replace('\n', '')
				final_ini_list.append(a)
			#for i in final_ini_list:
			#	print i
			if (len(error_list)==0):
				return final_ini_list
			else:
				return error_list 

		elif branch == 'R4.0':
			if openstack_version == 'mitaka':
				client = paramiko.SSHClient()
                                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                client.connect(host, username = username, password = password)
                                #stdin, stdout, stderr = client.exec_command('ls %s | grep .ini | grep report_details_jenkins-VT_CB_R4.0_ub1404_Mitaka' %path)
                                stdin, stdout, stderr = client.exec_command('ls %s | grep .ini' %path)
				ini_list =stdout.readlines()
				#print "Hey"
				#print ini_list
                                error_list = stderr.readlines()
                                client.close()
			elif openstack_version == 'newton':
				client = paramiko.SSHClient()
                                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                client.connect(host, username = username, password = password)
                                #stdin, stdout, stderr = client.exec_command('ls %s | grep .ini | grep report_details_jenkins-VT_CB_R4.0_ub1604_Newton' %path)
                                stdin, stdout, stderr = client.exec_command('ls %s | grep .ini' %path)
				ini_list =stdout.readlines()
                                error_list = stderr.readlines()
                                client.close()

			print ini_list
                        for i in ini_list:
                                a = str(i).replace('\n', '')
                                final_ini_list.append(a)
                        #for i in final_ini_list:
                        #       print i
                        if (len(error_list)==0):
                                return final_ini_list
                        else:
                                return error_list

		elif branch == 'mainline':
			if openstack_version == 'mitaka':
                                client = paramiko.SSHClient()
                                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                client.connect(host, username = username, password = password)
                                #stdin, stdout, stderr = client.exec_command('ls %s | grep .ini | grep report_details_jenkins-VT_CB_mainline_ub1404_Mitaka' %path)
                                stdin, stdout, stderr = client.exec_command('ls %s | grep .ini' %path)
				ini_list =stdout.readlines()
                                error_list = stderr.readlines()
                                client.close()
                        elif openstack_version == 'newton':
                                client = paramiko.SSHClient()
                                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                client.connect(host, username = username, password = password)
				stdin, stdout, stderr = client.exec_command('ls %s | grep .ini' %path)
                                #stdin, stdout, stderr = client.exec_command('ls %s | grep .ini | grep report_details_jenkins-VT_CB_mainline_ub1604_Newton' %path)
                                ini_list =stdout.readlines()
                                error_list = stderr.readlines()
                                client.close()

			print ini_list
                        for i in ini_list:
                                a = str(i).replace('\n', '')
                                final_ini_list.append(a)
                        #for i in final_ini_list:
                        #       print i
                        if (len(error_list)==0):
                                return final_ini_list
                        else:
                                return error_list


info_dict = {"mitaka_jobs": {}, "kilo_jobs": {}, "liberty_jobs": {}, "R4.0_mitaka_jobs":{}, "R4.0_newton_jobs":{}, "mainline_mitaka_jobs": {}, "mainline_newton_jobs": {}}
#info_dict = {"mitaka_jobs": {}, "R4.0_mitaka_jobs":{}, "R4.0_newton_jobs":{}, "mainline_mitaka_jobs": {}, "mainline_newton_jobs": {}}

def get_detailed_data_from_ini_files(branch='', build='', openstack_version=''):
	host = '10.204.216.50'
	username = 'bhushana'
	password = 'c0ntrail!23'
	#info_dict = {"mitaka_jobs": {}, "kilo_jobs": {}, "liberty_jobs": {}}
	path = str(get_exact_path(branch=branch, build=build, openstack_version=openstack_version))
	print path
	if path == None:
		print "The Branch name or build number is wrong please check"
	else:
		if branch == "R3.2":
			#path = '/var/www/html/Docs/sanity/daily/R3.0/3.0.2.0-26'
			#print openstack_version
			#print "I am in get_detailed_data_from_ini_files"
			ini_list = get_all_ini_files(branch=branch, build=build, openstack_version=openstack_version)
			#print ini_list
			if not ini_list:
				print "There is an Error Fetching all the ini files from the given build: %s and Branch : %s" %(build,branch) 
                        	info_dict[build] ={}
			else:
				print "\nDownloading all the report.ini files in the given path and getting the reiquired data from them "

                        	num = 0
                        	#print "\nDownloading all the report.ini files in the given path and getting the reiquired data from them "
                        	#info_dict[build] ={}
				final_test_number_kilo = 0
				final_test_number_mitaka = 0
				final_test_number_liberty = 0  
				final_success_rate_kilo = 0
				final_success_rate_mitaka = 0
				final_success_rate_liberty = 0
                        	for i in ini_list:
					
                                	new_path = path + '/'+ i
					print new_path
                                	#print "Downloading the following file: ",new_path
                                	os.system('sshpass -p "c0ntrail!23" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=error bhushana@10.204.216.50:%s .' %new_path)
					time.sleep(10)
					check_if_object_downloaded(file=i)
                                	Dict_1 = get_data_from_ini_file(i)
			
					test_num_dict = get_summary_from_html_file(Dict_1['report'])
					Dict_1['testcase_results'] = test_num_dict
					internal_no_of_testcase = int(Dict_1['testcase_results']['values'][0])
					internal_success_rate = Dict_1['testcase_results']['values'][4]
					#print Dict_1
					#import pdb; pdb.set_trace()	
                                	#info_dict[build][num] = Dict_1
					#if "jenkins-ubuntu-14-04_kilo_Multi_Node_Sanity" in i :

					if "VT_CB_R3.2_ub1404_Kilo" in i :
						if internal_no_of_testcase > final_test_number_kilo:
							final_test_number_kilo = internal_no_of_testcase
							temp_success_rate = float((internal_success_rate.replace('%','')))
							final_success_rate_kilo = temp_success_rate
							info_dict["kilo_jobs"][build] = Dict_1
						elif internal_no_of_testcase == final_test_number_kilo:
							temp_success_rate = float((internal_success_rate.replace('%','')))
							if temp_success_rate > final_success_rate_kilo:
								final_success_rate_kilo = temp_success_rate
								info_dict["kilo_jobs"][build] = Dict_1
					
					#if "jenkins-ubuntu-14-04_mitaka_Multi_Node_Sanity" in i:
					if "VT_CB_R3.2_ub1404_Mitaka" in i:
						if internal_no_of_testcase > final_test_number_mitaka:
							final_test_number_mitaka = internal_no_of_testcase
							temp_success_rate = float((internal_success_rate.replace('%','')))
							final_success_rate_mitaka = temp_success_rate
							info_dict["mitaka_jobs"][build] = Dict_1
						elif internal_no_of_testcase == final_test_number_mitaka:
							temp_success_rate = float((internal_success_rate.replace('%','')))
							if temp_success_rate > final_success_rate_mitaka:
								final_success_rate_mitaka = temp_success_rate
								info_dict['mitaka_jobs'][build] = Dict_1
					
					#if "jenkins-ubuntu-14-04_liberty_Multi_Node_Sanity" in i:
					if "VT_CB_R3.2_ub1404_Liberty" in i:
						if internal_no_of_testcase > final_test_number_liberty:
							final_test_number_liberty = final_test_number_liberty
							temp_success_rate = float((internal_success_rate.replace('%','')))
							final_success_rate_liberty = temp_success_rate
							info_dict['liberty_jobs'][build] = Dict_1
						elif internal_no_of_testcase == final_test_number_liberty:
							temp_success_rate = float((internal_success_rate.replace('%','')))
							if temp_success_rate > final_success_rate_liberty:
								final_success_rate_liberty = temp_success_rate
								info_dict['liberty_jobs'][build] = Dict_1
                                	os.system('rm -f %s' %i)
					check_if_object_deleted(file=i)	
                                	#print "Done %d " %num
                                	num += 1

			#print info_dict
			print "\n"
			print "Adding the summary data to the already collected data from the ini files"
			#print "______________________________________________________________________________________"
			#print "RESULTS :-"
			#print "______________________________________________________________________________________"
                	'''
			if info_dict[build]:
				for i in info_dict[build]:
					test_num_dict = get_summary_from_html_file(info_dict[build][i]["report"])
					info_dict[build][i]["testcase_results"] = test_num_dict
			return info_dict
			'''
			#if build in info_dict["kilo_jobs"]:
			#	#print info_dict["kilo_jobs"][build]
			#	test_num_dict = get_summary_from_html_file(info_dict["kilo_jobs"][build]["report"])
			#	info_dict["kilo_jobs"][build]["testcase_results"] = test_num_dict
			#if build in info_dict["mitaka_jobs"]:
                	#	test_num_dict = get_summary_from_html_file(info_dict["mitaka_jobs"][build]["report"])
                        #	info_dict["mitaka_jobs"][build]["testcase_results"] = test_num_dict

			#if build in info_dict["liberty_jobs"]:
                	#	test_num_dict = get_summary_from_html_file(info_dict["liberty_jobs"][build]["report"])
                        #	info_dict["liberty_jobs"][build]["testcase_results"] = test_num_dict
	
			return_dict = {}
                        return_dict['jobs'] = {}
                        return_dict['jobs']['R3.2_mitaka'] = info_dict['mitaka_jobs']
                        return_dict['jobs']['R3.2_kilo'] = info_dict['kilo_jobs']
                        return_dict['jobs']['R3.2_liberty'] = info_dict['liberty_jobs']
			return return_dict
			#return info_dict
		
		# Get data from branch R4.0 
		elif branch == "R4.0":
			ini_list = get_all_ini_files(branch=branch, build= build, openstack_version=openstack_version)
			if not ini_list:
				print "There is an Error Fetching all the ini files from the given build: %s and Branch : %s" %(build,branch)
				info_dict[build] ={}
			else:
				print "\nDownloading all the report.ini files in the R4.0 branch  path and getting the reiquired data from them "
				num = 0
				final_test_number = 0
				final_success_rate = 0
				final_test_number_newton = 0
				final_success_rate_newton = 0
				for i in ini_list:
					new_path = path + '/' + i
					os.system('sshpass -p "c0ntrail!23" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=error bhushana@10.204.216.50:%s .' %new_path)
					time.sleep(10)
					check_if_object_downloaded(file=i)
					Dict_1 = get_data_from_ini_file(i)
					
					test_num_dict = get_summary_from_html_file(Dict_1['report'])
					Dict_1['testcase_results'] = test_num_dict
					internal_no_of_testcase = int(Dict_1['testcase_results']['values'][0])
					internal_success_rate = Dict_1['testcase_results']['values'][4]
					#print internal_no_of_testcase
					#print internal_success_rate
					#if internal_no_of_testcase > final_test_number :
					#	temp_success_rate = float((internal_success_rate.replace('%','')))
					#	if temp_success_rate > final_success_rate:
									
					#print Dict_1
					
					# The names of thses files are not fixed yet. We might have to chnage it
					if "VT_CB_R4.0_ub1404_Mitaka" in i:
						if internal_no_of_testcase > final_test_number :
							final_test_number = internal_no_of_testcase
							temp_success_rate = float((internal_success_rate.replace('%','')))
							final_success_rate = temp_success_rate
							#print "hey"
							info_dict["R4.0_mitaka_jobs"][build] = Dict_1
						elif internal_no_of_testcase == final_test_number :
							#print "Same no of testcases"
							temp_success_rate = float((internal_success_rate.replace('%','')))
							if temp_success_rate > final_success_rate:
								final_success_rate = temp_success_rate
								info_dict["R4.0_mitaka_jobs"][build] = Dict_1
					if "VT_CB_R4.0_ub1604_Newton" in i:
						if internal_no_of_testcase > final_test_number_newton :
							final_test_number_newton = internal_no_of_testcase
							temp_success_rate = float((internal_success_rate.replace('%','')))
							final_success_rate_newton = temp_success_rate
							info_dict["R4.0_newton_jobs"][build] = Dict_1
						elif internal_no_of_testcase == final_test_number_newton :
							temp_success_rate = float((internal_success_rate.replace('%','')))
							if temp_success_rate > final_success_rate_newton:
								temp_success_rate = temp_success_rate
								info_dict["R4.0_newton_jobs"][build] = Dict_1
					os.system('rm -f %s' %i)
					check_if_object_deleted(file=i)
					num += 1
			print "\n"
			print "Adding the summary data to the already collected data from the ini files"
			#if build in info_dict["R4.0_mitaka_jobs"]:
			#	test_num_dict = get_summary_from_html_file(info_dict["R4.0_mitaka_jobs"][build]["report"])
			#	info_dict["R4.0_mitaka_jobs"][build]["testcase_results"] = test_num_dict

			#if build in info_dict["R4.0_newton_jobs"]:
			#	test_num_dict = get_summary_from_html_file(info_dict["R4.0_newton_jobs"][build]["report"])
			#	info_dict["R4.0_newton_jobs"][build]["testcase_results"] = test_num_dict
	
			#print info_dict
			return_dict = {}
			return_dict['jobs'] = {}
			return_dict['jobs']['R4.0_mitaka'] = info_dict['R4.0_mitaka_jobs']
			return_dict['jobs']['R4.0_newton'] = info_dict['R4.0_newton_jobs']
			return return_dict
			#return info_dict

		# Get data from the mainline branch 
		elif branch == "mainline":
			ini_list = get_all_ini_files(branch=branch, build= build, openstack_version=openstack_version)
			if not ini_list:
				print "There is an Error Fetching all the ini files from the given build: %s and Branch : %s" %(build,branch)
				info_dict[build] ={}
			else:
				print "\nDownloading all the report.ini files in the mainline branch  path and getting the reiquired data from them "
				num = 0
				final_test_number_mitaka = 0
				final_success_rate_mitaka = 0
				final_test_number_newton = 0
				final_success_rate_newton = 0
				for i in ini_list:
					new_path = path + '/' + i
					os.system('sshpass -p "c0ntrail!23" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=error bhushana@10.204.216.50:%s .' %new_path)
					time.sleep(10)
					check_if_object_downloaded(file=i)
					Dict_1 = get_data_from_ini_file(i)

					test_num_dict = get_summary_from_html_file(Dict_1['report'])
					Dict_1['testcase_results'] = test_num_dict
					internal_no_of_testcase = int(Dict_1['testcase_results']['values'][0])
					internal_success_rate = Dict_1['testcase_results']['values'][4]
					
					# The names of thses files are not fixed yet. We might have to chnage it
					if "VT_CB_mainline_ub1404_Mitaka" in i:
						if internal_no_of_testcase > final_test_number_mitaka:
							final_test_number_mitaka = internal_no_of_testcase
							temp_success_rate = float((internal_success_rate.replace('%','')))
							final_success_rate_mitaka = temp_success_rate
							info_dict["mainline_mitaka_jobs"][build] = Dict_1
						elif internal_no_of_testcase == final_test_number_mitaka:
							temp_success_rate = float((internal_success_rate.replace('%','')))
							if temp_success_rate > final_success_rate_mitaka:
								final_success_rate_mitaka = temp_success_rate
								info_dict["mainline_mitaka_jobs"][build] = Dict_1

					if "VT_CB_mainline_ub1604_Newton" in i:
						if internal_no_of_testcase > final_test_number_newton:
							final_test_number_newton = final_test_number_newton
							temp_success_rate = float((internal_success_rate.replace('%','')))
							final_success_rate_newton = temp_success_rate
							info_dict["mainline_newton_jobs"][build] = Dict_1
						elif internal_no_of_testcase == final_test_number_newton:
							temp_success_rate = float((internal_success_rate.replace('%','')))
							if temp_success_rate > final_success_rate_newton:
								final_success_rate_newton = temp_success_rate
								info_dict["mainline_newton_jobs"][build] = Dict_1

					os.system('rm -f %s' %i)
					check_if_object_deleted(file=i)
					num += 1
			print "\n"
			print "Adding the summary data to the already collected data from the ini files"
			#if build in info_dict["mainline_mitaka_jobs"]:
			#	test_num_dict = get_summary_from_html_file(info_dict["mainline_mitaka_jobs"][build]["report"])
			#	info_dict["mainline_mitaka_jobs"][build]["testcase_results"] = test_num_dict

			#if build in info_dict["mainline_newton_jobs"]:
			#	test_num_dict = get_summary_from_html_file(info_dict["mainline_newton_jobs"][build]["report"])
			#	info_dict["mainline_newton_jobs"][build]["testcase_results"] = test_num_dict
			
			return_dict = {}
                        return_dict['jobs'] = {}
                        return_dict['jobs']['mainline_mitaka'] = info_dict['mainline_mitaka_jobs']
                        return_dict['jobs']['mainline_newton'] = info_dict['mainline_newton_jobs']
                        return return_dict
			#return info_dict



def print_report_summary(branch='', build=''):
	info_dict = get_detailed_data_from_ini_files(branch=branch, build=build)
	print "______________________________________________________________________________________"
	print "RESULTS :-"
	print "______________________________________________________________________________________"
	for i in info_dict:
		print "Distro : %s" % info_dict[i]["distro"]
		print "Build : %s" % info_dict[i]["build"]
		print "Report Link : %s" % info_dict[i]["report"]
		topo_string = str(info_dict[i]["topology"])
		replaced_topo_string = topo_string.replace('<br/>', '')
		print "Topology : %s" % replaced_topo_string
		print "Topology Summaty: %s" %info_dict[i]['topo_summary']
		test_result_dict_lables = info_dict[i]["testcase_results"]["labels"]
		test_result_dict_values = info_dict[i]["testcase_results"]["values"]
		#print test_result_dict_lables
		#print test_result_dict_values
		num = len(test_result_dict_values)
		itr = 0
		print "TEST RESULTS SUMMARY : "
		while (itr < num):
			print "   %s : %s " %(test_result_dict_lables[itr], test_result_dict_values[itr])
			itr += 1
		print "______________________________________________________________________________________"


def print_into_text_file(info_dict):
        import os, time
        mydir = os.path.join(os.getcwd(), time.strftime("%Y_%m_%d"))
        if not os.path.exists(mydir):
            os.makedirs(mydir)
        filename = time.strftime("%H_%M_%S") 
        print 'Generating text report at %s/%s' %(mydir,filename)
        f = open(os.path.join(mydir,filename), 'w')
        for key in info_dict:
            for i in info_dict[key]:
	        f.write("Distro : %s\n" % info_dict[key][i]["distro"])
                f.write("Build : %s\n" % info_dict[key][i]["build"])
                f.write("Report Link : %s\n" % info_dict[key][i]["report"])
                topo_string = str(info_dict[key][i]["topology"])
                replaced_topo_string = topo_string.replace('<br/>', '')
                f.write("Topology : %s\n" % replaced_topo_string)
                f.write("Topology Summary: %s\n" %info_dict[key][i]['topo_summary'])
                test_result_dict_lables = info_dict[key][i]["testcase_results"]["labels"]
                test_result_dict_values = info_dict[key][i]["testcase_results"]["values"]
                #print test_result_dict_lables
                #print test_result_dict_values
                num = len(test_result_dict_values)
                itr = 0
                f.write("TEST RESULTS SUMMARY : ")
                while (itr < num):
                        f.write("   %s : %s \n" %(test_result_dict_lables[itr], test_result_dict_values[itr]))
                        itr += 1
                f.write( "______________________________________________________________________________________\n")
        f.close()

def print_xml_file(info_dict):
	import xml.etree.cElementTree as ET
        import os, time
        import json
        with open('result.json', 'w') as fp:
            json.dump(info_dict, fp)
        mydir = os.path.join(os.getcwd(), time.strftime("%Y_%m_%d"))
        if not os.path.exists(mydir):
            os.makedirs(mydir)
        filexml = time.strftime("%H_%M_%S")+".xml"
        filename = os.path.join("/var/www/html/summary.xml")
        #filename = os.path.join(mydir,filexml)
	root = ET.Element("Sanity")
        print 'Generating text report at %s' %(filename)
        for key in info_dict:
            for i in info_dict[key]:
                topo_string = str(info_dict[key][i]["topology"])
                replaced_topo_string = topo_string.replace('<br/>', '')
                dist = ET.SubElement(root, "Distro", name="Run_Info")
                dist.text = info_dict[key][i]["distro"]
		ET.SubElement(dist, "Build", name="Build Number").text = key
		ET.SubElement(dist, "Date",name="Build Date").text = info_dict[key][0]["date"]
		ET.SubElement(dist, "Branch",name="Branch").text = info_dict[key][i]["build"]
		ET.SubElement(dist, "Report",name="Link").text = info_dict[key][i]["report"]
		ET.SubElement(dist, "Topology", name="Testbed Topology").text = info_dict[key][i]['topo_summary'] 
                summ = ''
                test_result_dict_lables = info_dict[key][i]["testcase_results"]["labels"]
                test_result_dict_values = info_dict[key][i]["testcase_results"]["values"]
                num = len(test_result_dict_values)
                itr = 0

                while (itr < num):
                        summ = summ + " %s:%s " % (test_result_dict_lables[itr], test_result_dict_values[itr])
                        itr += 1
		ET.SubElement(dist, "Summary", name="Result Summary").text = summ 
	tree = ET.ElementTree(root)
	tree.write(filename)

def get_latest_build_number_individual(branch='', openstack_version=''):
	host = '10.84.24.64'
	username = 'root'
	password = 'c0ntrail123'
	path = '/cs-build/'
	if branch == 'R3.2':
		print openstack_version
		print branch
		if openstack_version == 'mitaka':
			path = path + 'CB-R3.2-ubuntu14-mitaka/builds'
		elif openstack_version =='kilo':
			path = path + 'CB-R3.2-ubuntu14-kilo/builds'
		elif openstack_version == 'liberty':
			path = path + 'CB-R3.2-ubuntu14-liberty/builds'
	elif branch == 'R4.0':
		print openstack_version
		print branch
		if openstack_version == 'mitaka':
			path = path + 'CB-R4.0-ubuntu14-mitaka/builds'
		elif openstack_version == 'newton':
			path = path + 'CB-R4.0-ubuntu16-newton/builds'
	elif branch == 'mainline':
		print openstack_version
		print branch
		if openstack_version == 'mitaka':
			path = path + 'CB-mainline-ubuntu14-mitaka/builds'
		elif openstack_version == 'newton':
			path = path + 'CB-mainline-ubuntu16-newton/builds'
	print path	
	#Now lets do some regex to get the exact last build number	
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, username = username, password = password)
	stdin, stdout, stderr = client.exec_command('ls %s -ltrh' %(path))
	a = stdout.readlines()
	client.close()
	#print len(a)
	#print a[(len(a) - 1)]
	#print a
	if a == []:
		return -1
	else:
		len_a = len(a)
		print len_a
		var_b = a[(len_a - 1)]
		print "echo"
		print var_b
		var_b_list = var_b.split(' ')
		#print var_b_list
		var_b_list_len = len(var_b_list)
		#print var_b_list_len
		var_c = var_b_list[(var_b_list_len - 1)]
		#print var_c
		latest_build = var_c.replace('\n', '')
		return latest_build

	

def get_latest_build_number(branch=''):
	branch = branch 
	host = '10.84.5.31'
	username = 'vivekgarg'
	password = 'vivekgarg123'
	path = "/github-build/%s" % branch 
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, username = username, password = password)
	#print path
	stdin, stdout, stderr = client.exec_command('ls %s -ltrh| grep LATEST' %(path))
	a = stdout.readlines()
	print a
	client.close()
	b = a[0].split('->')
	latest_build = b[1].strip(' ')
	latest_build = latest_build.strip('\n')
	return latest_build
	

def get_build_date_from_jenkins_server(branch='', build='', openstack_version=''):
	host = '10.84.24.64'
	username = 'root'
	password = 'c0ntrail123'
	path = '/cs-build/'
	if branch == 'R3.2':
		print 'I am in R3.2 branch'
		print openstack_version
		if openstack_version == 'mitaka':
			path = path + 'CB-R3.2-ubuntu14-mitaka/builds/%s' %build
		elif openstack_version == 'kilo':
			path = path + 'CB-R3.2-ubuntu14-kilo/builds/%s' %build
		elif openstack_version == 'liberty':
			path = path + 'CB-R3.2-ubuntu14-liberty/builds/%s' %build
	elif branch == 'R4.0':
		print 'I am in R4.0 branch'
		print openstack_version
		if openstack_version == 'mitaka':
			path = path + 'CB-R4.0-ubuntu14-mitaka/builds/%s' %build
		elif openstack_version == 'newton':
			path = path + 'CB-R4.0-ubuntu16-newton/builds/%s' %build
	elif branch == 'mainline':
		print 'I am in mainline branch'
		print openstack_version
		if openstack_version == 'mitaka':
			path = path + 'CB-mainline-ubuntu14-mitaka/builds/%s' %build
		elif openstack_version == 'newton':
			path = path + 'CB-mainline-ubuntu16-newton/builds/%s' %build
	print path
	if (int(build) <= 0):
		return "Build Not Found"
	else:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(host, username = username, password = password)
		cmd='stat %s  | grep Change | cut -d" " -f2' %(path)
		print cmd
		#stdin, stdout, stderr = client.exec_command('stat %s/%s  | grep Change | cut -d" " -f2' %(path, build))
		stdin, stdout, stderr = client.exec_command(cmd)
		a = stdout.readlines()
		print a
		b=a[0].replace('\n', '')
		client.close()
		print b
		return b

def get_build_date(branch='', build=''):
        branch= branch
        build = build
        host = '10.84.5.31'
        username = 'vivekgarg'
        password = 'vivekgarg123'
        ini_list = []
        err_list = []
        path = "/github-build/"
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username = username, password = password)
        stdin, stdout, stderr = client.exec_command('ls %s | grep %s' %(path, branch))
        a = stdout.readlines()
        for i in a:
                b = i.replace('\n', '')
                ini_list.append(b)
        #err_list = stderr.readlines()
        client.close()
        if (len(ini_list) == 1):
                path = path + ini_list[0] + '/'
                #print path
        if (len(ini_list) > 1):
                for j in ini_list:
                        if j == branch:
                                path = path + j + '/'
                                #print path
        else:
                return None
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username = username, password = password)
        cmd='stat %s%s  | grep Change | cut -d" " -f2' %(path, build)
        print cmd
        stdin, stdout, stderr = client.exec_command('stat %s/%s  | grep Change | cut -d" " -f2' %(path, build))
        a = stdout.readlines()
        b=a[0].replace('\n', '')
        client.close()
	print b
	return b
        #client.close()


def process_summary(summary=""):
        m = re.search('Success rate:(.*)%',summary)
        success_rate = float(m.group(1))
        if success_rate >= 85 :
 		return "PASS"
        else:
		return "FAIL"	
        


# Function to get the final dict for all the branchs
def get_all_branch_final_dict(build=''):
	info_dict_combined = {}
	#lets get data from R3.2 branch
	#int_build_number = build
	info_dict_combined['R3.2_data']={}
	int_build_number_mitaka = get_latest_build_number_individual(branch='R3.2', openstack_version = 'mitaka')
	int_build_number_kilo = get_latest_build_number_individual(branch='R3.2', openstack_version = 'kilo')
	int_build_number_liberty = get_latest_build_number_individual(branch='R3.2', openstack_version = 'liberty')
	for i in range(5):
		info_dict_combined['R3.2_data'].update(get_detailed_data_from_ini_files(branch='R3.2', build=int_build_number_mitaka, openstack_version='mitaka'))
		time.sleep(2)
		info_dict_combined['R3.2_data'].update(get_detailed_data_from_ini_files(branch='R3.2', build=int_build_number_kilo, openstack_version='kilo'))
		time.sleep(2)
		info_dict_combined['R3.2_data'].update(get_detailed_data_from_ini_files(branch='R3.2', build=int_build_number_liberty, openstack_version='liberty'))
		time.sleep(2)
		int_build_number_mitaka = str(int(int_build_number_mitaka)-1)
		int_build_number_kilo = str(int(int_build_number_kilo) -1)
		int_build_number_liberty = str(int(int_build_number_liberty) -1)
	# Lets get data from R4.0 branch
	#int_build_number = build
	info_dict_combined['R4.0_data']={}
	int_build_number_r4_mitaka = get_latest_build_number_individual(branch='R4.0', openstack_version = 'mitaka')
	int_build_number_r4_newton = get_latest_build_number_individual(branch='R4.0', openstack_version = 'newton')
	for i in range(5):
		#int_build_number = get_latest_build_number_individual(branch='R4.2', openstack_version = 'mitaka')
		info_dict_combined['R4.0_data'].update(get_detailed_data_from_ini_files(branch='R4.0', build=int_build_number_r4_mitaka, openstack_version='mitaka'))
		time.sleep(2)
		#int_build_number = get_latest_build_number_individual(branch='R4.0', openstack_version = 'newton')
		info_dict_combined['R4.0_data'].update(get_detailed_data_from_ini_files(branch='R4.0', build=int_build_number_r4_newton, openstack_version='newton'))
		time.sleep(2)
		#int_build_number = str(int(int_build_number)-1)
		int_build_number_r4_mitaka = str(int(int_build_number_r4_mitaka) - 1)
		int_build_number_r4_newton = str(int(int_build_number_r4_newton) - 1)
	# Now Lets get data from mainline branch 
	#int_build_number = build
	info_dict_combined['mainline_data']={}
	int_build_number_mainline_mitaka = get_latest_build_number_individual(branch='mainline', openstack_version = 'mitaka')
	int_build_number_mainline_newton = get_latest_build_number_individual(branch='mainline', openstack_version = 'newton')
	for i in range(5):
		#int_build_number = get_latest_build_number_individual(branch='mainline', openstack_version = 'mitaka')
		info_dict_combined['mainline_data'].update(get_detailed_data_from_ini_files(branch='mainline', build=int_build_number_mainline_mitaka, openstack_version='mitaka'))
		time.sleep(2)
		#int_build_number = get_latest_build_number_individual(branch='mainline', openstack_version = 'newton')
		info_dict_combined['mainline_data'].update(get_detailed_data_from_ini_files(branch='mainline', build=int_build_number_mainline_newton, openstack_version='newton'))
		time.sleep(2)
		#int_build_number = str(int(int_build_number)-1)
		int_build_number_mainline_mitaka = str(int(int_build_number_mainline_mitaka) - 1)
		int_build_number_mainline_newton = str(int(int_build_number_mainline_newton) - 1)

	with open('result.json', 'w') as fp:
		json.dump(info_dict_combined, fp)
	print info_dict_combined
	return info_dict_combined


def get_specific_branch_final_dict(branch='', build=''):
	info_dict_combined = {}
	int_build_number = build
	if branch == 'R3.2':
		info_dict_combined['R3.2_data']={}
		info_dict_combined['R3.2_data']['mitaka']={}
		info_dict_combined['R3.2_data']['kilo']={}
		info_dict_combined['R3.2_data']['liberty']={}
		for i in range(5):
			info_dict_combined['R3.2_data']['mitaka'].update(get_detailed_data_from_ini_files(branch='R3.2', build=int_build_number, openstack_version='mitaka'))
			#info_dict_combined['R3.2_data']['kilo'].update(get_detailed_data_from_ini_files(branch='R3.2', build=int_build_number, openstack_version='kilo'))
			#info_dict_combined['R3.2_data']['liberty'].update(get_detailed_data_from_ini_files(branch='R3.2', build=int_build_number, openstack_version='liberty'))
			int_build_number = str(int(int_build_number)-1)
	elif branch == 'R4.0':
		info_dict_combined['R4.0_data']={}
		#print info_dict_combined
                #info_dict_combined['R4.0_data']['mitaka']={}
		#print info_dict_combined
                #info_dict_combined['R4.0_data']['newton']={}
		print info_dict_combined
		for i in range(5):
			info_dict_combined['R4.0_data'].update(get_detailed_data_from_ini_files(branch='R4.0', build=int_build_number, openstack_version='mitaka'))
			info_dict_combined['R4.0_data'].update(get_detailed_data_from_ini_files(branch='R4.0', build=int_build_number, openstack_version='newton'))
			int_build_number = str(int(int_build_number)-1)
	elif branch == 'mainline':
		for i in range (5):
			info_dict_combined['mainline_data']['mitaka'].update(get_detailed_data_from_ini_files(branch='mainline', build=int_build_number, openstack_version='mitaka'))
			info_dict_combined['mainline_data']['newton'].update(get_detailed_data_from_ini_files(branch='mainline', build=int_build_number, openstack_version='newton'))
			int_build_number = str(int(int_build_number)-1)
	with open('result.json', 'w') as fp:
		json.dump(info_dict_combined, fp)
	#print info_dict_combined
	return info_dict_combined


#def get_latest_build_number_individual(branch=''):
	

def build_final_json(dict_1):
	print dict_1
	final_info_dict ={}
	final_info_dict['Sanity']={}
	final_job_list = []
	# Lets get the R3.2 branch data for the final json
	for i in dict_1['R3.2_data']['jobs']:
		#print i
		individual_info_dict = {}
		if i == 'R3.2_mitaka':
			individual_info_dict['JobName'] = 'R3.2-Mitaka'
			Ostack_ver = 'mitaka'
		elif i == 'R3.2_kilo':
			individual_info_dict['JobName'] = 'R3.2-Kilo'
			Ostack_ver = 'kilo'
		elif i == 'R3.2_liberty':
			individual_info_dict['JobName'] = 'R3.2-Liberty'
			Ostack_ver = 'liberty'

		all_build_list = []
		last_good_build_info_dict = {'build_no': '', 'sanity_percentage': '', 'report_link': ''}
		build_no_for_computation_internal = get_latest_build_number_individual(branch='R3.2', openstack_version = Ostack_ver)
		#build_no_for_computation_internal = '27' # for testing purpose
		for j in range(5):
			branch = 'R3.2'
			if build_no_for_computation_internal in dict_1['R3.2_data']['jobs'][i]:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				indi_build_dict["Build date"] = get_build_date_from_jenkins_server(branch, indi_build_dict["Build number"], openstack_version = Ostack_ver)
				indi_build_dict["Report"] = dict_1['R3.2_data']['jobs'][i][build_no_for_computation_internal]['report']
				indi_build_dict["Total tests"] = dict_1['R3.2_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][0]
				indi_build_dict["Failures"] = dict_1['R3.2_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][1]
				indi_build_dict["Errors"] = dict_1['R3.2_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][2]
				indi_build_dict["Skipped"] = dict_1['R3.2_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][3]
				# Total Tests = Total Tests - Skipped Tests 
				temp_total = (int(indi_build_dict["Total tests"]) - int(indi_build_dict["Skipped"]))
				indi_build_dict["Total tests"] = str(temp_total)
				indi_build_dict["Success rate"] = dict_1['R3.2_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][4]
				indi_build_dict['status'] = 'complete'
				if Ostack_ver == 'mitaka':
					final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R3.2-ubuntu14-mitaka/builds/%s/archive/packages/' % indi_build_dict["Build number"]
				elif Ostack_ver == 'kilo':
					final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R3.2-ubuntu14-kilo/builds/%s/archive/packages/' % indi_build_dict["Build number"]
				elif Ostack_ver == 'liberty':
					final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R3.2-ubuntu14-liberty/builds/%s/archive/packages/' % indi_build_dict["Build number"]
				indi_build_dict['BuildLink'] = final_build_path
				# Lets get the data about the last good sanity with respect to the success percent
				if last_good_build_info_dict['build_no'] == '':
					success_percent_str = indi_build_dict["Success rate"]
					success_percent_str_list = success_percent_str.split('%')
					success_percent = float(success_percent_str_list[0])
					if success_percent == 100 :
						last_good_build_info_dict['lastGoddBuildLink'] = indi_build_dict["BuildLink"]
						last_good_build_info_dict['build_no'] = indi_build_dict["Build number"]
						last_good_build_info_dict['sanity_percentage'] = indi_build_dict["Success rate"]
						last_good_build_info_dict['report_link'] = indi_build_dict["Report"]
				# Lets Put this created dict in the list that contains all the dicts of the summary of the build
				all_build_list.append(indi_build_dict)

			else:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				indi_build_dict["Build date"] = get_build_date_from_jenkins_server(branch, indi_build_dict["Build number"], openstack_version = Ostack_ver)
				indi_build_dict["Report"] = 'Test Did Not Run'
				indi_build_dict["Total tests"] = '0'
				indi_build_dict["Failures"] = '0'
				indi_build_dict["Errors"] = '0'
				indi_build_dict["Skipped"] = '0'
				indi_build_dict["Success rate"] = '0%'
				indi_build_dict['status'] = 'incomplete'
				if Ostack_ver == 'mitaka':
                                        final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R3.2-ubuntu14-mitaka/builds/%s/archive/packages/' % indi_build_dict["Build number"]
                                elif Ostack_ver == 'kilo':
                                        final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R3.2-ubuntu14-kilo/builds/%s/archive/packages/' % indi_build_dict["Build number"]
                                elif Ostack_ver == 'liberty':
                                        final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R3.2-ubuntu14-liberty/builds/%s/archive/packages/' % indi_build_dict["Build number"]
                                indi_build_dict['BuildLink'] = final_build_path
				all_build_list.append(indi_build_dict)

			build_no_for_computation_internal = str(int(build_no_for_computation_internal) - 1)
		individual_info_dict['Last good build'] = last_good_build_info_dict['build_no']
		individual_info_dict['Last good sanity'] = last_good_build_info_dict['sanity_percentage']
		individual_info_dict['Last good sanity link'] = last_good_build_info_dict['report_link']
		individual_info_dict['Builds'] = all_build_list
		final_job_list.append(individual_info_dict)

	# Lets get the R4.0 branch data for the final json
	for i in dict_1['R4.0_data']['jobs']:
		#print i
		individual_info_dict = {}
		if i == 'R4.0_mitaka':
			individual_info_dict['JobName'] = 'R4.0-Mitaka'
			Ostack_ver = 'mitaka'
		elif i == 'R4.0_newton':
			individual_info_dict['JobName'] = 'R4.0-Newton'
			Ostack_ver = 'newton'

		all_build_list = []
		last_good_build_info_dict = {'build_no': '', 'sanity_percentage': '', 'report_link': ''}
		build_no_for_computation_internal = get_latest_build_number_individual(branch='R4.0', openstack_version = Ostack_ver)
		#build_no_for_computation_internal = '27'
		for j in range(5):
			branch = 'R4.0'
			if build_no_for_computation_internal in dict_1['R4.0_data']['jobs'][i]:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				print "Error will occur after this "
				indi_build_dict["Build date"] = get_build_date_from_jenkins_server(branch, indi_build_dict["Build number"], openstack_version = Ostack_ver)
				indi_build_dict["Report"] = dict_1['R4.0_data']['jobs'][i][build_no_for_computation_internal]['report']
				indi_build_dict["Total tests"] = dict_1['R4.0_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][0]
				indi_build_dict["Failures"] = dict_1['R4.0_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][1]
				indi_build_dict["Errors"] = dict_1['R4.0_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][2]
				indi_build_dict["Skipped"] = dict_1['R4.0_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][3]
				indi_build_dict["Success rate"] = dict_1['R4.0_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][4]
				indi_build_dict['status'] = 'complete'
                                temp_total = (int(indi_build_dict["Total tests"]) - int(indi_build_dict["Skipped"]))
                                indi_build_dict["Total tests"] = str(temp_total)
				if Ostack_ver == 'mitaka':
					final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R4.0-ubuntu14-mitaka/builds/%s/archive/packages/' % indi_build_dict["Build number"]
				elif Ostack_ver == 'newton':
					final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R4.0-ubuntu16-newton/builds/%s/archive/packages/' % indi_build_dict["Build number"]
				indi_build_dict['BuildLink'] = final_build_path	

				# Lets get the data about the last good sanity with respect to the success percent
				if last_good_build_info_dict['build_no'] == '':
					success_percent_str = indi_build_dict["Success rate"]
					success_percent_str_list = success_percent_str.split('%')
					success_percent = float(success_percent_str_list[0])
					if success_percent == 100 :
						last_good_build_info_dict['lastGoddBuildLink'] = indi_build_dict['BuildLink']
						last_good_build_info_dict['build_no'] = indi_build_dict["Build number"]
						last_good_build_info_dict['sanity_percentage'] = indi_build_dict["Success rate"]
						last_good_build_info_dict['report_link'] = indi_build_dict["Report"]
				# Lets Put this created dict in the list that contains all the dicts of the summary of the build
				all_build_list.append(indi_build_dict)

			else:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				indi_build_dict["Build date"] = get_build_date_from_jenkins_server(branch, indi_build_dict["Build number"], openstack_version = Ostack_ver)
				indi_build_dict["Report"] = 'Test Did Not Run'
				indi_build_dict["Total tests"] = '0'
				indi_build_dict["Failures"] = '0'
				indi_build_dict["Errors"] = '0'
				indi_build_dict["Skipped"] = '0'
				indi_build_dict["Success rate"] = '0%'
				indi_build_dict['status'] = 'incomplete'
				if Ostack_ver == 'mitaka':
                                        final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R4.0-ubuntu14-mitaka/builds/%s/archive/packages/' % indi_build_dict["Build number"]
                                elif Ostack_ver == 'newton':
                                        final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-R4.0-ubuntu16-newton/builds/%s/archive/packages/' % indi_build_dict["Build number"]
                                indi_build_dict['BuildLink'] = final_build_path
				all_build_list.append(indi_build_dict)

			build_no_for_computation_internal = str(int(build_no_for_computation_internal) - 1)
		individual_info_dict['Last good build'] = last_good_build_info_dict['build_no']
		individual_info_dict['Last good sanity'] = last_good_build_info_dict['sanity_percentage']
		individual_info_dict['Last good sanity link'] = last_good_build_info_dict['report_link']
		individual_info_dict['Builds'] = all_build_list
		final_job_list.append(individual_info_dict)			

	# Lets get the mainline branch data for the final json
	for i in dict_1['mainline_data']['jobs']:
		#print i
		individual_info_dict = {}
		if i == 'mainline_mitaka':
			individual_info_dict['JobName'] = 'R4.1-Mitaka'
			Ostack_ver = 'mitaka'
		elif i == 'mainline_newton':
			individual_info_dict['JobName'] = 'R4.1-Newton'
			Ostack_ver = 'newton'

		all_build_list = []
		last_good_build_info_dict = {'build_no': '', 'sanity_percentage': '', 'report_link': ''}
		build_no_for_computation_internal = get_latest_build_number_individual(branch='mainline', openstack_version = Ostack_ver)
		#build_no_for_computation_internal = '27'
		for j in range(5):
			branch = 'mainline'
			if build_no_for_computation_internal in dict_1['mainline_data']['jobs'][i]:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				indi_build_dict["Build date"] = get_build_date_from_jenkins_server(branch, indi_build_dict["Build number"], openstack_version = Ostack_ver)
				indi_build_dict["Report"] = dict_1['mainline_data']['jobs'][i][build_no_for_computation_internal]['report']
				indi_build_dict["Total tests"] = dict_1['mainline_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][0]
				indi_build_dict["Failures"] = dict_1['mainline_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][1]
				indi_build_dict["Errors"] = dict_1['mainline_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][2]
				indi_build_dict["Skipped"] = dict_1['mainline_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][3]
				indi_build_dict["Success rate"] = dict_1['mainline_data']['jobs'][i][build_no_for_computation_internal]["testcase_results"]["values"][4]
				indi_build_dict['status'] = 'complete'
                                temp_total = (int(indi_build_dict["Total tests"]) - int(indi_build_dict["Skipped"]))
                                indi_build_dict["Total tests"] = str(temp_total)
				if Ostack_ver == 'mitaka':
					final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-mainline-ubuntu14-mitaka/builds/%s/archive/packages/' % indi_build_dict["Build number"]
				elif Ostack_ver == 'newton':
					final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-mainline-ubuntu16-newton/builds/%s/archive/packages/' % indi_build_dict["Build number"]
				indi_build_dict['BuildLink'] = final_build_path
	
				# Lets get the data about the last good sanity with respect to the success percent
				if last_good_build_info_dict['build_no'] == '':
					success_percent_str = indi_build_dict["Success rate"]
					success_percent_str_list = success_percent_str.split('%')
					success_percent = float(success_percent_str_list[0])
					if success_percent == 100 :
						last_good_build_info_dict['lastGoddBuildLink'] = indi_build_dict['BuildLink']
						last_good_build_info_dict['build_no'] = indi_build_dict["Build number"]
						last_good_build_info_dict['sanity_percentage'] = indi_build_dict["Success rate"]
						last_good_build_info_dict['report_link'] = indi_build_dict["Report"]
				# Lets Put this created dict in the list that contains all the dicts of the summary of the build
				all_build_list.append(indi_build_dict)

			else:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				indi_build_dict["Build date"] = get_build_date_from_jenkins_server(branch, indi_build_dict["Build number"], openstack_version = Ostack_ver)
				indi_build_dict["Report"] = 'Test Did Not Run'
				indi_build_dict["Total tests"] = '0'
				indi_build_dict["Failures"] = '0'
				indi_build_dict["Errors"] = '0'
				indi_build_dict["Skipped"] = '0'
				indi_build_dict["Success rate"] = '0%'
				indi_build_dict['status'] = 'incomplete'
				if Ostack_ver == 'mitaka':
                                        final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-mainline-ubuntu14-mitaka/builds/%s/archive/packages/' % indi_build_dict["Build number"]
                                elif Ostack_ver == 'newton':
                                        final_build_path = 'http://10.84.5.120/cs-build/jenkins-jobs/CB-mainline-ubuntu16-newton/builds/%s/archive/packages/' % indi_build_dict["Build number"]
                                indi_build_dict['BuildLink'] = final_build_path
				all_build_list.append(indi_build_dict)

			build_no_for_computation_internal = str(int(build_no_for_computation_internal) - 1)
		individual_info_dict['Last good build'] = last_good_build_info_dict['build_no']
		individual_info_dict['Last good sanity'] = last_good_build_info_dict['sanity_percentage']
		individual_info_dict['Last good sanity link'] = last_good_build_info_dict['report_link']
		individual_info_dict['Builds'] = all_build_list
		final_job_list.append(individual_info_dict)	
	
	# Lets put the list of all the jobs in final_info_dict['sanity']['jobs']
	final_info_dict["Sanity"]["Job"] = final_job_list
	
	#creating the static bug config
	demo_bug_list = [{"Bug id":"1234567", "Description": "This is a bug", "Link": "http://launchpad.net/juniperopenstack/+bug/1234567", "Assignee": "Soumil"}, {"Bug id":"1234563", "Description": "This is a bug", "Link": "http://launchpad.net/juniperopenstack/+bug/1234563", "Assignee": "Jeba"}]
	final_info_dict["Sanity"]["Bugs"] = demo_bug_list
        # Lets create the final json file that will be used to create the web page
        pprint_final_info_dict = json.dumps(final_info_dict, indent=4)
        fp = open('final_result.json', 'w')
        print >> fp, pprint_final_info_dict
        fp.close()





def get_final_dict(branch= '', build= ''):
	if branch == "all":
		dict_to_build_final_json = get_all_branch_final_dict(build=build)
		build_final_json(dict_to_build_final_json)
	else:
		print "Function not in use. Please put branch parameter to be equal to 'all'"
		dict_to_build_final_json = get_specific_branch_final_dict(branch=branch, build=build)
		build_final_json(dict_to_build_final_json)

	# make changes to the code from here
	# +++++++++++++
	"""
	build_no_for_computation = build
	#print build
        info_dict_combined = {}
        for i in range(5):
		print build
                info_dict_combined.update(get_detailed_data_from_ini_files(branch=branch, build=build))
                build = str(int(build) - 1)
        with open('result.json', 'w') as fp:
            json.dump(info_dict_combined, fp)
        print info_dict_combined
        # Now Lets create the final dict that will be used to create html file
        final_info_dict = {}
        final_info_dict["Sanity"] = {}
        final_job_list = []
        for i in info_dict_combined:
                individual_info_dict = {}
                if i == "liberty_jobs":
                        individual_info_dict["JobName"] = "%s-Liberty" % branch
                if i == "kilo_jobs":
                        individual_info_dict["JobName"] = "%s-Kilo" % branch
                if i == "mitaka_jobs":
                        individual_info_dict["JobName"] = "%s-Mitaka" % branch

                all_build_list = []
		'''
                for j in info_dict_combined[i]:
                        indi_build_dict = {}
                        indi_build_dict["Build number"] = j
                        indi_build_dict["Report"] = info_dict_combined[i][j]["report"]
                        indi_build_dict["Total tests"] = info_dict_combined[i][j]["testcase_results"]["values"][0]
                        indi_build_dict["Failures"] = info_dict_combined[i][j]["testcase_results"]["values"][1]
                        indi_build_dict["Errors"] = info_dict_combined[i][j]["testcase_results"]["values"][2]
                        indi_build_dict["Skipped"] = info_dict_combined[i][j]["testcase_results"]["values"][3]
                        indi_build_dict["Success rate"] = info_dict_combined[i][j]["testcase_results"]["values"][4]
                        # Lets Put this created dict in the list that contains all the dicts of the summary of the build
                        all_build_list.append(indi_build_dict)
		
                #Now see if all the data from all the  last 5 builds is present in the list
		'''
		last_good_build_info_dict = {'build_no': '', 'sanity_percentage': '', 'report_link': ''}
		build_no_for_computation_internal = build_no_for_computation
		for j in range (5):
			if build_no_for_computation_internal in info_dict_combined[i]:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				indi_build_dict["Build date"] = get_build_date(branch, indi_build_dict["Build number"])
				indi_build_dict["Report"] = info_dict_combined[i][build_no_for_computation_internal]["report"]
				indi_build_dict["Total tests"] = info_dict_combined[i][build_no_for_computation_internal]["testcase_results"]["values"][0]
				indi_build_dict["Failures"] = info_dict_combined[i][build_no_for_computation_internal]["testcase_results"]["values"][1]
				indi_build_dict["Errors"] = info_dict_combined[i][build_no_for_computation_internal]["testcase_results"]["values"][2]
				indi_build_dict["Skipped"] = info_dict_combined[i][build_no_for_computation_internal]["testcase_results"]["values"][3]
				indi_build_dict["Success rate"] = info_dict_combined[i][build_no_for_computation_internal]["testcase_results"]["values"][4]
			
				# Lets get the data about the last good sanity with respect to the success percent
				if last_good_build_info_dict['build_no'] == '':
					success_percent_str = indi_build_dict["Success rate"]
					success_percent_str_list = success_percent_str.split('%')
					success_percent = float(success_percent_str_list[0])
					if success_percent > 80 :
						last_good_build_info_dict['build_no'] = indi_build_dict["Build number"]
						last_good_build_info_dict['sanity_percentage'] = indi_build_dict["Success rate"]
						last_good_build_info_dict['report_link'] = indi_build_dict["Report"]	
				# Lets Put this created dict in the list that contains all the dicts of the summary of the build
				all_build_list.append(indi_build_dict)

			else:
				indi_build_dict = {}
				indi_build_dict["Build number"] = build_no_for_computation_internal
				indi_build_dict["Build date"] = get_build_date(branch, indi_build_dict["Build number"])
				indi_build_dict["Report"] = "Test Did Not Run"
				indi_build_dict["Total tests"] = '0'
				indi_build_dict["Failures"] = '0'
				indi_build_dict["Errors"] = '0'
				indi_build_dict["Skipped"] = '0'
				indi_build_dict["Success rate"] = '0%'
				all_build_list.append(indi_build_dict)
	
			build_no_for_computation_internal = str(int(build_no_for_computation_internal) - 1)
		
		# Now lets put the above generated data about the last good sanity run in the dict		
		individual_info_dict['Last good build'] = last_good_build_info_dict['build_no']
		individual_info_dict['Last good sanity'] = last_good_build_info_dict['sanity_percentage']
		individual_info_dict['Last good sanity link'] = last_good_build_info_dict['report_link']

                individual_info_dict["Builds"] = all_build_list

                final_job_list.append(individual_info_dict)

        final_info_dict["Sanity"]["Job"] = final_job_list

	demo_bug_list = [{"Bug id":"1234567", "Description": "This is a bug", "Link": "http://launchpad.net/juniperopenstack/+bug/1234567", "Assignee": "Soumil"}, {"Bug id":"1234563", "Description": "This is a bug", "Link": "http://launchpad.net/juniperopenstack/+bug/1234563", "Assignee": "Jeba"}]
	
	final_info_dict["Sanity"]["Bugs"] = demo_bug_list
	# Lets create the final json file that will be used to create the web page
        pprint_final_info_dict = json.dumps(final_info_dict, indent=4)
        fp = open('final_result.json', 'w')
        print >> fp, pprint_final_info_dict
        fp.close()
	"""

def get_html_file(dest_file="", branch='', build=''):
        info_dict_combined = {}
        for i in range(5):
	    info_dict_combined.update(get_detailed_data_from_ini_files(branch=branch, build=build))
        #    if info_dict_combined[build]:
        #        info_dict_combined[build][0]["date"]=get_build_date(branch, build)
            build = str(int(build) - 1)
 
        print_xml_file(info_dict_combined)
	html_string = '''
	<!DOCTYPE html>
	<html>
	<head>
	<title> TEST SUMMARY GATHERING TOOL </title>
	</head>
	<body>
	<h1>Daily Sanity Report Summary</h1>
	<style>
		table {
		    font-family: arial, sans-serif;
		    border-collapse: collapse;
		    width: 100%;
		}

		td, th {
		    border: 1px solid #dddddd;
		    text-align: left;
		    padding: 8px;
		}

		tr:nth-child(even) {
		    background-color: #dddddd;
		}
	</style>
	<table>
		<tr>
			<th> DISTRO </th>
			<th> BUILD </th>
			<th> REPORT LINK </th>
			<th> TOPOLOGY </th>
			<th> TEST SUMMARY </th>
			<th> STATUS </th>
		</tr>\n
	'''
	for key in info_dict_combined:
	    for i in info_dict_combined[key]:
             # if re.match(".*jenkins-ubuntu-14-04*",info_dict_combined[key][i]["report"]):
		html_string = html_string + '''
		<tr>
			<th> %s </th>
			<th> %s </th>
			<th> <a href="%s"> click here </th>
			<th> %s </th>
		''' % (info_dict_combined[key][i]["distro"], info_dict_combined[key][i]["build"], info_dict_combined[key][i]["report"], info_dict_combined[key][i]['topo_summary'])
		summ = ''
		test_result_dict_lables = info_dict_combined[key][i]["testcase_results"]["labels"]
		test_result_dict_values = info_dict_combined[key][i]["testcase_results"]["values"]
		num = len(test_result_dict_values)
		itr = 0 
		while (itr < num):
			summ = summ + " %s:%s " % (test_result_dict_lables[itr], test_result_dict_values[itr])
			itr += 1 
		html_string = html_string + '''
			<th> %s </th>
		''' % summ
                status = process_summary(summ)
                if status == 'PASS':
			html_string = html_string + '''
				<th bgcolor="#4DE343"> %s </th>
			</tr> 
			''' % status
		else:
			html_string = html_string + '''
				<th bgcolor="#F8510D"> %s </th>
			</tr> 
			''' % status
	      #else:
	#	continue
	html_string = html_string + """
	</table>
	</body>
	</html>
	"""
	#print html_string
	#print dest_file
	if dest_file == None:
		f = open('result_summary.html', 'w')
		f.write(html_string)
		f.close()
	else:
		f = open(dest_file, 'w')
		f.write(html_string)
		f.close()

def main():
	parser = OptionParser()
	parser.add_option('-d','--dest_file_name', help="Give a name to the destination html file", type="string", dest='dest_file_name')
	parser.add_option('--branch', help="Branch Name", type="string", dest="branch")
	parser.add_option('--build', help="Build Number", type="string", dest="build")
	parser.add_option('-o', '--output_format', help="Print output / get html file (print/html)", type="string", dest="out_format")
	#parser.add_option('-h', '--help', help='python sanity_summary.py --dest_file_name <output file name> --branch <Branch Name> --build <Build Number> --output_format <print / html>')
	(opts, args) = parser.parse_args()
	#print opts
	if opts.out_format == "print":
		print_report_summary(branch=opts.branch, build=opts.build)
	elif opts.out_format == "html":
		if opts.branch == "all":
			if opts.build == "latest":
				#latest_build = get_latest_build_number(opts.branch) 
				get_final_dict(branch=opts.branch, build=opts.build)
			else:
				#get_html_file(dest_file=opts.dest_file_name, branch=opts.branch, build=opts.build)
				get_final_dict(branch=opts.branch, build=opts.build)
		else:
			if opts.build == "latest":
				#latest_build = get_latest_build_number(opts.branch)
				get_final_dict(branch=opts.branch, build=opts.build)
			else:
				get_final_dict(branch=opts.branch, build=opts.build)
	else:
		print " Wrong Option Selected. Please select 'print/html'"

	#get_html_file(dest_file=opts.dest_file_name)



main()
