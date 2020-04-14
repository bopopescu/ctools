import sys 
#from beautifultable import BeautifulTable
from tabulate import tabulate
from optparse import OptionParser


def get_all_data_dict(inp_file=''):
	file  = open(inp_file)
	file_string  = ''
	for i in file:
		file_string = file_string + str(i)
	list1 = file_string.split('==================================================================')
	dict_1 = {}
	for i in range(len(list1)):
		dict_1[i] = list1[i].split('\n')
	main_ret_dict = {}
	for i in dict_1:
		#print dict_1[i] 
		#print "_____"
		ret_dict = {}
		list_of_values = []
		name = ''
		for j in dict_1[i]:
			if j == '':
				pass
			else:
				par = j.split(":")
				#print par
				#print len(par)
				if par[0] == 'test_profile':
					ret_dict['test_profile'] = par[1]
				if par[0] == 'encap ':
					ret_dict['encap'] = par[1]
				if par[0] == 'cores ':
					ret_dict['cores'] = par[1]
				if par[0] == 'family':
					ret_dict['family'] = par[1]
				if par[0] == 'instances ':
					ret_dict['instances'] = par[1]
				if par[0] == 'test':
					ret_dict['test'] = par[1]
					name = par[1]
				if len(par) == 1:
					list_of_values.append(par[0])
		if len(ret_dict) != 0:
			ret_dict['titles'] = list_of_values
			working_list = ret_dict['titles']
			#print working_list
			titles_string = working_list.pop(0)
			#print titles_string
			#print working_list
			titiles_list = titles_string.split(',')
			#print titiles_list
			temp_titles_list = []
			for k in titiles_list:
				if '\r' in k:
					ab = k.strip('\r')
					temp_titles_list.append(ab)
				else:
					temp_titles_list.append(k)
			ret_dict["final_titles_list"] = temp_titles_list
			#print temp_titles_list
			val_list = []
			while (len(working_list) != 0):
				temp_string = working_list.pop(0)
				temp_list = temp_string.split(',')
				val_list.append(temp_list)
			ret_dict['list_of_val_list'] = val_list
			main_ret_dict[name] = ret_dict
	return main_ret_dict

def establish_key_value_pair_of_titles_and_vales(dict_1):
	#print dict_1
	ret_dict = {}
	for i in dict_1:
		temp_dict = {}
		name = i
		titles_list = dict_1[i]['final_titles_list']
		for j in titles_list:
			temp_dict[j] = []
		#print titles_list
		#print temp_dict
		list_of_values_list = dict_1[i]['list_of_val_list']
		for k in range (len(list_of_values_list)):
			itr = 0
			while (itr < len(titles_list)):
				temp_dict[(titles_list[itr])].append(list_of_values_list[k][itr])
				itr +=1
		#print temp_dict
		ret_dict[i] = temp_dict
	#print ret_dict
	return ret_dict

def print_latency_table(dict_1):
	#for i in dict_1['final_key_value_pairs']:
	#print dict_1['final_key_value_pairs']['Avg Latency (ns)\r\r']
	name = dict_1['test']
	instances = dict_1['instances']
	encap = dict_1['encap']
	column_name_list = ['Packet Size', 'PPS', 'Throughput (kbps)', 'Average Latency (ns)', 'Max Latency (ns)']
	frame_size_list = dict_1['final_key_value_pairs']['Framesize']
	#print frame_size_list
	pps_list  = dict_1['final_key_value_pairs']['Agg Rx Throughput (fps)']
	#print pps_list
	throughput_list = dict_1['final_key_value_pairs']['Agg Rx Throughput (Kbps)']
	#print throughput_list
	avg_latency_list = dict_1['final_key_value_pairs']['Avg Latency (ns)']
	#print avg_latency_list
	max_latency_list = dict_1['final_key_value_pairs']['Max Latency (ns)']
	intergated_list = []
	#print len(max_latency_list)
	for i in range(len(max_latency_list)):
		temp_list = [] 
		temp_list.append(str(frame_size_list[i]))
		temp_list.append(str(pps_list[i]))
		temp_list.append(str(throughput_list[i]))
		temp_list.append(str(avg_latency_list[i]))
		temp_list.append(str(max_latency_list[i]))
		intergated_list.append(temp_list)
	#print intergated_list
	#print max_latency_list
	print "\n\n"
	print "--> NAME : %s" % name
	print "ENCAP: %s" % encap
	print "NUMBER OF GUEST VIRTUAL MACHINES: %s" % instances
	#table = BeautifulTable()
	#table.column_headers = column_name_list
	#print column_name_list
	#table.append_row()
	#print intergated_list
	#for i in intergated_list:
	#	a_list = i
	#	#print a_list
	#	table.append_row(a_list)
	#print table
	print tabulate(intergated_list, headers=column_name_list)

def print_jitter_table(dict_1):
	#print dict_1['test']
	name = dict_1['test']
	#print name
	instances = dict_1['instances']
	encap = dict_1['encap']
	column_name_list = ['Packet Size', 'PPS', 'Throughput (kbps)', 'Average Jitter (ns)', 'Max Jitter (ns)']
	frame_size_list = dict_1['final_key_value_pairs']['Framesize']
	#print frame_size_list
	pps_list  = dict_1['final_key_value_pairs']['Agg Rx Throughput (fps)']
	#print pps_list
	throughput_list = dict_1['final_key_value_pairs']['Agg Rx Throughput (Kbps)']
	avg_jitter_list = dict_1['final_key_value_pairs']['Avg Delay Variation (ns)']
	#print avg_jitter_list
	max_jitter_list = dict_1['final_key_value_pairs']['Max Delay Variation (ns)']
	intergated_list = []
	for i in range(len(max_jitter_list)):
		temp_list = []
		temp_list.append(str(frame_size_list[i]))
		temp_list.append(str(pps_list[i]))
		temp_list.append(str(throughput_list[i]))
		temp_list.append(str(avg_jitter_list[i]))
		temp_list.append(str(max_jitter_list[i]))
		intergated_list.append(temp_list)
	print "\n\n"
	print "--> Name : %s" % name
	print "ENCAP : %s" % encap
	print "NUMBER OF GUEST VIRTUAL MACHINES: %s" % instances
	print tabulate(intergated_list, headers=column_name_list)




def print_tables(dict_1):
	#print dict_1
	for i in dict_1:
		#print i 
		#print dict_1[i]["test"]
		if 'latency' in dict_1[i]['test']:
			print_latency_table(dict_1[i])
		if 'jitter' in dict_1[i]['test']:
			print_jitter_table(dict_1[i])

def main():
	parser = OptionParser()
	parser.add_option('-f', '--file', help="Input Results file", type="string", dest="input_file")
	(opts, args) = parser.parse_args()
	if opts.input_file == '' :
		print "Please provide input file for parsing"
	dict_1 = get_all_data_dict(inp_file=opts.input_file)
	dict_2 = establish_key_value_pair_of_titles_and_vales(dict_1)
	#print dict_2
	for i in dict_2:
		if i in dict_1:
			dict_1[i]["final_key_value_pairs"] = dict_2[i]
	#print dict_1
	print_tables(dict_1)

main()












