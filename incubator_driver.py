from incubator import Incubator
import time
import sys

start_time = int(time.time())
current_time = int(time.time())

# create new Incubator with sensor, switch and target temperature
incubator = Incubator(21, 20, 30, 10, list(range(0, 24)))


# run for 10mins and exit, scheduled in cron for every 10mins
while current_time - start_time < 86400 - incubator.update_time:
    incubator.monitor(sys.argv[1], sys.argv[2])
    time.sleep(incubator.update_time)
    current_time = int(time.time())
