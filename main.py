from pythonping import ping
from datetime import datetime, timedelta
import time
import csv
import random

internet_ip = '8.8.8.8'
wireless_ip = '192.168.0.1'
append_each = 60000
delay = 500
timeout = 0.1

hosts = [['wireless.csv', '192.168.0.1', timeout], ['google.csv', '8.8.8.8', timeout]]


def check_ping(target, timeout):
    # return not random.randint(1, 100) <= 30
    return "Timed out" not in str(
        ping(timeout=timeout, count=1, target=target, out=None, out_format=None, size=56)._responses[0])


def append_to_csv(status, m, file_name):
    rate = sum(1 for value in status if not value) / len(status)
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([m, '%.4f' % rate, len(status)])


if __name__ == '__main__':
    next_time = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=1)
    next_append = next_time + timedelta(milliseconds=append_each - delay)
    hosts_status = {}
    internet_status = []
    wireless_status = []
    while True:
        if datetime.now() >= next_time:
            next_time = next_time + timedelta(milliseconds=delay)
            for host in hosts:
                if host[0] not in hosts_status.keys():
                    hosts_status[host[0]] = []

                hosts_status[host[0]].append(check_ping(host[1], host[2]))

            if datetime.now() >= next_append:
                time_of_log = next_append.replace(second=0, microsecond=0)
                for entry in hosts_status:
                    append_to_csv(hosts_status[entry], time_of_log, entry)
                hosts_status = {}
                next_append = next_time + timedelta(milliseconds=append_each - delay)
        time.sleep(0.01)
