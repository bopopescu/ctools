
import itertools
import copy
import re
import sys 
import os 
import errno 
import json 
import random 
import time 
import shutil


if ( len (sys.argv)!=2 ): 
    print """ 
    Two runtime arguments are mandary. Not more not less. 
    Argument count found currently = ["""+str (len (sys.argv) - 1)+"""] 

    Format, 
        python """+sys.argv[ 0 ]+""" testbed_file_name 
    """ 
    exit ( 1 ) 


try: 
    with open(sys.argv[1]) as f:  lines = f.read().splitlines() 
except IOError: 
    print """ 
    Testbed file not found. 
    """+sys.argv[ 1 ]+""" 
    """ 
    exit ( 1 ); 

role_list   = [
    "contrail-analyticsdb",
    "contrail-analytics",
    "contrail-controller",
    "openstack",
]


dir_name = "set_files" 
compute_host_upper_index = 6 
host_count  = 3
COUNT_TO_PICK = 5 

fixed_role_list = [ 
    ["contrail-lb"], 
    ["contrail-compute"], 
    ["contrail-compute"], 
] 

    
def get_role_combination_list (role_list=None): 
    if role_list is None: 
        return [] 
    all_combinations_list   = []
    for r in range ( 1, len (role_list)+1 ):
        all_combinations_this_r     = []
        all_combinations_this_r     = list ( itertools.combinations ( role_list, r ) )
        all_combinations_list.extend ( [ list (x) for x in all_combinations_this_r ] )
    return all_combinations_list 


def get_host_role_list__dynamic (combination_list=None, host_count=None): 
    if (combination_list is None or host_count is None): 
        return [] 
    host_role_list = list ( itertools.combinations ( combination_list, host_count ) ) 
    return host_role_list 

def add_fixed_role_host_list (host_role_list=None, fixed_role_list=None): 
    if (host_role_list is None or fixed_role_list is None): 
        return [] 
    for i in range (len (host_role_list)): 
        host_role_list[ i ] = list (host_role_list[ i ]) 
        host_role_list[ i ].extend ( fixed_role_list ) 
    return host_role_list 

def one_or_three_filter (host_role_list=None, role_name=None): 
    if host_role_list is None: 
        return [] 
    if role_name is None: 
        return host_role_list 
    new_role_host_list = [] 
    for i in range (len (host_role_list)): 
        # host_role_list[ i ] = list (host_role_list[ i ]) 
        role_count = get_role_count ( host_role_list=host_role_list[ i ], role_name=role_name ) 
        # print "role_count = ["+repr (role_count)+"] " 
        if ( role_count==1 or role_count==3 ): 
            new_role_host_list.append ( host_role_list[ i ] ) 
    return new_role_host_list 

def one_filter (host_role_list=None, role_name=None): 
    if host_role_list is None: 
        return [] 
    if role_name is None: 
        return host_role_list 
    new_role_host_list = [] 
    for i in range (len (host_role_list)): 
        # host_role_list[ i ] = list (host_role_list[ i ]) 
        role_count = get_role_count ( host_role_list=host_role_list[ i ], role_name=role_name ) 
        # print "role_count = ["+repr (role_count)+"] " 
        if ( role_count==1 ): 
            new_role_host_list.append ( host_role_list[ i ] ) 
    return new_role_host_list 

def get_role_count ( host_role_list=None, role_name=None ): 
    if host_role_list is None: 
        return 0 
    if role_name is None: 
        return 0 
    role_count = 0 
    for i in range (len (host_role_list)): 
        for j in range ( len (host_role_list[ i ]) ): 
            if ( host_role_list[ i ][ j ]==role_name ): 
                role_count = role_count + 1 
    return role_count 

def print_role_list (host_role_list=[]): 
    try: 
        shutil.rmtree( dir_name )
    except Exception: 
        print "Not deleting directory as it is not found. " 

    for i in range (len (host_role_list)): 
        set_name = "SET"+repr (i) 
        print ("\n\nSET"+repr (i)) 
        c = 0 
        testbed = {} 
        for j in range ( len (host_role_list[ i ]) ): 
            # print ("\nH"+str (c+1)+" = ", end="") 
            a = "H"+str (c+1)+" = " 
            for k in range ( len (host_role_list[ i ][ j ]) ): 
                if k==0: 
                    # print (repr (host_role_list[ i ][ j ][ k ]), end="") 
                    a = a + repr (host_role_list[ i ][ j ][ k ]) 
                else: 
                    # print (", "+repr (host_role_list[ i ][ j ][ k ]), end="") 
                    a = a + ", " + repr (host_role_list[ i ][ j ][ k ]) 

                role_item = host_role_list[ i ][ j ][ k ] 
                host_name = "host"+str (j+1)
                try:
                    testbed[ role_item ].append ( host_name )
                except KeyError:
                    testbed[ role_item ] = [ host_name ]

            print a 
            c = c + 1 


        testbed_roledef( dataset = testbed, unique_tag=set_name ) 
        testbed.clear() 


def format_dump ( dataset = {} ): 
    output = """ { """ 
    for role in dataset: 
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
            "build"   : [ "host_build" ], 
        } ) 

        with open(sys.argv[1]) as f:  lines = f.read().splitlines()

        prepend_dir_part = "" 
        try: 
            os.makedirs ( dir_name ) 
        except OSError as exception: 
            if exception.errno!=errno.EEXIST: 
                raise 
        prepend_dir_part = dir_name +"/" 

        with open(prepend_dir_part+'testbed_'+unique_tag+'.py', 'w') as f: 
            for line in lines: 
                if ( re.search (r"^\s*\{\s*env_roledefs\s*\}\s*$", line ) ): 
                    line = line.format ( 
                        env_roledefs = "env.roledefs = "+format_dump ( dataset ) 
                    ) 
                f.write(line+"\n")


def get_combination_list (): 
    combination_list = get_role_combination_list (role_list=role_list) 
    # print "combination_list = ["+json.dumps ( combination_list, sort_keys=True, indent=4 )+"] " 
    
    host_role_list = get_host_role_list__dynamic (combination_list=combination_list, host_count=host_count ) 
    # print "host_role_list = ["+json.dumps ( host_role_list, sort_keys=True, indent=4 )+"] " 
    
    
    role_list_dynamic_fixed = add_fixed_role_host_list (host_role_list=host_role_list, fixed_role_list=fixed_role_list) 
    # print "role_list_dynamic_fixed = ["+json.dumps ( role_list_dynamic_fixed, sort_keys=True, indent=4 )+"] " 
    
    
    role_list_final = one_or_three_filter (host_role_list=role_list_dynamic_fixed, role_name="contrail-analyticsdb") 
    # print "role_list_final = ["+json.dumps ( role_list_final, sort_keys=True, indent=4 )+"] " 
    
    role_list_final = one_filter (host_role_list=role_list_final, role_name="openstack") 
    # print "role_list_final = ["+json.dumps ( role_list_final, sort_keys=True, indent=4 )+"] " 
    
    picked_list = random.sample (role_list_final, COUNT_TO_PICK) 
    # print "picked_list = ["+json.dumps ( picked_list, sort_keys=True, indent=4 )+"] " 

    print_role_list (host_role_list=picked_list) 

    return picked_list 

get_combination_list () 


