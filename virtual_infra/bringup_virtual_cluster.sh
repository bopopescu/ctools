#!/usr/bin/env bash
source ./virtual_infra/virtual_infra_utils.sh
launch_virtual_testbed
provision_cluster_wrapper
teardown_virtual_testbed
