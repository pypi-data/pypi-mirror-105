from  multiprocessing import current_process


def write_pid(pidfile_path):
    f = open(pidfile_path, 'w')
    f.write(str(current_process().pid))
    f.close()
