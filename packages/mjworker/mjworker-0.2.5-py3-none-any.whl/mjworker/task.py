import requests
import time
import signal
import subprocess
from queue import Queue
from multiprocessing import  current_process
from threading import Thread
import json
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from .variables import task_pidfile
from .public import write_pid

def post_task_status(hisId, jobState, jobResult, master_data):
    data = {"sessionId": master_data['sessionId'], "timestamp": str(round(time.time()*1000000)),
            "hisId": hisId, "jobState": jobState, "jobResult": jobResult}
    headers = {"Content-Type": "application/json"}
    url = urljoin(master_data["server"], "/worker/PutJobResult")
    try:
        r = requests.post(url=url, json=data, headers=headers)
    except Exception as e:
        print("error alert:", e)
    else:
        response_text = json.loads(str(r.text))
        if response_text["statusCode"] == "00":
            print("update task status successful")
            return 0
        print("post task status failed", r.text)

def get_task(master_data):
    data = {"sessionId": master_data['sessionId'], "timestamp": str(round(time.time()*1000000)), 
            "workerId": master_data['workerId']}
    headers = {"Content-Type": "application/json"}
    url = urljoin(master_data["server"], "/worker/PullJob")
    try:
        r = requests.post(url=url, json=data, headers=headers)
        task = json.loads(str(r.text))
    except Exception as e:
        print("get_task error",e)
    else:
        if task["statusCode"] == "00":
            return r.text
        return False

def task_timeout(func):
    '''
    timeout decorator
    '''
    def wrapper(*args, **kwargs):
        def signal_handle(signum, frame): 
            raise RuntimeError
        try:
            signal.signal(signal.SIGALRM, signal_handle)
            signal.alarm(kwargs['timeout'])
            r = func(*args, **kwargs)
            signal.alarm(0)
        except RuntimeError as e:
            return e
        else:
            return r
    return wrapper


# @task_timeout
def task_consumer(task, master_data):
    try:
        task_dic = json.loads(task)
    except Exception as e:
        print("task_consumer error", e)
    else:
        his_id = task_dic["content"]["his_id"]
        job_content = task_dic["content"]["job_content"]
        r = subprocess.run(job_content, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # print("comand output: ", r.stdout)
        post_task_status(his_id, r.returncode, str(r.stdout), master_data)

def task_producer(queue, master_data):
    while True:
        task = get_task(master_data)
        if not task:
            print("get task failed:", task)
            continue
        print("---入队列: {}".format(task))
        queue.put(task)

def task_runner(master_data):
    print("---------------")
    print("task_runner:", master_data)
    print("---------------")
    write_pid(current_process().pid, task_pidfile)
    queue = Queue(maxsize=0)
    producer = Thread(target=task_producer, args=(queue, master_data))
    producer.start()
    while True:
        task = queue.get()
        print("---出队列: {}".format(task))
        task_consumer(task, master_data)

if __name__ == '__main__':
    master_data = {'server': 'http://172.17.36.204:8000', 'workerId': '7344df70-c1cd-55e7-899c-16de62b79607', 'sessionId': 'bccb4f8c-b2c9-11eb-adba-005056b9fd37', 'timeout': 10}
    task_runner(master_data)