from incubator import Incubator
import time

start_time = int(time.time())
current_time = int(time.time())

# create new Incubator with sensor, switch and target temperature
incubator = Incubator(18, 23, 30)

# run for 55s and exit, scheduled in cron for every minute
while current_time - start_time < 55:
    incubator.monitor()
    time.sleep(5)
    current_time = int(time.time())
