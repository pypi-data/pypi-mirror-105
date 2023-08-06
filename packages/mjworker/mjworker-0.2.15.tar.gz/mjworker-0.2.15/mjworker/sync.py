from psutil import pid_exists
import re
import time

from mjworker.variables import sync_pidfile, pid_files
from mjworker.public import write_pid

def check_proc_status(pid_check_list):
    failed_proc = []
    for pid_file in pid_check_list:
        with open(pid_file, 'r') as f:
            pid = int(f.readline())
            # print(pid_file, type(pid), pid)
            f.close()
            if not pid_exists(pid):
                pid_name = re.split('/|\.', pid_file[0])[-2]
                failed_proc.append(pid_name)
    return failed_proc


def sync_status(pid_check_list):
    failed_proc = check_proc_status(pid_check_list)
    if not len(failed_proc):
        print('process check successful')
    else:
        print(failed_proc, 'process check error')

def sync_runner(master_data):
    write_pid(sync_pidfile)
    time.sleep(2)
    while True:
        sync_status(pid_files)
        time.sleep(10)