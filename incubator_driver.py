from incubator import Incubator
from project_utils import kill_previous_from_file
import time
import sys

kill_previous_from_file("/home/pi/Documents/healthmind/incubator_last_pid.tmp")

# create new Incubator with sensor, switch and target temperature
incubator = Incubator(sensor_gpio=21,
                      heater_gpio=20,
                      target_temperature=27,
                      update_time=5,
                      email_notify_hours=list(range(0, 24)))

while True:
    incubator.monitor(sys.argv[1], sys.argv[2])
    time.sleep(incubator.update_time)
