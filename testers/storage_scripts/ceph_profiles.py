
profiles_tests = {}
profiles_tests['PROF01'] = []
profiles_tests['PROF01'].append('python,fix_ntp.py,fix_ntp.conf')
profiles_tests['PROF01'].append('python,check_cinder_type.py,check_cinder_type.conf')
profiles_tests['PROF01'].append('python,live_migrate.py,live_migrate.conf')

# PROF02 - fab basic test.disks only and journal
profiles_tests['PROF02'] = []
profiles_tests['PROF02'].append('python,fix_ntp.py,fix_ntp.conf')
profiles_tests['PROF02'].append('python,check_cinder_type.py,check_cinder_type.conf')
profiles_tests['PROF02'].append('python,live_migrate.py,live_migrate.conf')

#PROF04 - fab test.ssd-disks,local-disks,nfs and journal
profiles_tests['PROF04'] = []
profiles_tests['PROF04'].append('python,fix_ntp.py,fix_ntp.conf')
profiles_tests['PROF04'].append('python,check_cinder_type.py,check_cinder_type.conf')
profiles_tests['PROF04'].append('python,live_migrate.py,live_migrate.conf')

#PROF05 - fab test.nfs only disks
profiles_tests['PROF05'] = []
profiles_tests['PROF05'].append('python,fix_ntp.py,fix_ntp.conf')
profiles_tests['PROF05'].append('python,check_cinder_type.py,check_cinder_type.conf')
profiles_tests['PROF05'].append('python,live_migrate.py,live_migrate.conf')


#PROF07 - fab test.storage node addition.
profiles_tests['PROF07'] = []
profiles_tests['PROF07'].append('python,fix_ntp.py,fix_ntp.conf')
profiles_tests['PROF07'].append('python,check_cinder_type.py,check_cinder_type.conf')
profiles_tests['PROF07'].append('python,add_storage_node.py,add_storage_node.conf')
profiles_tests['PROF07'].append('python,live_migrate.py,live_migrate.conf')

#PROF08 - fab test.multi-chassis test.
profiles_tests['PROF08'] = []
profiles_tests['PROF08'].append('python,fix_ntp.py,fix_ntp.conf')
profiles_tests['PROF08'].append('python,check_cinder_type.py,check_cinder_type.conf')
profiles_tests['PROF08'].append('python,multi_chassis_test.py,multi_chassis_test.conf')
profiles_tests['PROF08'].append('python,live_migrate.py,live_migrate.conf')
