from psutil import pid_exists
import re
import time

from mjworker.variables import sync_pidfile, pid_files
from mjworker.public import write_pid

def check_process_status(pid_check_list):
    failed_process = []
    for pid_file in pid_check_list:
        with open(pid_file, 'r') as f:
            pid = int(f.readline())
            # print(pid_file, type(pid), pid)
            f.close()
            if not pid_exists(pid):
                pid_name = re.split('/|\.', pid_file[0])[-2]
                failed_process.append(pid_name)
    return failed_process


def sync_status(pid_check_list):
    failed_process = check_process_status(pid_check_list)
    if not len(failed_process):
        print('process check successful')
    else:
        print(failed_process, 'process check error')

def sync_runner(master_data):
    write_pid(sync_pidfile)
    time.sleep(2)
    while True:
        sync_status(pid_files)
        time.sleep(10)