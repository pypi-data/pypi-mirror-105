import time

from .variables import publish_pidfile
from .public import write_pid

def publish_metrc():
    """
    publish metrics for  monitor
    """
    while True:
        time.sleep(11111111)


def publish_runner(master_data):
    write_pid(publish_pidfile)
    publish_metrc()