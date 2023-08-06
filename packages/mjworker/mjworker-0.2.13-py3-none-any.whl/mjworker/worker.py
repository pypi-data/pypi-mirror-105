import time
from  multiprocessing import Process
import click
import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from mjworker.variables import sync_pidfile
from mjworker.sync import sync_runner
from mjworker.publish import publish_runner
from mjworker.task import task_runner


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
        key = t.strip().split('=', 1)[0]
        value = t.strip().split('=', 1)[1]
        tags[key] = value
    data = {"sessionId": "", "timestamp": timestamp, "label": label, "tags": tags}
    headers = {"Content-Type": "application/json"}
    url = urljoin(server, "/worker/RegisterWorker")
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
    sync_process = Process(target=sync_runner, daemon=True, args=(master_data,))
    task_process.start()
    publish_process.start()
    sync_process.start()
    sync_process.join()
    publish_process.join()
    publish_process.join()

cli.add_command(register)
cli.add_command(run)

if __name__ == '__main__':
    cli()