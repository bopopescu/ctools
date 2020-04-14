from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.84.25.1'
host2 = 'root@10.84.25.2'
host3 = 'root@10.84.25.3'
host4 = 'root@10.84.21.36'
host5 = 'root@10.84.21.37'
host6 = 'root@10.84.21.34'
host7 = 'root@10.84.21.35'
host8 = 'root@10.84.21.32'
host9 = 'root@10.84.21.33'
host10 = 'root@10.84.21.30'
host11 = 'root@10.84.21.31'
host12 = 'root@10.84.21.38'
host13 = 'root@10.84.21.39'
host14 = 'root@10.84.22.9'
host15 = 'root@10.84.22.8'
#host16 = 'root@10.84.22.1'
host17 = 'root@10.84.22.3'
host18 = 'root@10.84.22.2'
host19 = 'root@10.84.22.5'
host20 = 'root@10.84.22.4'
host21 = 'root@10.84.22.7'
host22 = 'root@10.84.22.6'
host23 = 'root@10.84.22.20'
host24 = 'root@10.84.21.18'
host25 = 'root@10.84.21.19'
host26 = 'root@10.84.21.14'
host27 = 'root@10.84.21.15'
host28 = 'root@10.84.21.16'
host29 = 'root@10.84.21.17'
host30 = 'root@10.84.21.10'
host31 = 'root@10.84.21.11'
host32 = 'root@10.84.21.12'
host33 = 'root@10.84.21.13'
host34 = 'root@10.84.23.1'
host35 = 'root@10.84.23.2'
host36 = 'root@10.84.23.3'
host37 = 'root@10.84.23.4'
host38 = 'root@10.84.23.5'
host39 = 'root@10.84.23.6'
host40 = 'root@10.84.23.7'
host41 = 'root@10.84.23.8'
host42 = 'root@10.84.23.9'
host43 = 'root@10.84.25.8'
host44 = 'root@10.84.25.9'
host48 = 'root@10.84.25.6'
host49 = 'root@10.84.25.7'
host50 = 'root@10.84.25.4'
host51 = 'root@10.84.25.5'
host52 = 'root@10.84.23.18'
host53 = 'root@10.84.23.19'
host54 = 'root@10.84.23.12'
host55 = 'root@10.84.23.13'
host56 = 'root@10.84.23.10'
host57 = 'root@10.84.23.11'
host58 = 'root@10.84.23.16'
host59 = 'root@10.84.23.17'
host60 = 'root@10.84.23.14'
host61 = 'root@10.84.23.15'
host67 = 'root@10.84.21.6'
host68 = 'root@10.84.21.7'
host69 = 'root@10.84.21.4'
host70 = 'root@10.84.21.5'
host71 = 'root@10.84.21.2'
host72 = 'root@10.84.21.3'
host73 = 'root@10.84.21.1'
host74 = 'root@10.84.21.8'
host75 = 'root@10.84.21.9'
host76 = 'root@10.84.22.11'
host77 = 'root@10.84.22.10'
host78 = 'root@10.84.22.13'
host79 = 'root@10.84.22.12'
host80 = 'root@10.84.22.15'
host81 = 'root@10.84.22.14'
host82 = 'root@10.84.22.17'
host83 = 'root@10.84.22.16'
host84 = 'root@10.84.22.19'
host85 = 'root@10.84.22.18'
host86 = 'root@10.84.25.32'
host87 = 'root@10.84.25.33'
host90 = 'root@10.84.25.34'
host91 = 'root@10.84.23.20'
host92 = 'root@10.84.21.43'
host93 = 'root@10.84.21.42'
host94 = 'root@10.84.21.40'
host95 = 'root@10.84.21.24'
host96 = 'root@10.84.21.21'
host97 = 'root@10.84.21.20'
host98 = 'root@10.84.21.23'
host99 = 'root@10.84.21.22'
host100 = 'root@10.84.21.29'
host101 = 'root@10.84.21.28'
host104 = 'root@10.84.25.10'
host105 = 'root@10.84.25.11'
host106 = 'root@10.84.25.12'
host107 = 'root@10.84.25.13'
host108 = 'root@10.84.25.14'
host109 = 'root@10.84.25.15'
host110 = 'root@10.84.25.16'
#host111 = 'root@10.84.25.17'
#External routers if any
#for eg. 
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = [('mx1', '10.204.216.253')]
router_asn = 64510
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.64/29"


#Host from which the fab commands are triggered to install and provision
host_build = 'stack@10.84.24.64'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4,host5,host6,host7,host8,host9,host10,host11,host12,host13,host14,host15,host17,host18,host19,host20,host21,host22,host23,host24,host25,host26,host27,host28,host29,host30,host31,host32,host33,host34,host35,host36,host37,host38,host39,host40,host41,host42,host43,host44,host48,host49,host50,host51,host52,host53,host54,host55,host56,host57,host58,host59,host60,host61,host67,host68,host69,host70,host71,host72,host73,host74,host75,host76,host77,host78,host79,host80,host81,host82,host83,host84,host85,host86,host87,host90,host91,host92,host93,host94,host95,host96,host97,host98,host99,host100,host101,host104,host105,host106,host107,host108,host109,host110 ],
    'cfgm': [host1, host2, host3],
    'control': [host1, host2, host3],
    'compute': [host4,host5,host6,host7,host8,host9,host10,host11,host12,host13,host14,host15,host17,host18,host19,host20,host21,host22,host23,host24,host25,host26,host27,host28,host29,host30,host31,host32,host33,host34,host35,host36,host37,host38,host39,host40,host41,host42,host43,host44,host48,host49,host50,host51,host52,host53,host54,host55,host56,host57,host58,host59,host60,host61,host67,host68,host69,host70,host71,host72,host73,host74,host75,host76,host77,host78,host79,host80,host81,host82,host83,host84,host85,host86,host87,host90,host91,host92,host93,host94,host95,host96,host97,host98,host99,host100,host101,host104,host105,host106,host107,host108,host109,host110],
    'collector': [host1, host2, host3],
    'webui': [host1],
    'database': [host1, host2, host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['b5s1', 'b5s2', 'b5s3', 'b1s36', 'b1s37', 'b1s34', 'b1s35', 'b1s32', 'b1s33', 'b1s30', 'b1s31', 'b1s38', 'b1s39', 'b2s9', 'b2s8', 'b2s3', 'b2s2', 'b2s5', 'b2s4', 'b2s7', 'b2s6', 'b2s20', 'b1s18', 'b1s19', 'b1s14', 'b1s15', 'b1s16', 'b1s17', 'b1s10', 'b1s11', 'b1s12', 'b1s13', 'b3s1', 'b3s2', 'b3s3', 'b3s4', 'b3s5', 'b3s6', 'b3s7', 'b3s8', 'b3s9', 'b5s8', 'b5s9', 'b5s6', 'b5s7', 'b5s4', 'b5s5', 'b3s18', 'b3s19', 'b3s12', 'b3s13', 'b3s10', 'b3s11', 'b3s16', 'b3s17', 'b3s14', 'b3s15', 'b1s6', 'b1s7', 'b1s4', 'b1s5', 'b1s2', 'b1s3', 'b1s1', 'b1s8', 'b1s9', 'b2s11', 'b2s10', 'b2s13', 'b2s12', 'b2s15', 'b2s14', 'b2s17', 'b2s16', 'b2s19', 'b2s18', 'b5s32', 'b5s33', 'b5s34', 'b3s20', 'b1s43', 'b1s42', 'b1s40', 'b1s24', 'b1s21', 'b1s20', 'b1s23', 'b1s22', 'b1s29', 'b1s28', 'b5s10', 'b5s11', 'b5s12', 'b5s13', 'b5s14', 'b5s15', 'b5s16']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
host4: 'c0ntrail123',
host5: 'c0ntrail123',
host6: 'c0ntrail123',
host7: 'c0ntrail123',
host8: 'c0ntrail123',
host9: 'c0ntrail123',
host10: 'c0ntrail123',
host11: 'c0ntrail123',
host12: 'c0ntrail123',
host13: 'c0ntrail123',
host14: 'c0ntrail123',
host15: 'c0ntrail123',
#host16: 'c0ntrail123',
host17: 'c0ntrail123',
host18: 'c0ntrail123',
host19: 'c0ntrail123',
host20: 'c0ntrail123',
host21: 'c0ntrail123',
host22: 'c0ntrail123',
host23: 'c0ntrail123',
host24: 'c0ntrail123',
host25: 'c0ntrail123',
host26: 'c0ntrail123',
host27: 'c0ntrail123',
host28: 'c0ntrail123',
host29: 'c0ntrail123',
host30: 'c0ntrail123',
host31: 'c0ntrail123',
host32: 'c0ntrail123',
host33: 'c0ntrail123',
host34: 'c0ntrail123',
host35: 'c0ntrail123',
host36: 'c0ntrail123',
host37: 'c0ntrail123',
host38: 'c0ntrail123',
host39: 'c0ntrail123',
host40: 'c0ntrail123',
host41: 'c0ntrail123',
host42: 'c0ntrail123',
host43: 'c0ntrail123',
host44: 'c0ntrail123',
host48: 'c0ntrail123',
host49: 'c0ntrail123',
host50: 'c0ntrail123',
host51: 'c0ntrail123',
host52: 'c0ntrail123',
host53: 'c0ntrail123',
host54: 'c0ntrail123',
host55: 'c0ntrail123',
host56: 'c0ntrail123',
host57: 'c0ntrail123',
host58: 'c0ntrail123',
host59: 'c0ntrail123',
host60: 'c0ntrail123',
host61: 'c0ntrail123',
host67: 'c0ntrail123',
host68: 'c0ntrail123',
host69: 'c0ntrail123',
host70: 'c0ntrail123',
host71: 'c0ntrail123',
host72: 'c0ntrail123',
host73: 'c0ntrail123',
host74: 'c0ntrail123',
host75: 'c0ntrail123',
host76: 'c0ntrail123',
host77: 'c0ntrail123',
host78: 'c0ntrail123',
host79: 'c0ntrail123',
host80: 'c0ntrail123',
host81: 'c0ntrail123',
host82: 'c0ntrail123',
host83: 'c0ntrail123',
host84: 'c0ntrail123',
host85: 'c0ntrail123',
host86: 'c0ntrail123',
host87: 'c0ntrail123',
host90: 'c0ntrail123',
host91: 'c0ntrail123',
host92: 'c0ntrail123',
host93: 'c0ntrail123',
host94: 'c0ntrail123',
host95: 'c0ntrail123',
host96: 'c0ntrail123',
host97: 'c0ntrail123',
host98: 'c0ntrail123',
host99: 'c0ntrail123',
host100: 'c0ntrail123',
host101: 'c0ntrail123',
host104: 'c0ntrail123',
host105: 'c0ntrail123',
host106: 'c0ntrail123',
host107: 'c0ntrail123',
host108: 'c0ntrail123',
host109: 'c0ntrail123',
host110: 'c0ntrail123',
#host111: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

#To enable multi-tenancy feature
multi_tenancy = False
minimum_diskGB=32
#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.log_scenario='scale Kubernets Sanity'

env.test = {
  'mail_to' : 'vjoshi@juniper.net',
  'webserver_host': '10.204.216.50',
  'webserver_user' : 'bhushana',
  'webserver_password' : 'c0ntrail!23',
  'webserver_log_path' :  '/home/bhushana/Documents/technical/logs',
  'webserver_report_path': '/home/bhushana/Documents/technical/sanity',
  'webroot' : 'Docs/logs',
  'mail_server' :  '10.204.216.49',
  'mail_port' : '25',
  'mail_sender': 'contrailbuild@juniper.net',
}
env.test_repo_dir='/root/vjoshi/contrail-tools/contrail-test'
env.orchestrator='kubernetes'

env.kubernetes = {
'mode' : 'baremetal',
'master': host1,
'slaves': [host4,host5,host6,host7,host8,host9,host10,host11,host12,host13,host14,host15,host17,host18,host19,host20,host21,host22,host23,host24,host25,host26,host27,host28,host29,host30,host31,host32,host33,host34,host35,host36,host37,host38,host39,host40,host41,host42,host43,host44,host48,host49,host50,host51,host52,host53,host54,host55,host56,host57,host58,host59,host60,host61,host67,host68,host69,host70,host71,host72,host73,host74,host75,host76,host77,host78,host79,host80,host81,host82,host83,host84,host85,host86,host87,host90,host91,host92,host93,host94,host95,host96,host97,host98,host99,host100,host101,host104,host105,host106,host107,host108,host109,host110 ]
}
