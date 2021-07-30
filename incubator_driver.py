from incubator import Incubator
import time
import sys
import os
import signal

try:
    with open("/home/pi/Documents/healthmind/incubator_last_pid.tmp", "r") as f:
        pid = f.read()
    os.kill(int(pid), signal.SIGTERM)
except Exception as e:
    print(e)
    pass

with open("/home/pi/Documents/healthmind/incubator_last_pid.tmp", "w+") as f:
    f.write(str(os.getpid()))


start_time = int(time.time())
current_time = int(time.time())

# create new Incubator with sensor, switch and target temperature
incubator = Incubator(sensor_gpio=21,
                      heater_gpio=20,
                      target_temperature=27,
                      update_time=5,
                      email_notify_hours=list(range(0, 24)))


# run for 10mins and exit, scheduled in cron for every 10mins
while current_time - start_time < 86400 - incubator.update_time:
    incubator.monitor(sys.argv[1], sys.argv[2])
    time.sleep(incubator.update_time)
    current_time = int(time.time())
