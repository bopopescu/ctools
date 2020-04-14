# Jenkins sometimes terminates the job even before cleanup is run
LOCK_FILE_DIR=/cs-shared/testbed_locks

function remove_lock_file() {
    rm -f ${LOCK_FILE_DIR}/lockfile1
    return 0
}

echo "Current active jobs: "

lockfile ${LOCK_FILE_DIR}/lockfile1
tb_lock_file=`grep -l "Occupied! .*$BUILD_TAG" $LOCK_FILE_DIR/*.py` || \
            echo "No testbed found for unlocking"
if [[ ! -s $tb_lock_file ]]; then
   remove_lock_file
   exit 0
fi
if ! grep -xq "Testbed locked..Unlock when debug complete" $tb_lock_file ; then
   sed -i "/Occupied! .*$BUILD_TAG/d" $tb_lock_file
else
   echo "Testbed $tb_lock_file is locked for debug..."
fi
cat $tb_lock_file
remove_lock_file

