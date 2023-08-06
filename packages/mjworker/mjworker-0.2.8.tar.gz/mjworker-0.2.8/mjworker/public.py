import time
def write_pid(pid, pidfile_path):
    f = open(pidfile_path, 'w')
    f.write(str(pid))
    f.close()
