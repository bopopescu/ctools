"""
Author: Soumil Kulkarni
Name: Performance_test_result_analyzing_tool
Usage: python performance_analysis_tool.py --file <Input (.csv) file> --output_file <output html file> --job <job to run >
       jobs can be one pf these: time_throughput / time_vs_conn_rate_flow_tests / time_vs_conn_rate_flow_scale_tests

"""
import sys
import csv
import matplotlib.pyplot as plt
import copy
import numpy
from optparse import OptionParser

time_list = []
established_tcp_conn_per_sec = []
min_tcp_syn_ack_list = []
max_tcp_syn_ack_list = []
avg_tcp_syn_ack_list = []
concurrent_tcp_connections_list = []
throughput_list = []
throughput_response_list = []


def get_list_of_elapsed_time(inp_file = ''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
        if len(line) <= 0:
            continue
        else:
            if itr == 1:
                time_list.append(float(line[0]))
            if itr == 0:
                if line[0] == 'Seconds Elapsed':
                    itr = 1
    # print time_list


def get_list_of_number_of_TCP_conn_per_sec(inp_file =''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
        if len(line) <= 136:
            continue
        else:
            if itr == 1:
                established_tcp_conn_per_sec.append(float(line[136]))
            if itr == 0:
                if line[136] == 'Established TCP Connection Rate (Connections/sec)':
                    itr = 1
    # print established_tcp_conn_per_sec


def get_throughput(inp_file=''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
        if len(line) <= 18:
            continue
        else:
            #print line[18]
            if itr == 1:
                throughput_list.append(float(line[18]))
            if itr == 0:
                if line[18] == 'Incoming Traffic (Kbps)':
                    itr = 1
    #`print throughput_list

def get_throughput_response(inp_file= ''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
        if len(line) <= 255:
            continue
        else:
            #print line[255]
            if itr == 1:
                throughput_response_list.append(float(line[255]))
            if itr == 0:
                if line[255] == 'Average Response Time Per URL (msec)':
                    itr = 1
    #print throughput_response_list    

def get_list_of_min_time_to_tcp_syn_ack(inp_file=''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
    	if len(line) <= 137:
    		continue
    	else:
	    	#print line
	        if itr == 1:
	            #print line[0]
	            min_tcp_syn_ack_list.append(float(line[137]))
	        if itr == 0:
	            #print line[137]
	            if line[137] == 'Minimum Time to TCP SYN/ACK (msec)':
	            	itr = 1
    #print min_tcp_syn_ack_list


def get_list_of_max_time_to_tcp_syn_ack(inp_file=''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
    	if len(line) <= 138:
    		continue
    	else:
	        if itr == 1:
	            max_tcp_syn_ack_list.append(float(line[138]))
	        if itr == 0:
	            if line[138] == 'Maximum Time to TCP SYN/ACK (msec)':
	                itr = 1
    #print max_tcp_syn_ack_list


def get_list_of_avg_time_to_tcp_syn_ack(inp_file=''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
        if len(line) <= 139:
            continue
        else:
            if itr == 1:
                avg_tcp_syn_ack_list.append(float(line[139]))
            if itr == 0:
                if line[139] == 'Average Time to TCP SYN/ACK (msec)':
                    itr = 1
    # print avg_tcp_syn_ack_list


def get_list_of_concurrent_tcp_connections(inp_file=''):
    #file = open('/Users/soumilk/Downloads/realtime.csv')
    #file = open(sys.argv[1])
    file = open(inp_file)
    data = csv.reader(file)
    itr = 0
    for line in data:
        if len(line) <= 135:
            continue
        else:
        	#print line[135]
        	if itr == 1:
        		concurrent_tcp_connections_list.append(float(line[135]))
        	if itr == 0:
        		if line[135] == 'Current Established TCP Connections':
        			itr = 1
    #print concurrent_tcp_connections_list

def plot_graph(*argv):
    if len(argv) == 3:
        #print "hey"
        x_axis = argv[0]
        y_1_axis = argv[1]
        y_2_axis = argv[2]
        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx()
        ax1.plot(x_axis, y_1_axis, 'g')
        ax2.plot(x_axis, y_2_axis, 'b', linewidth=2)

        ax1.set_xlabel('Elapsed Time')
        ax1.set_ylabel('Established TCP Connections per second', color = 'g')
        ax2.set_ylabel('Average Time per TCP SYN/ACK', color = 'b')
        plt.grid()
        #plt.savefig('/Users/soumilk/Downloads/soumil.png')
        plt.savefig('test.png')
        #plt.show()
    elif len(argv) == 4:
        if argv[0] == 'throughput':
            x_axis = argv[1]
            y_1_axis = argv[2]
            y_2_axis = argv[3]
            fig, ax1 = plt.subplots()

            ax2 = ax1.twinx()
            ax1.plot(x_axis, y_1_axis, 'g')
            ax2.plot(x_axis, y_2_axis, 'b', linewidth=2)
            #ax2.yticks(numpy.arrange(min(y_2_axis), max(y_2_axis)+1, 100))

            ax1.set_xlabel('Elapsed Time')
            ax1.set_ylabel('Incoming Traffic (Kbps)', color = 'g')
            ax2.set_ylabel('Average Response Time Per URL (msec)', color = 'b')
            plt.grid()
            #plt.savefig('/Users/soumilk/Downloads/soumil.png')
            plt.savefig('test.png')
            #plt.show()
        else:
            #print "hey"
            x_axis = argv[0]
            y_1_axis = argv[1]
            y_2_axis = argv[2]
            y_3_axis = argv[3]
            fig, ax1 = plt.subplots(2, sharex=True)

            ax2 = ax1[0].twinx()
            ax1[0].plot(x_axis, y_3_axis, 'g')
            ax2.plot(x_axis, y_2_axis, 'b', linewidth=2)
            ax1[1].plot(x_axis, y_1_axis,'r')

            ax1[0].set_xlabel('Elapsed Time')
            ax1[1].set_xlabel('Elapsed Time')
            ax1[1].set_ylabel('Established TCP Conn/sec', color = 'r')
            ax1[0].set_ylabel('Concurrent tcp Conn/sec', color = 'g')
            ax2.set_ylabel('Average Time per TCP SYN/ACK', color = 'b')
            plt.grid()
            #plt.savefig('/Users/soumilk/Downloads/soumil.png')
            plt.savefig('test.png')
            #plt.show()

def get_diff(list_1, list2):
    diff_list = []
    len_list = len(list_1)
    for i in range(len(list_1) - 1):
        diff_list.append(format(float(list_1[i + 1] - list_1[i]), '.2f'))
    print diff_list
    # print len(list_1)
    # print len(diff_list)
    # for num in diff_list:
    ind = diff_list.index('1')
    print "Number of established TCP Connection before the avalanch effect: %f" % list2[ind]
    print "Avg time for TCP SYN/ACK before avalanch effect: %f" % list_1[ind]

def get_std(list_1):
    std = numpy.std(list_1)
    return std

def get_median(list_1):
    med = numpy.median(list_1)
    return med

def create_html_file(dict1):
    # print dict1
    html_string = '''
	<!DOCTYPE html>
	<html>
	<head>
	<title> Performance Tests Results </title>
	</head>
	<body>
    \n'''
    if "title" in dict1:
        html_string = html_string + "<h1>%s</h1>\n" % dict1["title"]
    if "final_elapsed_time" in dict1:
        html_string = html_string + "<p>Elapsed Time at Final Point: %s sec</p>\n" % dict1["final_elapsed_time"]
    if "establised_tcp_connections" in dict1:
        html_string = html_string + "<p>Establised TCP Connections at the final point: %s</p>\n" % dict1["establised_tcp_connections"]
    if "avg_time_for_tcp_syn_ack" in dict1:
        html_string = html_string + "<p>Average Time for TCP SYN/ACK at the final point: %s msec</p>\n" % dict1["avg_time_for_tcp_syn_ack"]
    if "min_time_for_tcp_syn_ack" in dict1:
        html_string = html_string + "<p>Minimum Time : %s</p>\n" % dict1["min_time_for_tcp_syn_ack"]
    if "max_time_for_tcp_syn_ack" in dict1:
        html_string = html_string + "<p>Maximum Time : %s</p>\n" % dict1["max_time_for_tcp_syn_ack"]
    if "final_incoming_traffic" in dict1:
        html_string = html_string + "<p>Final value of Incoming traffic: %s kbps</p>\n" % dict1["final_incoming_traffic"]
    if "final_throughput_response" in dict1:
        html_string = html_string + "<p>Final throughput response time: %s msec</p>\n" %dict1["final_throughput_response"]
    if "min_time_for_tcp_syn_ack" in dict1:
        html_string = html_string + "<p>Minimum Time: %s msce</p>\n" %dict1["min_time_for_tcp_syn_ack"]
    if "median_of_response_times" in dict1:
        html_string = html_string + "<p>The median of the response times: %s msec</p>\n" %dict1["median_of_response_times"]
    if "standard_deviation_of_response_times" in dict1:
        html_string = html_string + "<p>The Standard Deviation of the response times: %s msec</p>\n" %dict1["standard_deviation_of_response_times"]
    if "max_object_download_time" in dict1:
        html_string = html_string + "<p>Max Obejct Download Time in Throughput Test: %s msec</p>\n" %dict1["max_object_download_time"]
    if "graph_image_path" in dict1:
        html_string = html_string + '<img src="%s" alt="Could not find the graph image" width="800" height="500">\n' %dict1["graph_image_path"]
    """
    <h1>%s</h1>
	<p>Elapsed Time at the final Point : %s sec</p>
	<p>Established TCP Connections at final point: %s </p>
	<p>Average time for TCP Syn/Ack at that point: %s msec</p>
	<p>Minimum time for TCP Syn/Ack : %s</p>
	<p>Maximum time for TCP Syn/Ack : %s</p>
	<img src="%s" alt="Could not find the graph image" width="800" height="500">
	</body>
	</html>
	 % (dict1["title"], dict1["final_elapsed_time"], dict1["established_tcp_connections"], dict1["avg_time_for_tcp_syn_ack"], dict1["min_time_for_tcp_syn_ack"], dict1["max_time_for_tcp_syn_ack"], dict1["graph_image_path"])
    """
    #file = '%s' % dict1["destination_path_for_html_file"]
    if "out_file" in dict1:
        file = '%s' % dict1["out_file"]
    else:
        file = 'test.html'
    html_file = open(file, 'w')
    html_file.write(html_string)
    html_file.close()

"""
def time_vs_conn_rate_flow_tests():
    get_list_of_elapsed_time()
    get_list_of_number_of_TCP_conn_per_sec()
    get_list_of_avg_time_to_tcp_syn_ack()
    plot_graph(time_list, established_tcp_conn_per_sec, avg_tcp_syn_ack_list)
    # print established_tcp_conn_per_sec
    # print "_____________________"
    # print avg_tcp_syn_ack_list
    res_list = copy.deepcopy(avg_tcp_syn_ack_list)
    total_elements_in_list = len(res_list)
    # print total_elements_in_list
    posn = 0
    starting_pt = 0
    itr = 0
    while (itr < len(res_list)):
        if res_list[itr] <= 30:
            starting_pt = res_list[itr]
            # print starting_pt
            itr += 1
        else:
            posn = itr
            check = 0
            for i in range(20):
                if (res_list[posn] <= 30):
                    itr += 1
                    break
                else:
                    posn += 1
                    if (i == 19):
                        check = 1
            if check == 1:
                break
    # print starting_pt
    ind = avg_tcp_syn_ack_list.index(starting_pt)
    print "Elapsed Time at the final Point : %.2f sec" % time_list[ind]
    print "Established TCP Connections at final point: %.2f" % established_tcp_conn_per_sec[ind]
    print "Average time for TCP Syn/Ack at that point: %.2f" % avg_tcp_syn_ack_list[ind]
    web_page_dict = {
        'title': " Contrail Performance Flow ",
        "graph_image_path": "/Users/soumilk/Downloads/soumil.png",
        "destination_path_for_html_file": "/Users/soumilk/Desktop/code/Performance_Analysis_Tool/perf_flow.html",
        "final_elapsed_time": str(
            time_list[ind]),
        "established_tcp_connections": str(
            established_tcp_conn_per_sec[ind]),
        "avg_time_for_tcp_syn_ack": str(
            avg_tcp_syn_ack_list[ind])}
    create_html_file(web_page_dict)
    #get_diff(avg_tcp_syn_ack_list, established_tcp_conn_per_sec)
"""


def time_throughput(inp_file='', out_file=''):
    get_list_of_elapsed_time(inp_file= inp_file)
    get_throughput_response(inp_file = inp_file)
    get_throughput(inp_file=inp_file)
    plot_graph('throughput', time_list, throughput_list, throughput_response_list)
    #print throughput_list
    #print "---------"
    #print throughput_response_list
    res_list = copy.deepcopy(throughput_response_list)
    #print res_list
    total_elements_in_list = len(res_list)
    # print total_elements_in_list
    posn = 0
    starting_pt = 0
    itr = 0
    while (itr < len(res_list)):
        if res_list[itr] <= 6:
            starting_pt = res_list[itr]
            # print starting_pt
            itr += 1
        else:
            posn = itr
            check = 0
            for i in range(5):
                if (res_list[posn] <= 6):
                    itr += 1
                    break
                else:
                    posn += 1
                    if (i == 4):
                        check = 1
            if check == 1:
                break
    #print starting_pt
    ind = throughput_response_list.index(starting_pt)
    final_elapsed_time = time_list[ind]
    final_incoming_tafffic = throughput_list[ind]
    final_throughput_response  = throughput_response_list[ind]
    print "Elapsed Time at the final Point : %.2f sec" % final_elapsed_time
    print "Final Value of Incoming Traffic at the final point: %.2f kbps" % final_incoming_tafffic
    print "Final throughput Response at the final point: %.2f msec" % final_throughput_response
    max_object_download_time = max(throughput_response_list)
    print "Maximum Object Download Time in Throughput test: %.2f msec" % max_object_download_time
    web_page_dict = {
        'title': " Contrail Performance Throughput ",
        "graph_image_path": "/Users/soumilk/Downloads/soumil.png",
        "destination_path_for_html_file": "/Users/soumilk/Desktop/code/Performance_Analysis_Tool/throughput_flow.html",
        "final_elapsed_time": str(
            final_elapsed_time),
	"max_object_download_time": str(
	    max_object_download_time),
        "final_incoming_traffic": str(
            final_incoming_tafffic),
        "final_throughput_response": str(
            final_throughput_response)}
    if out_file != '':
        web_page_dict["out_file"] = out_file
    create_html_file(web_page_dict)


def time_vs_conn_rate_flow_tests(inp_file='', out_file=''):
    get_list_of_elapsed_time(inp_file=inp_file)
    get_list_of_number_of_TCP_conn_per_sec(inp_file=inp_file)
    get_list_of_avg_time_to_tcp_syn_ack(inp_file=inp_file)
    get_list_of_min_time_to_tcp_syn_ack(inp_file=inp_file)
    get_list_of_max_time_to_tcp_syn_ack(inp_file=inp_file)
    plot_graph(time_list, established_tcp_conn_per_sec, avg_tcp_syn_ack_list)
    # print established_tcp_conn_per_sec
    # print "_____________________"
    # print avg_tcp_syn_ack_list
    res_list = copy.deepcopy(avg_tcp_syn_ack_list)
    total_elements_in_list = len(res_list)
    # print total_elements_in_list
    posn = 0
    starting_pt = 0
    itr = 0
    while (itr < len(res_list)):
        if res_list[itr] <= 20:
            starting_pt = res_list[itr]
            # print starting_pt
            itr += 1
        else:
            posn = itr
            check = 0
            for i in range(20):
                if (res_list[posn] <= 20):
                    itr += 1
                    break
                else:
                    posn += 1
                    if (i == 19):
                        check = 1
            if check == 1:
                break
    # print starting_pt
    ind = avg_tcp_syn_ack_list.index(starting_pt)
    elap_time = time_list[ind]
    establish_tcp_conn = established_tcp_conn_per_sec[ind]
    avg_time_syn_ack = avg_tcp_syn_ack_list[ind]
    new_establish_tcp_conn = establish_tcp_conn * .90
    check_if_present = 0
    if new_establish_tcp_conn in established_tcp_conn_per_sec:
    	check_if_present = 1
    	final_established_tcp_conn_per_sec = new_establish_tcp_conn
    #print establish_tcp_conn
    #print new_establish_tcp_conn 
    if check_if_present == 0:
    	stack_list = []
    	for i in established_tcp_conn_per_sec:
    		if i == establish_tcp_conn:
    			stack_list.insert(0,i)
    			break
    		else:
    			stack_list.insert(0, i)
    	#print stack_list
    	check_pt = 0
    	while(check_pt != 1):
    		if ((new_establish_tcp_conn - stack_list[0]) <= 0):
    			stack_list.pop(0)
    		else:
				final_established_tcp_conn_per_sec = stack_list[0]
				check_pt = 1    			
    	#final_established_tcp_conn_per_sec = min(established_tcp_conn_per_sec, key=lambda x:abs(x - new_establish_tcp_conn))
    	#print final_established_tcp_conn_per_sec
    final_index = established_tcp_conn_per_sec.index(final_established_tcp_conn_per_sec)
    final_elapsed_time = time_list[final_index]
    count = 0 
    sum_of_avgs = 0
    list_for_calculating_std = []
    list_for_calculating_min = []
    list_for_calculating_max = []
    while(count != final_index):
        list_for_calculating_std.append(avg_tcp_syn_ack_list[count])
        list_for_calculating_min.append(min_tcp_syn_ack_list[count])
        list_for_calculating_max.append(max_tcp_syn_ack_list[count])
    	sum_of_avgs += avg_tcp_syn_ack_list[count]
    	count += 1
    final_avg_tcp_syn_ack = (sum_of_avgs/count)
    final_min_time_to_syn_ack = min(list_for_calculating_min)
    final_max_time_to_syn_ack = max(list_for_calculating_max)
    #print final_avg_tcp_syn_ack
    #print final_elapsed_time
    std = get_std(list_for_calculating_std)
    #print std
    med = get_median(list_for_calculating_std)
    print "Elapsed Time at the final Point : %.2f sec" % final_elapsed_time
    print "Established TCP Connections at final point: %.2f" % final_established_tcp_conn_per_sec
    print "Average of Average time for TCP Syn/Ack at that point: %.2f msec" % final_avg_tcp_syn_ack
    print "Standard Deviation of Avg time for TCP Syn/Ack list: %.2f msec" %std
    print "Median of Avg time for TCP SYN/ACK list: %.2f msec" %med
    print "Minimum Time for TCP Syn/Ack: %.2f msec" %final_min_time_to_syn_ack
    print "Maximum Time for TCP Syn/Ack: %.2f msec" %final_max_time_to_syn_ack
    #print min_tcp_syn_ack_list
    #print max_tcp_syn_ack_list
    web_page_dict = {
        'title': " Contrail Performance Flow ",
        "graph_image_path": "/Users/soumilk/Downloads/soumil.png",
        "destination_path_for_html_file": "/Users/soumilk/Desktop/code/Performance_Analysis_Tool/perf_flow.html",
        "final_elapsed_time": str(
            final_elapsed_time),
        "established_tcp_connections": str(
            final_established_tcp_conn_per_sec),
        "avg_time_for_tcp_syn_ack": str(
            final_avg_tcp_syn_ack),
        "min_time_for_tcp_syn_ack": str(
        	final_min_time_to_syn_ack),
        "max_time_for_tcp_syn_ack":str(
        	final_max_time_to_syn_ack),
        "standard_deviation_of_response_times": str(
            std),
        "median_of_response_times" : str(
            med)}
    if out_file != '':
        web_page_dict["out_file"] = out_file
    create_html_file(web_page_dict)
    #get_diff(avg_tcp_syn_ack_list, established_tcp_conn_per_sec)



'''
def time_vs_conn_rate_flow_scale_tests():
    get_list_of_elapsed_time()
    get_list_of_number_of_TCP_conn_per_sec()
    get_list_of_avg_time_to_tcp_syn_ack()
    plot_graph(time_list, established_tcp_conn_per_sec, avg_tcp_syn_ack_list)
    # print established_tcp_conn_per_sec
    # print "_____________________"
    # print avg_tcp_syn_ack_list
    res_list = copy.deepcopy(avg_tcp_syn_ack_list)
    total_elements_in_list = len(res_list)
    # print total_elements_in_list
    posn = 0
    starting_pt = 0
    itr = 0
    while (itr < len(res_list)):
        if res_list[itr] < 50:
            starting_pt = res_list[itr]
            itr += 1
        else:
            break
    print starting_pt
    ind = avg_tcp_syn_ack_list.index(starting_pt)
    print "Elapsed Time at the final Point : %.2f sec" % time_list[ind]
    print "Established TCP Connections at final point: %.2f" % established_tcp_conn_per_sec[ind]
    print "Average time for TCP Syn/Ack at that point: %.2f" % avg_tcp_syn_ack_list[ind]
    web_page_dict = {
        'title': " Contrail Performance Flow at Scale",
        "graph_image_path": "/Users/soumilk/Downloads/soumil.png",
        "destination_path_for_html_file": "/Users/soumilk/Desktop/code/Performance_Analysis_Tool/perf_flow_scale.html",
        "final_elapsed_time": str(
            time_list[ind]),
        "established_tcp_connections": str(
            established_tcp_conn_per_sec[ind]),
        "avg_time_for_tcp_syn_ack": str(
            avg_tcp_syn_ack_list[ind])}
    create_html_file(web_page_dict)
    #get_diff(avg_tcp_syn_ack_list, established_tcp_conn_per_sec)
'''


def time_vs_conn_rate_flow_scale_tests(inp_file='', out_file=''):
    get_list_of_elapsed_time(inp_file=inp_file)
    get_list_of_number_of_TCP_conn_per_sec(inp_file=inp_file)
    get_list_of_avg_time_to_tcp_syn_ack(inp_file=inp_file)
    get_list_of_min_time_to_tcp_syn_ack(inp_file=inp_file)
    get_list_of_max_time_to_tcp_syn_ack(inp_file=inp_file)
    get_list_of_concurrent_tcp_connections(inp_file=inp_file)
    plot_graph(time_list, established_tcp_conn_per_sec, avg_tcp_syn_ack_list, concurrent_tcp_connections_list)
    #plot_graph(time_list, established_tcp_conn_per_sec, avg_tcp_syn_ack_list)
    # print established_tcp_conn_per_sec
    # print "_____________________"
    # print avg_tcp_syn_ack_list
    res_list = copy.deepcopy(avg_tcp_syn_ack_list)
    total_elements_in_list = len(res_list)
    # print total_elements_in_list
    posn = 0
    starting_pt = 0
    itr = 0
    while (itr < len(res_list)):
        if res_list[itr] < 50:
            starting_pt = res_list[itr]
            itr += 1
        else:
            break
    #print starting_pt
    ind = avg_tcp_syn_ack_list.index(starting_pt)
    sum_established_tcp = 0
    for i in established_tcp_conn_per_sec:
    	sum_established_tcp += i
    #final_elapsed_time = sum_elapsed_time/len(time_list)
    #print final_elapsed_timez
    sum_avg_tcp = 0
    for i in avg_tcp_syn_ack_list:
    	sum_avg_tcp += i
    final_avg_tcp_syn_ack = sum_avg_tcp/len(avg_tcp_syn_ack_list)
    final_established_tcp_conn_per_sec = sum_established_tcp/len(established_tcp_conn_per_sec)
    count = 0
    #list_for_calculating_min = []
    #list_for_calculating_max = []
    #list_for_calculating_std = []
    #while (count <= ind):
    #    list_for_calculating_min.append(min_tcp_syn_ack_list[count])
    #    list_for_calculating_max.append(max_tcp_syn_ack_list[count])
    #    list_for_calculating_std.append(avg_tcp_syn_ack_list[count])
    #    count += 1
    final_min_time_to_syn_ack = min(min_tcp_syn_ack_list)
    final_max_time_to_syn_ack = max(max_tcp_syn_ack_list)
    std = get_std(avg_tcp_syn_ack_list)
    med = get_median(avg_tcp_syn_ack_list)
    print "Elapsed Time at the final Point : %.2f sec" % time_list[ind]
    #print "Established TCP Connections at final point: %.2f" % established_tcp_conn_per_sec[ind]
    print "Average of Established TCP Connections : %.2f" % final_established_tcp_conn_per_sec
    #print "Average time for TCP Syn/Ack at that point: %.2f msec" % avg_tcp_syn_ack_list[ind]
    print "Average of all the Average times for TCP Syn/Ack : %.2f msec" % final_avg_tcp_syn_ack
    print "Standard Deviation of Average times for TCP SYN/Ack: %.2f msec" %std
    print "Median of Average times for TCP SYN/ACK: %.2f msec" %med
    print "Minimum time for TCP Syn/ACK: %.2f msec" % final_min_time_to_syn_ack
    print "Maximum time for TCP SYN/ACK: %.2f msec" % final_max_time_to_syn_ack
    web_page_dict = {
        'title': " Contrail Performance Flow at Scale",
        "graph_image_path": "/Users/soumilk/Downloads/soumil.png",
        "destination_path_for_html_file": "/Users/soumilk/Desktop/code/Performance_Analysis_Tool/perf_flow_scale.html",
        "final_elapsed_time": str(
            time_list[ind]),
        "established_tcp_connections": str(
            established_tcp_conn_per_sec[ind]),
        "avg_time_for_tcp_syn_ack": str(
            avg_tcp_syn_ack_list[ind]),
        "min_time_for_tcp_syn_ack": str(
        	final_min_time_to_syn_ack),
        "max_time_for_tcp_syn_ack": str(
        	final_max_time_to_syn_ack),
        "median_of_response_times": str(
            med),
        "standard_deviation_of_response_times": str(
            std)}
    if out_file != '':
        web_page_dict["out_file"] = out_file
    create_html_file(web_page_dict)
    #get_diff(avg_tcp_syn_ack_list, established_tcp_conn_per_sec)


def main():
    parser = OptionParser()
    parser.add_option('-f', '--file', help="Input '.csv' file", type="string", dest="input_file")
    parser.add_option('-o', '--output_file', help="Name of the output file name (.html) if you want to customise the file name ", type="string", dest="output_file_name")
    parser.add_option('-j', '--job', help="Job To Run (time_throughput / time_vs_conn_rate_flow_tests / time_vs_conn_rate_flow_scale_tests)", type="string", dest="job")
    (opts, args) = parser.parse_args()
    if opts.input_file == '':
        print "Please Provide an Inupt .csv file"
    if opts.job == "time_throughput":
        time_throughput(inp_file=opts.input_file, out_file=opts.output_file_name)
    elif opts.job == "time_vs_conn_rate_flow_tests":
        time_vs_conn_rate_flow_tests(inp_file=opts.input_file, out_file=opts.output_file_name)
    elif opts.job == "time_vs_conn_rate_flow_scale_tests":
        time_vs_conn_rate_flow_scale_tests(inp_file=opts.input_file, out_file=opts.output_file_name)
    else:
        print "The Job can only be one of these three (time_throughput, time_vs_conn_rate_flow_tests, time_vs_conn_rate_flow_scale_testss)"


main()
'''
# time_vs_conn_rate()
if __name__ == "__main__":
    globals()[sys.argv[2]]()
'''
