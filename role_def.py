import itertools
import copy
import re
import sys 
import os 
import errno 
import json 

# print """ 
# ARGS = ["""+repr (sys.argv)+"""] 
# """ 

if ( len (sys.argv)!=3 ): 
    print """ 
    Two runtime arguments are mandary. Not more not less. 
    Argument count found currently = ["""+str (len (sys.argv) - 1)+"""] 

    Format, 
        python """+sys.argv[ 0 ]+""" filter_name testbed_file_name 
    """ 
    exit ( 1 ) 


try: 
    with open(sys.argv[2]) as f:  lines = f.read().splitlines() 
except IOError: 
    print """ 
    Testbed file not found. 
    """+sys.argv[ 2 ]+""" 
    """ 
    exit ( 1 ); 



role_list   = [
    "cfgm",
    "database",
    "collector",
    "control",
    "openstack",
    "webui"
]

host_count  = 3
compute_host_upper_index = 6 

MIN_ROLE_COUNT_IN_ONE_HOST  = 3
# MAX_PER_FILTER  = 6 
MAX_PER_FILTER__MAP = { 
    "exclusive"     : 6,
    "inclusive"     : 6,
    "subset"        : 6, 
    "HA_openstack"  : 6, 
    "HA_contrail"   : 6, 
    # "HA_Contrail"   : 3, 
} 


def format_dump ( dataset = {} ): 
    output = """ { """ 
    for role in dataset: 
        # output += "\n" 
        host_string = "" 
        for host in dataset[ role ]: 
            host_string += host + ", " 
        output += """ 
    '"""+role+"' : ["+host_string+"], " 
    output += """ 
} 
""" 
    return output 

def testbed_roledef ( dataset = {}, unique_tag = None ): 
    if dataset and unique_tag: 
        content = "" 
 	
        dataset.update ( { 
            "all" : [ "host"+str (x) for x in range ( 1, compute_host_upper_index+1) ], 
            "compute" : [ "host"+str (x) for x in range ( host_count+1, compute_host_upper_index+1) ], 
            "build"   : [ "host_build" ], 
        } ) 
        #print format_dump ( dataset ) 

        # if ( filter_name == "HA_openstack" or filter_name == "HA_contrail" ):
        #     with open('testbed_sample_HA.py') as f:  lines = f.read().splitlines()
        # else:
        #     with open('testbed_sample.py') as f:  lines = f.read().splitlines() 
        with open(sys.argv[2]) as f:  lines = f.read().splitlines()

        prepend_dir_part = "" 
        if filter_runtime_arg__found: 
            try: 
                os.makedirs ( sys.argv[1] ) 
            except OSError as exception: 
                if exception.errno!=errno.EEXIST: 
                    raise 
            prepend_dir_part = sys.argv[1]+"/" 

        # with open(sys.argv[1]+'/testbed_sample_'+unique_tag+'.py', 'w') as f: 
        # with open(prepend_dir_part+'testbed_sample_'+unique_tag+'.py', 'w') as f: 
        with open(prepend_dir_part+'testbed_'+unique_tag+'.py', 'w') as f: 
            for line in lines: 
                if ( re.search (r"^\s*\{\s*env_roledefs\s*\}\s*$", line ) ): 
                    #print line.format ( 
                    #    env_roledefs = "env.roledefs = "+format_dump ( dataset ) 
                    #) 
                    line = line.format ( 
                        env_roledefs = "env.roledefs = "+format_dump ( dataset ) 
                    ) 
                #if ( re.search (r"^\s*\{\s*log_scenario\s*\}\s*$", line ) ):
                searchExp = "Multi-Node Virtual Testbed Sanity"
                replaceExp = "Multi-Node Virtual "+unique_tag+" Testbed Sanity" 
                if searchExp in line:
                    line = line.replace(searchExp,replaceExp)
                f.write(line+"\n") 


def check_min_member_count ( input_list ):
    return True if len (input_list)>1 else False

def HA_openstack_filter (input_list):
    cfgm_found     = False
    database_found = False
    openstack_found = False 

    role_count  = 0

    for item in xrange( len( input_list ) ):
        if ( input_list[item] == "cfgm" ):
            cfgm_found    = True
        if (input_list[ item ] == "database") :
            database_found    = True
        if ( input_list[item] == "openstack" ):
            openstack_found   = True 
        role_count  += 1
    if ( (not cfgm_found) or (not database_found) or (not openstack_found) ): 
        return False

    if ( role_count<MIN_ROLE_COUNT_IN_ONE_HOST):
        return  False

    return check_min_member_count (input_list)

# def HA_Contrail_filter (input_list):
#     cfgm_found     = False
#     database_found = False
# 
#     role_count  = 0
# 
#     for item in xrange( len( input_list ) ):
#         if ( input_list[item] == "cfgm" ):
#             cfgm_found    = True
#         if (input_list[ item ] == "database") :
#             database_found    = True
#         role_count  += 1
#     if ( (not cfgm_found) or (not database_found) ): 
#         return False
# 
#     if ( role_count<MIN_ROLE_COUNT_IN_ONE_HOST):
#         return  False
# 
#     return check_min_member_count (input_list)

def exclusive_filter (input_list):
    cfgm_found    = False
    database_found        = False

    role_count  = 0

    for item in xrange( len( input_list ) ):
        if ( input_list[item] == "cfgm" ):
            cfgm_found    = True
        if (input_list[ item ] == "database") :
            database_found    = True
        if ( cfgm_found and database_found ):
            return False
        role_count  += 1

    if ( role_count<MIN_ROLE_COUNT_IN_ONE_HOST):
        return  False

    return check_min_member_count (input_list)
    # return True

def inclusive_filter (input_list):
    # print "input_list = [" + repr( input_list ) + "] "

    cfgm_found    = False
    database_found = False

    role_count  = 0

    for item in xrange( len( input_list ) ):
        if (input_list[ item ] == "cfgm"):
            cfgm_found    = True
        if (input_list[ item ] == "database") :
            database_found    = True
        role_count += 1

    if ( ( not cfgm_found ) or ( not database_found) ):
        return False

    if (role_count < MIN_ROLE_COUNT_IN_ONE_HOST) :
        return False

    return check_min_member_count( input_list )
    # return True

def subset_filter (input_list):

    # print "input_list = ["+repr (input_list)+"] "

    cfgm_found    = False
    database_found        = False

    role_count  = 0

    for item in xrange ( len(input_list) ) :
        if (input_list[ item ] == "cfgm") :
            cfgm_found    = True
        if (input_list[ item ] == "database") :
            database_found    = True
        role_count += 1

    if ( cfgm_found and ( not database_found ) ) :
        return False

    if (role_count < MIN_ROLE_COUNT_IN_ONE_HOST) :
        return False

    return check_min_member_count( input_list )
    # return True

# def odd_count_filter ( input_list ):
def count_filter( input_list = [], filter_name = "" ) :
    # print "input_list = [" + repr( input_list ) + "] "
    # print "input_list = [" + repr( list (input_list) ) + "] "

    cfgm_count    = 0
    database_count        = 0
    openstack_count = 0

    for item in xrange( len( input_list ) ) :
        if (input_list[ item ] == "cfgm") :
            cfgm_count += 1
        if (input_list[ item ] == "database") :
            database_count += 1
        if ( input_list[item] == "openstack" ):
            openstack_count += 1 

    # print "database_count = [" + str( database_count ) + "] cfgm_count = [" + str( cfgm_count ) + "] "

    # Number of "database"s should be an odd number.
    if (database_count % 2 == 0) :
        # print "False | database_count % 2 == 0 "
        return False

    #if ( filter_name == "inclusive" ):
        #if ( input_list[item] == "openstack" ):
        #   openstack_count += 1

    if ( filter_name != "HA_openstack" ):
        if (openstack_count > 2) :
            return False

    if ( filter_name == "subset" ):
        # print "database_count = ["+str(database_count)+"] cfgm_count = ["+str (cfgm_count)+"] "
        # Number of "database"s should be >= 3.
        if (database_count < 3) :
            # print "False | database_count < 3"
            return False

        # Number of "databases" should be > Number of "cfgm"s.
        if ( database_count<=cfgm_count ):
            # print "False | database_count<=cfgm_count "
            return False

        # Number of "cfgm"s should be >= 2.
        if ( cfgm_count < 2 ):
            # print "False | cfgm_count < 2 "
            return False


    # print "    True "
    return True




def check_all_present ( input_list ):
    # print "check_all_present"
    # print input_list
    input_list_set = list ( set( input_list ) )
    # print input_list_set
    # hash = [ { input_list_set[k], ""} for k in xrange ( len (input_list_set) ) ]
    hash    = {}
    for k in xrange( len( input_list_set ) ):
        hash[ input_list_set[k] ]   = ""
    # print hash
    # exit ()
    for item in role_list:
        try:
            if ( hash[item] ):
                pass
        except KeyError:
            return False
    return True


def is_collector_in_all ( input_list ):
    # print "input_list x = ["+repr (input_list)+"] "
    collector_count     = 0
    for i in xrange ( len ( input_list) ):
        # print "input_list[i] = ["+repr (input_list[i])+"] "
        if ( "collector" in input_list[i] ):
            collector_count     += 1
            if ( collector_count == host_count ):
                # print "return True "
                return True
    # print "return False "
    return False

def is_openstack_on_odd_number_of_hosts ( input_list ):
    # print "input_list x = ["+repr (input_list)+"] "
    openstack_count     = 0
    for i in xrange ( len ( input_list) ):
        # print "input_list[i] = ["+repr (input_list[i])+"] "
        if ( "openstack" in input_list[i] ):
            openstack_count     += 1
    if ( openstack_count%2==0 ):
    	return False
    return True


# if check_all_present ( ['cfgm', 'r3', 'cfgm', 'r4', 'cfgm', 'r5', "database"] ):
#     print "True"
# else:
#     print "False"
# exit ()


superset_filter_list     = {
    "exclusive"     : exclusive_filter,
    "inclusive"     : inclusive_filter,
    "subset"        : subset_filter, 
    "HA_openstack"  : HA_openstack_filter, 
    "HA_contrail"   : inclusive_filter, 
} 

if ( sys.argv[ 1 ] not in superset_filter_list ): 
    print """ 
    Filter Name is not recognized. 
    """+sys.argv[ 1 ]+""" 
    """ 
    exit ( 1 ) 

filter_runtime_arg__found = False 
try: 
    filter_list = { 
        sys.argv[1] : superset_filter_list[ sys.argv[1] ], 
    } 
    filter_runtime_arg__found = True 
except (KeyError, IndexError): 
    filter_list     = {
        "exclusive"     : exclusive_filter,
        "inclusive"     : inclusive_filter,
        "subset"        : subset_filter, 
    	"HA_openstack"  : HA_openstack_filter, 
        "HA_contrail"   : inclusive_filter, 
    }
#     print """ Runtime parameter having one of below values should be provided. 
# exclusive 
# inclusive 
# subset 
# """ 
#     exit ( 1 ) 
# filter_list     = {
#     "exclusive"     : exclusive_filter,
#     "inclusive"     : inclusive_filter,
#     "subset"        : subset_filter
# }


def return_specific_values ( master_list, this_filter_name ): 
    indices_to_pick = MAX_PER_FILTER__MAP[ this_filter_name ] 
    # print "indices_to_pick = ["+repr (indices_to_pick)+"] " 
    master_list_length = len (master_list) 
    # print "master_list_length = ["+repr (master_list_length)+"] " 
    index_list = (lambda indices_to_pick, master_list_length: [i*master_list_length//indices_to_pick + master_list_length//(2*indices_to_pick) for i in range(indices_to_pick)])( indices_to_pick, master_list_length ) 

    selected_item_list = [] 
    for this_index in index_list: 
        selected_item_list.append ( copy.deepcopy (master_list[ this_index ]) )
    #import pdb;pdb.set_trace() 
    print "selected_item_list = ["+repr (selected_item_list)+"] " 
    print "selected_item_list = ["+json.dumps ( selected_item_list, sort_keys=True, indent=4 )+"] " 
    #outer_key_list    = len (selected_item_list)
    #print "outer_key_list = [" + repr( outer_key_list ) + "] "
    #for i in xrange ( outer_key_list ) :
    #    inner_key_list = len(selected_item_list[i])
    #    #inner_key_list = len (selected_item_list [outer_key_list][i].keys( ))
    #    print "inner_key_list = [" + repr( inner_key_list ) + "] "
    return selected_item_list 


all_combinations_list   = []
for r in xrange ( 1, len (role_list)+1 ):
    all_combinations_this_r     = []
    all_combinations_this_r     = list ( itertools.combinations ( role_list, r ) )
    all_combinations_list.extend ( [ list (x) for x in all_combinations_this_r ] )

# print all_combinations_list

for filter_name in filter_list:
    # print "\nFilter = ["+filter_name+"] "
    this_host_filtered_list = list( itertools.ifilter( lambda x : filter_list[ filter_name ]( x ), all_combinations_list ) )
    # print "\nList matching this filter = [" + repr( this_host_filtered_list ) + "]"
    all_combinations_across_given_hosts     = list( itertools.combinations( this_host_filtered_list, host_count ) )
    filtered_list   = list( itertools.ifilter( lambda x : count_filter ( input_list= list (itertools.chain.from_iterable (x) ), filter_name=filter_name), all_combinations_across_given_hosts ) )
    # print "\nFinal List for this filter = ["+repr (filtered_list)+"]"

    filtered_list_final     = []
    for i in xrange( len( filtered_list ) ) :
        if check_all_present ( list (itertools.chain.from_iterable (filtered_list[i]) ) ):
            #if not is_collector_in_all ( list (filtered_list[i]) ):
            if is_openstack_on_odd_number_of_hosts ( list (filtered_list[i]) ): 
                    # filtered_list_final.append ( filtered_list[i]  )
                    # x = filtered_list[ i ].deepcopy ()
                filtered_list_final.append( copy.deepcopy ( filtered_list[ i ] ) )

    print "\n\n\n\n"
    # for i in xrange ( len (filtered_list_final) ):
    #     print filter_name + "| " + repr( list( filtered_list_final[ i ] ) )

    # for i in xrange( len( filtered_list_final ) ) :
    #     print "Filter = ["+filter_name+"] "
    #     for j in xrange ( len ( list (filtered_list_final[i]) ) ):
    #         print "N"+str (j+1)+" = " + repr ( filtered_list_final[i][j] )



    # print "filtered_list_final = ["+repr (filtered_list_final)+"] " 
    selected_item_list = return_specific_values ( 
        master_list = filtered_list_final, 
        this_filter_name = filter_name, 
    ) 


    testbed = {} 
    print "Filter = [" + filter_name + "] "
    for i in xrange (len (selected_item_list)):
        outer_key_list = list (selected_item_list[i])
        #print "outer_key_list = [" + repr( outer_key_list ) + "] "
        print "SET [" + str( i + 1 ) + "] "
        
        for j in xrange (len (outer_key_list) ):      
            inner_key_list = outer_key_list[j]
            #print "inner_key_list = [" + repr( inner_key_list ) + "] "
            print "host"+str (j+1)+" = " + repr ( selected_item_list[i] [j] )
                
            for y in range ( len ( selected_item_list[i] [j] ) ):
                    role_item = selected_item_list[i] [j] [y]
                    host_name = "host"+str (j+1)
                    try:
                        testbed[ role_item ].append ( host_name )
                    except KeyError:
                        testbed[ role_item ]        = [ host_name ]

        testbed_roledef( dataset = testbed, unique_tag = filter_name + str (i) )
        testbed.clear()

    #exit ()





import pprint 
# print "testbed = ["+pprint.pprint (testbed)+"] " 


