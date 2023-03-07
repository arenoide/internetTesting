from pythonping import ping
from datetime import datetime, timedelta
import time
import csv
import random
import concurrent.futures

internet_ip = '8.8.8.8'
wireless_ip = '192.168.0.1'
append_each = 60000  # In milliseconds
delay = 500  # Delay between checks in milliseconds
timeout = 400  # Request timeout in milliseconds

hosts = [['wireless.csv', '192.168.0.1'], ['google.csv', '8.8.8.8']]
hosts_status = {}


def check_ping(target):
    # return not random.randint(1, 100) <= 30
    return "Timed out" not in str(
        ping(timeout=timeout / 1000, count=1, target=target, out_format=None, size=56, verbose=True)._responses[0])


def append_to_csv(status, m, file_name):
    rate = sum(1 for value in status if not value) / len(status)
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([m, '%.4f' % rate])


def append_results(results):
    i = 0
    for host in hosts:
        if host[0] not in hosts_status.keys():
            hosts_status[host[0]] = []
        hosts_status[host[0]].append(results[i])
        i = i + 1


def parallel_request(hs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_ping, h[1]) for h in hs]

        results = [f.result() for f in futures]

        append_results(results)


if __name__ == '__main__':
    next_time = datetime.now().replace(microsecond=0)
    next_append = next_time.replace(second=0) + timedelta(milliseconds=append_each - delay)

    while True:
        if datetime.now() >= next_time:

            next_time = next_time + timedelta(milliseconds=delay)
            parallel_request(hosts)

            if datetime.now() >= next_append:
                time_of_log = next_append.replace(second=0)
                for entry in hosts_status:
                    append_to_csv(hosts_status[entry], time_of_log, entry)
                hosts_status = {}
                next_append = next_time + timedelta(milliseconds=append_each - delay)
        time.sleep(0.01)
