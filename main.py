from datetime import datetime, timedelta
import subprocess
import time
import csv
import sys
import re

append_each = 60  # In seconds
count = 200  # Amount of requests done within the append_each time
delay = 1000 * append_each / count
to = str((delay - 20) / 1000).replace('.', ',')
d = str((delay - 10) / 1000).replace('.', ',')
host = [sys.argv[1], sys.argv[2]]
patron = r'(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)'


def is_float(rate):
    try:
        float(rate)
        return True
    except:
        return False


def getValues(text):
    rate = (re.search(r'(\d+(?:[.,]\d+)?)(?=% packet loss,)', str(text))).group(1).replace(",", ".")
    if not is_float(rate) or float(rate) > 1:
        print(text)
    t = re.search(patron, str(text))
    min_ping = t.group(1)
    avg_ping = t.group(2)
    max_ping = t.group(3)
    mdev = t.group(4)
    if not is_float(min_ping) or not is_float(avg_ping) or not is_float(max_ping) or not is_float(mdev):
        print("Non float: " + text)
    return rate, t.group(1), t.group(2), t.group(3), t.group(4)


def ping_values(target):
    try:
        # command = 'ping ' + target + ' -w ' + str(append_each) + ' -W ' + to + ' -i ' + d + ' -q -s 68'
        # a = subprocess.check_output(['sudo', 'bash', '-c', command])
        text = subprocess.check_output(['ping', target, '-c', str(count), '-W', to, '-i', d, '-q', '-s', '68'])
        rate, min_ping, avg_ping, max_ping, mdev = getValues(text)

        return rate, min_ping, avg_ping, max_ping, mdev
    except:
        print("ERROR")
        return 0


def append_to_csv(values, m, file_name):
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([m, values[0], values[1], values[2], values[3], values[4]])


if __name__ == '__main__':
    next_time = datetime.now().replace(microsecond=0, second=0) + timedelta(minutes=1)

    while True:
        if datetime.now() >= next_time:
            append_to_csv(ping_values(host[0]), next_time, host[1])
            next_time = next_time + timedelta(seconds=append_each)
        time.sleep(0.01)
