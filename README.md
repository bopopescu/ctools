It is a one-stop place where you could setup/reimage/provision/test/run-tempest tests

    git clone git@github.com/vedujoshi/contrail-tools.git
    cd contrail-tools

# Introduction
Using this tool-set, Given a pool of testbeds, we can reserve a testbed from the pool, do our stuff on it, and unreserve it
If all the testbeds in the pool are occupied, it will wait for one of the testbeds to be free before proceeding
The testbed locks are maintained in /cs-shared/test_runs/<testbed_file_name.py>

This is espicially useful in Daily Sanity environments where we can gradually expand the pool of available testbeds and testbed resources can be used efficiently

The testbeds currently used for Daily sanity run are in contrail-tools/testbeds/

# Common step for all tasks
Export your testbed(s) to be used for later tasks. If you have more than one testbed, mention them separated by comma without any spaces in between. 

    cd contrail-tools
    export TOOLS_WS=$PWD
    export AVAILABLE_TESTBEDS=$TOOLS_WS/testbeds/testbed_sanity_nodec21.py

    # PKG_FILE should be path of the install package in /github-build
    export PKG_FILE=/github-build/mainline/2422/ubuntu-12-04/havana/contrail-install-packages_2.0-2422~havana_all.deb 
    # Alternative to PKG_FILE : export the below four variables
    export BUILDID=2422
    export BRANCH
    export DISTRO=centos64_os
    export SKU=havana

# Bringup and Sanity 
By default, testers/reserve_and_run.sh reimages the node, installs packages, runs provisioning scripts, and then runs Regular sanity

Example: 

    bash -x testers/reserve_and_run.sh

The contrail-fabric-utils and contrail-test files are artifacts from the identified build. They are copied to a config node (in $HOME) for provisioning and sanity.
To run the new contrail-test infra scripts in github.com:bhushana/contrail-test, export NEW_TEST_INFRA=1 before running

# Running Tempest (supported on Ubuntu only)
By default, tempest networking tests are not run. It can be enabled by exporting SKIP_TEMPEST=0
The script logs into a config node and runs the tempest tests. 

    export SKIP_TEMPEST=0
    bash -x testers/reserve_and_run.sh

Results will be in tempest/result.xml
Refer to testers/environment.sh to configure incase of separate openstack node and control other parameters. 

# Skipping one or or more tasks
You may sometimes just want to setup your environment and not run any tests. 
Or you may want to keep rerunning tests and not reimage/bringup everytime.
This can be controlled by exporting the below variables. value of 1 enables it and 0 disables it

    export SKIP_SANITY=<0/1>
    export SKIP_TEMPEST=<0/1>
    export SKIP_REIMAGE=<0/1>
    export SKIP_BRINGUP=<0/1>

Take a look at testers/environment.sh for a full list of environment variables which can be controlled

# To Manually run tempest
Below is a sample to manually run tempest on a all-in-one setup using tempest_run.sh 

    git clone https://github.com/Juniper/tempest.git
    export TEMPEST_WS=$PWD/tempest
    bash -x <path to contrail-tools>/testers/tempest/tempest_run.sh 

Send an email to vjoshi@juniper.net or cf-test@juniper.net for any enhancements/queries/issues
