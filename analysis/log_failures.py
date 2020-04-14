#--------------------------------------------------------------------
# Tool to generate summary info of all test job results for a build
# 
# To be run on the webserver (ex: mayamruga) which hosts the reports/results
# Argument : Path to folder which has the report_details files for a build 
#            Ex: Documents/technical/sanity/daily/R2.0/2.01-37/
#--------------------------------------------------------------------
import glob
import ConfigParser
from lxml import etree as ET
import pprint
import sys
#path='Documents/technical/sanity/daily/R2.0/2.01-37/'
path = sys.argv[1]



reports = glob.glob('%s/report_details*.ini' % (path))
failure_dict = {}
test_summary_dict = {}

for report_file in reports:
    config = ConfigParser.ConfigParser()
    config.read(report_file)
    logs_path = config.get('Test', 'logslocation')
    build =  config.get('Test', 'build')
    timestamp =  config.get('Test', 'timestamp')
    distro_sku =  config.get('Test', 'distro_sku')
    if not build or not timestamp:
        continue
    test_data_path = 'Documents/technical/logs/%s_%s/' % (build, timestamp)
    total_tc_count = 0
    passed_tc_count = 0
    failed_tc_count = 0 
    error_tc_count = 0 
    skip_tc_count = 0
    #result_files = ['result.xml']
    result_files = glob.glob('%s/result*.xml' % (test_data_path))
    for result_file in result_files:
        doc = ET.parse(result_file)        
        root = doc.getroot()
        tc_count = int(root.get('tests') or 0)
        failed = int(root.get('failures') or 0)
        error_count = int(root.get('errors') or 0)
        skip_count = int(root.get('skipped') or 0)

        total_tc_count += tc_count
        failed_tc_count += failed
        error_tc_count += error_count
        skip_tc_count += skip_count
        passed_tc_count += tc_count - failed - error_count - skip_count
        try:
            tests = doc.xpath("/testsuite/testcase")
            for test in tests:
                if test.xpath('failure'):
                    test_name = test.get('name')
                    if test_name in failure_dict.keys():
                        failure_dict[test_name].append(distro_sku)
                    else:
                        failure_dict[test_name] = [distro_sku]
        except Exception,e:
            print e
        test_summary_dict[distro_sku] = {} 
        test_summary_dict[distro_sku]['tests'] = total_tc_count
        test_summary_dict[distro_sku]['failures'] = failed_tc_count
        test_summary_dict[distro_sku]['errors'] = error_tc_count
        test_summary_dict[distro_sku]['skipped'] = skip_tc_count
        test_summary_dict[distro_sku]['passed'] = passed_tc_count
   
    # Print summary
print "SUMMARY : "
print "========="
print "{:<50} {:<10} {:<10} {:<10} {:<10} {:<10}".format('Scenario',
    'Tests','Passed','Failed','Errors','Skipped')
for key in test_summary_dict.keys():
    scenario = key
    tests = test_summary_dict[key]['tests']
    passed = test_summary_dict[key]['passed']
    failed = test_summary_dict[key]['failures']
    errors = test_summary_dict[key]['errors']
    skipped = test_summary_dict[key]['skipped']
    print "{:<50} {:<10} {:<10} {:<10} {:<10} {:<10}".format(scenario, 
        tests, passed, failed, errors, skipped)
print ""

# print the failure details
print "FAILED TESTS : "
print "=============="
for k,v in failure_dict.iteritems():
    print k,": "
    for distro_sku in v:
        print "\t%s" % (distro_sku)
    print ""


