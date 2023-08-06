import time
from  multiprocessing import Process, current_process
import click
import requests
from urllib import parse

from variables import pid_files, sync_pidfile
from sync import sync_status
from public import write_pid
from publish import publish_runner
from task import task_runner


@click.group()
def cli():
    '''
    This is the monitor agent
    '''

@click.command()
@click.option("--timeout", default=10, help="timeout")
@click.option("--server", required=True, help="Controller infomation")
@click.option("--label", required=True, help="worker unique identification")
@click.option("--tag", multiple=True, help="worker authentication code")
def register(server, label, tag, timeout):
    timestamp = str(round(time.time() * 1000000))
    tags = {}
    for t in tag:
        key = t.split('=', maxsplit=1)[0]
        value = t.split('=', maxsplit=1)[1]
        tags[key] = value
    data = {"sessionId": "", "timestamp": timestamp, "label": label, "tags": tags}
    headers = {"Content-Type": "application/json"}
    url = parse.urljoin(server, "/worker/RegisterWorker")
    try:
        r = requests.post(url=url, json=data, timeout=timeout, headers=headers)
    except Exception as e:
        print(e)
    else:
        if r.status_code != 200:
            print(r)
        print(r.text)

@click.command()
@click.option("--timeout", default=10, help="command timeout")
@click.option("--server", required=True, help="Controller infomation")
@click.option("--workerId", required=True, help="worker unique id")
@click.option("--sessionId", required=True, help="session id")
def run(server, workerid, sessionid, timeout):
    master_data = {"server": server, "workerId": workerid, "sessionId": sessionid, "timeout": timeout}
    task_process = Process(target=task_runner, daemon=True, args=(master_data,))
    publish_process = Process(target=publish_runner, daemon=True, args=(master_data,))
    task_process.start()
    publish_process.start()
    write_pid(current_process().pid, sync_pidfile)
    time.sleep(2)
    while True:
        sync_status(pid_files)
        time.sleep(10)

cli.add_command(register)
cli.add_command(run)

if __name__ == '__main__':
    cli()