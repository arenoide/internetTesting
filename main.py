from pythonping import ping
from datetime import datetime, timedelta
import subprocess
import time
import csv
import random
import sys
import concurrent.futures

append_each = 60000  # In milliseconds
delay = 500  # Delay between checks in milliseconds
timeout = 200  # Request timeout in milliseconds


host = [sys.argv[1], sys.argv[2]]
host_status = []


def check_ping(target):
    # return not random.randint(1, 100) <= 30
    # print(subprocess.check_output(['ping', '8.8.8.8', '-f', '-c', '10']))
    return "Timed out" not in str(
        ping(timeout=timeout / 1000, count=1, target=target, out=None, out_format=None)._responses[0])


def append_to_csv(status, m, file_name):
    rate = sum(1 for value in status if not value) / len(status)
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([m, '%.4f' % rate])


def ping_request():
    result = check_ping(host[0])
    host_status.append(result)


if __name__ == '__main__':
    next_time = datetime.now().replace(microsecond=0)
    next_append = next_time.replace(second=0) + timedelta(milliseconds=append_each - delay)

    while True:
        if datetime.now() >= next_time:

            next_time = next_time + timedelta(milliseconds=delay)
            ping_request()

            if datetime.now() >= next_append:
                time_of_log = next_append.replace(second=0)
                append_to_csv(host_status, time_of_log, host[1])
                host_status = []
                next_append = next_time + timedelta(milliseconds=append_each - delay)
        time.sleep(0.01)
