from incubator import Incubator
import time
import sys

start_time = int(time.time())
current_time = int(time.time())

# create new Incubator with sensor, switch and target temperature
incubator = Incubator(18, 23, 30)

# run for 10mins and exit, scheduled in cron for every 10mins
while current_time - start_time < 590:
    incubator.monitor(sys.argv[1])
    time.sleep(10)
    current_time = int(time.time())
