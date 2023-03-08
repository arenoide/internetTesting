from datetime import datetime, timedelta
import subprocess
import time
import csv
import sys
import re

append_each = 60  # In seconds
delay = 300  # Delay between checks in milliseconds
timeout = 300  # Request timeout in milliseconds
host = [sys.argv[1], sys.argv[2]]


def ping_rate(target):
    try:
        to = str(timeout / 1000).replace('.', ',')
        d = str(delay / 1000).replace('.', ',')
        # command = 'ping ' + target + ' -w ' + str(append_each) + ' -W ' + to + ' -i ' + d + ' -q -s 68'
        # a = subprocess.check_output(['sudo', 'bash', '-c', command])
        a = subprocess.check_output(['ping', target, '-w', str(append_each), '-W', to, '-i', d, '-q', '-s', '68'])
        rate = (re.search(r'(\d+(?:[.,]\d+)?)(?=% packet loss,)', str(a))).group(1).replace(",", ".")
        if not rate.isnumeric() or int(rate) > 1:
            print(a)
        return rate
    except:
        print("ERROR")
        return 0


def append_to_csv(rate, m, file_name):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([m, rate])


if __name__ == '__main__':
    next_time = datetime.now().replace(microsecond=0, second=0) + timedelta(minutes=1)

    while True:
        if datetime.now() >= next_time:
            append_to_csv(ping_rate(host[0]), next_time, host[1])
            next_time = next_time + timedelta(seconds=append_each)
        time.sleep(0.01)
