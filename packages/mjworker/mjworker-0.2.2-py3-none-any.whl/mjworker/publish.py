import time
from  multiprocessing import  current_process

from .variables import pid_files, task_pidfile, sync_pidfile, publish_pidfile
from .public import write_pid

def publish_metrc():
    """
    publish metrics for  monitor
    """
    while True:
        time.sleep(11111111)


def publish_runner(master_data):
    write_pid(current_process().pid, publish_pidfile)
    publish_metrc()